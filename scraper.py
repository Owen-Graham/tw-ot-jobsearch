"""
Web scraper for job postings from oturoc.org.tw using Playwright
Filters and sends Telegram alerts for matching positions
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime, date
import json
import os
from pathlib import Path
import re
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobScraper:
    """Scrapes job postings from oturoc.org.tw using Playwright"""

    URL = "https://www.oturoc.org.tw/index.php?action=recruit"

    # Filter criteria
    TARGET_LOCATIONS = {"台北", "臺北", "新北", "新北市", "台北市", "桃園", "桃園市"}
    EXCLUDE_KEYWORDS = {"小兒", "小兒自費", "pediatric"}
    TARGET_START_DATE_MIN = date(2026, 2, 15)  # Feb 15, 2026
    TARGET_START_DATE_MAX = date(2026, 4, 15)  # Apr 15, 2026

    # File to track seen job IDs
    SEEN_JOBS_FILE = Path("data/seen_jobs.json")

    def __init__(self):
        self.SEEN_JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.seen_jobs = self._load_seen_jobs()

    async def fetch_all_pages(self) -> Optional[str]:
        """Fetch all job postings pages using Playwright by clicking through pagination"""
        import os
        # Detect if running in CI environment (GitHub Actions, etc.)
        is_ci = os.getenv('CI') or os.getenv('GITHUB_ACTIONS')
        headless_mode = True if is_ci else False

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless_mode)
            page = await browser.new_page()

            try:
                await page.goto(self.URL, wait_until='networkidle')
                await page.wait_for_timeout(2000)

                all_html = []
                page_num = 1
                previous_html = None

                while True:
                    logger.info(f"Fetching page {page_num}...")
                    current_html = await page.content()

                    # Check if content changed from previous page
                    if previous_html == current_html:
                        logger.info(f"Content unchanged - reached end of pagination")
                        break

                    all_html.append(current_html)
                    previous_html = current_html

                    # Try to find and click the next button
                    next_button = await page.query_selector("a.arrow.next")

                    if not next_button:
                        logger.info(f"No next button found - reached last page")
                        break

                    # Click next button
                    logger.info(f"Clicking next button to go to page {page_num + 1}...")
                    await next_button.click()

                    # Wait for page to load
                    await page.wait_for_timeout(2500)

                    page_num += 1

                await browser.close()

                # Combine all HTML pages into one
                if all_html:
                    combined_html = all_html[0]  # Start with first page
                    # For additional pages, extract just the job items and append
                    for html in all_html[1:]:
                        combined_html += html
                    return combined_html
                else:
                    return None

            except Exception as e:
                logger.error(f"Failed to fetch pages: {e}")
                await browser.close()
                return None

    def parse_jobs(self, html: str) -> List[Dict]:
        """Parse job postings from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []

        # Find all job items - look for common patterns
        job_items = soup.find_all('div', class_=re.compile(r'recruit|job', re.I))

        logger.debug(f"Found {len(job_items)} potential job elements")

        for item in job_items:
            try:
                job = self._extract_job_info(item)
                if job and job.get('title'):  # Only add if we got a title
                    jobs.append(job)
            except Exception as e:
                logger.debug(f"Failed to extract job info: {e}")
                continue

        logger.info(f"Found {len(jobs)} total job postings")
        return jobs

    def _extract_job_info(self, item) -> Optional[Dict]:
        """Extract information from a job posting element"""
        job = {}

        # Try to find title - look in common places
        title_elem = None
        for selector in [['h3', 'h4', 'h2'], ['span', 'a']]:
            for tag in selector:
                candidates = item.find_all(tag)
                for candidate in candidates:
                    text = candidate.get_text(strip=True)
                    if len(text) > 5 and len(text) < 100:  # Reasonable title length
                        title_elem = candidate
                        break
                if title_elem:
                    break
            if title_elem:
                break

        job['title'] = title_elem.get_text(strip=True) if title_elem else item.get_text(strip=True)[:50]

        # Extract all text for comprehensive filtering
        job['full_text'] = item.get_text(separator=' ', strip=True).lower()

        # Try to extract location - often contains Taiwan region names
        location_match = re.search(r'(台北|臺北|新北|桃園|新北市|台北市|桃園市)', job['full_text'])
        job['location'] = location_match.group(0) if location_match else ""

        # Extract organization - usually before job title or in parent elements
        org_lines = []
        for text in job['full_text'].split():
            if len(text) > 2 and not any(keyword in text for keyword in ['職', '助理', '治療', '護理']):
                org_lines.append(text)
        job['organization'] = org_lines[0] if org_lines else ""

        # Extract start date - look for date patterns
        date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', job['full_text'])
        job['start_date'] = date_match.group(0) if date_match else ""

        # Extract employment type
        job['employment_type'] = "正職" if "正職" in job['full_text'] else ""

        # Extract salary if present
        salary_match = re.search(r'[\d,]+.*?[\d,]+', job['full_text'])
        job['salary'] = salary_match.group(0) if salary_match else ""

        job['url'] = self.URL

        # Generate unique hash ID from all job fields
        job['id'] = self._generate_job_id(job)

        return job

    def _generate_job_id(self, job_dict: Dict) -> str:
        """Generate a unique hash ID from the entire job posting for maximum uniqueness"""
        import hashlib
        # Create a deterministic string from all job fields
        job_string = json.dumps(job_dict, sort_keys=True, ensure_ascii=False)
        # Hash it for a compact, unique identifier
        job_hash = hashlib.sha256(job_string.encode('utf-8')).hexdigest()[:16]
        return job_hash

    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on criteria"""
        filtered = []

        for job in jobs:
            # Skip if already seen
            if job['id'] in self.seen_jobs:
                logger.debug(f"Skipping already seen job: {job['title']}")
                continue

            # Check location
            location = job['location'].lower()
            location_match = any(loc.lower() in location for loc in self.TARGET_LOCATIONS)

            if not location_match:
                logger.debug(f"Filtered out (location): {job['title']} - {job['location']}")
                continue

            # Check pediatric exclusion
            full_text = job['full_text']
            has_excluded = any(keyword in full_text for keyword in self.EXCLUDE_KEYWORDS)

            if has_excluded:
                logger.debug(f"Filtered out (pediatric): {job['title']}")
                continue

            # Check start date
            if not self._check_start_date(job['start_date']):
                logger.debug(f"Filtered out (start date): {job['title']} - {job['start_date']}")
                continue

            filtered.append(job)

        logger.info(f"Filtered to {len(filtered)} matching job postings")
        return filtered

    def get_new_unmatched_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Get newly posted jobs that don't match criteria but haven't been seen before"""
        new_unmatched = []

        for job in jobs:
            # Skip if already seen
            if job['id'] in self.seen_jobs:
                continue

            # Check location
            location = job['location'].lower()
            location_match = any(loc.lower() in location for loc in self.TARGET_LOCATIONS)

            # Check pediatric exclusion
            full_text = job['full_text']
            has_excluded = any(keyword in full_text for keyword in self.EXCLUDE_KEYWORDS)

            # Check start date
            date_ok = self._check_start_date(job['start_date'])

            # Include if it's new AND doesn't match the criteria
            # (i.e., fails at least one filter)
            if not (location_match and not has_excluded and date_ok):
                new_unmatched.append(job)

        logger.info(f"Found {len(new_unmatched)} new unmatched job postings")
        return new_unmatched

    def _check_start_date(self, date_text: str) -> bool:
        """Check if job start date is within target range (Feb 14 - Apr 15, 2026)"""
        if not date_text:
            return True  # Accept if date not found

        try:
            patterns = [
                r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # 2026/2/20 or 2026-02-20
            ]

            for pattern in patterns:
                match = re.search(pattern, date_text)
                if match:
                    groups = match.groups()
                    year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                    job_date = date(year, month, day)
                    # Check if date is within range
                    return self.TARGET_START_DATE_MIN <= job_date <= self.TARGET_START_DATE_MAX
        except (ValueError, IndexError) as e:
            logger.debug(f"Could not parse date '{date_text}': {e}")
            return True

        return True

    def _load_seen_jobs(self) -> set:
        """Load previously seen job IDs"""
        if self.SEEN_JOBS_FILE.exists():
            try:
                with open(self.SEEN_JOBS_FILE, 'r') as f:
                    return set(json.load(f))
            except Exception as e:
                logger.warning(f"Failed to load seen jobs: {e}")
        return set()

    def save_seen_jobs(self, jobs: List[Dict]):
        """Save job IDs to prevent duplicate alerts"""
        self.seen_jobs.update(job['id'] for job in jobs)
        try:
            with open(self.SEEN_JOBS_FILE, 'w') as f:
                json.dump(list(self.seen_jobs), f)
        except Exception as e:
            logger.error(f"Failed to save seen jobs: {e}")

    async def scrape(self, translate: bool = True) -> List[Dict]:
        """
        Run the complete scraping process

        Args:
            translate: Whether to translate jobs to English (default: True)

        Returns:
            List of filtered jobs with optional translations
        """
        logger.info("Starting job scraping...")

        html = await self.fetch_all_pages()
        if not html:
            return []

        jobs = self.parse_jobs(html)
        filtered_jobs = self.filter_jobs(jobs)
        self.save_seen_jobs(jobs)  # Mark all as seen to avoid duplicates

        # Add translations if requested
        if translate:
            from translator import JobTranslator
            translator = JobTranslator()
            translated_jobs = []
            for job in filtered_jobs:
                translated_job = await translator.translate_job(job)
                translated_jobs.append(translated_job)
            return translated_jobs

        return filtered_jobs
