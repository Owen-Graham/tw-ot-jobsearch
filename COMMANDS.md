# Command Reference

## Activation

Before running any commands, activate the virtual environment:

```bash
cd /home/owen/workspace/tw_ot_jobsearch
source venv/bin/activate
```

## Main Commands

### Normal Operation

Start the job monitor with automatic scheduling:

```bash
python main.py
```

**What it does:**
- Connects to Telegram bot
- Checks for jobs immediately
- Schedules periodic checks (every 30 minutes by default)
- Sends alerts for NEW jobs only
- Logs to `job_monitor.log`

**Stop:** Press `Ctrl+C`

### Test Mode

Preview all matching jobs:

```bash
python main.py --test
```

**What it does:**
- Scrapes the job website
- Filters jobs based on criteria
- Translates to English
- Sends ALL matching jobs to Telegram
- Exits without starting the scheduler

**Use cases:**
- Verify filters are working
- Check translations
- See what jobs exist
- Preview alert format

### Help

Show command options:

```bash
python main.py --help
```

## Testing & Debugging

### Test the Scraper

Scrape and parse jobs (without Telegram):

```bash
python test_scraper.py
```

**Output:**
- Opens browser
- Shows parsing results
- Saves `test_results.json`
- Displays first 3-5 job examples

### Check Logs

View application logs:

```bash
tail -f job_monitor.log
```

Shows:
- Job checks
- Jobs found/filtered
- Telegram messages sent
- Errors and warnings

### View Seen Jobs

Check which jobs have been processed:

```bash
cat data/seen_jobs.json | python -m json.tool
```

Shows all job IDs the system has seen.

### Reset Tracking

Clear seen jobs (treat all as new next run):

```bash
rm data/seen_jobs.json
```

## Configuration

### Edit Settings

Update check interval and other settings:

```bash
nano .env
```

**Available settings:**
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_MINUTES=30
```

### Apply Changes

Most changes take effect on next restart:

```bash
# Stop current instance
Ctrl+C

# Restart
python main.py
```

## Process Management

### Using tmux (Recommended)

Create background session:

```bash
tmux new-session -d -s jobs "cd /home/owen/workspace/tw_ot_jobsearch && source venv/bin/activate && python main.py"
```

Check status:

```bash
tmux ls
```

View output:

```bash
tmux capture-pane -p -t jobs
```

Stop session:

```bash
tmux kill-session -t jobs
```

### Using screen

Create background session:

```bash
screen -S jobs
# Type: source venv/bin/activate && python main.py
# Press Ctrl+A then D to detach
```

Reattach:

```bash
screen -r jobs
```

## Maintenance

### Update Dependencies

If you change `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Reinstall Playwright Browsers

If browsers get corrupted:

```bash
playwright install --with-deps
```

### Check Python Syntax

Verify code before running:

```bash
python -m py_compile main.py scraper.py translator.py telegram_notifier.py
```

## Monitoring

### Check Application Status

While running:

```bash
ps aux | grep "python main.py"
```

Shows if the process is running.

### Monitor CPU/Memory

While running:

```bash
watch -n 5 'ps aux | grep "python main.py" | grep -v grep'
```

Updates every 5 seconds.

### Watch Telegram Messages

Monitor real-time alerts:

Open your Telegram chat and watch for incoming messages.

## Development

### Run Specific Functions

Test individual modules:

```python
# Test translator
python -c "from translator import JobTranslator; print(JobTranslator())"

# Test scraper
python -c "from scraper import JobScraper; print(JobScraper())"

# Test notifier
python -c "from telegram_notifier import TelegramNotifier; print(TelegramNotifier('test', 'test'))"
```

### Debug Mode

Enable verbose logging:

Edit `main.py` or `scraper.py` and change:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

## Common Workflows

### Initial Setup Workflow

```bash
# 1. Install dependencies
./setup.sh

# 2. Configure credentials
nano .env

# 3. Test scraper
python test_scraper.py

# 4. Test with all jobs
python main.py --test

# 5. Start automation
python main.py
```

### Daily Check Workflow

```bash
# Activate
source venv/bin/activate

# View recent logs
tail -20 job_monitor.log

# Check if running
ps aux | grep "python main.py"
```

### Reset Everything Workflow

```bash
# Stop current process
pkill -f "python main.py"

# Clear tracking
rm data/seen_jobs.json

# Start fresh
python main.py --test

# Then normal operation
python main.py
```

## Troubleshooting Commands

### Check Telegram Connection

```bash
# View error logs
grep "Telegram" job_monitor.log

# Test manual send
python -c "
from telegram_notifier import TelegramNotifier
import os
from dotenv import load_dotenv
load_dotenv()
n = TelegramNotifier(os.getenv('TELEGRAM_BOT_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
print(n.test_connection())
"
```

### Check Scraping

```bash
python test_scraper.py

# Or inspect raw output
python -c "
import asyncio
from scraper import JobScraper
async def test():
    s = JobScraper()
    html = await s.fetch_page()
    print(f'HTML length: {len(html) if html else 0}')
asyncio.run(test())
"
```

### View Database

```bash
# See tracked jobs
cat data/seen_jobs.json | wc -l  # Count

# See test results
cat test_results.json | python -m json.tool
```
