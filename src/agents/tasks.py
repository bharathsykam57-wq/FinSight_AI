"""
Task Definitions Module.

Defines the two CrewAI tasks that form the FinSight AI pipeline:
    - Fundamental Analysis Task: Collects all raw financial data.
    - Report Generation Task: Synthesizes data into a markdown report.

Usage:
    from src.agents.tasks import FinancialTasks
    tasks = FinancialTasks()
    task1 = tasks.fundamental_analysis(agent, ticker)
"""

from crewai import Task
from crewai import Agent


class FinancialTasks:
    """Factory class for creating the FinSight AI task pipeline."""

    def fundamental_analysis(self, agent: Agent, ticker: str) -> Task:
        """
        Creates the data gathering task for the Quantitative Analyst.

        Args:
            agent: The agent responsible for executing this task.
            ticker: The stock ticker symbol to analyze (e.g., 'NVDA').

        Returns:
            A configured CrewAI Task instance.
        """
        return Task(
            description=(
                f"Perform a comprehensive financial analysis on {ticker}. "
                f"Use the available tools to:\n"
                f"1. Fetch fundamental metrics (P/E, Beta, Market Cap, EPS, etc.)\n"
                f"2. Compare {ticker} performance against a major benchmark (SPY)\n"
                f"3. Search for the latest news and analyst sentiment on {ticker}\n"
                f"Compile all findings into a structured summary for the strategist."
            ),
            expected_output=(
                f"A detailed structured summary of {ticker} including:\n"
                f"- Key fundamental metrics\n"
                f"- 1-year performance vs SPY\n"
                f"- Latest news headlines and sentiment\n"
                f"- Any notable risks or opportunities identified"
            ),
            agent=agent
        )

    def generate_report(
        self,
        agent: Agent,
        ticker: str,
        context: list
    ) -> Task:
        """
        Creates the report writing task for the Investment Strategist.

        Args:
            agent: The agent responsible for executing this task.
            ticker: The stock ticker symbol being reported on.
            context: List of upstream tasks whose output feeds into this task.

        Returns:
            A configured CrewAI Task instance.
        """
        return Task(
            description=(
                f"Using the quantitative analyst's findings, write a professional "
                f"investment report for {ticker}. The report must:\n"
                f"1. Start with an executive summary\n"
                f"2. Cover fundamental analysis findings\n"
                f"3. Address market sentiment and recent news\n"
                f"4. Identify key risks and opportunities\n"
                f"5. End with a clear BUY, HOLD, or SELL recommendation "
                f"with supporting rationale"
            ),
            expected_output=(
                f"A professional markdown investment report for {ticker} with:\n"
                f"- Executive Summary\n"
                f"- Fundamental Analysis\n"
                f"- Market Sentiment\n"
                f"- Risk & Opportunity Assessment\n"
                f"- Final Recommendation (BUY / HOLD / SELL)"
            ),
            agent=agent,
            context=context,
            output_file=f"investment_report_{ticker}.md"
        )