import streamlit as st
import pandas as pd
from pathlib import Path
from common import df_filtered, get_filtered_df

st.title("Game Data Overview")

# --- INTERACTIVE FILTERS (SIDEBAR) ---
st.sidebar.header("Filters")



df_filtered = get_filtered_df()