"""
Text Generation Routes
=======================
Endpoints for LinkedIn post text generation.
"""

import logging
import time

from fastapi import APIRouter, HTTPException, status

from ..config import settings
from ..providers import TextGenerationRequest, ProviderError
from ..prompts import get_linkedin_text_prompt
from ..services import session_manager, usage_logger
from ..services.prompt_logger import get_prompt_logger
from .provider_factory import get_text_provider
from .schemas import (
    TextGenerationRequestSchema,
    TextGenerationResponseSchema,
    ImageRecommendationSchema,
    ImageStrategySchema,
    ImagePromptSchema,
    ImageFingerprintSchema,
    InfographicTextStructureSchema,
    InfographicSectionSchema,
    ErrorResponse,
)


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Text Generation"])
prompt_logger = get_prompt_logger()


@router.post(
    "/generate-text",
    response_model=TextGenerationResponseSchema,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def generate_text(request: TextGenerationRequestSchema):
    """
    Generate LinkedIn post text with image prompts.

    Returns EVERYTHING in one call:
    - post_text: LinkedIn-ready text with Unicode formatting + emojis
    - hashtags: 3-5 separate hashtags (not in post body)
    - image_strategy: Recommended image count and reason
    - image_prompts: ALWAYS generated (user decides to use)
    - image_fingerprint: Visual consistency params
    """
    start_time = time.time()

    try:
        # Get provider
        provider = get_text_provider(request.text_model.provider)

        # Build generation request
        # Convert enum to string value (handles both enum instances and strings)
        post_length_str = request.post_length.value if hasattr(request.post_length, 'value') else str(request.post_length)
        tone_str = request.tone.value if hasattr(request.tone, 'value') else str(request.tone)
        cta_style_str = request.cta_style.value if hasattr(request.cta_style, 'value') else str(request.cta_style)

        gen_request = TextGenerationRequest(
            idea=request.idea,
            post_angle=request.post_angle,
            draft_post=request.draft_post,
            post_length=post_length_str,
            tone=tone_str,
            audience=request.audience,
            cta_style=cta_style_str,
            session_id=request.session_id,  # For pipeline step logging
        )

        # Use appropriate prompt based on text provider
        # Ollama (Mistral/Llama) needs simpler, more explicit prompts
        # Bedrock (Claude) can handle complex prompts
        provider_to_model = {
            "nova": "nova",
            "titan": "titan",
            "sdxl": "sdxl"
        }
        image_model_name = provider_to_model.get(request.image_model.provider.value, "nova")

        # Choose prompt based on text provider
        text_provider_str = request.text_model.provider.value if hasattr(request.text_model.provider, 'value') else str(request.text_model.provider)
        if text_provider_str == "ollama":
            # Ollama now uses 3-step pipeline internally
            # System prompt is for logging only - pipeline uses its own prompts
            system_prompt = "[OLLAMA PIPELINE - Uses internal 3-step prompts for 95%+ success]"
        else:
            # Full prompts for Claude (Bedrock)
            system_prompt = get_linkedin_text_prompt(
                image_model=image_model_name,
                generate_images=request.generate_images
            )

        # Log the prompt being sent
        prompt_logger.log_text_generation(
            session_id=request.session_id,
            provider=request.text_model.provider.value,
            model=request.text_model.model,
            system_prompt=system_prompt,
            user_input={
                "idea": request.idea,
                "post_angle": request.post_angle,
                "draft_post": request.draft_post,
                "post_length": post_length_str,
                "tone": tone_str,
                "audience": request.audience,
                "cta_style": cta_style_str,
            },
        )

        # Generate
        result = await provider.generate(
            request=gen_request,
            model=request.text_model.model,
            system_prompt=system_prompt,
            max_tokens=settings.max_text_output_tokens,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Log the response
        prompt_logger.log_text_generation(
            session_id=request.session_id,
            provider=request.text_model.provider.value,
            model=request.text_model.model,
            system_prompt="[SAME AS ABOVE]",
            user_input={"idea": request.idea[:100] + "..."},
            response={
                "post_text_preview": result.post_text[:200] + "..." if len(result.post_text) > 200 else result.post_text,
                "short_post": result.short_post,
                "hashtags": result.hashtags,
                "image_count": result.image_strategy.get("image_count") if isinstance(result.image_strategy, dict) else None,
                "tokens_used": result.tokens_used,
            },
        )

        # Store in session (for image generation)
        session_manager.update(
            session_id=request.session_id,
            post_text=result.post_text,
            short_post=result.short_post,
            hashtags=result.hashtags,
            image_recommendation=result.image_recommendation,
            image_strategy=result.image_strategy if result.image_strategy else None,
            image_prompts=[p.model_dump() for p in result.image_prompts] if result.image_prompts else [],
            image_fingerprint=result.image_fingerprint.model_dump() if result.image_fingerprint else None,
            # Store infographic_text to avoid second LLM call during rendering
            infographic_text=result.infographic_text.model_dump() if result.infographic_text else None,
            tone=tone_str,
            audience=request.audience,
            text_model_used=result.model_used,
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

        # Build response
        # Convert infographic_text if present
        infographic_text_schema = None
        if result.infographic_text:
            sections = [
                InfographicSectionSchema(title=s.title, bullets=s.bullets)
                for s in result.infographic_text.sections
            ]
            infographic_text_schema = InfographicTextStructureSchema(
                title=result.infographic_text.title,
                subtitle=result.infographic_text.subtitle,
                sections=sections,
                takeaway=result.infographic_text.takeaway,
            )

        return TextGenerationResponseSchema(
            post_text=result.post_text,
            short_post=result.short_post,
            hashtags=result.hashtags,
            image_recommendation=ImageRecommendationSchema(**result.image_recommendation) if result.image_recommendation else None,
            image_strategy=ImageStrategySchema(**result.image_strategy) if result.image_strategy else None,
            image_prompts=[
                ImagePromptSchema(**p.model_dump()) for p in result.image_prompts
            ] if result.image_prompts else [],
            image_fingerprint=ImageFingerprintSchema(**result.image_fingerprint.model_dump()) if result.image_fingerprint else None,
            infographic_text=infographic_text_schema,  # Pre-extracted for infographic rendering
            session_id=request.session_id,
            model_used=result.model_used,
            image_model_used=image_model_name if request.generate_images else "none",
            tokens_used=result.tokens_used,
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
        elapsed_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Unexpected error in text generation: {str(e)}", exc_info=True)

        usage_logger.log_text_generation(
            session_id=request.session_id,
            provider=request.text_model.provider.value if hasattr(request, 'text_model') else "unknown",
            model=request.text_model.model if hasattr(request, 'text_model') else "unknown",
            duration_ms=elapsed_ms,
            success=False,
            error_message=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )

