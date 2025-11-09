# 🚀 Taiwan OT Job Search Monitor - START HERE

Welcome! This system automatically finds and alerts you about occupational therapy jobs in Taiwan.

## What It Does

✅ Scrapes all job postings from https://www.oturoc.org.tw/
✅ Filters by location (Taipei, New Taipei, Taoyuan)
✅ Filters by date (Nov 2025 - Apr 2026)
✅ Excludes pediatric positions
✅ **Automatically translates to English**
✅ **Sends Telegram alerts** for new jobs
✅ **Runs every 6 hours** (no computer needed!)

## Quick Start (5 Minutes)

### Option A: GitHub Actions (Recommended - Automated)

```bash
# 1. Create private repo at https://github.com/new
#    Name: tw-ot-jobsearch
#    Select: Private

# 2. Add secrets (Settings → Secrets and variables → Actions)
#    TELEGRAM_BOT_TOKEN = your_bot_token
#    TELEGRAM_CHAT_ID = your_chat_id

# 3. Push code
git clone <your-repo-url>
cd tw-ot-jobsearch
git add .
git commit -m "Initial commit"
git push

# 4. Run workflow (Actions tab → Run workflow)

# 5. Check Telegram for alerts!
```

**Read:** `SETUP_GITHUB_REPO.md` for detailed instructions

### Option B: Local Testing

```bash
# Test mode (see all matching jobs)
python main.py --test

# Normal mode (see only new jobs)
python main.py
```

**Read:** `QUICK_START.md` for detailed local setup

## System Overview

```
Website (93 jobs) → Scraper → Parser → Filter (18 jobs)
                                          ↓
                                      Translator
                                          ↓
                                    Telegram (alerts)
                                          ↓
                                    Tracking (no duplicates)
```

**With GitHub Actions:**
- Runs every 6 hours automatically
- No computer needs to be on
- Completely free (on GitHub's free tier)
- Secure (credentials are encrypted)

## What You Need

- Telegram account & bot (5 minutes to set up)
- GitHub account (for automated version)
- Python 3.12+ (for local testing)

## First Steps

1. **Get Telegram credentials** (5 min)
   - Chat @BotFather on Telegram
   - Create bot, get token
   - Chat @userinfobot to get chat ID

2. **Choose your setup:**
   - **GitHub Actions (Recommended):** Read `SETUP_GITHUB_REPO.md`
   - **Local testing:** Read `QUICK_START.md`

3. **Test it works:**
   ```bash
   python main.py --test
   ```
   You should get Telegram alerts!

4. **Set it and forget it:**
   - GitHub Actions: Runs automatically every 6 hours
   - Local: You can run on your schedule

## Documentation

| Document | Purpose |
|----------|---------|
| `SETUP_GITHUB_REPO.md` | Complete GitHub Actions setup (10 min) |
| `QUICK_START.md` | Local setup and testing (15 min) |
| `GITHUB_ACTIONS_SUMMARY.md` | How GitHub Actions automation works |
| `GITHUB_ACTIONS_QUICK_REFERENCE.md` | Common tasks and troubleshooting |
| `README.md` | Full project documentation |
| `FEATURES.md` | Detailed feature explanations |

## Key Features

### 🌐 Multi-Page Scraping
- Scrapes all 9 pages of job listings
- Finds ~93 total jobs per check
- Automatically detects end of pagination

### 🇺🇸 Automatic Translation
- Every job translated to English
- Uses free Google Translate API
- No API key needed

### 💬 Telegram Alerts
- Bilingual format (Chinese + English)
- Only new jobs (tracks seen jobs)
- Professional formatting

### ⏰ Smart Scheduling
- Every 6 hours on GitHub Actions
- No server needed (runs on GitHub's servers)
- Works 24/7 automatically

### 🔐 Secure
- Credentials encrypted in GitHub
- Private repository
- No secrets in code

## How to Use

### First Time
1. Set up Telegram (5 min)
2. Set up GitHub Actions OR local environment (10 min)
3. Run test: `python main.py --test` (5 min)
4. Done! 🎉

### Updates
```bash
# Want to change filters?
nano scraper.py  # Edit lines 31-34
python main.py --test  # Test locally
git add .
git commit -m "Update filters"
git push  # GitHub Actions uses updated code next run
```

### Monitoring
- **GitHub Actions:** Check Actions tab to see runs
- **Local:** Check job_monitor.log file

## Example

When a new job matches your criteria, you get a Telegram alert like:

```
🇹🇼 新工作機會！ | 🇺🇸 New Job Opportunity!

職位 | Position:
臺北市立聯合醫院松德院區職能治療科
Taipei Veterans General Hospital Occupational Therapy

地點 | Location:
臺北 - Taipei

開始日期 | Start Date: 2025-12-15

[查看詳情 | View Details]
```

## Common Questions

**Q: Will this work 24/7?**
A: Yes! GitHub Actions runs automatically every 6 hours, even when your computer is off.

**Q: Is it free?**
A: Yes! Everything is free (GitHub, Telegram, Google Translate API).

**Q: Can I change when it checks?**
A: Yes! Edit `.github/workflows/job-check.yml` and change the cron expression.

**Q: What if I want to test it locally first?**
A: Run `python main.py --test` to see all matching jobs.

**Q: Can I adjust the filters?**
A: Yes! Edit `scraper.py` lines 31-34 (location, keywords, dates).

**Q: What if no jobs are found?**
A: Check the logs - it probably ran but no jobs matched your criteria. That's normal!

## Troubleshooting

**Not receiving alerts?**
1. Check you added secrets correctly (Settings → Secrets)
2. Run workflow manually (Actions tab → Run workflow)
3. Check logs for errors

**Browser window not showing?**
- GitHub Actions automatically uses headless mode (no window)
- Local runs show browser window by default
- Both work the same way

**Seeing duplicates?**
- System tracks seen jobs (data/seen_jobs.json)
- Use test mode if you want to see all jobs: `python main.py --test`

**More help?**
- Read the relevant docs file above
- Check logs in Actions tab
- Review the error message

## Next Steps

Choose one:

### 👉 I want automated checks (GitHub Actions)
→ Read: `SETUP_GITHUB_REPO.md` (10 min)

### 👉 I want to test locally first
→ Read: `QUICK_START.md` (15 min)

### 👉 I want to understand everything
→ Read: `README.md` (full documentation)

---

## Technology Stack

- **Language:** Python 3.12
- **Web Scraping:** Playwright (browser automation)
- **Parsing:** BeautifulSoup
- **Translation:** Google Translate API (free)
- **Notifications:** Telegram Bot API
- **Scheduling:** GitHub Actions (cloud automation)
- **Cost:** Free! 🎉

## Support

If something isn't working:

1. Check the relevant documentation file (see above)
2. Look at the logs (Actions tab or job_monitor.log)
3. Search for your error in documentation
4. Read the troubleshooting section

---

**Ready to get started?** Pick an option above and follow the guide. You'll be receiving job alerts within 15 minutes! ✨
