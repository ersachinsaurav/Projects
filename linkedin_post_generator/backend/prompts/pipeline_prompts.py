"""
3-Step Pipeline Prompts for Ollama + Qwen 2.5 7B
=================================================
Production-ready prompt templates designed for 95%+ success rate.

Philosophy:
- One cognitive task per step
- No negative constraints in early stages
- No strict formatting until content is frozen
- Model never reasons about JSON and prose simultaneously
- All brittle rules are enforced AFTER generation

STEP 1: Content Generation (Creativity) - Temp: 0.6-0.7
STEP 2: Style Normalization (Editing)   - Temp: 0.2
STEP 3: JSON Packaging (Mechanical)     - Temp: 0.1

Reference: https://github.com/ggerganov/llama.cpp/discussions
"""

from typing import Optional


# =============================================================================
# STEP 1: CONTENT GENERATION (Idea Fidelity Only)
# =============================================================================
# Goal: Generate high-quality long-form content that:
# - Stays on the idea
# - Respects the angle
# - Sounds like a senior practitioner
# - IGNORES formatting, emojis, JSON, hashtags
#
# This is where 7B models are STRONGEST.
# Temperature: 0.6-0.7 | Max tokens: ~1500 | Retries: 1
# =============================================================================

def get_step1_system_prompt() -> str:
    """
    System prompt for Step 1: Content Generation.

    KEEP IT SHORT - Ollama injects its own system context.
    Qwen 7B degrades when system prompt is long + authoritative.
    """
    return "You write LinkedIn posts that feel like quiet discoveries, not advice. Story-first, insight-earned."


def get_step1_user_prompt(
    idea: str,
    post_angle: Optional[str] = None,
    draft_post: Optional[str] = None,
    post_length: str = "medium",
    tone: str = "professional",
    audience: list[str] = None,
) -> str:
    """
    Build Step 1 user prompt for content generation.

    Key principles:
    - No ASCII policing
    - No forbidden phrase list
    - No schema
    - Clear structure but low pressure
    - Single creative task
    - Flexible structure (no strict section headers)
    """
    audience = audience or ["tech professionals"]
    audience_str = ", ".join(audience)

    # Map post_length to word counts and paragraph guidance
    length_guidance = {
        "short": ("80-150 words", "3-4 paragraphs"),
        "medium": ("150-300 words", "4-5 paragraphs"),
        "long": ("350-600 words", "5-7 paragraphs"),
    }
    word_count, para_count = length_guidance.get(post_length, ("150-300 words", "4-5 paragraphs"))

    # Build the prompt - using the viral discovery arc pattern
    parts = [
        f"Write a LinkedIn post ({word_count}, {para_count}).",
        "",
        "WHO YOU ARE:",
        "A senior tech lead who DISCOVERS insights through observation.",
        "You position as a LEARNER who noticed something, not an expert teaching.",
        "Your tone is calm, reflective, and peer-to-peer.",
        "",
        "POLISH RULES (make every sentence stronger):",
        "- Prefer OBSERVATIONAL over DECLARATIVE statements",
        '- Use CONFIDENT language, avoid qualifiers like "just", "often", "usually"',
        '  WEAKER: "They just notice their work getting done."',
        '  STRONGER: "They notice their work getting done."',
        "- Keep RHYTHM CONSISTENT within repeated patterns",
        '  WEAKER: "Day one: nothing. Week one: still nothing. Week two: silence."',
        '  STRONGER: "Day one: silence. Week one: silence. Week two: still silence."',
        "- When describing data, use ACTIVE verbs for flow",
        '  WEAKER: "Hundreds of packets generated."',
        '  STRONGER: "Hundreds of packets being generated."',
        "",
        f"TOPIC: {idea}",
    ]

    if post_angle:
        parts.extend([
            f"ANGLE: {post_angle}",
        ])

    parts.extend([
        f"AUDIENCE: {audience_str}",
    ])

    if draft_post:
        parts.extend([
            "",
            "DRAFT TO IMPROVE (rewrite using the structure below):",
            f"{draft_post}",
        ])

    parts.extend([
        "",
        "VIRAL POST STRUCTURE (follow this discovery arc):",
        "1. OPENING SCENE (1-2 sentences) - Start with a MOMENT, not an opinion",
        '   Example: "Last week, I noticed..." or "A teammate showed me..."',
        "   NEVER open with an insight or thesis",
        "",
        "2. INITIAL DISMISSAL (1-2 sentences) - Show you almost ignored it",
        '   Example: "I almost scrolled past..." or "It seemed too simple..."',
        "",
        "3. OBSERVATION (2-4 sentences) - Watch the pattern unfold",
        "   Introduce a character, describe concrete behaviors",
        "",
        "4. QUIET CONTRAST (2-3 sentences) - Show the tension",
        '   Example: "Meanwhile, I was..."',
        "",
        "5. DELAYED REALIZATION (1-2 sentences) - The insight emerges",
        '   Example: "That\'s when I noticed..."',
        "",
        "6. IDENTITY REFRAME (1-2 sentences) - What changed in your thinking",
        "",
        "7. CLOSING QUESTION (1 sentence) - Easy to answer, invites memory",
        '   NOT: "What do you think?"',
        '   YES: "What small thing have you noticed that stuck with you?"',
        "",
        "WHAT TO AVOID:",
        "- Opening with an insight or opinion (kills curiosity)",
        "- Bullet points (signal you can skim)",
        "- Positioning as the expert with answers",
        "- Explicit CTAs like 'Repost' or 'Follow'",
        "",
        "STYLE:",
        "- Write naturally, like you're reflecting to a peer",
        "- Use concrete examples and specific details",
        "- No emojis, no hashtags (we add those later)",
        "",
        "Write the post now:",
    ])

    return "\n".join(parts)


