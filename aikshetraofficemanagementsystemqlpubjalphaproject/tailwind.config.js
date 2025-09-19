/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
        "*.{js,ts,jsx,tsx,mdx}"
    ],
  theme: {
    extend: {
      colors: {
        background: '#111111', // Very dark gray / soft black
        surface: '#1E1E1E',    // Lighter dark gray for cards
        primary: {
          DEFAULT: '#DC2626', // Red-600
          hover: '#F87171',   // Red-400
        },
        secondary: {
          DEFAULT: '#EF4444', // Red-500
          hover: '#B91C1C',   // Red-700
        },
        'text-primary': '#F5F5F5', // Off-white (Neutral-100)
        'text-secondary': '#A3A3A3', // Muted gray (Neutral-400)
        border: '#404040', // Neutral-700
        accent: '#FFFFFF',
      },
      boxShadow: {
        'glow': '0 0 15px rgba(220, 38, 38, 0.4)',
      }
    },
  },
  plugins: [],
};
