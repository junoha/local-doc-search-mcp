"""Data models for local doc search MCP Server."""

from typing import Optional
from pydantic import BaseModel


class SearchResult(BaseModel):
    """Model for search results."""

    id: str
    content: str
    url: str
    score: float
