import os
import sys
from dotenv import load_dotenv
from src.database import initialize_db, mark_articles_sent
from src.ingestion import fetch_weekly_updates, fetch_geopolitics_news, fetch_local_news
from src.synthesis import synthesize_articles
from src.delivery import convert_markdown_to_html, send_newsletter_email

def main():
    # Configure stdout to use UTF-8 encoding, preventing crashes on Windows console with non-ASCII characters
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=========================================")
    print("AI NEWSLETTER PIPELINE STARTING")
    print("=========================================")
    
    # Load environment variables from .env
    load_dotenv()
    
    # Configuration Validation
    required_env = ["GEMINI_API_KEY", "EXA_API_KEY", "RESEND_API_KEY", "RECIPIENT_EMAIL"]
    missing = [var for var in required_env if not os.environ.get(var)]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file or GitHub Secrets configuration.")
        sys.exit(1)
        
    db_path = "newsletter_state.db"
    recipient = os.environ["RECIPIENT_EMAIL"]
    
    # Step 1: Initialize State Database
    print("\n[1/5] Initializing SQLite state database...")
    initialize_db(db_path)
    
    # Step 2: Ingest Recent Announcements and News via Exa.ai
    print("\n[2/5] Ingesting recent articles from Exa.ai...")
    
    print("   - Fetching tech company announcements...")
    tech_articles = fetch_weekly_updates(db_path=db_path, days_back=7)
    print(f"     -> Found {len(tech_articles)} new, unsent tech articles.")
    
    print("   - Fetching global politics & geopolitics...")
    politics_articles = fetch_geopolitics_news(db_path=db_path, days_back=7)
    print(f"     -> Found {len(politics_articles)} new, unsent politics articles.")
    
    print("   - Fetching local news (Illinois/Chicago/Naperville)...")
    local_articles = fetch_local_news(db_path=db_path, days_back=7)
    print(f"     -> Found {len(local_articles)} new, unsent local articles.")
    
    all_articles = tech_articles + politics_articles + local_articles
    print(f"\n-> Total new, unsent articles across all sections: {len(all_articles)}")
    
    if not all_articles:
        print("\nNo new articles or updates detected this week across any section. Terminating pipeline gracefully.")
        sys.exit(0)
        
    # Print summary of ingested articles to stdout
    if tech_articles:
        print("\n   [Tech Updates]:")
        for a in tech_articles:
            print(f"     * [{a['company']}] {a['title']}")
    if politics_articles:
        print("\n   [Geopolitics News]:")
        for a in politics_articles:
            print(f"     * {a['title']}")
    if local_articles:
        print("\n   [Local News]:")
        for a in local_articles:
            print(f"     * [{a['location']}] {a['title']}")
        
    # Step 3: Strategic LLM Synthesis via Gemini
    print("\n[3/5] Synthesizing articles using Gemini...")
    newsletter_markdown = synthesize_articles(
        tech_articles=tech_articles,
        politics_articles=politics_articles,
        local_articles=local_articles
    )
    
    # Step 4: Convert to Premium Inline-Styled HTML
    print("\n[4/5] Compiling HTML template with responsive, high-end design...")
    newsletter_html = convert_markdown_to_html(newsletter_markdown)
    
    # Step 5: Deliver Newsletter via Resend
    print("\n[5/5] Delivering strategic newsletter email via Resend...")
    success = send_newsletter_email(newsletter_html, recipient)
    
    if success:
        print("\nEmail delivered successfully!")
        # Step 6: Update Database to Prevent Future Duplicates
        print("Marking articles as processed in SQLite...")
        mark_articles_sent(db_path, all_articles)
        print("Done! Database state updated.")
    else:
        print("\nError: Email delivery failed. Articles not marked as sent in DB.")
        sys.exit(1)
        
    print("\n=========================================")
    print("AI NEWSLETTER PIPELINE COMPLETE")
    print("=========================================")

if __name__ == "__main__":
    main()

