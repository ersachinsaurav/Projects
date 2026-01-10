/**
 * TypeScript type definitions for LinkedIn Post Generator
 *
 * Supports Ollama (Mistral/Llama) and Bedrock (Claude) models with single-phase generation.
 * Simplified single-user architecture (no multi-tenancy).
 */

// =============================================================================
// ENUMS
// =============================================================================

export type PostLength = 'short' | 'medium' | 'long';
export type Tone = 'professional' | 'opinionated' | 'reflective';
export type CTAStyle = 'question' | 'statement' | 'none';
export type TextProvider = 'ollama' | 'bedrock';  // Ollama (Mistral/Llama/Qwen) or Bedrock (Claude)
export type ImageProvider = 'nova' | 'titan' | 'sdxl';  // Nova Canvas (recommended), Titan, or SDXL

// =============================================================================
// MODEL CONFIGS
// =============================================================================

export interface TextModelConfig {
  provider: TextProvider;
  model: string;
}

export interface ImageModelConfig {
  provider: ImageProvider;
  model: string;
}

// =============================================================================
// TEXT GENERATION
// =============================================================================

export interface TextGenerationRequest {
  session_id: string;
  idea: string;
  post_angle?: string | null;
  draft_post?: string | null;
  post_length: PostLength;
  tone: Tone;
  audience: string[];
  cta_style: CTAStyle;
  text_model: TextModelConfig;
  generate_images: boolean;  // If False, only generate short_post (saves tokens)
  image_model: ImageModelConfig;  // Only used if generate_images=True
}

export interface ImagePrompt {
  id: number;
  concept: string;
  prompt: string;
  style_notes: string;
  composition_note: string;
  negative_prompt?: string | null;  // SDXL-specific: things to avoid in generation
}

export interface ImageFingerprint {
  visual_style: string;
  color_palette: string;
  composition: string;
  lighting: string;
  concept_type: string;
}

export interface ImageStrategy {
  image_count: number;
  reason: string;
}

export interface ImageRecommendation {
  recommended_type: 'post_card' | 'cartoon_narrative' | 'cartoon_abstract' | 'abstract_minimal' | 'infographic';
  reasoning: string;  // Chain-of-thought explanation
  confidence: 'high' | 'medium' | 'low';
  alternative_types: string[];
  style_notes: string;
}

export interface InfographicSection {
  title: string;
  bullets: string[];
}

export interface InfographicTextStructure {
  title: string;
  subtitle?: string | null;
  sections: InfographicSection[];
  takeaway?: string | null;
}

export interface TextGenerationResponse {
  post_text: string;
  short_post: string;  // REQUIRED - Punchy summary for post cards
  hashtags: string[];
  image_recommendation: ImageRecommendation | null;  // ALWAYS present - AI recommendation for image type
  image_strategy: ImageStrategy | null;  // Only if generate_images=True
  image_prompts: ImagePrompt[];  // Only if generate_images=True
  image_fingerprint: ImageFingerprint | null;  // Only if generate_images=True
  infographic_text?: InfographicTextStructure | null;  // Pre-extracted text for infographic overlays
  session_id: string;
  model_used: string;
  image_model_used: string;  // Which model prompts were generated for (nova or titan)
  tokens_used?: number;
  generation_time_ms?: number;
}

// =============================================================================
// IMAGE GENERATION
// =============================================================================

export interface ImageGenerationRequest {
  session_id: string;
  image_prompts?: ImagePrompt[] | null;
  image_fingerprint?: ImageFingerprint | null;
  image_model: ImageModelConfig;
  generate_carousel?: boolean;  // Generate carousel: AI cover + post card sections (default: false)
  // Note: post_text, short_post, and infographic_text are read from session
  // (stored during text generation) to avoid duplication
}

export interface GeneratedImage {
  id: number;
  base64_data: string;
  prompt_used: string;
  concept: string;
  format: string;
  width: number;
  height: number;
}

export interface ImageGenerationResponse {
  images: GeneratedImage[];
  pdf_base64?: string | null;
  pdf_title?: string | null;  // Title for PDF filename (for carousels)
  session_id: string;
  model_used: string;
  image_count: number;
  generation_time_ms?: number;
}

// =============================================================================
// POST CARD GENERATION TYPES
// =============================================================================

