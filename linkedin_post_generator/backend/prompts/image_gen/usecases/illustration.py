"""
AI Illustration Use Case Prompt Builder
========================================
Generates prompts for editorial-style illustrations with infographic overlays.

Illustrations need:
- Soft pastel backgrounds
- Small characters/icons at edges
- Large empty areas for text overlay
- Editorial, professional style
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class IllustrationPromptBuilder:
    """Builds prompts optimized for editorial illustrations."""

    # Default styles for illustrations
    STYLES = {
        "editorial": {
            "base": "editorial illustration, modern tech blog style, soft pastel colors",
            "elements": "subtle workspace elements, small developer character at corner",
        },
        "conceptual": {
            "base": "conceptual illustration, abstract metaphors, clean vector style",
            "elements": "geometric shapes, symbolic icons, floating elements",
        },
        "friendly": {
            "base": "friendly illustration, storybook style, warm inviting colors",
            "elements": "approachable characters, cozy workspace scene",
        },
    }

    def get_base_prompt(self, context: "PromptContext") -> str:
        """
        Generate the base prompt for an illustration.

        Args:
            context: The prompt context with style preferences

        Returns:
            Base prompt string
        """
        # Determine style
        style_name = context.visual_style or "editorial"
        style = self.STYLES.get(style_name, self.STYLES["editorial"])

        # Determine colors
        if context.color_palette:
            colors = context.color_palette
        else:
            colors = "soft pastel, warm peach, light blue, cream tones"

        prompt_parts = [
            # Style foundation
            style["base"],
            "flat design elements",
            "clean line art",

            # Color palette
            f"{colors}",

            # Scene elements (at edges only)
            style["elements"],
            "elements positioned at bottom corners",

            # Layout - CRITICAL
            "large empty center and upper area for text overlay",
            "light neutral background",
            "minimal clean composition",

            # Atmosphere
            "ambient soft lighting",
            "professional workspace aesthetic",

            # NO TEXT
            "NO TEXT NO WORDS NO LABELS",

            # Footer space
            "bottom 15% completely empty for footer",
        ]

        # Add concept if provided
        if context.concept:
            prompt_parts.insert(3, f"concept: {context.concept}")

        return ", ".join(prompt_parts)

    def get_style_notes(self, context: "PromptContext") -> str:
        """Get style notes for illustration generation."""
        if context.style_notes:
            return context.style_notes

        return (
            "Editorial illustration style with soft pastel colors. "
            "Small characters/elements at edges, large empty center for text. "
            "Professional, calm, thoughtful mood."
        )

