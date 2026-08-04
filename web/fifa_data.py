"""FIFA 2026 World Cup – Data layer reading from CSV files."""
import csv
import os

# ──────────────────────────────────────────────────────────────────────────────
# ACCURATE 48-team groups for FIFA World Cup 2026 (derived from matches.csv)
# ──────────────────────────────────────────────────────────────────────────────
GROUPS = {
    "A": ["Argentina", "Austria", "Algeria", "Jordan"],
    "B": ["United States", "Australia", "Paraguay", "Türkiye"],
    "C": ["Belgium", "Egypt", "IR Iran", "New Zealand"],
    "D": ["Canada", "Switzerland", "Qatar", "Bosnia–Herz"],
    "E": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "F": ["Spain", "Uruguay", "Saudi Arabia", "Cabo Verde"],
    "G": ["Portugal", "Colombia", "Uzbekistan", "Congo DR"],
    "H": ["England", "Croatia", "Panama", "Ghana"],
    "I": ["Germany", "Ecuador", "Côte d'Ivoire", "Curaçao"],
    "J": ["Mexico", "Korea Republic", "South Africa", "Czechia"],
    "K": ["France", "Norway", "Senegal", "Iraq"],
    "L": ["Netherlands", "Japan", "Sweden", "Tunisia"],
}

# ──────────────────────────────────────────────────────────────────────────────
# FLAGS – emoji flags for all 48 teams
# ──────────────────────────────────────────────────────────────────────────────
FLAGS = {
    "Argentina": "🇦🇷", "Austria": "🇦🇹", "Algeria": "🇩🇿", "Jordan": "🇯🇴",
    "United States": "🇺🇸", "Australia": "🇦🇺", "Paraguay": "🇵🇾", "Türkiye": "🇹🇷",
    "Belgium": "🇧🇪", "Egypt": "🇪🇬", "IR Iran": "🇮🇷", "New Zealand": "🇳🇿",
    "Canada": "🇨🇦", "Switzerland": "🇨🇭", "Qatar": "🇶🇦", "Bosnia–Herz": "🇧🇦",
    "Brazil": "🇧🇷", "Morocco": "🇲🇦", "Haiti": "🇭🇹", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Spain": "🇪🇸", "Uruguay": "🇺🇾", "Saudi Arabia": "🇸🇦", "Cabo Verde": "🇨🇻",
    "Portugal": "🇵🇹", "Colombia": "🇨🇴", "Uzbekistan": "🇺🇿", "Congo DR": "🇨🇩",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croatia": "🇭🇷", "Panama": "🇵🇦", "Ghana": "🇬🇭",
    "Germany": "🇩🇪", "Ecuador": "🇪🇨", "Côte d'Ivoire": "🇨🇮", "Curaçao": "🇨🇼",
    "Mexico": "🇲🇽", "Korea Republic": "🇰🇷", "South Africa": "🇿🇦", "Czechia": "🇨🇿",
    "France": "🇫🇷", "Norway": "🇳🇴", "Senegal": "🇸🇳", "Iraq": "🇮🇶",
    "Netherlands": "🇳🇱", "Japan": "🇯🇵", "Sweden": "🇸🇪", "Tunisia": "🇹🇳",
}

# Flag CDN base URL (flagcdn.com – reliable, no emoji dependency)
_CDN = "https://flagcdn.com/48x36"

