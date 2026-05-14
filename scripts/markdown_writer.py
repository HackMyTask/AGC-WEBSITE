import os
import hashlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownWriter:
    def __init__(self):
        self.write_log = "logs/writes.log"
        self._ensure_log_file()

    def _ensure_log_file(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.write_log):
            open(self.write_log, "w").close()

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _log_write(self, filepath: str, status: str):
        with open(self.write_log, "a") as f:
            f.write(f"{filepath} | {status}\n")

    def write(self, slug: str, content: str) -> bool:
        """Write markdown file with safety checks. Returns True if written, False if skipped."""
        filepath = f"src/content/glossary/{slug}.md"

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Validate frontmatter
        if not self._validate_frontmatter(content):
            logger.error(f"Invalid frontmatter for {slug}")
            self._log_write(filepath, "FAILED_INVALID_FRONTMATTER")
            return False

        # Check if file exists and compare hash
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing_content = f.read()

            existing_hash = self._compute_hash(existing_content)
            new_hash = self._compute_hash(content)

            if existing_hash == new_hash:
                logger.info(f"Skipping {slug}: content unchanged")
                self._log_write(filepath, "SKIPPED_IDENTICAL")
                return False

        # Atomic write: write to temp file first
        temp_filepath = f"{filepath}.tmp"
        try:
            with open(temp_filepath, "w", encoding="utf-8") as f:
                f.write(content)

            # Rename temp to final
            os.replace(temp_filepath, filepath)
            logger.info(f"Wrote {filepath}")
            self._log_write(filepath, "WRITTEN")
            return True
        except Exception as e:
            logger.error(f"Failed to write {filepath}: {e}")
            self._log_write(filepath, f"FAILED_{str(e)}")
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return False

    def _validate_frontmatter(self, content: str) -> bool:
        """Validate frontmatter is valid YAML-like format."""
        if not content.startswith("---"):
            return False

        parts = content.split("---")
        if len(parts) < 3:
            return False

        frontmatter_text = parts[1].strip()
        required_keys = ["title", "slug", "description", "keywords", "cluster"]

        for key in required_keys:
            if f"{key}:" not in frontmatter_text:
                return False

        return True
