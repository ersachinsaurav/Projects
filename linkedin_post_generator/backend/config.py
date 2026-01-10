"""
Configuration Module
====================
All settings loaded from .env file. See env.example for options.
"""

from functools import lru_cache
from typing import Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # App Settings
    app_name: str = "LinkedIn Post Generator"
    app_version: str = "1.0.0"
    debug: bool = False

    # API Settings
    api_prefix: str = "/api/v1"
    cors_origins: Union[str, list[str]] = "http://localhost:5173,http://localhost:5170"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Branding (configure in .env - see env.example)
    brand_name: str = "Your Name"
    brand_handle: str = "@yourusername"
    brand_website: str = "yourwebsite.com"
    brand_linkedin_url: str = "linkedin.com/in/yourusername"
    brand_instagram_url: str = "instagram.com/yourusername"

    # AWS Bedrock
    aws_region: str = "us-east-1"
    bedrock_claude_opus_model: str = "us.anthropic.claude-opus-4-5-20251101-v1:0"
    bedrock_claude_sonnet_model: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    bedrock_titan_image_model: str = "amazon.titan-image-generator-v2:0"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"

    # SDXL WebUI
    sdxl_webui_url: str = "http://localhost:7860"
    sdxl_steps: int = 25
    sdxl_sampler: str = "DPM++ 2M Karras"
    sdxl_cfg_scale: float = 6.5
    sdxl_width: int = 900
    sdxl_height: int = 1200

    # Generation Limits
    max_text_output_tokens: int = 4000
    max_images_per_request: int = 7
    max_image_prompt_length: int = 1000

    # Session
    session_ttl_seconds: int = 3600

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

