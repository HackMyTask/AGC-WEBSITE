import os
import logging
import requests
from typing import Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)

        if self.enabled:
            logger.info("Telegram notifications enabled")
        else:
            logger.warning("Telegram notifications disabled (missing BOT_TOKEN or CHAT_ID)")

    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send message to Telegram."""
        if not self.enabled:
            return False

        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode,
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram notification sent")
                return True
            else:
                logger.error(f"Telegram error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    def notify_generation_start(self, batch_size: int, priority: Optional[int] = None):
        """Notify generation started."""
        priority_text = f" (Priority {priority})" if priority else ""
        message = f"""
🚀 <b>Content Generation Started</b>

📊 Batch Size: {batch_size} articles{priority_text}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_generation_success(self, generated_count: int, total_batch: int, tokens_used: int):
        """Notify generation completed successfully."""
        success_rate = (generated_count / total_batch * 100) if total_batch > 0 else 0
        message = f"""
✅ <b>Content Generation Completed</b>

📝 Articles Generated: {generated_count}/{total_batch}
📊 Success Rate: {success_rate:.1f}%
🔑 Tokens Used: {tokens_used}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_generation_failure(self, error_message: str, batch_size: int):
        """Notify generation failed."""
        message = f"""
❌ <b>Content Generation Failed</b>

📊 Batch Size: {batch_size} articles
❗ Error: {error_message}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_quality_failures(self, failure_count: int, failures: list):
        """Notify quality gate failures."""
        failures_text = "\n".join([f"• {f}" for f in failures[:5]])
        if len(failures) > 5:
            failures_text += f"\n• ... and {len(failures) - 5} more"

        message = f"""
⚠️ <b>Quality Gate Failures</b>

❌ Failed Articles: {failure_count}

{failures_text}

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_api_rotation(self, provider: str, old_index: int, new_index: int, reason: str):
        """Notify API key rotation."""
        message = f"""
🔄 <b>API Key Rotated</b>

🔑 Provider: {provider}
📍 Key: {old_index} → {new_index}
📌 Reason: {reason}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_deployment_start(self):
        """Notify deployment started."""
        message = f"""
🚀 <b>Deployment Started</b>

📦 Building Astro site...
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_deployment_success(self, url: str = "https://ai-glossary.pages.dev"):
        """Notify deployment completed."""
        message = f"""
✅ <b>Deployment Completed</b>

🌐 Site: <a href="{url}">AI Glossary</a>
📍 Platform: Cloudflare Pages
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_deployment_failure(self, error_message: str):
        """Notify deployment failed."""
        message = f"""
❌ <b>Deployment Failed</b>

❗ Error: {error_message}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)

    def notify_daily_summary(self, stats: dict):
        """Notify daily generation summary."""
        message = f"""
📊 <b>Daily Generation Summary</b>

✅ Generated: {stats.get('generated', 0)} articles
❌ Failed: {stats.get('failed', 0)} articles
🔑 Tokens Used: {stats.get('tokens', 0)}
🔄 API Rotations: {stats.get('rotations', 0)}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        self.send_message(message)
