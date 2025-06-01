"""local doc search MCP Server implementation."""

import os
from loguru import logger
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from mcp.server.fastmcp import FastMCP

# Import models
from mcp_server.model import SearchResult

# Initialize global variables
embeddings = None
vector_store = None
mcp = None


def get_embeddings():
    """Get or initialize embeddings model."""
    global embeddings
    if embeddings is None:
        embeddings = BedrockEmbeddings(
            model_id=os.environ.get(
                "EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"
            ),
            region_name=os.environ.get("REGION_NAME", "us-west-2"),
            client=None,
        )
    return embeddings


def get_vector_store():
    """Get or initialize vector store."""
    global vector_store
    if vector_store is None:
        # Use Chroma as the vector store for local documentation
        # Ensure the persist directory exists
        vector_store = Chroma(
            embedding_function=get_embeddings(),
            collection_name=os.environ.get("CHROMA_COLLECTION_NAME", "dbt_all_docs"),
            persist_directory=os.environ.get(
                "CHROMA_PERSIST_DIR", "/path/to/chroma_dbt_langchain_db"
            ),
        )
    return vector_store


def initialize_mcp():
    """Initialize MCP server."""
    global mcp
    if mcp is None:
        mcp = FastMCP(
            name="local-doc-search-mcp",
            instructions="""
            # local documentation search MCP
            This MCP server provides tools for searching documentation in local chroma index.
            The index is stored in English, so any queries non-English should first be translated into English.
            
            ## Capabilities
            - Search local documentation for specific terms or phrases
            - Retrieve relevant documentation snippets

            ## Use Cases
            - Documentation search for dbt projects
            - Developer assistance in finding dbt documentation
            """,
        )
    return mcp


# Initialize server components
mcp = initialize_mcp()


@mcp.tool(name="search_local_docs")
def search_local_docs(query: str, k: str) -> list[SearchResult]:
    """
    Search the local documentation for a given query
    Args:
        query (str): The search term to look for in the documentation.
        k (str): The number of results to return.
    Returns:
        str: A string containing the search results.
    """

    try:
        # Use get_vector_store() to ensure the vector store is initialized
        vs = get_vector_store()
        vector_search_results = vs.similarity_search_with_relevance_scores(
            query=query, k=int(k)
        )

        results: list[SearchResult] = []
        for doc, score in vector_search_results:
            results.append(
                SearchResult(
                    id=doc.id,
                    content=doc.page_content,
                    url=doc.metadata["source"],
                    score=score,
                )
            )

        # Sort results by score in descending order
        results.sort(key=lambda x: x.score, reverse=True)
        return results
    except ValueError as e:
        logger.error(f"Invalid input for search_docs: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching local documentation: {e}")
        return []
