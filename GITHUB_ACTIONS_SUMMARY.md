# GitHub Actions Automation - Complete Summary

## What's Been Set Up

Your Taiwan OT Job Search Monitor is now configured to run **automatically every 6 hours** using GitHub Actions!

### The System

```
┌─────────────────────────────────────────────────────────┐
│         GitHub Actions (Cloud Automation)               │
│                                                         │
│  Every 6 hours (0:00, 6:00, 12:00, 18:00 UTC):        │
│                                                         │
│  1. Scrape all 9 pages of job listings               │
│  2. Find ~93 total jobs                              │
│  3. Filter by your criteria                          │
│  4. Translate to English                             │
│  5. Send Telegram alerts                             │
│  6. Track seen jobs (no duplicates)                  │
│                                                         │
│  Time per run: ~5 minutes                             │
│  Cost: FREE (on GitHub's free tier)                 │
└─────────────────────────────────────────────────────────┘
```

## Files Created/Modified

### Workflow Configuration
- **`.github/workflows/job-check.yml`** - GitHub Actions automation
  - Runs every 6 hours automatically
  - Can be manually triggered anytime
  - Handles dependency installation
  - Manages artifact caching

### Code Changes
- **`main.py`** - Updated to run single check (no scheduler needed)
  - `single_check()` function for GitHub Actions
  - `test_mode()` function for local testing
  - Proper error handling

- **`scraper.py`** - Enhanced pagination + CI detection
  - Auto-detects CI environment (GitHub Actions)
  - Runs in headless mode on GitHub (no browser window)
  - Runs with browser window locally

### Documentation
- **`SETUP_GITHUB_REPO.md`** - Complete setup guide (10 minutes)
- **`GITHUB_ACTIONS_SETUP.md`** - Detailed workflow explanation
- **`GITHUB_ACTIONS_QUICK_REFERENCE.md`** - Quick reference card

## How to Set It Up

### Quick Setup (10 minutes)

1. **Create private GitHub repo**
   ```
   https://github.com/new
   → Name: tw-ot-jobsearch
   → Private: YES
   → Create
   ```

2. **Add secrets**
   ```
   Settings → Secrets and variables → Actions
   → New secret
      Name: TELEGRAM_BOT_TOKEN
      Value: (your bot token)
   → New secret
      Name: TELEGRAM_CHAT_ID
      Value: (your chat ID)
   ```

3. **Push code**
   ```bash
   cd tw-ot-jobsearch
   git init
   git remote add origin https://github.com/YOUR_USERNAME/tw-ot-jobsearch.git
   git add .
   git commit -m "Initial: Taiwan OT Job Monitor with GitHub Actions"
   git push -u origin main
   ```

4. **Test it**
   ```
   Actions tab → "Check for New Job Postings"
   → "Run workflow"
   → Wait 2-5 minutes
   → Check Telegram
   ```

5. **Done!** It now runs automatically every 6 hours.

## Schedule

Runs automatically at these UTC times (every 6 hours):

| UTC Time | Taiwan Time | Your Local |
|----------|------------|-----------|
| 00:00 | 06:00 (6 AM) | TBD |
| 06:00 | 14:00 (2 PM) | TBD |
| 12:00 | 20:00 (8 PM) | TBD |
| 18:00 | 02:00 (2 AM next day) | TBD |

## What Each Run Does

1. **Scrapes Website** - Fetches all 9 pages
   - Uses Playwright with pagination
   - Clicks through ">" button 8 times
   - Waits 2.5 seconds between clicks

2. **Parses Jobs** - Extracts job data
   - Title, location, organization
   - Start date, employment type, salary

3. **Filters** - Applies your criteria
   - Location: Taipei, New Taipei, Taoyuan
   - Date range: Nov 1, 2025 - Apr 15, 2026
   - Excludes: Pediatric jobs

4. **Translates** - Converts to English
   - Uses free Google Translate API
   - Translates all fields
   - Caches results for speed

5. **Sends Alerts** - Telegram notifications
   - Only for NEW jobs (tracks seen jobs)
   - Bilingual format (Chinese + English)
   - Professional formatting

6. **Exits** - No continuous running
   - GitHub Actions automatically handles scheduling
   - Completes in ~5 minutes
   - Very efficient

## Cost Analysis

| Item | Cost | Notes |
|------|------|-------|
| GitHub (Free tier) | $0 | 2,000 min/month, using ~120 |
| Telegram | $0 | Free tier unlimited |
| Google Translate | $0 | Free tier (public API) |
| Playwright | $0 | Open source |
| **Total** | **$0** | ✅ Everything free! |

## Advantages of GitHub Actions

