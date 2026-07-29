"""
cli_controller.py
==================
CLIController – the main menu loop, user prompts, and routing logic.

This is the "brain" of the CLI. It creates and wires together
DataManager, AnalyticsEngine, and VisualizationEngine.
"""

import os
from .data_manager import DataManager
from .analytics_engine import AnalyticsEngine
from .visualization_engine import VisualizationEngine

# Default autosave path
DEFAULT_CSV = os.path.join("data", "matches.csv")

# ANSI colour helpers (work on Windows with modern terminal)
class C:
    HEADER  = "\033[95m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"


def _print_sep(char="─", width=52):
    print(C.CYAN + char * width + C.RESET)


class CLIController:
    """Entry-point controller that orchestrates the full CLI application."""

    def __init__(self):
        self._dm = DataManager()
        self._ae = AnalyticsEngine(self._dm)
        self._ve = VisualizationEngine(self._dm)

        # Auto-load saved data if it exists
        if os.path.isfile(DEFAULT_CSV):
            try:
                count = self._dm.import_csv(DEFAULT_CSV)
                print(f"{C.GREEN}✔  Loaded {count} saved match(es) from {DEFAULT_CSV}{C.RESET}")
            except Exception as e:
                print(f"{C.YELLOW}⚠  Could not load saved data: {e}{C.RESET}")

    # ── Main Menu ─────────────────────────────────────────────────────────────

    def main_menu(self) -> None:
        """Display the main menu in a loop until the user exits."""
        while True:
            print()
            _print_sep("═")
            print(f"{C.BOLD}{C.HEADER}  🏆  PlayStats – Sports Score Visualizer{C.RESET}")
            _print_sep("═")
            print(f"  {C.CYAN}[1]{C.RESET} Enter Match Result")
            print(f"  {C.CYAN}[2]{C.RESET} View / Edit Data")
            print(f"  {C.CYAN}[3]{C.RESET} Generate Charts")
            print(f"  {C.CYAN}[4]{C.RESET} View Analytics")
            print(f"  {C.CYAN}[5]{C.RESET} Import / Export Data")
            print(f"  {C.CYAN}[6]{C.RESET} Exit")
            _print_sep()

            choice = input("  Enter your choice: ").strip()

            if choice == "1":
                self.prompt_match_entry()
            elif choice == "2":
                self.prompt_edit()
            elif choice == "3":
                self.prompt_chart()
            elif choice == "4":
                self.prompt_analytics()
            elif choice == "5":
                self.prompt_import_export()
            elif choice == "6":
                self._exit()
                break
            else:
                print(f"{C.RED}  ✗ Invalid option. Please enter 1–6.{C.RESET}")

    # ── Option 1: Enter Match ─────────────────────────────────────────────────

    def prompt_match_entry(self) -> None:
        """Guided prompts to add a new match result."""
        _print_sep()
        print(f"{C.BOLD}  ➕  Enter Match Result{C.RESET}")
        _print_sep()

        date   = self._prompt_field("Date (YYYY-MM-DD)", validator=self._validate_date_input)
        team_1 = self._prompt_field("Team 1 name",       validator=self._validate_non_empty)
        team_2 = self._prompt_field("Team 2 name",       validator=self._validate_non_empty)
        score_1 = self._prompt_field(f"Score for {team_1}", validator=self._validate_score_input)
        score_2 = self._prompt_field(f"Score for {team_2}", validator=self._validate_score_input)

        try:
            self._dm.add_match(date, team_1, team_2, int(score_1), int(score_2))
            print(f"{C.GREEN}  ✔  Match added: {team_1} {score_1} – {score_2} {team_2} on {date}{C.RESET}")
        except ValueError as e:
            print(f"{C.RED}  ✗ Error: {e}{C.RESET}")

    # ── Option 2: View / Edit ─────────────────────────────────────────────────

    def prompt_edit(self) -> None:
        """Display matches and allow the user to edit or delete one."""
        if self._dm.is_empty():
            print(f"{C.YELLOW}  ⚠  No matches recorded yet.{C.RESET}")
            return

        self._display_matches()

        action = input(
            "\n  Enter match ID to [e]dit / [d]elete, or press Enter to go back: "
        ).strip()

        if not action:
            return

        try:
            match_id = int(action)
        except ValueError:
            print(f"{C.RED}  ✗ Please enter a valid numeric ID.{C.RESET}")
            return

        sub = input("  Action – [e]dit or [d]elete? ").strip().lower()

        if sub == "e":
            self._do_edit(match_id)
        elif sub == "d":
            self._do_delete(match_id)
        else:
            print(f"{C.RED}  ✗ Unknown action.{C.RESET}")

    def _do_edit(self, match_id: int) -> None:
        print(f"  (Leave blank to keep current value)")
        df = self._dm.get_matches()
        row = df.loc[match_id]
        updates = {}

        fields = {
            "date":    f"Date [{row['date']}]",
            "team_1":  f"Team 1 [{row['team_1']}]",
            "team_2":  f"Team 2 [{row['team_2']}]",
            "score_1": f"Score 1 [{row['score_1']}]",
            "score_2": f"Score 2 [{row['score_2']}]",
        }

        for key, label in fields.items():
            val = input(f"  {label}: ").strip()
            if val:
                updates[key] = val

        if not updates:
            print(f"{C.YELLOW}  No changes made.{C.RESET}")
            return

        try:
            self._dm.edit_match(match_id, **updates)
            print(f"{C.GREEN}  ✔  Match #{match_id} updated.{C.RESET}")
        except (IndexError, ValueError) as e:
            print(f"{C.RED}  ✗ {e}{C.RESET}")

    def _do_delete(self, match_id: int) -> None:
        confirm = input(f"  Delete match #{match_id}? (y/N): ").strip().lower()
        if confirm == "y":
            try:
                self._dm.delete_match(match_id)
                print(f"{C.GREEN}  ✔  Match #{match_id} deleted.{C.RESET}")
            except IndexError as e:
                print(f"{C.RED}  ✗ {e}{C.RESET}")
        else:
            print("  Cancelled.")

    # ── Option 3: Generate Charts ─────────────────────────────────────────────

    def prompt_chart(self) -> None:
        """Ask which chart to show and render it."""
        if self._dm.is_empty():
            print(f"{C.YELLOW}  ⚠  No data to visualize. Add some matches first.{C.RESET}")
            return

        _print_sep()
        print(f"{C.BOLD}  📊  Generate Chart{C.RESET}")
        _print_sep()
        print(f"  {C.CYAN}[1]{C.RESET} Line chart – team score over time")
        print(f"  {C.CYAN}[2]{C.RESET} Bar chart  – wins / losses / draws per team")
        choice = input("  Chart type: ").strip()

        if choice == "1":
            team = input("  Enter team name: ").strip()
            if not team:
                print(f"{C.RED}  ✗ Team name cannot be empty.{C.RESET}")
                return
            try:
                self._ve.plot_line_chart(team)
            except ValueError as e:
                print(f"{C.RED}  ✗ {e}{C.RESET}")

        elif choice == "2":
            try:
                self._ve.plot_bar_chart()
            except ValueError as e:
                print(f"{C.RED}  ✗ {e}{C.RESET}")

        else:
            print(f"{C.RED}  ✗ Invalid choice.{C.RESET}")

    # ── Option 4: Analytics ───────────────────────────────────────────────────

    def prompt_analytics(self) -> None:
        """Display summary stats for all teams, then optionally a single team."""
        if self._dm.is_empty():
            print(f"{C.YELLOW}  ⚠  No match data available. Add some matches first.{C.RESET}")
            return

        try:
            stats = self._ae.get_summary_stats()
            _print_sep()
            print(f"{C.BOLD}  📈  Summary Statistics – All Teams{C.RESET}")
            _print_sep()
            print(stats.to_string(index=False))

            # Highest-scoring match
            best = self._ae.get_highest_scoring_match()
            print(f"\n  {C.GREEN}🔥  Highest-scoring match:{C.RESET}")
            print(f"     {best['team_1']} {int(best['score_1'])} – {int(best['score_2'])} "
                  f"{best['team_2']}  [{best['date']}]")

        except ValueError as e:
            print(f"{C.RED}  ✗ {e}{C.RESET}")
            return

        see_team = input("\n  View stats for a specific team? (y/N): ").strip().lower()
        if see_team == "y":
            team = input("  Team name: ").strip()
            try:
                ts = self._ae.get_team_stats(team)
                _print_sep()
                print(f"{C.BOLD}  📋  Stats for {team}{C.RESET}")
                _print_sep()
                for k, v in ts.items():
                    print(f"   {C.CYAN}{k:<18}{C.RESET} {v}")
            except ValueError as e:
                print(f"{C.RED}  ✗ {e}{C.RESET}")

    # ── Option 5: Import / Export ─────────────────────────────────────────────

    def prompt_import_export(self) -> None:
        """Handle CSV import or export."""
        _print_sep()
        print(f"{C.BOLD}  💾  Import / Export Data{C.RESET}")
        _print_sep()
        print(f"  {C.CYAN}[1]{C.RESET} Import from CSV")
        print(f"  {C.CYAN}[2]{C.RESET} Export to CSV")
        print(f"  {C.CYAN}[3]{C.RESET} Back")
        choice = input("  Choice: ").strip()

        if choice == "1":
            path = input("  Enter CSV filepath: ").strip()
            if not path:
                print(f"{C.YELLOW}  Cancelled.{C.RESET}")
                return
            try:
                count = self._dm.import_csv(path)
                print(f"{C.GREEN}  ✔  Imported {count} match(es) from '{path}'.{C.RESET}")
            except (FileNotFoundError, ValueError) as e:
                print(f"{C.RED}  ✗ {e}{C.RESET}")

        elif choice == "2":
            path = input(
                f"  Enter output filepath [default: {DEFAULT_CSV}]: "
            ).strip() or DEFAULT_CSV
            try:
                self._dm.export_csv(path)
                print(f"{C.GREEN}  ✔  Data exported to '{path}'.{C.RESET}")
            except OSError as e:
                print(f"{C.RED}  ✗ Export failed: {e}{C.RESET}")

        elif choice == "3":
            return
        else:
            print(f"{C.RED}  ✗ Invalid choice.{C.RESET}")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _exit(self) -> None:
        """Auto-save before quitting."""
        if not self._dm.is_empty():
            try:
                self._dm.export_csv(DEFAULT_CSV)
                print(f"{C.GREEN}  ✔  Data auto-saved to {DEFAULT_CSV}{C.RESET}")
            except OSError as e:
                print(f"{C.YELLOW}  ⚠  Auto-save failed: {e}{C.RESET}")
        print(f"\n{C.BOLD}  Goodbye! 🏆{C.RESET}\n")

    def _display_matches(self) -> None:
        """Print the current match table to the terminal."""
        df = self._dm.get_matches()
        _print_sep()
        print(f"{C.BOLD}  📋  All Matches ({len(df)} record(s)){C.RESET}")
        _print_sep()
        print(f"  {'ID':<5} {'Date':<12} {'Team 1':<18} {'Score':^7} {'Team 2':<18}")
        _print_sep("─", 60)
        for idx, row in df.iterrows():
            score = f"{int(row['score_1'])} – {int(row['score_2'])}"
            print(f"  {idx:<5} {row['date']:<12} {row['team_1']:<18} {score:^7} {row['team_2']:<18}")

    def _prompt_field(self, label: str, validator=None) -> str:
        """Repeatedly prompt until validator passes (or there's no validator)."""
        while True:
            val = input(f"  {label}: ").strip()
            if validator:
                error = validator(val)
                if error:
                    print(f"{C.RED}  ✗ {error}{C.RESET}")
                    continue
            return val

    # ── Field Validators (return error string or None) ─────────────────────────

    @staticmethod
    def _validate_date_input(val: str):
        from datetime import datetime
        try:
            datetime.strptime(val, "%Y-%m-%d")
        except ValueError:
            return f"Invalid date '{val}'. Use YYYY-MM-DD."
        return None

    @staticmethod
    def _validate_non_empty(val: str):
        if not val:
            return "This field cannot be empty."
        return None

    @staticmethod
    def _validate_score_input(val: str):
        try:
            if int(val) < 0:
                raise ValueError()
        except ValueError:
            return f"Score must be a non-negative integer. Got '{val}'."
        return None
