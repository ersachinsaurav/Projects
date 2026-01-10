/**
 * Postcard Creator Component
 * ===========================
 * Independent post card generation from pasted text.
 * Self-contained with its own text input and preview.
 */

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Image as ImageIcon,
  Moon,
  Sun,
  Copy,
  Check,
  Download,
  FileText,
} from 'lucide-react';
import { cn, copyToClipboard, downloadImage, sanitizeFilename } from '../lib/utils';

interface PostcardCreatorProps {
  onGeneratePostcard: (text: string, theme: 'dark' | 'light') => Promise<void>;
  generatedImage: string | null;
  isGenerating: boolean;
}

export function PostcardCreator({
  onGeneratePostcard,
  generatedImage,
  isGenerating,
}: PostcardCreatorProps) {
  const [postText, setPostText] = useState('');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [copied, setCopied] = useState(false);

  const hasContent = postText.trim().length > 0;

  const handleGenerate = useCallback(async () => {
    if (!hasContent) return;
    await onGeneratePostcard(postText, theme);
  }, [postText, theme, hasContent, onGeneratePostcard]);

  const handleCopy = useCallback(async () => {
    if (postText) {
      await copyToClipboard(postText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [postText]);

  const handleDownload = useCallback(() => {
    if (generatedImage) {
      // Use shared utility for consistent filename generation
      const firstLine = postText.split('\n').find(line => line.trim()) || '';
      const filename = `${sanitizeFilename(firstLine, 'postcard')}.png`;
      downloadImage(generatedImage, filename);
    }
  }, [generatedImage, postText]);

  return (
    <div className="space-y-4">
      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Left: Text Input */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="linkedin-card p-5 space-y-4"
        >
          {/* Header */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-violet-500 to-purple-600 rounded-lg">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-linkedin-text dark:text-dark-text">
                Post Text
              </h3>
              <p className="text-xs text-linkedin-text-secondary dark:text-dark-text/60">
                Paste or type your LinkedIn post
              </p>
            </div>
          </div>

          {/* Text Area */}
          <textarea
            value={postText}
            onChange={(e) => setPostText(e.target.value)}
            placeholder={`Paste your LinkedIn post here...

Example:
I learned something important today about leadership.

Great leaders don't just give orders. They create an environment where people feel safe to fail.

What makes a great leader in your experience?`}
            rows={14}
            className="textarea-field text-sm resize-none"
          />

          {/* Character count + Copy */}
          <div className="flex items-center justify-between">
            <span className="text-xs text-linkedin-text-secondary dark:text-dark-text/60">
              {postText.length} characters
            </span>
            <button
              onClick={handleCopy}
              disabled={!hasContent}
              className="flex items-center gap-1.5 text-xs text-linkedin-blue hover:text-linkedin-blue-dark disabled:opacity-50"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>

          {/* Theme Selection */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-linkedin-text dark:text-dark-text">
              Theme
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => setTheme('dark')}
                className={cn(
                  'flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg border-2 transition-all',
                  theme === 'dark'
                    ? 'border-violet-500 bg-gray-900 text-white shadow-lg shadow-violet-500/20'
                    : 'border-gray-200 dark:border-dark-border bg-gray-900 text-white hover:border-gray-300'
                )}
              >
                <Moon className={cn('w-4 h-4', theme === 'dark' && 'text-violet-300')} />
                <span className="text-sm font-medium">Dark</span>
              </button>
              <button
                onClick={() => setTheme('light')}
                className={cn(
                  'flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg border-2 transition-all',
                  theme === 'light'
                    ? 'border-amber-400 bg-white text-gray-800 shadow-lg shadow-amber-400/30'
                    : 'border-gray-200 dark:border-dark-border bg-white text-gray-800 hover:border-gray-300'
                )}
              >
                <Sun className={cn('w-4 h-4', theme === 'light' && 'text-amber-500')} />
                <span className="text-sm font-medium">Light</span>
              </button>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={!hasContent || isGenerating}
            className={cn(
              'w-full py-3 rounded-full font-semibold transition-all flex items-center justify-center gap-2',
              hasContent && !isGenerating
                ? 'bg-gradient-to-r from-violet-500 to-purple-600 text-white hover:shadow-lg hover:scale-[1.02]'
                : 'bg-gray-200 dark:bg-dark-border text-gray-400 cursor-not-allowed'
            )}
          >
            {isGenerating ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <ImageIcon className="w-5 h-5" />
                Generate Postcard
              </>
            )}
          </button>
        </motion.div>

        {/* Right: Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="linkedin-card p-5 space-y-4"
        >
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-linkedin-blue to-accent-primary rounded-lg">
                <ImageIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-linkedin-text dark:text-dark-text">
                  Preview
                </h3>
                <p className="text-xs text-linkedin-text-secondary dark:text-dark-text/60">
                  Your generated postcard
                </p>
              </div>
            </div>
            {generatedImage && (
              <button
                onClick={handleDownload}
                className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-linkedin-blue border border-linkedin-blue rounded-full hover:bg-linkedin-blue hover:text-white transition-colors"
              >
                <Download className="w-4 h-4" />
                Download
              </button>
            )}
          </div>

          {/* Image Preview */}
          <div className="bg-gray-100 dark:bg-dark-border rounded-lg overflow-hidden min-h-[300px] flex items-center justify-center">
            {isGenerating ? (
              <div className="flex flex-col items-center gap-3 text-linkedin-text-secondary dark:text-dark-text/60">
                <div className="w-10 h-10 border-3 border-violet-200 border-t-violet-500 rounded-full animate-spin" />
                <span className="text-sm">Generating postcard...</span>
              </div>
            ) : generatedImage ? (
              <img
                src={`data:image/png;base64,${generatedImage}`}
                alt="Generated postcard"
                className="w-full h-auto"
              />
            ) : (
              <div className="flex flex-col items-center gap-3 text-linkedin-text-secondary dark:text-dark-text/60 p-8 text-center">
                <ImageIcon className="w-12 h-12 opacity-30" />
                <div>
                  <p className="font-medium">No postcard yet</p>
                  <p className="text-xs mt-1">
                    Paste your post text and click "Generate Postcard"
                  </p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

