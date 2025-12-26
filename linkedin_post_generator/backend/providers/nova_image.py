"""
Amazon Nova Canvas Image Provider
===================================
Optimized for LinkedIn infographic-style illustrations.

Nova Canvas Best Practices:
- Supports longer prompts (up to 1024 chars)
- Better at understanding natural language descriptions
- Produces higher quality, more artistic images
- Strong negative prompt support

Optimized for:
- Professional infographic style illustrations
- Clean, modern design aesthetic
- Top-weighted composition (content in upper 85%)
- Minimal, abstract, symbolic visuals
"""

import base64
import json
import time
import logging
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from ..config import settings
from .base import (
    ImageModelProvider,
    ImageGenerationRequest,
    ImageGenerationResponse,
    GeneratedImage,
    ProviderError,
)

logger = logging.getLogger(__name__)


# Nova Canvas specific prompt templates
NOVA_SYSTEM_STYLE = """Professional infographic illustration style,
clean modern design, soft pastel colors with subtle gradients,
cute cartoon style with friendly rounded characters if people needed,
tech-forward aesthetic, educational visual,
high quality digital illustration, crisp lines, professional look"""

NOVA_COMPOSITION = """Composition rules: All important visual elements must be
in the upper 85% of the image. The bottom 15% should be empty,
minimal, or have only subtle gradient/background - never key content.
This space is reserved for branding overlay."""

NOVA_NEGATIVE_PROMPT = """text, words, letters, numbers, watermark, signature, logo, brand name,
blurry, low quality, distorted, ugly, deformed, disfigured,
realistic human faces, photorealistic people, real photographs,
cluttered, busy, messy, chaotic, dark, gloomy, depressing,
amateur, unprofessional, stock photo, generic clip art,
important elements at bottom of image, content near bottom edge,
cropped, cut off, partial objects, harsh shadows, overly complex"""


class NovaCanvasProvider(ImageModelProvider):
    """Amazon Nova Canvas - optimized for LinkedIn infographic illustrations."""

    MODEL_MAPPING = {
        "nova-canvas": "amazon.nova-canvas-v1:0",
    }

    def __init__(self, region: Optional[str] = None):
        """Initialize Bedrock client for Nova Canvas."""
        self.region = region or settings.aws_region

        config = Config(
            region_name=self.region,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )

        self.client = boto3.client("bedrock-runtime", config=config)

    @property
    def provider_name(self) -> str:
        return "nova"

    @property
    def available_models(self) -> list[str]:
        return list(self.MODEL_MAPPING.keys())

    async def validate_model(self, model: str) -> bool:
        """Check if model is in available list."""
        return model in self.MODEL_MAPPING

    def _get_model_id(self, model: str) -> str:
        """Get Bedrock model ID from friendly name."""
        if model not in self.MODEL_MAPPING:
            raise ProviderError(
                f"Model '{model}' not found. Available: {list(self.MODEL_MAPPING.keys())}",
                provider="nova",
                model=model,
            )
        return self.MODEL_MAPPING[model]

    async def generate(
        self,
        request: ImageGenerationRequest,
        model: str,
    ) -> ImageGenerationResponse:
        """
        Generate LinkedIn infographic-style images using Nova Canvas.
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="nova",
                model=model,
            )

        model_id = self._get_model_id(model)
        start_time = time.time()
        images = []
        errors = []

        logger.info(f"Generating {len(request.prompts)} infographic images with Nova Canvas")

        for prompt_data in request.prompts:
            try:
                # Get prompt - could be 'prompt' or 'description' attribute
                prompt_text = getattr(prompt_data, 'prompt', '') or getattr(prompt_data, 'description', '')
                style_notes = getattr(prompt_data, 'style_notes', '')
                concept = getattr(prompt_data, 'concept', '')

                if not prompt_text:
                    logger.warning(f"Empty prompt for image {prompt_data.id}")
                    continue

                enhanced_prompt = self._build_infographic_prompt(
                    prompt_text,
                    style_notes,
                    request.fingerprint,
                )

                logger.info(f"Nova image {prompt_data.id}: {enhanced_prompt[:300]}...")

                body = json.dumps({
                    "taskType": "TEXT_IMAGE",
                    "textToImageParams": {
                        "text": enhanced_prompt[:1024],
                        "negativeText": NOVA_NEGATIVE_PROMPT,
                    },
                    "imageGenerationConfig": {
                        "numberOfImages": 1,
                        "height": 1024,
                        "width": 1024,
                        "quality": "premium",
                    },
                })

                response = self.client.invoke_model(
                    body=body,
                    modelId=model_id,
                    accept="application/json",
                    contentType="application/json",
                )

                response_body = json.loads(response.get("body").read())

                if "images" in response_body and len(response_body["images"]) > 0:
                    image_data = response_body["images"][0]
                    images.append(GeneratedImage(
                        id=prompt_data.id,
                        base64_data=image_data,
                        prompt_used=enhanced_prompt,
                        format="png",
                        width=1024,
                        height=1024,
                    ))
                    logger.info(f"Successfully generated infographic {prompt_data.id}")
                else:
                    error_msg = f"No images in response for prompt {prompt_data.id}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            except ClientError as e:
                error_msg = f"AWS error for image {prompt_data.id}: {e.response['Error']['Message']}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
            except Exception as e:
                error_msg = f"Failed to generate image {prompt_data.id}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue

        if not images:
            error_detail = "; ".join(errors) if errors else "Unknown error"
            raise ProviderError(
                f"Failed to generate any images. Errors: {error_detail}",
                provider="nova",
                model=model,
            )

        elapsed_ms = int((time.time() - start_time) * 1000)

        return ImageGenerationResponse(
            images=images,
            model_used=model,
            generation_time_ms=elapsed_ms,
        )

    def _build_infographic_prompt(
        self,
        base_prompt: str,
        style_notes: str,
        fingerprint,
    ) -> str:
        """
        Build an infographic-optimized prompt for Nova Canvas.

        Creates LinkedIn-style educational infographic illustrations:
        - Cute cartoon characters with glasses (like the reference)
        - Clean pastel color palettes
        - Modern tech aesthetic
        - Clear visual hierarchy
        - Empty bottom for footer overlay
        """
        # Extract fingerprint styling
        if fingerprint is None:
            fp_palette = "soft pastel with blue and pink accents"
            fp_mood = "friendly and professional"
        elif isinstance(fingerprint, dict):
            fp_palette = fingerprint.get('color_palette', 'soft pastel')
            fp_mood = fingerprint.get('mood', 'friendly and professional')
        else:
            fp_palette = getattr(fingerprint, 'color_palette', 'soft pastel')
            fp_mood = getattr(fingerprint, 'mood', 'friendly and professional')

        # Build rich natural language prompt for Nova
        prompt_parts = [
            # Core scene description
            f"Create a professional LinkedIn infographic illustration: {base_prompt[:400]}",

            # Style guidance
            f"Style: {NOVA_SYSTEM_STYLE}",

            # Color and mood
            f"Color palette: {fp_palette}. Mood: {fp_mood}.",

            # Character style (if applicable)
            "If showing people: use cute cartoon style with big friendly eyes, round faces, and modern casual-tech attire.",

            # Composition (critical for footer)
            NOVA_COMPOSITION,

            # Additional style notes
            f"Additional context: {style_notes[:100]}" if style_notes else "",

            # Quality
            "Render in high quality, crisp details, suitable for professional LinkedIn content.",
        ]

        return " ".join(filter(None, prompt_parts))
