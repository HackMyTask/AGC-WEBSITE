import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const glossary = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/glossary' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    keywords: z.array(z.string()).default([]),
    cluster: z.string().default(''),
    related_terms: z.array(z.string()).default([]),
    created_at: z.string().optional(),
  }),
});

export const collections = { glossary };
