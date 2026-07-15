import pandas as pd
import time
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

class HeavyNgramTrainer:
    def __init__(self):
        self.best_model = None

    def train_model(self, csv_path):
        print("="*60)
        print(" 🧠 INITIATING HEAVY BIGRAM-TRIGRAM TRAINING SEQUENCE")
        print("="*60)
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: Could not find CSV at {csv_path}")
            return False

        print("1. Loading dataset into memory...")
        df = pd.read_csv(csv_path)
        
        # Ensure we are reading text as strings
        X = df['text'].astype(str)
        y = df['task_1']

        print("2. Configuring Bigram-Trigram Pipeline...")
        # This pipeline links the Bigram-Trigram extractor directly to a Random Forest ML algorithm
        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(ngram_range=(2, 3))), # Strictly 2-word and 3-word combinations
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        print("3. Setting up Hyperparameter Grid (This creates the heavy workload)...")
        # By providing multiple options here, the model will train itself 81 different times
        # across 5 data folds (405 total training cycles). This takes serious time!
        param_grid = {
            'vectorizer__min_df': [1, 3, 5],
            'classifier__n_estimators': [100, 300, 500],
            'classifier__max_depth': [None, 20, 50],
            'classifier__min_samples_split': [2, 5, 10]
        }

        # n_jobs=-1 tells your computer to use all CPU cores.
        # verbose=3 will print live updates to the terminal so you can watch it train.
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=3)

        print("\n⏳ STARTING GRID SEARCH CROSS-VALIDATION...")
        print("⚠️ Warning: This will take 10-20 minutes depending on your CPU hardware.")
        
        start_time = time.time()
        
        # --- THIS IS THE LINE THAT TAKES 20 MINUTES ---
        grid_search.fit(X, y)
        
        elapsed_minutes = (time.time() - start_time) / 60
        
        self.best_model = grid_search.best_estimator_
        
        print("\n" + "="*60)
        print(f" ✅ TRAINING COMPLETE IN {elapsed_minutes:.2f} MINUTES")
        print("="*60)
        print(f"Best Configuration Found: {grid_search.best_params_}\n")
        return True

    def analyze_tweets(self, tweets):
        if not self.best_model:
            print("Error: Model must be trained before analysis.")
            return

        print("="*50)
        print(" 🔍 PHASE 2: TERMINAL TWEET ANALYSIS")
        print("="*50 + "\n")
        
        flagged_count = 0
        
        # Use the fully trained 20-minute model to predict the new tweets
        predictions = self.best_model.predict(tweets)

        for idx, (tweet, prediction) in enumerate(zip(tweets, predictions), 1):
            print(f"--- TWEET #{idx} ---")
            print(f"Original Text : '{tweet}'")
            
            if prediction == "HOF":
                print("STATUS: 🚩 FLAGGED (Hate/Offensive Theme detected via N-Grams)")
                flagged_count += 1
            else:
                print("STATUS: ✅ SAFE")
                
            print("-" * 50)
            
        print(f"\nANALYSIS SUMMARY: {flagged_count} out of {len(tweets)} tweets flagged.\n")

if __name__ == "__main__":
    csv_file_path = r"C:\twitter_profile_analyzer\en_Hasoc2021_train.csv"

    new_tweets_to_check = [
        "Why do they always want to destroy the nation?",
        "I just bought a new car today.",
        "People who say I hate India should be questioned.",
        "The weather is amazing today."
    ]

    model = HeavyNgramTrainer()
    
    # 1. This will run for 10 to 20 minutes
    if model.train_model(csv_file_path):
        # 2. This will instantly analyze the tweets using the massive model
        model.analyze_tweets(new_tweets_to_check)