"""
Session Manager
================
In-memory session storage with Redis-ready interface.
Stores text generation results for subsequent image generation.

Simplified single-user architecture (no multi-tenancy).
Uses asyncio-compatible locks for thread safety in async context.
"""

import asyncio
import time
from typing import Optional, Any
from dataclasses import dataclass, field

from ..config import settings


@dataclass
class SessionData:
    """Session data container for generation flow."""
    session_id: str
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    # Text generation results
    post_text: Optional[str] = None
    short_post: Optional[str] = None  # For post cards
    hashtags: Optional[list] = None
    image_recommendation: Optional[dict] = None  # AI recommendation for image type
    image_strategy: Optional[dict] = None
    tone: Optional[str] = None
    audience: Optional[list] = None
    text_model_used: Optional[str] = None

    # Infographic text structure (pre-extracted to avoid second LLM call)
    infographic_text: Optional[dict] = None

    # Image prompt results
    image_prompts: Optional[list] = None
    image_fingerprint: Optional[dict] = None

    # Image generation results
    generated_images: Optional[list] = None
    pdf_data: Optional[str] = None
    image_model_used: Optional[str] = None

    def is_expired(self, ttl_seconds: int) -> bool:
        """Check if session has expired."""
        return (time.time() - self.updated_at) > ttl_seconds

    def touch(self):
        """Update the last access time."""
        self.updated_at = time.time()


class SessionManager:
    """
    In-memory session manager.

    Designed with Redis-compatible interface for easy migration.
    Sessions are identified by session_id only (no multi-tenancy).

    Note: Uses a regular dict with thread-safe operations.
    For high-concurrency scenarios, consider using asyncio.Lock()
    or migrating to Redis.
    """

    def __init__(self, ttl_seconds: int = None):
        """Initialize with optional TTL override."""
        self.ttl = ttl_seconds or settings.session_ttl_seconds
        self._store: dict[str, SessionData] = {}
        # Note: For simple in-memory storage with FastAPI, we use sync operations
        # since the session operations are fast (no I/O). For Redis migration,
        # these would become async operations.

    def get(self, session_id: str) -> Optional[SessionData]:
        """
        Get session data.

        Returns None if not found or expired.
        """
        session = self._store.get(session_id)

        if session is None:
            return None

        if session.is_expired(self.ttl):
            del self._store[session_id]
            return None

        session.touch()
        return session

    def create(self, session_id: str) -> SessionData:
        """Create a new session."""
        session = SessionData(session_id=session_id)
        self._store[session_id] = session
        return session

    def get_or_create(self, session_id: str) -> SessionData:
        """Get existing session or create new one."""
        session = self.get(session_id)
        if session is None:
            session = self.create(session_id)
        return session

    def update(self, session_id: str, **kwargs: Any) -> Optional[SessionData]:
        """
        Update session data.

        Only updates provided fields.
        """
        session = self.get_or_create(session_id)

        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        session.touch()

        return session

    def delete(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._store:
            del self._store[session_id]
            return True
        return False

    def cleanup_expired(self) -> int:
        """
        Remove all expired sessions.

        Call periodically to prevent memory leaks.
        Returns count of removed sessions.
        """
        expired_keys = [
            key for key, session in self._store.items()
            if session.is_expired(self.ttl)
        ]

        for key in expired_keys:
            del self._store[key]

        return len(expired_keys)

    def get_stats(self) -> dict:
        """Get session store statistics."""
        active = sum(
            1 for s in self._store.values()
            if not s.is_expired(self.ttl)
        )

        return {
            "total_sessions": len(self._store),
            "active_sessions": active,
            "ttl_seconds": self.ttl,
        }


# Global instance
session_manager = SessionManager()
