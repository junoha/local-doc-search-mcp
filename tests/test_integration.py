"""Integration tests for local-doc-search-mcp."""

import pytest
import os
from mcp_server.server import search_local_docs


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"), reason="Integration tests not enabled"
)
def test_search_integration():
    """Integration test with a real Chroma DB.

    This test is skipped by default. To run it, set the RUN_INTEGRATION_TESTS
    environment variable to any value.
    """
    # This test would use a small test database
    # It's marked to be skipped by default

    # Create test query
    query = "dbt models"

    # Call function
    results = search_local_docs(query, "3")

    # Basic assertions
    assert len(results) > 0
    for result in results:
        assert hasattr(result, "content")
        assert hasattr(result, "score")
        assert hasattr(result, "url")


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"), reason="Integration tests not enabled"
)
def test_search_integration_with_real_environment():
    """Integration test that uses the real Chroma vector store and Bedrock embeddings.

    This test is skipped by default and relies on properly configured AWS credentials
    and environment variables.
    """
    # Skip this test unless specifically enabled
    if not os.environ.get("RUN_REAL_AWS_TESTS"):
        pytest.skip("Test requires RUN_REAL_AWS_TESTS environment variable")

    # Use actual environment for vector store and embeddings
    query = "dbt models"

    # Call function and verify basic structure
    results = search_local_docs(query, "2")

    # We can't assert too much about actual results since they depend on the data
    assert isinstance(results, list)
    if results:  # If the database has data
        assert hasattr(results[0], "content")
        assert hasattr(results[0], "score")
