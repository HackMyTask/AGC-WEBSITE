import os
import re
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityGate:
    def __init__(self):
        self.failure_log = "logs/quality_failures.log"
        self._ensure_log_file()

        self.checks = {
            "min_words": 300,
            "max_words": 1400,
            "flesch_kincaid_max": 14,
            "has_required_sections": [
                "## What is",
                "## Think of It Like This",
                "## Why Should You Care",
                "## Where You've Already Seen It",
                "## The One Thing to Remember",
            ],
            "ai_cliche_detector": [
                "delve",
                "leverage",
                "it's worth noting",
                "in the realm of",
                "game-changer",
                "revolutionize",
                "cutting-edge",
                "seamlessly",
                "robust",
                "paradigm",
                "foster",
                "facilitate",
                "utilize",
            ],
            "duplicate_intro_patterns": [
                "In the world of AI",
                "In today's rapidly evolving",
                "Artificial intelligence has",
                "In recent years",
                "The world of artificial",
            ],
            "description_max_chars": 160,
        }

    def _ensure_log_file(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.failure_log):
            open(self.failure_log, "w").close()

    def _log_failure(self, term: str, reason: str):
        with open(self.failure_log, "a") as f:
            f.write(f"{term} | {reason}\n")

    def _count_words(self, text: str) -> int:
        return len(text.split())

    def _extract_body(self, content: str) -> str:
        """Extract content after frontmatter."""
        parts = content.split("---")
        if len(parts) >= 3:
            return parts[2].strip()
        return content

    def _flesch_kincaid_grade(self, text: str) -> float:
        """Estimate Flesch-Kincaid grade level."""
        sentences = len(re.split(r"[.!?]+", text))
        words = len(text.split())
        syllables = self._count_syllables(text)

        if words == 0 or sentences == 0:
            return 0

        grade = (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59
        return max(0, grade)

    def _count_syllables(self, text: str) -> int:
        """Rough syllable counter."""
        count = 0
        vowels = "aeiouy"
        previous_was_vowel = False

        for char in text.lower():
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        return max(1, count)

    def _parse_frontmatter(self, content: str) -> Dict:
        """Extract frontmatter as dict."""
        parts = content.split("---")
        if len(parts) < 3:
            return {}

        frontmatter_text = parts[1].strip()
        frontmatter = {}

        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    def validate(self, content: str, term: str) -> Tuple[bool, List[str]]:
        """Run all quality checks. Returns (passed, errors)."""
        errors = []
        body = self._extract_body(content)
        frontmatter = self._parse_frontmatter(content)

        # Word count
        word_count = self._count_words(body)
        if word_count < self.checks["min_words"]:
            errors.append(f"Too short: {word_count} words (min {self.checks['min_words']})")
        if word_count > self.checks["max_words"]:
            errors.append(f"Too long: {word_count} words (max {self.checks['max_words']})")

        # Flesch-Kincaid
        grade = self._flesch_kincaid_grade(body)
        if grade > self.checks["flesch_kincaid_max"]:
            errors.append(f"Reading level too high: grade {grade:.1f} (max {self.checks['flesch_kincaid_max']})")

        # Required sections
        for section in self.checks["has_required_sections"]:
            if section not in content:
                errors.append(f"Missing section: {section}")

        # AI clichés
        body_lower = body.lower()
        found_cliches = [c for c in self.checks["ai_cliche_detector"] if c in body_lower]
        if found_cliches:
            errors.append(f"AI clichés detected: {', '.join(found_cliches)}")

        # Duplicate intro patterns
        for pattern in self.checks["duplicate_intro_patterns"]:
            if body_lower.startswith(pattern.lower()):
                errors.append(f"Generic intro pattern: {pattern}")

        # Frontmatter validation
        if "title" not in frontmatter:
            errors.append("Missing frontmatter: title")
        if "slug" not in frontmatter:
            errors.append("Missing frontmatter: slug")
        if "description" not in frontmatter:
            errors.append("Missing frontmatter: description")

        description = frontmatter.get("description", "")
        if len(description) > self.checks["description_max_chars"]:
            errors.append(
                f"Description too long: {len(description)} chars (max {self.checks['description_max_chars']})"
            )

        if errors:
            self._log_failure(term, " | ".join(errors))
            return False, errors

        return True, []
