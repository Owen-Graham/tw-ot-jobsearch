# Recent Updates

## Version 2.0 - Translation & Test Mode

### New Features

1. **English Translations** ✨
   - All job postings are automatically translated to English
   - Uses Google Translate API (free, no API key required)
   - Translation fields: title, location, organization, employment type, salary
   - Results cached for performance

2. **Bilingual Telegram Messages** 🇹🇼 🇺🇸
   - Each alert shows Chinese and English side-by-side
   - Clear formatting with field labels in both languages
   - Makes job opportunities accessible to English speakers

3. **Test Mode** 🧪
   - New `--test` flag to preview all matching jobs
   - Bypasses the "seen jobs" filter
   - Translates and sends all current matches to Telegram
   - Perfect for verifying filters before automation

### Updated Filters

**Date Range Changed:**
- **Old:** Single date (Feb 20, 2026 or later)
- **New:** Date range (Feb 14 - Apr 15, 2026)

```python
TARGET_START_DATE_MIN = date(2026, 2, 14)  # Feb 14, 2026
TARGET_START_DATE_MAX = date(2026, 4, 15)  # Apr 15, 2026
```

### New Files

- **translator.py** - Translation module using Google Translate API

### Modified Files

- **scraper.py**
  - Updated date filter to check date range
  - Added `translate` parameter to scrape() method
  - Integrates translator for automatic English translations

- **telegram_notifier.py**
  - Updated message format to include English translations
  - Bilingual field labels and content

- **main.py**
  - Added `--test` command-line argument
  - New `test_mode()` function for preview functionality
  - Enhanced configuration loading

- **requirements.txt** - No new dependencies (uses free APIs)

- **README.md** - Updated with new features and usage
- **QUICK_START.md** - Added test mode instructions

### Usage Examples

**Preview jobs before enabling automation:**
```bash
python main.py --test
```

**Run normal monitoring:**
```bash
python main.py
```

The `--test` flag is useful for:
- Verifying filter criteria
- Checking translation quality
- Previewing what alerts look like
- Fine-tuning location/date ranges

### Technical Details

- Translation API: Google Translate (free, no authentication needed)
- Translation caching: Translations cached in memory
- Date range: Feb 14 - Apr 15, 2026 (inclusive)
- Bilingual alerts: Chinese + English in each Telegram message

### Migration Notes

If you were using the previous version:
1. The date filter has changed from a single date to a range
2. All alerts now include English translations
3. The `--test` flag is optional but recommended for first run
4. No configuration changes needed; `.env` file remains the same
