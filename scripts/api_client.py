import os
import time
import logging
from typing import Optional
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
        self._ensure_log_file()

    def _ensure_log_file(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            open(self.log_file, "w").close()

    def _log_usage(self, tokens: int, model: str, term: str):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | {model} | {term} | tokens: {tokens}\n")
        self.tokens_used_today += tokens

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
        """Generate content using configured AI provider with retry logic."""
        if not self._check_daily_limit():
            return None

        if self.provider == "groq":
            return self._generate_groq(prompt, term, model or "llama-3.3-70b-versatile", max_retries)
        elif self.provider == "gemini":
            return self._generate_gemini(prompt, term, model or "gemini-2.0-flash", max_retries)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _generate_groq(self, prompt: str, term: str, model: str, max_retries: int) -> Optional[str]:
        """Generate using Groq API."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

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
                self._log_usage(tokens, model, term)
                return content
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Generation failed: {e}")
                    return None

    def _generate_gemini(self, prompt: str, term: str, model: str, max_retries: int) -> Optional[str]:
        """Generate using Google Gemini API."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)

        for attempt in range(max_retries):
            try:
                response = gemini_model.generate_content(prompt)
                content = response.text
                # Gemini doesn't expose token count in free tier, estimate
                estimated_tokens = len(content.split()) + len(prompt.split())
                self._log_usage(estimated_tokens, model, term)
                return content
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Generation failed: {e}")
                    return None
