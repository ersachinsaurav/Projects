"""
Usage Logger
=============
Tracks usage per session for analytics.

Simplified single-user architecture (no multi-tenancy).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from threading import Lock

from ..config import settings


@dataclass
class UsageRecord:
    """Single usage record."""
    timestamp: str
    session_id: str
    operation: str  # "text_generation" or "image_generation"
    provider: str
    model: str
    tokens_used: Optional[int] = None
    image_count: Optional[int] = None
    duration_ms: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None


class UsageLogger:
    """
    Log usage for analytics.

    In production, this would write to a database or message queue.
    For now, we use file-based logging that can be easily extended.
    """

    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize with log directory."""
        self.log_dir = log_dir or Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

        # In-memory aggregation for quick access
        self._usage: dict = {
            "text_generations": 0,
            "image_generations": 0,
            "total_tokens": 0,
            "total_images": 0,
            "errors": 0,
        }

    def _get_log_file(self) -> Path:
        """Get the log file for today."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"usage_{date_str}.jsonl"

    def log_text_generation(
        self,
        session_id: str,
        provider: str,
        model: str,
        tokens_used: Optional[int] = None,
        duration_ms: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Log a text generation event."""
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            operation="text_generation",
            provider=provider,
            model=model,
            tokens_used=tokens_used,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message,
        )

        self._write_record(record)
        self._update_aggregation(record)

    def log_image_generation(
        self,
        session_id: str,
        provider: str,
        model: str,
        image_count: int,
        duration_ms: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Log an image generation event."""
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            operation="image_generation",
            provider=provider,
            model=model,
            image_count=image_count,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message,
        )

        self._write_record(record)
        self._update_aggregation(record)

    def _write_record(self, record: UsageRecord):
        """Write record to log file."""
        with self._lock:
            log_file = self._get_log_file()
            with open(log_file, "a") as f:
                f.write(json.dumps(asdict(record)) + "\n")

    def _update_aggregation(self, record: UsageRecord):
        """Update in-memory aggregation."""
        with self._lock:
            if record.operation == "text_generation":
                self._usage["text_generations"] += 1
                if record.tokens_used:
                    self._usage["total_tokens"] += record.tokens_used
            elif record.operation == "image_generation":
                self._usage["image_generations"] += 1
                if record.image_count:
                    self._usage["total_images"] += record.image_count

            if not record.success:
                self._usage["errors"] += 1

    def get_usage(self) -> dict:
        """Get aggregated usage."""
        with self._lock:
            return dict(self._usage)


# Global instance
usage_logger = UsageLogger()
