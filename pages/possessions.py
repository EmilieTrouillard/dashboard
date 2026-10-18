import pandas as pd
import streamlit as st
from charts.possessions import (
    possessions_outcome_table,
    possessions_sources_chart,
    possessions_sources_agg_df,
)
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

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Denmark", width="stretch", text_alignment="center")
    with st.container(border=True, key="my_white_containerpossessions3"):
        agg_df_dk, max_dk = possessions_sources_agg_df(df_filtered, "Denmark")
        agg_df_op, max_op = possessions_sources_agg_df(df_filtered, "Opposition")
        max_range = max(max_dk, max_op)
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
    opponent_name = (
        df_filtered["opposition"].iloc[0]
        if "opposition" in df_filtered.columns
        and not df_filtered.empty
        and len(st.session_state.get("opponent") or []) == 1
        else "Opposition"
    )
    st.subheader(opponent_name, width="stretch", text_alignment="center")
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
