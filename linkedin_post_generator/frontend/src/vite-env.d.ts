/// <reference types="vite/client" />

// Environment variables (loaded from .env in project root)
interface ImportMetaEnv {
  readonly VITE_BRAND_NAME: string;
  readonly VITE_BRAND_HANDLE: string;
  readonly VITE_BRAND_TITLE: string;
  readonly VITE_BRAND_VERIFIED: string;
  readonly VITE_BRAND_WEBSITE: string;
  readonly VITE_BRAND_LINKEDIN_URL: string;
  readonly VITE_BRAND_INSTAGRAM_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

// Image imports
declare module '*.jpeg' {
  const src: string;
  export default src;
}

declare module '*.jpg' {
  const src: string;
  export default src;
}

declare module '*.png' {
  const src: string;
  export default src;
}

declare module '*.svg' {
  const src: string;
  export default src;
}

declare module '*.webp' {
  const src: string;
  export default src;
}

