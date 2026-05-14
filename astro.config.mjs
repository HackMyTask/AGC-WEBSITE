import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  output: 'static',
  site: process.env.SITE_URL || 'https://ai-glossary.pages.dev',
  vite: {
    ssr: {
      external: ['svgo']
    }
  }
});
