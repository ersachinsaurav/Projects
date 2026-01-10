/**
 * Application Constants
 * ======================
 * Centralized constants to avoid hardcoding values throughout the app.
 */

// =============================================================================
// PROFILE CONFIGURATION
// =============================================================================

export const PROFILE_CONFIG = {
  name: 'Sachin Saurav',
  handle: '@ersachinsaurav',
  title: 'Tech Lead @ Entrata India | Full Stack Software Engineer',
  verified: true,
  linkedin_url: 'linkedin.com/in/ersachinsaurav',
  instagram_url: 'instagram.com/ersachinsaurav',
  website: 'sachinsaurav.dev',
} as const;

// =============================================================================
// LINKEDIN LIMITS
// =============================================================================

export const LINKEDIN_LIMITS = {
  maxPostChars: 3000,
  visibleCharsBeforeMore: 140,
  maxHashtags: 5,
  minHashtags: 3,
} as const;

// =============================================================================
// UNDO/REDO
// =============================================================================

export const EDITOR_CONFIG = {
  maxHistorySize: 50,
} as const;

// =============================================================================
// IMAGE TYPE CONFIGURATION
// =============================================================================

export const IMAGE_TYPE_CONFIG: Record<string, {
  label: string;
  color: string;
  description: string;
  isInstant?: boolean;
}> = {
  text_only: {
    label: 'Text Only',
    color: 'bg-slate-600',
    description: 'No image - whitespace reinforces message (best for quiet/reflective posts)',
    isInstant: true,
  },
  post_card: {
    label: 'Post Card',
    color: 'bg-gray-600',
    description: 'Text-based card with profile pic and short insight (instant, no AI)',
    isInstant: true,
  },
  cartoon_narrative: {
    label: 'Cartoon Narrative',
    color: 'bg-purple-600',
    description: 'Illustrated scene with characters (AI-generated, avoid for serious topics)',
  },
  cartoon_abstract: {
    label: 'Cartoon Abstract',
    color: 'bg-blue-600',
    description: 'Stylized illustration without specific narrative (AI-generated)',
  },
  abstract_minimal: {
    label: 'Abstract Minimal',
    color: 'bg-teal-600',
    description: 'Geometric shapes and colors, minimalist feel (AI-generated)',
  },
  infographic: {
    label: 'Infographic',
    color: 'bg-orange-600',
    description: 'Data or process visualization (AI-generated, carousels flatten pacing)',
  },
} as const;

