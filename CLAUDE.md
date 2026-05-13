# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: AI Glossary for Beginners

A static site glossary explaining AI concepts in plain language for non-technical audiences. Built with Astro, TailwindCSS, and automated content generation via Python scripts.

## Tech Stack

- **Frontend:** Astro (static site generation) + TailwindCSS v4
- **Content:** Markdown files in `content/glossary/`
- **Automation:** Python 3.9+ scripts for content generation
- **AI Providers:** Groq (default) or Google Gemini
- **Deployment:** Cloudflare Pages
- **Data:** CSV-based term management (`data/terms.csv`)

## Project Structure

```
AGC-WEBSITE/
├── content/glossary/          ← Generated .md articles
├── data/terms.csv             ← Source of truth (50 seed terms)
├── scripts/
│   ├── api_client.py          ← AI provider abstraction (Groq/Gemini)
│   ├── generate.py            ← Main content generation CLI
│   ├── quality_gate.py        ← Content validation (word count, reading level, clichés)
│   ├── internal_links.py      ← Bidirectional link injection
│   └── markdown_writer.py     ← Safe atomic file writing
├── src/
│   ├── layouts/Layout.astro   ← Main layout (header, footer, nav)
│   └── pages/
│       ├── index.astro        ← Homepage
│       ├── about.astro        ← About page
│       ├── search.astro       ← Search page (Pagefind integration)
│       └── glossary/[slug].astro ← Dynamic glossary pages
├── prompts/article.txt        ← AI prompt template (reusable)
├── astro.config.mjs
├── tailwind.config.mjs
└── package.json
```

## Development Commands

### Content Generation

```bash
npm run generate:batch          # Generate next 20 pending terms
npm run generate:priority1      # Generate only priority 1 terms
npm run generate:single -- <slug>  # Regenerate single term
npm run generate:dry-run        # Preview without writing
npm run links                   # Update internal links
```

### Site Development

```bash
npm run dev                     # Start dev server (localhost:3000)
npm run build                   # Build for production
npm run preview                 # Preview production build
```

## Architecture & Key Concepts

### Content Pipeline

1. **Data Layer:** `data/terms.csv` is the single source of truth
   - 50 seed terms across 4 clusters (ai-basics, llms, prompt-engineering, ai-tools)
   - Fields: term, slug, cluster, status (pending/done/skip), priority (1/2)

2. **Generation Flow:**
   - Read pending terms from CSV
   - Check if `.md` already exists (dedup protection)
   - Send to AI via `api_client.py` (Groq or Gemini)
   - Validate with `quality_gate.py` (word count, reading level, clichés, sections)
   - Write to `content/glossary/[slug].md` via `markdown_writer.py`
   - Update CSV status to `done`
   - Inject bidirectional links via `internal_links.py`