# =============================================================================
# STEP 2: STYLE + CONSTRAINT NORMALIZATION
# =============================================================================
# Goal: Turn Step 1 output into policy-compliant prose:
# - ASCII-only
# - Sentence counts enforced
# - Tone tightened
# - Forbidden phrases removed
# - STILL NO JSON
#
# This step is purely transformational, NOT creative.
# Temperature: 0.2 | Max tokens: ~1500 | Retries: 2
# =============================================================================

def get_step2_system_prompt() -> str:
    """System prompt for Step 2: Style Normalization."""
    return "You are editing professional writing for clarity and consistency."


def get_step2_user_prompt(step1_output: str) -> str:
    """
    Build Step 2 user prompt for style normalization.

    Key principles:
    - Model EDITS instead of inventing
    - Negative constraints now apply to stable text
    - Sentence counting is easier than generation
    - 7B models are GOOD at rewriting
    """
    return f"""Below is a LinkedIn post draft. Rewrite it to improve clarity and flow.

---BEGIN POST---
{step1_output}
---END POST---

YOUR TASK:
1. Keep all the ideas and examples from the post above.
2. Remove section headers like [Opening observation] - make it flow naturally.
3. Use short paragraphs (1-3 sentences each).
4. Keep a calm, reflective, peer-to-peer tone.
5. Ensure the insight is DELAYED (not revealed in opening).
6. End with a question that's easy to answer and invites shared experience.

REMOVE these phrases if present:
- As a senior engineer
- In today's fast-paced world
- Let's talk about
- Have you ever wondered
- It's no secret that
- Repost to spread the word
- Follow for more

PUNCTUATION RULES:
- Periods and commas go INSIDE closing quotes (American style)
- CORRECT: "This is correct."
- WRONG: "This is wrong".

STRUCTURE CHECK:
- Does the post OPEN with a scene/moment (not opinion)?
- Is there CONTRAST between expectation and reality?
- Is the insight EARNED through the story, not stated upfront?

DO NOT:
- Add emojis
- Add hashtags
- Add explicit CTAs ("Repost", "Follow", etc.)
- Add bullet points
- Echo these instructions

OUTPUT:
Write ONLY the rewritten post. Nothing else."""


