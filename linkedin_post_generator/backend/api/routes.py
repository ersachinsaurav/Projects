"""
API Routes - Combined Router
=============================
Combines all modular route files into a single router.

Route modules:
- routes_health.py: Health check and utility endpoints
- routes_text.py: Text generation endpoints
- routes_image.py: Image generation and post card endpoints
- routes_session.py: Session management and usage endpoints
"""

from fastapi import APIRouter

from .routes_health import router as health_router
from .routes_text import router as text_router
from .routes_image import router as image_router
from .routes_session import router as session_router


# Create combined router
router = APIRouter()

# Include all sub-routers
router.include_router(health_router)
router.include_router(text_router)
router.include_router(image_router)
router.include_router(session_router)
