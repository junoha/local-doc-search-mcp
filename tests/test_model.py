"""Tests for the SearchResult model."""

from mcp_server.model import SearchResult
import pytest
from pydantic import ValidationError


def test_search_result_creation():
    """Test creating a valid SearchResult object."""
    result = SearchResult(
        id="test-id",
        content="Test content",
        url="https://example.com",
        score=0.95,
    )

    assert result.id == "test-id"
    assert result.content == "Test content"
    assert result.url == "https://example.com"
    assert result.score == 0.95


def test_search_result_validation():
    """Test validation of SearchResult object."""
    # Test with invalid score type
    with pytest.raises(ValidationError):
        SearchResult(
            id="test-id",
            content="Test content",
            url="https://example.com",
            score="not-a-float",  # Should be float
        )

    # Test with missing required field
    with pytest.raises(ValidationError):
        SearchResult(
            content="Test content",
            url="https://example.com",
            score=0.95,
            # Missing id field
        )
