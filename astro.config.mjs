import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  output: 'static',
  site: 'https://ai-glossary.example.com',
  vite: {
    ssr: {
      external: ['svgo']
    }
  }
});
