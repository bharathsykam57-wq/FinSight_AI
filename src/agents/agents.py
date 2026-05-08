"""
Agent Definitions Module.

Defines the two CrewAI agents that power the FinSight AI pipeline:
    - Quantitative Analyst: Fetches hard financial data and metrics.
    - Investment Strategist: Interprets data and writes the final report.

Usage:
    from src.agents.agents import FinancialAgents
    agents = FinancialAgents()
    quant = agents.quantitative_analyst()
"""

import os
from crewai import Agent
from src.agents.tools.financial import FundamentalAnalysisTool, CompareStocksTool
from src.agents.tools.scraper import SentimentSearchTool
from src.shared.config import settings


class FinancialAgents:
    """Factory class for creating the FinSight AI agent workforce."""

    def __init__(self) -> None:
        """Initialize all tools and set OpenAI API key in environment."""
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key

        self.fundamental_tool = FundamentalAnalysisTool()
        self.compare_tool = CompareStocksTool()
        self.sentiment_tool = SentimentSearchTool()

    def quantitative_analyst(self) -> Agent:
        """
        Creates the Quantitative Analyst agent.

        Responsible for fetching raw financial metrics and stock
        performance comparisons using Yahoo Finance and Firecrawl.

        Returns:
            A configured CrewAI Agent instance.
        """
        return Agent(
            role="Senior Quantitative Analyst",
            goal=(
                "Gather and analyze comprehensive financial data for the requested "
                "stock, including fundamental metrics, recent price performance, "
                "and relevant market sentiment from news sources."
            ),
            backstory=(
                "You are a seasoned quantitative analyst at a top-tier hedge fund. "
                "You have 15 years of experience extracting actionable signals from "
                "financial data. You are methodical, precise, and never speculate "
                "without data to back it up."
            ),
            tools=[
                self.fundamental_tool,
                self.compare_tool,
                self.sentiment_tool
            ],
            llm=settings.openai_model_name,
            verbose=True
        )

    def investment_strategist(self) -> Agent:
        """
        Creates the Investment Strategist agent.

        Responsible for synthesizing the analyst's findings into a
        structured markdown investment report with a clear recommendation.

        Returns:
            A configured CrewAI Agent instance.
        """
        return Agent(
            role="Chief Investment Strategist",
            goal=(
                "Synthesize the quantitative analyst's findings into a clear, "
                "professional investment report with a definitive BUY, HOLD, "
                "or SELL recommendation supported by evidence."
            ),
            backstory=(
                "You are the Chief Investment Strategist at a leading asset "
                "management firm. You are known for translating complex financial "
                "data into compelling, clear narratives that drive investment "
                "decisions. Your reports are trusted by portfolio managers worldwide."
            ),
            tools=[],
            llm=settings.openai_model_name,
            verbose=True
        )