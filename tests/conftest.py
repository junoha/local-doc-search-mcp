"""Shared test fixtures for local-doc-search-mcp."""

import pytest
import os
from unittest.mock import Mock
from langchain_core.documents import Document
from mcp_server.model import SearchResult


@pytest.fixture
def setup_environment():
    """Setup and teardown environment variables."""
    # Save original environment
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["EMBEDDING_MODEL_ID"] = "amazon.titan-embed-text-v2:0"
    os.environ["REGION_NAME"] = "us-west-2"
    os.environ["CHROMA_COLLECTION_NAME"] = "dbt_all_docs"
    os.environ["CHROMA_PERSIST_DIR"] = "./chroma_dbt_langchain_db"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_vector_store_fixture(monkeypatch):
    """Create a fixture for mocking the vector store."""
    mock_store = Mock()
    monkeypatch.setattr("mcp_server.server.vector_store", mock_store)
    return mock_store


@pytest.fixture
def mock_embeddings():
    """Mock for BedrockEmbeddings."""
    mock_embed = Mock()
    mock_embed.embed_query.return_value = [0.1, 0.2, 0.3]  # Mock embedding vector
    return mock_embed


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        Document(
            page_content="dbt Core is an open-source tool that enables data teams to transform data.",
            metadata={"source": "https://docs.getdbt.com/docs/introduction"},
            id="doc1",
        ),
        Document(
            page_content="Models are .sql files that select from sources or other models to create tables and views.",
            metadata={"source": "https://docs.getdbt.com/docs/build/models"},
            id="doc2",
        ),
    ]


@pytest.fixture
def mock_chroma(sample_documents):
    """Mock for Chroma vector store."""
    mock_vs = Mock()

    # Mock similarity_search_with_relevance_scores to return documents with scores
    mock_vs.similarity_search_with_relevance_scores.return_value = [
        (sample_documents[0], 0.95),
        (sample_documents[1], 0.85),
    ]

    return mock_vs
