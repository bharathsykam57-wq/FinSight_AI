"""
CLI Entry Point for FinSight AI.

Runs the full multi-agent analysis pipeline from the command line,
uploads the generated report to Azure Blob Storage, and saves
it to Azure PostgreSQL.

Run with:
    uv run python main.py
"""

import sys
from src.agents.crew import FinSightCrew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService


def main() -> None:
    """Execute the full FinSight AI pipeline from the command line."""
    print("========================================")
    print("         FinSight AI - CLI Mode         ")
    print("========================================\n")

    ticker = input("Enter stock ticker to analyze (e.g. NVDA): ").strip().upper()

    if not ticker:
        print("Error: Ticker cannot be empty.")
        sys.exit(1)

    print(f"\nStarting multi-agent analysis for {ticker}...\n")

    try:
        crew = FinSightCrew(ticker=ticker)
        report = crew.run()
    except (RuntimeError, ValueError) as e:
        print(f"Error running analysis: {e}")
        sys.exit(1)

    print("\n--- Report Generated ---\n")
    print(report)

    report_filename = f"investment_report_{ticker}.md"

    print("\nUploading report to Azure Blob Storage...")
    try:
        storage = StorageService()
        blob_url = storage.upload_file(report_filename, report_filename)
        print(f"Report uploaded: {blob_url}")
    except (RuntimeError, ValueError) as e:
        print(f"Warning: Blob upload failed: {e}")

    print("\nSaving report to Azure PostgreSQL...")
    try:
        db = DatabaseService()
        db.save_report(ticker=ticker, content=report)
        print("Report saved to database.")
    except (RuntimeError, ValueError) as e:
        print(f"Warning: Database save failed: {e}")

    print("\n========================================")
    print(f"  Analysis complete for {ticker}!")
    print("========================================")


if __name__ == "__main__":
    main()