"""
SDXL WebUI Image Provider
==========================
Provider for local Stable Diffusion XL via Automatic1111 WebUI API.

This provider connects to a local SDXL instance running on port 7860
(default) and generates images using the txt2img API endpoint.

SDXL WebUI API:
- Endpoint: http://localhost:7860/sdapi/v1/txt2img
- Supports full prompt control
- High quality image generation
- Configurable sampling parameters
"""

import base64
import json
import time
import logging
from typing import Optional

import httpx

from ..config import settings
from .base import (
    ImageModelProvider,
    ImageGenerationRequest,
    ImageGenerationResponse,
    GeneratedImage,
    ProviderError,
)

logger = logging.getLogger(__name__)


# SDXL default negative prompt (fallback - AI-generated negative prompts are preferred)
# Optimized for editorial infographic style
# CRITICAL: Includes anti-collage/grid prompts to prevent multi-panel generation
SDXL_NEGATIVE_PROMPT = """text, words, letters, labels, captions, titles, headlines, subtitles,
writing, typography, fonts, numbers, digits, annotations, watermark, signature, logo,
speech bubbles, text boxes, text overlays, inscriptions, handwriting,
collage, grid, multiple panels, split image, tiled, mosaic, diptych, triptych,
photo collage, image grid, four panels, multiple frames, side by side,
photorealistic, realism, ultra realistic, 3d render,
corporate vector illustration, flat icon-only style,
anime, manga, chibi, kawaii,
dark colors, harsh shadows, dramatic lighting,
high contrast neon colors,
messy layout, cluttered background,
distorted faces, extra fingers, malformed hands,
low resolution, blurry, noisy, grainy,
important elements at bottom of image, content near bottom edge"""