# ISO country codes for flag CDN
_COUNTRY_CODES = {
    "Argentina": "ar", "Austria": "at", "Algeria": "dz", "Jordan": "jo",
    "United States": "us", "Australia": "au", "Paraguay": "py", "Türkiye": "tr",
    "Belgium": "be", "Egypt": "eg", "IR Iran": "ir", "New Zealand": "nz",
    "Canada": "ca", "Switzerland": "ch", "Qatar": "qa", "Bosnia–Herz": "ba",
    "Brazil": "br", "Morocco": "ma", "Haiti": "ht", "Scotland": "gb-sct",
    "Spain": "es", "Uruguay": "uy", "Saudi Arabia": "sa", "Cabo Verde": "cv",
    "Portugal": "pt", "Colombia": "co", "Uzbekistan": "uz", "Congo DR": "cd",
    "England": "gb-eng", "Croatia": "hr", "Panama": "pa", "Ghana": "gh",
    "Germany": "de", "Ecuador": "ec", "Côte d'Ivoire": "ci", "Curaçao": "cw",
    "Mexico": "mx", "Korea Republic": "kr", "South Africa": "za", "Czechia": "cz",
    "France": "fr", "Norway": "no", "Senegal": "sn", "Iraq": "iq",
    "Netherlands": "nl", "Japan": "jp", "Sweden": "se", "Tunisia": "tn",
}

# Reverse lookup: team → group letter
_TEAM_TO_GROUP = {}
for _g, _teams in GROUPS.items():
    for _t in _teams:
        _TEAM_TO_GROUP[_t] = _g

# ── Stage name normalisation ─────────────────────────────────────────────────
# CSV uses these exact strings; map them to display-friendly names
_STAGE_MAP = {
    "Group stage": "Group Stage",
    "Round of 32": "Round of 32",
    "Round of 16": "Round of 16",
    "Quarter-finals": "Quarter-finals",
    "Semi-finals": "Semi-finals",
    "Third-place match": "Third Place",
    "Final": "Final",
}

# ── Winner / special info ────────────────────────────────────────────────────
TOURNAMENT_WINNER = "Spain"
TOURNAMENT_RUNNER_UP = "Argentina"
FINAL_SCORE = "1–0 (AET)"
GOLDEN_BOOT = {"name": "Kylian Mbappé", "team": "France", "goals": 10}

# ── CSV paths ────────────────────────────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MATCHES_CSV = os.path.join(_BASE_DIR, "matches.csv")
_PLAYERS_CSV = os.path.join(_BASE_DIR, "players.csv")


# ══════════════════════════════════════════════════════════════════════════════
# MATCH PARSING
# ══════════════════════════════════════════════════════════════════════════════

