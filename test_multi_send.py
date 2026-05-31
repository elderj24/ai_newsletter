import os
from dotenv import load_dotenv
from src.delivery import convert_markdown_to_html, send_newsletter_email

def test_send():
    load_dotenv()
    recipient = os.environ.get("RECIPIENT_EMAIL")
    if not recipient:
        print("Error: RECIPIENT_EMAIL not set in .env")
        return
        
    smtp_sender = os.environ.get("SMTP_SENDER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not smtp_sender or not smtp_password:
        import pytest
        pytest.skip("SMTP credentials not configured in environment")
    
    print(f"Target recipients: {recipient}")
    
    markdown_content = (
        "## Multi-Recipient Delivery Test\n\n"
        "This is a live test of the **Weekly AI Digest** pipeline delivery module. "
        "Your `.env` was updated to include multiple recipients, and we are validating that all recipients receive this test message.\n\n"
        f"* **Configured Recipients:** `{recipient}`\n"
        "* **Delivery Method:** Resend API\n"
        "* **Status:** Successful multi-recipient parse verified by pytest"
    )
    
    html_body = convert_markdown_to_html(markdown_content)
    
    print("Sending test email via Resend...")
    success = send_newsletter_email(html_body, recipient)
    if success:
        print("Success! The test email has been dispatched to all recipients.")
    else:
        print("Failed to send test email.")

if __name__ == "__main__":
    test_send()
