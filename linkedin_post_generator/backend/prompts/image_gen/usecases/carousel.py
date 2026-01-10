"""
Carousel Cover Use Case Prompt Builder
=======================================
Generates prompts for LinkedIn carousel cover images.

Carousel covers need:
- Friendly cartoon character(s) as the main focus
- Character positioned in UPPER 70% of image
- Bottom 30% empty for title/subtitle overlay
- Single unified scene (NO collages or grids)
- Warm, inviting, storybook illustration style

SDXL Prompt Format (LinkedIn Leadership / Recognition Theme):
- Flat editorial illustration style
- Warm pastel color palette
- Single developer/knowledge worker at desk
- Cozy modern workspace with minimal elements
- Soft gradients, clean vector shapes
- Top-weighted composition with bottom 30% empty
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import PromptContext


class CarouselPromptBuilder:
    """Builds prompts optimized for carousel cover images."""

    # Character descriptions - cartoon developer style for SDXL
    # Reference style: Cartoon developer with big round glasses, messy brown hair,
    # blue shirt, holding coffee mug, sitting at desk with monitor, excited expression
    CHARACTER_STYLE_HINT = (
        "cartoon character with big round eyes and glasses, "
        "messy brown hair, wearing blue shirt, "
        "excited happy expression with open mouth smile, "
        "holding coffee mug with logo, "
        "sitting at desk with computer monitor showing code, "
        "colorful cartoon illustration style like Pixar or modern app illustrations"
    )

    CHARACTER_STYLES = {
        "developer": (
            f"a cartoon developer character with big round glasses and big expressive eyes, "
            f"messy brown hair, wearing casual blue shirt, "
            f"sitting at desk with computer monitor showing colorful code, "
            f"holding coffee mug, excited happy expression, "
            f"modern cartoon illustration style, warm and inviting"
        ),
        "leader": (
            f"a cartoon professional character with big round glasses, "
            f"confident friendly smile, wearing blue shirt, "
            f"gesturing warmly as if explaining something, "
            f"modern cartoon illustration style, approachable leader vibe"
        ),
        "team": (
            f"two cartoon developer characters with big expressive eyes, "
            f"one with glasses giving thumbs-up to the other, "
            f"both wearing casual shirts, at a shared desk with monitors, "
            f"modern cartoon illustration style, collaborative atmosphere"
        ),
        "thinker": (
            f"a cartoon developer character with big round glasses, "
            f"messy hair, thoughtful expression looking at screen, "
            f"lightbulb icon floating nearby, holding chin, "
            f"modern cartoon illustration style, moment of realization"
        ),
        "helper": (
            f"a cartoon professional character with big friendly eyes, "
            f"welcoming open posture with gentle smile, "
            f"modern cartoon illustration style, supportive demeanor"
        ),
        "recognition": (
            f"two cartoon developer characters at workspace, "
            f"one with big round glasses giving thumbs-up to colleague, "
            f"chat bubble with checkmark icon nearby, "
            f"modern cartoon illustration style, warm recognition moment"
        ),
    }

    # Detailed color palettes for SDXL
    COLOR_PALETTES = {
        "warm": "warm pastel color palette with peach, soft coral, light blue, and cream tones",
        "professional": "soft professional blues, light gray, cream, subtle navy accents",
        "friendly": "gentle pastel pink, soft yellow, light blue, warm cream",
        "tech": "soft mint green, light blue, white, subtle teal accents",
        "leadership": "warm gold, soft cream, gentle brown, light orange tones",
        "recognition": "warm peach, soft coral, cream, gentle orange with blue accents",
    }

    # Workspace elements for atmosphere
    WORKSPACE_ELEMENTS = [
        "small potted plant",
        "coffee mug",
        "subtle chat bubble or checkmark icon nearby to symbolize acknowledgment",
    ]

    def get_base_prompt(self, context: "PromptContext") -> str:
        """
        Generate a detailed prompt for carousel cover optimized for SDXL.

        Based on GPT's recommended SDXL format for LinkedIn content.

        Args:
            context: The prompt context with style preferences

        Returns:
            Detailed prompt string
        """
        # Determine character style based on context
        character = self._select_character_style(context)

        # Determine color palette
        if context.color_palette:
            colors = context.color_palette
        else:
            colors = self.COLOR_PALETTES.get("warm", self.COLOR_PALETTES["warm"])

        # Build the detailed prompt following SDXL best practices
        prompt_parts = [
            # Style foundation - modern cartoon illustration
            "modern cartoon illustration",
            "colorful digital art style like Pixar or Slack illustrations",
            colors,

            # CAMERA/FRAMING - CRITICAL: Show full scene, not close-up
            "wide shot showing full upper body and desk",
            "medium distance view not close-up",
            "character takes up about 40 percent of frame height",
            "plenty of space around character",

            # Character style - big expressive eyes, friendly
            "cartoon character with big round expressive eyes",
            "big round glasses on character",
            "messy brown hair",
            "wearing casual blue shirt",
            "excited happy expression",

            # Character and scene - detailed description
            character,

            # Workspace elements - visible in frame
            "desk with computer monitor showing colorful code visible in scene",
            "coffee mug on desk",
            "small potted plant nearby",
            "workspace environment visible",

            # Visual style
            "soft pastel background",
            "clean smooth shapes",
            "bold outlines",
            "vibrant but soft colors",

            # Composition - CRITICAL for layout
            "composition is top-weighted",
            "character and workspace centered in upper 60 percent of frame",
            "large empty area at bottom for text overlay",
            "bottom 30 percent is simple solid pastel color with no details",

            # Lighting and mood
            "soft ambient lighting",
            "friendly and uplifting mood",
            "warm inviting atmosphere",

            # Style keywords
            "professional cartoon style",
            "modern app illustration aesthetic",
            "suitable for LinkedIn content",

            # CRITICAL: No text
            "no text in the image",
            "no words",
            "no labels",
            "no typography",
        ]

        return ", ".join(prompt_parts)

    def _select_character_style(self, context: "PromptContext") -> str:
        """Select appropriate character style based on context."""
        # Try to infer from concept or style notes
        if context.concept:
            concept_lower = context.concept.lower()

            # Recognition/acknowledgment themed
            if any(word in concept_lower for word in ["recogni", "acknowledg", "appreciat", "thank", "shoutout"]):
                return self.CHARACTER_STYLES["recognition"]
            # Team collaboration
            elif any(word in concept_lower for word in ["team", "collaborat", "together", "colleague"]):
                return self.CHARACTER_STYLES["team"]
            # Leadership
            elif any(word in concept_lower for word in ["lead", "manage", "guide", "mentor"]):
                return self.CHARACTER_STYLES["leader"]
            # Helping/supporting
            elif any(word in concept_lower for word in ["help", "support", "assist"]):
                return self.CHARACTER_STYLES["helper"]
            # Thinking/learning
            elif any(word in concept_lower for word in ["think", "idea", "learn", "realiz"]):
                return self.CHARACTER_STYLES["thinker"]

        # Default to developer character
        return self.CHARACTER_STYLES["developer"]

    def get_style_notes(self, context: "PromptContext") -> str:
        """Get style notes for carousel cover generation."""
        if context.style_notes:
            # Truncate to avoid prompt bloat
            return context.style_notes[:150]

        return (
            "Friendly cartoon character as main focus. "
            "Warm pastel colors, storybook illustration style. "
            "Character in upper portion, bottom empty for text overlay."
        )

    def get_layout_requirements(self) -> dict:
        """Get specific layout requirements for carousel covers."""
        return {
            "width": 512,
            "height": 768,
            "content_area_percent": 70,  # Top 70% for character
            "overlay_area_percent": 30,  # Bottom 30% for text
            "aspect_ratio": "portrait",
        }

