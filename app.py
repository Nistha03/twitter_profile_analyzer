import logging
import sys
from database.database import DatabaseManager
from fetcher.browser_launcher import BrowserLauncher
from fetcher.tweet_scraper import TweetScraper
from classifier.fasttext_classifier import FastTextClassifier
from llm.bitnet_client import BitNetClient
from visualization.charts import ChartGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("App")

def main():
    profile_url = input("Enter the public Twitter/X profile URL to analyze: ").strip()
    
    db = DatabaseManager()
    launcher = BrowserLauncher()
    scraper = TweetScraper(launcher)
    classifier = FastTextClassifier()
    llm = BitNetClient()
    visualizer = ChartGenerator()

    if not scraper.validate_url(profile_url):
        logger.error("Invalid profile URL syntax provided.")
        return

    profile_handle = profile_url.rstrip("/").split("/")[-1]
    logger.info(f"Analyzing profile: @{profile_handle}")

    # --- UPGRADE 1: Fetch up to 100 tweets ---
    raw_tweets = scraper.fetch_profile_tweets(profile_url, max_tweets=100)
    
    # Fallback simulation data if browser path hits platform wall/login screen
    if not raw_tweets:
        logger.warning("No live timeline data scraped due to platform layout wall. Activating 100-tweet simulation fallback dataset...")
        
        # --- UPGRADE 2: Diverse data so your pie chart gets multiple colorful slices ---
        raw_tweets = [
            {"text": "Upgraded my home audio gaming center with custom soundboard electronics and headsets."},
            {"text": "Just pushed a massive software pipeline automation bug fix to our production servers."},
            {"text": "Grabbed a brand new lightweight cotton jacket and comfortable winter apparel shoes."},
            {"text": "Watching an incredible new cinematic movie streaming on television tonight."},
            {"text": "Writing some clean python software source code for my machine learning class sessional."},
            {"text": "Testing out the new smartphone screen display hardware electronics design."}
        ]
        
        # --- UPGRADE 3: Multiply the mock data to simulate exactly 100 database rows! ---
        raw_tweets = (raw_tweets * 20)[:100]

    profile_id = db.insert_profile(profile_handle, profile_url)
    db.insert_raw_tweets(profile_id, raw_tweets)

    # Core AI Analysis Loop
    unprocessed = db.get_unprocessed_tweets(profile_id)
    logger.info(f"Processing {len(unprocessed)} tweets through the AI pipeline...")
    
    for record in unprocessed:
        cleaned_text = classifier.clean_text(record['tweet_text'])
        category, _ = classifier.predict_category(cleaned_text)
        meta = llm.process_all_semantic_tasks(record['tweet_text'])
        
        db.update_analysis_results(record['id'], {
            "category": category,
            "sentiment": meta["sentiment"],
            "topic": meta["topic"],
            "entities": meta["entities"]
        })

    # Output Results
    final_data = db.get_profile_analytics(profile_id)
    print("\n" + "="*50 + "\n PROFILED USER ANALYTICS SUMMARY \n" + "="*50)
    
    # --- UPGRADE 4: Only print the first 5 to the console so it doesn't spam your screen ---
    for i, data in enumerate(final_data[:5], 1):
        print(f"Tweet #{i}: {data['tweet_text'][:80]}...")
        print(f" ├── Category : {data['predicted_category']}\n ├── Sentiment: {data['sentiment']}\n └── Topic    : {data['topic']}\n")
    
    print(f"... and {len(final_data) - 5} more tweets analyzed and saved to the database.")
    
    chart_path = visualizer.generate_category_pie_chart(final_data)
    if chart_path:
        logger.info(f"Visual metrics chart generated successfully at: {chart_path}")

if __name__ == "__main__":
    main()