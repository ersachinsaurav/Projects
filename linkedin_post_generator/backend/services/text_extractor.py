"""
Text Extractor for Infographics
================================
Uses LLM to extract structured text sections from post content for infographic overlays.
"""

import json
import logging
from typing import Optional, Dict, List

from ..providers import BedrockTextProvider, ProviderError
from ..api.provider_factory import get_text_provider
from ..utils.constants import TextProvider

logger = logging.getLogger(__name__)


TEXT_EXTRACTION_PROMPT = """You are an expert at extracting structured content from LinkedIn posts for infographic overlays.

## TASK
Extract the following from the post text:
1. A compelling title (main headline, 5-10 words)
2. A subtitle/context (optional, 1-2 sentences)
3. Key sections with bullets (2-3 sections max, 2-3 bullets each)
4. A takeaway message (strong closing statement)

## RULES
- Title should be punchy and attention-grabbing
- Subtitle provides context or sets up the problem
- Sections should have clear titles and concise bullets
- Takeaway should be memorable and actionable
- Keep all text concise - infographics need brevity
- Remove Unicode formatting (bold, etc.) - keep plain text

## OUTPUT FORMAT (STRICT JSON)
{
  "title": "Main headline (5-10 words)",
  "subtitle": "Optional context or problem statement (1-2 sentences)",
  "sections": [
    {
      "title": "Section title",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]
    }
  ],
  "takeaway": "Strong closing statement or actionable insight"
}

## CRITICAL
- Return ONLY valid JSON
- No markdown code blocks
- Start with { and end with }
- Max 3 sections, max 3 bullets per section
- All text should be plain (no Unicode formatting)"""


async def extract_text_structure_llm(
    post_text: str,
    short_post: Optional[str] = None,
    text_provider: Optional[BedrockTextProvider] = None,
    model: str = "claude-sonnet-4.5",
) -> Dict:
    """
    Use LLM to extract structured text from post for infographic overlay.

    Args:
        post_text: Full post text
        short_post: Optional short version
        text_provider: Optional text provider instance
        model: Model to use for extraction

    Returns:
        Dict with title, subtitle, sections, takeaway
    """
    if not text_provider:
        text_provider = get_text_provider(TextProvider.BEDROCK)

    user_message = f"""# LinkedIn Post Text

{post_text}

{f"# Short Version\n{short_post}" if short_post else ""}

Extract structured content for infographic overlay."""

    try:
        # Use the text provider's internal method to call Bedrock
        # Access the client and model mapping from the provider
        from ..providers.bedrock_text import BedrockTextProvider

        if not isinstance(text_provider, BedrockTextProvider):
            text_provider = get_text_provider(TextProvider.BEDROCK)

        # Get model ID
        model_id = text_provider._get_model_id(model)

        # Call Bedrock Converse API
        response = text_provider.client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": user_message}]}],
            system=[{"text": TEXT_EXTRACTION_PROMPT}],
            inferenceConfig={"maxTokens": 1000, "temperature": 0.3},
        )

        # Extract response
        raw_content = ""
        for block in response.get("output", {}).get("message", {}).get("content", []):
            if "text" in block:
                raw_content = block["text"]
                break

        # Clean JSON response
        content = raw_content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            if content.startswith("```json"):
                content = content[7:]
            else:
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        # Find JSON object
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end > start:
            content = content[start:end]

        # Parse JSON
        data = json.loads(content)

        # Validate and structure response
        result = {
            "title": data.get("title", "Key Insight"),
            "subtitle": data.get("subtitle"),
            "sections": data.get("sections", []),
            "takeaway": data.get("takeaway"),
        }

        # Ensure sections are properly formatted
        if result["sections"]:
            result["sections"] = [
                {
                    "title": s.get("title", "Section"),
                    "bullets": s.get("bullets", [])[:3],  # Max 3 bullets
                }
                for s in result["sections"][:3]  # Max 3 sections
            ]

        return result

    except Exception as e:
        logger.warning(f"LLM text extraction failed: {e}. Falling back to simple extraction.")
        # Fallback to simple extraction
        return _simple_extract(post_text, short_post)


def _simple_extract(post_text: str, short_post: Optional[str] = None) -> Dict:
    """Simple fallback extraction without LLM."""
    lines = post_text.split("\n")
    title = lines[0].strip() if lines else "Key Insight"

    subtitle = short_post if short_post else None

    sections = []
    current_section = None

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        if len(line) < 50 and not line.endswith((".", "!", "?")):
            if current_section:
                sections.append(current_section)
            current_section = {"title": line, "bullets": []}
        elif current_section:
            current_section["bullets"].append(line)
        else:
            current_section = {"title": "Key Points", "bullets": [line]}

    if current_section:
        sections.append(current_section)

    takeaway = None
    if sections:
        last_section = sections[-1]
        if last_section["bullets"]:
            takeaway = last_section["bullets"][-1]
        else:
            takeaway = last_section["title"]

    return {
        "title": title,
        "subtitle": subtitle,
        "sections": sections[:3],
        "takeaway": takeaway,
    }

