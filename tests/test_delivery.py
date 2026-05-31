import pytest
from unittest.mock import patch, MagicMock
from src.delivery import convert_markdown_to_html, send_newsletter_email

def test_convert_markdown_to_html():
    markdown = (
        "# Main Title\n"
        "## Sub Title\n"
        "### Section Title\n"
        "#### Local Sub Title\n"
        "This is **bold** text and a [Google Link](https://google.com).\n"
        "* Bullet 1\n"
        "* Bullet 2"
    )
    
    html = convert_markdown_to_html(markdown)
    
    # Asserting correct HTML structures and styles are in place
    assert "Main Title" in html
    assert "Sub Title" in html
    assert "Section Title" in html
    assert "Local Sub Title" in html
    assert 'color: #475569; font-size: 14px;' in html
    assert "<strong>bold</strong>" in html
    assert 'href="https://google.com"' in html
    assert '<li style="margin-bottom: 6px;">Bullet 1</li>' in html
    assert '<li style="margin-bottom: 6px;">Bullet 2</li>' in html
    assert "</ul>" in html

@patch("src.delivery.resend.Emails.send")
def test_send_newsletter_email_success(mock_send):
    mock_response = MagicMock()
    mock_response.id = "test-email-id"
    mock_send.return_value = mock_response
    
    with patch.dict("os.environ", {"RESEND_API_KEY": "test_resend_key"}):
        result = send_newsletter_email("<p>Test Body</p>", "recipient@example.com")
        
    assert result is True
    mock_send.assert_called_once_with({
        "from": "AI Digest <onboarding@resend.dev>",
        "to": "recipient@example.com",
        "subject": mock_send.call_args[0][0]["subject"],
        "html": "<p>Test Body</p>"
    })

@patch("src.delivery.resend.Emails.send")
def test_send_newsletter_email_multiple_recipients(mock_send):
    mock_response = MagicMock()
    mock_response.id = "test-email-id"
    mock_send.return_value = mock_response
    
    with patch.dict("os.environ", {"RESEND_API_KEY": "test_resend_key"}):
        result = send_newsletter_email("<p>Test Body</p>", "recipient1@example.com, recipient2@example.com")
        
    assert result is True
    mock_send.assert_called_once_with({
        "from": "AI Digest <onboarding@resend.dev>",
        "to": ["recipient1@example.com", "recipient2@example.com"],
        "subject": mock_send.call_args[0][0]["subject"],
        "html": "<p>Test Body</p>"
    })

