import pandas as pd
import streamlit as st
from charts.possessions import possessions_table
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


# Display the styled dataframe in Streamlit
with st.container(border=True, key="my_white_containerpossessions1"):
    styled_df = possessions_table(df_filtered, "Denmark")
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
