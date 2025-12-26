/**
 * LinkedIn Preview Component
 * ===========================
 * Shows complete LinkedIn post preview (text + hashtags + image)
 * Like how it appears in the actual LinkedIn feed
 *
 * Features:
 * - Editor mode with inline hashtags
 * - Image display integrated with post
 * - Keyboard shortcuts for formatting
 * - Regenerate buttons for text/images separately
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Copy,
  Check,
  Linkedin,
  Clock,
  Zap,
  Bold,
  Italic,
  Underline,
  Strikethrough,
  Undo2,
  Redo2,
  Download,
  RefreshCw,
  Sparkles,
  Image as ImageIcon,
  X,
  FileText,
  MessageSquare,
  ThumbsUp,
  Share2,
  Send,
} from 'lucide-react';
import type { TextGenerationResponse, ImageGenerationResponse } from '../types';
import { cn, copyToClipboard, formatNumber, formatDuration, downloadImage, downloadPDF } from '../lib/utils';
import {
  toUnicodeBold,
  toUnicodeItalic,
  toUnicodeUnderline,
  toUnicodeStrikethrough,
  removeUnicodeFormatting,
} from '../lib/unicode';
import { PROFILE_CONFIG, LINKEDIN_LIMITS, EDITOR_CONFIG } from '../lib/constants';
import { RecommendationSection } from './RecommendationSection';
import profilePicture from '../images/profilePicture.jpeg';

interface LinkedInPreviewProps {
  textData: TextGenerationResponse | null;
  imageData: ImageGenerationResponse | null;
  isTextLoading: boolean;
  isImageLoading: boolean;
  onTextChange?: (text: string, hashtags: string[]) => void;
  onRegenerateText: () => void;
  onRegenerateImages: () => void;
  onGeneratePostCard?: (theme: 'dark' | 'light') => void;
  onGenerateWithRecommendation?: (type: string, isAlternative?: boolean) => void;
  useAIImages: boolean;
}

export function LinkedInPreview({
  textData,
  imageData,
  isTextLoading,
  isImageLoading,
  onTextChange: _onTextChange, // Reserved for future use
  onRegenerateText,
  onRegenerateImages,
  onGeneratePostCard,
  onGenerateWithRecommendation,
  useAIImages,
}: LinkedInPreviewProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(''); // Combined text + hashtags
  const [copied, setCopied] = useState(false);
  const [selectedImage, setSelectedImage] = useState<number | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Undo/Redo history
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const isUndoRedoRef = useRef(false);

  // Combine text and hashtags for editing
  const getFullContent = useCallback(() => {
    if (!textData) return '';
    const text = textData.post_text || '';
    const hashtags = textData.hashtags?.join(' ') || '';
    return hashtags ? `${text}\n\n${hashtags}` : text;
  }, [textData]);

  // Initialize content when data changes
  useEffect(() => {
    if (textData) {
      const content = getFullContent();
      setEditedContent(content);
      setHistory([content]);
      setHistoryIndex(0);
      // Auto-enable editing mode when content is generated
      setIsEditing(true);
    }
  }, [textData?.post_text, textData?.hashtags, getFullContent]);

  // Track content changes for undo/redo
  useEffect(() => {
    if (isUndoRedoRef.current) {
      isUndoRedoRef.current = false;
      return;
    }

    if (editedContent && history[historyIndex] !== editedContent) {
      const newHistory = history.slice(0, historyIndex + 1);
      newHistory.push(editedContent);
      if (newHistory.length > EDITOR_CONFIG.maxHistorySize) {
        newHistory.shift();
      }
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
    }
  }, [editedContent]);

  const handleUndo = useCallback(() => {
    if (historyIndex > 0) {
      isUndoRedoRef.current = true;
      setHistoryIndex(historyIndex - 1);
      setEditedContent(history[historyIndex - 1]);
    }
  }, [history, historyIndex]);

  const handleRedo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      isUndoRedoRef.current = true;
      setHistoryIndex(historyIndex + 1);
      setEditedContent(history[historyIndex + 1]);
    }
  }, [history, historyIndex]);

  const canUndo = historyIndex > 0;
  const canRedo = historyIndex < history.length - 1;

  const handleCopy = async () => {
    const success = await copyToClipboard(editedContent);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Apply Unicode formatting to selected text
  const applyFormatting = useCallback((formatter: (text: string) => string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = editedContent.slice(start, end);

    if (selectedText.length === 0) return;

    const formattedText = formatter(selectedText);
    const newContent = editedContent.slice(0, start) + formattedText + editedContent.slice(end);

    setEditedContent(newContent);

    requestAnimationFrame(() => {
      textarea.focus();
      textarea.setSelectionRange(start, start + formattedText.length);
    });
  }, [editedContent]);

  const resetFormatting = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    if (start === end) {
      const plainText = removeUnicodeFormatting(editedContent);
      setEditedContent(plainText);
    } else {
      const selectedText = editedContent.slice(start, end);
      const plainText = removeUnicodeFormatting(selectedText);
      const newContent = editedContent.slice(0, start) + plainText + editedContent.slice(end);
      setEditedContent(newContent);

      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(start, start + plainText.length);
      });
    }
  }, [editedContent]);

  // Keyboard shortcuts
  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const modifier = isMac ? e.metaKey : e.ctrlKey;

    if (modifier) {
      switch (e.key.toLowerCase()) {
        case 'z':
          e.preventDefault();
          if (e.shiftKey) {
            handleRedo();
          } else {
            handleUndo();
          }
          break;
        case 'y':
          e.preventDefault();
          handleRedo();
          break;
        case 'b':
          e.preventDefault();
          applyFormatting(toUnicodeBold);
          break;
        case 'i':
          e.preventDefault();
          applyFormatting(toUnicodeItalic);
          break;
        case 'u':
          e.preventDefault();
          applyFormatting(toUnicodeUnderline);
          break;
        case 's':
          if (e.shiftKey) {
            e.preventDefault();
            applyFormatting(toUnicodeStrikethrough);
          }
          break;
        case 'r':
          if (e.shiftKey) {
            e.preventDefault();
            resetFormatting();
          }
          break;
      }
    }
  }, [applyFormatting, resetFormatting, handleUndo, handleRedo]);

  const handleDownloadImage = (base64: string, index: number) => {
    downloadImage(base64, `linkedin-image-${index + 1}.png`);
  };

  const handleDownloadPDF = () => {
    if (imageData?.pdf_base64) {
      downloadPDF(imageData.pdf_base64, 'linkedin-carousel.pdf');
    }
  };

  const charCount = editedContent.length;
  const isOverLimit = charCount > LINKEDIN_LIMITS.maxPostChars;
  const hasImages = imageData && imageData.images.length > 0;

  // Empty state
  if (!textData && !isTextLoading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="linkedin-card p-6"
      >
        <div className="text-center py-16">
          <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-linkedin-blue/20 to-accent-primary/20 flex items-center justify-center">
            <Linkedin className="w-10 h-10 text-linkedin-blue" />
          </div>
          <h3 className="text-xl font-semibold text-linkedin-text mb-2">
            Your LinkedIn Post Preview
          </h3>
          <p className="text-sm text-linkedin-text-secondary max-w-xs mx-auto">
            Fill in your idea on the left and hit "Generate Post" to see your content appear here.
          </p>
        </div>
      </motion.div>
    );
  }

  // Loading state
  if (isTextLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="linkedin-card p-6 space-y-4"
      >
        {/* Profile skeleton */}
        <div className="flex items-center gap-3">
          <div className="skeleton w-12 h-12 rounded-full" />
          <div className="space-y-2 flex-1">
            <div className="skeleton h-4 w-32" />
            <div className="skeleton h-3 w-48" />
          </div>
        </div>

        {/* Content skeleton */}
        <div className="space-y-2 pt-4">
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-5/6" />
          <div className="skeleton h-4 w-4/6" />
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-3/6" />
        </div>

        {/* Image skeleton */}
        <div className="skeleton h-64 w-full rounded-lg mt-4" />

        <div className="flex items-center justify-center py-4">
          <div className="flex items-center gap-2 text-linkedin-blue">
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span className="text-sm">Generating your post...</span>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-4"
      >
        {/* Post Preview */}
        {(
          <div className="linkedin-card overflow-hidden">
            {/* LinkedIn-style Header */}
            <div className="p-4 border-b border-linkedin-border">
          <div className="flex items-center gap-3">
            <img
              src={profilePicture}
              alt={PROFILE_CONFIG.name}
              className="w-12 h-12 rounded-full object-cover"
            />
            <div className="flex-1">
              <div className="font-semibold text-linkedin-text">{PROFILE_CONFIG.name}</div>
              <div className="text-xs text-linkedin-text-secondary">
              {PROFILE_CONFIG.title} • 1st
              </div>
              <div className="text-xs text-linkedin-text-secondary flex items-center gap-1">
                <span>Just now</span>
                <span>•</span>
                <span>🌐</span>
              </div>
            </div>

            {/* Follow button */}
            <button className="px-4 py-1.5 text-sm font-semibold text-linkedin-blue border border-linkedin-blue rounded-full hover:bg-linkedin-blue hover:text-white transition-colors">
              + Follow
            </button>

            {/* Action buttons */}
            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className={cn(
                  'p-2 rounded-full transition-colors',
                  copied ? 'bg-green-100 text-green-600' : 'hover:bg-gray-100 text-linkedin-text-secondary'
                )}
                title="Copy to clipboard"
              >
                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </div>

        {/* Formatting Toolbar */}
        {isEditing && (
          <div className="px-4 py-2 border-b border-linkedin-border bg-gray-50 flex items-center gap-1 flex-wrap">
            <button
              onClick={handleUndo}
              disabled={!canUndo}
              className={cn(
                'p-1.5 rounded transition-colors',
                canUndo ? 'hover:bg-gray-200 text-linkedin-text' : 'text-gray-300 cursor-not-allowed'
              )}
              title="Undo (⌘Z)"
            >
              <Undo2 className="w-4 h-4" />
            </button>
            <button
              onClick={handleRedo}
              disabled={!canRedo}
              className={cn(
                'p-1.5 rounded transition-colors',
                canRedo ? 'hover:bg-gray-200 text-linkedin-text' : 'text-gray-300 cursor-not-allowed'
              )}
              title="Redo (⌘⇧Z)"
            >
              <Redo2 className="w-4 h-4" />
            </button>

            <div className="w-px h-5 bg-gray-300 mx-1" />

            <button
              onClick={() => applyFormatting(toUnicodeBold)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Bold (⌘B)"
            >
              <Bold className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toUnicodeItalic)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Italic (⌘I)"
            >
              <Italic className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toUnicodeUnderline)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Underline (⌘U)"
            >
              <Underline className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toUnicodeStrikethrough)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Strikethrough (⌘⇧S)"
            >
              <Strikethrough className="w-4 h-4 text-linkedin-text" />
            </button>

            <div className="w-px h-5 bg-gray-300 mx-1" />

            <button
              onClick={resetFormatting}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors text-xs text-linkedin-text-secondary"
              title="Reset formatting"
            >
              Clear
            </button>

            <span className="text-xs text-linkedin-text-secondary ml-auto">
              {formatNumber(charCount)} / {formatNumber(LINKEDIN_LIMITS.maxPostChars)}
              {isOverLimit && <span className="text-red-500 ml-1">⚠️</span>}
            </span>
          </div>
        )}

        {/* Post Content (Editor) */}
        <div className="p-4">
          <textarea
            ref={textareaRef}
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            onKeyDown={handleKeyDown}
            className={cn(
              'w-full min-h-[350px] p-0 border-none focus:outline-none focus:ring-0 resize-y',
              'font-sans text-sm leading-relaxed text-linkedin-text bg-transparent',
              isOverLimit && 'text-red-500'
            )}
            placeholder="Your post content will appear here..."
          />
        </div>

        {/* Image Section */}
        <div className="border-t border-linkedin-border">
          {isImageLoading ? (
            <div className="p-4">
              <div className="w-full h-80 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <RefreshCw className="w-12 h-12 mx-auto mb-3 text-linkedin-blue animate-spin" />
                  <span className="text-base font-medium text-gray-600">Generating image...</span>
                  <p className="text-sm text-gray-400 mt-1">This may take a few moments</p>
                </div>
              </div>
            </div>
          ) : hasImages ? (
            <div className="relative">
              {/* Single image or first image of carousel */}
              <img
                src={`data:image/${imageData.images[0].format};base64,${imageData.images[0].base64_data}`}
                alt="Post image"
                className="w-full object-cover cursor-pointer"
                onClick={() => setSelectedImage(0)}
              />

              {/* Multiple images indicator */}
              {imageData.images.length > 1 && (
                <div className="absolute top-4 right-4 bg-black/70 text-white text-xs px-2 py-1 rounded-full">
                  1 / {imageData.images.length}
                </div>
              )}

              {/* Image thumbnails for carousel */}
              {imageData.images.length > 1 && (
                <div className="p-2 flex gap-2 overflow-x-auto">
                  {imageData.images.map((img, idx) => (
                    <img
                      key={img.id}
                      src={`data:image/${img.format};base64,${img.base64_data}`}
                      alt={`Image ${idx + 1}`}
                      className={cn(
                        'w-16 h-16 object-cover rounded cursor-pointer border-2 transition-all',
                        idx === 0 ? 'border-linkedin-blue' : 'border-transparent hover:border-gray-300'
                      )}
                      onClick={() => setSelectedImage(idx)}
                    />
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="p-4 text-center text-sm text-linkedin-text-secondary">
              <ImageIcon className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>Image will appear here after generation</p>
            </div>
          )}
        </div>

        {/* LinkedIn-style Engagement Bar */}
        <div className="px-4 py-2 border-t border-linkedin-border">
          <div className="flex items-center justify-between text-xs text-linkedin-text-secondary pb-2 border-b border-linkedin-border">
            <span className="flex items-center gap-1">
              <span className="flex -space-x-1">
                <span className="w-4 h-4 rounded-full bg-blue-500 flex items-center justify-center text-white text-[8px]">👍</span>
                <span className="w-4 h-4 rounded-full bg-red-500 flex items-center justify-center text-white text-[8px]">❤️</span>
              </span>
              <span className="ml-1">42</span>
            </span>
            <span>3 comments • 1 repost</span>
          </div>
          <div className="flex items-center justify-around py-1">
            <button className="flex items-center gap-2 px-4 py-2 rounded hover:bg-gray-100 transition-colors text-linkedin-text-secondary">
              <ThumbsUp className="w-4 h-4" />
              <span className="text-sm font-medium">Like</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded hover:bg-gray-100 transition-colors text-linkedin-text-secondary">
              <MessageSquare className="w-4 h-4" />
              <span className="text-sm font-medium">Comment</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded hover:bg-gray-100 transition-colors text-linkedin-text-secondary">
              <Share2 className="w-4 h-4" />
              <span className="text-sm font-medium">Repost</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded hover:bg-gray-100 transition-colors text-linkedin-text-secondary">
              <Send className="w-4 h-4" />
              <span className="text-sm font-medium">Send</span>
            </button>
          </div>
        </div>

        {/* AI Image Recommendation */}
        {textData?.image_recommendation && (
          <RecommendationSection
            recommendation={textData.image_recommendation}
            onGenerate={onGenerateWithRecommendation}
            isLoading={isTextLoading || isImageLoading}
            hasImagePrompts={Boolean(textData.image_prompts?.length)}
          />
        )}

        {/* Regenerate Buttons */}
        <div className="px-4 py-3 bg-gray-50 border-t border-linkedin-border flex items-center gap-3">
          <button
            onClick={onRegenerateText}
            disabled={isTextLoading}
            className={cn(
              'flex-1 py-2 px-4 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors',
              isTextLoading
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-white border border-linkedin-border text-linkedin-text hover:bg-gray-50'
            )}
          >
            <RefreshCw className={cn('w-4 h-4', isTextLoading && 'animate-spin')} />
            Regenerate Text
          </button>
          <button
            onClick={useAIImages ? onRegenerateImages : () => onGeneratePostCard?.('dark')}
            disabled={isImageLoading || !textData}
            className={cn(
              'flex-1 py-2 px-4 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors',
              isImageLoading || !textData
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : useAIImages
                  ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white hover:shadow-lg'
                  : 'bg-gray-900 text-white hover:bg-gray-800'
            )}
          >
            <Sparkles className={cn('w-4 h-4', isImageLoading && 'animate-pulse')} />
            {useAIImages ? 'Regenerate AI Image' : 'Regenerate Card'}
          </button>
        </div>

        {/* Stats Footer */}
        {(textData?.generation_time_ms || imageData?.generation_time_ms) && (
          <div className="px-4 py-2 bg-gray-50 border-t border-linkedin-border flex items-center justify-between text-xs text-linkedin-text-secondary">
            <div className="flex items-center gap-4">
              {textData?.tokens_used && (
                <span className="flex items-center gap-1">
                  <Zap className="w-3 h-3" />
                  {formatNumber(textData.tokens_used)} tokens
                </span>
              )}
              {textData?.generation_time_ms && (
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  Text: {formatDuration(textData.generation_time_ms)}
                </span>
              )}
              {imageData?.generation_time_ms && (
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  Image: {formatDuration(imageData.generation_time_ms)}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              {textData?.model_used && (
                <span className="bg-gray-200 px-2 py-0.5 rounded text-xs">
                  {textData.model_used}
                </span>
              )}
              {imageData?.model_used && (
                <span className="bg-gray-200 px-2 py-0.5 rounded text-xs">
                  {imageData.model_used}
                </span>
              )}
            </div>
          </div>
        )}

          {/* Download Options */}
          {hasImages && (
            <div className="px-4 py-2 bg-gray-50 border-t border-linkedin-border flex items-center justify-end gap-2">
              <button
                onClick={() => handleDownloadImage(imageData.images[0].base64_data, 0)}
                className="text-xs text-linkedin-blue hover:underline flex items-center gap-1"
              >
                <Download className="w-3 h-3" />
                Download Image
              </button>
              {imageData.images.length > 1 && imageData.pdf_base64 && (
                <button
                  onClick={handleDownloadPDF}
                  className="text-xs text-linkedin-blue hover:underline flex items-center gap-1"
                >
                  <FileText className="w-3 h-3" />
                  Download PDF
                </button>
              )}
            </div>
          )}
          </div>
        )}
      </motion.div>

      {/* Image Lightbox */}
      <AnimatePresence>
        {selectedImage !== null && imageData && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
            onClick={() => setSelectedImage(null)}
          >
            <button
              className="absolute top-4 right-4 p-2 bg-white/10 rounded-full hover:bg-white/20 transition-colors"
              onClick={() => setSelectedImage(null)}
            >
              <X className="w-6 h-6 text-white" />
            </button>

            <motion.img
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              src={`data:image/${imageData.images[selectedImage].format};base64,${imageData.images[selectedImage].base64_data}`}
              alt="Full size preview"
              className="max-w-full max-h-full object-contain rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />

            {/* Navigation for multiple images */}
            {imageData.images.length > 1 && (
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedImage(Math.max(0, selectedImage - 1));
                  }}
                  disabled={selectedImage === 0}
                  className="px-4 py-2 bg-white/20 rounded-full text-white disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="text-white">
                  {selectedImage + 1} / {imageData.images.length}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedImage(Math.min(imageData.images.length - 1, selectedImage + 1));
                  }}
                  disabled={selectedImage === imageData.images.length - 1}
                  className="px-4 py-2 bg-white/20 rounded-full text-white disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

