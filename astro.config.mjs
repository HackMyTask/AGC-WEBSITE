import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  integrations: [tailwind(), sitemap({
    filter: (page) => page !== 'https://ailibrary.site/404/',
    serialize: (item) => {
      if (item.url === 'https://ailibrary.site/') {
        return { ...item, priority: 1.0, changefreq: 'weekly' };
      }
      if (item.url.includes('/glossary/')) {
        return { ...item, priority: 0.8, changefreq: 'monthly' };
      }
      if (item.url.includes('/topics/')) {
        return { ...item, priority: 0.7, changefreq: 'weekly' };
      }
      return { ...item, priority: 0.5, changefreq: 'monthly' };
    }
  })],
  output: 'static',
  site: 'https://ailibrary.site',
  vite: {
    ssr: {
      external: ['svgo']
    }
  }
});
