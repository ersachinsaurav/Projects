"""
Titan Image Generator Prompt Builder
=====================================
Optimized prompts for Amazon Titan Image Generator.

Titan works best with:
- Concise, focused prompts
- Clear style keywords
- Minimal complexity
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class TitanPromptBuilder:
    """Builds optimized prompts for Titan Image Generator."""

    STYLE_PREFIX = "Professional illustration, clean design"

    def enhance_prompt(self, base_prompt: str, context: "PromptContext") -> str:
        """
        Enhance a base prompt for Titan.

        Titan prefers shorter, more focused prompts.

        Args:
            base_prompt: The usecase-generated base prompt
            context: Additional context for customization

        Returns:
            Enhanced prompt optimized for Titan
        """
        # Titan works better with shorter prompts
        # Truncate if too long
        if len(base_prompt) > 500:
            base_prompt = base_prompt[:500]

        parts = [self.STYLE_PREFIX, base_prompt]

        # Add color palette if provided (brief)
        if context.color_palette:
            # Extract just key colors
            colors = context.color_palette.split(",")[:3]
            parts.append(f"Colors: {', '.join(colors)}")

        # Layout instruction
        if context.leave_space_bottom:
            parts.append("Bottom area empty for text")

        return ". ".join(filter(None, parts))

    def get_negative_prompt(self, usecase: str, context: "PromptContext") -> str:
        """
        Get the negative prompt for Titan.

        Titan supports basic negative prompts.
        """
        return (
            "text, words, labels, watermark, signature, logo, "
            "blurry, low quality, distorted, ugly, deformed, "
            "busy background, cluttered, messy"
        )

    def get_settings(self, usecase: str) -> dict:
        """Get recommended Titan settings for a usecase."""
        return {
            "numberOfImages": 1,
            "quality": "premium",
        }