# =============================================================================
# STEP 3: PACKAGING + METADATA (Mechanical Output)
# =============================================================================
# Goal: Wrap already-clean text into:
# - JSON
# - short_post
# - hashtags
# - image metadata
# - emojis (ONLY here)
#
# This step is mostly deterministic.
# Temperature: 0.1 | Max tokens: ~2000 | Retries: 3
# =============================================================================

def get_step3_system_prompt() -> str:
    """System prompt for Step 3: JSON Packaging."""
    return "You are a JSON formatter. Output ONLY valid JSON, nothing else. No explanations."


def get_step3_user_prompt(step2_output: str, author_hashtags: list[str] = None) -> str:
    """
    Build Step 3 user prompt for JSON packaging.

    Key principles:
    - Model is no longer thinking about content
    - JSON errors drop sharply
    - Emoji misplacement becomes rare
    - Can re-run Step 3 independently if it fails
    - NO GENERIC PLACEHOLDERS - force model to extract from content
    """
    from ..utils.constants import get_branding_hashtag
    if author_hashtags is None:
        author_hashtags = [get_branding_hashtag()]  # Single branding tag only

    hashtags_str = ", ".join(f'"{h}"' for h in author_hashtags)
    hashtags_list_example = ", ".join(f'"{h}"' for h in author_hashtags)

    return f"""Convert this LinkedIn post into JSON.

POST TO CONVERT:
---
{step2_output}
---

INSTRUCTIONS:
1. "post_text": Copy the post above. Add \\n\\n between paragraphs. Add 1-2 emojis MAXIMUM (placed naturally, not at every paragraph start).
2. "short_post": DISTILL the post into 5-8 SHORT punchy lines (3-10 words each). Open with ACTION. Use REPETITION for rhythm. SPLIT the insight into 2 short lines. NO emojis. NO hashtags. Use \\n between lines. Use CONFIDENT language (avoid "just").
3. "hashtags": Create 3-4 content hashtags from the post's topics, THEN add {hashtags_str} at the end (4-5 total). ONLY use {hashtags_str} as the personal branding tag - DO NOT add any other personal branding hashtags like #YogevCodes, #CodeWithMJ, etc.
4. "image_recommendation.reasoning": Write 1 sentence explaining why post_card fits THIS specific post's topic.
5. "image_prompts[0].concept": Describe the main visual idea from THIS post (not generic).
6. "image_prompts[0].prompt": Write a detailed image prompt based on the post's actual content.
7. "infographic_text.title": Extract the core insight/realization from the post (5-10 words).
8. "infographic_text.takeaway": Write the identity shift or key lesson from the post.

EMOJI RULES:
- Use 1-2 emojis MAXIMUM in the entire post (prefer none)
- NEVER place emoji at paragraph start (manufactured look)
- Place naturally where emphasis helps

SHORT_POST EXAMPLE (optimal rhythm):
Shipped a high-stakes legal workflow feature.
Waited for bug reports.
Day one: silence.
Week one: silence.
Week two: still silence.
The most satisfying sound in engineering is silence.
When your code becomes invisible.
Users notice their work getting done.

CRITICAL:
- Do NOT use placeholder text. Extract real content from the post.
- Do NOT add CTAs like "Repost" or "Follow" in post_text.

OUTPUT ONLY THIS JSON (start with {{ end with }}):
{{
  "post_text": "[Full post with emojis and paragraph breaks]",
  "short_post": "[5-8 SHORT punchy lines with rhythm, use confident language]",
  "hashtags": ["#Topic1", "#Topic2", "#Topic3", "#Topic4", {hashtags_list_example}],
  "image_recommendation": {{
    "recommended_type": "post_card | text_only | cartoon_narrative | cartoon_abstract",
    "reasoning": "[Chain-of-thought: If post is about silence/absence, text_only may work best. Explain why.]",
    "confidence": "high",
    "alternative_types": ["text_only", "cartoon_abstract"],
    "style_notes": "Clean professional style. For serious topics (legal, evictions), avoid cartoon styles.",
    "text_only_rationale": "[If post is about quiet success or invisible work, explain why images may add noise]"
  }},
  "image_strategy": {{
    "image_count": 1,
    "reason": "One image to complement the post. For quiet/reflective posts, 0 images (text_only) may perform better."
  }},
  "image_prompts": [
    {{
      "id": 1,
      "concept": "[Specific visual concept from THIS post]",
      "prompt": "FOR SERIOUS topics (legal, infra, reliability): Minimal abstract illustration representing system reliability and quiet success, soft muted color palette (sage green, cream), clean professional style, no characters, no text, simple shapes suggesting stability, calm balanced composition, generous negative space, modern editorial style. FOR LIGHTER topics: Modern cartoon illustration, warm pastel palette, cartoon character, desk with computer, bottom 30% empty solid pastel for text, no text no words no labels.",
      "style_notes": "AVOID cartoon styles for serious topics (legal, evictions, reliability). Prefer abstract/symbolic for quiet success themes.",
      "composition_note": "Main content in upper 70%, bottom empty",
      "negative_prompt": "text, words, labels, watermark, blurry, excited expression, celebrating",
      "prompt_variant": "abstract_symbolic for serious topics, cartoon for lighter stories"
    }}
  ],
  "image_fingerprint": {{
    "visual_style": "editorial | abstract_symbolic",
    "color_palette": "soft pastel or muted sage/cream",
    "composition": "top-weighted with generous negative space",
    "lighting": "soft ambient",
    "concept_type": "symbolic of quiet confidence"
  }},
  "infographic_text": {{
    "title": "[Observational headline (5-10 words, NOT a slogan)]",
    "subtitle": "[Optional context line]",
    "sections": [
      {{
        "title": "Before/What We Expect",
        "bullets": ["High stakes", "Complex rules", "Many ways things could break"]
      }},
      {{
        "title": "After/What Actually Matters",
        "bullets": ["No alerts", "No urgent messages", "No support tickets"]
      }}
    ],
    "takeaway": "The best code disappears. Users notice their work getting done.",
    "infographic_guidance": "Use ONLY when sharing a framework or seeking saves/bookmarks. SKIP when insight is emotional or pacing matters. Max 2 sections. Generalize bullets for reuse. PREFER PROGRESSION-BASED structure (Before→After, Anti-pattern→Failure→Fix) over CATEGORICAL lists."
  }}
}}"""


