# Features Reference

## Translation Feature

### Automatic English Translation

Every job posting is automatically translated from Chinese to English:

```
原文 (Chinese):      職業治療師助理
翻譯 (English):      Occupational Therapist Assistant

原文:               台北市大安區
翻譯:               Taipei City, Daan District
```

### Translation Scope

The following fields are translated:
- **Title** - Job position name
- **Location** - Where the job is located
- **Organization** - Hospital/clinic/organization name
- **Employment Type** - 正職 (Full-time), etc.
- **Salary** - Salary range in TWD

### Translation Quality

- Uses Google Translate API
- Translations are cached for performance
- If translation fails, original text is shown
- All translations happen asynchronously to not slow down processing

### Disabling Translation

If you want to disable translation (for faster processing):

In `scraper.py`, modify the `scrape()` call:
```python
# With translation (default)
jobs = await scraper.scrape(translate=True)

# Without translation
jobs = await scraper.scrape(translate=False)
```

## Test Mode Feature

### What is Test Mode?

Test mode scrapes ALL matching jobs and sends them to Telegram, bypassing the "seen jobs" tracking. This lets you preview alerts before enabling automation.

### When to Use Test Mode

- **First time setup**: Verify filters are working
- **After changing filters**: See what jobs the new filters find
- **To verify translations**: Check translation quality
- **To see message format**: Preview what alerts will look like

### Running Test Mode

```bash
python main.py --test
```

### What Happens in Test Mode

1. Opens browser (headless=False) and scrapes jobs
2. Parses and filters jobs based on criteria
3. Translates all filtered jobs to English
4. Sends each job as a Telegram message
5. Exits (doesn't start the scheduler)

### Example Output

```
✓ Test mode completed! Sent 5/5 messages
```

This means:
- Found 5 jobs matching your filters
- Translated all 5 to English
- Successfully sent all 5 to Telegram

### Differences: Test Mode vs Normal Mode

| Feature | Test Mode | Normal Mode |
|---------|-----------|------------|
| Scrape on demand | ✓ | Every N minutes |
| Show seen jobs | ✓ (all) | ✗ (new only) |
| Send alerts | ✓ (all) | ✓ (new only) |
| Keep running | ✗ (exits) | ✓ (continuous) |
| Track seen jobs | ✗ | ✓ |

## Date Range Filter

### Date Filter Details

- **Minimum**: November 1, 2025
- **Maximum**: April 15, 2026
- **Logic**: Job start date must fall within this range (inclusive)

**Note:** Dates are configurable in `scraper.py` to match current job postings on the website.

### Examples

These jobs would be included:
- Start date: 2025-11-01 ✓
- Start date: 2026-01-15 ✓
- Start date: 2026-03-01 ✓
- Start date: 2026-04-15 ✓

These jobs would be excluded:
- Start date: 2025-10-31 ✗ (too early)
- Start date: 2026-04-16 ✗ (too late)
- Start date: 2025-09-01 ✗ (too early)
- Start date: 2026-06-01 ✗ (too late)

### Modifying Date Range

Edit `scraper.py`:

```python
TARGET_START_DATE_MIN = date(2025, 11, 1)  # Change these dates as needed
TARGET_START_DATE_MAX = date(2026, 4, 15)
```

For example, to match only Feb 14 - Apr 15, 2026:
```python
TARGET_START_DATE_MIN = date(2026, 2, 14)
TARGET_START_DATE_MAX = date(2026, 4, 15)
```

## Location Filter

### Current Locations

Jobs are only included if they're in:
- Taipei (台北, 臺北, 台北市)
- New Taipei (新北, 新北市)
- Taoyuan (桃園, 桃園市)

### Modifying Locations

Edit `scraper.py`:

```python
TARGET_LOCATIONS = {"台北", "臺北", "新北", "新北市", "台北市", "桃園", "桃園市"}
```

To add locations, add them to the set:
```python
TARGET_LOCATIONS = {"台北", "新北", "桃園", "新竹", "中壢"}  # Added 新竹 and 中壢
```

## Pediatric Exclusion Filter

### Current Exclusions

Jobs are excluded if they contain:
- 小兒 (pediatric)
- 小兒自費 (private pediatric)
- pediatric (English keyword)

### Modifying Exclusions

Edit `scraper.py`:

```python
EXCLUDE_KEYWORDS = {"小兒", "小兒自費", "pediatric"}
```

To add more exclusions:
```python
EXCLUDE_KEYWORDS = {"小兒", "小兒自費", "pediatric", "復健", "護理"}
```

## Bilingual Telegram Messages

### Message Format

Each Telegram alert shows:

```
🇹🇼 新工作機會！ | 🇺🇸 New Job Opportunity!

職位 | Position:
[Chinese Title]
[English Translation]

地點 | Location:
[Chinese Location] [English Translation]

機構 | Organization:
[Chinese Name]
[English Translation]

開始日期 | Start Date: [Date]

職位類型 | Employment Type:
[Chinese] [English]

薪資 | Salary:
[Chinese] [English]

[Link to view details]
```

### Why Bilingual?

- Reaches English speakers interested in Taiwan jobs
- Makes opportunities clear to international applicants
- Provides context with both original and translated text

## Seen Jobs Tracking

### How It Works

- Normal mode: Tracks jobs in `data/seen_jobs.json`
- Only new jobs trigger alerts
- Prevents duplicate notifications

### Resetting Tracking

To reset and get alerts for all jobs again:

```bash
# Remove the tracking file
rm data/seen_jobs.json

# Next run will treat all jobs as "new"
python main.py
```

### Test Mode Bypass

Test mode ignores the seen jobs file:
```bash
python main.py --test
# Sends ALL matching jobs, regardless of tracking
```

## Performance Tips

1. **Translation Caching**: Translations are cached in memory during a run
2. **Check Interval**: Increase `CHECK_INTERVAL_MINUTES` to reduce API calls
3. **Filter Specificity**: More restrictive filters = faster processing
4. **Headless Mode**: Can switch to headless=True for server deployments

## Troubleshooting

### No translations appearing?

- Check internet connection (translation requires Google API)
- Verify the text isn't already in English
- Check logs for translation errors

### Too many alerts?

- Make filters more specific (narrow date range, add location)
- Increase `CHECK_INTERVAL_MINUTES` to check less frequently
- Use `--test` mode first to see what jobs match

### Missing jobs in alerts?

- Check if job was already seen (check `data/seen_jobs.json`)
- Verify filters match the job (location, date, content)
- Use `--test` mode to see all matching jobs

### Translations look bad?

- This is sometimes a Google Translate limitation
- Check if original Chinese text has typos
- Consider using test mode to verify before automation
