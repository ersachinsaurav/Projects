/**
 * Recommendation Section Component
 * ==================================
 * Displays AI-powered image type recommendations
 * with expandable reasoning and quick action buttons.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  Lightbulb,
  Wand2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import type { TextGenerationResponse } from '../types';
import { cn } from '../lib/utils';
import { IMAGE_TYPE_CONFIG } from '../lib/constants';

export interface RecommendationSectionProps {
  recommendation: NonNullable<TextGenerationResponse['image_recommendation']>;
  onGenerate?: (type: string, isAlternative?: boolean) => void;
  isLoading: boolean;
  hasImagePrompts: boolean;
}

export function RecommendationSection({
  recommendation,
  onGenerate,
  isLoading,
  hasImagePrompts
}: RecommendationSectionProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const config = IMAGE_TYPE_CONFIG[recommendation.recommended_type] || {
    label: recommendation.recommended_type,
    color: 'bg-gray-600',
    description: '',
    isInstant: false,
  };
  const isPostCard = recommendation.recommended_type === 'post_card';

  return (
    <div className="border-t border-linkedin-border bg-gradient-to-r from-amber-50 to-orange-50">
      {/* Header - always visible */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-amber-100/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className={cn(
            'w-8 h-8 rounded-full flex items-center justify-center',
            isPostCard ? 'bg-gray-100' : 'bg-amber-100'
          )}>
            {isPostCard ? (
              <FileText className="w-4 h-4 text-gray-600" />
            ) : (
              <Lightbulb className="w-4 h-4 text-amber-600" />
            )}
          </div>
          <div className="text-left">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm font-semibold text-gray-800">AI Recommends:</span>
              <span className={cn('px-2 py-0.5 rounded-full text-xs font-medium text-white', config.color)}>
                {config.label}
              </span>
              {isPostCard && (
                <span className="px-1.5 py-0.5 rounded text-xs font-medium bg-gray-200 text-gray-700">
                  ⚡ instant
                </span>
              )}
              <span className={cn(
                'px-1.5 py-0.5 rounded text-xs font-medium',
                recommendation.confidence === 'high' ? 'bg-green-100 text-green-700' :
                recommendation.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                'bg-gray-100 text-gray-600'
              )}>
                {recommendation.confidence}
              </span>
            </div>
          </div>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-gray-500" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-500" />
        )}
      </button>

      {/* Expanded content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 space-y-3">
              {/* Type Description */}
              <div className="text-sm text-gray-600 italic">
                {config.description}
              </div>

              {/* Reasoning (Chain-of-Thought) */}
              <div className={cn(
                'rounded-lg p-3 border',
                isPostCard ? 'bg-gray-50 border-gray-200' : 'bg-white border-amber-200'
              )}>
                <div className={cn(
                  'text-xs font-medium mb-1',
                  isPostCard ? 'text-gray-600' : 'text-amber-700'
                )}>
                  AI Reasoning:
                </div>
                <p className="text-sm text-gray-700 leading-relaxed">{recommendation.reasoning}</p>
              </div>

              {/* Style Notes - only show for AI types, not post_card */}
              {!isPostCard && recommendation.style_notes && (
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Style notes:</span> {recommendation.style_notes}
                </div>
              )}

              {/* Alternatives */}
              {recommendation.alternative_types?.length > 0 && (
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-xs text-gray-500">Alternatives (regenerates post):</span>
                  {recommendation.alternative_types.map(alt => {
                    const altConfig = IMAGE_TYPE_CONFIG[alt] || { label: alt, color: 'bg-gray-400' };
                    return (
                      <button
                        key={alt}
                        onClick={() => onGenerate?.(alt, true)}  // isAlternative = true
                        disabled={isLoading}
                        className={cn(
                          'px-2 py-0.5 rounded-full text-xs font-medium text-white transition-opacity',
                          altConfig.color,
                          isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'
                        )}
                      >
                        {altConfig.label}
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={() => onGenerate?.(recommendation.recommended_type, false)}
                disabled={isLoading}
                className={cn(
                  'w-full py-2 px-4 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-all',
                  isLoading
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : recommendation.recommended_type === 'post_card'
                      ? 'bg-gray-900 text-white hover:bg-gray-800'  // Post card style
                      : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:shadow-lg hover:from-amber-600 hover:to-orange-600'
                )}
              >
                {recommendation.recommended_type === 'post_card' ? (
                  <>
                    <FileText className={cn('w-4 h-4', isLoading && 'animate-pulse')} />
                    Generate Post Card (instant)
                  </>
                ) : (
                  <>
                    <Wand2 className={cn('w-4 h-4', isLoading && 'animate-pulse')} />
                    {hasImagePrompts
                      ? `Generate ${config.label} Image`
                      : `Generate ${config.label} (with AI prompts)`}
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

