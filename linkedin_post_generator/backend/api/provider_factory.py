"""
Provider Factory
=================
Factory functions for creating text and image provider instances.
"""

from fastapi import HTTPException, status

from ..providers import BedrockTextProvider, OllamaTextProvider, TitanImageProvider, NovaCanvasProvider, SDXLWebUIProvider
from ..utils.constants import TextProvider, ImageProvider


def get_text_provider(provider: TextProvider):
    """
    Get the appropriate text provider instance.

    Providers:
    - 'ollama': Ollama with 3-step pipeline (Qwen/Mistral/Llama) - 95%+ success rate
    - 'bedrock': AWS Bedrock (Claude)

    Args:
        provider: The text provider enum value (or string that will be converted)

    Returns:
        An instance of the text provider

    Raises:
        HTTPException: If provider is unknown
    """
    # Handle both enum and string inputs
    provider_str = provider.value if hasattr(provider, 'value') else str(provider)

    if provider_str == TextProvider.OLLAMA.value or provider_str == "ollama":
        # OllamaTextProvider now uses 3-step pipeline internally
        return OllamaTextProvider()
    elif provider_str == TextProvider.BEDROCK.value or provider_str == "bedrock":
        return BedrockTextProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown text provider: {provider_str}. Supported: 'ollama' or 'bedrock'.",
    )


def get_image_provider(provider: ImageProvider):
    """
    Get the appropriate image provider instance - Nova Canvas (recommended), Titan, or SDXL.

    Args:
        provider: The image provider enum value

    Returns:
        An instance of the image provider

    Raises:
        HTTPException: If provider is unknown
    """
    if provider == ImageProvider.NOVA:
        return NovaCanvasProvider()
    elif provider == ImageProvider.TITAN:
        return TitanImageProvider()
    elif provider == ImageProvider.SDXL:
        return SDXLWebUIProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown image provider: {provider}. Use 'nova' (recommended), 'titan', or 'sdxl'.",
    )

