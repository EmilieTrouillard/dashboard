import plotly.graph_objects as go
import streamlit as st
from typing import Literal
import pandas as pd

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
            y=-0.3,
            xanchor="center",
            x=0.5,
            itemclick=False,
            itemdoubleclick=False,
            traceorder="normal",
        ),
        height=120,
        margin=dict(l=10, r=10, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
