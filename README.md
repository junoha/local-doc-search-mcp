# Local Documentation Search MCP

A Model Context Protocol (MCP) server for local document searching. This tool primarily provides vector search for dbt documentation, but allowing developers to efficiently search for any public OSS document.

## Key Features

- Efficient vector search for local indexed documentation
- Ranking of search results based on relevance scores
- Easy integration with AI assistants through MCP

## Setup

### Requirements

- Python 3.12 or higher
- AWS credentials (for accessing Bedrock service)

### Installation Requirements

Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)

### Installation

```bash
$ uv sync
```

## Usage

Here are mcp.json format.

```json
{
  "mcpServers": {
    "local-doc-search-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/local-doc-search-mcp",
        "run",
        "main.py"
      ],
      "env": {
        "AWS_PROFILE": "<profile-name>",
        "AWS_REGION": "<Bedrock-model-region>",
        "CHROMA_PERSIST_DIR": "<persisted-chrome-index-directory-path>",
        "CHROMA_COLLECTION_NAME": "<chroma-index-name>"
      },
      "autoApprove": ["search_local_docs"]
    }
  }
}
```

For example:

```json
{
  "mcpServers": {
    "local-doc-search-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/local-doc-search-mcp",
        "run",
        "main.py"
      ],
      "env": {
        "AWS_PROFILE": "sandbox",
        "AWS_REGION": "us-west-2",
        "CHROMA_PERSIST_DIR": "/path/to/local-doc-search-mcp/chroma_dbt_langchain_db",
        "CHROMA_COLLECTION_NAME": "dbt_all_docs"
      },
      "autoApprove": ["search_local_docs"]
    }
  }
}
```

## Tools

### search_local_docs

```py
def search_local_docs(query: str, k: str) -> list[SearchResult]:
    """
    Search the local documentation for a given query
    Args:
        query (str): The search term to look for in the documentation.
        k (str): The number of results to return.
    Returns:
        str: A string containing the search results.
   """
```


## Vector Database Preparation

For information on how to vectorize documents and store them in Chroma, refer to `prepare_chroma_persist_db/dbt_docs.ipynb`. You can share chroma index directory to other user to skip Bedrock embedding and building index.

## Testing

This document provides instructions for running and extending the test suite for the local Documentation Search MCP.

### Test Structure

The tests are organized as follows:

- `tests/test_model.py`: Tests for the `SearchResult` model
- `tests/test_server.py`: Tests for the `search_local_docs` functionality with mocked dependencies
- `tests/test_integration.py`: Optional integration tests that require a real vector database (disabled by default)
- `tests/conftest.py`: Shared fixtures and test utilities

### Running Tests

#### Run with Coverage

To run tests with coverage reporting:

```bash
uv run pytest --cov=mcp_server
```

### Integration Tests

Integration tests are skipped by default because they require a real Chroma vector database and AWS Bedrock credentials.

To run integration tests:

1. Set up the required environment variables:
   ```bash
   export RUN_INTEGRATION_TESTS=1
   export EMBEDDING_MODEL_ID="amazon.titan-embed-text-v2:0"
   export REGION_NAME="us-west-2"
   export CHROMA_COLLECTION_NAME="dbt_all_docs"
   export CHROMA_PERSIST_DIR="/path/to/your/chroma_db"
   ```

2. Run the integration tests:
   ```bash
   uv run pytest tests/test_integration.py
   ```

## Adding New Tests

When adding new tests, follow these guidelines:

1. Use fixtures from `conftest.py` when possible
2. Mock external dependencies like Chroma and Bedrock
3. Group related tests in the same file
4. Follow the naming convention: `test_<function_name>_<scenario>`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
