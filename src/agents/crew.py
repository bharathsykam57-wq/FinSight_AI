"""
Crew Orchestration Module.

Assembles the FinSight AI agents and tasks into a sequential CrewAI
pipeline and exposes a single run() method to execute the full analysis.

Usage:
    from src.agents.crew import FinSightCrew
    crew = FinSightCrew(ticker="NVDA")
    result = crew.run()
"""

from crewai import Crew, Process
from src.agents.agents import FinancialAgents
from src.agents.tasks import FinancialTasks


class FinSightCrew:
    """Orchestrates the full FinSight AI analysis pipeline for a given ticker."""

    def __init__(self, ticker: str) -> None:
        """
        Initializes the crew with the target stock ticker.

        Args:
            ticker: The stock ticker symbol to analyze (e.g., 'NVDA').
        """
        self.ticker = ticker.upper()
        self.agents = FinancialAgents()
        self.tasks = FinancialTasks()

    def run(self) -> str:
        """
        Assembles and executes the full analysis pipeline.

        Returns:
            The final markdown investment report as a string.
        """
        # --- Build Agents ---
        quant = self.agents.quantitative_analyst()
        strategist = self.agents.investment_strategist()

        # --- Build Tasks ---
        analysis_task = self.tasks.fundamental_analysis(
            agent=quant,
            ticker=self.ticker
        )
        report_task = self.tasks.generate_report(
            agent=strategist,
            ticker=self.ticker,
            context=[analysis_task]
        )

        # --- Assemble Crew ---
        crew = Crew(
            agents=[quant, strategist],
            tasks=[analysis_task, report_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)