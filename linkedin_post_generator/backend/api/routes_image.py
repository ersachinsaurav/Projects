"""
Image Generation Routes
========================
Endpoints for image generation and post cards.
"""

import logging
import time

from fastapi import APIRouter, HTTPException, status

from ..config import settings
from ..providers import (
    ImagePromptGenerationRequest,
    ImageGenerationRequest,
    ImagePrompt,
    ImageFingerprint,
    ProviderError,
)
from ..prompts import get_image_prompt_generation_prompt
from ..prompts.image_gen import get_image_prompt, PromptContext
from ..services import session_manager, usage_logger, ImageProcessor, PostCardBuilder, PostCardStyle, InfographicRenderer, CarouselBuilder
from ..services.prompt_logger import get_prompt_logger
from .provider_factory import get_text_provider, get_image_provider
from .schemas import (
    ImagePromptRequestSchema,
    ImagePromptResponseSchema,
    ImagePromptSchema,
    ImageFingerprintSchema,
    ImageGenerationRequestSchema,
    ImageGenerationResponseSchema,
    GeneratedImageSchema,
    PostCardGenerationRequestSchema,
    PostCardGenerationResponseSchema,
    ErrorResponse,
)


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Image Generation"])
prompt_logger = get_prompt_logger()


@router.post(
    "/generate-image-prompts",
    response_model=ImagePromptResponseSchema,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def generate_image_prompts(request: ImagePromptRequestSchema):
    """
    Generate image prompts grounded in finalized post text (Phase 2).

    This endpoint:
    1. Takes the finalized post text (from session or request)
    2. Generates image prompts that are SPECIFIC to this post
    3. Ensures footer-safe compositions

    Must be called AFTER /generate-text.
    """
    start_time = time.time()

    # Get session data
    session = session_manager.get(request.session_id)

    # Get post text
    post_text = request.post_text
    if not post_text:
        if session and session.post_text:
            post_text = session.post_text
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No post text available. Call /generate-text first or provide post_text.",
            )

    # Get image count
    image_count = request.image_count
    if not image_count:
        if session and session.image_strategy:
            image_count = session.image_strategy.get("image_count", 1)
        else:
            image_count = 1

    # Validate image count
    if image_count < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="image_count must be at least 1",
        )
    if image_count > settings.max_images_per_request:
        image_count = settings.max_images_per_request

    # Get tone and audience from session
    from ..utils.constants import DEFAULT_TONE, DEFAULT_AUDIENCES
    tone = session.tone if session and session.tone else DEFAULT_TONE.value
    audience = session.audience if session and session.audience else list(DEFAULT_AUDIENCES)

    try:
        provider = get_text_provider(request.text_model.provider)

        gen_request = ImagePromptGenerationRequest(
            post_text=post_text,
            image_count=image_count,
            tone=tone,
            audience=audience,
        )

        # Get image model for prompt generation
        provider_to_model = {
            "nova": "nova",
            "titan": "titan",
            "sdxl": "sdxl"
        }
        image_model_name = provider_to_model.get(request.image_model.provider.value, "nova")
        system_prompt = get_image_prompt_generation_prompt(image_model=image_model_name)

        result = await provider.generate_image_prompts(
            request=gen_request,
            model=request.text_model.model,
            system_prompt=system_prompt,
            max_tokens=2000,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Store in session
        session_manager.update(
            session_id=request.session_id,
            image_prompts=[p.model_dump() for p in result.image_prompts],
            image_fingerprint=result.image_fingerprint.model_dump(),
        )

        # Log usage
        usage_logger.log_text_generation(
            session_id=request.session_id,
            provider=request.text_model.provider.value,
            model=request.text_model.model,
            tokens_used=result.tokens_used,
            duration_ms=elapsed_ms,
            success=True,
        )

        return ImagePromptResponseSchema(
            image_prompts=[
                ImagePromptSchema(**p.model_dump()) for p in result.image_prompts
            ],
            image_fingerprint=ImageFingerprintSchema(**result.image_fingerprint.model_dump()),
            session_id=request.session_id,
            post_text_used=post_text,
            model_used=result.model_used,
            generation_time_ms=elapsed_ms,
        )

    except ProviderError as e:
        elapsed_ms = int((time.time() - start_time) * 1000)

        usage_logger.log_text_generation(
            session_id=request.session_id,
            provider=request.text_model.provider.value,
            model=request.text_model.model,
            duration_ms=elapsed_ms,
            success=False,
            error_message=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/generate-images",
    response_model=ImageGenerationResponseSchema,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def generate_images(request: ImageGenerationRequestSchema):
    """
    Generate actual images (Phase 3).

    This endpoint:
    1. Uses image prompts from session or request
    2. Calls the image generation model
    3. Applies footer overlay to images
    4. Creates PDF if multiple images

    Must be called AFTER /generate-image-prompts.
    """
    start_time = time.time()

    session = session_manager.get(request.session_id)

    # Determine image prompts
    if request.image_prompts:
        image_prompts = [
            ImagePrompt(
                id=p.id,
                concept=p.concept,
                prompt=p.prompt,
                style_notes=p.style_notes,
                composition_note=p.composition_note,
                negative_prompt=getattr(p, 'negative_prompt', None),
            )
            for p in request.image_prompts
        ]
    elif session and session.image_prompts:
        try:
            image_prompts = [
                ImagePrompt(
                    id=p.get("id", idx),
                    concept=p.get("concept", ""),
                    prompt=p.get("prompt", ""),
                    style_notes=p.get("style_notes", ""),
                    composition_note=p.get("composition_note", ""),
                    negative_prompt=p.get("negative_prompt", None),
                )
                for idx, p in enumerate(session.image_prompts, start=1)
                if isinstance(p, dict) and p.get("prompt")
            ]
            if not image_prompts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No valid image prompts in session data.",
                )
        except (TypeError, ValueError, KeyError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image prompt data in session: {str(e)}",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image prompts available. Call /generate-image-prompts first.",
        )

    # Determine fingerprint
    if request.image_fingerprint:
        fingerprint = ImageFingerprint(**request.image_fingerprint.model_dump())
    elif session and session.image_fingerprint:
        fingerprint = ImageFingerprint(**session.image_fingerprint)
    else:
        fingerprint = ImageFingerprint(
            visual_style="minimal",
            color_palette="neutral",
            composition="top-weighted",
            lighting="soft",
            concept_type="abstract",
        )

    # Get post_text and short_post from session (stored during text generation)
    post_text = session.post_text if session else ""
    short_post = session.short_post if session else None

    # Enforce image limit
    # If carousel mode, only generate 1 AI image (cover)
    if request.generate_carousel:
        image_prompts = image_prompts[:1]  # Only first image for carousel cover

        if image_prompts:
            prompt_data = image_prompts[0]
            original_prompt = prompt_data.prompt or ""
            style_notes = prompt_data.style_notes or ""

            # USE CLAUDE'S PROMPT DIRECTLY - only enhance with carousel-specific requirements
            # Claude should already generate SDXL-optimized prompts with the updated system prompt

            # Check if Claude's prompt already has the right format (SDXL-style)
            has_sdxl_format = any(kw in original_prompt.lower() for kw in [
                "flat editorial", "editorial illustration", "pastel color palette",
                "composition is top-weighted", "vector-like", "soft gradients"
            ])

            if has_sdxl_format:
                # Claude already generated a good SDXL prompt - use it with minor enhancements
                logger.info("Using Claude's SDXL-optimized prompt directly")

                # Ensure bottom space requirement is explicit
                if "bottom 30%" not in original_prompt.lower() and "bottom 30 percent" not in original_prompt.lower():
                    # Add layout requirement
                    enhanced_prompt = (
                        f"{original_prompt}, "
                        f"single unified scene NOT a collage, "
                        f"character in upper 70% of frame, "
                        f"bottom 30% is empty solid pastel background for text overlay"
                    )
                    prompt_data.prompt = enhanced_prompt
                # else use as-is

                logger.info(f"Using Claude's carousel prompt: {prompt_data.prompt[:250]}...")
            else:
                # Claude's prompt doesn't follow SDXL format - use modular fallback
                logger.warning("Claude's prompt not in SDXL format, using modular fallback")

                from ..prompts.image_gen.base import PromptContext

                prompt_context = PromptContext(
                    concept=prompt_data.concept,
                    style_notes=style_notes,
                    color_palette=fingerprint.color_palette if fingerprint else None,
                    visual_style=fingerprint.visual_style if fingerprint else None,
                    leave_space_bottom=True,
                    bottom_space_percent=30,
                )

                model_name = request.image_model.model.lower()
                prompt_result = get_image_prompt(
                    usecase="carousel",
                    model=model_name,
                    context=prompt_context.__dict__,
                )

                prompt_data.prompt = prompt_result["prompt"]
                if prompt_result.get("negative_prompt") and not prompt_data.negative_prompt:
                    prompt_data.negative_prompt = prompt_result["negative_prompt"]

                logger.info(f"Built carousel prompt using fallback: {prompt_data.prompt[:250]}...")

            # Ensure negative prompt exists for SDXL
            if request.image_model.model.lower() == "sdxl" and not prompt_data.negative_prompt:
                prompt_data.negative_prompt = (
                    "text, words, letters, typography, captions, headlines, labels, logos, watermark, signature, "
                    "collage, grid, multiple panels, split image, tiled, mosaic, diptych, triptych, "
                    "blurry, low resolution, noisy, oversaturated, harsh lighting, dark shadows, "
                    "cluttered layout, busy background, photorealistic, 3D render, stock photo look, "
                    "distorted anatomy, extra limbs, missing limbs"
                )
    elif len(image_prompts) > settings.max_images_per_request:
        image_prompts = image_prompts[:settings.max_images_per_request]

    try:
        provider = get_image_provider(request.image_model.provider)

        # For carousel, request 512x768 portrait images (width x height)
        # This gives us more space for title and footer at bottom
        carousel_width = 512 if request.generate_carousel else None
        carousel_height = 768 if request.generate_carousel else None

        gen_request = ImageGenerationRequest(
            prompts=image_prompts,
            fingerprint=fingerprint,
            post_text=post_text,
            width=carousel_width,
            height=carousel_height,
        )

        # Log the prompts (including negative_prompt for SDXL)
        prompt_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            prompts=[{
                "id": p.id,
                "concept": p.concept,
                "prompt": p.prompt,
                "style_notes": p.style_notes,
                "negative_prompt": p.negative_prompt,  # SDXL-specific
            } for p in gen_request.prompts],
            fingerprint=gen_request.fingerprint.model_dump(),
        )

        result = await provider.generate(
            request=gen_request,
            model=request.image_model.model,
        )

        # Log the response
        prompt_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            prompts=[{
                "id": img.id,
                "concept": getattr(img, "concept", ""),
                "prompt": img.prompt_used[:100] + "..." if len(img.prompt_used) > 100 else img.prompt_used,
            } for img in result.images],
            fingerprint=gen_request.fingerprint.model_dump(),
            response={
                "image_count": len(result.images),
                "success": True,
            },
        )

        # Process images
        # Check if we should use infographic renderer (SDXL + infographic style)
        # DO NOT apply infographic overlay for carousel - carousel has its own cover renderer
        # Apply overlay if:
        # 1. NOT generating carousel
        # 2. Using SDXL image model
        # 3. Session exists
        # 4. Either infographic_text is available OR recommended_type suggests infographic style
        use_infographic_overlay = (
            not request.generate_carousel and  # Skip overlay for carousel
            request.image_model.provider.value == "sdxl" and
            session and
            (
                # If infographic_text exists, use it (model generated structured text for overlays)
                (session.infographic_text is not None) or
                # OR if recommended_type suggests infographic style
                (
                    session.image_recommendation and
                    session.image_recommendation.get("recommended_type") in [
                        "infographic",
                        "cartoon_narrative",
                        "cartoon_abstract",  # Also include cartoon_abstract (used by Sonnet)
                        "abstract_minimal"    # Also include abstract_minimal
                    ]
                )
            )
        )

        # Create a mapping from image ID to prompt concept for filename generation
        prompt_concept_map = {p.id: p.concept for p in image_prompts}

        processed_images = []
        for img in result.images:
            img_data = img.base64_data

            # Apply infographic text overlay if needed
            if use_infographic_overlay and post_text:
                try:
                    renderer = InfographicRenderer()

                    # Use infographic_text from session (stored during text generation)
                    # Fallback to simple extraction if not available
                    text_structure = None
                    if session and session.infographic_text:
                        # Use cached infographic text from session (no LLM call!)
                        text_structure = session.infographic_text
                        logger.info(f"Using pre-extracted infographic_text from session. Model: {session.text_model_used}")

                        # Ensure sections are properly formatted (list of dicts)
                        if isinstance(text_structure, dict):
                            sections = text_structure.get("sections", [])
                            # Convert InfographicSection objects to dicts if needed
                            if sections and isinstance(sections[0], dict):
                                # Already dicts, good
                                pass
                            else:
                                # Convert Pydantic models to dicts
                                text_structure["sections"] = [
                                    sec.model_dump() if hasattr(sec, "model_dump") else sec
                                    for sec in sections
                                ]
                    else:
                        # Fallback: simple extraction without LLM
                        logger.warning(f"No infographic_text in session. Using simple extraction fallback. Session: {session is not None}, Model: {session.text_model_used if session else 'N/A'}")
                        text_structure = renderer._simple_extract_text(
                            post_text=post_text,
                            short_post=short_post,
                        )

                    # Validate text_structure before rendering
                    if not text_structure or not isinstance(text_structure, dict):
                        raise ValueError(f"Invalid text_structure format: {type(text_structure)}")

                    # Extract and validate sections
                    sections = text_structure.get("sections", [])
                    if sections and not isinstance(sections[0], dict):
                        logger.warning(f"Sections format issue: {type(sections[0]) if sections else 'empty'}. Converting...")
                        sections = [
                            {"title": sec.get("title", ""), "bullets": sec.get("bullets", [])}
                            if isinstance(sec, dict) else
                            {"title": getattr(sec, "title", ""), "bullets": getattr(sec, "bullets", [])}
                            for sec in sections
                        ]
                        text_structure["sections"] = sections

                    # Apply infographic overlay with layout selection (Step 3)
                    # Default to "infographic" layout, can be made configurable
                    layout = "infographic"  # Options: "infographic", "checklist", "quote", "comparison"
                    img_data = renderer.render_infographic(
                        base_image_base64=img_data,
                        title=text_structure.get("title") or "Key Insight",
                        subtitle=text_structure.get("subtitle"),
                        sections=text_structure.get("sections", []),
                        takeaway=text_structure.get("takeaway"),
                        add_footer=True,  # Footer is included in infographic renderer
                        layout=layout,
                    )
                    logger.info(f"Applied infographic overlay to image {img.id} with layout {layout}. Title: {text_structure.get('title')}, Sections: {len(text_structure.get('sections', []))}")
                except Exception as e:
                    logger.error(f"Failed to apply infographic overlay: {e}", exc_info=True)
                    # Fall through to standard processing

            # Get concept from prompt map (fallback to empty string)
            concept = prompt_concept_map.get(img.id, "")

            # Debug logging
            logger.debug(f"Image {img.id}: concept='{concept}', prompt_used length={len(img.prompt_used)}")

            processed_images.append({
                "id": img.id,
                "base64_data": img_data,
                "prompt_used": img.prompt_used,
                "concept": concept,
                "format": img.format,
                "width": img.width,
                "height": img.height,
            })

        # Check if carousel generation is requested
        if request.generate_carousel and processed_images and session:
            # Carousel mode: AI cover + post card sections
            try:
                carousel_builder = CarouselBuilder()

                # Get infographic_text from session
                infographic_text = session.infographic_text or {}
                if not isinstance(infographic_text, dict):
                    # Convert if needed
                    if hasattr(infographic_text, 'model_dump'):
                        infographic_text = infographic_text.model_dump()
                    else:
                        infographic_text = {}

                # Use first AI image as cover
                ai_cover = processed_images[0]["base64_data"]

                # Build carousel: cover + post cards
                carousel_images_base64 = carousel_builder.build_carousel(
                    ai_cover_image_base64=ai_cover,
                    infographic_text=infographic_text,
                    post_text=post_text or "",
                    short_post=short_post,
                )

                # Convert carousel images to processed_images format
                # Carousel uses 512x768 (width x height) for better content layout
                carousel_processed = []
                for idx, img_b64 in enumerate(carousel_images_base64):
                    carousel_processed.append({
                        "id": idx + 1,
                        "base64_data": img_b64,
                        "prompt_used": f"Carousel slide {idx + 1}",
                        "concept": "carousel-cover" if idx == 0 else f"carousel-section-{idx}",
                        "format": "png",
                        "width": 512,   # Fixed carousel width
                        "height": 768,  # Fixed carousel height (portrait)
                    })

                processed_images = carousel_processed
                logger.info(f"Generated carousel with {len(carousel_processed)} slides")

                # Carousel images already have footers - skip to PDF creation only
                processed = {"images": processed_images}
                if len(processed_images) > 1:
                    processor = ImageProcessor()
                    pdf_images = [img["base64_data"] for img in processed_images if img["base64_data"]]
                    if pdf_images:
                        # Priority order for PDF filename (same as image filenames):
                        # 1. infographic_text.title (if present)
                        # 2. First line of post_text (if title not present)
                        # 3. Fallback: linkedin-carousel
                        pdf_filename_text = None

                        # Priority 1: Use infographic title if available
                        if infographic_text.get('title'):
                            pdf_filename_text = infographic_text.get('title')
                        # Priority 2: Use first line of post_text if title not present
                        elif post_text:
                            first_line = post_text.split('\n')[0].strip() if post_text else None
                            if first_line:
                                pdf_filename_text = first_line

                        # Sanitize filename: SEO-friendly kebab-case (hyphens separate words)
                        if pdf_filename_text:
                            import re
                            sanitized = re.sub(r'[^\w\s]', '', pdf_filename_text)  # Remove special chars
                            sanitized = re.sub(r'\s+', '-', sanitized)  # Replace spaces with hyphens
                            sanitized = sanitized.lower().strip()
                            pdf_filename = f"{sanitized}.pdf" if sanitized else "linkedin-carousel.pdf"
                        else:
                            pdf_filename = "linkedin-carousel.pdf"

                        # Use original title for PDF metadata, sanitized for filename
                        carousel_title = infographic_text.get('title', 'LinkedIn Carousel')
                        processed["pdf_base64"] = processor.merge_to_pdf(pdf_images, title=carousel_title)
                        processed["pdf_title"] = pdf_filename

            except Exception as e:
                logger.error(f"Failed to generate carousel: {e}", exc_info=True)
                # Fall back to regular processing
                logger.warning("Falling back to regular image processing")
                processed = None  # Flag to use standard processing

        # Apply standard processing (footer, PDF) - but NOT for carousel (already processed above)
        if request.generate_carousel and 'processed' in dir() and processed is not None:
            # Carousel already processed above, skip standard processing
            pass
        elif not use_infographic_overlay:
            processor = ImageProcessor()
            processed = processor.process_images(
                images=processed_images,
                add_footer=True,
                create_pdf=len(processed_images) > 1,
            )
        else:
            # Infographic renderer already added footer, just create PDF if needed
            processed = {"images": processed_images}
            if len(processed_images) > 1:
                processor = ImageProcessor()
                pdf_images = [img["base64_data"] for img in processed_images if img["base64_data"]]
                if pdf_images:
                    processed["pdf_base64"] = processor.merge_to_pdf(pdf_images)

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Update session
        session_manager.update(
            session_id=request.session_id,
            generated_images=[img for img in processed["images"]],
            pdf_data=processed.get("pdf_base64"),
            image_model_used=result.model_used,
        )

        # Log usage
        usage_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            image_count=len(result.images),
            duration_ms=elapsed_ms,
            success=True,
        )

        return ImageGenerationResponseSchema(
            images=[GeneratedImageSchema(**img) for img in processed["images"]],
            pdf_base64=processed.get("pdf_base64"),
            pdf_title=processed.get("pdf_title"),
            session_id=request.session_id,
            model_used=result.model_used,
            image_count=len(result.images),
            generation_time_ms=elapsed_ms,
        )

    except ProviderError as e:
        elapsed_ms = int((time.time() - start_time) * 1000)

        usage_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            image_count=0,
            duration_ms=elapsed_ms,
            success=False,
            error_message=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Unexpected error in image generation: {str(e)}", exc_info=True)

        usage_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            image_count=0,
            duration_ms=elapsed_ms,
            success=False,
            error_message=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/generate-post-card",
    response_model=PostCardGenerationResponseSchema,
    summary="Generate Post Card Image",
    description="""
    Creates a social media style post card image (like Twitter/X posts).
    Pure code generation - no AI needed!

    Features:
    - Dark or light theme
    - Profile picture (rounded)
    - Name and verified badge
    - Post text with nice typography

    Perfect for sharing text-heavy content as images.
    """
)
async def generate_post_card(request: PostCardGenerationRequestSchema):
    """Generate a post card image."""
    start_time = time.time()

    try:
        style = PostCardStyle(
            theme=request.theme,
            name=request.name,
            handle=request.handle,
            verified=request.verified,
        )

        builder = PostCardBuilder(style)
        post_card_base64, calculated_height = builder.build(
            post_text=request.post_text,
            avatar_base64=request.avatar_base64,
            short_post=request.short_post,
        )

        generation_time = int((time.time() - start_time) * 1000)

        return PostCardGenerationResponseSchema(
            post_card_base64=post_card_base64,
            format="png",
            width=1080,
            height=calculated_height,
            session_id=request.session_id,
            theme=request.theme,
            generation_time_ms=generation_time,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate post card: {str(e)}",
        )

