/**
 * TypeScript type definitions for LinkedIn Post Generator
 *
 * Claude-only models with single-phase generation.
 * Simplified single-user architecture (no multi-tenancy).
 */

// =============================================================================
// ENUMS
// =============================================================================

export type PostLength = 'short' | 'medium' | 'long';
export type Tone = 'professional' | 'opinionated' | 'reflective';
export type CTAStyle = 'question' | 'statement' | 'none';
export type TextProvider = 'bedrock';  // Claude only
export type ImageProvider = 'nova' | 'titan';  // Nova Canvas (recommended) or Titan

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

export interface TextGenerationResponse {
  post_text: string;
  short_post: string;  // REQUIRED - Punchy summary for post cards
  hashtags: string[];
  image_recommendation: ImageRecommendation | null;  // ALWAYS present - AI recommendation for image type
  image_strategy: ImageStrategy | null;  // Only if generate_images=True
  image_prompts: ImagePrompt[];  // Only if generate_images=True
  image_fingerprint: ImageFingerprint | null;  // Only if generate_images=True
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
  bedrock: [
    'claude-opus-4.5',     // Default, best quality
    'claude-opus-4.1',
    'claude-opus-4',
    'claude-sonnet-4.5',
    'claude-sonnet-4',
    'claude-haiku-4.5',    // Fast, cheap
  ],
};

export const IMAGE_MODELS: Record<ImageProvider, string[]> = {
  nova: ['nova-canvas'],  // Recommended, higher quality
  titan: ['titan-image-generator-v2'],  // Fallback
};

export const DEFAULT_TEXT_MODEL: TextModelConfig = {
  provider: 'bedrock',
  model: 'claude-opus-4.5',
};

export const DEFAULT_IMAGE_MODEL: ImageModelConfig = {
  provider: 'nova',
  model: 'nova-canvas',
};

// Default audiences (most common LinkedIn targets)
export const AUDIENCE_OPTIONS = [
  'founders',
  'engineers',
  'leaders',
  'developers',
];

// All available audience options
export const ALL_AUDIENCE_OPTIONS = [
  'founders',
  'engineers',
  'leaders',
  'developers',
  'marketers',
  'designers',
  'product managers',
  'data scientists',
  'executives',
  'entrepreneurs',
  'investors',
  'consultants',
];

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
