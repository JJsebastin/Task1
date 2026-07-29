"""
visualization_engine.py
========================
VisualizationEngine – generates charts using matplotlib.

Charts available:
    - Line chart: team score trend over time
    - Bar chart: total wins/losses/draws per team
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from .data_manager import DataManager


class VisualizationEngine:
    """Reads match data from DataManager and renders matplotlib charts."""

    # Color palette
    COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
              "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]

    def __init__(self, data_manager: DataManager):
        self._dm = data_manager
        plt.style.use("dark_background")

    # ── Public Methods ────────────────────────────────────────────────────────

    def plot_line_chart(self, team_name: str) -> None:
        """
        Plot a team's score over time (line chart).

        Parameters
        ----------
        team_name : str
            The team to plot.

        Raises
        ------
        ValueError
            If there is no data or the team is not found.
        """
        if self._dm.is_empty():
            raise ValueError("No match data to visualize.")

        df = self._dm.get_matches()
        home = df[df["team_1"] == team_name][["date", "score_1"]].rename(columns={"score_1": "score"})
        away = df[df["team_2"] == team_name][["date", "score_2"]].rename(columns={"score_2": "score"})
        team_df = (
            home._append(away)
            .sort_values("date")
            .reset_index(drop=True)
        )

        if team_df.empty:
            raise ValueError(f"No matches found for team '{team_name}'.")

        # Parse dates
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in team_df["date"]]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, team_df["score"], marker="o", linewidth=2.5,
                color=self.COLORS[0], markersize=8, label=team_name)
        ax.fill_between(dates, team_df["score"], alpha=0.15, color=self.COLORS[0])

        # Labels & formatting
        ax.set_title(f"⚽  {team_name} – Score Over Time", fontsize=14, pad=12)
        ax.set_xlabel("Match Date")
        ax.set_ylabel("Score")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        ax.legend()
        ax.grid(True, alpha=0.2)

        plt.tight_layout()
        plt.show()

    def plot_bar_chart(self) -> None:
        """
        Plot a grouped bar chart showing wins, losses, and draws per team.

        Raises
        ------
        ValueError
            If there is no data.
        """
        if self._dm.is_empty():
            raise ValueError("No match data to visualize.")

        from .analytics_engine import AnalyticsEngine
        ae = AnalyticsEngine(self._dm)
        stats_df = ae.get_summary_stats()

        teams = stats_df["Team"].tolist()
        x = range(len(teams))
        width = 0.25

        fig, ax = plt.subplots(figsize=(max(8, len(teams) * 1.5), 5))

        bars_w = ax.bar([i - width for i in x], stats_df["Wins"],
                        width=width, label="Wins", color=self.COLORS[4], alpha=0.9)
        bars_l = ax.bar(x, stats_df["Losses"],
                        width=width, label="Losses", color=self.COLORS[2], alpha=0.9)
        bars_d = ax.bar([i + width for i in x], stats_df["Draws"],
                        width=width, label="Draws", color=self.COLORS[1], alpha=0.9)

        # Value labels on bars
        for bars in (bars_w, bars_l, bars_d):
            for bar in bars:
                h = bar.get_height()
                if h:
                    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05,
                            str(int(h)), ha="center", va="bottom", fontsize=8)

        ax.set_title("🏆  Team Performance – Wins / Losses / Draws", fontsize=14, pad=12)
        ax.set_xlabel("Team")
        ax.set_ylabel("Matches")
        ax.set_xticks(list(x))
        ax.set_xticklabels(teams, rotation=15, ha="right")
        ax.legend()
        ax.grid(True, axis="y", alpha=0.2)

        plt.tight_layout()
        plt.show()
