"""
API Routes Module.

Defines the /analyze endpoint that accepts a natural language query,
extracts the ticker, runs the CrewAI pipeline, uploads the report to
Azure Blob Storage, and saves it to Azure PostgreSQL.

Usage:
    Registered automatically via src/api/main.py
"""

import re
from fastapi import APIRouter, HTTPException
from src.api.models import AnalysisRequest, AnalysisResponse, ErrorResponse
from src.agents.crew import FinSightCrew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService


router = APIRouter()


def extract_ticker(query: str) -> str:
    """
    Extracts a stock ticker symbol from a natural language query.

    Looks for 1-5 uppercase letters. Falls back to the last
    uppercase word in the query if no match is found.

    Args:
        query: Natural language string (e.g., 'Tell me about NVDA stock').

    Returns:
        Extracted ticker symbol in uppercase.

    Raises:
        ValueError: If no ticker can be extracted from the query.
    """
    match = re.search(r'\b[A-Z]{1,5}\b', query)
    if match:
        return match.group(0)

    words = query.upper().split()
    if words:
        return words[-1]

    raise ValueError(f"Could not extract a ticker from query: '{query}'")


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Run a full stock investment analysis",
    description=(
        "Accepts a natural language query, extracts the ticker symbol, "
        "runs the multi-agent CrewAI pipeline, uploads the report to "
        "Azure Blob Storage, and logs it to Azure PostgreSQL."
    )
)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """
    Main analysis endpoint.

    Args:
        request: AnalysisRequest containing the natural language query.

    Returns:
        AnalysisResponse with ticker, report, blob URL, and status.

    Raises:
        HTTPException: If ticker extraction or crew execution fails.
    """
    try:
        ticker = extract_ticker(request.query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        crew = FinSightCrew(ticker=ticker)
        report = crew.run()
    except (RuntimeError, ValueError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent pipeline failed: {str(e)}"
        ) from e

    report_filename = f"investment_report_{ticker}.md"
    blob_url = "unavailable"
    try:
        storage = StorageService()
        blob_url = storage.upload_file(report_filename, report_filename)
    except (RuntimeError, ValueError) as e:
        print(f"Warning: Blob upload failed: {e}")

    try:
        db = DatabaseService()
        db.save_report(ticker=ticker, content=report)
    except (RuntimeError, ValueError) as e:
        print(f"Warning: Database save failed: {e}")

    return AnalysisResponse(
        ticker=ticker,
        report=report,
        blob_url=blob_url,
        status="success"
    )