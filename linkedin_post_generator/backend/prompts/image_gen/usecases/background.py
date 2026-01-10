"""
Background Prompt Builder
==========================
Generates prompts for simple textured backgrounds WITHOUT characters.

These backgrounds are designed to have text overlaid programmatically,
similar to viral LinkedIn/Instagram quote posts.

Styles:
- Paper texture (cream, white, off-white)
- Abstract gradient (soft, professional colors)
- Grid/notebook paper
- Solid with subtle texture
- Whiteboard/chalkboard
- Minimal with geometric accents

Key principle: NO CHARACTERS, NO COMPLEX SCENES, NO TEXT.
The AI generates ONLY the background, we add text in code.
"""

from typing import Optional
from dataclasses import dataclass

from ..base import PromptContext


@dataclass
class BackgroundStyle:
    """Configuration for background generation."""
    style: str = "paper_texture"  # paper_texture, abstract, grid, solid, whiteboard, minimal
    mood: str = "professional"  # professional, warm, calm, energetic, serious
    color_scheme: str = "neutral"  # neutral, warm, cool, dark, light


class BackgroundPromptBuilder:
    """
    Builds prompts for simple textured backgrounds.

    These are meant for text overlay - no characters, no complex scenes.
    Think: viral LinkedIn quote posts, Jean Lee style, paper texture quotes.
    """

    # Style-specific prompts
    STYLE_PROMPTS = {
        "paper_texture": {
            "base": "minimalist paper texture background, subtle grain, clean surface",
            "variations": [
                "cream colored handmade paper texture, gentle fiber patterns",
                "white paper with subtle crinkle texture, soft shadows",
                "off-white parchment paper, warm aged look, clean and simple",
                "recycled paper texture, light speckles, natural feel",
            ]
        },
        "abstract": {
            "base": "abstract minimalist background, soft gradient, professional",
            "variations": [
                "soft pastel gradient background, peach to cream transition",
                "subtle abstract shapes, muted colors, gentle curves",
                "professional abstract background, soft blues and grays",
                "warm abstract gradient, coral to cream, soft and inviting",
            ]
        },
        "grid": {
            "base": "graph paper background, light grid lines, clean minimal",
            "variations": [
                "notebook grid paper, subtle blue lines, clean white background",
                "engineering paper texture, light green grid, professional",
                "dotted grid paper, minimal design, soft grey dots",
            ]
        },
        "solid": {
            "base": "solid color background with subtle texture",
            "variations": [
                "solid dark blue-grey background, subtle noise texture",
                "clean white background with very subtle grain",
                "warm cream solid background, professional minimal",
                "soft grey background, subtle paper-like texture",
            ]
        },
        "whiteboard": {
            "base": "whiteboard surface, clean reflective, office setting",
            "variations": [
                "clean whiteboard texture, slight gloss, professional",
                "dry erase board surface, subtle reflections, minimal",
            ]
        },
        "minimal": {
            "base": "ultra minimal background, negative space, clean design",
            "variations": [
                "minimal white background with subtle geometric accent",
                "clean background with soft shadow element",
                "pure minimalist surface, gentle gradient, professional",
            ]
        },
    }

    # Mood modifiers
    MOOD_MODIFIERS = {
        "professional": "professional, clean, business appropriate",
        "warm": "warm tones, inviting, friendly feel",
        "calm": "serene, peaceful, gentle colors",
        "energetic": "vibrant undertones, dynamic feel",
        "serious": "muted, understated, corporate feel",
    }

    # Color scheme modifiers
    COLOR_MODIFIERS = {
        "neutral": "neutral tones, grays, whites, creams",
        "warm": "warm colors, cream, peach, soft coral",
        "cool": "cool colors, soft blues, light grays",
        "dark": "dark background, deep colors, dramatic",
        "light": "light airy colors, whites, soft pastels",
    }

    # Critical: What to exclude
    ALWAYS_EXCLUDE = [
        "text", "words", "letters", "writing", "typography",
        "people", "person", "character", "figure", "face", "human",
        "hands", "body parts",
        "complex scene", "detailed illustration",
        "logo", "branding", "watermark",
    ]

    def get_base_prompt(self, context: PromptContext) -> str:
        """
        Generate base prompt for a textured background.

        Args:
            context: PromptContext with style preferences

        Returns:
            Base prompt string for background generation
        """
        # Determine style from context or default
        style = context.visual_style or "paper_texture"
        if style not in self.STYLE_PROMPTS:
            style = "paper_texture"

        # Get style-specific prompts
        style_data = self.STYLE_PROMPTS[style]

        # Pick a variation or use base
        import random
        if context.original_prompt:
            # If we have specific guidance, use base + guidance
            base_prompt = style_data["base"]
        else:
            # Random variation for variety
            variations = style_data.get("variations", [style_data["base"]])
            base_prompt = random.choice(variations)

        # Add mood and color modifiers
        mood = context.mood or "professional"
        mood_mod = self.MOOD_MODIFIERS.get(mood, self.MOOD_MODIFIERS["professional"])

        color = context.color_palette or "neutral"
        color_mod = self.COLOR_MODIFIERS.get(color, self.COLOR_MODIFIERS["neutral"])

        # Combine prompt parts
        prompt_parts = [
            base_prompt,
            mood_mod,
            color_mod,
            "high quality, 4k resolution, clean design",
            "perfect for text overlay, large empty space",
        ]

        # Add specific context if provided
        if context.style_notes:
            prompt_parts.append(context.style_notes)

        return ", ".join(prompt_parts)

    def get_style_notes(self, context: PromptContext) -> str:
        """Get style notes for background generation."""
        return (
            "Generate ONLY a simple textured background. "
            "NO characters, NO text, NO complex scenes. "
            "The background should have large empty areas suitable for text overlay. "
            "Think: viral LinkedIn quote posts, paper texture aesthetics."
        )

    def get_negative_prompt(self) -> str:
        """Get negative prompt to ensure clean backgrounds."""
        return ", ".join(self.ALWAYS_EXCLUDE + [
            "busy", "cluttered", "complex", "detailed scene",
            "photo", "photograph", "realistic",
            "cartoon character", "anime", "illustration with characters",
        ])


# Convenience function for quick background prompt generation
def get_background_prompt(
    style: str = "paper_texture",
    mood: str = "professional",
    color_scheme: str = "neutral",
) -> dict:
    """
    Quick function to get a background prompt.

    Args:
        style: paper_texture, abstract, grid, solid, whiteboard, minimal
        mood: professional, warm, calm, energetic, serious
        color_scheme: neutral, warm, cool, dark, light

    Returns:
        Dict with prompt and negative_prompt
    """
    builder = BackgroundPromptBuilder()
    context = PromptContext(
        visual_style=style,
        mood=mood,
        color_palette=color_scheme,
    )

    return {
        "prompt": builder.get_base_prompt(context),
        "negative_prompt": builder.get_negative_prompt(),
        "style_notes": builder.get_style_notes(context),
    }

