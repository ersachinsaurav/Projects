"""
SDXL Prompt Builder
====================
Optimized prompts for Stable Diffusion XL via WebUI API.

SDXL works best with:
- Quality prefixes at the start
- Explicit style keywords
- Detailed negative prompts
- Clear layout instructions
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class SDXLPromptBuilder:
    """Builds optimized prompts for SDXL image generation."""

    # Quality prefix - added to start of all prompts
    QUALITY_PREFIX = (
        "masterpiece, best quality, highly detailed illustration, "
        "professional digital art, clean lines"
    )

    # Quality suffix - added to end of all prompts
    QUALITY_SUFFIX = (
        "high resolution, sharp focus, vibrant colors, "
        "professional artwork, artstation quality"
    )

    # Base negative prompt - common to all usecases
    BASE_NEGATIVE = (
        "text, words, letters, labels, captions, titles, headlines, subtitles, "
        "writing, typography, fonts, numbers, digits, annotations, watermark, signature, logo, "
        "speech bubbles, text boxes, text overlays, inscriptions, handwriting, "
        "collage, grid, multiple panels, split image, tiled, mosaic, diptych, triptych, "
        "photo collage, image grid, four panels, multiple frames, side by side, "
        "photorealistic, realism, ultra realistic, 3d render, "
        "low resolution, blurry, noisy, grainy, "
        "distorted faces, extra fingers, malformed hands"
    )

    # Usecase-specific negative additions
    NEGATIVE_ADDITIONS = {
        "carousel": (
            ", dark colors, harsh shadows, dramatic lighting, "
            "high contrast neon colors, messy layout, cluttered background, "
            "important elements at bottom of image, content near bottom edge, "
            "anime, manga, chibi, kawaii"
        ),
        "illustration": (
            ", corporate vector illustration, flat icon-only style, "
            "anime, manga, chibi, kawaii, "
            "dark colors, harsh shadows, dramatic lighting, "
            "messy layout, cluttered background"
        ),
        "postcard": (
            ", complex backgrounds, busy scenes, "
            "characters, people, animals, "
            "dark colors, dramatic lighting"
        ),
    }

    def enhance_prompt(self, base_prompt: str, context: "PromptContext") -> str:
        """
        Enhance a base prompt with SDXL-specific optimizations.

        Args:
            base_prompt: The usecase-generated base prompt
            context: Additional context for customization

        Returns:
            Enhanced prompt optimized for SDXL
        """
        parts = [self.QUALITY_PREFIX]

        # Add the base prompt
        parts.append(base_prompt)

        # Add color palette if provided
        if context.color_palette:
            parts.append(f"{context.color_palette} color palette")

        # Add style notes if provided (truncated)
        if context.style_notes:
            # Only take first 100 chars to avoid prompt bloat
            style_excerpt = context.style_notes[:100]
            parts.append(style_excerpt)

        # Add quality suffix
        parts.append(self.QUALITY_SUFFIX)

        return ", ".join(filter(None, parts))

    def get_negative_prompt(self, usecase: str, context: "PromptContext") -> str:
        """
        Get the negative prompt for SDXL.

        Args:
            usecase: The usecase (carousel, illustration, postcard)
            context: Additional context

        Returns:
            Complete negative prompt
        """
        negative = self.BASE_NEGATIVE

        # Add usecase-specific negatives
        addition = self.NEGATIVE_ADDITIONS.get(usecase, self.NEGATIVE_ADDITIONS["illustration"])
        negative += addition

        return negative

    def get_settings(self, usecase: str) -> dict:
        """
        Get recommended SDXL settings for a usecase.

        Returns:
            Dict with cfg_scale, steps, sampler recommendations
        """
        settings = {
            "carousel": {
                "cfg_scale": 7,
                "steps": 35,
                "sampler": "DPM++ 2M Karras",
                "aspect_ratio": "512x768",  # Portrait for carousel
            },
            "illustration": {
                "cfg_scale": 7,
                "steps": 30,
                "sampler": "DPM++ 2M Karras",
                "aspect_ratio": "1024x1024",  # Square
            },
            "postcard": {
                "cfg_scale": 6,
                "steps": 25,
                "sampler": "DPM++ 2M Karras",
                "aspect_ratio": "1024x1024",  # Square
            },
        }
        return settings.get(usecase, settings["illustration"])

