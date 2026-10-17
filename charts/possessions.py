import plotly.graph_objects as go
import streamlit as st
from typing import Literal
from functools import reduce
import pandas as pd
import plotly.express as px
from .common import TEAM


# Define styling function for the Total row
def highlight_total(row):
    if row["Phases"] == "Total":
        return [
            "background-color: #f7f9fa; font-weight: bold; border-top: 2px solid #d1d5db;"
        ] * len(row)
    return [""] * len(row)


def aggregate_events(df, metric_name):
    if df is None or df.empty:
        return pd.DataFrame(columns=["phases", metric_name])
    # Group by 'phases', count rows, and rename the column
    agg = df.groupby("phases").size().reset_index(name=metric_name)
    return agg


def possessions_table(df: pd.DataFrame, team: TEAM):
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
        & (df["original_possession"] == team)
    ]
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

    # 2. Merge all DataFrames on the "phases" column using an outer join
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

    # Convert numeric columns to integers
    filled_df[numeric_cols] = filled_df[numeric_cols].astype(int)

    # 3. Calculate the "Total" column (sum across each row)
    filled_df["Total"] = filled_df[numeric_cols].sum(axis=1)

    # 4. Calculate the "Total" row (sum across each column)
    total_row = filled_df[numeric_cols].sum(numeric_only=True)
    total_row["phases"] = "Total"
    total_row["Total"] = filled_df["Total"].sum()

    # Append the "Total" row to the DataFrame
    total_df = pd.DataFrame([total_row])
    total_df[numeric_cols + ["Total"]] = total_df[numeric_cols + ["Total"]].astype(int)

    final_df = pd.concat([filled_df, total_df], ignore_index=True)

    # 5. Format for display: turn 0s into empty strings for inner cells, keep 0 for Totals
    display_df = final_df.copy()

    for col in numeric_cols + ["Total"]:
        display_df[col] = display_df[col].astype(str)
        display_df.loc[display_df["phases"] != "Total", col] = display_df.loc[
            display_df["phases"] != "Total", col
        ].replace({"0": ""})

    display_df.loc[display_df["phases"] == "Total", numeric_cols + ["Total"]] = (
        display_df.loc[
            display_df["phases"] == "Total", numeric_cols + ["Total"]
        ].replace({"": "0"})
    )

    # Rename column "phases" to "Phases"
    display_df = display_df.rename(columns={"phases": "Phases"})

    # Apply styling: white background, clean borders, center-aligned text
    styled_df = (
        display_df.style.apply(highlight_total, axis=1)
        .set_properties(
            **{
                "background-color": "#FFFFFF",
                "color": "#111827",
                "text-align": "center",
                "border-color": "#e5e7eb",
                "padding": "8px 12px",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#f9fafb"),
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
            ]
        )
    )
    return styled_df
