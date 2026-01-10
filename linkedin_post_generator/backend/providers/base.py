"""
Provider Base Classes
======================
Abstract base classes defining the contract for text and image providers.
These ensure provider-agnostic code in the core flow.

Two-Phase Generation Architecture:
- Phase 1: Text + Hashtags + Image Strategy (TextGenerationResponse)
- Phase 2: Image Prompts grounded in text (ImagePromptGenerationResponse)
- Phase 3: Actual image generation (ImageGenerationResponse)
"""

from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, Field

from ..utils.constants import (
    DEFAULT_AUDIENCES,
    DEFAULT_POST_LENGTH,
    DEFAULT_TONE,
    DEFAULT_CTA_STYLE,
)


class TextGenerationRequest(BaseModel):
    """Standardized input for text generation (Phase 1)."""
    idea: str
    post_angle: Optional[str] = None
    draft_post: Optional[str] = None
    post_length: str = DEFAULT_POST_LENGTH.value
    tone: str = DEFAULT_TONE.value
    audience: list[str] = Field(default_factory=lambda: list(DEFAULT_AUDIENCES))
    cta_style: str = DEFAULT_CTA_STYLE.value
    session_id: Optional[str] = None  # For logging pipeline steps


class ImagePrompt(BaseModel):
    """Single image prompt with metadata."""
    id: int
    concept: str = Field(
        default="",
        description="The specific concept from the post this image represents"
    )
    prompt: str
    style_notes: str = Field(
        default="",
        description="Specific style guidance for this image"
    )
    composition_note: str = Field(
        default="",
        description="How the layout accommodates the footer"
    )
    negative_prompt: Optional[str] = Field(
        default=None,
        description="Negative prompt for image generation (SDXL-specific)"
    )


class ImageFingerprint(BaseModel):
    """Visual consistency parameters for image generation."""
    visual_style: str
    color_palette: str
    composition: str
    lighting: str
    concept_type: str


class InfographicSection(BaseModel):
    """Section within an infographic text structure."""
    title: str = Field(default="", description="Section title")
    bullets: list[str] = Field(default_factory=list, description="2-3 bullet points")


class InfographicTextStructure(BaseModel):
    """Structured text for infographic overlays.

    Generated during text generation to avoid a second LLM call for text extraction.
    """
    title: str = Field(..., description="Main headline (5-10 words)")
    subtitle: Optional[str] = Field(None, description="Optional context or problem statement")
    sections: list[InfographicSection] = Field(default_factory=list)
    takeaway: Optional[str] = Field(None, description="Strong closing statement")


class TextGenerationResponse(BaseModel):
    """
    Standardized output from text generation.

    Contains EVERYTHING in one call:
    - post_text: LinkedIn-ready with Unicode + emojis
    - short_post: Punchy summary for post cards
    - hashtags: Separate from body
    - image_strategy: Recommendation (user decides)
    - image_prompts: ALWAYS generated
    - image_fingerprint: Visual consistency
    - infographic_text: Pre-extracted text structure for infographic overlays
    """
    post_text: str = Field(
        ...,
        description="LinkedIn-ready text with Unicode formatting and strategic emojis. No markdown."
    )
    short_post: str = Field(
        ...,
        description="REQUIRED. Punchy 2-5 line summary for post cards. Max 280 chars."
    )
    hashtags: list[str] = Field(
        default_factory=list,
        description="3-5 relevant hashtags, separate from post body"
    )

    # Image recommendation (ALWAYS generated - helps user choose image type)
    image_recommendation: Optional[dict] = Field(
        default=None,
        description="AI recommendation: {recommended_type, reasoning, confidence, alternative_types, style_notes}"
    )

    # Image-related fields (only if generate_images=True)
    image_strategy: Optional[dict] = Field(
        default=None,
        description="Image generation strategy: {image_count: int, reason: str}"
    )
    image_prompts: list[ImagePrompt] = Field(
        default_factory=list,
        description="Image prompts grounded in post content. Only generated if generate_images=True."
    )
    image_fingerprint: Optional["ImageFingerprint"] = Field(
        default=None,
        description="Visual consistency parameters"
    )

    # Infographic text structure - pre-extracted to avoid second LLM call
    infographic_text: Optional[InfographicTextStructure] = Field(
        default=None,
        description="Structured text for infographic overlays - reused during image rendering"
    )

    # Metadata
    model_used: str
    tokens_used: Optional[int] = None
    raw_response: Optional[str] = None


