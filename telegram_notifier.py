"""
Telegram notification module for job alerts
"""

import logging
from typing import List, Dict, Optional
import httpx

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Sends job alerts via Telegram bot"""

    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier

        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Telegram chat ID or channel ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    async def send_job_alert(self, job: Dict) -> bool:
        """
        Send a job posting alert via Telegram

        Args:
            job: Job posting dictionary with title, location, etc.

        Returns:
            True if message sent successfully
        """
        message = self._format_job_message(job)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    },
                    timeout=10
                )
                response.raise_for_status()
                logger.info(f"Telegram message sent for: {job['title']}")
                return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    async def send_batch_alerts(self, jobs: List[Dict]) -> int:
        """
        Send alerts for multiple jobs

        Args:
            jobs: List of job postings

        Returns:
            Number of successfully sent messages
        """
        success_count = 0

        for job in jobs:
            if await self.send_job_alert(job):
                success_count += 1

        logger.info(f"Sent {success_count}/{len(jobs)} job alerts")
        return success_count

    async def send_unmatched_summary(self, jobs: List[Dict]) -> bool:
        """
        Send a summary of newly posted jobs that don't match criteria

        Args:
            jobs: List of unmatched job postings

        Returns:
            True if message sent successfully
        """
        if not jobs:
            return True

        message = self._format_unmatched_summary(jobs)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    },
                    timeout=10
                )
                response.raise_for_status()
                logger.info(f"Unmatched jobs summary sent: {len(jobs)} jobs")
                return True
        except Exception as e:
            logger.error(f"Failed to send unmatched summary: {e}")
            return False

    def _format_unmatched_summary(self, jobs: List[Dict]) -> str:
        """Format unmatched jobs into a brief summary message"""
        summary_lines = [
            "<b>📋 新發佈的職位摘要 | New Posted Jobs Summary</b>",
            "<i>(不符合篩選條件 | Does not match filter criteria)</i>",
            ""
        ]

        for idx, job in enumerate(jobs[:20], 1):  # Limit to first 20 to avoid message too long
            title = job.get('title', 'Unknown')
            location = job.get('location', 'N/A')
            start_date = job.get('start_date', 'N/A')
            job_id = job.get('id', 'N/A')

            summary_lines.append(f"{idx}. {title}")
            summary_lines.append(f"   📍 {location} | 📅 {start_date}")
            summary_lines.append(f"   🔗 ID: <code>{job_id}</code>")
            summary_lines.append("")

        if len(jobs) > 20:
            summary_lines.append(f"<i>... 及其他 {len(jobs) - 20} 筆職位 | ... and {len(jobs) - 20} more jobs</i>")

        message = "\n".join(summary_lines)
        return message

    def _format_job_message(self, job: Dict) -> str:
        """Format job data into a Telegram message with Chinese and English"""
        title = job.get('title', 'Unknown')
        title_en = job.get('title_en', '')
        location = job.get('location', 'N/A')
        location_en = job.get('location_en', '')
        organization = job.get('organization', 'N/A')
        organization_en = job.get('organization_en', '')
        start_date = job.get('start_date', 'N/A')
        employment_type = job.get('employment_type', 'N/A')
        employment_type_en = job.get('employment_type_en', '')
        salary = job.get('salary', 'N/A')
        salary_en = job.get('salary_en', '')
        url = job.get('url', '')
        job_id = job.get('id', 'N/A')

        # Build message with Chinese and English
        message = f"""<b>🇹🇼 新工作機會！ | 🇺🇸 New Job Opportunity!</b>

<b>職位 | Position:</b>
{title}
{title_en if title_en else ''}

<b>地點 | Location:</b>
{location} {location_en if location_en else ''}

<b>機構 | Organization:</b>
{organization}
{organization_en if organization_en else ''}

<b>開始日期 | Start Date:</b> {start_date}

<b>職位類型 | Employment Type:</b>
{employment_type} {employment_type_en if employment_type_en else ''}

<b>薪資 | Salary:</b>
{salary}
{salary_en if salary_en else ''}

<a href="{url}">查看詳情 | View Details</a>

<code>Job ID: {job_id}</code>
"""
        return message

    def test_connection(self) -> bool:
        """Test if the Telegram bot token is valid"""
        try:
            import httpx
            response = httpx.get(f"{self.base_url}/getMe", timeout=10)
            response.raise_for_status()
            logger.info("Telegram bot connection successful")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False
