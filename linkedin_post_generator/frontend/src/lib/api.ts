/**
 * API Client for LinkedIn Post Generator
 *
 * Clean, single-user architecture (no multi-tenancy).
 */

import type {
  TextGenerationRequest,
  TextGenerationResponse,
  ImageGenerationRequest,
  ImageGenerationResponse,
  PostCardGenerationRequest,
  PostCardGenerationResponse,
  HealthCheckResponse,
  ModelsResponse,
} from '../types';

const API_BASE = '/api/v1';

/**
 * Custom error class for API errors
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

/**
 * Make an API request with error handling
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    let detail = 'Unknown error';
    try {
      const errorData = await response.json();
      detail = errorData.detail || errorData.message || JSON.stringify(errorData);
    } catch {
      detail = response.statusText;
    }

    throw new APIError(
      `API Error: ${response.status}`,
      response.status,
      detail
    );
  }

  return response.json();
}

// =============================================================================
// HEALTH & UTILITY
// =============================================================================

/**
 * Health check
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
  return apiRequest<HealthCheckResponse>('/health');
}

/**
 * Get available models
 */
export async function getModels(): Promise<ModelsResponse> {
  return apiRequest<ModelsResponse>('/models');
}

// =============================================================================
// TEXT GENERATION
// =============================================================================

/**
 * Generate LinkedIn post text
 */
export async function generateText(
  request: TextGenerationRequest
): Promise<TextGenerationResponse> {
  return apiRequest<TextGenerationResponse>('/generate-text', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// =============================================================================
// IMAGE GENERATION
// =============================================================================

/**
 * Generate images for LinkedIn post
 */
export async function generateImages(
  request: ImageGenerationRequest
): Promise<ImageGenerationResponse> {
  return apiRequest<ImageGenerationResponse>('/generate-images', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * Generate post card image (pure code, no AI)
 */
export async function generatePostCard(
  request: PostCardGenerationRequest
): Promise<PostCardGenerationResponse> {
  return apiRequest<PostCardGenerationResponse>('/generate-post-card', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// =============================================================================
// SESSION & USAGE
// =============================================================================

/**
 * Get session state (for debugging)
 */
export async function getSession(
  sessionId: string
): Promise<Record<string, unknown>> {
  return apiRequest(`/session/${sessionId}`);
}

/**
 * Delete session
 */
export async function deleteSession(
  sessionId: string
): Promise<{ message: string }> {
  return apiRequest(`/session/${sessionId}`, {
    method: 'DELETE',
  });
}

/**
 * Get usage statistics
 */
export async function getUsage(): Promise<Record<string, number>> {
  return apiRequest('/usage');
}
