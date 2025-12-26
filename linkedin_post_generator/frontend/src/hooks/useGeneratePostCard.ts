/**
 * Hook for generating post card images (pure code, no AI)
 */

import { useMutation } from '@tanstack/react-query';
import { generatePostCard, APIError } from '../lib/api';
import type { PostCardGenerationRequest, PostCardGenerationResponse } from '../types';

export function useGeneratePostCard() {
  return useMutation<PostCardGenerationResponse, APIError, PostCardGenerationRequest>({
    mutationFn: generatePostCard,
    onError: (error) => {
      console.error('Post card generation failed:', error.message);
    },
  });
}
