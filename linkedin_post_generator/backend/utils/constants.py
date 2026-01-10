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

# Social branding for footer
SOCIAL_BRANDING = {
    "handle": "@ersachinsaurav",
    "website": "sachinsaurav.dev",
    "linkedin_url": "linkedin.com/in/ersachinsaurav",
    "instagram_url": "instagram.com/ersachinsaurav",
}

# CTA footer for text content
# NOTE: Explicit CTAs like "Repost" and "Follow" HURT engagement and make posts feel "creator-optimized"
# Strong content earns engagement without asking. Only used for image footers now.
def get_post_cta_footer(for_image: bool = False) -> str:
    """
    Get the CTA footer to append to images only.

    IMPORTANT: Explicit "Repost" and "Follow" CTAs hurt text post engagement.
    Research shows they trigger "creator post" detection and reduce shares.
    Only use for image footers where branding is expected.

    Args:
        for_image: If True, returns single-line CTA for image footer.
                   If False, returns EMPTY string (no CTA for text posts).

    Returns:
        CTA footer for images only, empty string for text posts
    """
    name = SOCIAL_BRANDING.get("name", "Sachin Saurav")

    if for_image:
        # Single line for image footer - NO EMOJIS (fonts don't render them properly)
        return f"+ Follow {name} for more insights"
    else:
        # NO CTA for text posts - strong content earns engagement without asking
        return ""


# Branding name for consistency
SOCIAL_BRANDING["name"] = "Sachin Saurav"

# Always generate at least 1 image prompt
MIN_IMAGE_COUNT = 1
MAX_IMAGE_COUNT = 7
