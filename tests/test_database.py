import os
import sqlite3
import pytest
from src.database import initialize_db, is_article_sent, mark_articles_sent

@pytest.fixture
def temp_db(tmp_path):
    """Provides a path to a temporary SQLite database for testing."""
    db_file = tmp_path / "test_state.db"
    return str(db_file)

def test_initialize_db(temp_db):
    initialize_db(temp_db)
    assert os.path.exists(temp_db)
    
    # Verify table schema
    conn = sqlite3.connect(temp_db)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
        table = cursor.fetchone()
        assert table is not None
        assert table[0] == "articles"
    finally:
        conn.close()

def test_article_checking_and_marking(temp_db):
    initialize_db(temp_db)
    
    test_url = "https://example.com/ai-update"
    assert not is_article_sent(temp_db, test_url)
    
    articles = [
        {"url": test_url, "title": "AI Update", "published_date": "2026-05-23"}
    ]
    
    mark_articles_sent(temp_db, articles)
    assert is_article_sent(temp_db, test_url)

def test_bulk_marking_and_duplicates(temp_db):
    initialize_db(temp_db)
    
    articles = [
        {"url": "https://example.com/1", "title": "One", "published_date": "2026-05-23"},
        {"url": "https://example.com/2", "title": "Two", "published_date": "2026-05-23"},
        {"url": "https://example.com/1", "title": "Duplicate One", "published_date": "2026-05-23"},
    ]
    
    mark_articles_sent(temp_db, articles)
    
    assert is_article_sent(temp_db, "https://example.com/1")
    assert is_article_sent(temp_db, "https://example.com/2")
    
    # Try marking the same again, it should execute without errors due to INSERT OR IGNORE
    mark_articles_sent(temp_db, [{"url": "https://example.com/1", "title": "One", "published_date": "2026-05-23"}])
    assert is_article_sent(temp_db, "https://example.com/1")
