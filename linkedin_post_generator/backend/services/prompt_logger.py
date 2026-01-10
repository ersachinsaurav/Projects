"""
Prompt Logger Service
======================
Logs all prompts sent to AI models for debugging and transparency.

Simplified single-user architecture (no multi-tenancy).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Any


class PromptLogger:
    """Logs prompts sent to AI models."""

    def __init__(self, log_dir: str = "logs/prompts"):
        """Initialize prompt logger."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_text_generation(
        self,
        session_id: str,
        provider: str,
        model: str,
        system_prompt: str,
        user_input: dict[str, Any],
        response: Optional[dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        """Log text generation prompt."""
        # Use local time to match usage_logger
        timestamp = datetime.now().isoformat()
        date_str = datetime.now().strftime("%Y-%m-%d")

        log_entry = {
            "timestamp": timestamp,
            "type": "text_generation",
            "session_id": session_id,
            "provider": provider,
            "model": model,
            "system_prompt": system_prompt,
            "user_input": user_input,
            "response": response,
            "error": error,
        }

        log_file = self.log_dir / f"text_prompts_{date_str}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def log_pipeline_step(
        self,
        session_id: str,
        provider: str,
        model: str,
        step_number: int,
        step_name: str,
        system_prompt: str,
        user_prompt: str,
        output: Optional[str] = None,
        tokens_used: Optional[int] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Log individual pipeline step for Ollama 3-step pipeline.

        This captures the ACTUAL prompts being sent to the model,
        not just placeholders.
        """
        # Use local time to match usage_logger
        timestamp = datetime.now().isoformat()
        date_str = datetime.now().strftime("%Y-%m-%d")

        log_entry = {
            "timestamp": timestamp,
            "type": "pipeline_step",
            "session_id": session_id,
            "provider": provider,
            "model": model,
            "step_number": step_number,
            "step_name": step_name,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "output": output,
            "tokens_used": tokens_used,
            "error": error,
        }

        log_file = self.log_dir / f"text_prompts_{date_str}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def log_image_generation(
        self,
        session_id: str,
        provider: str,
        model: str,
        prompts: list[dict[str, Any]],
        fingerprint: dict[str, Any],
        response: Optional[dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        """Log image generation prompt."""
        # Use local time to match usage_logger
        timestamp = datetime.now().isoformat()
        date_str = datetime.now().strftime("%Y-%m-%d")

        log_entry = {
            "timestamp": timestamp,
            "type": "image_generation",
            "session_id": session_id,
            "provider": provider,
            "model": model,
            "prompts": prompts,
            "fingerprint": fingerprint,
            "response": response,
            "error": error,
        }

        log_file = self.log_dir / f"image_prompts_{date_str}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# Singleton instance
_prompt_logger: Optional[PromptLogger] = None


def get_prompt_logger() -> PromptLogger:
    """Get the singleton prompt logger instance."""
    global _prompt_logger
    if _prompt_logger is None:
        _prompt_logger = PromptLogger()
    return _prompt_logger
