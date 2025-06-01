"""Tests for the server functionality."""

from mcp_server.server import search_local_docs


def test_search_local_docs_valid(mock_vector_store_fixture, sample_documents):
    """Test search_local_docs with valid parameters."""
    mock_vector_store_fixture.similarity_search_with_relevance_scores.return_value = [
        (sample_documents[0], 0.95),
        (sample_documents[1], 0.85),
    ]

    results = search_local_docs(query="dbt models", k="2")

    assert len(results) == 2
    assert results[0].score == 0.95
    assert results[1].score == 0.85
    assert "dbt Core" in results[0].content
    assert "Models are" in results[1].content

    # Verify mock was called correctly
    mock_vector_store_fixture.similarity_search_with_relevance_scores.assert_called_once_with(
        query="dbt models", k=2
    )


def test_search_local_docs_invalid_k(mock_vector_store_fixture):
    """Test search_local_docs with invalid k parameter."""
    # Call function with invalid k
    results = search_local_docs("dbt models", "not-a-number")

    # Should return empty list due to ValueError
    assert results == []

    # Verify mock was not called
    mock_vector_store_fixture.similarity_search_with_relevance_scores.assert_not_called()


def test_search_local_docs_empty_results(mock_vector_store_fixture):
    """Test search_local_docs with no results."""
    # Setup mock to return empty list
    mock_vector_store_fixture.similarity_search_with_relevance_scores.return_value = []

    # Call function
    results = search_local_docs("nonexistent query", "5")

    # Should return empty list
    assert results == []


def test_search_local_docs_exception(mock_vector_store_fixture):
    """Test search_local_docs error handling."""
    # Setup mock to raise exception
    mock_vector_store_fixture.similarity_search_with_relevance_scores.side_effect = (
        Exception("Test error")
    )

    # Call function
    results = search_local_docs("query", "5")

    # Should return empty list due to exception handling
    assert results == []
