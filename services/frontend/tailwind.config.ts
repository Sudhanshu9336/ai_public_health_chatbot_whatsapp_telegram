import type { Config } from 'tailwindcss'
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#14532d', // deep green
        accent: '#dc2626'   // red for alerts
      },
      borderRadius: {
        '2xl': '1.25rem'
      }
    }
  },
  plugins: [],
} satisfies Config
