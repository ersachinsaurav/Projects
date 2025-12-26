/**
 * Input Form Component
 * =====================
 * Main form for entering post idea and parameters
 * Includes both text and image model selection
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  Target,
  FileText,
  Settings2,
  Image as ImageIcon,
} from 'lucide-react';
import type {
  PostLength,
  Tone,
  CTAStyle,
  TextModelConfig,
  ImageModelConfig,
} from '../types';
import { cn } from '../lib/utils';

interface InputFormProps {
  idea: string;
  setIdea: (value: string) => void;
  postAngle: string;
  setPostAngle: (value: string) => void;
  draftPost: string;
  setDraftPost: (value: string) => void;
  postLength: PostLength;
  setPostLength: (value: PostLength) => void;
  tone: Tone;
  setTone: (value: Tone) => void;
  audience: string[];
  setAudience: (value: string[]) => void;
  ctaStyle: CTAStyle;
  setCtaStyle: (value: CTAStyle) => void;
  textModel: TextModelConfig;
  setTextModel: (value: TextModelConfig) => void;
  imageModel: ImageModelConfig;
  setImageModel: (value: ImageModelConfig) => void;
  generateImage: boolean;
  setGenerateImage: (value: boolean) => void;
  onGenerate: () => void;
  isGenerating: boolean;
}

const POST_LENGTH_OPTIONS: { value: PostLength; label: string; description: string }[] = [
  { value: 'short', label: 'Short', description: '100-200 chars' },
  { value: 'medium', label: 'Medium', description: '300-600 chars' },
  { value: 'long', label: 'Long', description: '800-1200 chars' },
];

const TONE_OPTIONS: { value: Tone; label: string; description: string }[] = [
  { value: 'professional', label: 'Professional', description: 'Formal, data-driven' },
  { value: 'opinionated', label: 'Opinionated', description: 'Bold takes' },
  { value: 'reflective', label: 'Reflective', description: 'Personal growth' },
];

const CTA_OPTIONS: { value: CTAStyle; label: string }[] = [
  { value: 'question', label: 'Question' },
  { value: 'statement', label: 'Statement' },
  { value: 'none', label: 'None' },
];

// Default audiences (most common targets)
const AUDIENCE_OPTIONS = [
  'founders', 'engineers', 'leaders', 'developers',
];

// Extended audience options
const EXTENDED_AUDIENCE_OPTIONS = [
  'marketers', 'designers', 'product managers', 'data scientists',
  'executives', 'entrepreneurs', 'investors', 'consultants',
];

// Claude models with latest Haiku
const TEXT_MODELS = [
  { provider: 'bedrock', model: 'claude-opus-4.5', label: 'Claude Opus 4.5', badge: 'Best' },
  { provider: 'bedrock', model: 'claude-opus-4.1', label: 'Claude Opus 4.1' },
  { provider: 'bedrock', model: 'claude-opus-4', label: 'Claude Opus 4' },
  { provider: 'bedrock', model: 'claude-sonnet-4.5', label: 'Claude Sonnet 4.5', badge: 'Balanced' },
  { provider: 'bedrock', model: 'claude-sonnet-4', label: 'Claude Sonnet 4' },
  { provider: 'bedrock', model: 'claude-haiku-4.5', label: 'Claude Haiku 4.5', badge: 'Fast' },
];

// Image models
const IMAGE_MODELS = [
  { provider: 'nova', model: 'nova-canvas', label: 'Nova Canvas', badge: 'Best', description: 'Higher quality, detailed prompts' },
  { provider: 'titan', model: 'titan-image-generator-v2', label: 'Titan v2', description: 'Fast, keyword-based prompts' },
];

export function InputForm({
  idea,
  setIdea,
  postAngle,
  setPostAngle,
  draftPost,
  setDraftPost,
  postLength,
  setPostLength,
  tone,
  setTone,
  audience,
  setAudience,
  ctaStyle,
  setCtaStyle,
  textModel,
  setTextModel,
  imageModel,
  setImageModel,
  generateImage,
  setGenerateImage,
  onGenerate,
  isGenerating,
}: InputFormProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleAudienceToggle = (item: string) => {
    if (audience.includes(item)) {
      setAudience(audience.filter((a) => a !== item));
    } else {
      setAudience([...audience, item]);
    }
  };

  const isValid = idea.trim().length >= 10;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="linkedin-card p-6 space-y-6"
    >
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="p-2 bg-gradient-to-br from-linkedin-blue to-accent-primary rounded-lg">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-linkedin-text">Create Your Post</h2>
          <p className="text-sm text-linkedin-text-secondary">Powered by Claude AI</p>
        </div>
      </div>

      {/* Main Idea Input */}
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
          <Lightbulb className="w-4 h-4 text-linkedin-blue" />
          What's your idea?
        </label>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="e.g., Share a lesson about why most startups fail at hiring..."
          rows={3}
          className="textarea-field"
        />
        <p className="text-xs text-linkedin-text-secondary">
          {idea.length} characters (minimum 10 required)
        </p>
      </div>

      {/* Post Angle (Optional) */}
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
          <Target className="w-4 h-4 text-linkedin-blue" />
          Hook or Angle
          <span className="text-linkedin-text-secondary font-normal">(optional)</span>
        </label>
        <textarea
          value={postAngle}
          onChange={(e) => setPostAngle(e.target.value)}
          placeholder="e.g., Contrarian take on remote work, Personal story about my first failed startup, Data-driven insight from analyzing 100 companies..."
          rows={2}
          className="textarea-field"
        />
      </div>

      {/* Quick Settings Row */}
      <div className="grid grid-cols-3 gap-4">
        {/* Post Length */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-linkedin-text">Length</label>
          <div className="flex flex-col gap-1">
            {POST_LENGTH_OPTIONS.map((option) => (
              <button
                key={option.value}
                onClick={() => setPostLength(option.value)}
                className={cn(
                  'px-3 py-1.5 text-sm rounded-md text-left transition-colors',
                  postLength === option.value
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tone */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-linkedin-text">Tone</label>
          <div className="flex flex-col gap-1">
            {TONE_OPTIONS.map((option) => (
              <button
                key={option.value}
                onClick={() => setTone(option.value)}
                className={cn(
                  'px-3 py-1.5 text-sm rounded-md text-left transition-colors',
                  tone === option.value
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* CTA Style */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-linkedin-text">CTA</label>
          <div className="flex flex-col gap-1">
            {CTA_OPTIONS.map((option) => (
              <button
                key={option.value}
                onClick={() => setCtaStyle(option.value)}
                className={cn(
                  'px-3 py-1.5 text-sm rounded-md text-left transition-colors',
                  ctaStyle === option.value
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Advanced Toggle */}
      <button
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="flex items-center gap-2 text-sm text-linkedin-blue hover:text-linkedin-blue-dark transition-colors"
      >
        <Settings2 className="w-4 h-4" />
        Advanced Options
        {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      {/* Advanced Options */}
      {showAdvanced && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="space-y-4 pt-2"
        >
          {/* Target Audience */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-linkedin-text">Target Audience</label>
            <div className="flex flex-wrap gap-2">
              {AUDIENCE_OPTIONS.map((item) => (
                <button
                  key={item}
                  onClick={() => handleAudienceToggle(item)}
                  className={cn(
                    'px-3 py-1 text-xs rounded-full transition-colors capitalize',
                    audience.includes(item)
                      ? 'bg-linkedin-blue text-white'
                      : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                  )}
                >
                  {item}
                </button>
              ))}
            </div>
            {/* Extended options */}
            <div className="flex flex-wrap gap-2 pt-1">
              {EXTENDED_AUDIENCE_OPTIONS.map((item) => (
                <button
                  key={item}
                  onClick={() => handleAudienceToggle(item)}
                  className={cn(
                    'px-3 py-1 text-xs rounded-full transition-colors capitalize',
                    audience.includes(item)
                      ? 'bg-accent-primary text-white'
                      : 'bg-gray-50 text-linkedin-text-secondary hover:bg-gray-100'
                  )}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          {/* Draft Post */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
              <FileText className="w-4 h-4 text-linkedin-blue" />
              Draft to Refine
              <span className="text-linkedin-text-secondary font-normal">(optional)</span>
            </label>
            <textarea
              value={draftPost}
              onChange={(e) => setDraftPost(e.target.value)}
              placeholder="Paste a draft post you want to improve..."
              rows={4}
              className="textarea-field"
            />
          </div>

          {/* Model Selection - Claude Only */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-linkedin-text">Text Model (Claude)</label>
            <div className="grid grid-cols-2 gap-2">
              {TEXT_MODELS.map((model) => (
                <button
                  key={model.model}
                  onClick={() => setTextModel({ provider: 'bedrock', model: model.model })}
                  className={cn(
                    'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                    textModel.model === model.model
                      ? 'bg-linkedin-blue text-white'
                      : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                  )}
                >
                  <div className="font-medium">{model.label}</div>
                  {model.badge && (
                    <span className={cn(
                      'absolute top-1 right-1 text-[10px] px-1.5 py-0.5 rounded-full',
                      textModel.model === model.model
                        ? 'bg-white/20 text-white'
                        : 'bg-linkedin-blue/10 text-linkedin-blue'
                    )}>
                      {model.badge}
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Image Generation Toggle */}
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex items-center gap-2">
                <ImageIcon className="w-5 h-5 text-accent-primary" />
                <div>
                  <span className="text-sm font-medium text-linkedin-text">Generate AI Illustration</span>
                  <p className="text-xs text-linkedin-text-secondary">
                    {generateImage ? 'AI will generate an illustration (slower)' : 'Post Card will be generated (instant)'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setGenerateImage(!generateImage)}
                className={cn(
                  'relative w-12 h-7 rounded-full transition-colors flex-shrink-0',
                  generateImage ? 'bg-accent-primary' : 'bg-gray-300'
                )}
              >
                <span
                  className={cn(
                    'absolute top-1 w-5 h-5 rounded-full bg-white shadow-md transition-transform',
                    generateImage ? 'left-6' : 'left-1'
                  )}
                />
              </button>
            </div>
          </div>

          {/* Image Model Selection - Only show when image gen is ON */}
          {generateImage && (
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
                <ImageIcon className="w-4 h-4 text-accent-primary" />
                Image Model
              </label>
              <div className="grid grid-cols-2 gap-2">
                {IMAGE_MODELS.map((model) => (
                  <button
                    key={model.model}
                    onClick={() => setImageModel({ provider: model.provider as 'nova' | 'titan', model: model.model })}
                    className={cn(
                      'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                      imageModel.model === model.model
                        ? 'bg-accent-primary text-white'
                        : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                    )}
                  >
                    <div className="font-medium">{model.label}</div>
                    <div className={cn(
                      'text-xs',
                      imageModel.model === model.model ? 'text-white/70' : 'text-linkedin-text-secondary'
                    )}>
                      {model.description}
                    </div>
                    {model.badge && (
                      <span className={cn(
                        'absolute top-1 right-1 text-[10px] px-1.5 py-0.5 rounded-full',
                        imageModel.model === model.model
                          ? 'bg-white/20 text-white'
                          : 'bg-accent-primary/10 text-accent-primary'
                      )}>
                        {model.badge}
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Generate Button */}
      <button
        onClick={onGenerate}
        disabled={!isValid || isGenerating}
        className={cn(
          'w-full py-3 rounded-full font-semibold transition-all flex items-center justify-center gap-2',
          isValid && !isGenerating
            ? 'bg-gradient-to-r from-linkedin-blue to-accent-primary text-white hover:shadow-lg hover:scale-[1.02]'
            : 'bg-gray-200 text-gray-400 cursor-not-allowed'
        )}
      >
        {isGenerating ? (
          <>
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Generating...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Generate Post {generateImage ? '+ AI Image' : '+ Card'}
          </>
        )}
      </button>
    </motion.div>
  );
}
