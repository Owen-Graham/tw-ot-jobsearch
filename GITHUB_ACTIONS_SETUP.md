# GitHub Actions Setup Guide

This guide explains how to set up automated job checking using GitHub Actions (runs every 6 hours).

## Prerequisites

1. A GitHub account
2. A private GitHub repository
3. Telegram bot token and chat ID (from earlier setup)

## Step 1: Create Private GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `tw-ot-jobsearch`
3. Select **Private** (important for security - keep bot token private)
4. Initialize with README (optional)
5. Click "Create repository"

## Step 2: Add Secrets to GitHub

GitHub Secrets are encrypted environment variables. Your bot token will be stored safely.

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   **Secret 1:**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: (paste your Telegram bot token)

   **Secret 2:**
   - Name: `TELEGRAM_CHAT_ID`
   - Value: (paste your Telegram chat ID)

4. Click "Add secret" for each

## Step 3: Push Code to GitHub

From your local machine:

```bash
cd /home/owen/workspace/tw_ot_jobsearch

# Initialize git (if not already done)
git init

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/tw-ot-jobsearch.git

# Configure git
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Taiwan OT Job Search Monitor with GitHub Actions"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Verify Workflow

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see "Check for New Job Postings" workflow
4. It will run automatically:
   - At 00:00 UTC (6:00 AM UTC+8 Taiwan)
   - At 06:00 UTC (2:00 PM UTC+8 Taiwan)
   - At 12:00 UTC (8:00 PM UTC+8 Taiwan)
   - At 18:00 UTC (2:00 AM next day UTC+8 Taiwan)

## Step 5: Trigger Manual Run (Optional)

To test the workflow immediately:

1. Go to **Actions** tab
2. Select "Check for New Job Postings"
3. Click "Run workflow" → "Run workflow"
4. Wait 2-5 minutes for it to complete
5. Check your Telegram for job alerts

## How It Works

**Workflow Timing:**
- Runs every 6 hours automatically (cron schedule)
- Can be manually triggered anytime
- Timeout: 30 minutes per run (should complete in ~5 minutes)

**Each Run:**
1. Checks out your code
2. Sets up Python 3.12
3. Installs dependencies
4. Runs the job scraper
5. Sends Telegram alerts for new jobs
6. Saves job tracking data
7. Uploads logs for debugging

**Job Tracking:**
- Seen jobs are cached between runs (in `data/seen_jobs.json`)
- Uses GitHub artifact cache (90-day retention)
- Prevents duplicate alerts across runs

**Logs:**
- Available in GitHub Actions for 7 days
- Stored in artifact `job-monitor-logs`
- Useful for debugging if something goes wrong

## Customizing Schedule

To change check frequency, edit `.github/workflows/job-check.yml`:

**Every 3 hours:**
```yaml
cron: '0 */3 * * *'
```

**Every 12 hours:**
```yaml
cron: '0 */12 * * *'
```

**Daily at 9 AM UTC:**
```yaml
cron: '0 9 * * *'
```

Then commit and push:
```bash
git add .github/workflows/job-check.yml
git commit -m "Update job check schedule to every 3 hours"
git push
```

## Disabling Workflow

To temporarily pause checks without deleting:

1. Go to **Actions** tab
2. Click workflow name
3. Click "..." menu
4. Select "Disable workflow"

To re-enable: click "Enable workflow"

## Troubleshooting

### Workflow not running at scheduled time?
- GitHub Actions may have slight delays (up to 15 minutes)
- Use "Run workflow" button to test immediately
- Check that your repository has Actions enabled

### No Telegram messages received?
1. Check workflow logs in Actions tab
2. Verify bot token and chat ID in Secrets
3. Ensure bot has permission to send messages
4. Run `python main.py --test` locally to verify setup

### Workflow failing?
1. Click the failed workflow run
2. Scroll to "Run job check" step
3. See the error message
4. Common issues:
   - Wrong secret names (must match exactly)
   - Timeout (increase `timeout-minutes` if needed)
   - Missing dependencies

## Cost

GitHub Actions on private repositories:
- **Free tier**: 2,000 minutes/month
- **Our usage**: ~5 minutes × 4 runs/day × 30 days = 600 minutes/month
- **Status**: Well within free tier ✅

## Security Notes

✅ Bot token stored securely in GitHub Secrets
✅ Private repository limits access
✅ No credentials in code or git history
✅ Logs are uploaded safely

## Updating Code

To update the scraper or any code:

```bash
# Make changes locally
# Test with: python main.py --test

# Commit and push
git add .
git commit -m "Update filter criteria"
git push

# Workflow will automatically use the updated code on next scheduled run
```

## Monitoring

To check job search history:

1. Go to **Actions** tab
2. Click on any workflow run to see:
   - Status (success/failure)
   - Execution time
   - Logs
   - Uploaded artifacts (job tracking, logs)

## Questions?

- Check the logs in Actions for error messages
- Review the workflow file: `.github/workflows/job-check.yml`
- See main README.md for general troubleshooting
