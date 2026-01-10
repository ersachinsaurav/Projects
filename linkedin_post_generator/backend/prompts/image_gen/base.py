"""
Base Image Prompt Utilities
============================
Shared utilities, styles, and model/usecase registry for image generation prompts.
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Supported models and usecases
SUPPORTED_MODELS = ["sdxl", "nova", "titan"]
SUPPORTED_USECASES = ["postcard", "illustration", "carousel", "background"]


@dataclass
class PromptContext:
    """Context for generating image prompts."""
    # Content context
    title: Optional[str] = None
    subtitle: Optional[str] = None
    concept: Optional[str] = None
    style_notes: Optional[str] = None

    # Style preferences
    color_palette: Optional[str] = None
    visual_style: Optional[str] = None
    mood: Optional[str] = None

    # Layout requirements
    leave_space_bottom: bool = True
    bottom_space_percent: int = 30  # For carousel: 30%, for others: 15%

    # Additional context from Claude
    original_prompt: Optional[str] = None
    fingerprint: Optional[Dict] = None


class ImagePromptBuilder:
    """
    Central prompt builder that delegates to model-specific and usecase-specific builders.

    This class orchestrates prompt generation by:
    1. Getting the base style for the usecase
    2. Applying model-specific enhancements
    3. Combining with context-specific details
    """

    def __init__(self):
        # Import here to avoid circular imports
        from .models import sdxl, nova, titan
        from .usecases import postcard, illustration, carousel, background

        # Model builders
        self.model_builders = {
            "sdxl": sdxl.SDXLPromptBuilder(),
            "nova": nova.NovaPromptBuilder(),
            "titan": titan.TitanPromptBuilder(),
        }

        # Usecase builders
        self.usecase_builders = {
            "postcard": postcard.PostcardPromptBuilder(),
            "illustration": illustration.IllustrationPromptBuilder(),
            "carousel": carousel.CarouselPromptBuilder(),
            "background": background.BackgroundPromptBuilder(),
        }

    def build(
        self,
        usecase: str,
        model: str,
        context: PromptContext,
    ) -> Dict[str, str]:
        """
        Build a complete prompt for the given usecase and model.

        Returns:
            Dict with keys:
            - prompt: The main positive prompt
            - negative_prompt: The negative prompt (for models that support it)
            - style_notes: Additional style guidance
        """
        # Validate inputs
        if usecase not in SUPPORTED_USECASES:
            logger.warning(f"Unknown usecase '{usecase}', defaulting to 'illustration'")
            usecase = "illustration"

        if model not in SUPPORTED_MODELS:
            logger.warning(f"Unknown model '{model}', defaulting to 'sdxl'")
            model = "sdxl"

        # Get usecase-specific base prompt
        usecase_builder = self.usecase_builders[usecase]
        base_prompt = usecase_builder.get_base_prompt(context)

        # Get model-specific enhancements
        model_builder = self.model_builders[model]
        enhanced_prompt = model_builder.enhance_prompt(base_prompt, context)
        negative_prompt = model_builder.get_negative_prompt(usecase, context)

        # Get style notes
        style_notes = usecase_builder.get_style_notes(context)

        return {
            "prompt": enhanced_prompt,
            "negative_prompt": negative_prompt,
            "style_notes": style_notes,
        }


# Singleton instance
_builder_instance: Optional[ImagePromptBuilder] = None


def get_image_prompt(
    usecase: str,
    model: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Convenience function to get an image prompt.

    Args:
        usecase: One of "postcard", "illustration", "carousel"
        model: One of "sdxl", "nova", "titan"
        context: Dict with context values (will be converted to PromptContext)

    Returns:
        Dict with prompt, negative_prompt, and style_notes
    """
    global _builder_instance
    if _builder_instance is None:
        _builder_instance = ImagePromptBuilder()

    # Convert dict to PromptContext
    ctx = PromptContext()
    if context:
        for key, value in context.items():
            if hasattr(ctx, key):
                setattr(ctx, key, value)

    return _builder_instance.build(usecase, model, ctx)


def get_negative_prompt_for_model(model: str, usecase: str = "illustration") -> str:
    """Get the negative prompt for a specific model and usecase."""
    global _builder_instance
    if _builder_instance is None:
        _builder_instance = ImagePromptBuilder()

    model = model.lower() if model in SUPPORTED_MODELS else "sdxl"
    model_builder = _builder_instance.model_builders[model]
    return model_builder.get_negative_prompt(usecase, PromptContext())


# Shared style constants
SHARED_STYLES = {
    "linkedin_professional": {
        "color_keywords": "soft pastel, warm neutrals, professional blues, muted tones",
        "mood_keywords": "calm, thoughtful, approachable, professional",
        "quality_keywords": "high quality, clean lines, professional illustration",
    },
    "warm_friendly": {
        "color_keywords": "warm peach, soft coral, cream, light blue",
        "mood_keywords": "friendly, inviting, genuine, uplifting",
        "quality_keywords": "storybook style, editorial illustration, clean design",
    },
    "tech_minimal": {
        "color_keywords": "soft blues, light grays, white, subtle accents",
        "mood_keywords": "modern, clean, focused, professional",
        "quality_keywords": "minimal design, geometric shapes, flat illustration",
    },
}


def get_shared_style(style_name: str) -> Dict[str, str]:
    """Get a shared style preset."""
    return SHARED_STYLES.get(style_name, SHARED_STYLES["linkedin_professional"])

