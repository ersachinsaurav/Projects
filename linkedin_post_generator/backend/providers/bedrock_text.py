"""
AWS Bedrock Text Provider
==========================
Implementation for Claude models via AWS Bedrock.

Supported Models:
- Claude Opus 4.5 (default, best quality)
- Claude Opus 4
- Claude Sonnet 4.5
- Claude Sonnet 4

Single-Phase Generation:
- generate() returns Text + Hashtags + Image Strategy + Image Prompts (all in one call)
"""

import json
import time
from typing import Optional

import boto3
from botocore.config import Config

from ..config import settings
from .base import (
    TextModelProvider,
    TextGenerationRequest,
    TextGenerationResponse,
    ImagePromptGenerationRequest,
    ImagePromptGenerationResponse,
    ImagePrompt,
    ImageFingerprint,
    ProviderError,
)


class BedrockTextProvider(TextModelProvider):
    """AWS Bedrock Claude text generation provider - Claude only."""

    # Model name to Bedrock model ID mapping
    # Using cross-region inference profiles (us. prefix) for on-demand throughput
    MODEL_MAPPING = {
        "claude-opus-4.5": "us.anthropic.claude-opus-4-5-20251101-v1:0",
        "claude-opus-4.1": "us.anthropic.claude-opus-4-1-20250805-v1:0",
        "claude-opus-4": "us.anthropic.claude-opus-4-20250514-v1:0",
        "claude-sonnet-4.5": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        "claude-sonnet-4": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "claude-haiku-4.5": "us.anthropic.claude-haiku-4-5-20251001-v1:0",  # Fast, cheap
    }

    def __init__(self, region: Optional[str] = None):
        """Initialize Bedrock client."""
        self.region = region or settings.aws_region

        # Configure with retry logic
        config = Config(
            region_name=self.region,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )

        self.client = boto3.client("bedrock-runtime", config=config)

    @property
    def provider_name(self) -> str:
        return "bedrock"

    @property
    def available_models(self) -> list[str]:
        return list(self.MODEL_MAPPING.keys())

    async def validate_model(self, model: str) -> bool:
        """Check if model is in available list."""
        return model in self.MODEL_MAPPING

    def _get_model_id(self, model: str) -> str:
        """Get Bedrock model ID from friendly name."""
        if model not in self.MODEL_MAPPING:
            raise ProviderError(
                f"Model '{model}' not found. Available: {list(self.MODEL_MAPPING.keys())}",
                provider="bedrock",
                model=model,
            )
        return self.MODEL_MAPPING[model]

    async def generate(
        self,
        request: TextGenerationRequest,
        model: str,
        system_prompt: str,
        max_tokens: int = 4000,
    ) -> TextGenerationResponse:
        """
        Generate LinkedIn post text (Phase 1).

        Returns text + hashtags + image strategy.
        Does NOT generate image prompts.
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="bedrock",
                model=model,
            )

        model_id = self._get_model_id(model)
        user_message = self._build_text_user_message(request)

        try:
            start_time = time.time()

            # Use Converse API
            response = self.client.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_message}],
                    }
                ],
                system=[{"text": system_prompt}],
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": 0.7,
                },
            )

            elapsed_ms = int((time.time() - start_time) * 1000)

            # Extract response content
            raw_content = ""
            for block in response.get("output", {}).get("message", {}).get("content", []):
                if "text" in block:
                    raw_content = block["text"]
                    break

            # Get token usage
            usage = response.get("usage", {})
            tokens_used = usage.get("inputTokens", 0) + usage.get("outputTokens", 0)

            return self._parse_text_response(
                raw_content=raw_content,
                model=model,
                tokens_used=tokens_used,
            )

        except json.JSONDecodeError as e:
            raise ProviderError(
                f"Failed to parse JSON response: {str(e)}",
                provider="bedrock",
                model=model,
                original_error=e,
            )
        except Exception as e:
            raise ProviderError(
                f"Bedrock API error: {str(e)}",
                provider="bedrock",
                model=model,
                original_error=e,
            )

    async def generate_image_prompts(
        self,
        request: ImagePromptGenerationRequest,
        model: str,
        system_prompt: str,
        max_tokens: int = 2000,
    ) -> ImagePromptGenerationResponse:
        """
        Generate image prompts grounded in finalized post text (Phase 2).

        Returns footer-aware image prompts connected to specific post content.
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="bedrock",
                model=model,
            )

        model_id = self._get_model_id(model)
        user_message = self._build_image_prompt_user_message(request)

        try:
            start_time = time.time()

            response = self.client.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_message}],
                    }
                ],
                system=[{"text": system_prompt}],
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": 0.7,
                },
            )

            elapsed_ms = int((time.time() - start_time) * 1000)

            # Extract response content
            raw_content = ""
            for block in response.get("output", {}).get("message", {}).get("content", []):
                if "text" in block:
                    raw_content = block["text"]
                    break

            usage = response.get("usage", {})
            tokens_used = usage.get("inputTokens", 0) + usage.get("outputTokens", 0)

            return self._parse_image_prompt_response(
                raw_content=raw_content,
                model=model,
                tokens_used=tokens_used,
                post_text_used=request.post_text,
            )

        except json.JSONDecodeError as e:
            raise ProviderError(
                f"Failed to parse JSON response: {str(e)}",
                provider="bedrock",
                model=model,
                original_error=e,
            )
        except Exception as e:
            raise ProviderError(
                f"Bedrock API error: {str(e)}",
                provider="bedrock",
                model=model,
                original_error=e,
            )

    def _build_text_user_message(self, request: TextGenerationRequest) -> str:
        """Build the user prompt for text generation (Phase 1)."""
        parts = ["# LinkedIn Post Request\n"]

        parts.append(f"**Core Idea:** {request.idea}")

        if request.post_angle:
            parts.append(f"**Angle/Hook:** {request.post_angle}")

        if request.draft_post:
            parts.append(f"**Draft to Refine:**\n{request.draft_post}")

        parts.append("\n## Parameters")
        parts.append(f"- **Length:** {request.post_length}")
        parts.append(f"- **Tone:** {request.tone}")
        parts.append(f"- **Target Audience:** {', '.join(request.audience)}")
        parts.append(f"- **CTA Style:** {request.cta_style}")

        parts.append("\n## Critical Reminders")
        parts.append("- Use Unicode bold (𝗧𝗵𝗶𝘀) NOT markdown (**this**)")
        parts.append("- Use minimal emojis for emphasis (max 3-5)")
        parts.append("- Hashtags in separate array, NOT in post_text")
        parts.append("- Return ONLY valid JSON, no markdown code blocks, no explanations before or after")
        parts.append("- Start your response with { and end with }")
        parts.append("- Ensure the JSON is complete and valid - do not truncate it")
        parts.append("- CRITICAL: Escape all double quotes inside string values with backslash (\\\")")
        parts.append('  Example: "I wore \\"always available\\" as a badge" NOT "I wore "always available" as a badge"')

        return "\n".join(parts)

    def _build_image_prompt_user_message(self, request: ImagePromptGenerationRequest) -> str:
        """Build the user prompt for image prompt generation (Phase 2)."""
        parts = ["# Image Prompt Generation Request\n"]

        parts.append("## The LinkedIn Post (Final Text)")
        parts.append("```")
        parts.append(request.post_text)
        parts.append("```\n")

        parts.append(f"## Number of Images Needed: {request.image_count}")
        parts.append(f"## Post Tone: {request.tone}")
        parts.append(f"## Target Audience: {', '.join(request.audience)}")

        parts.append("\n## Critical Requirements")
        parts.append("- Each image prompt must reference a SPECIFIC concept from the post above")
        parts.append("- Leave bottom 10% of image empty for branded footer")
        parts.append("- Place key visuals in top 70% of frame")
        parts.append("- NO text/words inside images")
        parts.append("- Prompts must NOT be reusable for other posts")
        parts.append("- Return ONLY valid JSON, no markdown code blocks, no explanations before or after")
        parts.append("- Start your response with { and end with }")
        parts.append("- Ensure the JSON is complete and valid - do not truncate it")

        return "\n".join(parts)

    def _clean_json_response(self, raw_content: str) -> str:
        """Clean Claude's response - may wrap JSON in markdown code blocks."""
        import re

        content = raw_content.strip()

        # First, try to extract JSON from markdown code block (most common case)
        # Match ```json ... ``` or ``` ... ``` (non-greedy, then greedy fallback)
        json_block_match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', content, re.DOTALL)
        if json_block_match:
            content = json_block_match.group(1).strip()
        else:
            # Fallback: try to find JSON object boundaries
            # Look for opening brace
            start_idx = content.find('{')
            if start_idx != -1:
                content = content[start_idx:]

            # Remove trailing markdown if present
            if content.endswith('```'):
                content = content[:-3].rstrip()

            # Find the matching closing brace (handle nested objects)
            brace_count = 0
            end_idx = -1
            for i, char in enumerate(content):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break

            if end_idx > 0:
                content = content[:end_idx]

        # Final cleanup: remove any leading/trailing whitespace or newlines
        content = content.strip()

        # If still doesn't start with '{', try one more time to find it
        if not content.startswith('{'):
            start = content.find('{')
            if start != -1:
                content = content[start:]
                # Find matching closing brace
                brace_count = 0
                end_idx = -1
                for i, char in enumerate(content):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                if end_idx > 0:
                    content = content[:end_idx]

        # Fix unescaped quotes inside JSON string values
        # This is a common issue with Claude outputting: "I wore "always available" as a badge"
        # Instead of: "I wore \"always available\" as a badge"
        content = self._fix_unescaped_quotes(content)

        return content.strip()

    def _fix_unescaped_quotes(self, json_str: str) -> str:
        """
        Fix unescaped double quotes inside JSON string values.

        Claude often outputs: {"text": "I wore "always available" as a badge"}
        This should be: {"text": "I wore \"always available\" as a badge"}

        Strategy: Walk through the string, track if we're inside a JSON string value,
        and escape any unescaped quotes we find inside string values.
        """
        result = []
        i = 0
        in_string = False
        escape_next = False

        while i < len(json_str):
            char = json_str[i]

            if escape_next:
                result.append(char)
                escape_next = False
                i += 1
                continue

            if char == '\\':
                result.append(char)
                escape_next = True
                i += 1
                continue

            if char == '"':
                if not in_string:
                    # Starting a string
                    in_string = True
                    result.append(char)
                else:
                    # We're inside a string - is this the end quote or an unescaped quote?
                    # Look ahead to see if this looks like an end quote
                    # End quotes are followed by: , } ] : or whitespace then these
                    remaining = json_str[i+1:].lstrip()

                    if not remaining:
                        # End of input - this is the closing quote
                        in_string = False
                        result.append(char)
                    elif remaining[0] in ',}]:':
                        # This is a proper end quote
                        in_string = False
                        result.append(char)
                    elif remaining.startswith('\n') or remaining.startswith('\r'):
                        # End of line after quote - likely end quote
                        # But check if it's followed by a key
                        rest = remaining.lstrip()
                        if rest and rest[0] == '"':
                            # Next line starts with a key - this is end quote
                            in_string = False
                            result.append(char)
                        else:
                            # Probably an unescaped quote inside string
                            result.append('\\')
                            result.append(char)
                    else:
                        # This quote is inside the string value - escape it
                        result.append('\\')
                        result.append(char)
                i += 1
                continue

            result.append(char)
            i += 1

        return ''.join(result)

    def _parse_text_response(
        self,
        raw_content: str,
        model: str,
        tokens_used: Optional[int],
    ) -> TextGenerationResponse:
        """Parse LLM response (text + hashtags + image strategy + image prompts)."""
        content = self._clean_json_response(raw_content)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            # Show more context in error - include both cleaned and raw content
            error_context = f"Cleaned content (first 1000 chars): {content[:1000]}\n\nRaw content (first 1000 chars): {raw_content[:1000]}"
            raise ProviderError(
                f"Invalid JSON in response. {str(e)}\n\n{error_context}",
                provider="bedrock",
                model=model,
                original_error=e,
            )

        # Extract hashtags (ensure they're a list)
        hashtags = data.get("hashtags", [])
        if isinstance(hashtags, str):
            hashtags = [h.strip() for h in hashtags.split(",") if h.strip()]

        # Ensure our branding hashtag is present
        from ..utils.constants import get_branding_hashtag
        our_branding = get_branding_hashtag()
        if our_branding not in hashtags:
            hashtags.append(our_branding)

        # Parse image prompts (only if present - when generate_images=True)
        image_prompts = []
        for prompt_data in data.get("image_prompts", []):
            image_prompts.append(ImagePrompt(
                id=prompt_data.get("id", len(image_prompts) + 1),
                concept=prompt_data.get("concept", ""),
                prompt=prompt_data.get("prompt", ""),
                style_notes=prompt_data.get("style_notes", ""),
                composition_note=prompt_data.get("composition_note", ""),
                negative_prompt=prompt_data.get("negative_prompt"),  # SDXL-specific
            ))

        # Parse image fingerprint (only if present)
        fingerprint_data = data.get("image_fingerprint", {})
        image_fingerprint = None
        if fingerprint_data:
            image_fingerprint = ImageFingerprint(
                visual_style=fingerprint_data.get("visual_style", "minimal"),
                color_palette=fingerprint_data.get("color_palette", "neutral"),
                composition=fingerprint_data.get("composition", "top-weighted"),
                lighting=fingerprint_data.get("lighting", "soft"),
                concept_type=fingerprint_data.get("concept_type", "abstract"),
            )

        # Parse image strategy (only if present - when generate_images=True)
        image_strategy = data.get("image_strategy")
        if not image_strategy and image_prompts:
            # Fallback: create default strategy if we have prompts but no strategy
            image_strategy = {"image_count": len(image_prompts), "reason": "Generated from post content"}

        # Parse image recommendation (ALWAYS generated - helps user choose image type)
        image_recommendation = data.get("image_recommendation")
        if not image_recommendation:
            # Fallback: default to post_card recommendation
            image_recommendation = {
                "recommended_type": "post_card",
                "reasoning": "Post card is the safest default for professional LinkedIn content.",
                "confidence": "medium",
                "alternative_types": ["cartoon_abstract", "abstract_minimal"],
                "style_notes": "Clean, minimal design with the post's key insight"
            }

        # Extract post text
        post_text = data.get("post_text", "")

        # Extract short_post - REQUIRED, but create fallback if model fails to provide
        short_post = data.get("short_post")
        if not short_post and post_text:
            # Fallback: take first 400 chars of post_text
            short_post = post_text[:400].rsplit('\n', 1)[0] if len(post_text) > 400 else post_text
        elif short_post and len(short_post) > 400:
            # Truncate if too long
            short_post = short_post[:400].rsplit('\n', 1)[0]

        # Parse infographic_text - pre-extracted for efficient infographic rendering
        from .base import InfographicTextStructure, InfographicSection
        infographic_text = None
        infographic_data = data.get("infographic_text")
        if infographic_data:
            sections = []
            for sec in infographic_data.get("sections", [])[:3]:  # Max 3 sections
                sections.append(InfographicSection(
                    title=sec.get("title", ""),
                    bullets=sec.get("bullets", [])[:3]  # Max 3 bullets
                ))
            infographic_text = InfographicTextStructure(
                title=infographic_data.get("title", "Key Insight"),
                subtitle=infographic_data.get("subtitle"),
                sections=sections,
                takeaway=infographic_data.get("takeaway"),
            )

        # Add CTA footer to post_text
        from ..utils.constants import get_post_cta_footer
        if post_text:
            post_text = post_text.rstrip() + get_post_cta_footer()

        return TextGenerationResponse(
            post_text=post_text,
            short_post=short_post or "Check out this insight! 🚀",  # Ultimate fallback
            hashtags=hashtags,
            image_recommendation=image_recommendation,  # ALWAYS present
            image_strategy=image_strategy,  # Can be None if generate_images=False
            image_prompts=image_prompts,
            image_fingerprint=image_fingerprint,
            infographic_text=infographic_text,  # Pre-extracted for infographic rendering
            model_used=model,
            tokens_used=tokens_used,
            raw_response=raw_content,
        )

    def _parse_image_prompt_response(
        self,
        raw_content: str,
        model: str,
        tokens_used: Optional[int],
        post_text_used: str,
    ) -> ImagePromptGenerationResponse:
        """Parse Phase 2 LLM response (image prompts)."""
        content = self._clean_json_response(raw_content)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            # Show more context in error - include both cleaned and raw content
            error_context = f"Cleaned content (first 1000 chars): {content[:1000]}\n\nRaw content (first 1000 chars): {raw_content[:1000]}"
            raise ProviderError(
                f"Invalid JSON in response. {str(e)}\n\n{error_context}",
                provider="bedrock",
                model=model,
                original_error=e,
            )

        # Parse image prompts
        image_prompts = []
        for prompt_data in data.get("image_prompts", []):
            image_prompts.append(ImagePrompt(
                id=prompt_data.get("id", len(image_prompts) + 1),
                concept=prompt_data.get("concept", ""),
                prompt=prompt_data.get("prompt", ""),
                style_notes=prompt_data.get("style_notes", ""),
                composition_note=prompt_data.get("composition_note", ""),
                negative_prompt=prompt_data.get("negative_prompt"),  # SDXL-specific
            ))

        # Parse image fingerprint
        fingerprint_data = data.get("image_fingerprint", {})
        image_fingerprint = ImageFingerprint(
            visual_style=fingerprint_data.get("visual_style", "minimal"),
            color_palette=fingerprint_data.get("color_palette", "neutral"),
            composition=fingerprint_data.get("composition", "top-weighted"),
            lighting=fingerprint_data.get("lighting", "soft"),
            concept_type=fingerprint_data.get("concept_type", "abstract"),
        )

        return ImagePromptGenerationResponse(
            image_prompts=image_prompts,
            image_fingerprint=image_fingerprint,
            post_text_used=post_text_used,
            model_used=model,
            tokens_used=tokens_used,
            raw_response=raw_content,
        )
