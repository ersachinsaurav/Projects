"""
Configuration Module
====================
Environment-based configuration with sensible defaults.
"""

from functools import lru_cache
from typing import Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

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

    # OpenAI Settings
    openai_api_key: Optional[str] = None
    openai_text_model_default: str = "gpt-4.1"
    openai_image_model: str = "gpt-image-1"

    # AWS Bedrock Settings
    # Using cross-region inference profiles (us. prefix) for on-demand throughput
    aws_region: str = "us-east-1"
    bedrock_claude_opus_model: str = "us.anthropic.claude-opus-4-5-20251101-v1:0"
    bedrock_claude_sonnet_model: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    bedrock_titan_image_model: str = "amazon.titan-image-generator-v2:0"

    # Ollama Settings
    ollama_base_url: str = "http://localhost:11434"

    # SDXL WebUI Settings
    sdxl_webui_url: str = "http://localhost:7860"
    sdxl_steps: int = 25
    sdxl_sampler: str = "DPM++ 2M Karras"
    sdxl_cfg_scale: float = 6.5
    sdxl_width: int = 900  # Synced with carousel size
    sdxl_height: int = 1200  # Synced with carousel size

    # Generation Limits
    max_text_output_tokens: int = 4000
    max_images_per_request: int = 7
    max_image_prompt_length: int = 1000

    # Session Settings
    session_ttl_seconds: int = 3600  # 1 hour

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


# Convenience access
settings = get_settings()

