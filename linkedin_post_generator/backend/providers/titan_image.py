"""
Amazon Titan Image Generator V2 Provider
==========================================
Optimized for LinkedIn infographic-style illustrations.

Titan V2 Constraints:
- 512 character prompt limit (strict!)
- Prefers keyword-style prompts
- Less sophisticated prompt understanding
- Good for simpler, cleaner compositions

Optimized for:
- Keyword-dense, concise prompts
- Clean professional illustrations
- Top-weighted composition
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


# Titan-optimized negative prompt (keep concise)
TITAN_NEGATIVE_PROMPT = """text, words, letters, watermark, logo, signature,
blurry, low quality, distorted, deformed, ugly,
realistic faces, photorealistic, photograph,
cluttered, messy, dark, gloomy, amateur,
content at bottom, elements near bottom edge"""


class TitanImageProvider(ImageModelProvider):
    """Amazon Titan Image Generator - keyword-optimized for 512 char limit."""

    MODEL_MAPPING = {
        "titan-image-generator-v2": "amazon.titan-image-generator-v2:0",
    }

    def __init__(self, region: Optional[str] = None):
        """Initialize Bedrock client for Titan."""
        self.region = region or settings.aws_region

        config = Config(
            region_name=self.region,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )

        self.client = boto3.client("bedrock-runtime", config=config)

    @property
    def provider_name(self) -> str:
        return "titan"

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
                provider="titan",
                model=model,
            )
        return self.MODEL_MAPPING[model]

    async def generate(
        self,
        request: ImageGenerationRequest,
        model: str,
    ) -> ImageGenerationResponse:
        """
        Generate LinkedIn infographic-style images using Titan.
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="titan",
                model=model,
            )

        model_id = self._get_model_id(model)
        start_time = time.time()
        images = []
        errors = []

        logger.info(f"Generating {len(request.prompts)} images with Titan")

        for prompt_data in request.prompts:
            try:
                prompt_text = getattr(prompt_data, 'prompt', '')
                style_notes = getattr(prompt_data, 'style_notes', '')
                concept = getattr(prompt_data, 'concept', '')

                if not prompt_text:
                    logger.warning(f"Empty prompt for image {prompt_data.id}")
                    continue

                enhanced_prompt = self._build_keyword_prompt(
                    prompt_text,
                    style_notes,
                    request.fingerprint,
                )

                logger.info(f"Titan image {prompt_data.id}: {enhanced_prompt}")

                # Use requested dimensions if provided (e.g., 512x512 for carousel), otherwise default to 1024x1024
                img_width = request.width if request.width else 1024
                img_height = request.height if request.height else 1024

                body = json.dumps({
                    "taskType": "TEXT_IMAGE",
                    "textToImageParams": {
                        "text": enhanced_prompt,  # Already truncated to 510
                        "negativeText": TITAN_NEGATIVE_PROMPT[:512],
                    },
                    "imageGenerationConfig": {
                        "numberOfImages": 1,
                        "height": img_height,
                        "width": img_width,
                        "cfgScale": 8.0,
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
                        width=img_width,
                        height=img_height,
                    ))
                    logger.info(f"Successfully generated Titan image {prompt_data.id}")
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
                provider="titan",
                model=model,
            )

        elapsed_ms = int((time.time() - start_time) * 1000)

        return ImageGenerationResponse(
            images=images,
            model_used=model,
            generation_time_ms=elapsed_ms,
        )

    def _build_keyword_prompt(
        self,
        base_prompt: str,
        style_notes: str,
        fingerprint,
    ) -> str:
        """
        Build a keyword-optimized prompt for Titan (512 char limit).

        Strategy:
        - Use comma-separated keywords
        - Front-load important descriptors
        - Include composition constraint
        - Stay well under 512 chars
        """
        # Extract fingerprint styling (brief)
        if fingerprint is None:
            fp_style = "minimal"
            fp_palette = "pastel"
        elif isinstance(fingerprint, dict):
            fp_style = fingerprint.get('visual_style', 'minimal')[:20]
            fp_palette = fingerprint.get('color_palette', 'pastel')[:20]
        else:
            fp_style = getattr(fingerprint, 'visual_style', 'minimal')[:20]
            fp_palette = getattr(fingerprint, 'color_palette', 'pastel')[:20]

        # Truncate base prompt aggressively for Titan
        base_short = base_prompt[:250]

        # Build keyword-style prompt
        keywords = [
            # Core subject
            base_short,
            # Style keywords
            "infographic illustration",
            "professional LinkedIn style",
            fp_style,
            fp_palette + " colors",
            # Quality keywords
            "clean modern design",
            "cute cartoon style",
            "high quality",
            "crisp details",
            # Composition (critical)
            "content in upper area",
            "empty space at bottom",
            "top-weighted composition",
        ]

        # Add style notes if short enough
        if style_notes and len(style_notes) < 40:
            keywords.insert(3, style_notes)

        # Join and ensure under 510 chars
        result = ", ".join(keywords)

        if len(result) > 510:
            result = result[:507] + "..."

        return result
