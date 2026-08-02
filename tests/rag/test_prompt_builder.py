"""Tests for the Prompt Builder."""

import pytest
from app.rag.prompt_builder import build_prompt, DEFAULT_SYSTEM_TEMPLATE, DEFAULT_USER_TEMPLATE

def test_empty_query_raises_value_error():
    """Test that an empty query raises a ValueError."""
    with pytest.raises(ValueError, match="Query cannot be empty."):
        build_prompt(query="", context="Valid context")

    with pytest.raises(ValueError, match="Query cannot be empty."):
        build_prompt(query="   ", context="Valid context")

def test_empty_context_raises_value_error():
    """Test that an empty context raises a ValueError."""
    with pytest.raises(ValueError, match="Context cannot be empty."):
        build_prompt(query="Valid query", context="")

    with pytest.raises(ValueError, match="Context cannot be empty."):
        build_prompt(query="Valid query", context="   ")

def test_invalid_input_types_raise_type_error():
    """Test that non-string inputs raise a TypeError."""
    with pytest.raises(TypeError, match="Query and context must be strings."):
        build_prompt(query=None, context="Valid context")

    with pytest.raises(TypeError, match="Query and context must be strings."):
        build_prompt(query="Valid query", context=123)

def test_valid_prompt_generation():
    """Test standard prompt generation with defaults."""
    query = "How does CVE-2024-1234 work?"
    context = "[CVE-2024-1234]\nDescription:\nBuffer overflow."

    result = build_prompt(query=query, context=context)

    assert result["system"] == DEFAULT_SYSTEM_TEMPLATE
    expected_user = DEFAULT_USER_TEMPLATE.format(query=query, context=context)
    assert result["user"] == expected_user

def test_deterministic_output():
    """Test that identical inputs always produce identical output."""
    query = "How does CVE-2024-1234 work?"
    context = "[CVE-2024-1234]\nDescription:\nBuffer overflow."

    result1 = build_prompt(query=query, context=context)
    result2 = build_prompt(query=query, context=context)
    result3 = build_prompt(query=query, context=context)

    assert result1 == result2
    assert result2 == result3

def test_prompt_size_limit_exceeded_raises_value_error():
    """Test that prompt generation fails if max_size is exceeded."""
    query = "Q"
    context = "C"

    # Calculate the size that would be generated without max_size
    result = build_prompt(query=query, context=context)
    total_size = len(result["system"]) + len(result["user"])

    # Set max_size to just below the required size
    with pytest.raises(ValueError, match="exceeds maximum allowed size"):
        build_prompt(query=query, context=context, max_size=total_size - 1)

    # Set max_size to exactly the required size, should not raise
    build_prompt(query=query, context=context, max_size=total_size)

def test_configurable_templates():
    """Test using custom templates for system and user prompts."""
    query = "Query"
    context = "Context"

    custom_system = "You are a custom assistant."
    custom_user = "Q: {query} | C: {context}"

    result = build_prompt(
        query=query,
        context=context,
        system_template=custom_system,
        user_template=custom_user
    )

    assert result["system"] == custom_system
    assert result["user"] == "Q: Query | C: Context"
