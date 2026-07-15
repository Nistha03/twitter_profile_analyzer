import re
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright
from fetcher.browser_launcher import BrowserLauncher

class TweetScraper:
    def __init__(self, launcher: BrowserLauncher) -> None:
        self.launcher = launcher

    @staticmethod
    def validate_url(url: str) -> bool:
        pattern = r"^https?://(www\.)?(twitter\.com|x\.com)/[a-zA-Z0-9_]{1,15}/?$"
        return bool(re.match(pattern, url))

    def fetch_profile_tweets(self, profile_url: str, max_tweets: int = 5) -> List[Dict[str, Any]]:
        tweets = []
        if not self.validate_url(profile_url):
            return tweets

        with sync_playwright() as p:
            context = self.launcher.get_context(p)
            page = context.new_page()
            try:
                page.goto(profile_url, wait_until="domcontentloaded")
                page.wait_for_timeout(20000)
                tweet_elements = page.locator("article[data-testid='tweet']").all()
                for elem in tweet_elements[:max_tweets]:
                    try:
                        text = elem.locator("div[data-testid='tweetText']").inner_text()
                        tweets.append({"text": text, "timestamp": ""})
                    except:
                        continue
            except Exception:
                pass
            finally:
                context.close()
        return tweets