"""LLM client for CyberRAG using the OpenRouter Chat Completions API."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_TIMEOUT_SECONDS = 60

SYSTEM_HEADER = "=== SYSTEM ==="
USER_QUERY_HEADER = "=== USER QUERY ==="


def _get_openrouter_config() -> tuple[str, str]:
    """Load required OpenRouter configuration from environment variables.

    Returns
    -------
    tuple of str
        API key and model name.

    Raises
    ------
    ValueError
        If a required environment variable is missing or empty.
    """
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")

    model = os.getenv("OPENROUTER_MODEL")
    if not model or not model.strip():
        raise ValueError("OPENROUTER_MODEL environment variable is not set.")

    return api_key.strip(), model.strip()


def _extract_response_text(response_data: dict[str, Any]) -> str:
    """Extract assistant response text from an OpenRouter API payload.

    Parameters
    ----------
    response_data : dict
        Parsed JSON response from the OpenRouter API.

    Returns
    -------
    str
        Generated response text from the model.

    Raises
    ------
    RuntimeError
        If the response does not contain a valid assistant message.
    """
    if "error" in response_data:
        error = response_data["error"]
        if isinstance(error, dict):
            message = error.get("message", error)
        else:
            message = error
        raise RuntimeError(f"OpenRouter API error: {message}")

    try:
        message_content = response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected OpenRouter API response format: {response_data}"
        ) from exc

    if message_content is None:
        raise RuntimeError("OpenRouter API returned an empty assistant message.")

    return str(message_content).strip()


def _build_messages(prompt: str) -> list[dict[str, str]]:
    """Build OpenRouter chat messages from a prompt string.

    When CyberRAG section headers are present, split the prompt into separate
    system and user messages. Otherwise, send the full prompt as one user
    message.

    Parameters
    ----------
    prompt : str
        Prompt text to convert into chat messages.

    Returns
    -------
    list of dict
        Messages payload for the OpenRouter Chat Completions API.
    """
    stripped_prompt = prompt.strip()

    if (
        SYSTEM_HEADER not in stripped_prompt
        or USER_QUERY_HEADER not in stripped_prompt
    ):
        return [{"role": "user", "content": stripped_prompt}]

    system_index = stripped_prompt.index(SYSTEM_HEADER)
    user_query_index = stripped_prompt.index(USER_QUERY_HEADER)

    if system_index >= user_query_index:
        return [{"role": "user", "content": stripped_prompt}]

    system_start = system_index + len(SYSTEM_HEADER)
    system_message = stripped_prompt[system_start:user_query_index].strip()
    user_message = stripped_prompt[
        user_query_index + len(USER_QUERY_HEADER):
    ].strip()

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]


def generate_response(prompt: str) -> str:
    """Send a prompt to the configured LLM and return the response text.

    Parameters
    ----------
    prompt : str
        Fully constructed prompt to send to the LLM.

    Returns
    -------
    str
        Generated response text from the LLM.

    Raises
    ------
    ValueError
        If ``prompt`` is empty or contains only whitespace, or if required
        OpenRouter configuration is missing.
    ConnectionError
        If a network error occurs while contacting the OpenRouter API.
    RuntimeError
        If the OpenRouter API returns an unexpected or error response.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty or contain only whitespace.")

    api_key, model = _get_openrouter_config()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": _build_messages(prompt),
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise ConnectionError(
            f"Failed to connect to OpenRouter API: {exc}"
        ) from exc

    try:
        response_data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"OpenRouter API returned non-JSON response: {response.text}"
        ) from exc

    if response.status_code != 200:
        if isinstance(response_data, dict) and "error" in response_data:
            error = response_data["error"]
            if isinstance(error, dict):
                message = error.get("message", error)
            else:
                message = error
            raise RuntimeError(
                f"OpenRouter API returned status {response.status_code}: {message}"
            )
        raise RuntimeError(
            f"OpenRouter API returned status {response.status_code}: {response.text}"
        )

    return _extract_response_text(response_data)
