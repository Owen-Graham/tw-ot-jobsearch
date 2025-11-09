# GitHub Actions Quick Reference

## Setup Checklist

- [ ] Create private GitHub repo: `tw-ot-jobsearch`
- [ ] Add `TELEGRAM_BOT_TOKEN` secret in Settings → Secrets
- [ ] Add `TELEGRAM_CHAT_ID` secret in Settings → Secrets
- [ ] Push code to main branch
- [ ] Manually run workflow to test
- [ ] Check Telegram for alerts

## Key Files

| File | Purpose |
|------|---------|
| `.github/workflows/job-check.yml` | GitHub Actions automation (runs every 6 hours) |
| `main.py` | Entry point (runs `single_check()` mode) |
| `scraper.py` | Pagination + job scraping |
| `translator.py` | English translations |
| `telegram_notifier.py` | Telegram alerts |
| `requirements.txt` | Python dependencies |

## Schedule

Runs automatically at:
- 00:00 UTC (6:00 AM Taipei)
- 06:00 UTC (2:00 PM Taipei)
- 12:00 UTC (8:00 PM Taipei)
- 18:00 UTC (2:00 AM next day Taipei)

## Modes

### Normal Mode (GitHub Actions)
```bash
python main.py
```
- Runs once
- Sends new jobs only
- Headless browser (no window)
- Exit when complete

### Test Mode (Local)
```bash
python main.py --test
```
- Runs once
- Sends ALL matching jobs (ignores seen filter)
- Shows browser window
- Good for testing locally

## What Happens Each Run

1. ✅ Scrapes all 9 pages
2. ✅ Finds 93 total jobs
3. ✅ Filters by criteria (location, date, content)
4. ✅ Translates to English
5. ✅ Sends Telegram alerts for NEW jobs only
6. ✅ Saves tracking data (seen_jobs.json)
7. ✅ Exits cleanly

Time per run: ~5 minutes

## Common Tasks

### Manual Test
1. Go to Actions tab
2. Click "Check for New Job Postings"
3. Click "Run workflow"
4. Wait 2-5 minutes
5. Check Telegram

### View Logs
1. Click Actions tab
2. Click latest workflow run
3. Click "check-jobs"
4. Expand "Run job check" step

### Change Filters
1. Edit `scraper.py` lines 31-34:
   ```python
   TARGET_LOCATIONS = {...}  # Add/remove locations
   EXCLUDE_KEYWORDS = {...}  # Exclude more keywords
   TARGET_START_DATE_MIN = date(...)  # Change min date
   TARGET_START_DATE_MAX = date(...)  # Change max date
   ```
2. Commit and push
3. Next run uses new filters

### Change Schedule
1. Edit `.github/workflows/job-check.yml` line 7
2. Change cron expression
3. Examples:
   - Every 3 hours: `cron: '0 */3 * * *'`
   - Every 12 hours: `cron: '0 */12 * * *'`
4. Commit and push

### Disable Checks
1. Go to Actions tab
2. Click workflow name
3. Click "..." menu
4. Select "Disable workflow"

### Re-enable Checks
1. Go to Actions tab
2. Click workflow name
3. Click "..." menu
4. Select "Enable workflow"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow doesn't run at scheduled time | GitHub may have delays (up to 15 min). Use "Run workflow" button to test manually. |
| No Telegram messages received | Check Actions logs. Verify secrets are named exactly right (use underscore, not dash). |
| "No new matching jobs found" | Normal if no new jobs match your criteria. Check logs to confirm it ran. |
| Workflow fails | Click the workflow, expand "Run job check" step, read error message. |
| Browser errors | Check `GITHUB_ACTIONS` environment variable detection in scraper.py. |

## File Structure in Repo

```
tw-ot-jobsearch/
├── .github/
│   └── workflows/
│       └── job-check.yml          ← Runs every 6 hours
├── main.py                        ← Entry point
├── scraper.py                     ← Pagination logic
├── translator.py                  ← Translations
├── telegram_notifier.py          ← Telegram
├── requirements.txt              ← Dependencies
├── .gitignore                    ← Ignore .env
├── .env.example                  ← Config template
└── README.md                     ← Documentation
```

## Deployment Workflow

1. **Make changes locally**
   ```bash
   # Edit code
   python main.py --test  # Verify works
   ```

2. **Commit and push**
   ```bash
   git add .
   git commit -m "Update filters"
   git push
   ```

3. **Automatic deployment**
   - GitHub Actions automatically uses your latest code
   - Next scheduled run uses updated version
   - No manual deployment needed!

## Cost

- GitHub Actions: Free (2,000 min/month, using ~120)
- Telegram: Free
- Translation API (Google): Free
- **Total Cost: $0** ✅

## GitHub Secrets Reference

**Names must be EXACT (case-sensitive, use underscore):**

```
TELEGRAM_BOT_TOKEN   ← Your bot token (starts with numbers:)
TELEGRAM_CHAT_ID     ← Your chat ID (just numbers)
```

**How to find if you forget:**
1. Search Telegram for @BotFather → /mybots → select bot → API Token
2. Search Telegram for @userinfobot → send message → get chat ID

## Useful Links

- GitHub Actions docs: https://docs.github.com/actions
- Cron expression builder: https://crontab.guru/
- Your repo Actions tab: https://github.com/YOUR_USERNAME/tw-ot-jobsearch/actions

## Emergency Stop

If something goes wrong:

1. Go to Actions tab
2. Click workflow
3. Click "..." menu
4. Select "Disable workflow"
5. Fix issue
6. Re-enable when ready

## Next Steps

1. Set up repo (see SETUP_GITHUB_REPO.md)
2. Add secrets
3. Push code
4. Test manually
5. Monitor logs
6. Let it run automatically!

---

**Questions?** Check the logs in the Actions tab first - they usually tell you exactly what went wrong!
