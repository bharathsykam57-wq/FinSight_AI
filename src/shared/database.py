"""
Azure PostgreSQL Database Service Module.

Handles saving analysis reports to Azure PostgreSQL using SQLAlchemy.
The reports_log table is created automatically on first run.
Gracefully skips DB operations if no connection string is provided.

Usage:
    from src.shared.database import DatabaseService
    db = DatabaseService()
    db.save_report(ticker="NVDA", content="## Report...")
"""

from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from src.shared.config import settings


Base = declarative_base()


class FinancialReport(Base):
    """SQLAlchemy model representing the reports_log table."""

    __tablename__ = "reports_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DatabaseService:
    """Manages connections and writes to Azure PostgreSQL."""

    def __init__(self) -> None:
        """Initialize the database engine and create tables if needed."""
        db_url = settings.azure_postgres_connection_string

        if not db_url:
            print("Warning: No database connection string provided. Skipping DB setup.")
            self.engine = None
            self.session_local = None
            return

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        self.engine = create_engine(db_url)
        self.session_local = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def save_report(self, ticker: str, content: str) -> None:
        """
        Saves a new analysis report to the database.

        Args:
            ticker: The stock ticker symbol (e.g., 'NVDA').
            content: The full markdown report text.
        """
        if not self.engine:
            print("Warning: Database not configured. Skipping save.")
            return

        session = self.session_local()
        try:
            new_report = FinancialReport(ticker=ticker, content=content)
            session.add(new_report)
            session.commit()
            print(f"Saved {ticker} report to database (ID: {new_report.id})")
        except (ValueError, RuntimeError) as e:
            print(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()