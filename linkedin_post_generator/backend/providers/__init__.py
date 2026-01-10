"""
Provider Package
================
Text: Claude (Bedrock), Ollama (Qwen/Mistral/Llama)
Image: Nova Canvas, Titan, SDXL WebUI
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
from .ollama_text import OllamaTextProvider
from .titan_image import TitanImageProvider
from .nova_image import NovaCanvasProvider
from .sdxl_image import SDXLWebUIProvider

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
    "OllamaTextProvider",  # Now uses 3-step pipeline internally
    "TitanImageProvider",
    "NovaCanvasProvider",
    "SDXLWebUIProvider",
]

