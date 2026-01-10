"""
Nova Canvas Prompt Builder
===========================
Optimized prompts for Amazon Nova Canvas image generation.

Nova Canvas works best with:
- Descriptive, natural language prompts
- Clear composition guidance
- Professional, clean aesthetics
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class NovaPromptBuilder:
    """Builds optimized prompts for Nova Canvas image generation."""

    # Nova prefers natural language descriptions
    STYLE_PREFIX = (
        "Professional editorial illustration, "
        "clean modern design, high quality digital art"
    )

    def enhance_prompt(self, base_prompt: str, context: "PromptContext") -> str:
        """
        Enhance a base prompt for Nova Canvas.

        Args:
            base_prompt: The usecase-generated base prompt
            context: Additional context for customization

        Returns:
            Enhanced prompt optimized for Nova
        """
        parts = [self.STYLE_PREFIX]

        # Add the base prompt
        parts.append(base_prompt)

        # Add color palette if provided
        if context.color_palette:
            parts.append(f"Color palette: {context.color_palette}")

        # Add mood if provided
        if context.mood:
            parts.append(f"Mood: {context.mood}")

        # Nova-specific quality keywords
        parts.append("sharp details, professional finish")

        # Layout instruction
        if context.leave_space_bottom:
            parts.append(f"Leave bottom {context.bottom_space_percent}% empty for text overlay")

        return ". ".join(filter(None, parts))

    def get_negative_prompt(self, usecase: str, context: "PromptContext") -> str:
        """
        Get the negative prompt for Nova.

        Nova has limited negative prompt support, so we keep it simple.
        """
        return (
            "text, words, labels, watermark, blurry, low quality, "
            "distorted, unprofessional, cluttered"
        )

    def get_settings(self, usecase: str) -> dict:
        """Get recommended Nova settings for a usecase."""
        return {
            "quality": "premium",
            "style": "photographic" if usecase == "postcard" else "digital-art",
        }

