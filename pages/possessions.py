import pandas as pd
import streamlit as st
from charts.possessions import (
    possessions_outcome_table,
    possessions_sources_chart,
    possessions_sources_agg_df,
)
from charts.score import display_score
from common import get_filtered_df

st.set_page_config(
    page_title="Possessions",
    layout="wide",
)
css = """
.st-key-my_white_containerpossessions1 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerpossessions2 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerpossessions3 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerpossessions4 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerpossessions5 {
    background-color: #FFFFFF !important;
}
"""

st.html(f"<style>{css}</style>")

st.title("Possessions")

df_filtered = get_filtered_df()
agg_df_dk, max_dk, total_dk, tries_dk = possessions_sources_agg_df(
    df_filtered, "Denmark"
)
agg_df_op, max_op, total_op, tries_op = possessions_sources_agg_df(
    df_filtered, "Opposition"
)
max_range = max(max_dk, max_op)

score_html = display_score("Possessions", total_dk, total_op)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Denmark", width="stretch", text_alignment="center")
with col2:
    opponent_name = (
        df_filtered["opposition"].iloc[0]
        if "opposition" in df_filtered.columns
        and not df_filtered.empty
        and len(st.session_state.get("opponent") or []) == 1
        else "Opposition"
    )
    st.subheader(opponent_name, width="stretch", text_alignment="center")

col_1, col_2, col_3 = st.columns([0.5, 1, 0.5])
with col_1:
    st.markdown(
        """
    <style>
    div[data-testid="stMetric"] {
        background-color: #e7e6e4;
        padding: 15px;
        border-radius: 8px;
    }
    /* Move the label below the value and style it */
    div[data-testid="stMetric"] label {
        order: 2;
        font-size: 14px;
        color: #4b5563;
        text-align: center;
        display: block;
        width: 100%;
    }
    /* Style the main value number */
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        order: 1;
        font-size: 32px;
        font-weight: bold;
        color: #111827;
        text-align: center;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Your metric card display
    st.metric(
        label="Possession conversion rate",
        value=f"{int(tries_dk / total_dk * 100) if total_dk > 0 else '--'}%",
    )
with col_2:
    st.markdown(score_html, unsafe_allow_html=True)
with col_3:
    st.markdown("")
    # Your metric card display
    st.metric(
        label="Possession conversion rate",
        value=f"{int(tries_op / total_op * 100) if total_op > 0 else '--'}%",
    )
col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True, key="my_white_containerpossessions3"):

        fig = possessions_sources_chart(agg_df_dk, max_range)
        st.plotly_chart(fig, width="stretch")
    with st.container(border=True, key="my_white_containerpossessions1"):
        st.text(
            "Possession Outcomes per Number of Phases",
            width="stretch",
            text_alignment="center",
        )
        styled_df = possessions_outcome_table(df_filtered, "Denmark")
        st.dataframe(styled_df, width="stretch", hide_index=True)

with col2:
    with st.container(border=True, key="my_white_containerpossessions4"):
        fig = possessions_sources_chart(agg_df_op, max_range)
        st.plotly_chart(fig, width="stretch")
    with st.container(border=True, key="my_white_containerpossessions2"):
        st.text(
            "Possession Outcomes per Number of Phases",
            width="stretch",
            text_alignment="center",
        )
        styled_df = possessions_outcome_table(df_filtered, "Opposition")
        st.dataframe(styled_df, width="stretch", hide_index=True)
