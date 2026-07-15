# Twitter Profile Analyzer — Architecture

## Entry Points

1. **web_app.py** — Streamlit UI (5 tweets default)
2. **app.py** — CLI full pipeline (100 tweets)
3. **twitter_ngram_analyzer.py** — CLI hate/offensive detection (25 tweets)

## Data Flow

```
User URL Input
    → TweetScraper.validate_url()
    → BrowserLauncher.get_context() [Playwright Chromium]
    → page.goto(profile_url) + 20s wait
    → DOM extract tweets [max_tweets configurable per entry point]
    → [Fallback simulation if empty]
    → DatabaseManager.insert_profile() + insert_raw_tweets()
    → [Path A] FastTextClassifier + BitNetClient → update_analysis_results()
    → [Path B] TfidfVectorizer + RandomForest → terminal flag output
    → ChartGenerator.generate_category_pie_chart() [Path A only]
```

## Module Dependencies

```
web_app.py / app.py
├── fetcher.browser_launcher.BrowserLauncher
├── fetcher.tweet_scraper.TweetScraper
├── database.database.DatabaseManager
├── classifier.fasttext_classifier.FastTextClassifier
├── llm.bitnet_client.BitNetClient
└── visualization.charts.ChartGenerator

twitter_ngram_analyzer.py
├── fetcher.browser_launcher.BrowserLauncher
├── fetcher.tweet_scraper.TweetScraper
├── pandas, sklearn, joblib
└── en_Hasoc2021_train.csv
```

## Storage

- SQLite: database/twitter_analyzer.db
- Models: models/google_taxonomy_model.bin, models/heavy_ngram_model.pkl
- Charts: outputs/category_distribution.png
- Session: browser_profile/
