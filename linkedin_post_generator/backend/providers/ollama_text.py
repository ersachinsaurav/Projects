"""
Ollama Text Provider - 3-Step Pipeline
========================================
Implementation for Qwen, Mistral, and Llama models via Ollama.

Uses a 3-step pipeline for 95%+ success rate:
- STEP 1: Content Generation (Creative) - Temp: 0.6
- STEP 2: Style Normalization (Editing) - Temp: 0.2
- STEP 3: JSON Packaging (Mechanical) - Temp: 0.1

Supported Models:
- qwen2.5:7b (default, analytical & reasoning)
- mistral:7b (professional content)
- llama3:8b (creative content)

Uses Ollama's direct HTTP API at http://localhost:11434
"""

import json
import logging
import re
import time
from typing import Optional

import httpx

from ..config import settings
from ..prompts.pipeline_prompts import (
    get_step1_system_prompt,
    get_step1_user_prompt,
    get_step2_system_prompt,
    get_step2_user_prompt,
    get_step3_system_prompt,
    get_step3_user_prompt,
    validate_step1_output,
    validate_step2_output,
    validate_step3_output,
    PipelineConfig,
)
# NOTE: prompt_logger is imported lazily in __init__ to avoid circular import
from .base import (
    TextModelProvider,
    TextGenerationRequest,
    TextGenerationResponse,
    ImagePromptGenerationRequest,
    ImagePromptGenerationResponse,
    ImagePrompt,
    ImageFingerprint,
    InfographicTextStructure,
    InfographicSection,
    ProviderError,
)


logger = logging.getLogger(__name__)


