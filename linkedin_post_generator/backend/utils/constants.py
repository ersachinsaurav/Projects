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
    """Text model providers - Claude only."""
    BEDROCK = "bedrock"


class ImageProvider(str, Enum):
    """Image model providers - Nova Canvas (recommended) + Titan."""
    NOVA = "nova"
    TITAN = "titan"


# Available text models - Claude only (via Bedrock)
TEXT_MODELS = {
    TextProvider.BEDROCK: [
        "claude-opus-4.5",     # Default, best quality
        "claude-opus-4.1",
        "claude-opus-4",
        "claude-sonnet-4.5",
        "claude-sonnet-4",
        "claude-haiku-4.5",    # Fast, cheap option
    ],
}

# Default text model
DEFAULT_TEXT_MODEL = "claude-opus-4.5"
DEFAULT_TEXT_PROVIDER = TextProvider.BEDROCK

# Available image models - Nova Canvas (recommended) + Titan
IMAGE_MODELS = {
    ImageProvider.NOVA: ["nova-canvas"],  # Recommended, higher quality
    ImageProvider.TITAN: ["titan-image-generator-v2"],  # Fallback
}

# Default image model - Nova Canvas is better quality
DEFAULT_IMAGE_MODEL = "nova-canvas"
DEFAULT_IMAGE_PROVIDER = ImageProvider.NOVA

# LinkedIn character limits
LINKEDIN_POST_MAX_CHARS = 3000
LINKEDIN_VISIBLE_CHARS = 140  # Before "see more"

# Default audiences (most common LinkedIn targets)
DEFAULT_AUDIENCES = [
    "founders",
    "engineers",
    "leaders",
    "developers",
]

# All available audience options
ALL_AUDIENCES = [
    "founders",
    "engineers",
    "leaders",
    "developers",
    "marketers",
    "designers",
    "product managers",
    "data scientists",
    "executives",
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

# Always generate at least 1 image prompt
MIN_IMAGE_COUNT = 1
MAX_IMAGE_COUNT = 7
