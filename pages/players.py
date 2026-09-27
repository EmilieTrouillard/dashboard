import pandas as pd
import streamlit as st

from charts.tackles import tackle_completion_bar, tackle_completion_per_player
from charts.tries import tries_sources_phases
from charts.turnovers import turnover_reasons_phases
from common import get_filtered_df

css = """
.st-key-my_white_containerplayers1 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerplayers2 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerplayers3 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerplayers4 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containerplayers5 {
    background-color: #FFFFFF !important;
}
"""

st.html(f"<style>{css}</style>")

df_filtered = get_filtered_df()

st.title("Players Data")

fig = tackle_completion_per_player(df_filtered)
if fig is not None:
    with st.container(border=True, key="my_white_containerplayers1"):
        st.plotly_chart(fig, use_container_width=True)
