/**
 * Utility functions
 */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind CSS classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Generate a UUID v4
 */
export function generateId(): string {
  return crypto.randomUUID?.() ||
    'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
}

/**
 * Format number with commas
 */
export function formatNumber(num: number): string {
  return num.toLocaleString();
}

/**
 * Format milliseconds to human-readable duration
 */
export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  const seconds = Math.round(ms / 1000);
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
}

/**
 * Count LinkedIn visible characters
 */
export function countLinkedInChars(text: string): {
  total: number;
  visible: number;
  showMore: boolean;
} {
  const total = text.length;
  const visible = 140; // LinkedIn's "see more" threshold

  return {
    total,
    visible: Math.min(total, visible),
    showMore: total > visible,
  };
}

/**
 * Format LinkedIn post preview
 */
export function formatLinkedInPreview(text: string): string {
  // Replace multiple newlines with double line breaks
  return text
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * Download a file from base64 data
 */
export function downloadBase64File(
  base64Data: string,
  filename: string,
  mimeType: string
): void {
  const byteCharacters = atob(base64Data);
  const byteNumbers = new Array(byteCharacters.length);

  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }

  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], { type: mimeType });

  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Download image from base64
 */
export function downloadImage(base64Data: string, filename: string): void {
  downloadBase64File(base64Data, filename, 'image/png');
}

/**
 * Download PDF from base64
 */
export function downloadPDF(base64Data: string, filename: string): void {
  downloadBase64File(base64Data, filename, 'application/pdf');
}

/**
 * Sanitize text for use as filename (SEO-friendly kebab-case)
 * Removes special characters, replaces spaces with hyphens, lowercases
 */
export function sanitizeFilename(text: string, fallback: string = 'untitled'): string {
  if (!text || !text.trim()) return fallback;

  const sanitized = text
    .trim()
    .replace(/[^\w\s]/g, '') // Remove all special chars, keep only alphanumeric and spaces
    .replace(/\s+/g, '-') // Replace spaces with hyphens (SEO best practice)
    .toLowerCase(); // Lowercase for consistency

  return sanitized || fallback;
}

/**
 * Get filename from text content with priority order
 * Priority: title > firstLine of text > concept > defaultName
 */
export function getFilenameFromContent(
  options: {
    title?: string;
    postText?: string;
    concept?: string;
    defaultName?: string;
    extension?: string;
  }
): string {
  const { title, postText, concept, defaultName = 'download', extension = 'png' } = options;

  let textToUse = '';

  // Priority 1: Use title if available
  if (title?.trim()) {
    textToUse = title;
  }
  // Priority 2: Use first line of postText
  else if (postText?.trim()) {
    const firstLine = postText.split('\n').find(line => line.trim()) || '';
    if (firstLine.trim()) {
      textToUse = firstLine;
    }
  }
  // Priority 3: Use concept
  if (!textToUse && concept?.trim()) {
    textToUse = concept;
  }

  if (textToUse) {
    return `${sanitizeFilename(textToUse, defaultName)}.${extension}`;
  }

  return `${defaultName}.${extension}`;
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand('copy');
      return true;
    } catch {
      return false;
    } finally {
      document.body.removeChild(textArea);
    }
  }
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

