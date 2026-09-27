import plotly.graph_objects as go
import streamlit as st
from typing import Literal
import pandas as pd
import plotly.express as px

TEAM = Literal["Denmark", "Opposition"]


def tackle_completion_bar(team: TEAM, df: pd.DataFrame, opponent_name: str):
    event_type = "Tackle" if team == "Denmark" else "Ball Carry"
    outcome_col = "outcome" if team == "Denmark" else "tackle_outcome"
    team_name = "Denmark" if team == "Denmark" else opponent_name
    fig = go.Figure()

    tackles = df[df["event_type"] == event_type].copy()
    total_tackles = len(tackles)
    categories = tackles[outcome_col].value_counts().to_dict()
    color_map: dict[str, str] = {
        "Completed": "#FF1E1E",
        "Missed": "#4A0404",
        "Ineffective": "#9CA3AF",
    }
    for key, value in categories.items():
        key = str(key)
        pct = (value / total_tackles) * 100 if total_tackles > 0 else 0
        label_text = f"{value} <b>{pct:.0f}%</b>"

        fig.add_trace(
            go.Bar(
                y=["Tackles"],
                x=[pct],
                name=key,
                orientation="h",
                marker=dict(color=color_map[key]),
                text=label_text,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=13),
                hovertemplate=f"<b>{key}</b>: {value} ({pct:.1f}%)<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        title=dict(
            text=f"<b>Tackle Completion - {team_name}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#111827"),
        ),
        xaxis=dict(
            range=[0, 100],
            tickvals=[0, 50, 100],
            ticktext=["0%", "50%", "100%"],
            showgrid=True,
            gridcolor="#E5E7EB",
            gridwidth=1,
            griddash="dot",
            zeroline=False,
        ),
        yaxis=dict(showticklabels=False, showgrid=False),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-1.0,
            xanchor="center",
            x=0.5,
            itemclick=False,
            itemdoubleclick=False,
            traceorder="normal",
        ),
        height=140,
        margin=dict(l=10, r=10, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def tackle_completion_per_player(df: pd.DataFrame):
    tackles = df[df["event_type"] == "Tackle"].copy()
    if tackles.empty:
        return
    grouped = (
        tackles.groupby(["player", "outcome"])
        .size()
        .reset_index(name="count")
        .sort_values(by=["player", "outcome"])
    )

    # Calculate total tackles per player
    total_tackles_per_player = (
        grouped.groupby("player")["count"].sum().reset_index(name="total_count")
    )

    # Merge total counts back to the grouped DataFrame
    grouped = pd.merge(grouped, total_tackles_per_player, on="player")
    grouped["percentage"] = (grouped["count"] / grouped["total_count"]) * 100

    # Define color palette matching the design (1: Solid Red, 2: Light Red/Pink, 3: Brown/Taupe)
    color_map = {
        "Completed": "#FF1E1E",
        "Missed": "#4A0404",
        "Ineffective": "#9CA3AF",
    }

    fig = px.bar(
        grouped,
        x="player",
        y="count",
        color="outcome",
        text=[
            f"{i} <b>{j:.0f}%</b>"
            for i, j in zip(grouped["count"], grouped["percentage"])
        ],
        title="<b>Tackle Completion per Player</b>",
        color_discrete_map=color_map,
        barmode="stack",
        category_orders={"outcome": sorted(grouped["outcome"].unique())},
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
