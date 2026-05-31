from exa_py import Exa
import os
import datetime
from src.database import is_article_sent

def fetch_weekly_updates(db_path: str = "newsletter_state.db", days_back: int = 7) -> list[dict]:
    """
    Searches official announcement/blog domains for Google, OpenAI, Anthropic, xAI, Cursor, Cognition, and NVIDIA
    using Exa.ai. Filters out any URLs already present in the SQLite database.
    """
    exa_api_key = os.environ.get("EXA_API_KEY")
    if not exa_api_key:
        raise ValueError("EXA_API_KEY environment variable is not set")
        
    exa = Exa(api_key=exa_api_key)
    
    # Calculate start date scoped to UTC timezone
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Domain list for our scoped search
    target_domains = [
        "openai.com", 
        "anthropic.com", 
        "blog.google", 
        "deepmind.google",
        "x.ai", 
        "cursor.com",
        "cursor.sh",
        "cognition.ai",
        "cognition-labs.com",
        "nvidia.com",
        "blogs.nvidia.com"
    ]
    
    # Query Exa using semantic search with contents configuration
    try:
        response = exa.search(
            query="recent corporate press releases, technical announcements, product updates, and blog posts",
            include_domains=target_domains,
            start_published_date=start_date_str,
            num_results=15,
            contents={
                "text": {
                    "include_html_tags": False  # Clean markdown instead of raw HTML
                }
            }
        )
    except Exception as e:
        print(f"Error during Exa search: {e}")
        return []
        
    articles = []
    
    for result in getattr(response, "results", []):
        url = result.url
        title = result.title
        published_date = getattr(result, "published_date", "") or ""
        text = getattr(result, "text", "") or ""
        
        # Check if already processed
        if is_article_sent(db_path, url):
            continue
            
        # Determine the company/source based on domain
        company = "Unknown"
        lower_url = url.lower()
        if "openai.com" in lower_url:
            company = "OpenAI"
        elif "anthropic.com" in lower_url:
            company = "Anthropic"
        elif "blog.google" in lower_url or "deepmind.google" in lower_url or "google" in lower_url:
            company = "Google"
        elif "x.ai" in lower_url:
            company = "xAI"
        elif "cursor.com" in lower_url or "cursor.sh" in lower_url:
            company = "Cursor"
        elif "cognition.ai" in lower_url or "cognition-labs.com" in lower_url:
            company = "Cognition"
        elif "nvidia.com" in lower_url:
            company = "NVIDIA"
            
        articles.append({
            "url": url,
            "title": title,
            "published_date": published_date,
            "markdown": text,
            "company": company
        })
        
    return articles

def fetch_geopolitics_news(db_path: str = "newsletter_state.db", days_back: int = 7) -> list[dict]:
    """
    Searches for major political and geopolitical news using Exa.ai.
    Filters out any URLs already present in the SQLite database.
    """
    exa_api_key = os.environ.get("EXA_API_KEY")
    if not exa_api_key:
        raise ValueError("EXA_API_KEY environment variable is not set")
        
    exa = Exa(api_key=exa_api_key)
    
    # Calculate start date scoped to UTC timezone
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        response = exa.search(
            query="major international relations, geopolitics, global political news, and national policy developments",
            start_published_date=start_date_str,
            num_results=10,
            contents={
                "text": {
                    "include_html_tags": False
                }
            }
        )
    except Exception as e:
        print(f"Error during Exa geopolitics search: {e}")
        return []
        
    articles = []
    for result in getattr(response, "results", []):
        url = result.url
        title = result.title
        published_date = getattr(result, "published_date", "") or ""
        text = getattr(result, "text", "") or ""
        
        if is_article_sent(db_path, url):
            continue
            
        articles.append({
            "url": url,
            "title": title,
            "published_date": published_date,
            "markdown": text,
            "source": "Geopolitics"
        })
        
    return articles

def fetch_local_news(db_path: str = "newsletter_state.db", days_back: int = 7) -> list[dict]:
    """
    Searches for major local news in Illinois, Chicago, and Naperville using Exa.ai.
    Filters out any URLs already present in the SQLite database.
    """
    exa_api_key = os.environ.get("EXA_API_KEY")
    if not exa_api_key:
        raise ValueError("EXA_API_KEY environment variable is not set")
        
    exa = Exa(api_key=exa_api_key)
    
    # Calculate start date scoped to UTC timezone
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        response = exa.search(
            query="major local news, community updates, city council decisions, and developments in Chicago, Naperville, and Illinois",
            start_published_date=start_date_str,
            num_results=10,
            contents={
                "text": {
                    "include_html_tags": False
                }
            }
        )
    except Exception as e:
        print(f"Error during Exa local news search: {e}")
        return []
        
    articles = []
    for result in getattr(response, "results", []):
        url = result.url
        title = result.title
        published_date = getattr(result, "published_date", "") or ""
        text = getattr(result, "text", "") or ""
        
        if is_article_sent(db_path, url):
            continue
            
        # Determine specific location tag
        lower_title = title.lower()
        lower_url = url.lower()
        lower_text = text.lower()
        
        location = "Illinois"
        if "naperville" in lower_title or "naperville" in lower_url or "naperville" in lower_text[:1000]:
            location = "Naperville"
        elif "chicago" in lower_title or "chicago" in lower_url or "chicago" in lower_text[:1000]:
            location = "Chicago"
            
        articles.append({
            "url": url,
            "title": title,
            "published_date": published_date,
            "markdown": text,
            "location": location
        })
        
    return articles

