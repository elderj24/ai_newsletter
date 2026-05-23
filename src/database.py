import sqlite3
import datetime
import os

def initialize_db(db_path: str = "newsletter_state.db") -> None:
    """Initializes the database schema if it doesn't already exist."""
    # Ensure directory exists if db_path contains subdirectories
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                published_date TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()

def is_article_sent(db_path: str, url: str) -> bool:
    """Checks if the given article URL is already marked as sent."""
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()

def mark_articles_sent(db_path: str, articles: list[dict]) -> None:
    """Bulk marks a list of articles as sent in the database.
    Each article dict should have: 'url', 'title', 'published_date'.
    """
    if not articles:
        return
        
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        # Using UTC timezone-neutral isoformat for SQLite timestamp
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data = [
            (a.get("url"), a.get("title", ""), a.get("published_date", ""), now)
            for a in articles if a.get("url")
        ]
        if data:
            cursor.executemany("""
                INSERT OR IGNORE INTO articles (url, title, published_date, sent_at)
                VALUES (?, ?, ?, ?)
            """, data)
            conn.commit()
    finally:
        conn.close()
