import pandas as pd
import streamlit as st

from charts.tackles import tackle_completion_bar
from charts.tries import tries_sources_phases
from charts.turnovers import turnover_reasons_phases
from common import get_filtered_df

st.set_page_config(
    page_title="Game Overview",
    layout="wide",
)
css = """
.st-key-my_white_containergame1 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containergame2 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containergame3 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containergame4 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_containergame5 {
    background-color: #FFFFFF !important;
}
"""
st.html(f"<style>{css}</style>")

st.title("Game Data Overview")

df_filtered = get_filtered_df()

# --- Custom CSS for Score/Metric Pills ---
st.markdown(
    """
    <style>
    .kpi-row-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .kpi-pill-header {
        font-size: 0.75rem;
        font-weight: 800;
        color: #374151;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 6px;
        min-height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1.1;
    }
    .kpi-pill {
        border-radius: 8px;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.1rem;
        text-align: center;
        padding: 8px 0;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .kpi-pill-dk {
        background-color: #D90429; /* Red for Denmark/DK */
    }
    .kpi-pill-opp {
        background-color: #030F26; /* Dark Navy for Opposition */
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CALCULATE OR EXTRACT METRICS ---
# Safely pulls data from df_filtered or falls back to sample values matching screenshot 2
opponent_name = (
    df_filtered["opposition"].iloc[0]
    if "opposition" in df_filtered.columns
    and not df_filtered.empty
    and len(st.session_state.get("opponent") or []) == 1
    else "Opposition"
)
tries = (
    df_filtered[df_filtered["event_type"] == "Try"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
tries_per_team = (
    tries["end_possession"].value_counts().to_dict() if not tries.empty else {}
)
turnovers = (
    df_filtered[df_filtered["event_type"] == "Turnover"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
turnovers_per_team = (
    turnovers["end_possession"].value_counts().to_dict() if not turnovers.empty else {}
)

possessions = df_filtered[
    (
        df_filtered["event_type"].isin(
            [
                "Penalty",
                "Free Kick",
                "Kick Off",
                "Kick Receipt",
                "Lineout",
                "Scrum",
                "Open Play Kick",
                "Turnover",
            ]
        )
    )
    & ~(df_filtered["type"] == "Set Piece")
    & ~(df_filtered["penalty"] == "Penalty")
    & ~(df_filtered["completed"] == False)
    & ~(
        df_filtered["outcome"].isin(
            ["Out", "Lost Not Straight", "Won Not Straight", "Won - Out", "Lost - Out"]
        )
    )
]
possessions_per_team = (
    possessions["end_possession"].value_counts().to_dict()
    if not possessions.empty
    else {}
)

penalties = (
    df_filtered[df_filtered["event_type"] == "Penalty"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
penalties_per_team = (
    penalties["outcome"].value_counts().to_dict() if not penalties.empty else {}
)
free_kicks = (
    df_filtered[df_filtered["event_type"] == "Free Kick"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
free_kicks_per_team = (
    free_kicks["outcome"].value_counts().to_dict() if not free_kicks.empty else {}
)
line_breaks = (
    df_filtered[df_filtered["event_type"] == "Line Break"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
line_breaks_per_team = (
    line_breaks["end_possession"].value_counts().to_dict()
    if not line_breaks.empty
    else {}
)
entries_22 = (
    df_filtered[df_filtered["event_type"] == "22m Entry"]
    if "event_type" in df_filtered.columns
    else pd.DataFrame()
)
entries_22_per_team = (
    entries_22["end_possession"].value_counts().to_dict()
    if not entries_22.empty
    else {}
)

metrics_data = [
    {
        "label": "Score",
        "dk": (
            int(df_filtered["points_scored"].sum())
            if "points_scored" in df_filtered.columns
            else 20
        ),
        "opp": (
            int(df_filtered["points_conceeded"].sum())
            if "points_conceeded" in df_filtered.columns
            else 0
        ),
    },
    {
        "label": "Tries",
        "dk": (tries_per_team.get("Denmark", 0)),
        "opp": (tries_per_team.get("Opposition", 0)),
    },
    {
        "label": "Turnovers",
        "dk": (turnovers_per_team.get("Denmark", 0)),
        "opp": (turnovers_per_team.get("Opposition", 0)),
    },
    {
        "label": "Possessions",
        "dk": (possessions_per_team.get("Denmark", 0)),
        "opp": (possessions_per_team.get("Opposition", 0)),
    },
    {
        "label": "Penalties Conceded",
        "dk": (penalties_per_team.get("Conceeded", 0)),
        "opp": (penalties_per_team.get("Rewarded", 0)),
    },
    {
        "label": "Free-Kicks Conceded",
        "dk": (free_kicks_per_team.get("Conceeded", 0)),
        "opp": (free_kicks_per_team.get("Rewarded", 0)),
    },
    {
        "label": "Linebreaks",
        "dk": (line_breaks_per_team.get("Denmark", 0)),
        "opp": (line_breaks_per_team.get("Opposition", 0)),
    },
    {
        "label": "22m Entries",
        "dk": (entries_22_per_team.get("Denmark", 0)),
        "opp": (entries_22_per_team.get("Opposition", 0)),
    },
]

# --- RENDER TABLE ---
# Create team label column + 1 column per metric
cols = st.columns([1.2] + [1] * len(metrics_data))

# Team Names Column (Row Labels)
with cols[0]:
    st.markdown(
        f"""
        <div class="kpi-pill-header">&nbsp;</div>
        <div class="kpi-pill kpi-pill-dk">DK</div>
        <div style="height: 8px;"></div>
        <div class="kpi-pill kpi-pill-opp">{opponent_name[:3].upper()}</div>
    """,
        unsafe_allow_html=True,
    )

# Metric Value Columns
for i, item in enumerate(metrics_data):
    with cols[i + 1]:
        st.markdown(
            f"""
            <div class="kpi-pill-header">{item['label']}</div>
            <div class="kpi-pill kpi-pill-dk">{item['dk']}</div>
            <div style="height: 8px;"></div>
            <div class="kpi-pill kpi-pill-opp">{item['opp']}</div>
        """,
            unsafe_allow_html=True,
        )
st.markdown("---")

col1, col2 = st.columns([1, 1])
with col1:
    fig = tries_sources_phases("Denmark", df_filtered, opponent_name)
    if fig is not None:
        with st.container(border=True, key="my_white_containergame1"):

            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
with col2:
    fig = tries_sources_phases("Opposition", df_filtered, opponent_name)
    if fig is not None:
        with st.container(border=True, key="my_white_containergame2"):

            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

col1, col2 = st.columns([1, 1])
with col1:
    with st.container(border=True, key="my_white_containergame3"):
        fig = tackle_completion_bar("Denmark", df_filtered, opponent_name)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with st.container(border=True, key="my_white_containergame4"):
        fig = tackle_completion_bar("Opposition", df_filtered, opponent_name)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
with col2:
    with st.container(border=True, key="my_white_containergame5"):
        fig = turnover_reasons_phases(df_filtered)
        if fig is not None:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
