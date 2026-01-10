"""
Constants and Enums
====================
Centralized definitions for all enums and constants.
"""

from enum import Enum


class PostLength(str, Enum):
    """LinkedIn post length options."""
    SHORT = "short"       # ~100-200 chars, punchy
    MEDIUM = "medium"     # ~300-600 chars, balanced
    LONG = "long"         # ~800-1200 chars, story-driven


class Tone(str, Enum):
    """Post tone options."""
    PROFESSIONAL = "professional"   # Formal, business-focused
    OPINIONATED = "opinionated"     # Bold, strong viewpoints
    REFLECTIVE = "reflective"       # Thoughtful, personal growth


class CTAStyle(str, Enum):
    """Call-to-action style."""
    QUESTION = "question"     # End with engaging question
    STATEMENT = "statement"   # End with bold statement
    NONE = "none"             # No explicit CTA


class TextProvider(str, Enum):
    """Text model providers - Ollama (uses 3-step pipeline) and Bedrock (Claude)."""
    OLLAMA = "ollama"  # Now uses 3-step pipeline internally for 95%+ success
    BEDROCK = "bedrock"


class ImageProvider(str, Enum):
    """Image model providers - Nova Canvas (recommended) + Titan + SDXL."""
    NOVA = "nova"
    TITAN = "titan"
    SDXL = "sdxl"


# Available text models - Ollama (Qwen/Mistral/Llama with 3-step pipeline) and Bedrock (Claude)
# Models marked with (Local) run on your machine, others use cloud APIs
TEXT_MODELS = {
    TextProvider.OLLAMA: [
        "qwen2.5:7b",          # (Local) Analytical & reasoning (uses 3-step pipeline)
        "mistral:7b",          # (Local) Professional content (uses 3-step pipeline)
        "llama3:8b",           # (Local) Creative content (uses 3-step pipeline)
    ],
    TextProvider.BEDROCK: [
        "claude-opus-4.5",     # Best quality (recommended default)
        "claude-opus-4.1",
        "claude-sonnet-4.5",
        "claude-haiku-4.5",    # Fast, cheap option
    ],
}

# Local model indicators for UI badges
LOCAL_TEXT_MODELS = ["qwen2.5:7b", "mistral:7b", "llama3:8b"]
LOCAL_IMAGE_MODELS = ["sdxl"]

# Default text model - Claude Opus 4.5 (best quality, recommended)
DEFAULT_TEXT_MODEL = "claude-opus-4.5"
DEFAULT_TEXT_PROVIDER = TextProvider.BEDROCK

# Default post generation parameters
DEFAULT_POST_LENGTH = PostLength.MEDIUM
DEFAULT_TONE = Tone.PROFESSIONAL
DEFAULT_CTA_STYLE = CTAStyle.QUESTION

# Available image models - Nova Canvas + Titan + SDXL (Local, recommended default)
# Note: Nova and Titan do NOT support text overlays like SDXL does
IMAGE_MODELS = {
    ImageProvider.NOVA: ["nova-canvas"],  # Cloud, no overlay support
    ImageProvider.TITAN: ["titan-image-generator-v2"],  # Cloud, no overlay support
    ImageProvider.SDXL: ["sdxl"],  # (Local) SDXL WebUI - supports overlays, recommended default
}

# Default image model - SDXL (free, local)
DEFAULT_IMAGE_MODEL = "sdxl"
DEFAULT_IMAGE_PROVIDER = ImageProvider.SDXL

# LinkedIn character limits
LINKEDIN_POST_MAX_CHARS = 3000
LINKEDIN_VISIBLE_CHARS = 140  # Before "see more"

# Default audiences (most common LinkedIn targets)
# NOTE: Order must match frontend/src/lib/defaults.ts
DEFAULT_AUDIENCES = [
    "founders",
    "executives",
    "leaders",
    "engineers",
    "developers",
]

# All available audience options
# NOTE: Order must match frontend/src/lib/defaults.ts
ALL_AUDIENCES = [
    "founders",
    "executives",
    "leaders",
    "engineers",
    "developers",
    "product managers",
    "marketers",
    "designers",
    "data scientists",
    "entrepreneurs",
    "investors",
    "consultants",
]

# Image generation constraints
IMAGE_STYLES = [
    "minimal",
    "abstract",
    "professional",
    "conceptual",
    "geometric",
    "gradient",
]

# Footer branding configuration
IMAGE_FOOTER_OPACITY = 0.85


# =============================================================================
# BRANDING FUNCTIONS (Load from .env via config.py)
# =============================================================================

def get_social_branding() -> dict:
    """
    Get social branding from environment configuration (.env file).

    Configure in .env:
        BRAND_NAME=Your Name
        BRAND_HANDLE=@yourusername
        BRAND_WEBSITE=yourwebsite.com
        BRAND_LINKEDIN_URL=linkedin.com/in/yourusername
        BRAND_INSTAGRAM_URL=instagram.com/yourusername
    """
    from ..config import settings
    return {
        "name": settings.brand_name,
        "handle": settings.brand_handle,
        "website": settings.brand_website,
        "linkedin_url": settings.brand_linkedin_url,
        "instagram_url": settings.brand_instagram_url,
    }


def get_branding_hashtag() -> str:
    """
    Get the branding hashtag from the configured name.
    Converts "Your Name" to "#YourName" for use in posts.
    """
    branding = get_social_branding()
    name = branding.get("name", "YourName")
    # Remove spaces and special characters, create hashtag
    hashtag = "".join(c for c in name if c.isalnum())
    return f"#{hashtag}"


def get_post_cta_footer(for_image: bool = False) -> str:
    """
    Get the CTA footer for image footers only.

    NOTE: Explicit CTAs hurt text post engagement - only used for images.
    """
    if for_image:
        branding = get_social_branding()
        name = branding.get("name", "Your Name")
        return f"+ Follow {name} for more insights"
    return ""


# Image generation limits
MIN_IMAGE_COUNT = 1
MAX_IMAGE_COUNT = 7
