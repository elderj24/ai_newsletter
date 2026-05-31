import pytest
from unittest.mock import MagicMock, patch
from src.ingestion import fetch_weekly_updates, fetch_geopolitics_news, fetch_local_news


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

    mock_result_3 = MagicMock()
    mock_result_3.url = "https://blogs.nvidia.com/blog/new-gpu"
    mock_result_3.title = "New GPU Architecture"
    mock_result_3.published_date = "2026-05-22T08:00:00Z"
    mock_result_3.text = "NVIDIA introduces new AI accelerators."
    
    mock_response = MagicMock()
    mock_response.results = [mock_result_1, mock_result_2, mock_result_3]
    mock_exa_instance.search.return_value = mock_response
    
    # Mock deduplication: first and third URLs are new, second URL is already sent
    mock_is_article_sent.side_effect = lambda db, url: url == "https://cursor.sh/blog/version-1"
    
    with patch.dict("os.environ", {"EXA_API_KEY": "test_key"}):
        results = fetch_weekly_updates(db_path="mock.db", days_back=7)
        
    # Asserting that only the non-duplicate OpenAI and NVIDIA articles remain
    assert len(results) == 2
    assert results[0]["url"] == "https://openai.com/blog/new-gpt"
    assert results[0]["title"] == "New GPT Release"
    assert results[0]["company"] == "OpenAI"
    assert results[0]["markdown"] == "GPT-5 has been officially released."

    assert results[1]["url"] == "https://blogs.nvidia.com/blog/new-gpu"
    assert results[1]["title"] == "New GPU Architecture"
    assert results[1]["company"] == "NVIDIA"
    assert results[1]["markdown"] == "NVIDIA introduces new AI accelerators."
    
    # Verify Exa client was initialized and searched correctly
    mock_exa_class.assert_called_once_with(api_key="test_key")
    mock_exa_instance.search.assert_called_once()

@patch("src.ingestion.Exa")
@patch("src.ingestion.is_article_sent")
def test_fetch_geopolitics_news(mock_is_article_sent, mock_exa_class):
    mock_exa_instance = MagicMock()
    mock_exa_class.return_value = mock_exa_instance
    
    mock_result = MagicMock()
    mock_result.url = "https://reuters.com/world/some-geopolitics"
    mock_result.title = "Global Trade Deal Signed"
    mock_result.published_date = "2026-05-20T10:00:00Z"
    mock_result.text = "A new trade agreement has been signed by major global powers."
    
    mock_response = MagicMock()
    mock_response.results = [mock_result]
    mock_exa_instance.search.return_value = mock_response
    
    mock_is_article_sent.return_value = False
    
    with patch.dict("os.environ", {"EXA_API_KEY": "test_key"}):
        results = fetch_geopolitics_news(db_path="mock.db", days_back=7)
        
    assert len(results) == 1
    assert results[0]["url"] == "https://reuters.com/world/some-geopolitics"
    assert results[0]["title"] == "Global Trade Deal Signed"
    assert results[0]["source"] == "Geopolitics"
    assert results[0]["markdown"] == "A new trade agreement has been signed by major global powers."

@patch("src.ingestion.Exa")
@patch("src.ingestion.is_article_sent")
def test_fetch_local_news(mock_is_article_sent, mock_exa_class):
    mock_exa_instance = MagicMock()
    mock_exa_class.return_value = mock_exa_instance
    
    mock_result_chicago = MagicMock()
    mock_result_chicago.url = "https://chicagotribune.com/news/1"
    mock_result_chicago.title = "Chicago City Council Votes on Budget"
    mock_result_chicago.published_date = "2026-05-20T10:00:00Z"
    mock_result_chicago.text = "The Chicago city council passed a new fiscal plan."
    
    mock_result_naperville = MagicMock()
    mock_result_naperville.url = "https://dailyherald.com/naperville/2"
    mock_result_naperville.title = "Naperville Library Event"
    mock_result_naperville.published_date = "2026-05-21T12:00:00Z"
    mock_result_naperville.text = "The local library in Naperville hosts a tech workshop."

    mock_result_illinois = MagicMock()
    mock_result_illinois.url = "https://illinois.gov/news/3"
    mock_result_illinois.title = "Illinois State Park Upgrades"
    mock_result_illinois.published_date = "2026-05-22T08:00:00Z"
    mock_result_illinois.text = "The state of Illinois announced major park renovations."
    
    mock_response = MagicMock()
    mock_response.results = [mock_result_chicago, mock_result_naperville, mock_result_illinois]
    mock_exa_instance.search.return_value = mock_response
    
    mock_is_article_sent.return_value = False
    
    with patch.dict("os.environ", {"EXA_API_KEY": "test_key"}):
        results = fetch_local_news(db_path="mock.db", days_back=7)
        
    assert len(results) == 3
    
    # Assert locations are parsed correctly
    assert results[0]["location"] == "Chicago"
    assert results[1]["location"] == "Naperville"
    assert results[2]["location"] == "Illinois"

