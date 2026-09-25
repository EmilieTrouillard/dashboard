from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Rugby Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)



# Custom CSS for KPI Container Cards (Styles st.container(border=True) directly)
st.markdown(
    """
    <style>
    /* Override Streamlit container styling to match your single white card design */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px 20px 10px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }

    /* Section Title inside Cards */
    .kpi-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)



# Stage / Tournament Info Display
match_title = (
    f"Match Analysis: Denmark vs {st.session_state.get("opponent")[0]}"
    if len(st.session_state.get("opponent") or []) == 1
    else "Match Performance Overview"
)
tournament_info = (
    f"{st.session_state.get("tournament")[0]} ({st.session_state.get("stage")[0]})"
    if len(st.session_state.get("tournament") or []) == 1
    and len(st.session_state.get("stage") or []) == 1
    else ""
)

# -----------------------------------------------------------------------------
# DASHBOARD HEADER
# -----------------------------------------------------------------------------
st.title(f"{match_title}")
if tournament_info:
  st.caption(f"**Tournament:** {tournament_info}")

st.markdown("---")

# -----------------------------------------------------------------------------


pages = {
  "Game": [
    st.Page("pages/kpis.py", title = "KPIs"),
    st.Page("pages/game.py", title = "Game Data Overview"),
  ],
  "Players": []
}
pages_list = [
    st.Page("pages/kpis.py", title = "KPIs"),
    st.Page("pages/game.py", title = "Game Data Overview"),
  ]
st.navigation(pages_list, position='top').run()