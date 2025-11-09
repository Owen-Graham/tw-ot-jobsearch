"""
Test script to verify scraper works correctly
Run this before setting up the full automation
"""

import asyncio
import json
import logging
from pathlib import Path

from scraper import JobScraper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main():
    """Test the scraper"""
    print("=" * 60)
    print("Testing Job Scraper")
    print("=" * 60)

    scraper = JobScraper()

    print("\n1. Fetching page with Playwright (headless=False)...")
    print("   (A browser window will open - you can watch the page load)")
    html = await scraper.fetch_page()

    if not html:
        print("❌ Failed to fetch page")
        return

    print(f"✓ Page fetched successfully ({len(html)} characters)")

    print("\n2. Parsing jobs from HTML...")
    jobs = scraper.parse_jobs(html)
    print(f"✓ Found {len(jobs)} total jobs")

    if jobs:
        print("\n   Sample of first 3 jobs:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n   Job {i}:")
            print(f"     Title: {job.get('title', 'N/A')[:60]}")
            print(f"     Location: {job.get('location', 'N/A')}")
            print(f"     Organization: {job.get('organization', 'N/A')}")
            print(f"     Start Date: {job.get('start_date', 'N/A')}")

    print("\n3. Filtering jobs based on criteria...")
    print("   Criteria:")
    print("     - Location: Taipei, New Taipei, Taoyuan")
    print("     - Exclude: pediatric (小兒/小兒自費)")
    print("     - Start date: >= 2026-02-20")

    filtered = scraper.filter_jobs(jobs)
    print(f"✓ Filtered to {len(filtered)} matching jobs")

    if filtered:
        print("\n   Matching jobs:")
        for i, job in enumerate(filtered, 1):
            print(f"\n   Job {i}:")
            print(f"     Title: {job.get('title', 'N/A')[:60]}")
            print(f"     Location: {job.get('location', 'N/A')}")
            print(f"     Organization: {job.get('organization', 'N/A')}")
            print(f"     Start Date: {job.get('start_date', 'N/A')}")
            print(f"     URL: {job.get('url', 'N/A')}")

        # Save results to file for inspection
        output_file = Path("test_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Results saved to {output_file}")
    else:
        print("\n   No matching jobs found")
        print("\n   All jobs found:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n   Job {i}:")
            print(f"     Title: {job.get('title', 'N/A')[:60]}")
            print(f"     Location: {job.get('location', 'N/A')}")
            print(f"     Start Date: {job.get('start_date', 'N/A')}")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