# =============================================================================
# RUNTIME CONFIGURATION
# =============================================================================

class PipelineConfig:
    """
    Recommended runtime settings for Ollama + Qwen 2.5 7B.

    These settings are model-specific and battle-tested.
    """

    # Step 1: Content Generation (Creative)
    STEP1_TEMPERATURE = 0.6
    STEP1_TOP_P = 0.9
    STEP1_MAX_TOKENS = 1500
    STEP1_RETRIES = 1

    # Step 2: Style Normalization (Editing)
    STEP2_TEMPERATURE = 0.2
    STEP2_TOP_P = 0.9
    STEP2_MAX_TOKENS = 1500
    STEP2_RETRIES = 2

    # Step 3: JSON Packaging (Mechanical)
    STEP3_TEMPERATURE = 0.1
    STEP3_TOP_P = 0.9
    STEP3_MAX_TOKENS = 2000
    STEP3_RETRIES = 3

    # Shared settings
    REPEAT_PENALTY = 1.1
    NUM_CTX = 4096


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_step1_output(output: str) -> tuple[bool, list[str]]:
    """
    Validate Step 1 output has reasonable content.

    We no longer require strict section headers since 7B models
    don't follow them consistently. Instead, we check for:
    - Minimum length
    - Multiple paragraphs
    - Ends with a question (optional)

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check for basic content length
    if len(output) < 200:
        errors.append("Output too short (< 200 chars)")

    # Check for multiple paragraphs (at least 2)
    paragraphs = [p.strip() for p in output.split('\n\n') if p.strip()]
    if len(paragraphs) < 2:
        # Try single newline split
        paragraphs = [p.strip() for p in output.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            errors.append("Output lacks paragraph structure")

    # Check that it doesn't contain common error patterns
    error_patterns = [
        "I cannot",
        "I'm sorry",
        "As an AI",
        "I don't have",
    ]
    for pattern in error_patterns:
        if pattern.lower() in output.lower()[:100]:
            errors.append(f"Output contains error pattern: {pattern}")

    return len(errors) == 0, errors


def validate_step2_output(output: str) -> tuple[bool, list[str]]:
    """
    Validate Step 2 output for style compliance.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check for forbidden phrases
    forbidden = [
        "As a senior engineer",
        "In today's fast-paced world",
        "Let's talk about",
        "Have you ever wondered",
        "It's no secret that",
    ]

    for phrase in forbidden:
        if phrase.lower() in output.lower():
            errors.append(f"Contains forbidden phrase: '{phrase}'")

    # Check for emojis (should not have any yet)
    import re
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    if emoji_pattern.search(output):
        errors.append("Contains emojis (should not have any in Step 2)")

    # Check for hashtags
    if re.search(r'#\w+', output):
        errors.append("Contains hashtags (should not have any in Step 2)")

    return len(errors) == 0, errors


