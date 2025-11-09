# Complete GitHub Actions Setup Guide

This guide walks you through setting up a private GitHub repository with automated job checking every 6 hours.

## Prerequisites

- GitHub account (free tier is fine)
- Telegram bot token and chat ID from earlier
- About 10 minutes of setup time

## Step-by-Step Setup

### 1. Create Private GitHub Repository

1. Go to https://github.com/new
2. Repository name: `tw-ot-jobsearch`
3. Description: "Taiwan OT Job Postings Monitor"
4. Select **Private** (important!)
5. Initialize with README
6. Click "Create repository"

### 2. Clone and Set Up Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/tw-ot-jobsearch.git
cd tw-ot-jobsearch

# Copy your project files into the repo
# (or if you're already in the project folder, just initialize git)
git init
git remote add origin https://github.com/YOUR_USERNAME/tw-ot-jobsearch.git
```

### 3. Add GitHub Secrets (IMPORTANT!)

This is where you store your Telegram credentials securely.

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**

**Add Secret #1:**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` (your actual bot token)
- Click "Add secret"

**Add Secret #2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: `123456789` (your actual chat ID)
- Click "Add secret"

✅ Your secrets are now encrypted and won't appear in logs or code

### 4. Add Files to Repository

Make sure these files are in your repository:

**Required files:**
- `main.py` - Entry point
- `scraper.py` - Web scraping logic
- `telegram_notifier.py` - Telegram integration
- `translator.py` - Translation module
- `scheduler.py` - Scheduling (kept for reference)
- `requirements.txt` - Python dependencies
- `.github/workflows/job-check.yml` - GitHub Actions workflow
- `.env.example` - Configuration template

**Optional files:**
- `README.md` - Documentation
- `.gitignore` - Git ignore rules
- Everything else

### 5. Create `.env` File (Local Only)

Create a `.env` file locally (for local testing):

```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
CHECK_INTERVAL_MINUTES=360  # (Not used in GitHub Actions, but keep for consistency)
```

**IMPORTANT:** Don't commit `.env` to GitHub! It's in `.gitignore`

### 6. Commit and Push to GitHub

```bash
# Configure git (first time only)
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Taiwan OT Job Search Monitor with GitHub Actions

- Automated job scraping every 6 hours
- Pagination through all job pages
- English translations
- Telegram notifications
- GitHub Actions scheduling"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Verify Setup

### Check Workflow File

1. Go to your GitHub repo
2. Click **Code** tab
3. Navigate to `.github/workflows/job-check.yml`
4. Verify the workflow file exists

### Check Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Verify you see:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### Test Workflow (Manual Trigger)

1. Click **Actions** tab
2. Click "Check for New Job Postings" workflow on the left
3. Click "Run workflow" button
4. Select **main** branch
5. Click "Run workflow"
6. Wait 2-5 minutes
7. Check Telegram for job alerts

### Check Logs

After workflow completes:

1. Click the completed workflow run
2. Click "check-jobs" job
3. Expand "Run job check" step to see logs
4. Look for:
   - "Found X total jobs"
   - "Filtered to X matching jobs"
   - "Sent X/X job alerts"

## Automated Schedule

The workflow now runs automatically at:

- **00:00 UTC** (06:00 Taipei time)
- **06:00 UTC** (14:00 Taipei time)
- **12:00 UTC** (20:00 Taipei time)
- **18:00 UTC** (02:00 next day Taipei time)

That's 4 times daily, every 6 hours.

## How to Update Code

If you need to change filters or update the scraper:

```bash
# Make changes locally
# Test with: python main.py --test

# Commit and push
git add .
git commit -m "Update filter criteria for jobs"
git push
```

The updated code will automatically run on the next scheduled check.

## Changing Schedule

To change how often checks run, edit `.github/workflows/job-check.yml`:

**Every 4 hours:**
```yaml
cron: '0 */4 * * *'
```

**Every 8 hours:**
```yaml
cron: '0 */8 * * *'
```

**Twice daily (6 AM & 6 PM UTC):**
```yaml
cron: '0 6,18 * * *'
```

Then commit and push:
```bash
git add .github/workflows/job-check.yml
git commit -m "Update schedule to every 4 hours"
git push
```

## Cost & Limits

GitHub Actions on private repositories:

| Plan | Monthly Minutes | Your Usage | Cost |
|------|-----------------|-----------|------|
| Free | 2,000 | ~120/month | Free ✅ |
| Pro | Unlimited | N/A | $4/month |

Your usage: ~5 min/run × 4 runs/day × 30 days = ~600 minutes/month

**You'll stay on free tier!**

## Troubleshooting

### Workflow not running at scheduled time?

GitHub Actions may have slight delays. This is normal.

**Solution:** Use the "Run workflow" button to trigger manually

### No Telegram messages received?

1. Check workflow logs in Actions tab
2. Look for error messages
3. Verify secrets are spelled exactly right:
   - `TELEGRAM_BOT_TOKEN` (with underscore, not dash)
   - `TELEGRAM_CHAT_ID` (with underscore, not dash)

### Workflow fails with error?

1. Click the failed workflow
2. Expand "Run job check" step
3. Read the error message
4. Common issues:
   - Secrets not set (check Settings → Secrets)
   - Wrong secret names
   - Timeout (takes longer than expected)

### Still seeing only first page of jobs?

1. Verify pagination code is updated
2. Test locally: `python main.py --test`
3. Commit and push any fixes

## Daily Monitoring

To see recent checks:

1. Click **Actions** tab
2. See workflow runs with timestamps
3. Click any run to see details
4. Scroll to "Run job check" step for logs

## Disabling Checks

If you need to pause checks:

1. Go to **Actions** tab
2. Click workflow name
3. Click "..." menu
4. Select "Disable workflow"

To re-enable: Click "Enable workflow"

## Next Steps

1. ✅ Create private GitHub repo
2. ✅ Add secrets (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
3. ✅ Push code to repo
4. ✅ Test workflow manually
5. ✅ Monitor logs to verify it's working
6. ✅ Let it run automatically every 6 hours!

## Questions?

Check the following for help:

- **Workflow not running:** Check Actions tab for scheduled runs
- **No messages received:** Check logs in Actions for errors
- **Need to change schedule:** Edit `.github/workflows/job-check.yml`
- **Need to change filters:** Edit `scraper.py` and push

You're all set! The system will now check for jobs automatically every 6 hours. 🎉
