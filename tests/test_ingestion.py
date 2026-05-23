import pytest
from unittest.mock import MagicMock, patch
from src.ingestion import fetch_weekly_updates

@patch("src.ingestion.Exa")
@patch("src.ingestion.is_article_sent")
def test_fetch_weekly_updates(mock_is_article_sent, mock_exa_class):
    # Set up client instance mock
    mock_exa_instance = MagicMock()
    mock_exa_class.return_value = mock_exa_instance
    
    # Mock Exa search results
    mock_result_1 = MagicMock()
    mock_result_1.url = "https://openai.com/blog/new-gpt"
    mock_result_1.title = "New GPT Release"
    mock_result_1.published_date = "2026-05-20T10:00:00Z"
    mock_result_1.text = "GPT-5 has been officially released."
    
    mock_result_2 = MagicMock()
    mock_result_2.url = "https://cursor.sh/blog/version-1"
    mock_result_2.title = "Cursor Version 1.0"
    mock_result_2.published_date = "2026-05-21T12:00:00Z"
    mock_result_2.text = "Cursor features new AI code generation modes."
    
    mock_response = MagicMock()
    mock_response.results = [mock_result_1, mock_result_2]
    mock_exa_instance.search.return_value = mock_response
    
    # Mock deduplication: first URL is new, second URL is already sent
    mock_is_article_sent.side_effect = lambda db, url: url == "https://cursor.sh/blog/version-1"
    
    with patch.dict("os.environ", {"EXA_API_KEY": "test_key"}):
        results = fetch_weekly_updates(db_path="mock.db", days_back=7)
        
    # Asserting that only the non-duplicate OpenAI article remains
    assert len(results) == 1
    assert results[0]["url"] == "https://openai.com/blog/new-gpt"
    assert results[0]["title"] == "New GPT Release"
    assert results[0]["company"] == "OpenAI"
    assert results[0]["markdown"] == "GPT-5 has been officially released."
    
    # Verify Exa client was initialized and searched correctly
    mock_exa_class.assert_called_once_with(api_key="test_key")
    mock_exa_instance.search.assert_called_once()
