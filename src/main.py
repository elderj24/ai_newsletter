import os
import sys
from dotenv import load_dotenv
from src.database import initialize_db, mark_articles_sent
from src.ingestion import fetch_weekly_updates
from src.synthesis import synthesize_articles
from src.delivery import convert_markdown_to_html, send_newsletter_email

def main():
    print("=========================================")
    print("TILIA AI NEWSLETTER PIPELINE STARTING")
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
    
    # Step 2: Ingest Recent Announcements via Exa.ai
    print("\n[2/5] Ingesting recent tech articles from Exa.ai...")
    articles = fetch_weekly_updates(db_path=db_path, days_back=7)
    print(f"-> Found {len(articles)} new, unsent articles.")
    
    if not articles:
        print("\nNo new announcements or updates detected this week. Terminating pipeline gracefully.")
        sys.exit(0)
        
    # Print summary of ingested articles to stdout
    for a in articles:
        print(f"   - [{a['company']}] {a['title']}")
        
    # Step 3: Strategic LLM Synthesis via Gemini
    print("\n[3/5] Synthesizing articles using Gemini 1.5 Pro...")
    newsletter_markdown = synthesize_articles(articles)
    
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
        mark_articles_sent(db_path, articles)
        print("Done! Database state updated.")
    else:
        print("\nError: Email delivery failed. Articles not marked as sent in DB.")
        sys.exit(1)
        
    print("\n=========================================")
    print("TILIA AI NEWSLETTER PIPELINE COMPLETE")
    print("=========================================")

if __name__ == "__main__":
    main()
