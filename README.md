# AI Glossary for Beginners

A static site glossary explaining AI concepts in plain language for non-technical audiences.

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Groq or Gemini API key

### Setup

1. **Clone and install:**
   ```bash
   git clone <repo>
   cd AGC-WEBSITE
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Generate content:**
   ```bash
   npm run generate:batch
   ```

4. **Build and preview:**
   ```bash
   npm run build
   npm run preview
   ```

## Project Structure

```
AGC-WEBSITE/
├── content/glossary/          ← Generated .md articles
├── data/
│   └── terms.csv              ← Source of truth for all terms
├── scripts/
│   ├── api_client.py          ← AI provider abstraction
│   ├── generate.py            ← Main content generation
│   ├── quality_gate.py        ← Content validation
│   ├── internal_links.py      ← Bidirectional linking
│   └── markdown_writer.py     ← Safe file writing
├── src/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   └── styles/
├── prompts/
│   └── article.txt            ← AI prompt template
├── astro.config.mjs
├── tailwind.config.mjs
└── package.json
```

## Development Commands

### Content Generation

```bash
# Generate next 20 pending terms (default)
npm run generate:batch

# Generate specific batch sizes (10-50)
npm run generate:batch:10          # Generate 10 articles
npm run generate:batch:30          # Generate 30 articles
npm run generate:batch:50          # Generate 50 articles

# Generate random N articles (10-50)
npm run generate:random:10         # Random 10 articles
npm run generate:random:30         # Random 30 articles
npm run generate:random:50         # Random 50 articles

# Generate only priority 1 terms
npm run generate:priority1         # 20 priority 1 terms
npm run generate:priority1:50      # 50 priority 1 terms

# Regenerate single term
npm run generate:single -- what-is-rag

# Preview without writing files
npm run generate:dry-run

# Update internal links
npm run links
```

### Site Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Batch Size Options

**Range:** 10-50 articles per run

**Default:** 20 articles

**Examples:**
- Small batch: `npm run generate:batch:10` (10 articles)
- Medium batch: `npm run generate:batch:20` (20 articles)
- Large batch: `npm run generate:batch:50` (50 articles)

**Random generation:**
- `npm run generate:random:30` — Generate 30 random pending terms
- Useful for testing different term combinations

## Data Management

### terms.csv Format

```csv
term,slug,cluster,status,priority
What is RAG,what-is-rag,llms,pending,1
What is an AI Agent,what-is-an-ai-agent,ai-agents,pending,1
```

**Fields:**
- `term`: Display name
- `slug`: URL-safe identifier (lowercase, hyphenated)
- `cluster`: Topic category (ai-basics, llms, prompt-engineering, ai-tools)
- `status`: pending | done | skip
- `priority`: 1 (generate first) | 2 (secondary)

## Content Generation Pipeline

1. **Read** pending terms from `data/terms.csv`
2. **Check** if markdown file already exists (dedup)
3. **Generate** via AI provider (Groq or Gemini)
4. **Validate** with quality gate checks
5. **Write** to `content/glossary/[slug].md`
6. **Update** CSV status to `done`
7. **Link** related terms bidirectionally

## Quality Gate Checks

Every generated article must pass:
- ✓ 300–1400 words
- ✓ Flesch-Kincaid grade ≤ 10
- ✓ All 5 required sections present
- ✓ No AI clichés (delve, leverage, etc.)
- ✓ No generic intro patterns
- ✓ Valid frontmatter
- ✓ Description ≤ 160 characters

Failed articles are logged to `logs/quality_failures.log` and retried once.

## Article Structure

Each glossary article follows this template:

```markdown
---
title: "What is RAG?"
slug: "what-is-rag"
description: "A technique that lets AI access external information."
keywords: ["rag", "retrieval", "augmented", "generation", "ai"]
cluster: "llms"
related_terms: ["what-is-an-llm", "what-is-embedding"]
created_at: "2026-05-13T00:00:00Z"
updated_at: "2026-05-13T00:00:00Z"
author: "AI Glossary Team"
schema_type: "DefinedTerm"
---

## What is RAG?

[Simple 2–3 sentence explanation]

## Think of It Like This

[Real-world analogy]

## Why Should You Care?

[Practical relevance]

## Where You've Already Seen It

[Real tool examples]

## The One Thing to Remember

[One-sentence takeaway]

## Related Terms

[comma-separated slugs]
```

## API Providers

### Groq (Default)

```bash
AI_PROVIDER=groq
GROQ_API_KEY=your_key
```

Model: `llama-3.3-70b-versatile`

### Gemini

```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
```

Model: `gemini-2.0-flash`

### Multiple API Keys (Rotation)

To avoid rate limits, configure multiple API keys separated by commas or pipes:

```bash
# Comma-separated
GROQ_API_KEY=key1,key2,key3

# Pipe-separated
GROQ_API_KEY=key1|key2|key3
```

**How it works:**
1. Starts with first key
2. On rate limit, automatically rotates to next key
3. Retries with new key
4. Cycles through all keys
5. Logs all rotations to `logs/api_rotation.log`

**Example with 3 Groq keys:**
```bash
GROQ_API_KEY=gsk_abc123,gsk_def456,gsk_ghi789
```

Each key gets its own quota, so 3 keys = 3x the generation capacity.

## Logging

- `logs/usage.log` — Token usage per generation
- `logs/writes.log` — File write operations
- `logs/quality_failures.log` — Failed quality gate checks

## Deployment

### Cloudflare Pages

```bash
# Build command
npm run build && npx pagefind --site dist

# Output directory
dist/
```

**Environment variables:**
```
NODE_VERSION=18
```

## Topic Clusters

**Phase 1 (Current):**
- `ai-basics` — Fundamentals
- `llms` — Large Language Models
- `prompt-engineering` — Prompt techniques
- `ai-tools` — Popular AI applications

**Phase 2 (Future):**
- `ai-agents` — AI Agents
- `ai-image-video` — Image & Video generation
- `ai-automation` — Automation workflows
- `ai-coding` — AI for coding
- `ai-infrastructure` — Infrastructure & APIs

## SEO

- Schema markup: `DefinedTerm` + `Article` JSON-LD
- Meta tags: title, description, canonical
- Robots.txt: allows indexing, disallows scripts/data
- Sitemaps: split by alphabet (coming soon)
- RSS feed: 50 latest articles (coming soon)

## E-E-A-T

- ✓ Clear editorial mission on `/about`
- ✓ Author byline: "AI Glossary Team"
- ✓ Editorial note: "Reviewed for clarity and accuracy"
- ✓ `datePublished` and `dateModified` visible
- ✓ Contact mechanism: email link
- ✓ Privacy Policy and Terms pages

## Troubleshooting

### Generation fails with rate limit
- Increase `DAILY_LIMIT` in `.env`
- Retry after 1 hour
- Switch to different provider

### Quality gate rejects articles
- Check `logs/quality_failures.log` for reason
- Adjust prompt in `prompts/article.txt`
- Regenerate with `npm run generate:single`

### Build fails
- Ensure all `.md` files have valid frontmatter
- Check for broken links in related_terms
- Run `npm run build` with `--verbose` flag

## Contributing

1. Add new terms to `data/terms.csv`
2. Set `status=pending`
3. Run `npm run generate:batch`
4. Review generated articles
5. Commit and push

## License

MIT
