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
  Moon,
  Sun,
  Ruler,
  Mic,
  MousePointerClick,
  Users,
  Cpu,
} from 'lucide-react';
import type {
  PostLength,
  Tone,
  CTAStyle,
  TextModelConfig,
  ImageModelConfig,
} from '../types';
import { cn } from '../lib/utils';
import {
  POST_LENGTH_OPTIONS,
  TONE_OPTIONS,
  CTA_OPTIONS,
  DEFAULT_AUDIENCES,
  ALL_AUDIENCES,
  TEXT_MODELS,
  IMAGE_MODELS,
} from '../lib/defaults';

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
  generatePostcard: boolean;
  setGeneratePostcard: (value: boolean) => void;
  postcardTheme: 'dark' | 'light';
  setPostcardTheme: (value: 'dark' | 'light') => void;
  generateImage: boolean;
  setGenerateImage: (value: boolean) => void;
  generateCarousel: boolean;
  setGenerateCarousel: (value: boolean) => void;
  onGenerate: () => void;
  isGenerating: boolean;
}

// All constants are now imported from '../lib/defaults'

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
  generatePostcard,
  setGeneratePostcard,
  postcardTheme,
  setPostcardTheme,
  generateImage,
  setGenerateImage,
  generateCarousel,
  setGenerateCarousel,
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
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-linkedin-blue to-accent-primary">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-linkedin-text">Create Your Post</h2>
            <p className="text-sm text-linkedin-text-secondary">Powered by AI</p>
          </div>
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
          <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
            <Ruler className="w-4 h-4 text-linkedin-blue" />
            Length
          </label>
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
          <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
            <Mic className="w-4 h-4 text-linkedin-blue" />
            Tone
          </label>
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
          <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
            <MousePointerClick className="w-4 h-4 text-linkedin-blue" />
            CTA
          </label>
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
          className="space-y-6 pt-2"
        >
          {/* Target Audience */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
              <Users className="w-4 h-4 text-linkedin-blue" />
              Target Audience
            </label>
            <div className="flex flex-wrap gap-2">
              {(DEFAULT_AUDIENCES as readonly string[]).map((item: string) => (
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
              {(ALL_AUDIENCES as readonly string[]).filter((a: string) => !(DEFAULT_AUDIENCES as readonly string[]).includes(a as any)).map((item: string) => (
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

          {/* Model Selection - Ollama (Mistral/Llama) and Bedrock (Claude) */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
              <Cpu className="w-4 h-4 text-linkedin-blue" />
              Text Model
            </label>
            <div className="grid grid-cols-2 gap-2">
              {TEXT_MODELS.map((model) => (
                <button
                  key={`${model.provider}-${model.model}`}
                  onClick={() => setTextModel({ provider: model.provider, model: model.model })}
                  className={cn(
                    'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                    textModel.provider === model.provider && textModel.model === model.model
                      ? 'bg-linkedin-blue text-white'
                      : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                  )}
                >
                  <div className="font-medium">{model.label}</div>
                  <div className="text-xs opacity-70 capitalize mt-0.5">{model.provider}</div>
                  {model.badge && (
                    <span className={cn(
                      'absolute top-1 right-1 text-[10px] px-1.5 py-0.5 rounded-full',
                      textModel.provider === model.provider && textModel.model === model.model
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

          {/* Generation Mode Selection */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
              <Sparkles className="w-4 h-4 text-accent-primary" />
              Generation Mode
            </label>
            <div className="grid grid-cols-1 gap-2">
              {/* Generate Postcard */}
              <button
                onClick={() => {
                  setGeneratePostcard(true);
                  setGenerateImage(false);
                  setGenerateCarousel(false);
                  setPostcardTheme('dark'); // Reset theme to dark when switching back
                }}
                className={cn(
                  'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                  generatePostcard
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
              <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  <div className="flex-1">
                    <div className="font-medium">Postcard</div>
                    <div className={cn('text-xs', generatePostcard ? 'text-white/80' : 'text-linkedin-text-secondary')}>
                      Instant post card generation (no AI)
                    </div>
                  </div>
                </div>
                {generatePostcard && (
                  <span className="absolute top-1 right-1 px-1.5 py-0.5 text-xs font-medium bg-white/20 text-white rounded">
                    Default
                  </span>
                )}
              </button>

              {/* Dark/Light Theme Selection - Only visible when Generate Postcard is ON */}
              {generatePostcard && (
                <div className="space-y-1">
                  <label className="text-xs font-medium text-linkedin-text-secondary">Theme</label>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setPostcardTheme('dark')}
                      className={cn(
                        'flex-1 px-3 py-1.5 text-sm rounded-lg transition-colors text-center relative',
                        postcardTheme === 'dark'
                          ? 'bg-linkedin-blue text-white'
                          : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                      )}
                    >
                      <div className="flex items-center justify-center gap-1.5">
                        <Moon className="w-4 h-4" />
                        <span className="font-medium">Dark</span>
                      </div>
                    </button>
                    <button
                      onClick={() => setPostcardTheme('light')}
                      className={cn(
                        'flex-1 px-3 py-1.5 text-sm rounded-lg transition-colors text-center relative',
                        postcardTheme === 'light'
                          ? 'bg-linkedin-blue text-white'
                          : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                      )}
                    >
                      <div className="flex items-center justify-center gap-1.5">
                        <Sun className="w-4 h-4" />
                        <span className="font-medium">Light</span>
                      </div>
                    </button>
                </div>
              </div>
              )}

              {/* Generate AI Illustration */}
              <button
                onClick={() => {
                  setGenerateImage(true);
                  setGeneratePostcard(false);
                  setGenerateCarousel(false);
                  setPostcardTheme('dark'); // Reset theme to dark
                }}
                className={cn(
                  'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                  generateImage
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
                <div className="flex items-center gap-2">
                  <ImageIcon className="w-4 h-4" />
                  <div className="flex-1">
                    <div className="font-medium">AI Illustration</div>
                    <div className={cn('text-xs', generateImage ? 'text-white/80' : 'text-linkedin-text-secondary')}>
                      AI-generated illustrations (slower)
                    </div>
                  </div>
                </div>
              </button>

              {/* Generate Carousel */}
              <button
                onClick={() => {
                  setGenerateCarousel(true);
                  setGeneratePostcard(false);
                  setGenerateImage(false);
                  setPostcardTheme('dark'); // Reset theme to dark
                }}
                className={cn(
                  'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                  generateCarousel
                    ? 'bg-linkedin-blue text-white'
                    : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                )}
              >
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  <div className="flex-1">
                    <div className="font-medium">Carousel</div>
                    <div className={cn('text-xs', generateCarousel ? 'text-white/80' : 'text-linkedin-text-secondary')}>
                      AI cover + post card sections with arrows
                    </div>
                  </div>
                </div>
                </button>
              </div>
          </div>

          {/* Image Model Selection - Show when AI Illustration OR Carousel is ON */}
          {(generateImage || generateCarousel) && (
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-medium text-linkedin-text">
                <ImageIcon className="w-4 h-4 text-accent-primary" />
                Image Model
              </label>
              <div className="grid grid-cols-2 gap-2">
                {IMAGE_MODELS.map((model) => (
                  <button
                    key={model.model}
                    onClick={() => setImageModel({ provider: model.provider as 'nova' | 'titan' | 'sdxl', model: model.model })}
                    className={cn(
                      'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                      imageModel.model === model.model
                        ? 'bg-linkedin-blue text-white'
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
            {generateCarousel
              ? 'Generate Carousel'
              : generateImage
                ? 'Generate AI Illustration'
                : 'Generate Postcard'}
          </>
        )}
      </button>
    </motion.div>
  );
}
