"""
Main application for job posting monitor with Telegram alerts
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
import argparse

from scraper import JobScraper
from telegram_notifier import TelegramNotifier
from scheduler import JobScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from environment variables"""
    # Load from .env file if it exists
    from dotenv import load_dotenv
    load_dotenv()

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '30'))

    if not bot_token or not chat_id:
        raise ValueError(
            "Missing required environment variables:\n"
            "  - TELEGRAM_BOT_TOKEN\n"
            "  - TELEGRAM_CHAT_ID\n"
            "Set these in a .env file or as environment variables"
        )

    return {
        'bot_token': bot_token,
        'chat_id': chat_id,
        'check_interval': check_interval
    }


async def test_mode(bot_token: str, chat_id: str):
    """Test mode: scrape and send all jobs (regardless of seen status)"""
    try:
        logger.info("Running in TEST mode - scraping all jobs...")

        # Scrape jobs (all pages)
        scraper = JobScraper()
        html = await scraper.fetch_all_pages()

        if not html:
            logger.error("Failed to fetch pages")
            return

        logger.info("Parsing jobs...")
        jobs = scraper.parse_jobs(html)
        logger.info(f"Found {len(jobs)} total jobs")

        logger.info("Filtering jobs...")
        filtered_jobs = scraper.filter_jobs(jobs)
        logger.info(f"Filtered to {len(filtered_jobs)} matching jobs")

        if not filtered_jobs:
            logger.info("No matching jobs found")
            return

        # Add translations
        logger.info("Translating jobs to English...")
        from translator import JobTranslator
        translator = JobTranslator()
        translated_jobs = []
        for job in filtered_jobs:
            translated_job = await translator.translate_job(job)
            translated_jobs.append(translated_job)

        logger.info(f"Sending {len(translated_jobs)} jobs to Telegram...")

        # Send to Telegram
        notifier = TelegramNotifier(bot_token, chat_id)
        success_count = await notifier.send_batch_alerts(translated_jobs)

        logger.info(f"✓ Test mode completed! Sent {success_count}/{len(translated_jobs)} messages")

    except Exception as e:
        logger.error(f"Test mode error: {e}", exc_info=True)
        sys.exit(1)


async def single_check(bot_token: str, chat_id: str):
    """Run a single job check (used by GitHub Actions)"""
    try:
        logger.info("Running single job check...")

        scraper = JobScraper()
        html = await scraper.fetch_all_pages()

        if not html:
            logger.error("Failed to fetch pages")
            return

        logger.info("Parsing jobs...")
        jobs = scraper.parse_jobs(html)
        logger.info(f"Found {len(jobs)} total jobs")

        logger.info("Filtering jobs...")
        filtered_jobs = scraper.filter_jobs(jobs)
        logger.info(f"Filtered to {len(filtered_jobs)} matching jobs")

        if not filtered_jobs:
            logger.info("No new matching jobs found")
            return

        # Add translations
        logger.info("Translating jobs to English...")
        from translator import JobTranslator
        translator = JobTranslator()
        translated_jobs = []
        for job in filtered_jobs:
            translated_job = await translator.translate_job(job)
            translated_jobs.append(translated_job)

        logger.info(f"Sending {len(translated_jobs)} jobs to Telegram...")

        # Send to Telegram
        notifier = TelegramNotifier(bot_token, chat_id)
        success_count = await notifier.send_batch_alerts(translated_jobs)

        # Save seen jobs to prevent duplicates on next run
        scraper.save_seen_jobs(filtered_jobs)
        logger.info(f"Saved {len(filtered_jobs)} jobs as seen")

        logger.info(f"✓ Check completed! Sent {success_count}/{len(translated_jobs)} messages")

    except Exception as e:
        logger.error(f"Check error: {e}", exc_info=True)
        sys.exit(1)


async def show_listings(bot_token: str, chat_id: str):
    """Show all new listings in terminal with bilingual format"""
    try:
        logger.info("Fetching all matching job listings...")

        scraper = JobScraper()
        html = await scraper.fetch_all_pages()

        if not html:
            logger.error("Failed to fetch pages")
            return

        logger.info("Parsing jobs...")
        jobs = scraper.parse_jobs(html)
        logger.info(f"Found {len(jobs)} total jobs")

        logger.info("Filtering jobs...")
        filtered_jobs = scraper.filter_jobs(jobs)
        logger.info(f"Filtered to {len(filtered_jobs)} matching jobs\n")

        if not filtered_jobs:
            print("\n❌ No matching jobs found\n")
            return

        # Add translations
        logger.info("Translating jobs to English...")
        from translator import JobTranslator
        translator = JobTranslator()
        translated_jobs = []
        for job in filtered_jobs:
            translated_job = await translator.translate_job(job)
            translated_jobs.append(translated_job)

        # Display jobs in terminal with bilingual format
        print("\n" + "="*80)
        print(f"📋 Found {len(translated_jobs)} new job listings")
        print("="*80 + "\n")

        for idx, job in enumerate(translated_jobs, 1):
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

            print(f"[{idx}] 🇹🇼 新工作機會 | 🇺🇸 New Job Opportunity")
            print("-" * 80)

            print(f"職位 | Position:")
            print(f"  {title}")
            if title_en:
                print(f"  {title_en}")

            print(f"\n機構 | Organization:")
            print(f"  {organization}")
            if organization_en:
                print(f"  {organization_en}")

            print(f"\n地點 | Location:")
            print(f"  {location}")
            if location_en:
                print(f"  {location_en}")

            print(f"\n開始日期 | Start Date: {start_date}")

            print(f"\n職位類型 | Employment Type:")
            print(f"  {employment_type}")
            if employment_type_en:
                print(f"  {employment_type_en}")

            print(f"\n薪資 | Salary:")
            print(f"  {salary}")
            if salary_en:
                print(f"  {salary_en}")

            print(f"\n🔗 Link: {url}")
            print("\n" + "="*80 + "\n")

        print(f"✓ Display completed! Total listings: {len(translated_jobs)}\n")

    except Exception as e:
        logger.error(f"Show listings error: {e}", exc_info=True)
        sys.exit(1)


async def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='Taiwan OT Job Search Monitor with Telegram alerts'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: scrape and send all jobs (ignoring seen status)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show all new listings in terminal with bilingual format (Chinese + English)'
    )
    args = parser.parse_args()

    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Test Telegram connection
        notifier = TelegramNotifier(config['bot_token'], config['chat_id'])
        if not notifier.test_connection():
            logger.error("Failed to connect to Telegram. Check your bot token and chat ID.")
            sys.exit(1)

        # Run in show mode if --show flag is provided
        if args.show:
            await show_listings(config['bot_token'], config['chat_id'])
            return

        # Run in test mode if --test flag is provided
        if args.test:
            await test_mode(config['bot_token'], config['chat_id'])
            return

        # Normal operation: run single check (suitable for GitHub Actions)
        await single_check(config['bot_token'], config['chat_id'])

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
