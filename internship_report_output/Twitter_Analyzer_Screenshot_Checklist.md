# Screenshot Checklist
| Figure | Description | Command/Action | Must Show |
|--------|-------------|----------------|----------|
| Figure 1 | Project structure in VS Code | `cd "C:\twitter_profile_analyzer (1)"` | IDE file explorer |
| Figure 2 | venv activation | `.\venv\Scripts\Activate.ps1` | (venv) in PowerShell |
| Figure 3 | pip install success | `pip install -r requirements.txt && pip install streamlit pandas scikit-learn joblib` | Successfully installed messages |
| Figure 4 | Streamlit server | `streamlit run web_app.py` | Local URL: http://localhost:8501 |
| Figure 5 | Main UI | `Open http://localhost:8501` | Title, URL input, buttons |
| Figure 6 | Browser during fetch | `Click Fetch Tweets` | Chromium on X profile |
| Figure 7 | Fetch success | `After fetch completes` | Green success banner |
| Figure 8 | Pie chart | `Click Analyze & Chart` | Category distribution chart |
| Figure 9 | Data table | `After analysis` | Streamlit dataframe |
| Figure 10 | CLI app.py | `python app.py` | Console tweet summary |
| Figure 11 | N-gram output | `python twitter_ngram_analyzer.py` | FLAGGED/SAFE lines |
| Figure 12 | SQLite DB | `Open twitter_analyzer.db` | profiles + tweets tables |
| Figure 13 | Fallback warning | `Fetch without login` | Yellow warning message |
| Figure 14 | Invalid URL error | `Enter bad URL` | Red error in UI |
| Figure 15 | Chart PNG file | `Open outputs/category_distribution.png` | Saved pie chart |
