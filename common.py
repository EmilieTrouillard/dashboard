from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.errors import StreamlitDefaultNotInOptionsError


def update_filters():
    st.session_state["tournament"] = st.session_state.tournament
    st.session_state["opponent"] = st.session_state.opponent


# --- LOAD DATA FROM THE 'data/' FOLDER ---
@st.cache_data(ttl=300)
def load_data_from_folder(folder_path="data"):
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        return pd.DataFrame()

    csv_files = list(path.glob("*.csv"))
    if not csv_files:
        return pd.DataFrame()

    dfs = []
    for f in csv_files:
        try:
            temp_df = pd.read_csv(f)
            temp_df["source_filename"] = f.name
            dfs.append(temp_df)
        except Exception as e:
            st.sidebar.error(f"Read error: {f.name}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()


def get_filtered_df():
    # Initial load
    df_raw = load_data_from_folder("data")

    if df_raw.empty:
        st.warning("No CSV files were found in the `/data` folder.")
        st.stop()

    # --- INTERACTIVE FILTERS (SIDEBAR) ---
    st.sidebar.header("Some name for the filters")

    df_filtered = df_raw.copy()

    # Filter: Tournament
    selected_tournament = []
    if "tournament" in df_filtered.columns:
        tournaments = [x for x in df_filtered["tournament"].dropna().unique().tolist()]
        selected_tournament = st.sidebar.multiselect(
            "Tournament",
            tournaments,
            select_all=True,
            default=st.session_state.get("tournament"),
            on_change=update_filters,
        )
        st.session_state["tournament"] = selected_tournament
        if selected_tournament:
            df_filtered = df_filtered[
                df_filtered["tournament"].isin(selected_tournament)
            ]
    # Filter: Opponent
    selected_opp = []
    if "opposition" in df_filtered.columns:
        opponents = [x for x in df_filtered["opposition"].dropna().unique().tolist()]
        try:
            selected_opp = st.sidebar.multiselect(
                "Opponent",
                opponents,
                select_all=True,
                default=st.session_state.get("opponent"),
                on_change=update_filters,
            )
        except StreamlitDefaultNotInOptionsError:
            selected_opp = st.sidebar.multiselect(
                "Opponent",
                opponents,
                select_all=True,
                on_change=update_filters,
            )
        st.session_state["opponent"] = selected_opp
        if selected_opp:
            df_filtered = df_filtered[df_filtered["opposition"].isin(selected_opp)]

    return df_filtered


# df_filtered = get_filtered_df()
