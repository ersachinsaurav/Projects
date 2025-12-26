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
from ..services import session_manager, usage_logger, ImageProcessor, PostCardBuilder, PostCardStyle
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
    tone = session.tone if session and session.tone else "professional"
    audience = session.audience if session and session.audience else ["founders", "engineers"]

    try:
        provider = get_text_provider(request.text_model.provider)

        gen_request = ImagePromptGenerationRequest(
            post_text=post_text,
            image_count=image_count,
            tone=tone,
            audience=audience,
        )

        system_prompt = get_image_prompt_generation_prompt()

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

    post_text = session.post_text if session else ""

    # Enforce image limit
    if len(image_prompts) > settings.max_images_per_request:
        image_prompts = image_prompts[:settings.max_images_per_request]

    try:
        provider = get_image_provider(request.image_model.provider)

        gen_request = ImageGenerationRequest(
            prompts=image_prompts,
            fingerprint=fingerprint,
            post_text=post_text,
        )

        # Log the prompts
        prompt_logger.log_image_generation(
            session_id=request.session_id,
            provider=request.image_model.provider.value,
            model=request.image_model.model,
            prompts=[{
                "id": p.id,
                "concept": p.concept,
                "prompt": p.prompt,
                "style_notes": p.style_notes,
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
        processor = ImageProcessor()
        processed = processor.process_images(
            images=[{
                "id": img.id,
                "base64_data": img.base64_data,
                "prompt_used": img.prompt_used,
                "concept": getattr(img, "concept", ""),
                "format": img.format,
                "width": img.width,
                "height": img.height,
            } for img in result.images],
            add_footer=True,
            create_pdf=len(result.images) > 1,
        )

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

