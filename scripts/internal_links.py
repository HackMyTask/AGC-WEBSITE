#!/usr/bin/env python3
import os
import csv
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InternalLinker:
    def __init__(self):
        self.glossary_dir = "src/content/glossary"
        self.terms_csv = "data/terms.csv"
        self.max_links_per_article = 3

    def _read_terms(self) -> dict:
        """Read terms CSV and return dict of slug -> term data."""
        terms = {}
        with open(self.terms_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                terms[row["slug"]] = row
        return terms

    def _get_related_terms(self, slug: str, cluster: str, terms: dict) -> list:
        """Get related terms in same cluster (max 3)."""
        related = [
            s for s, t in terms.items()
            if t["cluster"] == cluster and s != slug and t["status"] == "done"
        ]
        return related[:3]

    def _extract_frontmatter(self, content: str) -> tuple:
        """Extract frontmatter and body. Returns (frontmatter_dict, body)."""
        parts = content.split("---")
        if len(parts) < 3:
            return {}, content

        frontmatter_text = parts[1].strip()
        body = "---".join(parts[2:]).strip()

        frontmatter = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter, body

    def _inject_inline_links(self, body: str, related_slugs: list, terms: dict) -> str:
        """Inject up to 3 natural inline links into body."""
        if not related_slugs:
            return body

        # Find natural link opportunities (first mention of related terms)
        links_added = 0
        for slug in related_slugs:
            if links_added >= self.max_links_per_article:
                break

            term = terms[slug]["term"]
            # Look for first occurrence of term (case-insensitive)
            pattern = rf"\b{re.escape(term)}\b"
            match = re.search(pattern, body, re.IGNORECASE)

            if match and f"[{term}]" not in body:  # Avoid double-linking
                start, end = match.span()
                body = body[:start] + f"[{term}](/glossary/{slug})" + body[end:]
                links_added += 1

        return body

    def _update_related_terms_section(self, body: str, related_slugs: list) -> str:
        """Update the Related Terms section with slugs."""
        related_section_pattern = r"## Related Terms\n\n.*?(?=\n##|\Z)"
        related_text = ", ".join(related_slugs) if related_slugs else "None"

        if re.search(related_section_pattern, body, re.DOTALL):
            body = re.sub(
                related_section_pattern,
                f"## Related Terms\n\n{related_text}",
                body,
                flags=re.DOTALL
            )
        else:
            body += f"\n\n## Related Terms\n\n{related_text}"

        return body

    def process_all(self):
        """Process all glossary files and inject bidirectional links."""
        terms = self._read_terms()

        if not os.path.exists(self.glossary_dir):
            logger.warning(f"Glossary directory not found: {self.glossary_dir}")
            return

        files = list(Path(self.glossary_dir).glob("*.md"))
        logger.info(f"Processing {len(files)} glossary files...")

        for filepath in files:
            slug = filepath.stem
            if slug not in terms:
                logger.warning(f"Slug not in terms.csv: {slug}")
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            frontmatter, body = self._extract_frontmatter(content)
            cluster = frontmatter.get("cluster", "")

            # Get related terms
            related_slugs = self._get_related_terms(slug, cluster, terms)

            # Inject inline links
            body = self._inject_inline_links(body, related_slugs, terms)

            # Update related terms section
            body = self._update_related_terms_section(body, related_slugs)

            # Reconstruct content
            frontmatter_text = "\n".join([f"{k}: {v}" for k, v in frontmatter.items()])
            updated_content = f"---\n{frontmatter_text}\n---\n\n{body}"

            # Write back
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

            logger.info(f"Updated {slug} with {len(related_slugs)} related terms")


def main():
    linker = InternalLinker()
    linker.process_all()


if __name__ == "__main__":
    main()
