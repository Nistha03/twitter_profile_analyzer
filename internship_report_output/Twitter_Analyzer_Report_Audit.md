# Twitter Profile Analyzer — Report Audit

Generated: 2026-07-10 19:24:17

## 1. Repository Files Inspected

### Python Source Files
- app.py
- web_app.py
- twitter_ngram_analyzer.py
- fetcher/browser_launcher.py
- fetcher/tweet_scraper.py
- database/database.py
- classifier/fasttext_classifier.py
- classifier/ngram_trainer.py
- llm/bitnet_client.py
- visualization/charts.py

### Configuration & Data
- requirements.txt
- en_Hasoc2021_train.csv
- models/taxonomy_train.txt (504,196+ lines)

### Browser Profile (Sensitive)
- browser_profile/ (Chromium persistent session data)

### Not Found
- README.md (project root)
- package.json / frontend React app
- scripts/setup_bitnet.ps1
- scripts/run_project.ps1
- Probing agent / crawler modules
- Test files (pytest, unittest)
- Screenshots (*.png, *.jpg)
- google_taxonomy_model.bin
- heavy_ngram_model.pkl
- Docker files

## 2. Important Source Files

| File | Role |
|------|------|
| web_app.py | Streamlit UI entry point |
| app.py | CLI taxonomy pipeline (100 tweets) |
| twitter_ngram_analyzer.py | CLI n-gram HOF/NOT flagging (25 tweets) |
| fetcher/tweet_scraper.py | Playwright DOM scraping |
| fetcher/browser_launcher.py | Persistent Chromium context |
| classifier/fasttext_classifier.py | FastText taxonomy |
| classifier/ngram_trainer.py | GridSearch n-gram trainer |
| database/database.py | SQLite persistence |
| llm/bitnet_client.py | Rule-based semantic heuristics |

## 3. Verified Technologies

| Technology | Evidence |
|------------|----------|
| Python | All .py files |
| Playwright 1.42.0 | requirements.txt, tweet_scraper.py, browser_launcher.py |
| Chromium | launch_persistent_context |
| Streamlit | web_app.py import (NOT in requirements.txt) |
| FastText | fasttext_classifier.py, requirements.txt |
| scikit-learn | twitter_ngram_analyzer.py, ngram_trainer.py |
| pandas | CSV loading |
| joblib | Model pickle save/load |
| SQLite | database.py |
| matplotlib | charts.py |
| numpy | requirements.txt |

### NOT Used (Verified Absent)
- FastAPI, Flask, Django, Uvicorn
- React, Vite, Node.js frontend
- Selenium, CloakBrowser
- Tweepy, snscrape, official X API
- PostgreSQL, MongoDB, Redis
- WebSockets
- spaCy, NLTK, Hugging Face Transformers
- Static n-gram dictionary file

## 4. Verified Browser Automation Method

- **Framework:** Playwright sync_api
- **Launch:** chromium.launch_persistent_context
- **user_data_dir:** browser_profile
- **headless:** False
- **args:** --disable-blink-features=AutomationControlled

## 5. Verified Data Collection Method

- Navigate to user-supplied profile URL
- Wait 20 seconds (wait_for_timeout(20000))
- Select article[data-testid='tweet']
- Extract div[data-testid='tweetText'] inner_text
- No scrolling implemented
- No home feed access

## 6. Verified N-Gram Logic

- **NOT a static dictionary** — ML-based TF-IDF features
- **twitter_ngram_analyzer.py:** TfidfVectorizer(ngram_range=(1,3)) + RandomForestClassifier
- **ngram_trainer.py:** TfidfVectorizer(ngram_range=(2,3)) + RandomForestClassifier
- **Training data:** en_Hasoc2021_train.csv, labels in task_1 (HOF, NOT)
- **Model cache:** models/heavy_ngram_model.pkl

## 7. Verified Flagging Logic

- **Condition:** prediction == "HOF"
- **Scope:** Per-tweet only
- **Output:** Terminal print FLAGGED/SAFE + summary count
- **No user-level flagging**
- **No confidence threshold**
- FastText path does NOT flag users

## 8. Verified Backend Routes

None. No REST API. Streamlit runs in-process.

## 9. Verified Frontend Components

- Streamlit page: Twitter Profile Analyzer
- Sidebar setup instructions
- URL text input
- Wait time slider (0-120s, default 90)
- Fetch Tweets button
- Analyze & Chart button
- Pie chart display (st.image)
- Dataframe display (st.dataframe)

## 10. Verified Commands

```powershell
cd "C:\twitter_profile_analyzer (1)"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install streamlit pandas scikit-learn joblib
playwright install chromium
streamlit run web_app.py
python app.py
python twitter_ngram_analyzer.py
```

## 11. Commands Requiring Manual Verification

- Streamlit default port 8501
- Exact Playwright install path on student machine
- First-run FastText training duration on large taxonomy_train.txt
- GridSearchCV training time (10-20 min cited in code)
- Whether live X scraping works with student's browser session

## 12. Screenshots Found

None in repository.

## 13. Screenshots Missing (All 15 — Student Must Capture)

See Twitter_Analyzer_Screenshot_Checklist.md

## 14. Claims Requiring Student Confirmation

- [YOUR FULL NAME]
- Internship Role
- Internship Duration
- Mentor / Manager name
- Submission Date
- Personal contribution ownership per module
- Actual test results (Section 27)
- Whether live scraping succeeded on their machine

## 15. Unresolved Technical Limitations

- No probing agent / home feed crawler
- Incomplete requirements.txt
- Missing scripts/ folder referenced in web_app.py
- BitNetClient is heuristic, not real BitNet LLM
- DOM scraping fragile without login
- No automated tests
- No rate limiting / retries

## 16. Security-Sensitive Files (Exclude from ZIP)

- browser_profile/ (entire directory — cookies, session storage)
- database/twitter_analyzer.db (may contain scraped tweet text)
- venv/ (large, machine-specific)
- __pycache__/ directories
- Any .env file if created with credentials

## 17. Remaining Report Placeholders

- Cover page: student name, role, duration, mentor, date
- Section 27: all test observed results
- Section 29: all 15 screenshot placeholders
- Contribution ownership disclaimer in Section 5
