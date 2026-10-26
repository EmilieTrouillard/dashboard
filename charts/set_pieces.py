from typing import Tuple
from functools import reduce
import pandas as pd
import plotly.express as px
from .common import TEAM


def set_pieces_rates(df: pd.DataFrame) -> dict[str, int | None]:
    res: dict[str, int | None] = {
        "scrum_retention_rate": None,
        "lineout_retention_rate": None,
        "scrum_steal_rate": None,
        "lineout_steal_rate": None,
    }
    dk_scrums = df[
        (df["event_type"] == "Scrum") & (df["original_possession"] == "Denmark")
    ]
    total_dk_scrums = len(dk_scrums)
    if total_dk_scrums > 0:
        dk_scrum_retained = len(dk_scrums[dk_scrums["end_possession"] == "Denmark"])
        res["scrum_retention_rate"] = int((dk_scrum_retained / total_dk_scrums) * 100)
    opp_scrums = df[
        (df["event_type"] == "Scrum") & (df["original_possession"] == "Opposition")
    ]
    total_opp_scrums = len(opp_scrums)
    if total_opp_scrums > 0:
        opp_scrum_lost = len(opp_scrums[opp_scrums["end_possession"] == "Denmark"])
        res["scrum_steal_rate"] = int((opp_scrum_lost / total_opp_scrums) * 100)
    dk_lineouts = df[
        (df["event_type"] == "Lineout") & (df["original_possession"] == "Denmark")
    ]
    total_dk_lineouts = len(dk_lineouts)
    if total_dk_lineouts > 0:
        dk_lineout_retained = len(
            dk_lineouts[dk_lineouts["end_possession"] == "Denmark"]
        )
        res["lineout_retention_rate"] = int(
            (dk_lineout_retained / total_dk_lineouts) * 100
        )
    opp_lineouts = df[
        (df["event_type"] == "Lineout") & (df["original_possession"] == "Opposition")
    ]
    total_opp_lineouts = len(opp_lineouts)
    if total_opp_lineouts > 0:
        opp_lineout_lost = len(
            opp_lineouts[opp_lineouts["end_possession"] == "Denmark"]
        )
        res["lineout_steal_rate"] = int((opp_lineout_lost / total_opp_lineouts) * 100)
    return res
