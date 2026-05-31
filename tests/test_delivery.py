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

@patch("src.delivery.smtplib.SMTP")
def test_send_newsletter_email_success(mock_smtp_class):
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value = mock_smtp_instance
    
    with patch.dict("os.environ", {
        "SMTP_SENDER": "sender@gmail.com",
        "SMTP_PASSWORD": "test_password"
    }):
        result = send_newsletter_email("<p>Test Body</p>", "recipient@example.com")
        
    assert result is True
    # Verify SMTP calls
    mock_smtp_class.assert_called_once_with("smtp.gmail.com", 587)
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with("sender@gmail.com", "test_password")
    mock_smtp_instance.sendmail.assert_called_once()
    mock_smtp_instance.quit.assert_called_once()

@patch("src.delivery.smtplib.SMTP")
def test_send_newsletter_email_multiple_recipients(mock_smtp_class):
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value = mock_smtp_instance
    
    with patch.dict("os.environ", {
        "SMTP_SENDER": "sender@gmail.com",
        "SMTP_PASSWORD": "test_password"
    }):
        result = send_newsletter_email("<p>Test Body</p>", "recipient1@example.com, recipient2@example.com")
        
    assert result is True
    mock_smtp_class.assert_called_once_with("smtp.gmail.com", 587)
    mock_smtp_instance.sendmail.assert_called_once()
    
    # Asserting that both emails are in to_list passed to sendmail
    call_args = mock_smtp_instance.sendmail.call_args[0]
    assert call_args[0] == "sender@gmail.com"
    assert call_args[1] == ["recipient1@example.com", "recipient2@example.com"]


