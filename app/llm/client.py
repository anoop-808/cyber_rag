"""LLM Interface for CyberRAG."""

import logging
import time
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    RetryCallState,
    Retrying
)

from app.core.config import config

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Base exception for LLM-related errors."""


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""


class LLMTimeoutError(LLMError):
    """Raised when an LLM request times out."""


class LLMProviderError(LLMError):
    """Raised when the LLM provider returns an error."""


def _is_transient_error(exc: Exception) -> bool:
    """Check if an exception is a transient error that should be retried."""
    if isinstance(exc, httpx.TimeoutException):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        # Retry on 5xx errors (server errors) or 429 (Too Many Requests)
        return exc.response.status_code >= 500 or exc.response.status_code == 429
    if isinstance(exc, httpx.NetworkError):
        return True
    return False


def generate_response(system_prompt: str, user_prompt: str) -> str:
    """Generate a response from the configured language model.

    Parameters
    ----------
    system_prompt : str
        The system prompt providing context and rules.
    user_prompt : str
        The user prompt containing the question and formatted context.

    Returns
    -------
    str
        The raw response text from the language model.

    Raises
    ------
    LLMConfigurationError
        If required configuration (like API key for OpenRouter) is missing.
    LLMTimeoutError
        If the request times out after all retries.
    LLMProviderError
        If the provider returns a non-transient error or invalid response.
    LLMError
        For other unexpected errors.
    """
    provider = config.LLM_PROVIDER.lower()
    model = config.LLM_MODEL
    base_url = config.LLM_BASE_URL.rstrip("/")
    api_key = getattr(config, "OPENROUTER_API_KEY", None)

    if provider == "openrouter" and not api_key:
        raise LLMConfigurationError("OPENROUTER_API_KEY is required for OpenRouter provider.")

    headers = {
        "Content-Type": "application/json"
    }

    if provider == "openrouter":
        headers["Authorization"] = f"Bearer {api_key}"
        headers["HTTP-Referer"] = "https://github.com/cyberrag/cyberrag"
        headers["X-Title"] = config.APP_NAME

        # Adjust endpoint path if not already included in base_url
        if not base_url.endswith("/chat/completions"):
            endpoint = f"{base_url}/chat/completions"
        else:
            endpoint = base_url
    else:
        # Default OpenAI compatible endpoint
        if not base_url.endswith("/chat/completions"):
            endpoint = f"{base_url}/chat/completions"
        else:
            endpoint = base_url

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": config.LLM_TEMPERATURE,
        "max_tokens": config.LLM_MAX_TOKENS,
    }

    logger.info(f"Starting LLM request to provider='{provider}', model='{model}'")
    start_time = time.time()

    def do_request() -> httpx.Response:
        try:
            with httpx.Client(timeout=config.LLM_TIMEOUT) as client:
                response = client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            if not _is_transient_error(e):
                raise LLMProviderError(f"Provider error {e.response.status_code}: {e.response.text}") from e
            raise # Re-raise transient errors for retry
        except httpx.RequestError as e:
            if not _is_transient_error(e):
                raise LLMProviderError(f"Request failed: {str(e)}") from e
            raise

    try:
        for attempt in Retrying(
            stop=stop_after_attempt(config.LLM_MAX_RETRIES),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError, httpx.NetworkError)),
            reraise=True
        ):
            with attempt:
                response = do_request()

    except httpx.TimeoutException as e:
        logger.error(f"LLM request timed out after {config.LLM_MAX_RETRIES} attempts.")
        raise LLMTimeoutError(f"Request timed out after {config.LLM_MAX_RETRIES} attempts.") from e
    except (httpx.HTTPStatusError, httpx.NetworkError) as e:
        logger.error(f"LLM request failed after {config.LLM_MAX_RETRIES} attempts: {str(e)}")
        raise LLMProviderError(f"Provider request failed: {str(e)}") from e
    except LLMError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during LLM request: {str(e)}")
        raise LLMError(f"Unexpected error: {str(e)}") from e

    duration = time.time() - start_time
    logger.info(f"LLM request completed in {duration:.2f}s")

    try:
        data = response.json()
        if not data:
            raise ValueError("Empty response from provider")
        if "choices" not in data or not data["choices"]:
            raise ValueError("Invalid response format: missing 'choices'")

        content = data["choices"][0]["message"]["content"]
        if content is None:
            return ""
        return content
    except Exception as e:
        raise LLMProviderError(f"Failed to parse provider response: {str(e)}") from e