def validate_step3_output(output: str, author_hashtags: list[str] = None) -> tuple[bool, list[str]]:
    """
    Validate Step 3 JSON output.

    Returns:
        (is_valid, list_of_errors)
    """
    import json
    import re

    errors = []

    # Try to parse JSON
    try:
        # Clean the output first
        cleaned = output.strip()
        if cleaned.startswith("```"):
            # Extract from code block
            match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', cleaned)
            if match:
                cleaned = match.group(1).strip()

        # Find JSON boundaries
        start_idx = cleaned.find('{')
        if start_idx == -1:
            errors.append("No JSON object found")
            return False, errors

        cleaned = cleaned[start_idx:]

        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {str(e)}")
        return False, errors

    # Validate required fields
    required_fields = ["post_text", "short_post", "hashtags"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # Validate hashtags
    from ..utils.constants import get_branding_hashtag
    if author_hashtags is None:
        author_hashtags = [get_branding_hashtag()]  # Single branding tag only

    hashtags = data.get("hashtags", [])
    if len(hashtags) < 4:
        errors.append(f"Expected at least 4 hashtags (3 content + 1 branding), got {len(hashtags)}")

    for required_tag in author_hashtags:
        if required_tag not in hashtags:
            errors.append(f"Missing required hashtag: {required_tag}")

    # Count emojis in post_text
    post_text = data.get("post_text", "")
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    emojis = emoji_pattern.findall(post_text)
    emoji_count = sum(len(e) for e in emojis)

    # Be very lenient with emoji count for 7B models - 0 is acceptable, we'll add them in post-processing if needed
    # Emoji validation is a WARNING, not an ERROR
    if emoji_count == 0:
        # Log warning but don't fail - we'll add emojis in post-processing if needed
        pass  # Emojis can be added in post-processing
    elif emoji_count > 15:
        errors.append(f"Too many emojis in post_text: {emoji_count} (need 3-5)")

    # Validate short_post has no emojis
    short_post = data.get("short_post", "")
    if emoji_pattern.search(short_post):
        errors.append("short_post contains emojis (should not)")

    # Validate short_post has no hashtags - SOFT warning, we can strip them
    # if re.search(r'#\w+', short_post):
    #     errors.append("short_post contains hashtags (should not)")
    # Note: We'll strip hashtags from short_post in post-processing instead of failing

    return len(errors) == 0, errors


def count_sentences(text: str) -> int:
    """Count sentences in text (simple heuristic)."""
    import re
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def extract_section(text: str, header: str) -> str:
    """Extract content under a section header."""
    import re

    # Escape special characters in header
    escaped = re.escape(header)

    # Find content between this header and the next header or end
    pattern = f"{escaped}\n(.+?)(?=\\[|$)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()
    return ""