export interface PostCardGenerationRequest {
  session_id: string;
  post_text: string;
  short_post?: string | null;
  avatar_base64?: string | null;
  name?: string;
  handle?: string;
  verified?: boolean;
  theme?: 'dark' | 'light';
}

export interface PostCardGenerationResponse {
  post_card_base64: string;
  format: string;
  width: number;
  height: number;
  session_id: string;
  theme: string;
  generation_time_ms?: number | null;
}

// =============================================================================
// UTILITY TYPES
// =============================================================================

export interface HealthCheckResponse {
  status: string;
  version: string;
  providers: Record<string, boolean>;
}

export interface ModelsResponse {
  text_models: Record<string, string[]>;
  image_models: Record<string, string[]>;
}

export interface ErrorDetail {
  message: string;
  code: string;
  field?: string;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

// =============================================================================
// APP STATE (Simplified - no tenant)
// =============================================================================

export interface AppState {
  sessionId: string;

  // Form state
  idea: string;
  postAngle: string;
  draftPost: string;
  postLength: PostLength;
  tone: Tone;
  audience: string[];
  ctaStyle: CTAStyle;

  // Model selection
  textModel: TextModelConfig;
  imageModel: ImageModelConfig;

  // Generation state
  generatedText: TextGenerationResponse | null;
  generatedImages: ImageGenerationResponse | null;

  // UI state
  isGeneratingText: boolean;
  isGeneratingImages: boolean;
  error: string | null;
}

// =============================================================================
// AVAILABLE OPTIONS
// =============================================================================

export const TEXT_MODELS: Record<TextProvider, string[]> = {
  ollama: [
    'qwen2.5:7b',          // (Local) Analytical & reasoning
    'mistral:7b',          // (Local) Professional content
    'llama3:8b',           // (Local) Creative content
  ],
  bedrock: [
    'claude-opus-4.5',     // Default, best quality (recommended)
    'claude-opus-4.1',
    'claude-sonnet-4.5',
    'claude-haiku-4.5',    // Fast, cheap
  ],
};

export const IMAGE_MODELS: Record<ImageProvider, string[]> = {
  sdxl: ['sdxl'],  // (Local) Default, supports overlays
  nova: ['nova-canvas'],  // Cloud, no overlay support
  titan: ['titan-image-generator-v2'],  // Cloud, no overlay support
};

// DEPRECATED: Use '../lib/defaults' instead
// These are kept for backward compatibility but will be removed in future versions
import {
  DEFAULT_TEXT_MODEL as DEFAULT_TEXT_MODEL_FROM_DEFAULTS,
  DEFAULT_IMAGE_MODEL as DEFAULT_IMAGE_MODEL_FROM_DEFAULTS,
} from '../lib/defaults';

export const DEFAULT_TEXT_MODEL = DEFAULT_TEXT_MODEL_FROM_DEFAULTS;
export const DEFAULT_IMAGE_MODEL = DEFAULT_IMAGE_MODEL_FROM_DEFAULTS;

// DEPRECATED: Use '../lib/defaults' instead
// These are kept for backward compatibility but will be removed in future versions
import { DEFAULT_AUDIENCES, ALL_AUDIENCES } from '../lib/defaults';

export const AUDIENCE_OPTIONS = [...DEFAULT_AUDIENCES] as string[];
export const ALL_AUDIENCE_OPTIONS = [...ALL_AUDIENCES] as string[];

export const POST_LENGTH_OPTIONS: { value: PostLength; label: string; description: string }[] = [
  { value: 'short', label: 'Short', description: '100-200 chars, punchy' },
  { value: 'medium', label: 'Medium', description: '300-600 chars, balanced' },
  { value: 'long', label: 'Long', description: '800-1200 chars, story-driven' },
];

export const TONE_OPTIONS: { value: Tone; label: string; description: string }[] = [
  { value: 'professional', label: 'Professional', description: 'Formal, data-driven' },
  { value: 'opinionated', label: 'Opinionated', description: 'Bold, contrarian' },
  { value: 'reflective', label: 'Reflective', description: 'Personal, insightful' },
];

export const CTA_OPTIONS: { value: CTAStyle; label: string; description: string }[] = [
  { value: 'question', label: 'Question', description: 'End with engaging question' },
  { value: 'statement', label: 'Statement', description: 'End with bold statement' },
  { value: 'none', label: 'None', description: 'Natural ending' },
];
