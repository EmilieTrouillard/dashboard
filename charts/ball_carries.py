import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
from .common import TEAM


def ball_carries_per_player(df: pd.DataFrame):
    carries = df[df["event_type"] == "Ball Carry"].copy()
    carries.loc[carries["tackle_outcome"] == "Completed", "tackle_outcome"] = "Tackled"
    carries.loc[carries["tackle_outcome"] == "Missed", "tackle_outcome"] = "Offload"
    carries.loc[carries["tackle_outcome"] == "Ineffective", "tackle_outcome"] = (
        "Broken / Missed Tackle"
    )
    if carries.empty:
        return
    grouped = (
        carries.groupby(["player", "tackle_outcome"])
        .size()
        .reset_index(name="count")
        .sort_values(by=["player", "tackle_outcome"])
    )

    # Calculate total ball carries per player
    total_carries_per_player = (
        grouped.groupby("player")["count"].sum().reset_index(name="total_count")
    )

    # Merge total counts back to the grouped DataFrame
    grouped = pd.merge(grouped, total_carries_per_player, on="player")
    grouped["percentage"] = (grouped["count"] / grouped["total_count"]) * 100

    # Define color palette matching the design (1: Solid Red, 2: Light Red/Pink, 3: Brown/Taupe)
    color_map = {
        "Broken / Missed Tackle": "#FF1E1E",
        "Tackled": "#4A0404",
        "Offload": "#9CA3AF",
    }

    fig = px.bar(
        grouped,
        x="player",
        y="count",
        color="tackle_outcome",
        text=[
            f"{i} <b>{j:.0f}%</b>"
            for i, j in zip(grouped["count"], grouped["percentage"])
        ],
        title="<b>Ball Carries</b>",
        color_discrete_map=color_map,
        barmode="stack",
        category_orders={"tackle_outcome": sorted(grouped["tackle_outcome"].unique())},
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=13, color="white"),
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5, title=None
        ),
        font=dict(color="#333333"),
        title=dict(x=0.5, xanchor="center", font=dict(size=20)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=20, r=20, t=50, b=80),
    )
    return fig
