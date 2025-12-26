/**
 * Text Preview Component
 * =======================
 * LinkedIn-style post preview with editing capabilities
 *
 * Keyboard Shortcuts:
 * - Cmd/Ctrl + Z: Undo
 * - Cmd/Ctrl + Shift + Z (or Ctrl+Y): Redo
 * - Cmd/Ctrl + B: Bold (Unicode)
 * - Cmd/Ctrl + I: Italic (Unicode)
 * - Cmd/Ctrl + U: Underline (Unicode)
 * - Cmd/Ctrl + Shift + S: Strikethrough (Unicode)
 * - Cmd/Ctrl + Shift + R: Reset formatting
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Copy,
  Check,
  Edit2,
  Save,
  RotateCcw,
  Linkedin,
  Eye,
  EyeOff,
  Clock,
  Zap,
  Bold,
  Italic,
  Underline,
  Strikethrough,
  X,
  Code,
  ChevronDown,
  ChevronUp,
  Undo2,
  Redo2,
} from 'lucide-react';
import type { TextGenerationResponse } from '../types';
import { cn, copyToClipboard, formatNumber, formatDuration } from '../lib/utils';

interface TextPreviewProps {
  data: TextGenerationResponse | null;
  isLoading: boolean;
  onTextChange?: (text: string) => void;
}

// Unicode conversion functions
function toUnicodeBold(text: string): string {
  const boldUpperStart = 0x1D5D4;  // 𝗔
  const boldLowerStart = 0x1D5EE;  // 𝗮
  const boldDigitStart = 0x1D7EC;  // 𝟬

  return Array.from(text).map(char => {
    if (char >= 'A' && char <= 'Z') {
      return String.fromCodePoint(boldUpperStart + (char.charCodeAt(0) - 'A'.charCodeAt(0)));
    } else if (char >= 'a' && char <= 'z') {
      return String.fromCodePoint(boldLowerStart + (char.charCodeAt(0) - 'a'.charCodeAt(0)));
    } else if (char >= '0' && char <= '9') {
      return String.fromCodePoint(boldDigitStart + (char.charCodeAt(0) - '0'.charCodeAt(0)));
    }
    return char;
  }).join('');
}

function toUnicodeItalic(text: string): string {
  const italicUpperStart = 0x1D608;  // 𝘈
  const italicLowerStart = 0x1D622;  // 𝘢

  return Array.from(text).map(char => {
    if (char >= 'A' && char <= 'Z') {
      return String.fromCodePoint(italicUpperStart + (char.charCodeAt(0) - 'A'.charCodeAt(0)));
    } else if (char >= 'a' && char <= 'z') {
      return String.fromCodePoint(italicLowerStart + (char.charCodeAt(0) - 'a'.charCodeAt(0)));
    }
    return char;
  }).join('');
}

function toUnicodeUnderline(text: string): string {
  // Use combining underline character U+0332
  return Array.from(text).map(char => char + '\u0332').join('');
}

function toUnicodeStrikethrough(text: string): string {
  // Use combining strikethrough character U+0336
  return Array.from(text).map(char => char + '\u0336').join('');
}

function removeUnicodeFormatting(text: string): string {
  // Remove combining characters
  let result = text.replace(/[\u0332\u0336]/g, '');

  // Convert Unicode bold back to regular
  const boldUpperStart = 0x1D5D4;
  const boldLowerStart = 0x1D5EE;
  const boldDigitStart = 0x1D7EC;
  const italicUpperStart = 0x1D608;
  const italicLowerStart = 0x1D622;

  result = Array.from(result).map(char => {
    const code = char.codePointAt(0) || 0;

    // Bold uppercase
    if (code >= boldUpperStart && code < boldUpperStart + 26) {
      return String.fromCharCode('A'.charCodeAt(0) + (code - boldUpperStart));
    }
    // Bold lowercase
    if (code >= boldLowerStart && code < boldLowerStart + 26) {
      return String.fromCharCode('a'.charCodeAt(0) + (code - boldLowerStart));
    }
    // Bold digits
    if (code >= boldDigitStart && code < boldDigitStart + 10) {
      return String.fromCharCode('0'.charCodeAt(0) + (code - boldDigitStart));
    }
    // Italic uppercase
    if (code >= italicUpperStart && code < italicUpperStart + 26) {
      return String.fromCharCode('A'.charCodeAt(0) + (code - italicUpperStart));
    }
    // Italic lowercase
    if (code >= italicLowerStart && code < italicLowerStart + 26) {
      return String.fromCharCode('a'.charCodeAt(0) + (code - italicLowerStart));
    }

    return char;
  }).join('');

  return result;
}

// Max history size for undo/redo
const MAX_HISTORY_SIZE = 50;

export function TextPreview({ data, isLoading, onTextChange }: TextPreviewProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState('');
  const [editedHashtags, setEditedHashtags] = useState<string[]>([]);
  const [copied, setCopied] = useState(false);
  const [showFullPost, setShowFullPost] = useState(true);
  const [showPrompts, setShowPrompts] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Undo/Redo history
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const isUndoRedoRef = useRef(false);

  useEffect(() => {
    if (data?.post_text) {
      setEditedText(data.post_text);
      // Reset history when new text is generated
      setHistory([data.post_text]);
      setHistoryIndex(0);
    }
  }, [data?.post_text]);

  useEffect(() => {
    if (data?.hashtags) {
      setEditedHashtags([...data.hashtags]);
    }
  }, [data?.hashtags]);

  // Track text changes for undo/redo (debounced)
  useEffect(() => {
    if (isUndoRedoRef.current) {
      isUndoRedoRef.current = false;
      return;
    }

    // Don't add to history if it's the same as current
    if (history[historyIndex] === editedText) return;

    // Add to history
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(editedText);

    // Limit history size
    if (newHistory.length > MAX_HISTORY_SIZE) {
      newHistory.shift();
    }

    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  }, [editedText]);

  // Undo function
  const handleUndo = useCallback(() => {
    if (historyIndex > 0) {
      isUndoRedoRef.current = true;
      setHistoryIndex(historyIndex - 1);
      setEditedText(history[historyIndex - 1]);
    }
  }, [history, historyIndex]);

  // Redo function
  const handleRedo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      isUndoRedoRef.current = true;
      setHistoryIndex(historyIndex + 1);
      setEditedText(history[historyIndex + 1]);
    }
  }, [history, historyIndex]);

  const canUndo = historyIndex > 0;
  const canRedo = historyIndex < history.length - 1;

  const handleCopy = async () => {
    const textToCopy = editedText || data?.post_text || '';
    // Append hashtags when copying
    const hashtags = editedHashtags.join(' ') || '';
    const fullText = hashtags ? `${textToCopy}\n\n${hashtags}` : textToCopy;

    const success = await copyToClipboard(fullText);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleSave = () => {
    setIsEditing(false);
    onTextChange?.(editedText);
  };

  const handleReset = () => {
    // Reset text to original
    setEditedText(data?.post_text || '');
    // Reset hashtags to original
    setEditedHashtags(data?.hashtags ? [...data.hashtags] : []);
    // Reset history
    if (data?.post_text) {
      setHistory([data.post_text]);
      setHistoryIndex(0);
    }
    setIsEditing(false);
  };

  // Handle hashtag edit
  const handleHashtagChange = (index: number, value: string) => {
    const newHashtags = [...editedHashtags];
    newHashtags[index] = value;
    setEditedHashtags(newHashtags);
  };

  const handleHashtagRemove = (index: number) => {
    setEditedHashtags(editedHashtags.filter((_, i) => i !== index));
  };

  const handleHashtagAdd = () => {
    if (editedHashtags.length < 5) {
      setEditedHashtags([...editedHashtags, '#NewTag']);
    }
  };

  // Apply Unicode formatting to selected text
  const applyFormatting = useCallback((formatter: (text: string) => string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = editedText.slice(start, end);

    if (selectedText.length === 0) return;

    const formattedText = formatter(selectedText);
    const newText = editedText.slice(0, start) + formattedText + editedText.slice(end);

    setEditedText(newText);

    // Restore cursor position
    requestAnimationFrame(() => {
      textarea.focus();
      textarea.setSelectionRange(start, start + formattedText.length);
    });
  }, [editedText]);

  // Reset formatting for selected text
  const resetFormatting = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    if (start === end) {
      // No selection - reset entire text
      const plainText = removeUnicodeFormatting(editedText);
      setEditedText(plainText);
    } else {
      // Reset selected text
      const selectedText = editedText.slice(start, end);
      const plainText = removeUnicodeFormatting(selectedText);
      const newText = editedText.slice(0, start) + plainText + editedText.slice(end);
      setEditedText(newText);

      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(start, start + plainText.length);
      });
    }
  }, [editedText]);

  // Keyboard shortcut handler
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
          // Ctrl+Y for redo (Windows style)
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
            // Cmd+Shift+S = Strikethrough
            e.preventDefault();
            applyFormatting(toUnicodeStrikethrough);
          }
          // Cmd+S alone = allow default save behavior
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

  const charCount = (editedText || data?.post_text || '').length;
  const isOverLimit = charCount > 3000;

  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="linkedin-card p-6 space-y-4"
      >
        <div className="flex items-center gap-3">
          <div className="skeleton w-10 h-10 rounded-full" />
          <div className="space-y-2 flex-1">
            <div className="skeleton h-4 w-32" />
            <div className="skeleton h-3 w-48" />
          </div>
        </div>
        <div className="space-y-2">
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-5/6" />
          <div className="skeleton h-4 w-4/6" />
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-3/6" />
        </div>
        <div className="flex items-center justify-center py-4">
          <div className="flex items-center gap-2 text-linkedin-blue">
            <div className="w-5 h-5 border-2 border-linkedin-blue/30 border-t-linkedin-blue rounded-full animate-spin" />
            <span className="text-sm">Generating your post...</span>
          </div>
        </div>
      </motion.div>
    );
  }

  if (!data) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="linkedin-card p-6"
      >
        <div className="text-center py-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
            <Linkedin className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-linkedin-text mb-2">No post yet</h3>
          <p className="text-sm text-linkedin-text-secondary">
            Enter your idea and click "Generate Post" to create your LinkedIn content.
          </p>
        </div>
      </motion.div>
    );
  }

  const displayText = editedText || data.post_text;
  const previewText = showFullPost ? displayText : displayText.slice(0, 140) + (displayText.length > 140 ? '...' : '');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="linkedin-card overflow-hidden"
    >
      {/* Header */}
      <div className="p-4 border-b border-linkedin-border flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-linkedin-blue to-accent-primary flex items-center justify-center">
            <span className="text-white font-semibold text-sm">Y</span>
          </div>
          <div>
            <div className="font-semibold text-linkedin-text">Your Name</div>
            <div className="text-xs text-linkedin-text-secondary">Just now • 🌐</div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFullPost(!showFullPost)}
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            title={showFullPost ? 'Preview mode' : 'Full view'}
          >
            {showFullPost ? (
              <EyeOff className="w-4 h-4 text-linkedin-text-secondary" />
            ) : (
              <Eye className="w-4 h-4 text-linkedin-text-secondary" />
            )}
          </button>

          <button
            onClick={handleCopy}
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            title="Copy to clipboard (with hashtags)"
          >
            {copied ? (
              <Check className="w-4 h-4 text-green-500" />
            ) : (
              <Copy className="w-4 h-4 text-linkedin-text-secondary" />
            )}
          </button>

          {isEditing ? (
            <>
              <button
                onClick={handleSave}
                className="p-2 rounded-full hover:bg-green-50 transition-colors"
                title="Save changes"
              >
                <Save className="w-4 h-4 text-green-500" />
              </button>
              <button
                onClick={handleReset}
                className="p-2 rounded-full hover:bg-gray-100 transition-colors"
                title="Reset to original"
              >
                <RotateCcw className="w-4 h-4 text-linkedin-text-secondary" />
              </button>
            </>
          ) : (
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors"
              title="Edit post"
            >
              <Edit2 className="w-4 h-4 text-linkedin-text-secondary" />
            </button>
          )}
        </div>
      </div>

      {/* Formatting Toolbar (when editing) */}
      {isEditing && (
        <div className="px-4 py-2 border-b border-linkedin-border bg-gray-50 flex items-center gap-2 flex-wrap">
          {/* Undo/Redo */}
          <button
            onClick={handleUndo}
            disabled={!canUndo}
            className={cn(
              'p-1.5 rounded transition-colors',
              canUndo ? 'hover:bg-gray-200 text-linkedin-text' : 'text-gray-300 cursor-not-allowed'
            )}
            title="Undo (Cmd/Ctrl + Z)"
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
            title="Redo (Cmd/Ctrl + Shift + Z)"
          >
            <Redo2 className="w-4 h-4" />
          </button>

          <div className="w-px h-5 bg-gray-300 mx-1" />

          <span className="text-xs text-linkedin-text-secondary mr-1">Format:</span>
          <button
            onClick={() => applyFormatting(toUnicodeBold)}
            className="p-1.5 rounded hover:bg-gray-200 transition-colors"
            title="Bold (Cmd/Ctrl + B)"
          >
            <Bold className="w-4 h-4 text-linkedin-text" />
          </button>
          <button
            onClick={() => applyFormatting(toUnicodeItalic)}
            className="p-1.5 rounded hover:bg-gray-200 transition-colors"
            title="Italic (Cmd/Ctrl + I)"
          >
            <Italic className="w-4 h-4 text-linkedin-text" />
          </button>
          <button
            onClick={() => applyFormatting(toUnicodeUnderline)}
            className="p-1.5 rounded hover:bg-gray-200 transition-colors"
            title="Underline (Cmd/Ctrl + U)"
          >
            <Underline className="w-4 h-4 text-linkedin-text" />
          </button>
          <button
            onClick={() => applyFormatting(toUnicodeStrikethrough)}
            className="p-1.5 rounded hover:bg-gray-200 transition-colors"
            title="Strikethrough (Cmd/Ctrl + Shift + S)"
          >
            <Strikethrough className="w-4 h-4 text-linkedin-text" />
          </button>

          <span className="text-xs text-linkedin-text-secondary ml-auto hidden sm:block">
            Select text + shortcut
          </span>
        </div>
      )}

      {/* Post Content */}
      <div className="p-4">
        {isEditing ? (
          <textarea
            ref={textareaRef}
            value={editedText}
            onChange={(e) => setEditedText(e.target.value)}
            onKeyDown={handleKeyDown}
            className={cn(
              'w-full min-h-[350px] p-0 border-none focus:outline-none focus:ring-0 resize-y',
              'font-sans text-sm leading-relaxed text-linkedin-text',
              isOverLimit && 'text-red-500'
            )}
            autoFocus
          />
        ) : (
          <div className="linkedin-post-preview text-linkedin-text whitespace-pre-wrap">
            {previewText}
          </div>
        )}

        {!showFullPost && displayText.length > 140 && !isEditing && (
          <button
            onClick={() => setShowFullPost(true)}
            className="text-linkedin-text-secondary text-sm mt-2 hover:text-linkedin-blue"
          >
            ...see more
          </button>
        )}
      </div>

      {/* Hashtags Display - Editable */}
      {editedHashtags.length > 0 && (
        <div className="px-4 pb-3">
          {isEditing ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2 flex-wrap">
                {editedHashtags.map((tag, idx) => (
                  <div key={idx} className="flex items-center gap-1 bg-blue-50 rounded-full px-2 py-1">
                    <input
                      type="text"
                      value={tag}
                      onChange={(e) => handleHashtagChange(idx, e.target.value)}
                      className="bg-transparent text-sm text-linkedin-blue w-24 focus:outline-none focus:w-32 transition-all"
                    />
                    <button
                      onClick={() => handleHashtagRemove(idx)}
                      className="text-red-400 hover:text-red-600"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                ))}
                {editedHashtags.length < 5 && (
                  <button
                    onClick={handleHashtagAdd}
                    className="text-xs text-linkedin-blue hover:underline"
                  >
                    + Add
                  </button>
                )}
              </div>
              <p className="text-xs text-linkedin-text-secondary">
                {editedHashtags.length}/5 hashtags (editable)
              </p>
            </div>
          ) : (
            <div className="flex items-center gap-2 flex-wrap">
              {editedHashtags.map((tag, idx) => (
                <span
                  key={idx}
                  className="text-sm text-linkedin-blue hover:underline cursor-pointer"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Footer Stats */}
      <div className="px-4 pb-4">
        <div className="flex items-center justify-between text-xs text-linkedin-text-secondary border-t border-linkedin-border pt-3">
          <div className="flex items-center gap-4">
            <span className={cn('flex items-center gap-1', isOverLimit && 'text-red-500')}>
              {formatNumber(charCount)} / 3,000 chars
            </span>
            {data.tokens_used && (
              <span className="flex items-center gap-1">
                <Zap className="w-3 h-3" />
                {formatNumber(data.tokens_used)} tokens
              </span>
            )}
            {data.generation_time_ms && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {formatDuration(data.generation_time_ms)}
              </span>
            )}
          </div>
          <span className="text-xs bg-gray-100 px-2 py-0.5 rounded">
            {data.model_used}
          </span>
        </div>
      </div>

      {/* Image Strategy Hint */}
      {data.image_strategy && data.image_strategy.image_count > 0 && (
        <div className="px-4 pb-4">
          <div className="bg-blue-50 rounded-lg p-3 text-sm">
            <div className="font-medium text-linkedin-blue mb-1">
              📸 {data.image_strategy.image_count} image{data.image_strategy.image_count > 1 ? 's' : ''} recommended
            </div>
            <div className="text-xs text-linkedin-text-secondary">
              {data.image_strategy.reason}
            </div>
            {data.image_prompts && data.image_prompts.length > 0 && (
              <div className="text-xs text-green-600 mt-1">
                ✓ {data.image_prompts.length} image prompt{data.image_prompts.length > 1 ? 's' : ''} ready
              </div>
            )}
          </div>
        </div>
      )}

      {/* Prompt Viewer (Collapsible) */}
      {data.image_prompts && data.image_prompts.length > 0 && (
        <div className="px-4 pb-4">
          <button
            onClick={() => setShowPrompts(!showPrompts)}
            className="flex items-center gap-2 text-sm text-linkedin-text-secondary hover:text-linkedin-blue transition-colors w-full"
          >
            <Code className="w-4 h-4" />
            <span>View Image Prompts</span>
            {showPrompts ? (
              <ChevronUp className="w-4 h-4 ml-auto" />
            ) : (
              <ChevronDown className="w-4 h-4 ml-auto" />
            )}
          </button>

          {showPrompts && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-3 space-y-3"
            >
              {data.image_prompts.map((prompt, idx) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-3 text-xs">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-linkedin-text">
                      Image {prompt.id}
                    </span>
                    {prompt.concept && (
                      <span className="text-linkedin-blue bg-blue-100 px-2 py-0.5 rounded">
                        {prompt.concept}
                      </span>
                    )}
                  </div>
                  <div className="text-linkedin-text-secondary mb-2">
                    <strong>Prompt:</strong>
                    <p className="mt-1 whitespace-pre-wrap">{prompt.prompt}</p>
                  </div>
                  {prompt.style_notes && (
                    <div className="text-linkedin-text-secondary">
                      <strong>Style:</strong> {prompt.style_notes}
                    </div>
                  )}
                  {prompt.composition_note && (
                    <div className="text-linkedin-text-secondary mt-1">
                      <strong>Composition:</strong> {prompt.composition_note}
                    </div>
                  )}
                </div>
              ))}

              {data.image_fingerprint && (
                <div className="bg-purple-50 rounded-lg p-3 text-xs">
                  <div className="font-semibold text-purple-700 mb-2">Image Fingerprint</div>
                  <div className="grid grid-cols-2 gap-2 text-linkedin-text-secondary">
                    <div><strong>Style:</strong> {data.image_fingerprint.visual_style}</div>
                    <div><strong>Colors:</strong> {data.image_fingerprint.color_palette}</div>
                    <div><strong>Composition:</strong> {data.image_fingerprint.composition}</div>
                    <div><strong>Lighting:</strong> {data.image_fingerprint.lighting}</div>
                    <div><strong>Concept:</strong> {data.image_fingerprint.concept_type}</div>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </div>
      )}
    </motion.div>
  );
}
