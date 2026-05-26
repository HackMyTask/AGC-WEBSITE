import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GLOSSARY_DIR = path.resolve(__dirname, '../src/content/glossary');
const OUTPUT_DIR = path.resolve(__dirname, '../public/og');

function getMarkdownFiles(dir) {
  const entries = readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...getMarkdownFiles(fullPath));
    } else if (entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function escapeXml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function wrapText(text, maxCharsPerLine) {
  const words = text.split(' ');
  const lines = [];
  let currentLine = '';
  for (const word of words) {
    const test = (currentLine + ' ' + word).trim();
    if (test.length > maxCharsPerLine && currentLine) {
      lines.push(currentLine.trim());
      currentLine = word;
    } else {
      currentLine = test;
    }
  }
  if (currentLine.trim()) lines.push(currentLine.trim());
  return lines;
}

function generateOgSvg(title, description) {
  const shortTitle = title.replace(/^What is /i, '');
  const titleLine = `What is ${shortTitle}?`;

  const descLines = wrapText(description, 60);

    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="60" y="60" width="1080" height="510" rx="16" fill="none" stroke="#1e293b" stroke-width="2"/>
  <text x="600" y="210" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="#0ea5e9" text-anchor="middle">${escapeXml(titleLine)}</text>
  <text x="600" y="280" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1" text-anchor="middle">${escapeXml(descLines[0] || '')}</text>
  ${descLines.length > 1 ? `<text x="600" y="310" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1" text-anchor="middle">${escapeXml(descLines[1])}</text>` : ''}
  ${descLines.length > 2 ? `<text x="600" y="340" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#cbd5e1" text-anchor="middle">${escapeXml(descLines[2])}</text>` : ''}
  <text x="600" y="430" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#64748b" text-anchor="middle">AI Glossary for Beginners</text>
  <text x="600" y="510" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#475569" text-anchor="middle">ailibrary.site</text>
</svg>`;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) return null;
  const frontmatter = {};
  const lines = match[1].split(/\r?\n/);
  for (const line of lines) {
    const strMatch = line.match(/^(\w+):\s*"(.+)"$/);
    if (strMatch) {
      frontmatter[strMatch[1]] = strMatch[2];
      continue;
    }
    const rawMatch = line.match(/^(\w+):\s*(.+)$/);
    if (rawMatch && !rawMatch[2].startsWith('[') && !rawMatch[2].startsWith('{')) {
      frontmatter[rawMatch[1]] = rawMatch[2];
    }
  }
  return frontmatter;
}

async function main() {
  if (!existsSync(OUTPUT_DIR)) {
    mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const files = getMarkdownFiles(GLOSSARY_DIR);
  let generated = 0;

  for (const file of files) {
    const content = readFileSync(file, 'utf-8');
    const fm = parseFrontmatter(content);
    if (!fm || !fm.slug) continue;

    const slug = fm.slug;
    const title = fm.title || '';
    const description = (fm.description || '').replace(/\.\.\.$/, '');

    const svg = generateOgSvg(title, description);
    const outputPath = path.join(OUTPUT_DIR, `${slug}.svg`);
    writeFileSync(outputPath, svg, 'utf-8');
    generated++;
  }

  console.log(`Generated ${generated} OG images to ${OUTPUT_DIR}/`);
}

main().catch(console.error);
