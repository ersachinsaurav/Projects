"""
LinkedIn Post Generator - FastAPI Application
==============================================
Main entry point for the backend API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"   Debug mode: {settings.debug}")
    print(f"   OpenAI configured: {settings.openai_api_key is not None}")
    print(f"   AWS Region: {settings.aws_region}")

    yield

    # Shutdown
    print(f"👋 Shutting down {settings.app_name}")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="SaaS-ready API for generating LinkedIn posts and images using AI",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.api_prefix)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "api": settings.api_prefix,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

