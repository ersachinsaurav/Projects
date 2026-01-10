/**
 * Default Values
 * ==============
 * Centralized default values for the entire application.
 * All default values should be defined here and imported elsewhere.
 */

import type { PostLength, Tone, CTAStyle, TextModelConfig, ImageModelConfig } from '../types';

// Default post length
export const DEFAULT_POST_LENGTH: PostLength = 'medium';

// Default tone
export const DEFAULT_TONE: Tone = 'professional';

// Default CTA style
export const DEFAULT_CTA_STYLE: CTAStyle = 'question';

// Default audiences (must match backend DEFAULT_AUDIENCES)
export const DEFAULT_AUDIENCES = [
  'founders',
  'executives',
  'leaders',
  'engineers',
  'developers',
] as const;

// All available audience options (must match backend ALL_AUDIENCES)
export const ALL_AUDIENCES = [
  'founders',
  'executives',
  'leaders',
  'engineers',
  'developers',
  'product managers',
  'marketers',
  'designers',
  'data scientists',
  'entrepreneurs',
  'investors',
  'consultants',
] as const;

// Default text model - Claude Opus 4.5 (best quality, recommended)
export const DEFAULT_TEXT_MODEL: TextModelConfig = {
  provider: 'bedrock',
  model: 'claude-opus-4.5',
};

// Default image model
export const DEFAULT_IMAGE_MODEL: ImageModelConfig = {
  provider: 'sdxl',
  model: 'sdxl',
};

// Default postcard generation flag (default ON)
export const DEFAULT_GENERATE_POSTCARD = true;

// Default postcard theme
export const DEFAULT_POSTCARD_THEME: 'dark' | 'light' = 'dark';

// Default image generation flag (default OFF)
export const DEFAULT_GENERATE_IMAGE = false;

// Default carousel generation flag (default OFF)
export const DEFAULT_GENERATE_CAROUSEL = false;

// Post length options
export const POST_LENGTH_OPTIONS: { value: PostLength; label: string; description: string }[] = [
  { value: 'short', label: 'Short', description: '100-200 chars' },
  { value: 'medium', label: 'Medium', description: '300-600 chars' },
  { value: 'long', label: 'Long', description: '800-1200 chars' },
];

// Tone options
export const TONE_OPTIONS: { value: Tone; label: string; description: string }[] = [
  { value: 'professional', label: 'Professional', description: 'Formal, data-driven' },
  { value: 'opinionated', label: 'Opinionated', description: 'Bold takes' },
  { value: 'reflective', label: 'Reflective', description: 'Personal growth' },
];

// CTA options
export const CTA_OPTIONS: { value: CTAStyle; label: string }[] = [
  { value: 'question', label: 'Question' },
  { value: 'statement', label: 'Statement' },
  { value: 'none', label: 'None' },
];

// Text models - Ollama (Qwen/Mistral/Llama) and Bedrock (Claude)
// Models with 'Local' badge run on your machine, others use cloud APIs
export const TEXT_MODELS = [
  // Ollama models (local, via backend with prompts & logging)
  { provider: 'ollama' as const, model: 'qwen2.5:7b', label: 'Qwen 2.5 7B', badge: 'Local', description: 'Analytical & reasoning' },
  { provider: 'ollama' as const, model: 'mistral:7b', label: 'Mistral 7B', badge: 'Local', description: 'Professional content' },
  { provider: 'ollama' as const, model: 'llama3:8b', label: 'Llama 3 8B', badge: 'Local', description: 'Creative content' },
  // Bedrock models (Claude)
  { provider: 'bedrock' as const, model: 'claude-opus-4.5', label: 'Claude Opus 4.5', badge: 'Best', description: 'Recommended default' },
  { provider: 'bedrock' as const, model: 'claude-opus-4.1', label: 'Claude Opus 4.1' },
  { provider: 'bedrock' as const, model: 'claude-sonnet-4.5', label: 'Claude Sonnet 4.5', badge: 'Balanced' },
  { provider: 'bedrock' as const, model: 'claude-haiku-4.5', label: 'Claude Haiku 4.5', badge: 'Fast' },
];

// Image models
// Note: Nova and Titan do NOT support text overlays like SDXL does
export const IMAGE_MODELS = [
  { provider: 'sdxl' as const, model: 'sdxl', label: 'SDXL', badge: 'Local', description: 'Local WebUI, supports overlays (recommended)' },
  { provider: 'nova' as const, model: 'nova-canvas', label: 'Nova Canvas', description: 'Cloud, no overlay support' },
  { provider: 'titan' as const, model: 'titan-image-generator-v2', label: 'Titan v2', description: 'Cloud, no overlay support' },
];

