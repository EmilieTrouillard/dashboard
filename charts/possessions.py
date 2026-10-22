from typing import Tuple
from functools import reduce
import pandas as pd
import plotly.express as px
from .common import TEAM


def aggregate_events(df, metric_name):
    if df is None or df.empty:
        return pd.DataFrame(columns=["phases", metric_name])
    # Group by 'phases', count rows, and rename the column
    agg = df.groupby("phases").size().reset_index(name=metric_name)
    return agg


def possessions_sources_agg_df(
    df: pd.DataFrame, team: TEAM
) -> Tuple[pd.DataFrame, int, int, int]:
    possessions = df[
        (
            df["event_type"].isin(
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
        & ~(df["type"] == "Set Piece")
        & ~(df["penalty"] == "Penalty")
        & ~(df["completed"] == False)
        & ~(
            df["outcome"].isin(
                [
                    "Out",
                    "Lost Not Straight",
                    "Won Not Straight",
                    "Won - Out",
                    "Lost - Out",
                ]
            )
        )
        & (df["end_possession"] == team)
    ]

    tries_count = len(df[(df["event_type"] == "Try") & (df["end_possession"] == team)])
    # Aggregate data to count the number of events by type and original possession
    agg_df = (
        possessions.groupby(["event_type", "original_possession"])
        .size()
        .reset_index(name="count")
    )
    if team == "Opposition":
        agg_df.loc[agg_df["event_type"] == "Kick Off", "event_type"] = "temp"
        agg_df.loc[agg_df["event_type"] == "Kick Receipt", "event_type"] = "Kick Off"
        agg_df.loc[agg_df["event_type"] == "temp", "event_type"] = "Kick Receipt"
    max_count: int = (
        agg_df.groupby("event_type")["count"].sum().reset_index()["count"].max()
    )
    total_count: int = int(agg_df["count"].sum())
    return agg_df, max_count, total_count, tries_count


def possessions_sources_chart(agg_df: pd.DataFrame, max_range: int):

    totals = agg_df.groupby("event_type")["count"].sum().reset_index()
    sorted_events = totals.sort_values(by="count", ascending=False)[
        "event_type"
    ].tolist()

    # Create the grouped bar chart with Plotly Express
    fig = px.bar(
        agg_df,
        x="event_type",
        y="count",
        color="original_possession",
        barmode="stack",
        text="count",  # To display values on the bars if needed
        category_orders={
            "event_type": sorted_events,
            "original_possession": ["Denmark", "Opposition"],
        },  # Sort by highest bar
        color_discrete_map={
            "Denmark": "#ff0000",  # Bright red for Denmark
            "Opposition": "#3b0a0a",  # Dark brown for Opposition
        },
    )

    # Display values cleanly inside/above the bars
    fig.update_traces(textposition="inside", textfont_color="white")

    # Customize layout (title, subtitle, legend, grid)
    fig.update_layout(
        title={
            "text": "<b>Possession Sources</b>",
            "x": 0.5,
            "xanchor": "center",
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="",
        yaxis_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            title=dict(text="Original Possession"),
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f3f4f6",
            showticklabels=False,
            range=[0, max_range],
        ),
        bargap=0.2,
        bargroupgap=0.05,
    )
    return fig


def possessions_outcome_table(df: pd.DataFrame, team: TEAM):

    df_team = df[df["original_possession"] == team]
    df_tries = df_team[
        (df_team["event_type"] == "Try") & (df_team["end_possession"] == team)
    ]
    penalty_outcome_for = "Rewarded" if team == "Denmark" else "Conceeded"
    df_penalties_for = df_team[
        (df_team["event_type"] == "Penalty")
        & (df_team["outcome"] == penalty_outcome_for)
        & ~(df_team["reason"].isin(["Scrum", "Lineout"]))
    ]
    df_set_pieces_kept = df_team[
        (df_team["event_type"].isin(["Scrum", "Lineout"]))
        & (df_team["origin"] == "No Change")
    ]
    df_open_play_kicks = df_team[df_team["event_type"] == "Open Play Kick"]
    df_turnovers_lost = df_team[
        (df_team["event_type"] == "Turnover")
        & ~(df_team["penalty"] == "Penalty")
        & ~(df_team["reason"].isin(["PenKickOut Error"]))
        & (df_team["end_possession"] != team)
    ]
    penalties_against_outcome = "Conceeded" if team == "Denmark" else "Rewarded"
    df_penalties_against = df_team[
        (df_team["event_type"] == "Penalty")
        & (df_team["outcome"] == penalties_against_outcome)
        & ~(df_team["reason"].isin(["Scrum", "Lineout"]))
    ]

    # Process each DataFrame to convert raw rows into counts per phase
    df_tries_agg = aggregate_events(df_tries, "Tries Scored")
    df_penalties_for_agg = aggregate_events(df_penalties_for, "Penalties For")
    df_set_pieces_kept_agg = aggregate_events(df_set_pieces_kept, "Set Pieces Kept")
    df_open_play_kicks_agg = aggregate_events(df_open_play_kicks, "Open Play Kicks")
    df_turnovers_lost_agg = aggregate_events(df_turnovers_lost, "Turnovers Lost")
    df_penalties_against_agg = aggregate_events(
        df_penalties_against, "Penalties Against"
    )

    # List of all aggregated DataFrames
    dfs = [
        df_tries_agg,
        df_penalties_for_agg,
        df_set_pieces_kept_agg,
        df_open_play_kicks_agg,
        df_turnovers_lost_agg,
        df_penalties_against_agg,
    ]

    # Merge all DataFrames on the "phases" column using an outer join
    merged_df = reduce(
        lambda left, right: pd.merge(left, right, on="phases", how="outer"), dfs
    )

    # Drop rows where phases is missing, then convert phases to integer
    merged_df = merged_df.dropna(subset=["phases"])
    merged_df["phases"] = merged_df["phases"].astype(int)

    # Sort by phases in ascending order and reset index
    merged_df = merged_df.sort_values(by="phases").reset_index(drop=True)

    # Identify numerical columns (everything except 'phases')
    numeric_cols = [col for col in merged_df.columns if col != "phases"]

    # Fill NaNs with 0 in numeric columns so we can safely calculate and cast to int
    filled_df = merged_df.copy()
    filled_df[numeric_cols] = filled_df[numeric_cols].fillna(0)
    filled_df[numeric_cols] = filled_df[numeric_cols].astype(int)

    # --- TRANSPOSE TABLE ---
    # Set 'phases' as index and transpose so events become rows and phases become columns
    transposed = filled_df.set_index("phases").T

    # Calculate the "Total" column (sum across phases for each event)
    transposed["Total"] = transposed.sum(axis=1)

    # Calculate the "Total" row (sum across events for each phase)
    transposed.loc["Total"] = transposed.sum(axis=0)

    # Name index and reset to turn it into a regular column
    transposed.index.name = "Phases"
    final_df = transposed.reset_index()

    # Format for display: turn 0s into empty strings for inner cells, keep 0 for Totals
    display_df = final_df.copy()
    phase_cols = [col for col in display_df.columns if col not in ["Phases", "Total"]]

    for col in phase_cols + ["Total"]:
        display_df[col] = display_df[col].astype(str)
        display_df.loc[display_df["Phases"] != "Total", col] = display_df.loc[
            display_df["Phases"] != "Total", col
        ].replace({"0": ""})

    display_df.loc[display_df["Phases"] == "Total", phase_cols + ["Total"]] = (
        display_df.loc[display_df["Phases"] == "Total", phase_cols + ["Total"]].replace(
            {"": "0"}
        )
    )

    # Define row-specific styling function with placeholder colors
    def style_rows(row):
        event_name = row["Phases"]

        # Placeholder colors for each row (edit these hex codes as you prefer)
        row_colors = {
            "Tries Scored": "#FF1E1E",
            "Penalties For": "#CA0707",
            "Set Pieces Kept": "#700505",
            "Open Play Kicks": "#030201",
            "Turnovers Lost": "#575656",
            "Penalties Against": "#9b9b9b",
            "Total": "#111827",  # Dark Gray/Black for Total
        }

        color = row_colors.get(event_name, "#111827")

        if event_name == "Total":
            return [
                f"background-color: #f7f9fa; font-weight: bold; border-top: 2px solid #d1d5db; color: {color};"
            ] * len(row)
        else:
            return [
                (
                    f"color: {color}; font-weight: 500;"
                    if col not in ["Phases", "Total"]
                    else f"color: {color}; font-weight: bold;"
                )
                for col in row.index
            ]

    # Apply styling: white background, clean borders, center-aligned text
    styled_df = (
        display_df.style.apply(style_rows, axis=1)
        .set_properties(
            **{
                "background-color": "#FFFFFF",
                "border-color": "#e5e7eb",
                "padding": "8px 12px",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#FFFFFF"),
                        ("color", "#374151"),
                        ("font-weight", "bold"),
                        ("text-align", "center"),
                        ("border-bottom", "2px solid #d1d5db"),
                        ("padding", "10px 12px"),
                    ],
                },
                {
                    "selector": "table",
                    "props": [
                        ("background-color", "#FFFFFF"),
                        ("border-collapse", "collapse"),
                        ("width", "100%"),
                    ],
                },
                {
                    # Center-align all regular table data cells by default
                    "selector": "td",
                    "props": [
                        ("text-align", "center"),
                    ],
                },
                {
                    # Target the first column headers and cells to set width and left-align
                    "selector": "th:first-child, td:first-child",
                    "props": [
                        (
                            "min-width",
                            "180px",
                        ),  # Adjust this value if you need more/less space
                        ("text-align", "left"),
                        ("padding-left", "16px"),
                    ],
                },
            ]
        )
    )
    return styled_df