3. **Quality Gate Checks:**
   - Word count: 300–1400 words
   - Reading level: Flesch-Kincaid grade ≤ 10
   - Required sections: 5 (What is, Think of It Like This, Why Should You Care, Where You've Already Seen It, The One Thing to Remember)
   - No AI clichés (delve, leverage, cutting-edge, etc.)
   - No generic intro patterns
   - Valid frontmatter + description ≤ 160 chars

4. **Logging:**
   - `logs/usage.log` — Token usage per generation
   - `logs/writes.log` — File operations
   - `logs/quality_failures.log` — Failed validations

### Article Structure

Every glossary article has:
- **Frontmatter:** title, slug, description, keywords, cluster, related_terms, dates, author, schema_type
- **Body:** 5 required sections (see quality gate above)
- **Schema:** DefinedTerm + Article JSON-LD for SEO

### API Client (`api_client.py`)

- Abstracts Groq and Gemini behind unified interface
- Retry logic: 3 retries with exponential backoff on rate limits
- Token usage logging to `logs/usage.log`
- Daily limit enforcement (default 100 tokens/day, configurable)

### Markdown Writer (`markdown_writer.py`)

- Hash-based dedup: skips if content unchanged
- Atomic writes: temp file → rename (prevents corruption)
- Frontmatter validation before writing
- Logs all operations to `logs/writes.log`

### Internal Linker (`internal_links.py`)

- Injects up to 3 inline links per article (natural placement)
- Bidirectional: if A links to B, B links to A
- Updates "Related Terms" section with slugs
- Runs after every batch generation

## Configuration

### .env Setup

```bash
AI_PROVIDER=groq              # or gemini
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
DAILY_LIMIT=100               # Max tokens/day
BATCH_SIZE=20                 # Default batch size
```

### Astro Config

- Output: static (100% SSG, no runtime)
- Site URL: https://ai-glossary.example.com (update for production)
- Tailwind integration enabled

## Common Tasks

### Add new terms
1. Edit `data/terms.csv`
2. Add rows with status=pending
3. Run `npm run generate:batch`

### Regenerate single article
```bash
npm run generate:single -- what-is-rag
```

### Preview generation without writing
```bash
npm run generate:dry-run
```

### Update all internal links
```bash
npm run links
```

### Check generation logs
```bash
cat logs/quality_failures.log    # Failed validations
cat logs/usage.log               # Token usage
cat logs/writes.log              # File operations
```

## Deployment

### Cloudflare Pages

**Build command:**
```bash
npm run build && npx pagefind --site dist
```

**Output directory:** `dist/`

**Environment:** NODE_VERSION=18

## SEO & E-E-A-T

- ✓ Schema markup: DefinedTerm + Article JSON-LD per page
- ✓ Meta tags: title, description, canonical
- ✓ Author byline: "AI Glossary Team" on every article
- ✓ Editorial note: "Reviewed for clarity and accuracy"
- ✓ Dates visible: datePublished, dateModified
- ✓ About page: clear mission statement
- ✓ Contact: email link on about page
- ✓ Privacy Policy & Terms pages (static, minimal)

## Phase Roadmap

**Phase 1 (Current):** 1–1,000 pages
- 4 core clusters (ai-basics, llms, prompt-engineering, ai-tools)
- Priority 1 terms first
- Strict quality gate

**Phase 2:** 1,000–10,000 pages
- Expand to 9 clusters
- OG image generation per page
- Split sitemaps by alphabet

**Phase 3:** 10,000–100,000 pages
- IndexNow integration
- hreflang for multi-language
- Cluster sub-clusters

## gstack

gstack is installed at `~/.claude/skills/gstack` and provides specialized skills for code review, planning, design, deployment, and more.

### Web Browsing

**Use the `/browse` skill from gstack for all web browsing.** Never use `mcp__claude-in-chrome__*` tools.

### Available Skills

- `/office-hours` - Office hours
- `/plan-ceo-review` - CEO review planning
- `/plan-eng-review` - Engineering review planning
- `/plan-design-review` - Design review planning
- `/design-consultation` - Design consultation
- `/design-shotgun` - Rapid design iteration
- `/design-html` - HTML design
- `/review` - Code review
- `/ship` - Ship code
- `/land-and-deploy` - Land PRs and deploy
- `/canary` - Canary deployments
- `/benchmark` - Benchmarking
- `/browse` - Web browsing (use this, not mcp tools)
- `/connect-chrome` - Connect Chrome
- `/qa` - Quality assurance
- `/qa-only` - QA only
- `/design-review` - Design review
- `/setup-browser-cookies` - Setup browser cookies
- `/setup-deploy` - Setup deployment
- `/setup-gbrain` - Setup gbrain
- `/retro` - Retrospectives
- `/investigate` - Investigation
- `/document-release` - Document release
- `/codex` - Codex
- `/cso` - CSO
- `/autoplan` - Automatic planning
- `/plan-devex-review` - Developer experience review planning
- `/devex-review` - Developer experience review
- `/careful` - Careful mode
- `/freeze` - Freeze
- `/guard` - Guard
- `/unfreeze` - Unfreeze
- `/gstack-upgrade` - Upgrade gstack
- `/learn` - Learn

### Usage

Run any skill with `/<skill-name>` or use `/gstack-upgrade` to keep gstack current.
