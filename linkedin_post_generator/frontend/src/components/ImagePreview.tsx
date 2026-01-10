/**
 * Image Preview Component
 * ========================
 * Grid preview for generated images with download options
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Download,
  FileText,
  Image as ImageIcon,
  Maximize2,
  X,
  Clock,
  Sparkles,
} from 'lucide-react';
import type {
  ImageGenerationResponse,
  ImageModelConfig,
  TextGenerationResponse,
} from '../types';
import { cn, downloadImage, downloadPDF, formatDuration, getFilenameFromContent } from '../lib/utils';

interface ImagePreviewProps {
  textData: TextGenerationResponse | null;
  imageData: ImageGenerationResponse | null;
  isLoading: boolean;
  imageModel: ImageModelConfig;
  setImageModel: (model: ImageModelConfig) => void;
  onGenerate: () => void;
  canGenerate: boolean;
}

// Note: Nova and Titan do NOT support text overlays like SDXL does
const IMAGE_MODELS = [
  { provider: 'sdxl', model: 'sdxl', label: 'SDXL', badge: 'Local', description: 'Supports overlays (recommended)' },
  { provider: 'nova', model: 'nova-canvas', label: 'Nova Canvas', description: 'Cloud, no overlay support' },
  { provider: 'titan', model: 'titan-image-generator-v2', label: 'Titan v2', description: 'Cloud, no overlay support' },
];

export function ImagePreview({
  textData,
  imageData,
  isLoading,
  imageModel,
  setImageModel,
  onGenerate,
  canGenerate,
}: ImagePreviewProps) {
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

  const handleDownloadImage = (base64: string, index: number) => {
    // Use shared utility for consistent filename generation
    const concept = textData?.image_prompts?.[index]?.concept || imageData?.images[index]?.concept;
    const filename = getFilenameFromContent({
      title: textData?.infographic_text?.title,
      postText: textData?.post_text,
      concept,
      defaultName: `linkedin-image-${index + 1}`,
      extension: 'png',
    });

    downloadImage(base64, filename);
  };

  const handleDownloadPDF = () => {
    if (imageData?.pdf_base64) {
      let filename = imageData.pdf_title || 'linkedin-carousel.pdf';

      // If filename doesn't have .pdf extension, ensure it's clean
      if (!filename.endsWith('.pdf')) {
        filename = filename + '.pdf';
      }

      // Backend now sends sanitized filenames, so this should be fine
      downloadPDF(imageData.pdf_base64, filename);
    }
  };

  const handleDownloadAll = () => {
    imageData?.images.forEach((img, idx) => {
      setTimeout(() => {
        handleDownloadImage(img.base64_data, idx);
      }, idx * 200);
    });
  };

  const imageCount = textData?.image_strategy?.image_count || 0;
  const hasImages = imageData && imageData.images.length > 0;

  // Grid layout based on image count
  const getGridClass = (count: number) => {
    if (count === 1) return 'grid-cols-1';
    if (count === 2) return 'grid-cols-2';
    if (count <= 4) return 'grid-cols-2';
    return 'grid-cols-2 md:grid-cols-3';
  };

  if (!textData) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="linkedin-card p-6"
      >
        <div className="text-center py-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
            <ImageIcon className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-linkedin-text mb-2">Images coming soon</h3>
          <p className="text-sm text-linkedin-text-secondary">
            Generate your post text first, then create matching images.
          </p>
        </div>
      </motion.div>
    );
  }

  if (imageCount === 0 && !hasImages) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="linkedin-card p-6"
      >
        <div className="text-center py-8">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-amber-50 flex items-center justify-center">
            <FileText className="w-8 h-8 text-amber-500" />
          </div>
          <h3 className="text-lg font-medium text-linkedin-text mb-2">Text-only post recommended</h3>
          <p className="text-sm text-linkedin-text-secondary mb-4">
            The AI suggests this post works best without images.
          </p>
          <button
            onClick={onGenerate}
            className="btn-secondary text-sm"
          >
            Generate images anyway
          </button>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="linkedin-card overflow-hidden"
    >
      {/* Header */}
      <div className="p-4 border-b border-linkedin-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-accent-primary to-accent-secondary rounded-lg">
              <ImageIcon className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="font-semibold text-linkedin-text">Images</h2>
              <p className="text-xs text-linkedin-text-secondary">
                {hasImages
                  ? `${imageData.images.length} image${imageData.images.length > 1 ? 's' : ''} generated`
                  : `${imageCount} image${imageCount > 1 ? 's' : ''} suggested`
                }
              </p>
            </div>
          </div>

          {(hasImages || imageData?.pdf_base64) && (
            <div className="flex items-center gap-2">
              {imageData?.pdf_base64 && (
                <button
                  onClick={handleDownloadPDF}
                  className="btn-secondary text-xs py-1.5 px-3 flex items-center gap-1"
                >
                  <div className="w-3 h-3 flex items-center justify-center font-bold text-[10px]">PDF</div>
                </button>
              )}
              {hasImages && (
                <button
                  onClick={handleDownloadAll}
                  className="btn-primary text-xs py-1.5 px-3 flex items-center gap-1"
                >
                  <Download className="w-3 h-3" />
                  All
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {isLoading ? (
          <div className="space-y-4">
            <div className={`grid ${getGridClass(imageCount)} gap-4`}>
              {Array.from({ length: imageCount }).map((_, i) => (
                <div
                  key={i}
                  className="aspect-square bg-gray-100 rounded-lg animate-pulse flex items-center justify-center"
                >
                  <div className="text-center">
                    <div className="w-8 h-8 mx-auto mb-2 border-2 border-gray-300 border-t-linkedin-blue rounded-full animate-spin" />
                    <span className="text-xs text-gray-400">Generating...</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : hasImages ? (
          <>
            {/* Image Grid */}
            <div className={`grid ${getGridClass(imageData.images.length)} gap-4`}>
              {imageData.images.map((img, idx) => (
                <motion.div
                  key={img.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  className="relative group"
                >
                  <img
                    src={`data:image/${img.format};base64,${img.base64_data}`}
                    alt={`Generated image ${idx + 1}`}
                    className="w-full aspect-square object-cover rounded-lg border border-linkedin-border"
                  />

                  {/* Overlay */}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setSelectedImage(idx)}
                        className="p-2 bg-white rounded-full shadow-lg hover:scale-110 transition-transform"
                      >
                        <Maximize2 className="w-4 h-4 text-linkedin-text" />
                      </button>
                      <button
                        onClick={() => handleDownloadImage(img.base64_data, idx)}
                        className="p-2 bg-white rounded-full shadow-lg hover:scale-110 transition-transform"
                      >
                        <ImageIcon className="w-4 h-4 text-linkedin-text" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Stats */}
            <div className="mt-4 pt-3 border-t border-linkedin-border flex items-center justify-between text-xs text-linkedin-text-secondary">
              <div className="flex items-center gap-4">
                {imageData.generation_time_ms && (
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {formatDuration(imageData.generation_time_ms)}
                  </span>
                )}
              </div>
              <span className="bg-gray-100 px-2 py-0.5 rounded">
                {imageData.model_used}
              </span>
            </div>
          </>
        ) : (
          <>
            {/* Model Selection */}
            <div className="space-y-3 mb-4">
              <label className="text-sm font-medium text-linkedin-text">Choose Model</label>
              <div className="grid grid-cols-2 gap-2">
                {IMAGE_MODELS.map((model) => (
                  <button
                    key={`${model.provider}-${model.model}`}
                    onClick={() => setImageModel({
                      provider: model.provider as 'nova' | 'titan' | 'sdxl',
                      model: model.model
                    })}
                    className={cn(
                      'px-3 py-2 text-sm rounded-lg transition-colors text-left relative',
                      imageModel.provider === model.provider && imageModel.model === model.model
                        ? 'bg-accent-primary text-white'
                        : 'bg-gray-100 text-linkedin-text hover:bg-gray-200'
                    )}
                  >
                    <div className="font-medium">{model.label}</div>
                    <div className={cn(
                      'text-xs',
                      imageModel.provider === model.provider && imageModel.model === model.model
                        ? 'text-white/70'
                        : 'text-linkedin-text-secondary'
                    )}>
                      {model.description}
                    </div>
                    {model.badge && (
                      <span className={cn(
                        'absolute top-1 right-1 text-[10px] px-1.5 py-0.5 rounded-full',
                        imageModel.provider === model.provider && imageModel.model === model.model
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

            {/* Image Prompts Preview */}
            {textData.image_prompts.length > 0 && (
              <div className="space-y-2 mb-4">
                <label className="text-sm font-medium text-linkedin-text">Preview Prompts</label>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {textData.image_prompts.map((prompt) => (
                    <div
                      key={prompt.id}
                      className="p-2 bg-gray-50 rounded-lg text-xs text-linkedin-text-secondary"
                    >
                      <div className="font-medium text-linkedin-text mb-1">
                        Image {prompt.id}
                      </div>
                      <div className="line-clamp-2">{prompt.prompt}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Generate Button */}
            <button
              onClick={onGenerate}
              disabled={!canGenerate || isLoading}
              className={cn(
                'w-full py-3 rounded-full font-semibold transition-all flex items-center justify-center gap-2',
                canGenerate && !isLoading
                  ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white hover:shadow-lg hover:scale-[1.02]'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              )}
            >
              <Sparkles className="w-5 h-5" />
              Generate {imageCount} Image{imageCount > 1 ? 's' : ''}
            </button>
          </>
        )}
      </div>

      {/* Lightbox */}
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

            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-2">
              {/* PDF Download button */}
              {imageData.pdf_base64 && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDownloadPDF();
                  }}
                  className="px-4 py-2 bg-white rounded-full text-sm font-medium text-linkedin-text flex items-center gap-2 hover:bg-gray-100 transition-colors"
                >
                  <div className="w-4 h-4 flex items-center justify-center font-bold text-xs">PDF</div>
                  PDF
                </button>
              )}
              {/* Image Download button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDownloadImage(imageData.images[selectedImage].base64_data, selectedImage);
                }}
                className="px-4 py-2 bg-white rounded-full text-sm font-medium text-linkedin-text flex items-center gap-2 hover:bg-gray-100 transition-colors"
              >
                <ImageIcon className="w-4 h-4" />
                Download
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

