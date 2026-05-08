# FinSight AI

> **A production-grade multi-agent stock investment analysis system powered by CrewAI, FastAPI, Streamlit, and Azure Cloud.**
---

## What is FinSight AI?

FinSight AI is a fully autonomous multi-agent system that takes a natural language query like *"Tell me about NVDA stock"* and returns a professional investment report — complete with fundamental metrics, market sentiment, performance comparisons, and a final **BUY / HOLD / SELL** recommendation.

The system is built around two specialized AI agents that collaborate in a sequential pipeline:

- **Quantitative Analyst** — Fetches hard financial data using Yahoo Finance and scrapes the latest news using Firecrawl
- **Investment Strategist** — Synthesizes the analyst's findings into a structured markdown investment report

Reports are automatically uploaded to **Azure Blob Storage** and logged to **Azure PostgreSQL** for persistence.

---

## Architecture

![FinSight AI Architecture](architecture.png)

```

User Query (Natural Language)
        │
        ▼
┌─────────────────────┐
│   FastAPI Backend   │  ◄── POST /api/v1/analyze
│   (routes.py)       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│            CrewAI Pipeline              │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │   Agent 1: Quantitative Analyst  │   │
│  │   Tools:                         │   │
│  │   - FundamentalAnalysisTool      │   │
│  │   - CompareStocksTool            │   │
│  │   - SentimentSearchTool          │   │
│  └──────────────┬───────────────────┘   │
│                 │ findings              │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │  Agent 2: Investment Strategist  │   │
│  │  Output: Markdown Report         │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
 Azure Blob         Azure PostgreSQL
 Storage            (reports_log table)
 (report .md)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agents | CrewAI + OpenAI GPT-4o |
| Financial Data | yfinance (Yahoo Finance API) |
| Web Scraping | Firecrawl |
| REST API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Cloud Storage | Azure Blob Storage |
| Cloud Database | Azure PostgreSQL Flexible Server |
| Config Management | Pydantic Settings |
| ORM | SQLAlchemy |
| Package Manager | uv |

---

## Project Structure

```
finsight-ai/
├── src/
│   ├── agents/
│   │   ├── tools/
│   │   │   ├── financial.py      # yfinance tools (metrics + comparison)
│   │   │   └── scraper.py        # Firecrawl sentiment search tool
│   │   ├── agents.py             # Quantitative Analyst + Strategist agents
│   │   ├── tasks.py              # Task definitions and pipeline
│   │   └── crew.py               # Crew orchestration
│   ├── api/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routes.py             # /analyze endpoint
│   │   └── models.py             # Pydantic request/response schemas
│   └── shared/
│       ├── config.py             # Environment variable management
│       ├── storage.py            # Azure Blob Storage service
│       └── database.py           # Azure PostgreSQL service
├── frontend/
│   └── app.py                    # Streamlit UI
├── infra/
│   └── README.md                 # Azure infrastructure setup guide
├── main.py                       # CLI entry point
├── pyproject.toml
└── .env                          # API keys (never committed)
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Firecrawl API key
- Azure account (Storage + PostgreSQL)

### 1. Clone the Repository

```bash
git clone https://github.com/bharathsykam57-wq/FinSight_AI.git
cd FinSight_AI
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# AI
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o

# Firecrawl
FIRECRAWL_API_KEY=fc-...

# Azure
AZURE_BLOB_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_POSTGRES_CONNECTION_STRING=postgresql://user:password@host:5432/postgres?sslmode=require

# LangSmith (optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
```

> See `infra/README.md` for detailed Azure setup instructions.

### 4. Run the FastAPI Backend

```bash
uv run uvicorn src.api.main:app --reload
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### 5. Run the Streamlit Frontend

```bash
uv run streamlit run frontend/app.py
```

Frontend will be available at `http://localhost:8501`

### 6. Or Run via CLI

```bash
uv run python main.py
```

### 7. Or Run via Docker

```bash
docker build -t finsight-ai .
docker run -p 8000:8000 --env-file .env finsight-ai
```

---

## Sample Output

Given the query: *"Tell me about NVDA stock"*

```markdown
## Executive Summary
NVIDIA Corporation (NVDA) remains one of the most dominant players
in the semiconductor space, driven by explosive AI infrastructure demand...

## Fundamental Analysis
- Current Price: $211.50
- Market Cap: $5.14T
- P/E Ratio (Trailing): 43.08x
- Beta: 2.244 (high volatility)
- EPS: $4.91
- NVDA 1-year return: 80.24% vs SPY 30.95%

## Market Sentiment
Recent analyst upgrades from Morgan Stanley and Goldman Sachs...

## Risk & Opportunity Assessment
**Opportunities:** AI compute supercycle, data center expansion...
**Risks:** Geopolitical chip export restrictions, valuation premium...

## Final Recommendation: BUY
```

---

## Azure Infrastructure

| Resource | Purpose | Tier |
|---|---|---|
| Azure Blob Storage | Stores generated markdown reports | LRS (any tier) |
| Azure PostgreSQL Flexible Server | Logs all analysis requests | Standard_B1ms (free tier) |

> Full provisioning guide in [`infra/README.md`](infra/README.md)

---

## API Reference

### `POST /api/v1/analyze`

**Request:**

```json
{
  "query": "Tell me about NVDA stock"
}
```

**Response:**

```json
{
  "ticker": "NVDA",
  "report": "## Executive Summary\n...",
  "blob_url": "https://youraccount.blob.core.windows.net/reports/investment_report_NVDA.md",
  "status": "success"
}
```

### `GET /health`

```json
{
  "status": "healthy",
  "agents": "crewai",
  "storage": "azure_blob",
  "database": "azure_postgresql"
}
```

---

## Financial Terms Glossary

> *Not from finance? No problem. Here's what the report terms actually mean.*

| Term | What it means in plain English |
|---|---|
| **Ticker** | A short code that identifies a stock on the market. NVDA = NVIDIA, AAPL = Apple. |
| **Market Cap** | The total value of a company's shares. Large cap (>$10B) = big stable company. Small cap (<$2B) = smaller, riskier. |
| **P/E Ratio (Price-to-Earnings)** | How much investors pay per $1 of company profit. A P/E of 30 means you pay $30 for every $1 earned. Higher = more growth expected, but also more risk. |
| **Forward P/E** | Same as P/E but using *predicted* future earnings instead of past ones. Shows what the market expects going forward. |
| **PEG Ratio** | P/E ratio adjusted for growth rate. A PEG below 1.0 is generally considered undervalued. |
| **Beta** | Measures how volatile a stock is compared to the overall market. Beta > 1 = moves more than the market. Beta < 1 = more stable. |
| **EPS (Earnings Per Share)** | How much profit the company made per share of stock. Higher EPS = more profitable per share. |
| **52-Week High / Low** | The highest and lowest price the stock traded at over the past year. Useful for understanding where the stock sits in its recent range. |
| **BUY** | Analysts believe the stock price will rise. Good time to invest. |
| **HOLD** | The stock is fairly valued. Keep it if you own it, but not urgent to buy more. |
| **SELL** | Analysts believe the stock price will fall. Consider exiting the position. |
| **Sentiment** | The overall mood of the market toward a stock — positive, negative, or neutral — based on news, analyst ratings, and social media. |
| **Benchmark (SPY)** | SPY is an ETF that tracks the S&P 500 (top 500 US companies). Comparing a stock to SPY shows if it outperformed or underperformed the broader market. |
| **Fundamental Analysis** | Evaluating a stock based on real business data — revenue, profit, debt, growth — rather than just its price movements. |
