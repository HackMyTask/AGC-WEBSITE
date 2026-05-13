/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['General Sans', 'system-ui', 'sans-serif'],
      },
      colors: {
        accent: '#0ea5e9',
      },
    },
  },
  plugins: [],
};
