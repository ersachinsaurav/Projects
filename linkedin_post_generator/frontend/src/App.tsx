/**
 * LinkedIn Post Generator - Main App Component
 * =============================================
 * Single-page application for generating LinkedIn posts and images
 *
 * Features:
 * - Auto-generates images after text generation
 * - LinkedIn-style preview on the right
 * - Inline hashtag editing
 * - Separate regenerate buttons
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Linkedin,
  Github,
  Moon,
  Sun,
  RefreshCw,
  AlertCircle,
} from 'lucide-react';
import { InputForm } from './components/InputForm';
import { LinkedInPreview } from './components/LinkedInPreview';
import { TabLayout, ParentTab, ChildTab } from './components/TabLayout';
import { PostcardCreator } from './components/PostcardCreator';
import { useGenerateText } from './hooks/useGenerateText';
import { useGenerateImages } from './hooks/useGenerateImages';
import { useGeneratePostCard } from './hooks/useGeneratePostCard';
import { generateId } from './lib/utils';
import type {
  PostLength,
  Tone,
  CTAStyle,
  TextModelConfig,
  ImageModelConfig,
  TextGenerationResponse,
  ImageGenerationResponse,
} from './types';
import {
  DEFAULT_POST_LENGTH,
  DEFAULT_TONE,
  DEFAULT_CTA_STYLE,
  DEFAULT_AUDIENCES,
  DEFAULT_GENERATE_POSTCARD,
  DEFAULT_POSTCARD_THEME,
  DEFAULT_GENERATE_IMAGE,
  DEFAULT_GENERATE_CAROUSEL,
  DEFAULT_IMAGE_MODEL,
  DEFAULT_TEXT_MODEL,
} from './lib/defaults';
import { PROFILE_CONFIG } from './lib/constants';
// =============================================================================
// PROFILE PICTURE CUSTOMIZATION
// =============================================================================
//
// To use your own profile picture:
// 1. Add your photo as 'profilePicture.jpeg' (or .jpg/.png) in src/images/
// 2. Uncomment the import below and comment out the placeholder import
// 3. Recommended size: 200x200 pixels or larger (square)
//
// import profilePicture from './images/profilePicture.jpeg';
//
// Using placeholder by default:
import profilePicture from './images/placeholder-avatar.svg';

function App() {
  // Session management
  // Removed: tenantId (no multi-tenancy)
  const [sessionId, setSessionId] = useState(() => generateId());

  // Tab navigation
  const [parentTab, setParentTab] = useState<ParentTab>('ai');
  const [childTab, setChildTab] = useState<ChildTab>('generate');

  // Manual Postcard tab - independent state
  const [postcardImage, setPostcardImage] = useState<string | null>(null);

  // Form state
  const [idea, setIdea] = useState('');
  const [postAngle, setPostAngle] = useState('');
  const [draftPost, setDraftPost] = useState('');
  const [postLength, setPostLength] = useState<PostLength>(DEFAULT_POST_LENGTH);
  const [tone, setTone] = useState<Tone>(DEFAULT_TONE);
  const [audience, setAudience] = useState<string[]>([...DEFAULT_AUDIENCES]);
  const [ctaStyle, setCtaStyle] = useState<CTAStyle>(DEFAULT_CTA_STYLE);

  // Model selection
  const [textModel, setTextModel] = useState<TextModelConfig>(DEFAULT_TEXT_MODEL);
  const [imageModel, setImageModel] = useState<ImageModelConfig>(DEFAULT_IMAGE_MODEL);

  // Postcard generation toggle (default ON)
  const [generatePostcard, setGeneratePostcard] = useState(DEFAULT_GENERATE_POSTCARD);
  const [postcardTheme, setPostcardTheme] = useState<'dark' | 'light'>(DEFAULT_POSTCARD_THEME);

  // Image generation toggle (default OFF)
  const [generateImage, setGenerateImage] = useState(DEFAULT_GENERATE_IMAGE);

  // Carousel generation toggle (default OFF)
  const [generateCarousel, setGenerateCarousel] = useState(DEFAULT_GENERATE_CAROUSEL);

  // Generated content
  const [textData, setTextData] = useState<TextGenerationResponse | null>(null);
  const [imageData, setImageData] = useState<ImageGenerationResponse | null>(null);

  // Theme
  const [isDark, setIsDark] = useState(false);

  // Error state
  const [error, setError] = useState<string | null>(null);

  // Auto-generate images flag
  const [shouldAutoGenerateImages, setShouldAutoGenerateImages] = useState(false);

  // Mutations
  const textMutation = useGenerateText();
  const imageMutation = useGenerateImages();
  const postCardMutation = useGeneratePostCard();

  // Profile picture as base64 for post cards
  const [profilePicBase64, setProfilePicBase64] = useState<string | null>(null);

  // Load profile picture as base64 on mount
  useEffect(() => {
    const loadProfilePicture = async () => {
      try {
        const response = await fetch(profilePicture);
        const blob = await response.blob();
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64 = (reader.result as string).split(',')[1]; // Remove data:image/jpeg;base64, prefix
          setProfilePicBase64(base64);
        };
        reader.readAsDataURL(blob);
      } catch (err) {
        console.error('Failed to load profile picture:', err);
      }
    };
    loadProfilePicture();
  }, []);

  // Apply theme
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  // Mutual exclusivity: Only one mode can be active at a time
  useEffect(() => {
    if (generatePostcard) {
      // Postcard ON: Turn off AI Illustration and Carousel
      if (generateImage) setGenerateImage(false);
      if (generateCarousel) setGenerateCarousel(false);
      setImageModel(DEFAULT_IMAGE_MODEL); // Reset image model to default
    }
  }, [generatePostcard]);

  useEffect(() => {
    if (generateImage) {
      // AI Illustration ON: Turn off Postcard and Carousel
      if (generatePostcard) setGeneratePostcard(false);
      if (generateCarousel) setGenerateCarousel(false);
      setPostcardTheme('dark'); // Reset theme to dark
      setImageModel(DEFAULT_IMAGE_MODEL); // Reset image model to default
    }
  }, [generateImage]);

  useEffect(() => {
    if (generateCarousel) {
      // Carousel ON: Turn off Postcard and AI Illustration
      if (generatePostcard) setGeneratePostcard(false);
      if (generateImage) setGenerateImage(false);
      setPostcardTheme('dark'); // Reset theme to dark
      setImageModel(DEFAULT_IMAGE_MODEL); // Reset image model to default
    }
  }, [generateCarousel]);

  // Handle text generation
  const handleGenerateText = useCallback(async () => {
    setError(null);
    setImageData(null); // Clear previous images

    try {
      const result = await textMutation.mutateAsync({
        session_id: sessionId,
        idea,
        post_angle: postAngle || null,
        draft_post: draftPost || null,
        post_length: postLength,
        tone,
        audience,
        cta_style: ctaStyle,
        text_model: textModel,
        generate_images: generateImage || generateCarousel,  // Generate images if AI Illustration OR Carousel is enabled
        image_model: imageModel,  // Used if generate_images=True or generateCarousel=True
      });

      setTextData(result);
      // Trigger auto image generation
      setShouldAutoGenerateImages(true);
    } catch (err) {
      console.error('Text generation error in handleGenerateText:', err);
      const message = err instanceof Error ? err.message : 'Failed to generate text';
      const detail = (err as any)?.detail || (err as any)?.message || String(err);
      setError(`${message}${detail && detail !== message ? `: ${detail}` : ''}`);
    }
  }, [
    sessionId, idea, postAngle, draftPost,
    postLength, tone, audience, ctaStyle, textModel, imageModel, generateImage, generateCarousel, textMutation
  ]);

  // Handle image generation - uses image_prompts from text generation
  const handleGenerateImages = useCallback(async () => {
    if (!textData) return;

    setError(null);

    // Use regular image_prompts from text generation
    const prompts = textData.image_prompts;
    const fingerprint = textData.image_fingerprint;

    if (!prompts || prompts.length === 0) {
      // No prompts available - suggest using the recommendation
      setError('No image prompts available. Use the AI recommendation section to generate prompts first, or regenerate the post with "Generate AI Illustration" enabled.');
      return;
    }

    try {
      const result = await imageMutation.mutateAsync({
        session_id: sessionId,
        image_prompts: prompts,
        image_fingerprint: fingerprint,
        image_model: imageModel,
        // Pass carousel flag if generateCarousel is true (independent of generateImage)
        generate_carousel: generateCarousel,
        // Note: post_text, short_post, and infographic_text are read from session
        // (already stored during text generation) - no need to send again
      });

      setImageData(result);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to generate images';
      setError(message);
    }
  }, [sessionId, imageModel, textData, generateCarousel, imageMutation]);

  // Generate post card (pure code, no AI - instant!)
  const handleGeneratePostCard = useCallback(async (theme?: 'dark' | 'light') => {
    // Use theme from state if not provided
    const cardTheme = theme || postcardTheme;
    if (!textData?.post_text) {
      setError('No post content available.');
      return;
    }

    setError(null);

    try {
      const result = await postCardMutation.mutateAsync({
        session_id: sessionId,
        post_text: textData.post_text,
        short_post: textData.short_post || undefined,
        avatar_base64: profilePicBase64 || undefined,
        theme: cardTheme, // Use cardTheme which falls back to postcardTheme state
        name: PROFILE_CONFIG.name,
        handle: PROFILE_CONFIG.handle,
        verified: PROFILE_CONFIG.verified,
      });

      // Update imageData to show the post card in preview
      setImageData({
        images: [{
          id: 1,
          base64_data: result.post_card_base64,
          prompt_used: 'Post card generated with code',
          concept: `${cardTheme} theme post card`,
          format: 'png',
          width: result.width,
          height: result.height,
        }],
        pdf_base64: null,
        session_id: result.session_id,
        model_used: `PostCardBuilder (${cardTheme})`,
        image_count: 1,
        generation_time_ms: result.generation_time_ms ?? undefined,
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to generate post card';
      setError(message);
    }
  }, [sessionId, textData, postCardMutation, profilePicBase64]);

  // Auto-generate image when text is generated
  // If toggle ON: Generate AI illustration
  // If toggle OFF: Generate Post Card (instant)
  const lastTextDataIdRef = useRef<string | null>(null);
  const isGeneratingRef = useRef(false);

  useEffect(() => {
    // Only trigger if shouldAutoGenerateImages is true AND we haven't processed this textData yet
    if (shouldAutoGenerateImages && textData && !isGeneratingRef.current) {
      // Use a unique identifier to prevent duplicate calls for the same textData
      // Include short_post hash to ensure we're using the LATEST data
      const textDataId = `${textData.session_id}-${textData.post_text?.length}-${textData.short_post?.substring(0, 50)}`;

      if (lastTextDataIdRef.current !== textDataId) {
        lastTextDataIdRef.current = textDataId; // Mark this textData as processed
        isGeneratingRef.current = true;

        const generateAsync = async () => {
          try {
            if (generateCarousel) {
              // Carousel mode - needs image prompts
              if (textData.image_prompts?.length > 0) {
                await handleGenerateImages();
              }
            } else if (generateImage) {
              // AI Illustration mode
              if (textData.image_prompts?.length > 0) {
                await handleGenerateImages();
              }
            } else if (generatePostcard) {
              // Post Card mode (instant, no AI) - use current theme from state
              await handleGeneratePostCard(postcardTheme);
            }
          } finally {
            isGeneratingRef.current = false;
          }
        };

        generateAsync();
        setShouldAutoGenerateImages(false);
      }
    }

    // Reset when shouldAutoGenerateImages becomes false
    if (!shouldAutoGenerateImages) {
      lastTextDataIdRef.current = null;
    }
  }, [shouldAutoGenerateImages, textData, generatePostcard, generateImage, generateCarousel, postcardTheme, handleGenerateImages, handleGeneratePostCard]);

  // Generate based on AI recommendation
  // If type is post_card: generate post card
  // If type is AI image type AND we have prompts: just generate image
  // If type is AI image type AND we DON'T have prompts: regenerate text with prompts first
  const handleGenerateWithRecommendation = useCallback(async (recommendedType: string, isAlternative: boolean = false) => {
    if (!textData) return;

    setError(null);

    if (recommendedType === 'post_card') {
      // Post card - instant generation
      await handleGeneratePostCard(postcardTheme);
    } else {
      // AI image type
      // Check if we already have image prompts AND this is the recommended type (not alternative)
      const hasExistingPrompts = textData.image_prompts && textData.image_prompts.length > 0;

      if (hasExistingPrompts && !isAlternative) {
        // We have prompts - just generate the image directly (no text regeneration!)
        try {
          const imageResult = await imageMutation.mutateAsync({
            session_id: sessionId,
            image_prompts: textData.image_prompts,
            image_fingerprint: textData.image_fingerprint,
            image_model: imageModel,
            // Note: post_text, short_post, and infographic_text are read from session
          });
          setImageData(imageResult);
        } catch (err) {
          const message = err instanceof Error ? err.message : 'Failed to generate image';
          setError(message);
        }
      } else {
        // No prompts available OR user clicked alternative - need to regenerate text with image prompts
        try {
          // Step 1: Regenerate text WITH image prompts
          const result = await textMutation.mutateAsync({
            session_id: sessionId,
            idea,
            post_angle: postAngle,
            draft_post: draftPost || undefined,
            post_length: postLength,
            tone,
            audience,
            cta_style: ctaStyle,
            text_model: textModel,
            image_model: imageModel,
            generate_images: true,  // Force image prompts generation
          });

          setTextData(result);

          // Step 2: Generate the AI image using the new prompts
          if (result.image_prompts?.length > 0) {
            const imageResult = await imageMutation.mutateAsync({
              session_id: sessionId,
              image_prompts: result.image_prompts,
              image_fingerprint: result.image_fingerprint,
              image_model: imageModel,
              // Note: post_text, short_post, and infographic_text are read from session
            });
            setImageData(imageResult);
          }
        } catch (err) {
          const message = err instanceof Error ? err.message : 'Failed to generate with recommendation';
          setError(message);
        }
      }
    }
  }, [
    textData, sessionId, idea, postAngle, draftPost, postLength, tone, audience, ctaStyle,
    textModel, imageModel, textMutation, imageMutation, handleGeneratePostCard
  ]);

  // Regenerate text only (keeps same parameters)
  const handleRegenerateText = useCallback(async () => {
    setError(null);
    setImageData(null);

    try {
      const result = await textMutation.mutateAsync({
        session_id: sessionId,
        idea,
        post_angle: postAngle || null,
        draft_post: draftPost || null,
        post_length: postLength,
        tone,
        audience,
        cta_style: ctaStyle,
        text_model: textModel,
        generate_images: generateImage,  // If False, only generate short_post (saves tokens)
        image_model: imageModel,  // Only used if generate_images=True
      });

      setTextData(result);
      setShouldAutoGenerateImages(true);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to regenerate text';
      setError(message);
    }
  }, [
    sessionId, idea, postAngle, draftPost,
    postLength, tone, audience, ctaStyle, textModel, imageModel, generateImage, textMutation
  ]);

  // Reset session
  const handleReset = useCallback(() => {
    setSessionId(generateId());
    setIdea('');
    setPostAngle('');
    setDraftPost('');
    setPostLength(DEFAULT_POST_LENGTH);
    setTone(DEFAULT_TONE);
    setAudience([...DEFAULT_AUDIENCES]);
    setCtaStyle(DEFAULT_CTA_STYLE);
    setTextData(null);
    setImageData(null);
    setError(null);
    setGenerateImage(false);
  }, []);

  // Handle text/hashtag change from preview
  const handleTextChange = useCallback((text: string, hashtags: string[]) => {
    if (textData) {
      setTextData({
        ...textData,
        post_text: text,
        hashtags,
      });
    }
  }, [textData]);

  // Generate postcard from Manual → Postcard tab (independent, uses its own text)
  const handleManualPostcardGenerate = useCallback(async (text: string, theme: 'dark' | 'light') => {
    setError(null);

    try {
      const result = await postCardMutation.mutateAsync({
        session_id: sessionId,
        post_text: text,
        short_post: text.substring(0, 150).trim(),
        avatar_base64: profilePicBase64 || undefined,
        theme: theme,
        name: PROFILE_CONFIG.name,
        handle: PROFILE_CONFIG.handle,
        verified: PROFILE_CONFIG.verified,
      });

      // Store the generated image for the Postcard tab
      setPostcardImage(result.post_card_base64);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to generate post card';
      setError(message);
    }
  }, [sessionId, profilePicBase64, postCardMutation]);

  return (
    <div className={`min-h-screen transition-colors ${isDark ? 'bg-dark-bg' : 'bg-linkedin-background'}`}>
      {/* Header */}
      <header className={`sticky top-0 z-40 border-b ${isDark ? 'bg-dark-surface border-dark-border' : 'bg-white border-linkedin-border'}`}>
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-linkedin-blue to-accent-primary rounded-lg">
              <Linkedin className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className={`text-lg font-bold ${isDark ? 'text-dark-text' : 'text-linkedin-text'}`}>
                LinkedIn Post Generator
              </h1>
              <p className={`text-xs ${isDark ? 'text-dark-text/60' : 'text-linkedin-text-secondary'}`}>
                Powered by AI
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleReset}
              className={`p-2 rounded-full transition-colors ${isDark ? 'hover:bg-dark-border' : 'hover:bg-gray-100'}`}
              title="Start over"
            >
              <RefreshCw className={`w-5 h-5 ${isDark ? 'text-dark-text' : 'text-linkedin-text-secondary'}`} />
            </button>

            <button
              onClick={() => setIsDark(!isDark)}
              className={`p-2 rounded-full transition-colors ${isDark ? 'hover:bg-dark-border' : 'hover:bg-gray-100'}`}
              title={isDark ? 'Light mode' : 'Dark mode'}
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-dark-text" />
              ) : (
                <Moon className="w-5 h-5 text-linkedin-text-secondary" />
              )}
            </button>

            <a
              href="https://github.com/YOUR_USERNAME/linkedin_post_generator"
              target="_blank"
              rel="noopener noreferrer"
              className={`p-2 rounded-full transition-colors ${isDark ? 'hover:bg-dark-border' : 'hover:bg-gray-100'}`}
              title="View source on GitHub"
            >
              <Github className={`w-5 h-5 ${isDark ? 'text-dark-text' : 'text-linkedin-text-secondary'}`} />
            </a>
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-7xl mx-auto px-4 py-3"
        >
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-medium text-red-800">Something went wrong</h3>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-red-400 hover:text-red-600"
            >
              ×
            </button>
          </div>
        </motion.div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Tab Navigation - Always at top */}
        <TabLayout
          parentTab={parentTab}
          childTab={childTab}
          onParentTabChange={setParentTab}
          onChildTabChange={setChildTab}
        >
          {/* AI → Generate Tab */}
          {parentTab === 'ai' && childTab === 'generate' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <InputForm
                  idea={idea}
                  setIdea={setIdea}
                  postAngle={postAngle}
                  setPostAngle={setPostAngle}
                  draftPost={draftPost}
                  setDraftPost={setDraftPost}
                  postLength={postLength}
                  setPostLength={setPostLength}
                  tone={tone}
                  setTone={setTone}
                  audience={audience}
                  setAudience={setAudience}
                  ctaStyle={ctaStyle}
                  setCtaStyle={setCtaStyle}
                  textModel={textModel}
                  setTextModel={setTextModel}
                  imageModel={imageModel}
                  setImageModel={setImageModel}
                  generatePostcard={generatePostcard}
                  setGeneratePostcard={setGeneratePostcard}
                  postcardTheme={postcardTheme}
                  setPostcardTheme={setPostcardTheme}
                  generateImage={generateImage}
                  setGenerateImage={setGenerateImage}
                  generateCarousel={generateCarousel}
                  setGenerateCarousel={setGenerateCarousel}
                  onGenerate={handleGenerateText}
                  isGenerating={textMutation.isPending}
                />
              </div>
              <div className="lg:sticky lg:top-24 lg:self-start">
                <LinkedInPreview
                  textData={textData}
                  imageData={imageData}
                  isTextLoading={textMutation.isPending}
                  isImageLoading={imageMutation.isPending || postCardMutation.isPending}
                  onTextChange={handleTextChange}
                  onRegenerateText={handleRegenerateText}
                  onRegenerateImages={handleGenerateImages}
                  onGeneratePostCard={handleGeneratePostCard}
                  onGenerateWithRecommendation={handleGenerateWithRecommendation}
                  useAIImages={generateImage || generateCarousel}
                  usePostcard={generatePostcard}
                  useCarousel={generateCarousel}
                  postcardTheme={postcardTheme}
                />
              </div>
            </div>
          )}

          {/* Manual → Format Tab - Editor on left, tools on right */}
          {parentTab === 'manual' && childTab === 'format' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left: LinkedIn Preview Editor */}
              <div>
                <LinkedInPreview
                  textData={textData}
                  imageData={imageData}
                  isTextLoading={false}
                  isImageLoading={imageMutation.isPending || postCardMutation.isPending}
                  onTextChange={handleTextChange}
                  onRegenerateText={handleRegenerateText}
                  onRegenerateImages={handleGenerateImages}
                  onGeneratePostCard={handleGeneratePostCard}
                  onGenerateWithRecommendation={handleGenerateWithRecommendation}
                  useAIImages={false}
                  usePostcard={true}
                  postcardTheme={postcardTheme}
                  isManualMode={true}
                />
              </div>

              {/* Right: Quick Insert & Tips */}
              <div className="lg:sticky lg:top-24 lg:self-start space-y-4">
                {/* Quick Insert Section */}
                <div className="linkedin-card p-5 space-y-4">
                  <h3 className="font-semibold text-linkedin-text dark:text-dark-text">Quick Insert</h3>

                  {/* Arrows */}
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-linkedin-text-secondary dark:text-dark-text/60 uppercase tracking-wide">Arrows</label>
                    <div className="flex flex-wrap gap-1.5">
                      {['→', '➜', '➔', '➞', '⟶', '⇒', '▶', '►', '↳', '⤷', '➡️', '👉'].map((char) => (
                        <button
                          key={char}
                          onClick={() => navigator.clipboard.writeText(char)}
                          className="w-9 h-9 flex items-center justify-center text-lg bg-gray-100 dark:bg-dark-border hover:bg-linkedin-blue hover:text-white rounded-lg transition-colors"
                          title={`Copy ${char}`}
                        >
                          {char}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Bullets - Different Sizes */}
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-linkedin-text-secondary dark:text-dark-text/60 uppercase tracking-wide">Bullets (S → L)</label>
                    <div className="flex flex-wrap gap-1.5">
                      {['·', '∙', '•', '●', '◉', '⦿', '○', '◌', '◦', '▪', '▫', '■', '□', '◆', '◇', '★', '☆', '✦', '✧', '✓', '✗', '✔️', '❌'].map((char) => (
                        <button
                          key={char}
                          onClick={() => navigator.clipboard.writeText(char)}
                          className="w-9 h-9 flex items-center justify-center text-lg bg-gray-100 dark:bg-dark-border hover:bg-linkedin-blue hover:text-white rounded-lg transition-colors"
                          title={`Copy ${char}`}
                        >
                          {char}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Numbers */}
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-linkedin-text-secondary dark:text-dark-text/60 uppercase tracking-wide">Numbers</label>
                    <div className="flex flex-wrap gap-1.5">
                      {['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'].map((char) => (
                        <button
                          key={char}
                          onClick={() => navigator.clipboard.writeText(char)}
                          className="w-9 h-9 flex items-center justify-center text-lg bg-gray-100 dark:bg-dark-border hover:bg-linkedin-blue hover:text-white rounded-lg transition-colors"
                          title={`Copy ${char}`}
                        >
                          {char}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Emojis */}
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-linkedin-text-secondary dark:text-dark-text/60 uppercase tracking-wide">Popular Emojis</label>
                    <div className="flex flex-wrap gap-1.5">
                      {['🚀', '💡', '🔥', '✨', '💪', '🎯', '📈', '📉', '🤔', '👇', '⚡', '🙌', '💼', '🎉', '❤️', '👀', '🧠', '💰', '⏰', '🔑'].map((emoji) => (
                        <button
                          key={emoji}
                          onClick={() => navigator.clipboard.writeText(emoji)}
                          className="w-9 h-9 flex items-center justify-center text-lg bg-gray-100 dark:bg-dark-border hover:bg-gray-200 dark:hover:bg-dark-surface rounded-lg transition-colors"
                          title={`Copy ${emoji}`}
                        >
                          {emoji}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Dividers & Lines */}
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-linkedin-text-secondary dark:text-dark-text/60 uppercase tracking-wide">Dividers</label>
                    <div className="flex flex-wrap gap-1.5">
                      {['—', '─', '━', '═', '│', '┃', '∣', '|', '⸻', '~', '≈', '∼'].map((char) => (
                        <button
                          key={char}
                          onClick={() => navigator.clipboard.writeText(char)}
                          className="w-9 h-9 flex items-center justify-center text-lg bg-gray-100 dark:bg-dark-border hover:bg-linkedin-blue hover:text-white rounded-lg transition-colors"
                          title={`Copy ${char}`}
                        >
                          {char}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

              </div>
            </div>
          )}

          {/* Manual → Postcard Tab - Independent postcard creator */}
          {parentTab === 'manual' && childTab === 'postcard' && (
            <PostcardCreator
              onGeneratePostcard={handleManualPostcardGenerate}
              generatedImage={postcardImage}
              isGenerating={postCardMutation.isPending}
            />
          )}
        </TabLayout>
      </main>

      {/* Footer */}
      <footer className={`border-t mt-12 ${isDark ? 'border-dark-border' : 'border-linkedin-border'}`}>
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className={`text-center text-sm ${isDark ? 'text-dark-text/60' : 'text-linkedin-text-secondary'}`}>
            <p>Built with FastAPI + React + AI</p>
            <p className="mt-1">
              Session: <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">{sessionId.slice(0, 8)}</code>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
