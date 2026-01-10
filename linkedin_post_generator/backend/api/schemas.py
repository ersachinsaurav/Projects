"""
API Request/Response Schemas
=============================
Pydantic models for API validation and serialization.

Simplified single-user architecture (no multi-tenancy).
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator

from ..utils.constants import (
    PostLength, Tone, CTAStyle, TextProvider, ImageProvider,
    DEFAULT_AUDIENCES, DEFAULT_IMAGE_MODEL, DEFAULT_IMAGE_PROVIDER,
    DEFAULT_POST_LENGTH, DEFAULT_TONE, DEFAULT_CTA_STYLE,
    DEFAULT_TEXT_MODEL, DEFAULT_TEXT_PROVIDER,
)


# =============================================================================
# SHARED SCHEMAS
# =============================================================================

class ImagePromptSchema(BaseModel):
    """Single image prompt in response."""
    id: int
    concept: str = Field(default="", description="The specific concept from the post this image represents")
    prompt: str = Field(..., max_length=2500, description="Detailed image generation prompt")
    style_notes: str = ""
    composition_note: str = Field(default="", description="How the layout leaves room for the footer")
    negative_prompt: Optional[str] = Field(default=None, description="Negative prompt for image generation (SDXL-specific)")


class ImageFingerprintSchema(BaseModel):
    """Visual consistency parameters for all images."""
    visual_style: str = Field(default="minimal", description="minimal | geometric | gradient | conceptual")
    color_palette: str = "neutral"
    composition: str = Field(default="top-weighted", description="top-weighted | centered-upper | panoramic-horizon")
    lighting: str = "soft"
    concept_type: str = "abstract"


class ImageStrategySchema(BaseModel):
    """Image generation strategy decided during text generation."""
    image_count: int = Field(..., ge=0, le=7)
    reason: str


class ImageRecommendationSchema(BaseModel):
    """AI recommendation for what type of image would best complement the post."""
    recommended_type: str = Field(
        ...,
        description="post_card | cartoon_narrative | cartoon_abstract | abstract_minimal | infographic"
    )
    reasoning: str = Field(..., description="Chain-of-thought reasoning for this recommendation")
    confidence: str = Field(default="high", description="high | medium | low")
    alternative_types: list[str] = Field(
        default_factory=list,
        description="Other image types that could also work well"
    )
    style_notes: str = Field(default="", description="Specific style guidance for the recommended type")


class InfographicSectionSchema(BaseModel):
    """Section within an infographic text structure."""
    title: str = Field(..., description="Section title")
    bullets: list[str] = Field(default_factory=list, max_length=3, description="2-3 bullet points")


class InfographicTextStructureSchema(BaseModel):
    """Structured text for infographic overlays - extracted during text generation.

    This is generated once during text generation and reused during image rendering,
    avoiding a second LLM call for text extraction.
    """
    title: str = Field(..., description="Main headline (5-10 words)")
    subtitle: Optional[str] = Field(None, description="Optional context or problem statement")
    sections: list[InfographicSectionSchema] = Field(default_factory=list, max_length=3)
    takeaway: Optional[str] = Field(None, description="Strong closing statement or actionable insight")


# =============================================================================
# MODEL CONFIGS
# =============================================================================

class TextModelConfig(BaseModel):
    """Text model selection - Ollama (Mistral/Llama) or Bedrock (Claude)."""
    provider: TextProvider = DEFAULT_TEXT_PROVIDER
    model: str = DEFAULT_TEXT_MODEL


class ImageModelConfig(BaseModel):
    """Image model selection - SDXL (default, free, local), Nova Canvas, or Titan."""
    provider: ImageProvider = DEFAULT_IMAGE_PROVIDER
    model: str = DEFAULT_IMAGE_MODEL


# =============================================================================
# TEXT GENERATION SCHEMAS
# =============================================================================

class TextGenerationRequestSchema(BaseModel):
    """Request schema for POST /generate-text."""

    # Session identifier
    session_id: str = Field(..., min_length=1, max_length=100)

    # Core content
    idea: str = Field(..., min_length=10, max_length=2000)
    post_angle: Optional[str] = Field(None, max_length=500)
    draft_post: Optional[str] = Field(None, max_length=3000)

    # Generation parameters
    post_length: PostLength = DEFAULT_POST_LENGTH
    tone: Tone = DEFAULT_TONE
    audience: list[str] = Field(default_factory=lambda: list(DEFAULT_AUDIENCES), max_length=10)
    cta_style: CTAStyle = DEFAULT_CTA_STYLE

    # Model selection
    text_model: TextModelConfig = Field(default_factory=TextModelConfig)

    # Image generation flag - if False, only generate short_post (for post cards)
    generate_images: bool = Field(default=True, description="If True, generate image prompts. If False, only generate short_post.")

    # Image model selection (only used if generate_images=True)
    image_model: ImageModelConfig = Field(default_factory=ImageModelConfig)

    @field_validator("audience")
    @classmethod
    def validate_audience(cls, v):
        if not v:
            return list(DEFAULT_AUDIENCES)
        return [a.strip().lower() for a in v if a.strip()]


class TextGenerationResponseSchema(BaseModel):
    """Response schema for POST /generate-text."""

    # Generated content
    post_text: str = Field(..., description="LinkedIn-ready post text with Unicode formatting")
    short_post: str = Field(..., min_length=10, max_length=400, description="Punchy summary for post cards")
    hashtags: list[str] = Field(..., min_length=3, max_length=9, description="5-7 content hashtags + 2 branding hashtags")

    # Image recommendation (ALWAYS generated - helps user choose image type)
    image_recommendation: Optional[ImageRecommendationSchema] = None

    # Image-related fields (only if generate_images=True)
    image_strategy: Optional[ImageStrategySchema] = None
    image_prompts: list[ImagePromptSchema] = Field(default_factory=list)
    image_fingerprint: Optional[ImageFingerprintSchema] = None

    # Infographic text structure (generated during text generation to avoid second LLM call)
    # Used by InfographicRenderer for text overlays
    infographic_text: Optional[InfographicTextStructureSchema] = Field(
        None,
        description="Structured text for infographic overlays - reused during image rendering"
    )

    # Metadata
    session_id: str
    model_used: str
    image_model_used: str = Field(default="nova", description="Which image model prompts were generated for")
    tokens_used: Optional[int] = None
    generation_time_ms: Optional[int] = None

    @field_validator("hashtags")
    @classmethod
    def validate_hashtags(cls, v):
        validated = []
        for tag in v:
            tag = tag.strip()
            if not tag.startswith("#"):
                tag = f"#{tag}"
            tag = tag.replace(" ", "")
            validated.append(tag)
        return validated


# =============================================================================
# IMAGE PROMPT GENERATION SCHEMAS
# =============================================================================

class ImagePromptRequestSchema(BaseModel):
    """Request schema for POST /generate-image-prompts."""
    session_id: str = Field(..., min_length=1, max_length=100)
    post_text: Optional[str] = Field(None, max_length=3000)
    image_count: Optional[int] = Field(None, ge=1, le=7)
    text_model: TextModelConfig = Field(default_factory=TextModelConfig)
    image_model: ImageModelConfig = Field(default_factory=ImageModelConfig)


class ImagePromptResponseSchema(BaseModel):
    """Response schema for POST /generate-image-prompts."""
    image_prompts: list[ImagePromptSchema]
    image_fingerprint: ImageFingerprintSchema
    session_id: str
    post_text_used: str
    model_used: str
    generation_time_ms: Optional[int] = None


# =============================================================================
# IMAGE GENERATION SCHEMAS
# =============================================================================

class ImageGenerationRequestSchema(BaseModel):
    """Request schema for POST /generate-images."""
    session_id: str = Field(..., min_length=1, max_length=100)
    image_prompts: Optional[list[ImagePromptSchema]] = None
    image_fingerprint: Optional[ImageFingerprintSchema] = None
    image_model: ImageModelConfig = Field(default_factory=ImageModelConfig)
    generate_carousel: bool = Field(default=False, description="Generate carousel: AI cover + post card sections")
    # Note: post_text, short_post, and infographic_text are read from session
    # (stored during /generate-text call) to avoid duplication


class GeneratedImageSchema(BaseModel):
    """Single generated image."""
    id: int
    base64_data: str
    prompt_used: str
    concept: str = Field(default="")
    format: str = "png"
    width: int = 1024
    height: int = 1024


class ImageGenerationResponseSchema(BaseModel):
    """Response schema for POST /generate-images."""
    images: list[GeneratedImageSchema]
    pdf_base64: Optional[str] = None
    pdf_title: Optional[str] = Field(None, description="Title for PDF filename (for carousels)")
    session_id: str
    model_used: str
    image_count: int
    generation_time_ms: Optional[int] = None


# =============================================================================
# POST CARD GENERATION SCHEMAS
# =============================================================================

class PostCardGenerationRequestSchema(BaseModel):
    """Request schema for POST /generate-post-card."""
    session_id: str = Field(..., min_length=1, max_length=100)
    post_text: str = Field(..., min_length=1, max_length=2000)
    short_post: Optional[str] = Field(None, max_length=400)
    avatar_base64: Optional[str] = None
    name: str = "Your Name"  # Set via VITE_BRAND_NAME in .env
    handle: str = "@yourusername"  # Set via VITE_BRAND_HANDLE in .env
    verified: bool = False
    theme: Literal['dark', 'light'] = 'dark'


class PostCardGenerationResponseSchema(BaseModel):
    """Response schema for POST /generate-post-card."""
    post_card_base64: str
    format: str = "png"
    width: int = 1080
    height: int = 1080
    session_id: str
    theme: str
    generation_time_ms: Optional[int] = None


# =============================================================================
# ERROR & UTILITY SCHEMAS
# =============================================================================

class ErrorDetail(BaseModel):
    message: str
    code: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    version: str
    providers: dict[str, bool]


class ModelsResponse(BaseModel):
    text_models: dict[str, list[str]]
    image_models: dict[str, list[str]]
