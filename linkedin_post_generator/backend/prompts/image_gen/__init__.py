"""
Image Generation Prompts Package
=================================
Modular prompt system for different use cases and image models.

Structure:
- base.py: Base prompt utilities, shared styles, and model registry
- models/: Model-specific prompt builders (SDXL, Nova, Titan)
- usecases/: Use-case specific prompts (postcard, illustration, carousel)

Usage:
    from backend.prompts.image_gen import get_image_prompt

    prompt = get_image_prompt(
        usecase="carousel",
        model="sdxl",
        context={...}
    )
"""

from .base import (
    ImagePromptBuilder,
    PromptContext,
    get_image_prompt,
    get_negative_prompt_for_model,
    SUPPORTED_MODELS,
    SUPPORTED_USECASES,
)

__all__ = [
    "ImagePromptBuilder",
    "PromptContext",
    "get_image_prompt",
    "get_negative_prompt_for_model",
    "SUPPORTED_MODELS",
    "SUPPORTED_USECASES",
]

