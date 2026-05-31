import os
from dotenv import load_dotenv
from src.delivery import convert_markdown_to_html, send_newsletter_email

def main():
    load_dotenv()
    recipient_env = os.environ.get("RECIPIENT_EMAIL")
    if not recipient_env:
        print("Error: RECIPIENT_EMAIL not set in .env")
        return
        
    recipients = [r.strip() for r in recipient_env.split(",") if r.strip()]
    if len(recipients) < 2:
        print(f"Error: Expected at least 2 emails in RECIPIENT_EMAIL, but got: {recipients}")
        return
        
    second_recipient = recipients[1]
    print(f"Targeting second recipient: {second_recipient}")
    
    markdown_content = (
        "## Second Recipient Delivery Test\n\n"
        "This is a live test of the **Weekly AI Digest** pipeline delivery module. "
        "We are validating delivery specifically to the second email configured in your `.env` file.\n\n"
        f"* **Target Recipient:** `{second_recipient}`\n"
        "* **Delivery Method:** Resend API\n"
        "* **Status:** Running live test"
    )
    
    html_body = convert_markdown_to_html(markdown_content)
    
    print(f"Sending test email to {second_recipient} via Resend...")
    success = send_newsletter_email(html_body, second_recipient)
    if success:
        print("Success! The test email has been dispatched.")
    else:
        print("Failed to send test email.")

if __name__ == "__main__":
    main()
