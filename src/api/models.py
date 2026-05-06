"""
API Request and Response Models Module.

Defines the Pydantic schemas used by the FastAPI endpoints
for request validation and response serialization.

Usage:
    from src.api.models import AnalysisRequest, AnalysisResponse
"""

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Schema for incoming analysis requests."""

    query: str = Field(
        ...,
        description="Natural language query about a stock (e.g., 'Tell me about NVDA').",
        min_length=3,
        max_length=500
    )


class AnalysisResponse(BaseModel):
    """Schema for the analysis response returned to the client."""

    ticker: str = Field(
        ...,
        description="The extracted stock ticker symbol."
    )
    report: str = Field(
        ...,
        description="The full markdown investment report."
    )
    blob_url: str = Field(
        ...,
        description="Azure Blob Storage URL where the report is saved."
    )
    status: str = Field(
        default="success",
        description="Status of the analysis request."
    )


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    status: str = Field(default="error")
    message: str = Field(..., description="Description of the error.")