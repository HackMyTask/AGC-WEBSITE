#!/usr/bin/env python3
import os
import sys
import csv
import argparse
import logging
from datetime import datetime
from pathlib import Path

from api_client import AIClient
from quality_gate import QualityGate
from markdown_writer import MarkdownWriter
from telegram_notifier import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class ContentGenerator:
    def __init__(self):
        self.ai_client = AIClient()
        self.quality_gate = QualityGate()
        self.markdown_writer = MarkdownWriter()
        self.notifier = TelegramNotifier()
        self.terms_csv = "data/terms.csv"
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        with open("prompts/article.txt", "r") as f:
            return f.read()

    def _read_terms(self) -> list:
        """Read terms from CSV."""
        terms = []
        with open(self.terms_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                terms.append(row)
        return terms

    def _write_terms(self, terms: list):
        """Write terms back to CSV."""
        if not terms:
            return

        fieldnames = terms[0].keys()
        with open(self.terms_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(terms)

    def _get_pending_terms(self, terms: list, priority: int = None) -> list:
        """Filter pending terms, optionally by priority."""
        pending = [t for t in terms if t["status"] == "pending"]
        if priority:
            pending = [t for t in pending if int(t["priority"]) == priority]
        return pending

    def _slug_exists(self, slug: str) -> bool:
        """Check if markdown file already exists for slug."""
        return os.path.exists(f"src/content/glossary/{slug}.md")

    def _build_prompt(self, term: str, slug: str, cluster: str) -> str:
        """Build AI prompt from template."""
        prompt = self.prompt_template
        prompt = prompt.replace("{TERM}", term)
        prompt = prompt.replace("{SLUG}", slug)
        prompt = prompt.replace("{TITLE}", term)
        prompt = prompt.replace("{CLUSTER}", cluster)
        prompt = prompt.replace("{DATE}", datetime.now().isoformat())
        return prompt

    def _extract_keywords(self, term: str) -> list:
        """Generate keywords from term."""
        words = term.lower().split()
        keywords = [term.lower()]
        keywords.extend(words[:4])
        return keywords[:5]

    def generate_batch(self, batch_size: int = 20, priority: int = None, dry_run: bool = False):
        """Generate next N pending terms."""
        terms = self._read_terms()
        pending = self._get_pending_terms(terms, priority)

        if not pending:
            logger.info("No pending terms to generate")
            self.notifier.send_message("⚠️ No pending terms to generate")
            return

        logger.info(f"Found {len(pending)} pending terms. Generating {min(batch_size, len(pending))}...")
        self.notifier.notify_generation_start(batch_size, priority)

        generated_count = 0
        failed_count = 0
        quality_failures = []
        total_tokens = 0

        for term_data in pending[:batch_size]:
            term = term_data["term"]
            slug = term_data["slug"]
            cluster = term_data["cluster"]

            # Skip if already exists
            if self._slug_exists(slug):
                logger.info(f"Skipping {slug}: file already exists")
                continue

            logger.info(f"Generating: {term}")

            # Build prompt
            prompt = self._build_prompt(term, slug, cluster)

            # Generate content
            content = self.ai_client.generate(prompt, term)
            if not content:
                logger.error(f"Failed to generate {term}")
                failed_count += 1
                quality_failures.append(f"{term}: Generation failed")
                continue

            # Validate quality
            passed, errors = self.quality_gate.validate(content, term)
            if not passed:
                logger.warning(f"Quality gate failed for {term}: {errors}")
                failed_count += 1
                quality_failures.append(f"{term}: {errors[0]}")
                continue

            # Write file
            if dry_run:
                logger.info(f"[DRY RUN] Would write {slug}.md")
            else:
                if self.markdown_writer.write(slug, content):
                    # Update CSV status
                    for t in terms:
                        if t["slug"] == slug:
                            t["status"] = "done"
                    generated_count += 1
                    # Estimate tokens
                    total_tokens += len(content.split()) + len(prompt.split())

        # Write updated CSV
        if not dry_run and generated_count > 0:
            self._write_terms(terms)
            logger.info(f"Generated {generated_count} articles")

        # Send notifications
        if generated_count > 0:
            self.notifier.notify_generation_success(generated_count, batch_size, total_tokens)

        if failed_count > 0:
            self.notifier.notify_quality_failures(failed_count, quality_failures)

    def generate_single(self, slug: str, dry_run: bool = False):
        """Regenerate a single term."""
        terms = self._read_terms()
        term_data = next((t for t in terms if t["slug"] == slug), None)

        if not term_data:
            logger.error(f"Term not found: {slug}")
            return

        term = term_data["term"]
        cluster = term_data["cluster"]

        logger.info(f"Regenerating: {term}")

        prompt = self._build_prompt(term, slug, cluster)
        content = self.ai_client.generate(prompt, term)

        if not content:
            logger.error(f"Failed to generate {term}")
            return

        passed, errors = self.quality_gate.validate(content, term)
        if not passed:
            logger.warning(f"Quality gate failed: {errors}")
            return

        if dry_run:
            logger.info(f"[DRY RUN] Would write {slug}.md")
        else:
            if self.markdown_writer.write(slug, content):
                for t in terms:
                    if t["slug"] == slug:
                        t["status"] = "done"
                self._write_terms(terms)


def main():
    parser = argparse.ArgumentParser(description="Generate AI glossary content")
    parser.add_argument(
        "--batch",
        type=int,
        default=20,
        help="Number of terms to generate (10-50, default 20)"
    )
    parser.add_argument(
        "--term",
        type=str,
        help="Regenerate single term by slug"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing files"
    )
    parser.add_argument(
        "--priority",
        type=int,
        help="Only generate priority N terms (1 or 2)"
    )
    parser.add_argument(
        "--random",
        type=int,
        help="Generate random N articles (10-50)"
    )

    args = parser.parse_args()

    # Validate batch size
    batch_size = args.batch
    if batch_size < 10 or batch_size > 50:
        logger.error(f"Batch size must be between 10-50, got {batch_size}")
        sys.exit(1)

    generator = ContentGenerator()

    if args.term:
        generator.generate_single(args.term, dry_run=args.dry_run)
    elif args.random:
        if args.random < 10 or args.random > 50:
            logger.error(f"Random batch size must be between 10-50, got {args.random}")
            sys.exit(1)
        generator.generate_batch(batch_size=args.random, priority=args.priority, dry_run=args.dry_run)
    else:
        generator.generate_batch(batch_size=batch_size, priority=args.priority, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
