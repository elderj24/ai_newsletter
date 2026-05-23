import pytest
from unittest.mock import MagicMock, patch
from src.synthesis import synthesize_articles

@patch("src.synthesis.genai.Client")
def test_synthesize_articles_success(mock_client_class):
    # Set up Client mock
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance
    
    # Mock generation response
    mock_response = MagicMock()
    mock_response.text = "# Strategic Newsletter Output"
    mock_client_instance.models.generate_content.return_value = mock_response
    
    test_articles = [
        {
            "url": "https://openai.com/blog/1",
            "title": "GPT-5 Launch",
            "published_date": "2026-05-23",
            "markdown": "Detailed content here.",
            "company": "OpenAI"
        }
    ]
    
    with patch.dict("os.environ", {"GEMINI_API_KEY": "test_gemini_key"}):
        result = synthesize_articles(test_articles)
        
    assert result == "# Strategic Newsletter Output"
    mock_client_class.assert_called_once_with(api_key="test_gemini_key")
    mock_client_instance.models.generate_content.assert_called_once()

def test_synthesize_articles_empty():
    # Verify that an empty article list skips the LLM call and returns a graceful message
    result = synthesize_articles([])
    assert "No new corporate announcements or product updates" in result
