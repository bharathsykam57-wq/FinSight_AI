"""
Streamlit Frontend for FinSight AI.

Provides a clean web UI for submitting stock analysis queries
and displaying the generated investment reports.

Run with:
    uv run streamlit run frontend/app.py
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/analyze"

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="centered"
)

st.title("📈 FinSight AI")
st.subheader("Multi-Agent Stock Investment Analyzer")
st.markdown(
    "Powered by **CrewAI**, **FastAPI**, and **Azure Cloud**. "
    "Enter a natural language query about any stock to receive "
    "a professional investment report."
)

st.divider()

query = st.text_input(
    label="Stock Query",
    placeholder="e.g. Tell me about NVDA stock",
    help="Enter a natural language query containing a stock ticker symbol."
)

if st.button("🔍 Analyze", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a query before analyzing.")
    else:
        with st.spinner("Running multi-agent analysis... this may take a minute."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success(f"Analysis complete for **{data['ticker']}**")

                    st.markdown("### 📄 Investment Report")
                    st.markdown(data["report"])

                    st.divider()

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Ticker", value=data["ticker"])
                    with col2:
                        st.metric(label="Status", value=data["status"].capitalize())

                    if data["blob_url"] != "unavailable":
                        st.markdown(
                            f"📦 [View report in Azure Blob Storage]({data['blob_url']})"
                        )

                elif response.status_code == 400:
                    st.error(f"Bad request: {response.json().get('detail')}")
                else:
                    st.error(f"API error {response.status_code}: {response.json()}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. "
                    "Make sure the FastAPI server is running on port 8000."
                )
            except requests.exceptions.Timeout:
                st.error(
                    "Request timed out. The analysis is taking longer than expected. "
                    "Please try again."
                )

st.divider()
st.caption("FinSight AI © 2025 — Built with CrewAI, FastAPI, Streamlit & Azure")