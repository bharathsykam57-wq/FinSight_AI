"""
Web Scraping & Sentiment Extraction Module.

Classes:
    SentimentSearchTool: Searches the web for recent news articles.
"""

from typing import Any, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from firecrawl import FirecrawlApp
from src.shared.config import settings


class FirecrawlSearchInput(BaseModel):
    """Input schema for the SentimentSearchTool."""

    query: str = Field(
        ...,
        description="The search query string (e.g., 'NVDA recent analyst ratings')."
    )


class SentimentSearchTool(BaseTool):
    """Searches the web for latest news and sentiment using Firecrawl."""

    name: str = "Search Stock News"
    description: str = (
        "Searches the web for the latest news, analyst ratings, and market sentiment "
        "surrounding a specific stock or financial topic. "
        "Returns a summary of the top 3 relevant articles."
    )
    args_schema: Type[BaseModel] = FirecrawlSearchInput

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """Execute web search via Firecrawl and return scraped content."""
        query = kwargs.get("query") or (args[0] if args else None)

        if not settings.firecrawl_api_key:
            return "Error: FIRECRAWL_API_KEY is missing in configuration."

        try:
            app = FirecrawlApp(api_key=settings.firecrawl_api_key)
            results = app.search(
                query=query,
                limit=3,
                scrape_options={"formats": ["markdown"]}
            )
            return str(results)

        except (ValueError, ConnectionError, RuntimeError) as e:
            return f"Error executing Firecrawl search for query '{query}': {str(e)}"
        