def _safe_float(val):
    """Safely convert a value to float, returning 0.0 on failure."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def _safe_int(val):
    """Safely convert a value to int, returning 0 on failure."""
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0


_matches_cache = None


def _build_matches():
    """Read matches.csv and return a list of match dicts with full analytics."""
    global _matches_cache
    if _matches_cache is not None:
        return _matches_cache

    out = []
    try:
        with open(_MATCHES_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                home = row.get("home_team", "").strip()
                away = row.get("away_team", "").strip()
                if not home or not away:
                    continue

                # Stage normalisation
                raw_stage = row.get("round", "").strip()
                stage = _STAGE_MAP.get(raw_stage, raw_stage)

                # Group deduction
                grp = _TEAM_TO_GROUP.get(home, _TEAM_TO_GROUP.get(away, "-"))

                # Score
                score_str = row.get("score", "").strip()
                status = "FT" if score_str else "TBD"
                s1 = _safe_int(row.get("home_score"))
                s2 = _safe_int(row.get("away_score"))

                # Possession
                home_poss = _safe_float(row.get("home_possession"))
                away_poss = _safe_float(row.get("away_possession"))

                # Full analytics stats dict
                stats = {
                    "home_possession": home_poss,
                    "away_possession": away_poss,
                    "home_sot": _safe_float(row.get("home_sot")),
                    "away_sot": _safe_float(row.get("away_sot")),
                    "home_total_shots": _safe_float(row.get("home_total_shots")),
                    "away_total_shots": _safe_float(row.get("away_total_shots")),
                    "home_saves": _safe_float(row.get("home_saves")),
                    "away_saves": _safe_float(row.get("away_saves")),
                    "home_cards_yellow": _safe_float(row.get("home_cards_yellow")),
                    "away_cards_yellow": _safe_float(row.get("away_cards_yellow")),
                    "home_cards_red": _safe_float(row.get("home_cards_red")),
                    "away_cards_red": _safe_float(row.get("away_cards_red")),
                    "home_fouls": _safe_float(row.get("home_fouls")),
                    "away_fouls": _safe_float(row.get("away_fouls")),
                    "home_corners": _safe_float(row.get("home_corners")),
                    "away_corners": _safe_float(row.get("away_corners")),
                    "home_crosses": _safe_float(row.get("home_crosses")),
                    "away_crosses": _safe_float(row.get("away_crosses")),
                    "home_interceptions": _safe_float(row.get("home_interceptions")),
                    "away_interceptions": _safe_float(row.get("away_interceptions")),
                    "home_offsides": _safe_float(row.get("home_offsides")),
                    "away_offsides": _safe_float(row.get("away_offsides")),
                }

                venue = row.get("venue", "").strip()
                date = row.get("date", "").strip()
                notes = row.get("notes", "").strip()

                out.append({
                    "id": i + 1,
                    "group": grp,
                    "stage": stage,
                    "date": date,
                    "team1": {
                        "name": home,
                        "flag": FLAGS.get(home, "🏳️"),
                        "flag_url": f"{_CDN}/{_COUNTRY_CODES.get(home, home[:2].lower())}.png",
                    },
                    "team2": {
                        "name": away,
                        "flag": FLAGS.get(away, "🏳️"),
                        "flag_url": f"{_CDN}/{_COUNTRY_CODES.get(away, away[:2].lower())}.png",
                    },
                    "score1": s1,
                    "score2": s2,
                    "status": status,
                    "venue": venue,
                    "attendance": row.get("attendance", "").strip(),
                    "notes": notes,
                    "stats": stats,
                })
    except Exception as e:
        print(f"[PlayStats] Error reading matches.csv: {e}")

    _matches_cache = out
    return out


# ══════════════════════════════════════════════════════════════════════════════
# STANDINGS
# ══════════════════════════════════════════════════════════════════════════════

def _build_standings():
    """Build group-stage standings from CSV match results."""
    table = {}
    matches = _build_matches()

    # Initialise all group-stage teams
    for g, teams in GROUPS.items():
        for t in teams:
            table[t] = {
                "team": t, "flag": FLAGS.get(t, "🏳️"), "group": g,
                "played": 0, "won": 0, "drawn": 0, "lost": 0,
                "gf": 0, "ga": 0, "gd": 0, "pts": 0,
            }

    for m in matches:
        if m["stage"] != "Group Stage" or m["status"] != "FT":
            continue
        t1, t2 = m["team1"]["name"], m["team2"]["name"]
        if t1 not in table or t2 not in table:
            continue
        s1, s2 = m["score1"], m["score2"]
        r1, r2 = table[t1], table[t2]
        r1["played"] += 1; r2["played"] += 1
        r1["gf"] += s1; r1["ga"] += s2
        r2["gf"] += s2; r2["ga"] += s1
        if s1 > s2:
            r1["won"] += 1; r1["pts"] += 3; r2["lost"] += 1
        elif s1 < s2:
            r2["won"] += 1; r2["pts"] += 3; r1["lost"] += 1
        else:
            r1["drawn"] += 1; r1["pts"] += 1
            r2["drawn"] += 1; r2["pts"] += 1

    for t in table.values():
        t["gd"] = t["gf"] - t["ga"]
    return table


# ══════════════════════════════════════════════════════════════════════════════
# PLAYER PARSING
# ══════════════════════════════════════════════════════════════════════════════

_players_cache = None


def _build_players():
    """Read players.csv and return a list of player dicts sorted by goals."""
    global _players_cache
    if _players_cache is not None:
        return _players_cache

    out = []
    try:
        with open(_PLAYERS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = (row.get("player") or "").strip()
                team = (row.get("team") or "").strip()
                if not name or not team:
                    continue

                # Position – take first token
                raw_pos = (row.get("position") or "").strip()
                pos = raw_pos.split(",")[0].strip() if raw_pos else "MF"
                if pos not in ("FW", "MF", "DF", "GK"):
                    pos = "MF"

                goals = _safe_int(row.get("goals"))
                assists = _safe_int(row.get("assists"))
                minutes = _safe_int(row.get("minutes"))
                shots = _safe_int(row.get("shots"))
                sot = _safe_int(row.get("shots_on_target"))

                # Rating heuristic (0–10 scale)
                rating = min(10.0, 6.0 + (goals * 0.8) + (assists * 0.5) + (minutes / 900.0))

                # Country code for flag CDN
                code = _COUNTRY_CODES.get(team, team[:2].lower())

                # Per-player detailed stats — all fields from CSV
                stats = {
                    # Attacking
                    "shots":           _safe_float(row.get("shots")),
                    "sot":             _safe_float(row.get("shots_on_target")),
                    "shots_pct":       _safe_float(row.get("shots_on_target_pct")),
                    "goals_per_shot":  _safe_float(row.get("goals_per_shot")),
                    "goals_per90":     _safe_float(row.get("goals_per90")),
                    "assists_per90":   _safe_float(row.get("assists_per90")),
                    "crosses":         _safe_float(row.get("crosses")),
                    "offsides":        _safe_float(row.get("offsides")),
                    # Defending / Discipline
                    "fouls":           _safe_float(row.get("fouls")),
                    "fouled":          _safe_float(row.get("fouled")),
                    "interceptions":   _safe_float(row.get("interceptions")),
                    "tackles_won":     _safe_float(row.get("tackles_won")),
                    "cards_yellow":    _safe_float(row.get("cards_yellow")),
                    "cards_red":       _safe_float(row.get("cards_red")),
                    # Impact
                    "plus_minus":      _safe_float(row.get("plus_minus")),
                    "plus_minus_per90":_safe_float(row.get("plus_minus_per90")),
                    "pens_won":        _safe_float(row.get("pens_won")),
                    # GK-specific
                    "gk_saves":        _safe_float(row.get("gk_saves")),
                    "gk_save_pct":     _safe_float(row.get("gk_save_pct")),
                    "gk_clean_sheets": _safe_float(row.get("gk_clean_sheets")),
                    "gk_goals_against":_safe_float(row.get("gk_goals_against")),
                }

                out.append({
                    "id": i + 1,
                    "name": name,
                    "team": team,
                    "flag": FLAGS.get(team, "🏳️"),
                    "code": code.upper(),
                    "flag_url": f"{_CDN}/{code}.png",
                    "pos": pos,
                    "goals": goals,
                    "assists": assists,
                    "shots": shots,
                    "sot": sot,
                    "minutes": minutes,
                    "rating": round(rating, 1),
                    "stats": stats,
                })
    except Exception as e:
        print(f"[PlayStats] Error reading players.csv: {e}")

    _players_cache = sorted(out, key=lambda p: (-p["goals"], -p["assists"], -p["minutes"]))
    return _players_cache


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

def get_all_matches():
    return _build_matches()


def get_matches_by_stage(stage):
    return [m for m in _build_matches() if m["stage"] == stage]


def get_group_standings():
    table = _build_standings()
    groups = {}
    for g, teams in GROUPS.items():
        rows = sorted(
            [table[t] for t in teams if t in table],
            key=lambda x: (-x["pts"], -x["gd"], -x["gf"]),
        )
        groups[g] = rows
    return groups


def get_all_players():
    return _build_players()


def get_player(pid):
    return next((p for p in _build_players() if p["id"] == pid), None)


def get_team_stats(team):
    """Compute team stats dynamically from CSV matches."""
    matches = _build_matches()
    team_matches = [m for m in matches if m["team1"]["name"] == team or m["team2"]["name"] == team]
    if not team_matches:
        return {}

    totals = {
        "shots": 0, "sot": 0, "poss": 0, "saves": 0,
        "fouls_won": 0, "fouls_conc": 0, "yc": 0, "rc": 0,
        "gf": 0, "ga": 0, "won": 0, "drawn": 0, "lost": 0,
        "corners": 0, "crosses": 0, "interceptions": 0, "offsides": 0,
    }
    count = 0
    for m in team_matches:
        if m["status"] != "FT":
            continue
        count += 1
        s = m["stats"]
        is_home = m["team1"]["name"] == team
        if is_home:
            totals["shots"] += s["home_total_shots"]
            totals["sot"] += s["home_sot"]
            totals["poss"] += s["home_possession"]
            totals["saves"] += s["home_saves"]
            totals["fouls_conc"] += s["home_fouls"]
            totals["fouls_won"] += s["away_fouls"]
            totals["yc"] += s["home_cards_yellow"]
            totals["rc"] += s["home_cards_red"]
            totals["corners"] += s["home_corners"]
            totals["crosses"] += s["home_crosses"]
            totals["interceptions"] += s["home_interceptions"]
            totals["offsides"] += s["home_offsides"]
            totals["gf"] += m["score1"]
            totals["ga"] += m["score2"]
            if m["score1"] > m["score2"]:   totals["won"] += 1
            elif m["score1"] < m["score2"]: totals["lost"] += 1
            else:                           totals["drawn"] += 1
        else:
            totals["shots"] += s["away_total_shots"]
            totals["sot"] += s["away_sot"]
            totals["poss"] += s["away_possession"]
            totals["saves"] += s["away_saves"]
            totals["fouls_conc"] += s["away_fouls"]
            totals["fouls_won"] += s["home_fouls"]
            totals["yc"] += s["away_cards_yellow"]
            totals["rc"] += s["away_cards_red"]
            totals["corners"] += s["away_corners"]
            totals["crosses"] += s["away_crosses"]
            totals["interceptions"] += s["away_interceptions"]
            totals["offsides"] += s["away_offsides"]
            totals["gf"] += m["score2"]
            totals["ga"] += m["score1"]
            if m["score2"] > m["score1"]:   totals["won"] += 1
            elif m["score2"] < m["score1"]: totals["lost"] += 1
            else:                           totals["drawn"] += 1

    # Average possession
    if count > 0:
        totals["poss"] = round(totals["poss"] / count)

    # Convert floats to ints for cleaner display
    for k in totals:
        if k != "poss":
            totals[k] = int(totals[k])

    return totals


def get_top_scorers(n=10):
    return _build_players()[:n]


def get_chart_data():
    standings = _build_standings()
    matches = _build_matches()
    goals_by_group = {}
    for g in GROUPS:
        total = sum(
            m["score1"] + m["score2"]
            for m in matches
            if m["group"] == g and m["status"] == "FT"
        )
        goals_by_group[g] = [total]
    return {
        "goals_by_group": goals_by_group,
        "top_teams_goals": {
            t: standings[t]["gf"]
            for t in list(standings)[:12]
            if t in standings
        },
        "top_teams_wins": {
            t: standings[t]["won"]
            for t in list(standings)[:12]
            if t in standings
        },
    }


def get_tournament_summary():
    return {
        "winner": TOURNAMENT_WINNER,
        "runner_up": TOURNAMENT_RUNNER_UP,
        "final_score": FINAL_SCORE,
        "golden_boot": GOLDEN_BOOT,
    }


def get_attack_chart_data():
    """Return attacking metrics for top teams — used by the animated bar chart."""
    # Key teams to feature in the attacking chart
    FEATURED = [
        "Spain", "Argentina", "France", "England", "Portugal",
        "Brazil", "Germany", "Netherlands", "Morocco", "Norway",
    ]
    result = []
    for team in FEATURED:
        ts = get_team_stats(team)
        if ts:
            code = _COUNTRY_CODES.get(team, team[:2].lower())
            result.append({
                "team":       team,
                "flag_url":   f"{_CDN}/{code}.png",
                "goals":      ts.get("gf", 0),
                "shots":      ts.get("shots", 0),
                "sot":        ts.get("sot", 0),
                "corners":    ts.get("corners", 0),
                "crosses":    ts.get("crosses", 0),
            })
    # Sort by goals desc
    result.sort(key=lambda x: -x["goals"])
    return result