class SDXLWebUIProvider(ImageModelProvider):
    """SDXL WebUI Provider - connects to local Stable Diffusion XL instance."""

    MODEL_MAPPING = {
        "sdxl": "sdxl",
    }

    # Keywords that indicate we should use the full prompt instead of background-only
    # These trigger "illustration mode" which uses Claude's prompt with minimal modification
    ILLUSTRATION_KEYWORDS = [
        # Character-focused
        "cartoon", "illustrated", "character", "storybook", "scene",
        "narrative", "comic", "animation", "drawing", "sketch",
        "friendly character", "character design", "visual story",
        # SDXL format keywords (from updated Claude prompt)
        "flat editorial", "editorial illustration", "composition is top-weighted",
        "vector-like", "soft gradients", "developer seated", "workspace atmosphere",
        "single unified scene", "character in upper", "bottom 30%",
        # Workspace/professional scenes
        "developer", "knowledge worker", "seated at desk", "typing on laptop",
        "colleagues", "thumbs-up", "recognition", "acknowledgment",
    ]

    def __init__(self, webui_url: Optional[str] = None):
        """
        Initialize SDXL WebUI provider.

        Args:
            webui_url: Base URL for WebUI (default: http://localhost:7860)
        """
        self.webui_url = webui_url or settings.sdxl_webui_url
        self.api_url = f"{self.webui_url.rstrip('/')}/sdapi/v1/txt2img"
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 min timeout for generation

    @property
    def provider_name(self) -> str:
        return "sdxl"

    @property
    def available_models(self) -> list[str]:
        return list(self.MODEL_MAPPING.keys())

    async def validate_model(self, model: str) -> bool:
        """Check if model is in available list."""
        return model in self.MODEL_MAPPING

    async def _check_webui_health(self) -> bool:
        """Check if WebUI is running and accessible."""
        try:
            health_url = f"{self.webui_url.rstrip('/')}/sdapi/v1/options"
            response = await self.client.get(health_url, timeout=5.0)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"WebUI health check failed: {e}")
            return False

    async def generate(
        self,
        request: ImageGenerationRequest,
        model: str,
    ) -> ImageGenerationResponse:
        """
        Generate images using SDXL WebUI API.

        Args:
            request: Standardized image generation request
            model: Model name (should be "sdxl")

        Returns:
            ImageGenerationResponse with generated images

        Raises:
            ProviderError: If generation fails or WebUI is unavailable
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="sdxl",
                model=model,
            )

        # Check WebUI health
        if not await self._check_webui_health():
            raise ProviderError(
                f"SDXL WebUI is not accessible at {self.webui_url}. "
                "Make sure WebUI is running and accessible.",
                provider="sdxl",
                model=model,
            )

        start_time = time.time()
        images = []
        errors = []

        logger.info(f"Generating {len(request.prompts)} images with SDXL WebUI")

        for prompt_data in request.prompts:
            try:
                # Get prompt text
                prompt_text = getattr(prompt_data, 'prompt', '') or getattr(prompt_data, 'description', '')
                style_notes = getattr(prompt_data, 'style_notes', '')
                concept = getattr(prompt_data, 'concept', '')
                negative_prompt = getattr(prompt_data, 'negative_prompt', None)

                if not prompt_text:
                    logger.warning(f"Empty prompt for image {prompt_data.id}")
                    continue

                # Build enhanced prompt
                enhanced_prompt = self._build_sdxl_prompt(
                    prompt_text,
                    style_notes,
                    request.fingerprint,
                )

                # Use AI-generated negative prompt if available, otherwise fallback to default
                final_negative_prompt = negative_prompt if negative_prompt else SDXL_NEGATIVE_PROMPT

                logger.info(f"SDXL image {prompt_data.id}: {enhanced_prompt[:200]}...")
                logger.info(f"SDXL negative prompt {prompt_data.id}: {final_negative_prompt[:100]}...")

                # Use requested dimensions if provided (e.g., 512x512 for carousel), otherwise use settings
                img_width = request.width if request.width else settings.sdxl_width
                img_height = request.height if request.height else settings.sdxl_height

                # Prepare request payload
                payload = {
                    "prompt": enhanced_prompt,
                    "negative_prompt": final_negative_prompt,
                    "width": img_width,
                    "height": img_height,
                    "steps": settings.sdxl_steps,
                    "sampler_name": settings.sdxl_sampler,
                    "cfg_scale": settings.sdxl_cfg_scale,
                    "seed": -1,  # Random seed
                }

                # Make API request
                response = await self.client.post(
                    self.api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )

                response.raise_for_status()
                response_data = response.json()

                # Extract image from response
                if "images" in response_data and len(response_data["images"]) > 0:
                    # WebUI returns base64-encoded images (with data URI prefix)
                    image_base64 = response_data["images"][0]

                    # Remove data URI prefix if present (e.g., "data:image/png;base64,")
                    if "," in image_base64:
                        image_base64 = image_base64.split(",", 1)[1]

                    images.append(GeneratedImage(
                        id=prompt_data.id,
                        base64_data=image_base64,
                        prompt_used=enhanced_prompt,
                        format="png",
                        width=img_width,
                        height=img_height,
                    ))
                    logger.info(f"Successfully generated SDXL image {prompt_data.id}")
                else:
                    error_msg = f"No images in response for prompt {prompt_data.id}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP error for image {prompt_data.id}: {e.response.status_code} - {e.response.text[:200]}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
            except httpx.RequestError as e:
                error_msg = f"Request error for image {prompt_data.id}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
            except Exception as e:
                error_msg = f"Failed to generate image {prompt_data.id}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                continue

        if not images:
            error_detail = "; ".join(errors) if errors else "Unknown error"
            raise ProviderError(
                f"Failed to generate any images. Errors: {error_detail}",
                provider="sdxl",
                model=model,
            )

        elapsed_ms = int((time.time() - start_time) * 1000)

        return ImageGenerationResponse(
            images=images,
            model_used=model,
            generation_time_ms=elapsed_ms,
        )

    def _is_illustration_prompt(self, prompt: str) -> bool:
        """Check if the prompt requests an illustrated/cartoon scene."""
        prompt_lower = prompt.lower()
        return any(kw in prompt_lower for kw in self.ILLUSTRATION_KEYWORDS)

    def _build_sdxl_prompt(
        self,
        base_prompt: str,
        style_notes: str,
        fingerprint,
    ) -> str:
        """
        Build an optimized prompt for SDXL.

        Two modes:
        1. ILLUSTRATION MODE: If prompt contains illustration keywords (cartoon, character, etc.),
           use the detailed prompt directly with quality enhancements.
        2. BACKGROUND MODE: For infographic-style images, generate a clean background
           with empty space for text overlays.
        """
        # Check if this is an illustration/character prompt (e.g., carousel cover)
        if self._is_illustration_prompt(base_prompt):
            logger.info("SDXL: Detected illustration mode - using detailed prompt")
            return self._build_illustration_prompt(base_prompt, style_notes, fingerprint)
        else:
            logger.info("SDXL: Detected background mode - building clean background prompt")
            return self._build_background_prompt(base_prompt, style_notes, fingerprint)

    def _build_illustration_prompt(
        self,
        base_prompt: str,
        style_notes: str,
        fingerprint,
    ) -> str:
        """
        Build a prompt for illustrated/cartoon scenes.
        Uses the detailed prompt from Claude with quality enhancements.
        """
        # Extract fingerprint styling
        if fingerprint is None:
            fp_palette = "warm, inviting"
        elif isinstance(fingerprint, dict):
            fp_palette = fingerprint.get('color_palette', 'warm, inviting')
        else:
            fp_palette = getattr(fingerprint, 'color_palette', 'warm, inviting')

        # Quality prefixes for illustration
        quality_prefix = (
            "masterpiece, best quality, highly detailed illustration, "
            "professional digital art, clean lines, "
        )

        # Build the full prompt
        prompt_parts = [quality_prefix]

        # Add the main prompt from Claude (this is the detailed scene description)
        prompt_parts.append(base_prompt)

        # Add style notes if provided
        if style_notes and style_notes not in base_prompt:
            prompt_parts.append(style_notes)

        # Add color palette
        if fp_palette:
            prompt_parts.append(f"{fp_palette} color palette")

        # Quality suffix
        quality_suffix = (
            "high resolution, sharp focus, vibrant colors, "
            "professional artwork, artstation quality"
        )
        prompt_parts.append(quality_suffix)

        final_prompt = ", ".join(filter(None, prompt_parts))
        logger.info(f"SDXL illustration prompt: {final_prompt[:300]}...")
        return final_prompt

    def _build_background_prompt(
        self,
        base_prompt: str,
        style_notes: str,
        fingerprint,
    ) -> str:
        """
        Build a prompt for clean background images (for infographic overlays).
        Generates a simple background with empty space for text.
        """
        # Extract fingerprint styling
        if fingerprint is None:
            fp_palette = "soft pastel"
        elif isinstance(fingerprint, dict):
            fp_palette = fingerprint.get('color_palette', 'soft pastel')
        else:
            fp_palette = getattr(fingerprint, 'color_palette', 'soft pastel')

        # SIMPLE background prompt - NOT complex multi-panel
        # The key is: light colors, empty center, small illustrations at edges
        background_prompt_parts = [
            # Style foundation
            "soft gradient background illustration",
            "light pastel color palette",
            "clean minimalist design",
            "subtle paper texture",

            # Ensure EMPTY space for text overlays
            "large empty light-colored areas in center",
            "plenty of negative space for text overlay",
            "upper 70% mostly empty with soft gradient",

            # Small decorative elements at edges only
            "small decorative workspace elements at bottom corners",
            "tiny icons scattered at edges",
            "subtle developer desk scene at bottom right corner only",
            "minimal illustration, maximum empty space",

            # Technical quality
            "high quality illustration",
            "soft ambient lighting",
            "warm approachable aesthetic",

            # CRITICAL: No text
            "absolutely no text words or labels in the image",
            "no writing no typography no captions",

            # Footer space
            "bottom 15% completely empty for footer",
        ]

        # Add palette from fingerprint
        if fp_palette and "pastel" not in background_prompt_parts[1]:
            background_prompt_parts.insert(1, f"{fp_palette} tones")

        # Extract any thematic elements from base_prompt but keep it minimal
        # Only take very short descriptive words, not full sentences
        if base_prompt:
            # Extract simple keywords only, not the full detailed prompt
            simple_keywords = []
            keywords_to_look_for = [
                "workspace", "office", "desk", "computer", "developer",
                "coffee", "plant", "books", "window", "calm", "focus",
                "productivity", "creative", "modern", "tech", "professional"
            ]
            base_lower = base_prompt.lower()
            for kw in keywords_to_look_for:
                if kw in base_lower:
                    simple_keywords.append(kw)

            if simple_keywords:
                background_prompt_parts.append(f"subtle theme: {', '.join(simple_keywords[:5])}")

        return ", ".join(background_prompt_parts)

