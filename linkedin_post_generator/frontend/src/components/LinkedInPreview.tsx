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
  RefreshCw,
  Sparkles,
  Image as ImageIcon,
  X,
  MessageSquare,
  ThumbsUp,
  Share2,
  Send,
} from 'lucide-react';
import type { TextGenerationResponse, ImageGenerationResponse } from '../types';
import { cn, copyToClipboard, formatNumber, formatDuration, downloadImage, downloadPDF, getFilenameFromContent } from '../lib/utils';
import {
  removeUnicodeFormatting,
  toggleBold,
  toggleItalic,
  toggleUnderline,
  toggleStrikethrough,
} from '../lib/unicode';
import { PROFILE_CONFIG, LINKEDIN_LIMITS, EDITOR_CONFIG } from '../lib/constants';
import { RecommendationSection } from './RecommendationSection';

// =============================================================================
// PROFILE PICTURE CUSTOMIZATION
// =============================================================================
// To use your own profile picture:
// 1. Add your photo as 'profilePicture.jpeg' in src/images/
// 2. Comment out the placeholder import below
// 3. Uncomment the custom import
//
// import profilePicture from '../images/profilePicture.jpeg';
import profilePicture from '../images/placeholder-avatar.svg';

interface LinkedInPreviewProps {
  textData: TextGenerationResponse | null;
  imageData: ImageGenerationResponse | null;
  isTextLoading: boolean;
  isImageLoading: boolean;
  onTextChange?: (text: string, hashtags: string[]) => void;
  onRegenerateText: () => void;
  onRegenerateImages: () => void;
  onGeneratePostCard?: (theme?: 'dark' | 'light') => void;
  onGenerateWithRecommendation?: (type: string, isAlternative?: boolean) => void;
  useAIImages: boolean;
  usePostcard?: boolean;
  useCarousel?: boolean;  // Explicitly track carousel mode for button labels
  postcardTheme?: 'dark' | 'light';
  isManualMode?: boolean;  // If true, starts in edit mode for direct text entry
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
  usePostcard = false,
  useCarousel = false,
  postcardTheme = 'dark',
  isManualMode = false,
}: LinkedInPreviewProps) {
  // In manual mode, start in editing mode by default
  const [isEditing, setIsEditing] = useState(isManualMode);
  const [editedContent, setEditedContent] = useState(''); // Combined text + hashtags
  const [copied, setCopied] = useState(false);
  const [selectedImage, setSelectedImage] = useState<number>(0);
  const [isGalleryOpen, setIsGalleryOpen] = useState(false);
  const [isZoomed, setIsZoomed] = useState(false);
  const [panPosition, setPanPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [mouseDownPos, setMouseDownPos] = useState<{ x: number; y: number } | null>(null);
  const imageRef = useRef<HTMLImageElement>(null);
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
          applyFormatting(toggleBold);
          break;
        case 'i':
          e.preventDefault();
          applyFormatting(toggleItalic);
          break;
        case 'u':
          e.preventDefault();
          applyFormatting(toggleUnderline);
          break;
        case 's':
          if (e.shiftKey) {
            e.preventDefault();
            applyFormatting(toggleStrikethrough);
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
    // Use shared utility for consistent filename generation
    const concept = textData?.image_prompts?.[index]?.concept || imageData?.images[index]?.concept;
    const filename = getFilenameFromContent({
      title: textData?.infographic_text?.title,
      postText: textData?.post_text,
      concept,
      defaultName: `linkedin-post-image-${index + 1}`,
      extension: 'png',
    });

    downloadImage(base64, filename);
  };

  const handleDownloadPDF = () => {
    if (imageData?.pdf_base64) {
      let filename = imageData.pdf_title || 'linkedin-carousel.pdf';

      // If filename doesn't have .pdf extension or needs sanitization, ensure it's clean
      if (!filename.endsWith('.pdf')) {
        filename = filename + '.pdf';
      }

      // Ensure filename is already sanitized (backend should handle this, but double-check)
      // Backend now sends sanitized filenames, so this should be fine
      downloadPDF(imageData.pdf_base64, filename);
    }
  };

  const charCount = editedContent.length;
  const isOverLimit = charCount > LINKEDIN_LIMITS.maxPostChars;
  const hasImages = imageData && imageData.images.length > 0;

  // Reset selected image when images change
  useEffect(() => {
    if (hasImages && imageData) {
      if (selectedImage >= imageData.images.length) {
        setSelectedImage(0);
      }
    }
  }, [hasImages, imageData, selectedImage]);

  // Reset zoom when gallery closes or image changes
  useEffect(() => {
    if (!isGalleryOpen) {
      setIsZoomed(false);
      setPanPosition({ x: 0, y: 0 });
    }
  }, [isGalleryOpen]);

  useEffect(() => {
    setIsZoomed(false);
    setPanPosition({ x: 0, y: 0 });
  }, [selectedImage]);

  // Keyboard navigation for gallery
  useEffect(() => {
    if (!isGalleryOpen || !imageData) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't handle if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          if (!isZoomed && selectedImage > 0) {
            setSelectedImage(selectedImage - 1);
          }
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (!isZoomed && selectedImage < imageData.images.length - 1) {
            setSelectedImage(selectedImage + 1);
          }
          break;
        case 'Escape':
          e.preventDefault();
          setIsGalleryOpen(false);
          setIsZoomed(false);
          setPanPosition({ x: 0, y: 0 });
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isGalleryOpen, imageData, selectedImage, isZoomed]);

  // Pan/drag handlers for zoomed image
  const handleMouseDown = (e: React.MouseEvent<HTMLImageElement>) => {
    if (!isZoomed) return;
    e.preventDefault();
    setIsDragging(true);
    setMouseDownPos({ x: e.clientX, y: e.clientY });
    setDragStart({
      x: e.clientX - panPosition.x,
      y: e.clientY - panPosition.y,
    });
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLImageElement>) => {
    if (!isZoomed || !isDragging) return;
    e.preventDefault();
    setPanPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleMouseLeave = () => {
    setIsDragging(false);
    setMouseDownPos(null);
  };

  // Empty state - but NOT for manual mode (show editor directly)
  if (!textData && !isTextLoading && !isManualMode) {
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
              onClick={() => applyFormatting(toggleBold)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Bold (⌘B) - Toggle"
            >
              <Bold className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toggleItalic)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Italic (⌘I) - Toggle"
            >
              <Italic className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toggleUnderline)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Underline (⌘U) - Toggle"
            >
              <Underline className="w-4 h-4 text-linkedin-text" />
            </button>
            <button
              onClick={() => applyFormatting(toggleStrikethrough)}
              className="p-1.5 rounded hover:bg-gray-200 transition-colors"
              title="Strikethrough (⌘⇧S) - Toggle"
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
            placeholder={isManualMode
              ? "Paste your post here...\n\nUse the toolbar above to format text.\nAdd #hashtags at the end."
              : "Your post content will appear here..."
            }
          />
        </div>

        {/* Image Section - Hidden in manual mode unless there's an image */}
        {(!isManualMode || hasImages || isImageLoading) && (
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
                {/* Image container with navigation */}
                <div className="relative group">
                  {/* Current image display */}
                  <img
                    src={`data:image/${imageData.images[selectedImage].format};base64,${imageData.images[selectedImage].base64_data}`}
                    alt="Post image"
                    className="w-full object-cover cursor-pointer"
                    onClick={() => setIsGalleryOpen(true)}
                  />

                  {/* Download buttons overlay - appears on hover */}
                  <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity z-20 flex items-center gap-2">
                    {/* PDF Download button */}
                    {imageData.pdf_base64 && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDownloadPDF();
                        }}
                        className="p-2 bg-white/90 hover:bg-white rounded-full shadow-lg transition-all hover:scale-110"
                        title="Download PDF"
                      >
                        <div className="w-5 h-5 text-linkedin-text flex items-center justify-center font-bold text-xs">PDF</div>
                      </button>
                    )}
                    {/* Image Download button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDownloadImage(imageData.images[selectedImage].base64_data, selectedImage);
                      }}
                      className="p-2 bg-white/90 hover:bg-white rounded-full shadow-lg transition-all hover:scale-110"
                      title="Download image"
                    >
                      <ImageIcon className="w-5 h-5 text-linkedin-text" />
                    </button>
                  </div>

                  {/* Navigation arrows for multiple images */}
                  {imageData.images.length > 1 && (
                    <>
                      {/* Previous button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedImage(Math.max(0, selectedImage - 1));
                        }}
                        disabled={selectedImage === 0}
                        className={cn(
                          'absolute left-2 top-1/2 -translate-y-1/2 p-2 rounded-full text-white transition-all z-10',
                          'flex items-center justify-center',
                          selectedImage === 0
                            ? 'bg-black/30 opacity-50 cursor-not-allowed'
                            : 'bg-black/60 hover:bg-black/80 opacity-100'
                        )}
                        aria-label="Previous image"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                      </button>

                      {/* Next button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedImage(Math.min(imageData.images.length - 1, selectedImage + 1));
                        }}
                        disabled={selectedImage === imageData.images.length - 1}
                        className={cn(
                          'absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full text-white transition-all z-10',
                          'flex items-center justify-center',
                          selectedImage === imageData.images.length - 1
                            ? 'bg-black/30 opacity-50 cursor-not-allowed'
                            : 'bg-black/60 hover:bg-black/80 opacity-100'
                        )}
                        aria-label="Next image"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </>
                  )}

                  {/* Multiple images indicator */}
                  {imageData.images.length > 1 && (
                    <div className={cn(
                      "absolute top-4 bg-black/70 text-white text-xs px-2 py-1 rounded-full",
                      imageData.pdf_base64 ? "right-28" : "right-16"
                    )}>
                      {selectedImage + 1} / {imageData.images.length}
                    </div>
                  )}
                </div>

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
                          selectedImage === idx ? 'border-linkedin-blue' : 'border-transparent hover:border-gray-300'
                        )}
                        onClick={() => setSelectedImage(idx)}
                      />
                    ))}
                  </div>
                )}
              </div>
            ) : !isManualMode ? (
              <div className="p-4 text-center text-sm text-linkedin-text-secondary">
                <ImageIcon className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>Image will appear here after generation</p>
              </div>
            ) : null}
          </div>
        )}

        {/* LinkedIn-style Engagement Bar */}
        <div className="px-4 py-2 border-t border-linkedin-border">
          <div className="flex items-center justify-between text-xs text-linkedin-text-secondary pb-2 border-b border-linkedin-border">
            <span className="flex items-center gap-1">
              <span className="flex -space-x-1">
                <span className="w-4 h-4 rounded-full bg-blue-500 flex items-center justify-center text-white text-[8px]">👍</span>
                <span className="w-4 h-4 rounded-full bg-red-500 flex items-center justify-center text-white text-[8px]">❤️</span>
              </span>
              <span className="ml-1">41,435</span>
            </span>
            <span>61 comments • 52 reposts</span>
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

        {/* AI Image Recommendation - Hidden in manual mode */}
        {!isManualMode && textData?.image_recommendation && (
          <RecommendationSection
            recommendation={textData.image_recommendation}
            onGenerate={onGenerateWithRecommendation}
            isLoading={isTextLoading || isImageLoading}
            hasImagePrompts={Boolean(textData.image_prompts?.length)}
          />
        )}

        {/* Regenerate Buttons - Hidden in manual mode */}
        {!isManualMode && (
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
              onClick={useAIImages ? onRegenerateImages : () => onGeneratePostCard?.(postcardTheme)}
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
              {useCarousel
                ? 'Regenerate Carousel'
                : useAIImages
                  ? 'Regenerate AI Image'
                  : usePostcard
                    ? 'Regenerate Postcard'
                    : 'Regenerate Card'}
            </button>
          </div>
        )}


        {/* Stats Footer - Hidden in manual mode */}
        {!isManualMode && (textData?.generation_time_ms || imageData?.generation_time_ms) && (
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

          </div>
        )}
      </motion.div>

      {/* Image Lightbox */}
      <AnimatePresence>
        {isGalleryOpen && imageData && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 flex items-center justify-center pt-20 pb-4 px-4"
            onClick={() => {
              if (isZoomed) {
                setIsZoomed(false);
              } else {
                setIsGalleryOpen(false);
              }
            }}
          >
            {/* Close and Download buttons */}
            <div className="absolute top-20 right-4 flex items-center gap-2 z-[60]">
              {/* PDF Download button */}
              {!isZoomed && imageData.pdf_base64 && (
                <button
                  className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDownloadPDF();
                  }}
                  title="Download PDF"
                >
                  <div className="w-6 h-6 text-white flex items-center justify-center font-bold text-sm">PDF</div>
                </button>
              )}
              {/* Image Download button */}
              {!isZoomed && (
                <button
                  className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    const currentImage = imageData.images[selectedImage];
                    handleDownloadImage(currentImage.base64_data, selectedImage);
                  }}
                  title="Download image"
                >
                  <ImageIcon className="w-6 h-6 text-white" />
                </button>
              )}

              {/* Close button */}
              <button
                className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors"
                onClick={(e) => {
                  e.stopPropagation();
                  setIsGalleryOpen(false);
                  setIsZoomed(false);
                  setPanPosition({ x: 0, y: 0 });
                }}
                title="Close gallery"
              >
                <X className="w-6 h-6 text-white" />
              </button>
            </div>

            <motion.img
              ref={imageRef}
              key={selectedImage}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{
                scale: isZoomed ? 1.5 : 1,
                opacity: 1,
                x: isZoomed ? panPosition.x : 0,
                y: isZoomed ? panPosition.y : 0,
                cursor: isZoomed ? (isDragging ? 'grabbing' : 'grab') : 'zoom-in'
              }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ duration: 0.2 }}
              src={`data:image/${imageData.images[selectedImage].format};base64,${imageData.images[selectedImage].base64_data}`}
              alt={`Full size preview ${selectedImage + 1}`}
              className={cn(
                'object-contain rounded-lg select-none',
                isZoomed
                  ? 'max-w-[95vw] max-h-[95vh]'
                  : 'max-w-[85vw] max-h-[75vh]'
              )}
              onClick={(e) => {
                e.stopPropagation();
                // Only toggle zoom if we didn't drag (check if mouse moved more than 5px)
                if (mouseDownPos) {
                  const deltaX = Math.abs(e.clientX - mouseDownPos.x);
                  const deltaY = Math.abs(e.clientY - mouseDownPos.y);
                  // If moved more than 5px, it was a drag, don't toggle zoom
                  if (deltaX > 5 || deltaY > 5) {
                    setMouseDownPos(null);
                    return;
                  }
                }
                setMouseDownPos(null);
                setIsZoomed(!isZoomed);
                if (!isZoomed) {
                  setPanPosition({ x: 0, y: 0 });
                }
              }}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseLeave}
              title={isZoomed ? 'Drag to pan, click to zoom out' : 'Click to zoom in'}
            />

            {/* Navigation for multiple images */}
            {imageData.images.length > 1 && !isZoomed && (
              <>
                {/* Previous button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedImage(Math.max(0, selectedImage - 1));
                  }}
                  disabled={selectedImage === 0}
                  className={cn(
                    'absolute left-4 top-1/2 -translate-y-1/2 p-3 rounded-full text-white transition-all z-50',
                    'flex items-center justify-center',
                    selectedImage === 0
                      ? 'bg-white/10 opacity-50 cursor-not-allowed'
                      : 'bg-white/20 hover:bg-white/30 opacity-100'
                  )}
                  aria-label="Previous image"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>

                {/* Next button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedImage(Math.min(imageData.images.length - 1, selectedImage + 1));
                  }}
                  disabled={selectedImage === imageData.images.length - 1}
                  className={cn(
                    'absolute right-4 top-1/2 -translate-y-1/2 p-3 rounded-full text-white transition-all z-50',
                    'flex items-center justify-center',
                    selectedImage === imageData.images.length - 1
                      ? 'bg-white/10 opacity-50 cursor-not-allowed'
                      : 'bg-white/20 hover:bg-white/30 opacity-100'
                  )}
                  aria-label="Next image"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>

                {/* Image counter */}
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/70 text-white text-sm px-4 py-2 rounded-full z-50">
                  {selectedImage + 1} / {imageData.images.length}
                </div>
              </>
            )}

            {/* Zoom indicator */}
            {isZoomed && (
              <div className="absolute top-20 left-1/2 -translate-x-1/2 bg-black/70 text-white text-sm px-4 py-2 rounded-full z-50">
                Drag to pan • Click to zoom out • ESC to close
              </div>
            )}

          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}


