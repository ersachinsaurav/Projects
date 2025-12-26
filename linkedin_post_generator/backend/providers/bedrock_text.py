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
        parts.append("- NO emojis")
        parts.append("- Hashtags in separate array, NOT in post_text")
        parts.append("- Return ONLY valid JSON, no markdown code blocks")

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
        parts.append("- Return ONLY valid JSON, no markdown code blocks")

        return "\n".join(parts)

    def _clean_json_response(self, raw_content: str) -> str:
        """Clean Claude's response - may wrap JSON in markdown code blocks."""
        import re

        content = raw_content.strip()

        # Try to extract JSON from markdown code block
        # Match ```json ... ``` or ``` ... ```
        json_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
        if json_block_match:
            content = json_block_match.group(1).strip()
        else:
            # Fallback to simple stripping
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        # Try to find JSON object boundaries if there's extra text
        if not content.startswith('{'):
            start = content.find('{')
            if start != -1:
                content = content[start:]

        if not content.endswith('}'):
            # Find the last closing brace
            end = content.rfind('}')
            if end != -1:
                content = content[:end + 1]

        return content.strip()

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
            raise ProviderError(
                f"Invalid JSON in response: {raw_content[:500]}",
                provider="bedrock",
                model=model,
                original_error=e,
            )

        # Extract hashtags (ensure they're a list)
        hashtags = data.get("hashtags", [])
        if isinstance(hashtags, str):
            hashtags = [h.strip() for h in hashtags.split(",") if h.strip()]

        # Parse image prompts (only if present - when generate_images=True)
        image_prompts = []
        for prompt_data in data.get("image_prompts", []):
            image_prompts.append(ImagePrompt(
                id=prompt_data.get("id", len(image_prompts) + 1),
                concept=prompt_data.get("concept", ""),
                prompt=prompt_data.get("prompt", ""),
                style_notes=prompt_data.get("style_notes", ""),
                composition_note=prompt_data.get("composition_note", ""),
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

        return TextGenerationResponse(
            post_text=post_text,
            short_post=short_post or "Check out this insight! 🚀",  # Ultimate fallback
            hashtags=hashtags,
            image_recommendation=image_recommendation,  # ALWAYS present
            image_strategy=image_strategy,  # Can be None if generate_images=False
            image_prompts=image_prompts,
            image_fingerprint=image_fingerprint,
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
            raise ProviderError(
                f"Invalid JSON in response: {raw_content[:500]}",
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
