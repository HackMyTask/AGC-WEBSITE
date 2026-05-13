import os
import time
import logging
from typing import Optional, List
from datetime import datetime
import anthropic
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "groq").lower()
        self.daily_limit = int(os.getenv("DAILY_LIMIT", "100"))
        self.tokens_used_today = 0
        self.log_file = "logs/usage.log"
        self.rotation_log = "logs/api_rotation.log"

        # Load API keys for rotation
        self.groq_keys = self._load_api_keys("GROQ_API_KEY")
        self.gemini_keys = self._load_api_keys("GEMINI_API_KEY")
        self.current_groq_index = 0
        self.current_gemini_index = 0

        self._ensure_log_file()

    def _load_api_keys(self, env_var: str) -> List[str]:
        """Load API keys from env var (comma-separated for multiple keys)."""
        keys_str = os.getenv(env_var, "")
        if not keys_str:
            return []
        # Support both comma-separated and pipe-separated
        keys = [k.strip() for k in keys_str.replace("|", ",").split(",") if k.strip()]
        if keys:
            logger.info(f"Loaded {len(keys)} {env_var} keys for rotation")
        return keys

    def _ensure_log_file(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            open(self.log_file, "w").close()
        if not os.path.exists(self.rotation_log):
            open(self.rotation_log, "w").close()

    def _log_usage(self, tokens: int, model: str, term: str, api_key_index: int = 0):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | {model} | {term} | tokens: {tokens} | key_index: {api_key_index}\n")
        self.tokens_used_today += tokens

    def _log_rotation(self, provider: str, old_index: int, new_index: int, reason: str):
        """Log API key rotation events."""
        timestamp = datetime.now().isoformat()
        with open(self.rotation_log, "a") as f:
            f.write(f"{timestamp} | {provider} | rotated from key {old_index} to {new_index} | reason: {reason}\n")
        logger.info(f"Rotated {provider} API key: {old_index} → {new_index} ({reason})")

    def _get_next_groq_key(self) -> tuple[str, int]:
        """Get next Groq API key in rotation."""
        if not self.groq_keys:
            raise ValueError("No Groq API keys configured")
        key = self.groq_keys[self.current_groq_index]
        return key, self.current_groq_index

    def _rotate_groq_key(self, reason: str = "rate_limit"):
        """Rotate to next Groq API key."""
        old_index = self.current_groq_index
        self.current_groq_index = (self.current_groq_index + 1) % len(self.groq_keys)
        self._log_rotation("Groq", old_index, self.current_groq_index, reason)

    def _get_next_gemini_key(self) -> tuple[str, int]:
        """Get next Gemini API key in rotation."""
        if not self.gemini_keys:
            raise ValueError("No Gemini API keys configured")
        key = self.gemini_keys[self.current_gemini_index]
        return key, self.current_gemini_index

    def _rotate_gemini_key(self, reason: str = "rate_limit"):
        """Rotate to next Gemini API key."""
        old_index = self.current_gemini_index
        self.current_gemini_index = (self.current_gemini_index + 1) % len(self.gemini_keys)
        self._log_rotation("Gemini", old_index, self.current_gemini_index, reason)

    def _check_daily_limit(self) -> bool:
        if self.tokens_used_today >= self.daily_limit:
            logger.warning(f"Daily limit ({self.daily_limit}) reached")
            return False
        return True

    def generate(
        self,
        prompt: str,
        term: str,
        model: Optional[str] = None,
        max_retries: int = 3,
    ) -> Optional[str]:
        """Generate content using configured AI provider with retry logic and API key rotation."""
        if not self._check_daily_limit():
            return None

        if self.provider == "groq":
            return self._generate_groq(prompt, term, model or "llama-3.3-70b-versatile", max_retries)
        elif self.provider == "gemini":
            return self._generate_gemini(prompt, term, model or "gemini-2.0-flash", max_retries)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _generate_groq(self, prompt: str, term: str, model: str, max_retries: int) -> Optional[str]:
        """Generate using Groq API with key rotation on rate limit."""
        if not self.groq_keys:
            # Fallback to single key from env
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set")
            return self._try_groq_generation(api_key, prompt, term, model, max_retries, 0)

        # Try with multiple keys on rate limit
        for key_attempt in range(len(self.groq_keys)):
            api_key, key_index = self._get_next_groq_key()

            result = self._try_groq_generation(api_key, prompt, term, model, max_retries, key_index)
            if result:
                return result

            # If failed, rotate to next key
            if key_attempt < len(self.groq_keys) - 1:
                self._rotate_groq_key("exhausted")
                logger.info(f"Trying next Groq API key...")

        logger.error(f"All Groq API keys exhausted for {term}")
        return None

    def _try_groq_generation(
        self, api_key: str, prompt: str, term: str, model: str, max_retries: int, key_index: int
    ) -> Optional[str]:
        """Try generation with single Groq API key."""
        client = anthropic.Anthropic(api_key=api_key, base_url="https://api.groq.com/openai/v1")

        for attempt in range(max_retries):
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text
                tokens = response.usage.output_tokens + response.usage.input_tokens
                self._log_usage(tokens, model, term, key_index)
                return content
            except Exception as e:
                error_str = str(e).lower()
                if "rate_limit" in error_str or "quota" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited on key {key_index}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.warning(f"Rate limit exceeded on key {key_index}, will try next key")
                        return None
                else:
                    logger.error(f"Generation failed on key {key_index}: {e}")
                    return None

    def _generate_gemini(self, prompt: str, term: str, model: str, max_retries: int) -> Optional[str]:
        """Generate using Google Gemini API with key rotation on rate limit."""
        if not self.gemini_keys:
            # Fallback to single key from env
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not set")
            return self._try_gemini_generation(api_key, prompt, term, model, max_retries, 0)

        # Try with multiple keys on rate limit
        for key_attempt in range(len(self.gemini_keys)):
            api_key, key_index = self._get_next_gemini_key()

            result = self._try_gemini_generation(api_key, prompt, term, model, max_retries, key_index)
            if result:
                return result

            # If failed, rotate to next key
            if key_attempt < len(self.gemini_keys) - 1:
                self._rotate_gemini_key("exhausted")
                logger.info(f"Trying next Gemini API key...")

        logger.error(f"All Gemini API keys exhausted for {term}")
        return None

    def _try_gemini_generation(
        self, api_key: str, prompt: str, term: str, model: str, max_retries: int, key_index: int
    ) -> Optional[str]:
        """Try generation with single Gemini API key."""
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)

        for attempt in range(max_retries):
            try:
                response = gemini_model.generate_content(prompt)
                content = response.text
                # Gemini doesn't expose token count in free tier, estimate
                estimated_tokens = len(content.split()) + len(prompt.split())
                self._log_usage(estimated_tokens, model, term, key_index)
                return content
            except Exception as e:
                error_str = str(e).lower()
                if "rate_limit" in error_str or "quota" in error_str or "resource_exhausted" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited on key {key_index}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.warning(f"Rate limit exceeded on key {key_index}, will try next key")
                        return None
                else:
                    logger.error(f"Generation failed on key {key_index}: {e}")
                    return None
