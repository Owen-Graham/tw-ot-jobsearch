# Taiwan OT Job Search Monitor

Automated job posting monitor for occupational therapy positions in Taiwan with Telegram alerts.

## Features

- Scrapes job postings from https://www.oturoc.org.tw/index.php?action=recruit
- Filters jobs by:
  - Location: Taipei, New Taipei, Taoyuan
  - Excludes pediatric positions (小兒/小兒自費)
  - Start date: February 14 - April 15, 2026
- **Automatic English translations** of all job postings
- Sends Telegram notifications for matching jobs with bilingual content
- **Test mode** (`--test` flag) to preview all jobs before enabling automation
- Runs on a configurable schedule
- Uses Playwright for reliable web scraping (headless=False mode)

## Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 2. Set Up Telegram Bot

1. Open Telegram and search for @BotFather
2. Send `/start` and follow the prompts
3. Send `/newbot` to create a new bot
4. Choose a name and username for your bot
5. Copy the bot token (you'll need this)

### 3. Get Your Chat ID

1. Search for @userinfobot on Telegram
2. Send it any message
3. It will reply with your chat ID
4. Or use the bot you created and send it a message, then run:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Look for the `chat.id` value

### 4. Configure Environment

Copy the example config file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and fill in:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
CHECK_INTERVAL_MINUTES=30
```

### 5. Test the Scraper

Before running the full automation, test that the scraper works:

```bash
python test_scraper.py
```

This will:
- Open a browser window (you can watch it work)
- Scrape the job posting website
- Show filtered results
- Save results to `test_results.json`

### 6. Test Mode (Optional but Recommended)

Before enabling automatic monitoring, preview what jobs will be sent:

```bash
python main.py --test
```

This will:
- Scrape all matching jobs
- Translate them to English
- Send them all to Telegram (bypassing the "seen jobs" filter)
- Help you verify the filters are working correctly

### 7. Run the Application

```bash
python main.py
```

The application will:
1. Test the Telegram connection
2. Check for jobs immediately
3. Schedule periodic checks (default: every 30 minutes)
4. Send alerts to Telegram for matching jobs with English translations
5. Log all activity to `job_monitor.log`

## File Structure

```
tw_ot_jobsearch/
├── main.py              # Main application entry point (with --test flag)
├── scraper.py           # Job scraping logic using Playwright
├── telegram_notifier.py # Telegram integration with bilingual messages
├── translator.py        # English translation module (using Google Translate)
├── scheduler.py         # Periodic job checking
├── test_scraper.py      # Testing script
├── requirements.txt     # Python dependencies
├── .env.example        # Configuration template
├── .env                # Configuration (create from .env.example)
├── data/
│   └── seen_jobs.json  # Tracks seen jobs (auto-created)
└── job_monitor.log     # Log file (auto-created)
```

## Configuration

Edit `CHECK_INTERVAL_MINUTES` in `.env` to control how often the scraper checks for new jobs:
- 5 = check every 5 minutes
- 30 = check every 30 minutes (default)
- 60 = check every hour

## Filter Criteria

The filters are defined in `scraper.py` and can be modified:

```python
TARGET_LOCATIONS = {"台北", "臺北", "新北", "新北市", "台北市", "桃園", "桃園市"}
EXCLUDE_KEYWORDS = {"小兒", "小兒自費", "pediatric"}
TARGET_START_DATE_MIN = date(2025, 11, 1)   # Nov 1, 2025
TARGET_START_DATE_MAX = date(2026, 4, 15)   # Apr 15, 2026
```

**Note:** The start date range is currently set to Nov 1, 2025 - Apr 15, 2026 to match current job postings on the website. You can adjust these dates to match your preferences.

## Translation

Jobs are automatically translated to English using Google Translate API. The translation includes:
- Job title
- Location
- Organization
- Employment type
- Salary

All translations are cached to improve performance on subsequent runs.

## Troubleshooting

### Browser doesn't open
- Make sure Playwright browsers are installed: `playwright install`
- Check that your display/X11 server is available (for headless=False)

### No jobs found
- Check if the website structure has changed
- Run `test_scraper.py` to see what's being scraped
- Inspect `test_results.json` for debugging

### Telegram messages not sending
- Verify bot token and chat ID in `.env`
- Run `python test_scraper.py` to test
- Check the Telegram bot has permission to send messages to the chat

### Jobs not updating
- Check `data/seen_jobs.json` - if it has many entries, clear it to reset tracking
- Verify `CHECK_INTERVAL_MINUTES` is set appropriately
- Check `job_monitor.log` for errors

## Advanced Usage

### Manual scrape and alert

```python
import asyncio
from scraper import JobScraper
from telegram_notifier import TelegramNotifier

async def manual_check():
    scraper = JobScraper()
    notifier = TelegramNotifier('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')

    jobs = await scraper.scrape()
    await notifier.send_batch_alerts(jobs)

asyncio.run(manual_check())
```

### Running as a service (Linux/Mac)

Create a systemd service file `/etc/systemd/system/job-monitor.service`:

```ini
[Unit]
Description=Taiwan OT Job Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/tw_ot_jobsearch
Environment="PATH=/path/to/tw_ot_jobsearch/venv/bin"
ExecStart=/path/to/tw_ot_jobsearch/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable job-monitor
sudo systemctl start job-monitor
sudo systemctl status job-monitor
```

## License

MIT
