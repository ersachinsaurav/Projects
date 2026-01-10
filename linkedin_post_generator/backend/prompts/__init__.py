"""Prompt templates package."""

from .linkedin_text import (
    get_linkedin_text_prompt,
    get_image_prompt_generation_prompt,
)
from .ollama_linkedin_text import (
    get_ollama_linkedin_text_prompt,
    get_ollama_image_prompt_generation_prompt,
    get_mistral_linkedin_text_prompt,
    get_llama_linkedin_text_prompt,
)
from .pipeline_prompts import (
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
from .image_prompts import (
    get_image_enhancement_prompt,
    get_negative_prompt,
    get_linkedin_image_style_presets,
)

# New modular image generation prompts
from .image_gen import (
    get_image_prompt,
    get_negative_prompt_for_model,
    PromptContext,
    SUPPORTED_MODELS,
    SUPPORTED_USECASES,
)

__all__ = [
    # Legacy exports (Claude/Bedrock)
    "get_linkedin_text_prompt",
    "get_image_prompt_generation_prompt",
    # Ollama-specific prompts (Mistral/Llama)
    "get_ollama_linkedin_text_prompt",
    "get_ollama_image_prompt_generation_prompt",
    "get_mistral_linkedin_text_prompt",
    "get_llama_linkedin_text_prompt",
    # 3-Step Pipeline prompts (95%+ success rate)
    "get_step1_system_prompt",
    "get_step1_user_prompt",
    "get_step2_system_prompt",
    "get_step2_user_prompt",
    "get_step3_system_prompt",
    "get_step3_user_prompt",
    "validate_step1_output",
    "validate_step2_output",
    "validate_step3_output",
    "PipelineConfig",
    # Image prompts
    "get_image_enhancement_prompt",
    "get_negative_prompt",
    "get_linkedin_image_style_presets",
    # New modular exports
    "get_image_prompt",
    "get_negative_prompt_for_model",
    "PromptContext",
    "SUPPORTED_MODELS",
    "SUPPORTED_USECASES",
]
