from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from common import df_filtered, get_filtered_df, update_filters

st.set_page_config(
    page_title="Rugby Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS: Forces Streamlit border containers to have solid white background & custom shadow
st.markdown(
    """
    <style>
    /* Force Streamlit container boxes to be solid white */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 18px 20px 15px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #FFFFFF !important;
    }

    /* Card Title Styling */
    .kpi-card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }

    /* Metric Display styling (Left side) */
    .kpi-metric-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;
    }
    .kpi-metric-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #4B5563;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-metric-val {
        font-size: 2.8rem;
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
    }
    </style>
""",
    unsafe_allow_html=True,
)
css = """
.st-key-my_white_container1 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_container2 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_container3 {
    background-color: #FFFFFF !important;
}
.st-key-my_white_container4 {
    background-color: #FFFFFF !important;
}
"""
st.html(f"<style>{css}</style>")


# # --- LOAD DATA FROM THE 'data/' FOLDER ---
# @st.cache_data(ttl=300)
# def load_data_from_folder(folder_path="data"):
#   path = Path(folder_path)
#   if not path.exists() or not path.is_dir():
#     return pd.DataFrame()

#   csv_files = list(path.glob("*.csv"))
#   if not csv_files:
#     return pd.DataFrame()

#   dfs = []
#   for f in csv_files:
#     try:
#       temp_df = pd.read_csv(f)
#       temp_df["source_filename"] = f.name
#       dfs.append(temp_df)
#     except Exception as e:
#       st.sidebar.error(f"Read error: {f.name}")

#   if dfs:
#     return pd.concat(dfs, ignore_index=True)
#   return pd.DataFrame()


# # Initial load
# df_raw = load_data_from_folder("data")

# if df_raw.empty:
#   st.warning("No CSV files were found in the `/data` folder.")
#   st.stop()

# # --- INTERACTIVE FILTERS (SIDEBAR) ---
# st.sidebar.header("Filters")

# df_filtered = df_raw.copy()

# # Filter: Opponent
# selected_opp = []
# if "opposition" in df_filtered.columns:
#   opponents = [x for x in df_filtered["opposition"].dropna().unique().tolist()]
#   selected_opp = st.sidebar.multiselect("Opponent", opponents,key="opponent", select_all=True, default=st.session_state.get("opponent"), on_change=update_filters)
#   if selected_opp:
#     df_filtered = df_filtered[df_filtered["opposition"].isin(selected_opp)]

# # Filter: Tournament
# selected_tournament = []
# if "tournament" in df_filtered.columns:
#   tournaments = [
#       x for x in df_filtered["tournament"].dropna().unique().tolist()
#   ]
#   selected_tournament = st.sidebar.multiselect("Tournament", tournaments, key="tournament", select_all=True, default=st.session_state.get("tournament"), on_change=update_filters)
#   if selected_tournament:
#     df_filtered = df_filtered[
#         df_filtered["tournament"].isin(selected_tournament)
#     ]



# -----------------------------------------------------------------------------
# DASHBOARD HEADER
# -----------------------------------------------------------------------------
st.title("KPIs")

df_filtered = get_filtered_df()
# -----------------------------------------------------------------------------
# DYNAMIC SCORE CALCULATION & SCOREBOARD BANNER
# -----------------------------------------------------------------------------
dk_score = (
    int(df_filtered["points_scored"].sum())
    if "points_scored" in df_filtered.columns
    else 0
)
opp_score = (
    int(df_filtered["points_conceeded"].sum())
    if "points_conceeded" in df_filtered.columns
    else 0
)

st.markdown(
    f"""
    <div style="
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin: 15px auto 25px auto;
        max-width: 650px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    ">
        <div style="
            font-size: 0.9rem;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        ">
            SCORE
        </div>
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
        ">
            <div style="text-align: center;">
                <span style="font-size: 1.4rem; font-weight: 800; color: #DC2626; display: block;">DK</span>
                <span style="font-size: 3.5rem; font-weight: 900; color: #111827; line-height: 1;">{dk_score}</span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 300; color: #9CA3AF; margin-top: 15px;">-</div>
            <div style="text-align: center;">
                <span style="font-size: 1.4rem; font-weight: 800; color: #374151; display: block;">OPP</span>
                <span style="font-size: 3.5rem; font-weight: 900; color: #111827; line-height: 1;">{opp_score}</span>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)


# Helper function for pie charts
def create_pie_chart(labels, values, colors, legend_title="End Possession"):
  fig = go.Figure(
      data=[
          go.Pie(
              labels=labels,
              values=values,
              hole=0.55,
              marker=dict(colors=colors),
              textinfo="value+percent",
              textposition="inside",
              insidetextorientation="horizontal",
              direction="clockwise",
              sort=False,
          )
      ]
  )

  fig.update_layout(
      showlegend=True,
      legend=dict(
          x=1.0,
          y=0.5,
          xanchor="left",
          yanchor="middle",
          title=dict(text=f"<b>{legend_title}</b>"),
      ),
      margin=dict(l=0, r=0, t=10, b=10),
      height=210,
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
  )
  return fig


# -----------------------------------------------------------------------------
# 2x2 CARDS GRID USING NATIVE CONTAINERS
# -----------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

# --- CARD 1: RESTARTS ---
with row1_col1:
  with st.container(border=True, key="my_white_container1"):
    st.markdown(
        '<div class="kpi-card-title">Restarts</div>', unsafe_allow_html=True
    )

    restarts_df = df_filtered[
        df_filtered["event_type"].isin(["Kick Off", "Kick Receipt"])
    ]
    possession_counts = (
        restarts_df["end_possession"].value_counts().to_dict()
        if "end_possession" in restarts_df.columns
        else {}
    )

    denmark_cnt = possession_counts.get("Denmark", 0)
    opposition_cnt = possession_counts.get("Opposition", 0)
    kickoff_score = denmark_cnt - opposition_cnt
    score_display = (
        f"{kickoff_score:+d}" if kickoff_score > 0 else str(kickoff_score)
    )

    card_col_left, card_col_right = st.columns([1, 2], vertical_alignment="center")

    with card_col_left:
      st.markdown(
          f"""
            <div class="kpi-metric-container">
                <div class="kpi-metric-label">Kick Off Score</div>
                <div class="kpi-metric-val">{score_display}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

    with card_col_right:
      labels = ["Denmark", "Opposition"]
      values = [denmark_cnt, opposition_cnt]
      colors = ["#FF1E1E", "#4A0404"]

      if sum(values) > 0:
        fig_restarts = create_pie_chart(
            labels=labels,
            values=values,
            colors=colors,
            legend_title="End Possession",
        )
        st.plotly_chart(
            fig_restarts,
            width='content',
            config={"displayModeBar": False},
        )
      else:
        st.info("No restart data found.")

# --- CARD 2: TURNOVERS (PLACEHOLDER) ---
with row1_col2:
  with st.container(border=True, key="my_white_container2"):
    st.markdown(
        '<div class="kpi-card-title">Turnovers</div>', unsafe_allow_html=True
    )

    card_col_left, card_col_right = st.columns([1, 2], vertical_alignment="center")
    turnovers_df = df_filtered[
        df_filtered["event_type"].isin(["Turnover"])
    ]
    possession_counts = (
        turnovers_df["end_possession"].value_counts().to_dict()
        if "end_possession" in turnovers_df.columns
        else {}
    )

    denmark_cnt = possession_counts.get("Denmark", 0)
    opposition_cnt = possession_counts.get("Opposition", 0)
    turnover_score = denmark_cnt - opposition_cnt
    score_display = (
        f"{turnover_score:+d}" if turnover_score > 0 else str(turnover_score)
    )
    with card_col_left:
      st.markdown(
          f"""
            <div class="kpi-metric-container">
                <div class="kpi-metric-label">Turnover Score</div>
                <div class="kpi-metric-val">{score_display}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

    with card_col_right:
        labels = ["Denmark", "Opposition"]
        values = [denmark_cnt, opposition_cnt]
        colors = ["#FF1E1E", "#4A0404"]

        if sum(values) > 0:
            fig_restarts = create_pie_chart(
                labels=labels,
                values=values,
                colors=colors,
                legend_title="End Possession",
            )
            st.plotly_chart(
                fig_restarts,
                width='content',
                config={"displayModeBar": False},
            )
        else:
            st.info("No restart data found.")


row2_col1, row2_col2 = st.columns(2)

# --- CARD 3: TACKLES (PLACEHOLDER) ---
with row2_col1:
  with st.container(border=True, key="my_white_container3"):
    st.markdown(
        '<div class="kpi-card-title">Tackles</div>', unsafe_allow_html=True
    )
    tackles = df_filtered[
            df_filtered["event_type"].isin(["Tackle"])
        ]
    outcome_counts = (
            tackles["outcome"].value_counts().to_dict()
            if "outcome" in tackles.columns
            else {}
        )
    completed = outcome_counts.get("Completed", 0)
    missed = outcome_counts.get("Missed", 0)
    ineffective = outcome_counts.get("Ineffective", 0)
    completion_rate : float | None = completed / (completed + missed + ineffective) * 100 if (completed + missed + ineffective) > 0 else None
    completion_rate_display = f"{completion_rate:.0f}%" if completion_rate is not None else "-"
    
    card_col_left, card_col_right = st.columns([1, 2], vertical_alignment="center")

    with card_col_left:
      st.markdown(
          f"""
            <div class="kpi-metric-container">
                <div class="kpi-metric-label">Completion Rate</div>
                <div class="kpi-metric-val">{completion_rate_display}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

    with card_col_right:
        labels = ["Completed", "Ineffective", "Missed"]
        values = [completed, ineffective, missed]
        colors = ["#FF1E1E","#9CA3AF", "#4A0404"]
    
        if sum(values) > 0:
            fig_restarts = create_pie_chart(
                labels=labels,
                values=values,
                colors=colors,
                legend_title="Outcome",
            )
            st.plotly_chart(
                fig_restarts,
                width='content',
                config={"displayModeBar": False},
            )
        else:
            st.info("No restart data found.")
      

# --- CARD 4: ATTACKS (PLACEHOLDER) ---
with row2_col2:
  with st.container(border=True, key="my_white_container4"):
    st.markdown(
        '<div class="kpi-card-title">Attacks</div>', unsafe_allow_html=True
    )
    attacks = df_filtered[
        df_filtered["original_possession"].isin(["Denmark"])
    ]
    tries = len(attacks[
        attacks["event_type"].isin(["Try"])
    ])
    open_play_kicks = len(attacks[
        attacks["event_type"].isin(["Open Play Kick"])
    ])
    penalties_against = len(attacks[
        (attacks["event_type"].isin(["Penalty"])) & (attacks["outcome"].isin(["Conceeded"])) & ~(attacks["reason"].isin(["Scrum", "Lineout"]))
    ])
    penalties_for = len(attacks[
        (attacks["event_type"].isin(["Penalty"])) & (attacks["outcome"].isin(["Rewarded"])) & ~(attacks["reason"].isin(["Scrum", "Lineout"]))
    ])
    set_pieces_kept = len(attacks[
        (attacks["event_type"].isin(["Scrum", "Lineout"])) & (attacks["origin"].isin(["No Change"]))
    ])
    turnovers_lost = len(attacks[
        (attacks["event_type"].isin(["Turnover"])) & ~(attacks["penalty"].isin(["Penalty"])) & ~(attacks["reason"].isin(["PenKickOut Error"]))
    ])
    attack_completion_rate = tries / (tries + turnovers_lost + penalties_against + open_play_kicks) * 100 if (tries + turnovers_lost + penalties_against + open_play_kicks) > 0 else None
    attack_completion_rate_display = f"{attack_completion_rate:.0f}%" if attack_completion_rate is not None else "-"
          
    card_col_left, card_col_right = st.columns([1, 2], vertical_alignment="center")

    with card_col_left:
      st.markdown(
          f"""
            <div class="kpi-metric-container">
                <div class="kpi-metric-label">Attack Completion Rate</div>
                <div class="kpi-metric-val">{attack_completion_rate_display}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

    with card_col_right:
        labels = ["Try", "Penalty For", "Set Piece Kept", "Open Play Kick", "Turnover Lost", "Penalty Against"]
        values = [tries, penalties_for, set_pieces_kept, open_play_kicks, turnovers_lost, penalties_against]
        colors = [
          "#FF1E1E",
                              "#FCA5A5",
                              "#D1D5DB",
                              "#9CA3AF",
                              "#4A0404",
                              "#000000",]
    
        if sum(values) > 0:
            fig_restarts = create_pie_chart(
                labels=labels,
                values=values,
                colors=colors,
                legend_title="Outcome",
            )
            st.plotly_chart(
                fig_restarts,
                width='content',
                config={"displayModeBar": False},
            )
        else:
            st.info("No restart data found.")