class OllamaTextProvider(TextModelProvider):
    """
    Ollama text generation provider using 3-step pipeline.

    All Ollama models (Qwen, Mistral, Llama) use the pipeline for:
    - Higher success rate (95%+)
    - Better structured content
    - Reliable JSON output
    - Clean short_post without hashtags
    - Proper emoji placement
    """

    # Model name mapping
    MODEL_MAPPING = {
        "qwen2.5:7b": "qwen2.5:7b",  # Default - analytical & reasoning
        "mistral:7b": "mistral:7b",   # Professional content
        "llama3:8b": "llama3:8b",     # Creative content
    }

    def __init__(self, base_url: Optional[str] = None):
        """Initialize Ollama client with pipeline configuration."""
        self.base_url = base_url or getattr(settings, 'ollama_base_url', 'http://localhost:11434')
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=180.0,  # Pipeline takes longer (3 steps)
        )
        self.config = PipelineConfig()
        self._current_session_id: Optional[str] = None  # Set during generate()

        # Lazy import to avoid circular dependency
        # (providers → services → api → providers)
        from ..services.prompt_logger import get_prompt_logger
        self.prompt_logger = get_prompt_logger()

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def available_models(self) -> list[str]:
        return list(self.MODEL_MAPPING.keys())

    async def validate_model(self, model: str) -> bool:
        """Check if model is in available list."""
        return model in self.MODEL_MAPPING

    async def _check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = await self.client.get("/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def _call_ollama(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, int]:
        """
        Make a single call to Ollama API.

        Returns (raw_response_text, tokens_used).
        """
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = await self.client.post(
            "/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": self.config.STEP1_TOP_P,
                    "num_predict": max_tokens,
                    "repeat_penalty": self.config.REPEAT_PENALTY,
                    "num_ctx": self.config.NUM_CTX,
                },
            },
        )

        response.raise_for_status()
        data = response.json()

        tokens_used = data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
        return data.get("response", ""), tokens_used

    # =========================================================================
    # 3-STEP PIPELINE
    # =========================================================================

    async def _run_step1(
        self,
        request: TextGenerationRequest,
        model: str,
    ) -> tuple[str, int]:
        """
        STEP 1: Content Generation

        Goal: Generate high-quality long-form content.
        - Stays on the idea
        - Respects the angle
        - Sounds like a senior practitioner
        - IGNORES formatting, emojis, JSON, hashtags

        Temperature: 0.6 | Max tokens: 900 | Retries: 1
        """
        system_prompt = get_step1_system_prompt()
        user_prompt = get_step1_user_prompt(
            idea=request.idea,
            post_angle=request.post_angle,
            draft_post=request.draft_post,
            post_length=request.post_length,
            tone=request.tone,
            audience=request.audience,
        )

        total_tokens = 0
        last_error = None

        for attempt in range(self.config.STEP1_RETRIES + 1):
            try:
                output, tokens = await self._call_ollama(
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=self.config.STEP1_TEMPERATURE,
                    max_tokens=self.config.STEP1_MAX_TOKENS,
                )
                total_tokens += tokens

                # Validate output (soft validation - log warnings but don't fail)
                is_valid, errors = validate_step1_output(output)
                if not is_valid:
                    logger.warning(f"[PIPELINE] Step 1 validation warnings: {errors}")

                # Accept if output has reasonable length
                if len(output) > 100:
                    logger.info(f"[PIPELINE] Step 1 complete ({tokens} tokens)")

                    # Log the pipeline step with ACTUAL prompts
                    if self._current_session_id:
                        self.prompt_logger.log_pipeline_step(
                            session_id=self._current_session_id,
                            provider="ollama",
                            model=model,
                            step_number=1,
                            step_name="Content Generation",
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            output=output,
                            tokens_used=tokens,
                        )

                    return output, total_tokens

                last_error = "Output too short"

            except Exception as e:
                last_error = str(e)
                logger.warning(f"[PIPELINE] Step 1 attempt {attempt + 1} error: {last_error}")

        # Log error
        if self._current_session_id:
            self.prompt_logger.log_pipeline_step(
                session_id=self._current_session_id,
                provider="ollama",
                model=model,
                step_number=1,
                step_name="Content Generation",
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                error=last_error,
            )

        raise ProviderError(
            f"Step 1 (Content Generation) failed: {last_error}",
            provider="ollama",
            model=model,
        )

    async def _run_step2(
        self,
        step1_output: str,
        model: str,
    ) -> tuple[str, int]:
        """
        STEP 2: Style + Constraint Normalization

        Goal: Turn Step 1 output into policy-compliant prose.
        - ASCII-only
        - Sentence counts enforced
        - Tone tightened
        - Forbidden phrases removed
        - STILL NO JSON

        Temperature: 0.2 | Max tokens: 900 | Retries: 2
        """
        system_prompt = get_step2_system_prompt()
        user_prompt = get_step2_user_prompt(step1_output)

        total_tokens = 0
        last_error = None

        for attempt in range(self.config.STEP2_RETRIES + 1):
            try:
                output, tokens = await self._call_ollama(
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=self.config.STEP2_TEMPERATURE,
                    max_tokens=self.config.STEP2_MAX_TOKENS,
                )
                total_tokens += tokens

                # Validate output (soft validation)
                is_valid, errors = validate_step2_output(output)
                if not is_valid:
                    logger.warning(f"[PIPELINE] Step 2 validation warnings: {errors}")

                # Accept if output has reasonable length
                if len(output) > 100:
                    logger.info(f"[PIPELINE] Step 2 complete ({tokens} tokens)")

                    # Log the pipeline step with ACTUAL prompts
                    if self._current_session_id:
                        self.prompt_logger.log_pipeline_step(
                            session_id=self._current_session_id,
                            provider="ollama",
                            model=model,
                            step_number=2,
                            step_name="Style Normalization",
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            output=output,
                            tokens_used=tokens,
                        )

                    return output, total_tokens

                last_error = "Output too short"

            except Exception as e:
                last_error = str(e)
                logger.warning(f"[PIPELINE] Step 2 attempt {attempt + 1} error: {last_error}")

        # Log error
        if self._current_session_id:
            self.prompt_logger.log_pipeline_step(
                session_id=self._current_session_id,
                provider="ollama",
                model=model,
                step_number=2,
                step_name="Style Normalization",
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                error=last_error,
            )

        raise ProviderError(
            f"Step 2 (Style Normalization) failed: {last_error}",
            provider="ollama",
            model=model,
        )

    async def _run_step3(
        self,
        step2_output: str,
        model: str,
        author_hashtags: list[str] = None,
    ) -> tuple[dict, int]:
        """
        STEP 3: Packaging + Metadata (Mechanical Output)

        Goal: Wrap already-clean text into JSON.
        - JSON structure
        - short_post
        - hashtags
        - image metadata
        - emojis (ONLY here)

        Temperature: 0.1 | Max tokens: 1200 | Retries: 3
        """
        if author_hashtags is None:
            author_hashtags = ["#SachinSaurav", "#BySachinSaurav"]

        system_prompt = get_step3_system_prompt()
        user_prompt = get_step3_user_prompt(step2_output, author_hashtags)

        total_tokens = 0
        last_error = None
        last_output = None

        for attempt in range(self.config.STEP3_RETRIES + 1):
            try:
                output, tokens = await self._call_ollama(
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=self.config.STEP3_TEMPERATURE,
                    max_tokens=self.config.STEP3_MAX_TOKENS,
                )
                total_tokens += tokens
                last_output = output

                # Parse JSON
                data = self._parse_step3_json(output)

                # Validate (soft - we'll post-process anyway)
                is_valid, errors = validate_step3_output(output, author_hashtags)
                if not is_valid:
                    logger.warning(f"[PIPELINE] Step 3 validation warnings: {errors}")

                logger.info(f"[PIPELINE] Step 3 complete ({tokens} tokens)")

                # Log the pipeline step with ACTUAL prompts
                if self._current_session_id:
                    self.prompt_logger.log_pipeline_step(
                        session_id=self._current_session_id,
                        provider="ollama",
                        model=model,
                        step_number=3,
                        step_name="JSON Packaging",
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        output=output,
                        tokens_used=tokens,
                    )

                return data, total_tokens

            except json.JSONDecodeError as e:
                last_error = f"JSON parse error: {str(e)}"
                logger.warning(f"[PIPELINE] Step 3 attempt {attempt + 1}: {last_error}")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"[PIPELINE] Step 3 attempt {attempt + 1} error: {last_error}")

        # Log error
        if self._current_session_id:
            self.prompt_logger.log_pipeline_step(
                session_id=self._current_session_id,
                provider="ollama",
                model=model,
                step_number=3,
                step_name="JSON Packaging",
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                output=last_output,
                error=last_error,
            )

        raise ProviderError(
            f"Step 3 (JSON Packaging) failed after {self.config.STEP3_RETRIES + 1} attempts: {last_error}",
            provider="ollama",
            model=model,
        )

    def _parse_step3_json(self, raw_output: str) -> dict:
        """Parse and clean JSON from Step 3 output."""
        content = raw_output.strip()

        # Extract from markdown code block if present
        json_block_match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', content, re.DOTALL)
        if json_block_match:
            content = json_block_match.group(1).strip()
        else:
            # Find JSON object boundaries
            start_idx = content.find('{')
            if start_idx != -1:
                content = content[start_idx:]

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

        # Escape literal newlines in strings
        content = self._escape_newlines_in_json_strings(content)

        # Try to parse as-is first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try common fixes for 7B/8B model JSON issues
            content = self._fix_common_json_issues(content)
            return json.loads(content)

    def _fix_common_json_issues(self, json_str: str) -> str:
        """Fix common JSON issues from 7B/8B models."""
        # Remove trailing commas before } or ]
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)

        # Fix unquoted keys (key: value -> "key": value)
        json_str = re.sub(r'(\{|\,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)

        # Fix single quotes to double quotes (but be careful with apostrophes)
        # Only replace single quotes that are used as string delimiters
        json_str = re.sub(r":\s*'([^']*)'", r': "\1"', json_str)
        json_str = re.sub(r"\[\s*'", '["', json_str)
        json_str = re.sub(r"'\s*\]", '"]', json_str)
        json_str = re.sub(r"',\s*'", '", "', json_str)

        # Fix missing commas between key-value pairs (heuristic)
        # Look for }" followed by "key" without comma
        json_str = re.sub(r'"\s*\n\s*"([a-zA-Z_])', r'",\n"\1', json_str)

        return json_str

    def _escape_newlines_in_json_strings(self, json_str: str) -> str:
        """Escape literal newlines inside JSON string values."""
        result = []
        in_string = False
        escape_next = False

        for char in json_str:
            if escape_next:
                result.append(char)
                escape_next = False
                continue

            if char == '\\':
                result.append(char)
                escape_next = True
                continue

            if char == '"':
                in_string = not in_string
                result.append(char)
                continue

            if in_string and char == '\n':
                result.append('\\n')
                continue

            if in_string and char == '\r':
                result.append('\\r')
                continue

            if in_string and char == '\t':
                result.append('\\t')
                continue

            result.append(char)

        return ''.join(result)

    # =========================================================================
    # POST-PROCESSING
    # =========================================================================

    def _post_process_output(self, data: dict) -> dict:
        """
        Post-process Step 3 output to fix common 7B model issues.

        Fixes:
        - Add emojis to post_text if missing
        - Remove hashtags from short_post
        - Ensure proper paragraph formatting in post_text
        - Detect and remove duplicate paragraphs
        - Detect placeholder text and replace with actual content
        - Clean up any other formatting issues
        """
        # Fix short_post: remove any hashtags but PRESERVE newlines
        short_post = data.get("short_post", "")
        short_post = re.sub(r'\s*#\w+\s*', ' ', short_post).strip()
        # Clean up multiple spaces but PRESERVE newlines
        short_post = re.sub(r'[^\S\n]+', ' ', short_post)  # Replace horizontal whitespace only
        short_post = re.sub(r'\n{3,}', '\n\n', short_post)  # Max 2 consecutive newlines
        data["short_post"] = short_post

        # Fix post_text: ensure proper formatting and add emojis if missing
        post_text = data.get("post_text", "")

        # Emoji pattern for detection
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

        if post_text:
            # FIRST: Detect and remove duplicate paragraphs
            paragraphs = post_text.split('\n\n')
            seen_paragraphs = set()
            unique_paragraphs = []

            for para in paragraphs:
                # Normalize for comparison: strip whitespace and emojis
                normalized = emoji_pattern.sub('', para).strip().lower()
                # Use first 100 chars as key to catch near-duplicates
                key = normalized[:100] if len(normalized) > 100 else normalized

                if key and key not in seen_paragraphs:
                    seen_paragraphs.add(key)
                    unique_paragraphs.append(para.strip())

            paragraphs = unique_paragraphs if unique_paragraphs else paragraphs

            # SECOND: Detect placeholder text (model copied example format)
            placeholder_patterns = [
                r'^First paragraph\.$',
                r'^Second paragraph\.$',
                r'^Third paragraph with emoji\.$',
                r'^\[.*\]$',  # Any text in brackets like [Full post with emojis]
            ]

            filtered_paragraphs = []
            for para in paragraphs:
                is_placeholder = False
                for pattern in placeholder_patterns:
                    if re.match(pattern, para.strip(), re.IGNORECASE):
                        is_placeholder = True
                        logger.warning(f"[POST-PROCESS] Removed placeholder paragraph: {para[:50]}...")
                        break
                if not is_placeholder:
                    filtered_paragraphs.append(para)

            paragraphs = filtered_paragraphs if filtered_paragraphs else paragraphs

            # If it's a wall of text (only 1 "paragraph"), try to break it up
            if len(paragraphs) == 1 and len(paragraphs[0]) > 300:
                # Try to split by sentences where emojis appear
                emoji_split = re.split(r'(?=[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251])', paragraphs[0])
                if len(emoji_split) > 1:
                    paragraphs = [p.strip() for p in emoji_split if p.strip()]

            # Count existing emojis
            emojis = emoji_pattern.findall('\n\n'.join(paragraphs))
            emoji_count = sum(len(e) for e in emojis)

            if emoji_count < 2:
                # Add emojis at strategic points
                strategic_emojis = ['🔍', '💡', '🚀', '⚡']

                for i, emoji in enumerate(strategic_emojis[:min(4, len(paragraphs))]):
                    if i < len(paragraphs) and paragraphs[i]:
                        # Add emoji at start of paragraph if not already there
                        if not emoji_pattern.match(paragraphs[i][:2]):
                            paragraphs[i] = f"{emoji} {paragraphs[i]}"

            # Rejoin with proper paragraph breaks
            post_text = '\n\n'.join(paragraphs)
            data["post_text"] = post_text

        # THIRD: Fix placeholder text in image_recommendation
        img_rec = data.get("image_recommendation", {})
        if img_rec:
            reasoning = img_rec.get("reasoning", "")
            # Detect if reasoning is just the placeholder
            placeholder_reasoning = [
                "Why post_card fits this post",
                "Why post_card fits THIS post's topic",
                "[Why post_card fits",
            ]
            for placeholder in placeholder_reasoning:
                if placeholder.lower() in reasoning.lower():
                    # Generate better reasoning from post content
                    post_preview = post_text[:100] if post_text else "this professional content"
                    img_rec["reasoning"] = f"Post card format works well for this thought leadership piece about {post_preview.split('.')[0].strip()[:50]}."
                    logger.warning(f"[POST-PROCESS] Fixed placeholder image reasoning")
                    break
            data["image_recommendation"] = img_rec

        # FOURTH: Fix empty infographic_text
        infographic = data.get("infographic_text", {})
        if infographic:
            if not infographic.get("title") or infographic.get("title") in ["", "Main Headline", "[Main headline from post]"]:
                # Extract title from first sentence of post
                if post_text:
                    first_sentence = post_text.split('.')[0].strip()
                    # Remove emoji from start
                    first_sentence = emoji_pattern.sub('', first_sentence).strip()
                    infographic["title"] = first_sentence[:60] if len(first_sentence) > 60 else first_sentence
                    logger.warning(f"[POST-PROCESS] Generated infographic title from post")

            if not infographic.get("takeaway") or "[" in infographic.get("takeaway", ""):
                # Extract takeaway from last paragraph
                if paragraphs:
                    last_para = emoji_pattern.sub('', paragraphs[-1]).strip()
                    infographic["takeaway"] = last_para[:100] if len(last_para) > 100 else last_para
                    logger.warning(f"[POST-PROCESS] Generated infographic takeaway from post")

            data["infographic_text"] = infographic

        return data

    # =========================================================================
    # MAIN GENERATE METHOD (USES PIPELINE)
    # =========================================================================

    async def generate(
        self,
        request: TextGenerationRequest,
        model: str,
        system_prompt: str,  # Ignored - pipeline uses its own prompts
        max_tokens: int = 4000,  # Ignored - pipeline uses step-specific tokens
    ) -> TextGenerationResponse:
        """
        Generate LinkedIn post using 3-step pipeline.

        This replaces the old single-shot approach with a multi-step
        pipeline for higher reliability with 7B models.

        Steps:
        1. Content Generation (creative, temp=0.6)
        2. Style Normalization (editing, temp=0.2)
        3. JSON Packaging (mechanical, temp=0.1)
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="ollama",
                model=model,
            )

        if not await self._check_ollama_connection():
            raise ProviderError(
                f"Ollama is not running or not accessible at {self.base_url}. "
                "Please ensure Ollama is running: 'ollama serve'",
                provider="ollama",
                model=model,
            )

        model_id = self.MODEL_MAPPING[model]
        start_time = time.time()
        total_tokens = 0

        # Set session_id for pipeline step logging
        self._current_session_id = request.session_id
        logger.info(f"[PIPELINE] Session ID for logging: {self._current_session_id}")

        try:
            # STEP 1: Content Generation
            logger.info(f"[PIPELINE] Starting Step 1 (model={model_id})")
            step1_output, tokens1 = await self._run_step1(request, model_id)
            total_tokens += tokens1

            # STEP 2: Style Normalization
            logger.info("[PIPELINE] Starting Step 2")
            step2_output, tokens2 = await self._run_step2(step1_output, model_id)
            total_tokens += tokens2

            # STEP 3: JSON Packaging
            logger.info("[PIPELINE] Starting Step 3")
            data, tokens3 = await self._run_step3(step2_output, model_id)
            total_tokens += tokens3

            elapsed_ms = int((time.time() - start_time) * 1000)
            logger.info(f"[PIPELINE] Complete ({total_tokens} tokens, {elapsed_ms}ms)")

            # Post-process and build response
            data = self._post_process_output(data)
            return self._build_response(data, model, total_tokens, step1_output, step2_output)

        except ProviderError:
            raise
        except Exception as e:
            raise ProviderError(
                f"Pipeline failed: {str(e)}",
                provider="ollama",
                model=model,
                original_error=e,
            )
        finally:
            # Clear session_id after generation
            self._current_session_id = None

    def _build_response(
        self,
        data: dict,
        model: str,
        tokens_used: int,
        step1_output: str,
        step2_output: str,
    ) -> TextGenerationResponse:
        """Build TextGenerationResponse from parsed JSON data."""

        # Extract hashtags
        hashtags = data.get("hashtags", [])
        if isinstance(hashtags, str):
            hashtags = [h.strip() for h in hashtags.split(",") if h.strip()]

        # Ensure required personal hashtags are present
        required_hashtags = ["#SachinSaurav", "#BySachinSaurav"]
        for tag in required_hashtags:
            if tag not in hashtags:
                hashtags.append(tag)

        # Parse image prompts
        image_prompts = []
        for prompt_data in data.get("image_prompts", []):
            image_prompts.append(ImagePrompt(
                id=prompt_data.get("id", len(image_prompts) + 1),
                concept=prompt_data.get("concept", ""),
                prompt=prompt_data.get("prompt", ""),
                style_notes=prompt_data.get("style_notes", ""),
                composition_note=prompt_data.get("composition_note", ""),
                negative_prompt=prompt_data.get("negative_prompt"),
            ))

        # Parse image fingerprint
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

        # Parse image strategy
        image_strategy = data.get("image_strategy")
        if not image_strategy and image_prompts:
            image_strategy = {"image_count": len(image_prompts), "reason": "Generated from post content"}

        # Parse image recommendation
        image_recommendation = data.get("image_recommendation")
        if not image_recommendation:
            image_recommendation = {
                "recommended_type": "post_card",
                "reasoning": "Post card is the safest default for professional LinkedIn content.",
                "confidence": "medium",
                "alternative_types": ["cartoon_abstract", "abstract_minimal"],
                "style_notes": "Clean, minimal design with the post's key insight"
            }

        # Extract post text
        post_text = data.get("post_text", "")

        # Extract short_post
        short_post = data.get("short_post")
        if not short_post and post_text:
            short_post = post_text[:400].rsplit('\n', 1)[0] if len(post_text) > 400 else post_text
        elif short_post and len(short_post) > 400:
            short_post = short_post[:400].rsplit('\n', 1)[0]

        # Parse infographic_text
        infographic_text = None
        infographic_data = data.get("infographic_text")
        if infographic_data:
            sections = []
            for sec in infographic_data.get("sections", [])[:3]:
                sections.append(InfographicSection(
                    title=sec.get("title", ""),
                    bullets=sec.get("bullets", [])[:3]
                ))
            infographic_text = InfographicTextStructure(
                title=infographic_data.get("title", "Key Insight"),
                subtitle=infographic_data.get("subtitle"),
                sections=sections,
                takeaway=infographic_data.get("takeaway"),
            )

        # Build raw response (all steps combined for debugging)
        raw_response = f"=== STEP 1 ===\n{step1_output}\n\n=== STEP 2 ===\n{step2_output}\n\n=== STEP 3 ===\n{json.dumps(data, indent=2)}"

        # Add CTA footer to post_text
        from ..utils.constants import get_post_cta_footer
        if post_text:
            post_text = post_text.rstrip() + get_post_cta_footer()

        return TextGenerationResponse(
            post_text=post_text,
            short_post=short_post or "Check out this insight! 🚀",
            hashtags=hashtags,
            image_recommendation=image_recommendation,
            image_strategy=image_strategy,
            image_prompts=image_prompts,
            image_fingerprint=image_fingerprint,
            infographic_text=infographic_text,
            model_used=model,
            tokens_used=tokens_used if tokens_used > 0 else None,
            raw_response=raw_response,
        )

    # =========================================================================
    # IMAGE PROMPT GENERATION (uses simpler single-call approach)
    # =========================================================================

    async def generate_image_prompts(
        self,
        request: ImagePromptGenerationRequest,
        model: str,
        system_prompt: str,
        max_tokens: int = 2000,
    ) -> ImagePromptGenerationResponse:
        """
        Generate image prompts grounded in finalized post text.

        This uses a simpler single-call approach since the content
        is already finalized from the text generation step.
        """
        if not await self.validate_model(model):
            raise ProviderError(
                f"Model '{model}' not available. Choose from: {list(self.MODEL_MAPPING.keys())}",
                provider="ollama",
                model=model,
            )

        if not await self._check_ollama_connection():
            raise ProviderError(
                f"Ollama is not running or not accessible at {self.base_url}. "
                "Please ensure Ollama is running: 'ollama serve'",
                provider="ollama",
                model=model,
            )

        model_id = self.MODEL_MAPPING[model]
        user_message = self._build_image_prompt_user_message(request)

        try:
            output, tokens_used = await self._call_ollama(
                model=model_id,
                system_prompt=system_prompt,
                user_prompt=user_message,
                temperature=0.5,  # Medium creativity for image prompts
                max_tokens=max_tokens,
            )

            if not output:
                raise ProviderError(
                    "Empty response from Ollama",
                    provider="ollama",
                    model=model,
                )

            return self._parse_image_prompt_response(
                raw_content=output,
                model=model,
                tokens_used=tokens_used if tokens_used > 0 else None,
                post_text_used=request.post_text,
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ProviderError(
                    f"Model '{model_id}' not found. Please ensure it's downloaded: 'ollama pull {model_id}'",
                    provider="ollama",
                    model=model,
                    original_error=e,
                )
            raise ProviderError(
                f"Ollama API error (HTTP {e.response.status_code}): {e.response.text}",
                provider="ollama",
                model=model,
                original_error=e,
            )
        except httpx.RequestError as e:
            raise ProviderError(
                f"Failed to connect to Ollama at {self.base_url}. Is Ollama running?",
                provider="ollama",
                model=model,
                original_error=e,
            )
        except Exception as e:
            raise ProviderError(
                f"Unexpected error: {str(e)}",
                provider="ollama",
                model=model,
                original_error=e,
            )

    def _build_image_prompt_user_message(self, request: ImagePromptGenerationRequest) -> str:
        """Build the user prompt for image prompt generation."""
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
        parts.append("- Return ONLY valid JSON")
        parts.append("- Start your response with { and end with }")

        return "\n".join(parts)

    def _parse_image_prompt_response(
        self,
        raw_content: str,
        model: str,
        tokens_used: Optional[int],
        post_text_used: str,
    ) -> ImagePromptGenerationResponse:
        """Parse image prompt generation response."""
        content = self._parse_step3_json(raw_content)  # Reuse JSON parsing

        # Parse image prompts
        image_prompts = []
        for prompt_data in content.get("image_prompts", []):
            image_prompts.append(ImagePrompt(
                id=prompt_data.get("id", len(image_prompts) + 1),
                concept=prompt_data.get("concept", ""),
                prompt=prompt_data.get("prompt", ""),
                style_notes=prompt_data.get("style_notes", ""),
                composition_note=prompt_data.get("composition_note", ""),
                negative_prompt=prompt_data.get("negative_prompt"),
            ))

        # Parse image fingerprint
        fingerprint_data = content.get("image_fingerprint", {})
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
