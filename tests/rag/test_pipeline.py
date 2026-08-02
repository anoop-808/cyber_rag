import pytest
from unittest.mock import patch, MagicMock

from app.rag.pipeline import generate_answer

@pytest.fixture
def mock_documents():
    return [
        {
            "id": "CVE-2024-1234",
            "description": "Test vulnerability.",
            "metadata": {"severity": "HIGH", "cvss_score": 8.5}
        }
    ]

@pytest.fixture
def mock_context():
    return "[CVE-2024-1234]\nDescription:\nTest vulnerability."

@pytest.fixture
def mock_prompts():
    return {
        "system": "System prompt.",
        "user": "User prompt."
    }

@pytest.fixture
def mock_llm_response():
    return "This is the generated answer."

@pytest.fixture
def mock_formatted_response():
    return {
        "answer": "This is the generated answer.",
        "sources": ["CVE-2024-1234"],
        "metadata": [{"id": "CVE-2024-1234"}],
        "formatted_text": "Answer\n\nThis is the generated answer.\n\nSources\n\n- CVE-2024-1234"
    }

@patch("app.rag.pipeline.format_response")
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.build_prompt")
@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_success(
    mock_retrieve, mock_build_context, mock_build_prompt,
    mock_generate_response, mock_format_response,
    mock_documents, mock_context, mock_prompts,
    mock_llm_response, mock_formatted_response
):
    # Setup mocks
    mock_retrieve.return_value = mock_documents
    mock_build_context.return_value = mock_context
    mock_build_prompt.return_value = mock_prompts
    mock_generate_response.return_value = mock_llm_response
    mock_format_response.return_value = mock_formatted_response

    query = "What is CVE-2024-1234?"
    filters = {"severity": "HIGH"}

    # Execute
    result = generate_answer(query, filters=filters)

    # Assertions
    assert result == mock_formatted_response

    # Verify calls
    mock_retrieve.assert_called_once_with(query=query, filters=filters)
    mock_build_context.assert_called_once_with(retrieved_documents=mock_documents)
    mock_build_prompt.assert_called_once_with(query=query, context=mock_context)
    mock_generate_response.assert_called_once_with(
        system_prompt=mock_prompts["system"],
        user_prompt=mock_prompts["user"]
    )
    mock_format_response.assert_called_once_with(
        llm_response=mock_llm_response,
        retrieved_documents=mock_documents
    )

def test_generate_answer_empty_query():
    with pytest.raises(ValueError, match="Query cannot be empty."):
        generate_answer("")

    with pytest.raises(ValueError, match="Query cannot be empty."):
        generate_answer("   ")

@patch("app.rag.pipeline.retrieve")
def test_generate_answer_retrieval_failure(mock_retrieve):
    mock_retrieve.side_effect = Exception("Database connection failed")

    with pytest.raises(RuntimeError, match="Retrieval failed: Database connection failed"):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.retrieve")
def test_generate_answer_empty_retrieval(mock_retrieve):
    mock_retrieve.return_value = []

    with pytest.raises(ValueError, match="No relevant documents found for the given query."):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_context_builder_failure(mock_retrieve, mock_build_context, mock_documents):
    mock_retrieve.return_value = mock_documents
    mock_build_context.side_effect = Exception("Context error")

    with pytest.raises(RuntimeError, match="Context building failed: Context error"):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_empty_context(mock_retrieve, mock_build_context, mock_documents):
    mock_retrieve.return_value = mock_documents
    mock_build_context.return_value = ""

    with pytest.raises(ValueError, match="Failed to build context from retrieved documents."):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.build_prompt")
@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_prompt_builder_failure(mock_retrieve, mock_build_context, mock_build_prompt, mock_documents, mock_context):
    mock_retrieve.return_value = mock_documents
    mock_build_context.return_value = mock_context
    mock_build_prompt.side_effect = Exception("Prompt error")

    with pytest.raises(RuntimeError, match="Prompt generation failed: Prompt error"):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.build_prompt")
@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_llm_failure(mock_retrieve, mock_build_context, mock_build_prompt, mock_generate_response, mock_documents, mock_context, mock_prompts):
    mock_retrieve.return_value = mock_documents
    mock_build_context.return_value = mock_context
    mock_build_prompt.return_value = mock_prompts
    mock_generate_response.side_effect = Exception("LLM error")

    with pytest.raises(RuntimeError, match="LLM generation failed: LLM error"):
        generate_answer("What is CVE-2024-1234?")

@patch("app.rag.pipeline.format_response")
@patch("app.rag.pipeline.generate_response")
@patch("app.rag.pipeline.build_prompt")
@patch("app.rag.pipeline.build_context")
@patch("app.rag.pipeline.retrieve")
def test_generate_answer_formatter_failure(mock_retrieve, mock_build_context, mock_build_prompt, mock_generate_response, mock_format_response, mock_documents, mock_context, mock_prompts, mock_llm_response):
    mock_retrieve.return_value = mock_documents
    mock_build_context.return_value = mock_context
    mock_build_prompt.return_value = mock_prompts
    mock_generate_response.return_value = mock_llm_response
    mock_format_response.side_effect = Exception("Formatter error")

    with pytest.raises(RuntimeError, match="Response formatting failed: Formatter error"):
        generate_answer("What is CVE-2024-1234?")

def test_generate_answer_deterministic_output(
    mock_documents, mock_context, mock_prompts, mock_llm_response, mock_formatted_response
):
    # Verify the orchestration maintains identical output for same inputs across multiple runs
    with patch("app.rag.pipeline.retrieve") as mock_retrieve, \
         patch("app.rag.pipeline.build_context") as mock_build_context, \
         patch("app.rag.pipeline.build_prompt") as mock_build_prompt, \
         patch("app.rag.pipeline.generate_response") as mock_generate_response, \
         patch("app.rag.pipeline.format_response") as mock_format_response:

        mock_retrieve.return_value = mock_documents
        mock_build_context.return_value = mock_context
        mock_build_prompt.return_value = mock_prompts
        mock_generate_response.return_value = mock_llm_response
        mock_format_response.return_value = mock_formatted_response

        result1 = generate_answer("What is CVE-2024-1234?")
        result2 = generate_answer("What is CVE-2024-1234?")

        assert result1 == result2 == mock_formatted_response