✅ **No Server Needed** - Runs on GitHub's servers
✅ **Always On** - Runs automatically even if your computer is off
✅ **Free** - Well within GitHub's free tier
✅ **Secure** - Secrets are encrypted, never logged
✅ **Scalable** - Can easily handle more checks
✅ **Version Control** - Code is tracked in git
✅ **Easy Updates** - Just push to update

## Local Development Still Works

You can still test locally with:

```bash
# Test mode (see all jobs)
python main.py --test

# Normal mode (see only new jobs)
python main.py
```

Local testing uses headless=False (shows browser)
GitHub Actions uses headless=True (no display)

## Monitoring

### View Recent Runs
1. Go to Actions tab
2. See "Check for New Job Postings"
3. Click any run to see details

### Check Logs
1. Click workflow run
2. Click "check-jobs" job
3. Expand "Run job check" step
4. See:
   - "Found X total jobs"
   - "Filtered to X matching jobs"
   - "Sent X/X messages"
   - Any errors

### Track Over Time
All runs are logged with timestamps:
- Which ran successfully
- When they ran
- How many jobs found
- Success/failure status

## Common Tasks

### Update Filters
```bash
# Edit scraper.py
nano scraper.py  # Change lines 31-34

# Test locally
python main.py --test

# Push to GitHub
git add scraper.py
git commit -m "Update filter criteria"
git push

# Next run uses new filters automatically
```

### Change Schedule
```bash
# Edit workflow
nano .github/workflows/job-check.yml

# Change cron expression (line 7)
# Examples:
#   Every 3 hours: 0 */3 * * *
#   Every 12 hours: 0 */12 * * *
#   Daily at 9 AM UTC: 0 9 * * *

git add .github/workflows/job-check.yml
git commit -m "Change schedule to every 3 hours"
git push
```

### Pause Checks Temporarily
1. Actions tab
2. Click workflow name
3. "..." menu
4. "Disable workflow"
5. To resume: "Enable workflow"

## Troubleshooting Quick Guide

| Problem | Check | Solution |
|---------|-------|----------|
| Not running at scheduled time | GitHub Actions limits | Use "Run workflow" button instead |
| No messages received | Logs in Actions | Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID secrets |
| "No new jobs found" | Logs | Normal if no jobs match. Check logs to confirm it ran. |
| Workflow failed | Error message in logs | Read the error - usually missing secrets or timeout |

## Security

✅ **Secrets are encrypted** - Never displayed in logs
✅ **Private repo** - Only you can see code
✅ **No credentials in git** - `.env` is in `.gitignore`
✅ **No logs saved** - Only 7-day artifact retention
✅ **Read-only to public** - Your repo is private

## Key Differences from Local Scheduler

| Feature | Local Scheduler | GitHub Actions |
|---------|-----------------|-----------------|
| Always on | No (needs computer) | Yes ✅ |
| Cost | Free | Free ✅ |
| Complexity | Moderate | Simple ✅ |
| Setup time | 5 min | 10 min ✅ |
| Monitoring | Logs | GitHub UI ✅ |
| Scaling | Limited | Easy ✅ |
| Reliability | Depends on computer | 99.9% ✅ |

## Next Steps

1. **Read:** `SETUP_GITHUB_REPO.md` (complete setup guide)
2. **Create:** Private GitHub repo
3. **Add:** Secrets (bot token, chat ID)
4. **Push:** Code to main branch
5. **Test:** Manual workflow run
6. **Monitor:** Check Actions tab
7. **Relax:** It runs automatically!

## Files You Need to Keep

**Essential in repository:**
- `.github/workflows/job-check.yml` - The automation
- `main.py` - Entry point
- `scraper.py` - Scraping logic
- `translator.py` - Translations
- `telegram_notifier.py` - Telegram integration
- `requirements.txt` - Dependencies

**Do NOT commit (in .gitignore):**
- `.env` - Your credentials
- `venv/` - Virtual environment
- `data/seen_jobs.json` - (refreshes each run)
- `*.log` - Log files

## Final Checklist

- [ ] Create private GitHub repo
- [ ] Add TELEGRAM_BOT_TOKEN secret
- [ ] Add TELEGRAM_CHAT_ID secret
- [ ] Push code to main branch
- [ ] Test workflow manually
- [ ] Verify Telegram receives alerts
- [ ] Check logs look good
- [ ] Monitor over first week
- [ ] Make any filter adjustments
- [ ] Enjoy automatic job alerts! 🎉

## Questions?

1. **Workflow not running:** Check Actions tab, use "Run workflow" button
2. **No messages:** Check logs in Actions, verify secret names
3. **Want to change schedule:** Edit cron in `.github/workflows/job-check.yml`
4. **Want to change filters:** Edit `scraper.py` and push
5. **Need to debug:** Check logs in Actions tab - very detailed!

---

**You're all set!** Your Taiwan OT Job Search Monitor will now automatically check for jobs every 6 hours without needing your computer running. 🚀
