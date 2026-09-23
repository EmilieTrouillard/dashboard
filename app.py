from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Rugby Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for KPI Container Cards (Styles st.container(border=True) directly)
st.markdown(
    """
    <style>
    /* Override Streamlit container styling to match your single white card design */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px 20px 10px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }

    /* Section Title inside Cards */
    .kpi-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


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


# Initial load
df_raw = load_data_from_folder("data")

if df_raw.empty:
  st.warning("No CSV files were found in the `/data` folder.")
  st.stop()

# --- INTERACTIVE FILTERS (SIDEBAR) ---
st.sidebar.header("Some name for the filters")

df_filtered = df_raw.copy()

# Filter: Opponent
selected_opp = []
if "opposition" in df_filtered.columns:
  opponents = [x for x in df_filtered["opposition"].dropna().unique().tolist()]
  selected_opp = st.sidebar.multiselect("Opponent", opponents, select_all=True)
  if selected_opp:
    df_filtered = df_filtered[df_filtered["opposition"].isin(selected_opp)]

# Filter: Tournament
selected_tournament = []
if "tournament" in df_filtered.columns:
  tournaments = [
      x for x in df_filtered["tournament"].dropna().unique().tolist()
  ]
  selected_tournament = st.sidebar.multiselect("Tournament", tournaments)
  if selected_tournament:
    df_filtered = df_filtered[
        df_filtered["tournament"].isin(selected_tournament)
    ]

# Stage / Tournament Info Display
match_title = (
    f"Match Analysis: Denmark vs {df_filtered['opposition'].iloc[0]}"
    if len(selected_opp) == 1
    and not df_filtered.empty
    and "opposition" in df_filtered.columns
    else "Match Performance Overview"
)
tournament_info = (
    f"{df_filtered['tournament'].iloc[0]} ({df_filtered['stage'].iloc[0]})"
    if len(selected_tournament) == 1
    and not df_filtered.empty
    and "tournament" in df_filtered.columns
    and "stage" in df_filtered.columns
    else ""
)

# -----------------------------------------------------------------------------
# DASHBOARD HEADER
# -----------------------------------------------------------------------------
st.title(f"{match_title}")
if tournament_info:
  st.caption(f"**Tournament:** {tournament_info}")

st.markdown("---")

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


# Helper function to create Donut Charts with transparent background inside Card
def create_kpi_donut(
    labels,
    values,
    colors,
    center_metric_title,
    center_metric_val,
    legend_title="End Possession",
):
  fig = go.Figure(
      data=[
          go.Pie(
              labels=labels,
              values=values,
              hole=0.68,
              marker=dict(colors=colors),
              textinfo="value+percent",
              textposition="outside",
              direction="clockwise",
              sort=False,
              domain=dict(x=[0, 0.65]),
          )
      ]
  )

  fig.add_annotation(
      text=f"<b>{center_metric_title}</b><br><span style='font-size:22px; font-weight:bold;'>{center_metric_val}</span>",
      x=0.325,
      y=0.5,
      showarrow=False,
      font=dict(size=13, color="#111827"),
      align="center",
  )

  fig.update_layout(
      showlegend=True,
      legend=dict(
          x=0.70,
          y=0.5,
          xanchor="left",
          yanchor="middle",
          title=dict(text=f"<b>{legend_title}</b>"),
      ),
      margin=dict(l=0, r=0, t=10, b=10),
      height=230,
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
  )
  return fig


# -----------------------------------------------------------------------------
# 3. DONUT VISUALS GRID (2x2) IN SINGLE STYLED CONTAINERS
# -----------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

# --- CHART 1: RESTARTS ---
with row1_col1:
  with st.container(border=True):
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

    labels = ["Denmark", "Opposition"]
    values = [denmark_cnt, opposition_cnt]
    colors = ["#FF1E1E", "#4A0404"]

    if sum(values) > 0:
      fig_restarts = create_kpi_donut(
          labels=labels,
          values=values,
          colors=colors,
          center_metric_title="Kick Off<br>Score",
          center_metric_val=f"{kickoff_score:+d}"
          if kickoff_score > 0
          else str(kickoff_score),
          legend_title="End Possession",
      )
      st.plotly_chart(
          fig_restarts,
          use_container_width=True,
          config={"displayModeBar": False},
      )
    else:
      st.info("No data available")

# --- CHART 2: TURNOVERS ---
with row1_col2:
  with st.container(border=True):
    st.markdown(
        '<div class="kpi-card-title">Turnovers</div>', unsafe_allow_html=True
    )

    fig_turnovers = create_kpi_donut(
        labels=["Denmark", "Opposition"],
        values=[3, 3],
        colors=["#FF1E1E", "#4A0404"],
        center_metric_title="Turnover<br>Score",
        center_metric_val="0",
        legend_title="End Possession",
    )
    st.plotly_chart(
        fig_turnovers,
        use_container_width=True,
        config={"displayModeBar": False},
    )


row2_col1, row2_col2 = st.columns(2)

# --- CHART 3: TACKLES ---
with row2_col1:
  with st.container(border=True):
    st.markdown(
        '<div class="kpi-card-title">Tackles</div>', unsafe_allow_html=True
    )

    fig_tackles = create_kpi_donut(
        labels=["Completed", "Ineffective", "Missed"],
        values=[19, 2, 1],
        colors=["#FF1E1E", "#9CA3AF", "#4A0404"],
        center_metric_title="Tackle<br>Completion",
        center_metric_val="86%",
        legend_title="Outcome",
    )
    st.plotly_chart(
        fig_tackles,
        use_container_width=True,
        config={"displayModeBar": False},
    )

# --- CHART 4: ATTACKS ---
with row2_col2:
  with st.container(border=True):
    st.markdown(
        '<div class="kpi-card-title">Attacks</div>', unsafe_allow_html=True
    )

    fig_attacks = create_kpi_donut(
        labels=[
            "Try",
            "Penalty For",
            "Set Pieces Kept",
            "Open Play Kick",
            "Turnover Lost",
            "Penalty Against",
        ],
        values=[4, 1, 0, 0, 2, 1],
        colors=[
            "#FF1E1E",
            "#FCA5A5",
            "#D1D5DB",
            "#9CA3AF",
            "#4A0404",
            "#000000",
        ],
        center_metric_title="Attack<br>Completion",
        center_metric_val="57%",
        legend_title="Outcome",
    )
    st.plotly_chart(
        fig_attacks,
        use_container_width=True,
        config={"displayModeBar": False},
    )