# 📊 Twitter/X Profile Analyzer

An advanced, dual-track Python intelligence tool designed to scrape, categorize, and perform deep linguistic and sentiment analysis on live public Twitter/X timelines. The system provides an interactive graphical dashboard for high-level profile taxonomy alongside a highly optimized, custom machine learning N-gram inspector.

---

## 🚀 Key Features

* **Unified Content Profiler (`app.py`)**: Automates the extraction of up to 100 recent tweets to map a profile's core narrative. Powered by a pre-trained FastText model (`google_taxonomy_model.bin`), it outputs an instant, interactive **Matplotlib Pie Chart** visualizing the user's content distribution.
* **Deep N-Gram Inspector (`twitter_ngram_analyzer.py`)**: Evaluates a focused dataset of 25 tweets against a heavy machine learning pipeline (`TfidfVectorizer` + `RandomForestClassifier`). Utilizes hyperparameter tuning (`GridSearchCV`) to dissect phrases into **Bigrams** and **Trigrams** while running a terminal-based hate-speech classification filter.
* **Intelligent Execution Caching**: Features a robust persistent state framework (`joblib`). The script handles heavy cross-validation modeling on the first execution and serializes the brain locally so subsequent runs return actionable insights instantly.
* **Robust Scraping Architecture**: Utilizes an automated Playwright browser session manager configured to bypass aggressive modern layout variations and content protection boundaries securely.

---

## 🗂️ Repository Workspace Layout

Ensure your cloned workspace maintains the following structural integrity before running the tools:

```text
TWITTER_PROFILE_ANALYZER/
├── browser_profile/         # Persistent automated browser sessions & session cookies
├── classifier/
│   ├── fasttext_classifier.py
│   └── ngram_trainer.py
├── database/
│   └── database.py          # Session tracking log managers
├── fetcher/
│   ├── browser_launcher.py   # Automated browser configurations
│   └── tweet_scraper.py      # Core timeline processing engine
├── models/
│   ├── google_taxonomy_model.bin   # Core taxonomy classifier weights
│   └── heavy_ngram_model.pkl       # Serialized N-gram model (Generated on 1st run)
├── visualization/
│   └── charts.py             # Matplotlib rendering templates
├── app.py                   # Primary Graphical Entry Point
├── twitter_ngram_analyzer.py # Deep Phrase Inspection Entry Point
├── twitter_login.py         # Authentication helper utility
├── en_Hasoc2021_train.csv   # N-gram baseline training dataset
└── requirements.txt         # Package pinning manifesto
