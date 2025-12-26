"""
Provider Package
================
Claude (Bedrock) for text, Nova Canvas + Titan for images.
No OpenAI dependencies.
"""

from .base import (
    TextModelProvider,
    ImageModelProvider,
    TextGenerationRequest,
    TextGenerationResponse,
    ImagePromptGenerationRequest,
    ImagePromptGenerationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImagePrompt,
    ImageFingerprint,
    GeneratedImage,
    ProviderError,
)
from .bedrock_text import BedrockTextProvider
from .titan_image import TitanImageProvider
from .nova_image import NovaCanvasProvider

__all__ = [
    # Base classes
    "TextModelProvider",
    "ImageModelProvider",
    # Text generation
    "TextGenerationRequest",
    "TextGenerationResponse",
    # Image prompt generation
    "ImagePromptGenerationRequest",
    "ImagePromptGenerationResponse",
    # Image generation
    "ImageGenerationRequest",
    "ImageGenerationResponse",
    "GeneratedImage",
    # Common models
    "ImagePrompt",
    "ImageFingerprint",
    # Error handling
    "ProviderError",
    # Provider implementations
    "BedrockTextProvider",
    "TitanImageProvider",
    "NovaCanvasProvider",
]

