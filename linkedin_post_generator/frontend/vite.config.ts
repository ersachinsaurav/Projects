import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ mode }) => {
  // Load env from root directory (parent of frontend)
  const env = loadEnv(mode, path.resolve(__dirname, '..'), 'VITE_')

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    // Expose VITE_ prefixed env vars to the app
    define: {
      'import.meta.env.VITE_BRAND_NAME': JSON.stringify(env.VITE_BRAND_NAME || 'Your Name'),
      'import.meta.env.VITE_BRAND_HANDLE': JSON.stringify(env.VITE_BRAND_HANDLE || '@yourusername'),
      'import.meta.env.VITE_BRAND_TITLE': JSON.stringify(env.VITE_BRAND_TITLE || 'Your Professional Title | Your Company'),
      'import.meta.env.VITE_BRAND_VERIFIED': JSON.stringify(env.VITE_BRAND_VERIFIED || 'false'),
      'import.meta.env.VITE_BRAND_WEBSITE': JSON.stringify(env.VITE_BRAND_WEBSITE || 'yourwebsite.com'),
      'import.meta.env.VITE_BRAND_LINKEDIN_URL': JSON.stringify(env.VITE_BRAND_LINKEDIN_URL || 'linkedin.com/in/yourusername'),
      'import.meta.env.VITE_BRAND_INSTAGRAM_URL': JSON.stringify(env.VITE_BRAND_INSTAGRAM_URL || 'instagram.com/yourusername'),
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:5170',
          changeOrigin: true,
        },
      },
    },
  }
})

