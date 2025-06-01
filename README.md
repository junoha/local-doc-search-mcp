## Testing the local Documentation Search MCP

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
