from typing import Literal

TEAM = Literal["Denmark", "Opposition"]


def opponent_name(df_filtered) -> str:
    return (
        df_filtered["opposition"].iloc[0]
        if "opposition" in df_filtered.columns
        and not df_filtered.empty
        and len(df_filtered["opposition"].unique()) == 1
        else "Opposition"
    )
