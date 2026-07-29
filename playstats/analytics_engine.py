"""
analytics_engine.py
====================
AnalyticsEngine – computes summary statistics from match data
provided by DataManager.

Metrics computed:
    - Wins / Losses / Draws per team
    - Total matches played
    - Average score per team
    - Highest-scoring match
"""

import pandas as pd
from .data_manager import DataManager


class AnalyticsEngine:
    """Reads match data from DataManager and produces summary statistics."""

    def __init__(self, data_manager: DataManager):
        self._dm = data_manager

    # ── Public Methods ────────────────────────────────────────────────────────

    def get_summary_stats(self) -> pd.DataFrame:
        """
        Compute wins, losses, draws, total matches, and average score
        for every team in the dataset.

        Returns
        -------
        pd.DataFrame
            Columns: team, played, wins, losses, draws, avg_scored, avg_conceded

        Raises
        ------
        ValueError
            If there is no match data.
        """
        if self._dm.is_empty():
            raise ValueError("No match data available to compute statistics.")

        df = self._dm.get_matches()
        records = []

        teams = set(df["team_1"].tolist() + df["team_2"].tolist())
        for team in sorted(teams):
            home = df[df["team_1"] == team]
            away = df[df["team_2"] == team]

            wins = (
                (home["score_1"] > home["score_2"]).sum()
                + (away["score_2"] > away["score_1"]).sum()
            )
            losses = (
                (home["score_1"] < home["score_2"]).sum()
                + (away["score_2"] < away["score_1"]).sum()
            )
            draws = (
                (home["score_1"] == home["score_2"]).sum()
                + (away["score_1"] == away["score_2"]).sum()
            )

            scored = list(home["score_1"]) + list(away["score_2"])
            conceded = list(home["score_2"]) + list(away["score_1"])
            played = len(scored)

            avg_scored = round(sum(scored) / played, 2) if played else 0
            avg_conceded = round(sum(conceded) / played, 2) if played else 0

            records.append({
                "Team": team,
                "Played": played,
                "Wins": int(wins),
                "Losses": int(losses),
                "Draws": int(draws),
                "Avg Scored": avg_scored,
                "Avg Conceded": avg_conceded,
            })

        return pd.DataFrame(records)

    def get_team_stats(self, team_name: str) -> dict:
        """
        Return detailed statistics for a single team.

        Parameters
        ----------
        team_name : str
            Name of the team (case-sensitive).

        Returns
        -------
        dict
            Statistics for the given team.

        Raises
        ------
        ValueError
            If the team is not found or there is no data.
        """
        if self._dm.is_empty():
            raise ValueError("No match data available.")

        df = self._dm.get_matches()
        home = df[df["team_1"] == team_name]
        away = df[df["team_2"] == team_name]

        if home.empty and away.empty:
            raise ValueError(f"Team '{team_name}' not found in any match record.")

        wins = (
            (home["score_1"] > home["score_2"]).sum()
            + (away["score_2"] > away["score_1"]).sum()
        )
        losses = (
            (home["score_1"] < home["score_2"]).sum()
            + (away["score_2"] < away["score_1"]).sum()
        )
        draws = (
            (home["score_1"] == home["score_2"]).sum()
            + (away["score_1"] == away["score_2"]).sum()
        )

        scored = list(home["score_1"]) + list(away["score_2"])
        conceded = list(home["score_2"]) + list(away["score_1"])
        played = len(scored)

        return {
            "Team": team_name,
            "Played": played,
            "Wins": int(wins),
            "Losses": int(losses),
            "Draws": int(draws),
            "Total Scored": sum(scored),
            "Total Conceded": sum(conceded),
            "Avg Scored": round(sum(scored) / played, 2) if played else 0,
            "Avg Conceded": round(sum(conceded) / played, 2) if played else 0,
        }

    def get_highest_scoring_match(self) -> pd.Series:
        """
        Return the match row with the highest combined score.

        Raises
        ------
        ValueError
            If there is no match data.
        """
        if self._dm.is_empty():
            raise ValueError("No match data available.")

        df = self._dm.get_matches()
        df["_total"] = df["score_1"] + df["score_2"]
        best = df.loc[df["_total"].idxmax()]
        return best.drop("_total")
