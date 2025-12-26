"""
Provider Factory
=================
Factory functions for creating text and image provider instances.
"""

from fastapi import HTTPException, status

from ..providers import BedrockTextProvider, TitanImageProvider, NovaCanvasProvider
from ..utils.constants import TextProvider, ImageProvider


def get_text_provider(provider: TextProvider):
    """
    Get the appropriate text provider instance - Claude only.

    Args:
        provider: The text provider enum value

    Returns:
        An instance of the text provider

    Raises:
        HTTPException: If provider is unknown
    """
    if provider == TextProvider.BEDROCK:
        return BedrockTextProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown text provider: {provider}. Only 'bedrock' (Claude) is supported.",
    )


def get_image_provider(provider: ImageProvider):
    """
    Get the appropriate image provider instance - Nova Canvas (recommended) or Titan.

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

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown image provider: {provider}. Use 'nova' (recommended) or 'titan'.",
    )

