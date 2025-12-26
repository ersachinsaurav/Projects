/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // LinkedIn-inspired color palette
        linkedin: {
          blue: '#0A66C2',
          'blue-dark': '#004182',
          'blue-light': '#70B5F9',
          background: '#F4F2EE',
          surface: '#FFFFFF',
          text: '#000000',
          'text-secondary': '#666666',
          border: '#E0E0E0',
        },
        // Custom accent colors
        accent: {
          primary: '#6366F1',    // Indigo
          secondary: '#8B5CF6',  // Violet
          success: '#10B981',    // Emerald
          warning: '#F59E0B',    // Amber
          error: '#EF4444',      // Red
        },
        // Dark theme
        dark: {
          bg: '#0D1117',
          surface: '#161B22',
          border: '#30363D',
          text: '#C9D1D9',
        },
      },
      fontFamily: {
        // LinkedIn uses system fonts
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'sans-serif',
        ],
        // Display font for headings
        display: [
          'Cal Sans',
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'sans-serif',
        ],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'shimmer': 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

