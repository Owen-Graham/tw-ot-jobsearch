# Quick Start Guide

## 1. Get Telegram Credentials (5 minutes)

### Create a Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/start`, then `/newbot`
3. Follow the prompts:
   - Give your bot a display name (e.g., "OT Job Alert")
   - Give your bot a username (must end with "bot", e.g., "ot_job_alert_bot")
4. Copy the bot token you receive (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Get Your Chat ID
1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It replies with your chat ID (a number like `123456789`)

**OR** if you want notifications in a group/channel:
1. Add your bot to the group/channel
2. Send a message in that group
3. Run this in terminal (replace token):
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Look for the `chat.id` value

## 2. Configure the Application (2 minutes)

```bash
cd /home/owen/workspace/tw_ot_jobsearch
source venv/bin/activate
```

Edit the `.env` file with your credentials:
```bash
nano .env
```

Paste your values:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
CHECK_INTERVAL_MINUTES=30
```

Save (Ctrl+O, Enter, Ctrl+X)

## 3. Test the Scraper (5 minutes)

```bash
python test_scraper.py
```

This will:
- Open a browser window (headless=False, so you can see what it's doing)
- Scrape the job posting website
- Show you filtered results
- Save results to `test_results.json`

Check the results to make sure:
- It finds jobs
- The location filtering works (should show Taipei/New Taipei/Taoyuan only)
- Pediatric jobs are excluded
- Dates are between Feb 14 - Apr 15, 2026

## 4. Test Mode (Optional but Recommended!)

Before running the full automation, preview all matching jobs:

```bash
python main.py --test
```

This will:
- Scrape all matching jobs from the website
- Translate them to English
- Send them ALL to Telegram (bypassing the "seen jobs" filter)
- Help you verify the filters work correctly

This is useful to:
- See what kind of jobs you'll get alerts for
- Verify the location/date/pediatric filters are working
- Make sure the English translations look good

## 5. Run the Job Monitor

Once you're happy with the filters, start the automatic monitor:

```bash
python main.py
```

The application will:
1. Test the Telegram connection
2. Check for new jobs immediately
3. Send a Telegram alert for each NEW matching job (with English translation)
4. Schedule periodic checks (every 30 minutes by default)
5. Track jobs it's already seen (to avoid duplicate alerts)

Press Ctrl+C to stop the application.

## 6. Keep It Running (Optional)

To keep the application running 24/7, use a process manager like `tmux` or `screen`:

```bash
# Using tmux
tmux new-session -d -s job-monitor "cd /home/owen/workspace/tw_ot_jobsearch && source venv/bin/activate && python main.py"

# Check status
tmux ls

# View logs
tmux capture-pane -p -t job-monitor

# Stop
tmux kill-session -t job-monitor
```

Or use systemd (see README.md for details).

## Troubleshooting

### No jobs found
- The website might not have recent postings
- Check `test_results.json` to see what jobs exist
- Verify your filters match the actual job listings

### Telegram errors
- Double-check your bot token and chat ID in `.env`
- Make sure the bot has permission to send messages to the chat
- Test: `curl https://api.telegram.org/bot<TOKEN>/getMe`

### Browser doesn't open
- Ensure display is available (X11/Wayland)
- For headless operation, modify scraper.py to use `headless=True`

## Next Steps

- Monitor the logs: `tail -f job_monitor.log`
- Adjust CHECK_INTERVAL_MINUTES to change check frequency
- Modify filter criteria in `scraper.py` if needed
- Add more locations or change the start date as needed

Happy job hunting! 🎯
