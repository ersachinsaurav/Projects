"""
Postcard Use Case Prompt Builder
=================================
Generates prompts for text-overlay style postcards.

Postcards need:
- Simple, clean backgrounds
- Large empty areas for text
- Subtle gradients or solid colors
- Minimal decorative elements at edges only
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class PostcardPromptBuilder:
    """Builds prompts optimized for postcard/text-overlay images."""

    # Default color palettes for postcards
    COLOR_PALETTES = {
        "dark": "dark slate, charcoal gray, deep navy, subtle blue accents",
        "light": "soft cream, warm white, light gray, subtle peach accents",
        "warm": "warm beige, soft coral, cream, gentle orange tones",
        "cool": "soft blue, light gray, white, subtle cyan accents",
    }

    def get_base_prompt(self, context: "PromptContext") -> str:
        """
        Generate the base prompt for a postcard image.

        Args:
            context: The prompt context with style preferences

        Returns:
            Base prompt string
        """
        # Determine color palette
        if context.color_palette:
            colors = context.color_palette
        else:
            colors = self.COLOR_PALETTES.get("warm", self.COLOR_PALETTES["warm"])

        prompt_parts = [
            # Core requirements - clean background
            "soft gradient background",
            "clean minimalist design",
            "subtle paper texture",

            # Color
            f"{colors}",

            # Layout - CRITICAL for postcards
            "large empty center area for text overlay",
            "plenty of negative space",
            "upper 80% mostly empty with soft gradient",

            # Optional decorative elements
            "small decorative elements at corners only",
            "minimal subtle icons at edges",

            # Quality
            "professional design",
            "soft ambient lighting",

            # NO TEXT
            "absolutely no text words or labels in the image",

            # Footer space
            "bottom 15% empty for footer",
        ]

        return ", ".join(prompt_parts)

    def get_style_notes(self, context: "PromptContext") -> str:
        """Get style notes for postcard generation."""
        if context.style_notes:
            return context.style_notes

        return (
            "Clean, minimal background suitable for text overlay. "
            "Soft gradient or solid colors. No distracting elements. "
            "Professional, LinkedIn-appropriate aesthetic."
        )

