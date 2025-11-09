"""
Record pagination actions to a file for analysis
User demonstrates, script records what selectors/actions are involved
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
import logging

# Set up file logging
log_file = "pagination_record.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


async def record_pagination():
    """Record pagination HTML and element details to file"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        page_count = 0
        previous_html = None

        try:
            logger.info("=" * 100)
            logger.info("PAGINATION RECORDING STARTED")
            logger.info("=" * 100)
            logger.info("Browser opened. Navigate through pages and I'll record everything.")
            logger.info("Instructions:")
            logger.info("  1. Look at the page and find the '>' button")
            logger.info("  2. Click it to go to next page")
            logger.info("  3. Wait for page to load")
            logger.info("  4. Repeat until you can't click anymore")
            logger.info("  5. Press Ctrl+C when done")
            logger.info("")

            await page.goto("https://www.oturoc.org.tw/index.php?action=recruit",
                          wait_until='networkidle')
            await page.wait_for_timeout(2000)

            while True:
                page_count += 1
                logger.info(f"\n{'='*100}")
                logger.info(f"PAGE #{page_count} - RECORDING")
                logger.info(f"{'='*100}")

                # Wait for user input with timeout - they'll click the button
                logger.info(f"Waiting for you to click the '>' button or Ctrl+C to stop...")
                logger.info(f"Current URL: {page.url}")

                # Get current HTML
                html = await page.content()

                # Check if content changed
                if previous_html == html:
                    logger.info("⚠️  CONTENT DID NOT CHANGE - We've reached the end or same page")
                    logger.info("This is the signal to STOP pagination!")
                    break

                previous_html = html

                # Save HTML to file
                html_file = f"page_{page_count}_raw.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                logger.info(f"✓ Saved HTML to: {html_file}")

                # Get all pagination-related elements
                logger.info("\nSearching for pagination controls...")

                # Look for any links that might be next button
                all_links = await page.query_selector_all("a")
                logger.info(f"Total links on page: {len(all_links)}")

                # Log details about each link
                for i, link in enumerate(all_links):
                    try:
                        text = await link.inner_text()
                        href = await link.get_attribute("href")
                        classes = await link.get_attribute("class")
                        onclick = await link.get_attribute("onclick")

                        if text and (text.strip() == ">" or text.strip() == "next" or "next" in str(onclick).lower()):
                            logger.info(f"\n🔍 FOUND POTENTIAL NEXT BUTTON (Link #{i}):")
                            logger.info(f"   Text: '{text}'")
                            logger.info(f"   href: {href}")
                            logger.info(f"   class: {classes}")
                            logger.info(f"   onclick: {onclick}")
                            html_elem = await link.evaluate("el => el.outerHTML")
                            logger.info(f"   HTML: {html_elem}")
                            logger.info(f"   This might be what you need to click!")
                    except:
                        pass

                logger.info(f"\n💡 Now you should click the '>' button...")
                logger.info(f"   After clicking, wait ~3 seconds for page to load")
                logger.info(f"   Then press Enter in terminal or wait for automatic detection")

                # Wait for page to potentially change (user clicks button)
                await page.wait_for_timeout(4000)  # Wait 4 seconds for page load

        except KeyboardInterrupt:
            logger.info("\n" + "="*100)
            logger.info("RECORDING STOPPED BY USER (Ctrl+C)")
            logger.info("="*100)
            logger.info(f"\nRecorded {page_count} pages")
            logger.info(f"Check the following files for analysis:")
            logger.info(f"  - pagination_record.log (this file)")
            for i in range(1, page_count + 1):
                logger.info(f"  - page_{i}_raw.html")
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        finally:
            await browser.close()
            logger.info("Browser closed.")


if __name__ == "__main__":
    asyncio.run(record_pagination())
