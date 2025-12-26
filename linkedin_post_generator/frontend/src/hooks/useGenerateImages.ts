/**
 * Custom hook for image generation
 */

import { useMutation } from '@tanstack/react-query';
import { generateImages, APIError } from '../lib/api';
import type { ImageGenerationRequest, ImageGenerationResponse } from '../types';

export function useGenerateImages() {
  return useMutation<ImageGenerationResponse, APIError, ImageGenerationRequest>({
    mutationFn: generateImages,
    onError: (error) => {
      console.error('Image generation failed:', error.detail || error.message);
    },
  });
}

