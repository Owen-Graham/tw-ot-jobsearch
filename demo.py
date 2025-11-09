"""
Interactive demo script to show pagination navigation
User can navigate the browser and we'll capture actions
"""

import asyncio
from playwright.async_api import async_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_navigation():
    """Open browser in interactive mode for demonstration"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Set larger viewport for better visibility
        await page.set_viewport_size({"width": 1400, "height": 900})

        try:
            logger.info("Opening job listing website...")
            await page.goto("https://www.oturoc.org.tw/index.php?action=recruit",
                          wait_until='networkidle')

            logger.info("=" * 80)
            logger.info("BROWSER OPENED - Now navigate manually!")
            logger.info("=" * 80)
            logger.info("")
            logger.info("Instructions:")
            logger.info("  1. Look at the bottom of the page for the '>' (next page) button")
            logger.info("  2. Click it to go to the next page")
            logger.info("  3. Keep clicking until you reach the last page")
            logger.info("  4. Tell me:")
            logger.info("     - Where is the '>' button located?")
            logger.info("     - What does it look like? (color, text, etc)")
            logger.info("     - How does the page change when you click it?")
            logger.info("     - When do you stop seeing the '>' button?")
            logger.info("")
            logger.info("Close the browser window when done demonstrating.")
            logger.info("=" * 80)

            # Keep browser open - press Ctrl+C in terminal to stop
            logger.info("Browser will stay open. Navigate and demonstrate pagination.")
            logger.info("Press Ctrl+C in the terminal when done.")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("\nClosing browser...")

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            try:
                await browser.close()
            except:
                pass
            logger.info("Browser closed.")


if __name__ == "__main__":
    asyncio.run(demo_navigation())
