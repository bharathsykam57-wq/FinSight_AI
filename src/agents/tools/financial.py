"""
Financial Data Extraction Module.

Classes:
    FundamentalAnalysisTool: Fetches snapshot metrics (P/E, Beta, Cap).
    CompareStocksTool: Calculates relative performance over time.
"""

from typing import Any, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf


class StockAnalysisInput(BaseModel):
    """Input schema for the FundamentalAnalysisTool."""

    ticker: str = Field(
        ...,
        description="The stock ticker symbol (e.g., 'AAPL', 'NVDA', 'MSFT')."
    )


class CompareStocksInput(BaseModel):
    """Input schema for the CompareStocksTool."""

    ticker_a: str = Field(..., description="The first stock ticker to analyze.")
    ticker_b: str = Field(..., description="The second stock ticker to compare against.")


class FundamentalAnalysisTool(BaseTool):
    """Fetches key fundamental financial metrics for a stock via Yahoo Finance."""

    name: str = "Fetch Fundamental Metrics"
    description: str = (
        "Fetches key financial metrics for a specific stock ticker. "
        "Useful for quantitative analysis. Returns JSON-formatted data including "
        "P/E Ratio, Beta, Market Cap, EPS, and 52-week High/Low."
    )
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """Fetch fundamental metrics from Yahoo Finance."""
        ticker = kwargs.get("ticker") or (args[0] if args else None)
        try:
            stock = yf.Ticker(ticker)
            info: Dict[str, Any] = stock.info

            metrics = {
                "Ticker": ticker.upper(),
                "Current Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "P/E Ratio (Trailing)": info.get("trailingPE", "N/A"),
                "Forward P/E": info.get("forwardPE", "N/A"),
                "PEG Ratio": info.get("pegRatio", "N/A"),
                "Beta (Volatility)": info.get("beta", "N/A"),
                "EPS (Trailing)": info.get("trailingEps", "N/A"),
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Analyst Recommendation": info.get("recommendationKey", "none")
            }
            return str(metrics)

        except (ValueError, KeyError, ConnectionError) as e:
            return f"Error fetching fundamental data for '{ticker}': {str(e)}"


class CompareStocksTool(BaseTool):
    """Calculates relative price performance between two stocks over 1 year."""

    name: str = "Compare Stock Performance"
    description: str = (
        "Compares the historical performance of two stocks over the last 365 days. "
        "Returns the percentage gain or loss for both assets."
    )
    args_schema: Type[BaseModel] = CompareStocksInput

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """Compare 1-year performance of two tickers against each other."""
        ticker_a = kwargs.get("ticker_a") or (args[0] if args else None)
        ticker_b = kwargs.get("ticker_b") or (args[1] if len(args) > 1 else None)
        try:
            tickers = f"{ticker_a} {ticker_b}"
            data = yf.download(tickers, period="1y", progress=False)['Close']

            def calculate_return(symbol: str) -> float:
                """Calculate percentage return over the period."""
                start_price = data[symbol].iloc[0]
                end_price = data[symbol].iloc[-1]
                return ((end_price - start_price) / start_price) * 100

            perf_a = calculate_return(ticker_a)
            perf_b = calculate_return(ticker_b)

            return (
                f"Performance Comparison (Last 1 Year):\n"
                f"- {ticker_a.upper()}: {perf_a:.2f}%\n"
                f"- {ticker_b.upper()}: {perf_b:.2f}%"
            )

        except (ValueError, KeyError, ConnectionError) as e:
            return f"Error comparing stocks '{ticker_a}' and '{ticker_b}': {str(e)}"
        