"""
Health & Utility Routes
========================
Health check and utility endpoints.
"""

from fastapi import APIRouter

from ..config import settings
from ..utils.constants import TEXT_MODELS, IMAGE_MODELS
from .schemas import HealthCheckResponse, ModelsResponse


router = APIRouter(tags=["Health & Utility"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Check API health and provider availability."""
    providers_status = {
        "bedrock": True,  # Claude text models
        "nova": True,     # Nova Canvas (recommended for images)
        "titan": True,    # Titan (fallback for images)
    }

    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        providers=providers_status,
    )


@router.get("/models", response_model=ModelsResponse)
async def list_models():
    """List all available models."""
    return ModelsResponse(
        text_models={p.value: models for p, models in TEXT_MODELS.items()},
        image_models={p.value: models for p, models in IMAGE_MODELS.items()},
    )

