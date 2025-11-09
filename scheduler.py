"""
Job scheduler - periodically checks for new job postings
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from scraper import JobScraper
from telegram_notifier import TelegramNotifier

logger = logging.getLogger(__name__)


class JobScheduler:
    """Schedules periodic job scraping and alerts"""

    def __init__(self, bot_token: str, chat_id: str, check_interval_minutes: int = 30):
        """
        Initialize the job scheduler

        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID
            check_interval_minutes: How often to check for jobs (in minutes)
        """
        self.scraper = JobScraper()
        self.notifier = TelegramNotifier(bot_token, chat_id)
        self.check_interval_minutes = check_interval_minutes
        self.scheduler = AsyncIOScheduler()

    async def check_and_alert(self):
        """Check for new jobs and send alerts"""
        try:
            logger.info(f"Running job check at {datetime.now()}")

            # Scrape jobs
            new_jobs = await self.scraper.scrape()

            if new_jobs:
                logger.info(f"Found {len(new_jobs)} new matching jobs!")
                await self.notifier.send_batch_alerts(new_jobs)
            else:
                logger.info("No new matching jobs found")

        except Exception as e:
            logger.error(f"Error during job check: {e}")
            # Optionally send error alert to Telegram
            try:
                await self.notifier.send_message(
                    f"⚠️ Error during job check: {str(e)}"
                )
            except:
                pass

    def start(self):
        """Start the scheduler"""
        logger.info(
            f"Starting job scheduler (check every {self.check_interval_minutes} minutes)"
        )

        # Add job to scheduler
        self.scheduler.add_job(
            self.check_and_alert,
            trigger=IntervalTrigger(minutes=self.check_interval_minutes),
            id='job_check',
            name='Check for new job postings',
            replace_existing=True
        )

        # Run immediately on startup
        asyncio.create_task(self.check_and_alert())

        self.scheduler.start()

    async def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping job scheduler")
        self.scheduler.shutdown()