class ImagePromptGenerationRequest(BaseModel):
    """Standardized input for image prompt generation (Phase 2)."""
    post_text: str = Field(
        ...,
        description="The finalized post text to ground image prompts in"
    )
    image_count: int = Field(..., ge=1, le=7)
    tone: str = DEFAULT_TONE.value
    audience: list[str] = Field(default_factory=lambda: list(DEFAULT_AUDIENCES))


class ImagePromptGenerationResponse(BaseModel):
    """
    Standardized output from image prompt generation (Phase 2).

    Prompts are grounded in the specific post content.
    """
    image_prompts: list[ImagePrompt]
    image_fingerprint: ImageFingerprint
    post_text_used: str

    # Metadata
    model_used: str
    tokens_used: Optional[int] = None
    raw_response: Optional[str] = None


class ImageGenerationRequest(BaseModel):
    """Standardized input for image generation."""
    prompts: list[ImagePrompt]
    fingerprint: ImageFingerprint
    post_text: str  # Context for image generation
    width: Optional[int] = None  # Optional width override (e.g., 512 for carousel)
    height: Optional[int] = None  # Optional height override (e.g., 512 for carousel)


class GeneratedImage(BaseModel):
    """Single generated image."""
    id: int
    base64_data: str
    prompt_used: str
    format: str = "png"
    width: int = 1024
    height: int = 1024


class ImageGenerationResponse(BaseModel):
    """Standardized output from image generation."""
    images: list[GeneratedImage]
    model_used: str
    generation_time_ms: Optional[int] = None


class TextModelProvider(ABC):
    """
    Abstract base class for text generation providers.

    Implementations must handle:
    - API authentication
    - Request formatting for specific model
    - Response parsing to standard format
    - Error handling and retries

    Two-Phase Generation:
    - generate(): Phase 1 - Text + Hashtags + Image Strategy
    - generate_image_prompts(): Phase 2 - Image prompts grounded in text
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'openai', 'bedrock')."""
        pass

    @property
    @abstractmethod
    def available_models(self) -> list[str]:
        """Return list of available model names."""
        pass

    @abstractmethod
    async def generate(
        self,
        request: TextGenerationRequest,
        model: str,
        system_prompt: str,
        max_tokens: int = 4000,
    ) -> TextGenerationResponse:
        """
        Generate LinkedIn post text (Phase 1).

        Args:
            request: Standardized generation request
            model: Specific model to use
            system_prompt: System prompt for the LLM
            max_tokens: Maximum output tokens

        Returns:
            Text + hashtags + image strategy (no image prompts)

        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def generate_image_prompts(
        self,
        request: ImagePromptGenerationRequest,
        model: str,
        system_prompt: str,
        max_tokens: int = 2000,
    ) -> ImagePromptGenerationResponse:
        """
        Generate image prompts grounded in finalized post text (Phase 2).

        Args:
            request: Contains finalized post text and image count
            model: Specific model to use
            system_prompt: System prompt for image prompt generation
            max_tokens: Maximum output tokens

        Returns:
            Image prompts with footer-aware compositions

        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def validate_model(self, model: str) -> bool:
        """Check if the specified model is available."""
        pass


class ImageModelProvider(ABC):
    """
    Abstract base class for image generation providers.

    Implementations must handle:
    - API authentication
    - Prompt formatting for specific model
    - Image retrieval and encoding
    - Error handling and fallbacks
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'openai', 'titan')."""
        pass

    @property
    @abstractmethod
    def available_models(self) -> list[str]:
        """Return list of available model names."""
        pass

    @abstractmethod
    async def generate(
        self,
        request: ImageGenerationRequest,
        model: str,
    ) -> ImageGenerationResponse:
        """
        Generate images based on prompts.

        Args:
            request: Standardized image generation request
            model: Specific model to use

        Returns:
            Standardized image generation response

        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def validate_model(self, model: str) -> bool:
        """Check if the specified model is available."""
        pass


class ProviderError(Exception):
    """Base exception for provider-related errors."""

    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ):
        self.message = message
        self.provider = provider
        self.model = model
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        parts = [f"[{self.provider}]"]
        if self.model:
            parts.append(f"[{self.model}]")
        parts.append(self.message)
        return " ".join(parts)

