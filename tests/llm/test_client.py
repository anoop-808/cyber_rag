"""Tests for the LLM Interface."""

import pytest
import httpx
from unittest.mock import patch, MagicMock

from app.llm.client import (
    generate_response,
    LLMError,
    LLMConfigurationError,
    LLMTimeoutError,
    LLMProviderError
)
from app.core.config import config


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    original_provider = config.LLM_PROVIDER
    original_api_key = getattr(config, "OPENROUTER_API_KEY", None)
    original_retries = config.LLM_MAX_RETRIES

    config.LLM_PROVIDER = "openrouter"
    config.OPENROUTER_API_KEY = "test_key"
    config.LLM_MAX_RETRIES = 1  # Speed up tests

    yield config

    config.LLM_PROVIDER = original_provider
    config.OPENROUTER_API_KEY = original_api_key
    config.LLM_MAX_RETRIES = original_retries


def test_generate_response_success(mock_config):
    """Test successful LLM inference."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Test response"
                }
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_response):
        response = generate_response("System prompt", "User prompt")
        assert response == "Test response"


def test_generate_response_timeout(mock_config):
    """Test handling of request timeout."""
    with patch("httpx.Client.post", side_effect=httpx.TimeoutException("Timeout", request=MagicMock())):
        with pytest.raises(LLMTimeoutError):
            generate_response("System prompt", "User prompt")


def test_generate_response_retry_success(mock_config):
    """Test retry logic on transient errors."""
    mock_success_response = MagicMock()
    mock_success_response.status_code = 200
    mock_success_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Test response after retry"
                }
            }
        ]
    }

    # Simulate a network error, then a success
    mock_error = httpx.NetworkError("Transient connection error", request=MagicMock())

    with patch("httpx.Client.post", side_effect=[mock_error, mock_success_response]):
        # Temporarily increase retries for this test
        original_retries = mock_config.LLM_MAX_RETRIES
        mock_config.LLM_MAX_RETRIES = 2
        try:
            response = generate_response("System prompt", "User prompt")
            assert response == "Test response after retry"
        finally:
            mock_config.LLM_MAX_RETRIES = original_retries


def test_generate_response_invalid_configuration(mock_config):
    """Test behavior when API key is missing for OpenRouter."""
    original_api_key = mock_config.OPENROUTER_API_KEY
    mock_config.OPENROUTER_API_KEY = None
    try:
        with pytest.raises(LLMConfigurationError):
            generate_response("System prompt", "User prompt")
    finally:
        mock_config.OPENROUTER_API_KEY = original_api_key


def test_generate_response_empty_response(mock_config):
    """Test handling of empty response from provider."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # Empty response

    with patch("httpx.Client.post", return_value=mock_response):
        with pytest.raises(LLMProviderError) as exc_info:
            generate_response("System prompt", "User prompt")
        assert "Empty response" in str(exc_info.value)


def test_generate_response_invalid_format(mock_config):
    """Test handling of invalid response format from provider."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invalid_key": "data"}

    with patch("httpx.Client.post", return_value=mock_response):
        with pytest.raises(LLMProviderError) as exc_info:
            generate_response("System prompt", "User prompt")
        assert "Invalid response format" in str(exc_info.value)


def test_generate_response_provider_error(mock_config):
    """Test handling of non-transient provider error (e.g. 400 Bad Request)."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"

    mock_error = httpx.HTTPStatusError("400 Bad Request", request=MagicMock(), response=mock_response)

    with patch("httpx.Client.post", side_effect=mock_error):
        with pytest.raises(LLMProviderError) as exc_info:
            generate_response("System prompt", "User prompt")
        assert "Provider error 400" in str(exc_info.value)
