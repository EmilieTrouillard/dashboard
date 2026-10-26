from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.errors import StreamlitDefaultNotInOptionsError


def update_filters():
    st.session_state["tournament"] = st.session_state.tournament
    st.session_state["opponent"] = st.session_state.opponent
    st.session_state["stage"] = st.session_state.stage


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
    st.sidebar.header("Game Filters")

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

    # Filter: Stage
    selected_stage = []
    if "stage" in df_filtered.columns:
        stages = [x for x in df_filtered["stage"].dropna().unique().tolist()]
        try:
            selected_stage = st.sidebar.multiselect(
                "Stage",
                stages,
                select_all=True,
                default=st.session_state.get("stage"),
                on_change=update_filters,
            )
        except StreamlitDefaultNotInOptionsError:
            selected_stage = st.sidebar.multiselect(
                "Stage",
                stages,
                select_all=True,
                on_change=update_filters,
            )
        st.session_state["stage"] = selected_stage
        if selected_stage:
            df_filtered = df_filtered[df_filtered["stage"].isin(selected_stage)]
    # --- DISPLAY SELECTED GAMES (FORMATTED) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Selected Games")

    if not df_filtered.empty:
        has_opp = "opposition" in df_filtered.columns
        has_tourn = "tournament" in df_filtered.columns
        has_stage = "stage" in df_filtered.columns

        # Group by source_filename to get unique games, or fallback to unique combinations
        if "source_filename" in df_filtered.columns:
            game_df = (
                df_filtered.groupby("source_filename", dropna=False)
                .first()
                .reset_index()
            )
        else:
            subset_cols = [
                c
                for c in ["opposition", "tournament", "stage"]
                if c in df_filtered.columns
            ]
            game_df = (
                df_filtered.drop_duplicates(subset=subset_cols)
                if subset_cols
                else df_filtered
            )

        game_labels = []
        for _, row in game_df.iterrows():
            opp = (
                str(row.get("opposition", "Unknown Opponent"))
                if has_opp
                else "Unknown Opponent"
            )
            tourn = (
                str(row.get("tournament", "Unknown Tournament"))
                if has_tourn
                else "Unknown Tournament"
            )
            stage = str(row.get("stage", "")) if has_stage else ""

            # Format as "Opposition - Tournament (stage)" or omit stage if empty/NaN
            if stage and stage.lower() != "nan" and stage.strip() != "":
                label = f"{tourn} - {opp} ({stage})"
            else:
                label = f"{tourn} - {opp}"

            game_labels.append(label)

        unique_games = sorted(list(set(game_labels)))
        st.sidebar.caption(
            f"{len(unique_games)} game{'s' if len(unique_games) > 1 else ''} matching filters"
        )
        for game in unique_games:
            st.sidebar.text(f"• {game}")
    else:
        st.sidebar.caption("No games available")

    return df_filtered
