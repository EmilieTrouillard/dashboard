import plotly.graph_objects as go
import streamlit as st
from typing import Literal
import pandas as pd
import plotly.express as px

TEAM = Literal["Denmark", "Opposition"]


def tries_sources_phases(team: TEAM, df: pd.DataFrame, opponent_name: str):
    team_name = "Denmark" if team == "Denmark" else opponent_name

    tries_df = df[df["event_type"] == "Try"].copy()

    # Aggregate counts by Origin, and Phase
    tries = tries_df[tries_df["end_possession"] == team]
    if tries.empty:
        return
    grouped = tries.groupby(["origin", "phases"]).size().reset_index(name="count")

    # Combine end_possession and origin for clear x-axis labels
    # Example label: "Kick Receipt<br>Denmark"
    grouped["x_label"] = grouped["origin"]

    # Convert phases to string for categorical color discrete mapping
    grouped["phases"] = grouped["phases"].astype(int).astype(str)

    # Define color palette matching the design (1: Solid Red, 2: Light Red/Pink, 3: Brown/Taupe)
    color_map = {
        "1": "#FF0000",
        "2": "#FF9999",
        "3": "#AA8888",
        "4+": "#666666",
    }

    # --- 2. BUILD PLOTLY CHART ---
    fig = px.bar(
        grouped,
        x="x_label",
        y="count",
        color="phases",
        text="count",
        title=f"<b>{team_name}</b>",
        color_discrete_map=color_map,
        barmode="stack",
        category_orders={"phases": sorted(grouped["phases"].unique())},
    )

    # --- 3. CUSTOMIZE LAYOUT & STYLING ---
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=14, color="white", family="Arial Black"),
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            title=dict(text="<b>Phases</b>"),
        ),
        font=dict(color="#333333"),
        title=dict(x=0.5, xanchor="center", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=20, r=20, t=50, b=80),
    )

    # Hide y-axis lines/labels for clean aesthetic
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False)
    return fig
