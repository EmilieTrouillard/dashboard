import plotly.graph_objects as go
import streamlit as st
from typing import Literal
import pandas as pd
import plotly.express as px

TEAM = Literal["Denmark", "Opposition"]


def turnover_reasons_phases(df: pd.DataFrame):
    turnovers = df[df["event_type"] == "Turnover"].copy()

    if turnovers.empty:
        return
    grouped = turnovers.groupby(["reason", "outcome"]).size().reset_index(name="count")

    # Combine end_possession and origin for clear x-axis labels
    # Example label: "Kick Receipt<br>Denmark"
    grouped["x_label"] = grouped["reason"]

    # Convert phases to string for categorical color discrete mapping
    grouped["outcome"] = grouped["outcome"]

    # Define color palette matching the design (1: Solid Red, 2: Light Red/Pink, 3: Brown/Taupe)
    color_map = {"Won": "#FF0000", "Lost": "#4A0404"}

    # --- 2. BUILD PLOTLY CHART ---
    fig = px.bar(
        grouped,
        x="x_label",
        y="count",
        color="outcome",
        text="count",
        title="<b>Turnovers</b>",
        color_discrete_map=color_map,
        barmode="stack",
        category_orders={"outcome": sorted(grouped["outcome"].unique(), reverse=True)},
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
            orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5, title=None
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
