"""
API package.

Modular route organization:
- provider_factory.py: Factory functions for providers
- routes_health.py: Health and utility endpoints
- routes_text.py: Text generation endpoints
- routes_image.py: Image generation and post card endpoints
- routes_session.py: Session and usage endpoints
- routes.py: Combined router
- schemas.py: Pydantic request/response models
"""

from .routes import router

__all__ = ["router"]
