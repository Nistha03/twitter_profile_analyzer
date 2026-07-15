import os
import time
import logging
import sys
import pandas as pd
import joblib  # <-- This is the library that saves and loads the model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Match the exact scraper initialization from app.py
from fetcher.browser_launcher import BrowserLauncher
from fetcher.tweet_scraper import TweetScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("NgramApp")

def main():
    # ---------------------------------------------------------
    # STEP 1: INTERACTIVE URL INPUT
    # ---------------------------------------------------------
    profile_url = input("\nEnter the public Twitter/X profile URL to analyze: ").strip()
    
    launcher = BrowserLauncher()  
    scraper = TweetScraper(launcher)

    if not scraper.validate_url(profile_url):
        logger.error("Invalid profile URL syntax provided.")
        return

    profile_handle = profile_url.rstrip("/").split("/")[-1]
    logger.info(f"Analyzing profile: @{profile_handle}")

    # ---------------------------------------------------------
    # STEP 2: SCRAPE 25 REAL TWEETS
    # ---------------------------------------------------------
    raw_tweets = scraper.fetch_profile_tweets(profile_url, max_tweets=25)
    
    if not raw_tweets:
        logger.warning("No live timeline data scraped due to platform layout wall. Activating 25-tweet simulation fallback dataset...")
        raw_tweets = [
            {"text": "Why do they always want to destroy the nation?"},
            {"text": "I just bought a new car today and it runs perfectly."},
            {"text": "People who say I hate India should be questioned."},
            {"text": "The weather is absolutely amazing and clear today."},
            {"text": "Anti national elements are spreading fake news everywhere."},
            {"text": "Writing some clean python software source code for my class."}
        ]
        raw_tweets = (raw_tweets * 5)[:25]

    # ---------------------------------------------------------
    # STEP 3: SMART MODEL LOADING OR TRAINING
    # ---------------------------------------------------------
    # Path to save the brain right next to your google_taxonomy_model.bin!
    model_folder = "models"
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
        
    model_save_path = os.path.join(model_folder, "heavy_ngram_model.pkl")

    # If the brain is already saved, load it instantly!
    if os.path.exists(model_save_path):
        print("\n" + "="*60)
        print(" 🧠 PRE-TRAINED MODEL FOUND! Loading instantly...")
        print("="*60)
        best_model = joblib.load(model_save_path)
        
    # If not, do the 20-minute training and save it for next time!
    else:
        csv_file_path = "en_Hasoc2021_train.csv"
        print("\n" + "="*60)
        print(" 🧠 FIRST-TIME SETUP: INITIATING HEAVY ML GRID SEARCH")
        print("="*60)
        
        if not os.path.exists(csv_file_path):
            logger.error(f"Could not find CSV at {csv_file_path}")
            return

        df = pd.read_csv(csv_file_path)
        X = df['text'].astype(str)
        y = df['task_1']

        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(ngram_range=(1, 3))), 
            ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced'))
        ])

        param_grid = {
            'vectorizer__min_df': [1, 3, 5],
            'classifier__n_estimators': [100, 300, 500],
            'classifier__max_depth': [None, 20, 50],
            'classifier__min_samples_split': [2, 5, 10]
        }

        grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=3)

        print("⏳ STARTING LIVE 405-FIT CROSS-VALIDATION...")
        start_time = time.time()
        
        # Train it
        grid_search.fit(X, y)  
        
        best_model = grid_search.best_estimator_
        
        # Save it into your models folder!
        joblib.dump(best_model, model_save_path)
        
        elapsed_minutes = (time.time() - start_time) / 60
        print(f"\n✅ MODEL TRAINING COMPLETE IN {elapsed_minutes:.2f} MINUTES")
        print(f"💾 Saved as '{model_save_path}'. Next run will be instant!\n")

    # ---------------------------------------------------------
    # STEP 4: TERMINAL ANALYSIS
    # ---------------------------------------------------------
    print("\n" + "="*60)
    print(" 🔍 PHASE 2: TERMINAL BIGRAM-TRIGRAM BREAKDOWN")
    print("="*60 + "\n")
    
    vectorizer = best_model.named_steps['vectorizer']
    feature_names = vectorizer.get_feature_names_out()

    flagged_count = 0

    for idx, record in enumerate(raw_tweets, 1):
        tweet_text = record.get('text', '')
        if not tweet_text:
            continue
        
        prediction = best_model.predict([tweet_text])[0]
        category = "🚩 FLAGGED (Hate/Offensive Theme)" if prediction == "HOF" else "✅ SAFE"
        
        if prediction == "HOF":
            flagged_count += 1

        tweet_vector = vectorizer.transform([tweet_text]).toarray()[0]
        found_features = [feature_names[i] for i, val in enumerate(tweet_vector) if val > 0]
        bigrams = [f for f in found_features if f.count(' ') == 1]
        trigrams = [f for f in found_features if f.count(' ') == 2]

        print(f"--- TWEET #{idx} ---")
        print(f"Text : '{tweet_text}'")
        if bigrams:
            print(f" ├── ⚙️ ML BIGRAMS  : {bigrams[:4]}")
        if trigrams:
            print(f" ├── ⚙️ ML TRIGRAMS : {trigrams[:4]}")
        print(f" └── STATUS       : {category}\n" + "-"*60)

    print(f"\n📊 ANALYSIS SUMMARY: {flagged_count} out of {len(raw_tweets)} tweets flagged.")
    print("✅ Process complete. Returning to command line.\n")

if __name__ == "__main__":
    main()