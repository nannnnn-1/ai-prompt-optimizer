/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      screens: {
        'mobile': '320px',
        'tablet': '768px', 
        'desktop': '1024px',
        'wide': '1440px'
      },
      colors: {
        primary: {
          50: '#e6f7ff',
          100: '#bae7ff',
          200: '#7cc7ff',
          300: '#47a3f3',
          400: '#2378f7',
          500: '#1890ff',
          600: '#177ddc',
          700: '#1564ab',
          800: '#10467f',
          900: '#0b2f5c'
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace']
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true,
  }
} 