# Taiwan OT Job Search Monitor - Documentation Index

Welcome! Here's a guide to all the documentation:

## 📚 Start Here

### For First-Time Users
1. **[QUICK_START.md](QUICK_START.md)** - Get up and running in 15 minutes
2. **[README.md](README.md)** - Comprehensive setup and features overview

### For Understanding Features
- **[FEATURES.md](FEATURES.md)** - Detailed explanation of all features
  - English translations
  - Test mode
  - Filters and date ranges
  - Bilingual alerts

### For Commands
- **[COMMANDS.md](COMMANDS.md)** - All available commands and workflows

### For Changes
- **[UPDATES.md](UPDATES.md)** - What changed in version 2.0

## 🚀 Quick Navigation

### I want to...

**Get started quickly**
→ Read: [QUICK_START.md](QUICK_START.md)

**Understand what features exist**
→ Read: [FEATURES.md](FEATURES.md)

**Run a command**
→ Check: [COMMANDS.md](COMMANDS.md)

**Set up the system**
→ Read: [README.md](README.md) → Setup section

**Test before automation**
→ Run: `python main.py --test`

**Preview filtered jobs**
→ Run: `python test_scraper.py`

**See what changed**
→ Read: [UPDATES.md](UPDATES.md)

**Troubleshoot an issue**
→ Check: [README.md](README.md) → Troubleshooting section
→ Or: [COMMANDS.md](COMMANDS.md) → Troubleshooting Commands

## 📁 File Structure

### Documentation Files
- **README.md** - Main documentation
- **QUICK_START.md** - Fast setup guide
- **FEATURES.md** - Detailed feature descriptions
- **COMMANDS.md** - Command reference
- **UPDATES.md** - Version 2.0 changes
- **INDEX.md** - This file

### Python Code
- **main.py** - Entry point with --test mode
- **scraper.py** - Web scraping and filtering
- **translator.py** - English translation module
- **telegram_notifier.py** - Telegram integration
- **scheduler.py** - Job scheduling
- **test_scraper.py** - Testing utility

### Configuration & Setup
- **.env** - Your credentials (create from .env.example)
- **.env.example** - Configuration template
- **requirements.txt** - Python dependencies
- **setup.sh** - Automated setup script

### Data & Logs
- **data/seen_jobs.json** - Tracks processed jobs (auto-created)
- **job_monitor.log** - Application logs (auto-created)
- **test_results.json** - Results from test_scraper.py (auto-created)

## 🎯 Key Features

### 1. English Translations 🇺🇸
All job postings are automatically translated to English, making them accessible to English speakers.

### 2. Test Mode 🧪
Preview all matching jobs with `python main.py --test` before enabling automation.

### 3. Date Range Filter 📅
Jobs starting between Feb 14 - Apr 15, 2026 (configurable).

### 4. Location Filter 📍
Taipei, New Taipei, Taoyuan (configurable).

### 5. Pediatric Exclusion 🚫
Automatically excludes pediatric positions (configurable).

### 6. Bilingual Telegram Alerts 📱
Each alert shows Chinese and English side-by-side.

### 7. Smart Tracking 📊
Never sends duplicate alerts for the same job.

## 🔧 Setup Steps

1. **Install dependencies**
   ```bash
   ./setup.sh
   ```

2. **Configure credentials**
   ```bash
   nano .env
   ```

3. **Test the scraper**
   ```bash
   python test_scraper.py
   ```

4. **Preview with test mode**
   ```bash
   python main.py --test
   ```

5. **Start monitoring**
   ```bash
   python main.py
   ```

## ❓ FAQ

**Q: Do I need an API key for translations?**
A: No! Translations use Google Translate API which is free.

**Q: What does --test flag do?**
A: Sends all matching jobs to Telegram, useful for previewing before automation.

**Q: How often does it check?**
A: Default is every 30 minutes (configurable in .env).

**Q: Will I get duplicate alerts?**
A: No! The system tracks which jobs it has sent.

**Q: Can I change the filters?**
A: Yes! Edit TARGET_LOCATIONS, EXCLUDE_KEYWORDS, and date range in scraper.py.

**Q: How do I keep it running 24/7?**
A: Use tmux, screen, or systemd (see COMMANDS.md).

## 🐛 Troubleshooting Quick Links

- Browser won't open → README.md Troubleshooting
- No jobs found → README.md Troubleshooting
- Telegram not sending → COMMANDS.md Troubleshooting Commands
- Bad translations → FEATURES.md Translation Quality

## 📞 Support

Check the documentation in this order:
1. README.md (Troubleshooting section)
2. FEATURES.md (for feature-specific issues)
3. COMMANDS.md (for command/execution issues)
4. Log file: `tail -f job_monitor.log`

## 🎉 Getting Started Now

The fastest way to get started:

```bash
# 1. Run setup
./setup.sh

# 2. Edit config
nano .env

# 3. Test it
python main.py --test

# 4. Go!
python main.py
```

That's it! You're monitoring for jobs.

---

Last updated: 2025-11-08
Version: 2.0 (with translations and test mode)
