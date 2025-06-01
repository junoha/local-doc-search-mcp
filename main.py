"""Main entry point for the MCP server."""

from loguru import logger
from mcp_server.server import mcp


if __name__ == "__main__":
    logger.info("Starting MCP server in stdio mode")
    mcp.run(transport="stdio")
