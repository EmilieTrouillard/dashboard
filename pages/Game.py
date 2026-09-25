import streamlit as st
import pandas as pd
from pathlib import Path
from common import get_filtered_df

st.title("Game Data Overview")



df_filtered = get_filtered_df()