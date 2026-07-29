"""Flask routes for PlayStats FIFA 2026 web app."""
from flask import Blueprint, render_template, jsonify, abort
from web import fifa_data as fd

main_bp = Blueprint("main", __name__)

# ── Pages ─────────────────────────────────────────────────────────────────────

@main_bp.route("/")
def index():
    recent   = [m for m in fd.get_all_matches() if m["status"] == "FT"][-8:]
    scorers  = fd.get_top_scorers(8)
    summary  = fd.get_tournament_summary()
    return render_template("index.html", recent=recent, scorers=scorers, summary=summary)


@main_bp.route("/matches")
def matches():
    stages = ["Group Stage", "Round of 32", "Round of 16",
              "Quarterfinal", "Semifinal", "Third Place", "Final"]
    grouped = {s: fd.get_matches_by_stage(s) for s in stages}
    return render_template("matches.html", grouped=grouped)


@main_bp.route("/stats")
def stats():
    standings = fd.get_group_standings()
    return render_template("stats.html", standings=standings)


@main_bp.route("/stats/<team_name>")
def team_detail(team_name):
    ts = fd.get_team_stats(team_name)
    if not ts:
        abort(404)
    team_matches = [m for m in fd.get_all_matches()
                    if m["team1"]["name"] == team_name or m["team2"]["name"] == team_name]
    players = [p for p in fd.get_all_players() if p["team"] == team_name]
    return render_template("team_detail.html", team=team_name, ts=ts,
                           team_matches=team_matches, players=players)


@main_bp.route("/players")
def players():
    all_players = fd.get_all_players()
    return render_template("players.html", players=all_players)


@main_bp.route("/visualization")
def visualization():
    return render_template("visualization.html")


# ── JSON API ──────────────────────────────────────────────────────────────────

@main_bp.route("/api/matches")
def api_matches():
    return jsonify(fd.get_all_matches())


@main_bp.route("/api/standings")
def api_standings():
    return jsonify(fd.get_group_standings())


@main_bp.route("/api/players")
def api_players():
    return jsonify(fd.get_all_players())


@main_bp.route("/api/chart-data")
def api_chart_data():
    return jsonify(fd.get_chart_data())


@main_bp.route("/api/team/<team_name>")
def api_team(team_name):
    ts = fd.get_team_stats(team_name)
    if not ts:
        return jsonify({"error": "not found"}), 404
    return jsonify(ts)


@main_bp.route("/api/tournament")
def api_tournament():
    return jsonify(fd.get_tournament_summary())


# ── Error handlers ─────────────────────────────────────────────────────────────

@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, msg="Page not found"), 404
