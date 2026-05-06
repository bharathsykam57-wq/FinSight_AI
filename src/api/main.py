"""
FastAPI Application Entry Point.

Initialises the FastAPI app, registers routers, and configures
metadata for the auto-generated API docs at /docs.

Run with:
    uv run uvicorn src.api.main:app --reload
"""

from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="FinSight AI",
    description=(
        "A multi-agent stock investment analysis system powered by CrewAI, "
        "FastAPI, and Azure Cloud. Submit a natural language query about any "
        "stock and receive a full professional investment report."
    ),
    version="1.0.0",
    contact={
        "name": "Bharath Sykam",
        "url": "https://github.com/bharathsykam57-wq/FinSight_AI"
    }
)

app.include_router(router, prefix="/api/v1", tags=["Analysis"])


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Health check endpoint."""
    return {
        "service": "FinSight AI",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health() -> dict:
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "agents": "crewai",
        "storage": "azure_blob",
        "database": "azure_postgresql"
    }