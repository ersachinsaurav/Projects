"""
Image Enhancement Prompts
==========================
Additional prompts for image generation optimization.
"""


def get_image_enhancement_prompt() -> str:
    """
    Return instructions for enhancing image prompts.

    This is used to refine raw image prompts before sending to image models.
    """
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

    Used by models that support negative prompts (like Titan).
    """
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
    """
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

