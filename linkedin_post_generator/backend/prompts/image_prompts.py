"""
Image Enhancement Prompts (LEGACY)
===================================
DEPRECATED: These functions are superseded by the new image_gen/ module.

The new system provides:
- Model-specific prompt builders: image_gen/models/ (nova.py, sdxl.py, titan.py)
- Use-case handlers: image_gen/usecases/ (carousel.py, illustration.py, postcard.py)
- Main entry point: get_image_prompt() and get_negative_prompt_for_model()

These legacy functions are kept for backward compatibility but are NOT actively used.
Consider using the new image_gen module instead.
"""

import warnings


def get_image_enhancement_prompt() -> str:
    """
    Return instructions for enhancing image prompts.

    DEPRECATED: Use image_gen module instead.
    This is used to refine raw image prompts before sending to image models.
    """
    warnings.warn(
        "get_image_enhancement_prompt is deprecated. Use image_gen module instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return '''You are an AI image prompt engineer specializing in professional,
LinkedIn-appropriate imagery.

## Your Task
Enhance the given image prompt to produce high-quality, professional images
suitable for LinkedIn posts.

## Image Constraints (MANDATORY)
1. NO TEXT - Never include any text, words, letters, or numbers in images
2. NO PEOPLE'S FACES - Avoid showing identifiable faces
3. PROFESSIONAL - Business-appropriate aesthetics
4. MINIMAL - Clean, uncluttered compositions
5. ABSTRACT - Conceptual rather than literal where possible

## Style Guidelines
- Modern, contemporary aesthetic
- High contrast for feed visibility
- Colors that pop on white/light backgrounds
- Avoid: clichés, stock photo vibes, clipart feel

## Output
Return ONLY the enhanced prompt. No explanation.'''


def get_negative_prompt() -> str:
    """
    Return negative prompt for image generation.

    DEPRECATED: Use get_negative_prompt_for_model() from image_gen module instead.
    Used by models that support negative prompts (like Titan).
    """
    warnings.warn(
        "get_negative_prompt is deprecated. Use get_negative_prompt_for_model() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return '''text, words, letters, numbers, watermark, signature,
logo, brand name, writing, caption, label,
blurry, low quality, distorted, ugly, deformed,
people, faces, humans, portraits, selfies,
stock photo, generic, cliché, clipart,
NSFW, inappropriate, unprofessional,
busy, cluttered, chaotic, messy'''


def get_linkedin_image_style_presets() -> dict:
    """
    Return preset style configurations for different LinkedIn post types.

    DEPRECATED: The new image_gen module handles styles internally per usecase.
    """
    warnings.warn(
        "get_linkedin_image_style_presets is deprecated. Use image_gen usecases instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return {
        "thought_leadership": {
            "visual_style": "minimal",
            "color_palette": "navy blue, white, subtle gold accents",
            "composition": "centered",
            "lighting": "soft ambient",
            "concept_type": "abstract symbolic",
        },
        "success_story": {
            "visual_style": "gradient",
            "color_palette": "warm sunrise colors, orange to gold",
            "composition": "ascending diagonal",
            "lighting": "dramatic",
            "concept_type": "metaphorical journey",
        },
        "tech_insight": {
            "visual_style": "geometric",
            "color_palette": "electric blue, cyan, white",
            "composition": "grid-based",
            "lighting": "studio",
            "concept_type": "abstract data visualization",
        },
        "personal_story": {
            "visual_style": "soft gradient",
            "color_palette": "muted earth tones, warm neutrals",
            "composition": "rule-of-thirds",
            "lighting": "natural soft",
            "concept_type": "symbolic objects",
        },
        "controversial_take": {
            "visual_style": "high contrast",
            "color_palette": "bold red and black, white space",
            "composition": "asymmetric tension",
            "lighting": "dramatic shadows",
            "concept_type": "conceptual clash",
        },
    }

