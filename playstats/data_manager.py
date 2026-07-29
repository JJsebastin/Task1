"""
data_manager.py
===============
DataManager – handles in-memory match data storage (pandas DataFrame)
and CSV import/export.

DataFrame schema:
    ['date', 'team_1', 'team_2', 'score_1', 'score_2']
"""

import os
from datetime import datetime

import pandas as pd


class DataManager:
    """Manages match records in memory and persists them via CSV."""

    COLUMNS = ["date", "team_1", "team_2", "score_1", "score_2"]

    def __init__(self):
        self._df = pd.DataFrame(columns=self.COLUMNS)

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_matches(self) -> pd.DataFrame:
        """Return a copy of the current match DataFrame."""
        return self._df.copy()

    def is_empty(self) -> bool:
        """Return True if there are no matches recorded."""
        return self._df.empty

    # ── Create ────────────────────────────────────────────────────────────────

    def add_match(self, date: str, team_1: str, team_2: str,
                  score_1: int, score_2: int) -> None:
        """
        Validate and append a new match record.

        Raises
        ------
        ValueError
            If any field fails validation.
        """
        self._validate_date(date)
        self._validate_team(team_1, "Team 1")
        self._validate_team(team_2, "Team 2")
        self._validate_score(score_1, "Score 1")
        self._validate_score(score_2, "Score 2")

        new_row = pd.DataFrame(
            [[date, team_1.strip(), team_2.strip(), int(score_1), int(score_2)]],
            columns=self.COLUMNS,
        )
        self._df = pd.concat([self._df, new_row], ignore_index=True)

    # ── Update ────────────────────────────────────────────────────────────────

    def edit_match(self, match_id: int, **kwargs) -> None:
        """
        Edit an existing match by its DataFrame index.

        Supported kwargs: date, team_1, team_2, score_1, score_2
        Only fields provided in kwargs are updated.

        Raises
        ------
        IndexError
            If match_id is out of range.
        ValueError
            If a field fails validation.
        """
        if match_id not in self._df.index:
            raise IndexError(f"No match with ID {match_id}.")

        if "date" in kwargs:
            self._validate_date(kwargs["date"])
            self._df.at[match_id, "date"] = kwargs["date"]

        if "team_1" in kwargs:
            self._validate_team(kwargs["team_1"], "Team 1")
            self._df.at[match_id, "team_1"] = kwargs["team_1"].strip()

        if "team_2" in kwargs:
            self._validate_team(kwargs["team_2"], "Team 2")
            self._df.at[match_id, "team_2"] = kwargs["team_2"].strip()

        if "score_1" in kwargs:
            self._validate_score(kwargs["score_1"], "Score 1")
            self._df.at[match_id, "score_1"] = int(kwargs["score_1"])

        if "score_2" in kwargs:
            self._validate_score(kwargs["score_2"], "Score 2")
            self._df.at[match_id, "score_2"] = int(kwargs["score_2"])

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_match(self, match_id: int) -> None:
        """
        Remove a match by its DataFrame index.

        Raises
        ------
        IndexError
            If match_id is out of range.
        """
        if match_id not in self._df.index:
            raise IndexError(f"No match with ID {match_id}.")
        self._df = self._df.drop(index=match_id).reset_index(drop=True)

    # ── Persistence ───────────────────────────────────────────────────────────

    def export_csv(self, filepath: str) -> None:
        """
        Save the current DataFrame to a CSV file.

        Creates parent directories if they don't exist.

        Raises
        ------
        OSError
            If the file cannot be written.
        """
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        self._df.to_csv(filepath, index=False)

    def import_csv(self, filepath: str) -> int:
        """
        Load matches from a CSV file and merge with current data.

        Returns
        -------
        int
            Number of records loaded.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the CSV schema does not match.
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        loaded = pd.read_csv(filepath)

        # Validate columns
        missing = set(self.COLUMNS) - set(loaded.columns)
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {missing}\n"
                f"Expected: {self.COLUMNS}"
            )

        # Keep only the expected columns and cast types
        loaded = loaded[self.COLUMNS]
        loaded["score_1"] = pd.to_numeric(loaded["score_1"], errors="coerce").fillna(0).astype(int)
        loaded["score_2"] = pd.to_numeric(loaded["score_2"], errors="coerce").fillna(0).astype(int)

        self._df = pd.concat([self._df, loaded], ignore_index=True)
        return len(loaded)

    # ── Validation helpers ────────────────────────────────────────────────────

    @staticmethod
    def _validate_date(date: str) -> None:
        try:
            datetime.strptime(date.strip(), "%Y-%m-%d")
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid date '{date}'. Use YYYY-MM-DD format.")

    @staticmethod
    def _validate_team(name: str, label: str) -> None:
        if not name or not name.strip():
            raise ValueError(f"{label} name cannot be empty.")

    @staticmethod
    def _validate_score(score, label: str) -> None:
        try:
            val = int(score)
            if val < 0:
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a non-negative integer. Got: '{score}'")
