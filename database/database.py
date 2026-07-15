import sqlite3
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "database/twitter_analyzer.db") -> None:
        self.db_path = db_path
        self._create_tables()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self) -> None:
        query_profiles = """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_name TEXT UNIQUE NOT NULL,
            profile_url TEXT NOT NULL
        );"""
        query_tweets = """
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            tweet_text TEXT NOT NULL,
            predicted_category TEXT,
            sentiment TEXT,
            topic TEXT,
            named_entities TEXT,
            timestamp TEXT,
            FOREIGN KEY (profile_id) REFERENCES profiles (id)
        );"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_profiles)
            cursor.execute(query_tweets)
            conn.commit()

    def insert_profile(self, profile_name: str, profile_url: str) -> int:
        query = "INSERT OR IGNORE INTO profiles (profile_name, profile_url) VALUES (?, ?)"
        select_query = "SELECT id FROM profiles WHERE profile_name = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (profile_name, profile_url))
            cursor.execute(select_query, (profile_name,))
            row = cursor.fetchone()
            return row[0] if row else -1

    def insert_raw_tweets(self, profile_id: int, tweets: List[Dict[str, Any]]) -> None:
        query = "INSERT INTO tweets (profile_id, tweet_text, timestamp) VALUES (?, ?, ?)"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for t in tweets:
                cursor.execute(query, (profile_id, t['text'], t.get('timestamp', '')))
            conn.commit()

    def update_analysis_results(self, tweet_id: int, updates: Dict[str, Any]) -> None:
        query = """
        UPDATE tweets 
        SET predicted_category = ?, sentiment = ?, topic = ?, named_entities = ?
        WHERE id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (updates['category'], updates['sentiment'], updates['topic'], updates['entities'], tweet_id))
            conn.commit()

    def get_unprocessed_tweets(self, profile_id: int) -> List[Dict[str, Any]]:
        query = "SELECT id, tweet_text FROM tweets WHERE profile_id = ? AND predicted_category IS NULL"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (profile_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_profile_analytics(self, profile_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM tweets WHERE profile_id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (profile_id,))
            return [dict(row) for row in cursor.fetchall()]