from typing import Dict

class BitNetClient:
    def analyze_sentiment(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["great", "awesome", "launch", "love", "proud"]): return "Positive"
        if any(w in t for w in ["broken", "fail", "bug", "error", "bad"]): return "Negative"
        return "Neutral"

    def extract_topic(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["ml", "ai", "model"]): return "Artificial Intelligence"
        if any(w in t for w in ["code", "app", "software"]): return "Software Development"
        return "General Updates"

    def extract_entities(self, text: str) -> str:
        entities = []
        if "apple" in text.lower(): entities.append("Apple")
        if "google" in text.lower(): entities.append("Google")
        if "python" in text.lower(): entities.append("Python")
        return ", ".join(entities) if entities else "None"

    def process_all_semantic_tasks(self, text: str) -> Dict[str, str]:
        return {
            "sentiment": self.analyze_sentiment(text),
            "topic": self.extract_topic(text),
            "entities": self.extract_entities(text)
        }