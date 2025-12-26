/**
 * Custom hook for text generation
 */

import { useMutation } from '@tanstack/react-query';
import { generateText, APIError } from '../lib/api';
import type { TextGenerationRequest, TextGenerationResponse } from '../types';

export function useGenerateText() {
  return useMutation<TextGenerationResponse, APIError, TextGenerationRequest>({
    mutationFn: generateText,
    onError: (error) => {
      console.error('Text generation failed:', error.detail || error.message);
    },
  });
}

