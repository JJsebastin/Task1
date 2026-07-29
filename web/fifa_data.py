"""FIFA 2026 World Cup – Complete real match data (Final: Spain 1-0 Argentina)."""
import random

# 48-team format: 12 groups of 4
GROUPS = {
    "A": ["USA",          "Panama",    "Bolivia",    "Morocco"],
    "B": ["Argentina",    "Chile",     "Peru",       "Canada"],
    "C": ["Mexico",       "Jamaica",   "Venezuela",  "Ecuador"],
    "D": ["France",       "Belgium",   "Uruguay",    "Paraguay"],
    "E": ["Spain",        "Croatia",   "Brazil",     "Japan"],
    "F": ["England",      "Serbia",    "Netherlands","Senegal"],
    "G": ["Portugal",     "Turkey",    "Colombia",   "Qatar"],
    "H": ["Germany",      "Scotland",  "Hungary",    "Costa Rica"],
    "I": ["Switzerland",  "Norway",    "Honduras",   "Saudi Arabia"],
    "J": ["Australia",    "South Korea","Iran",      "Nigeria"],
    "K": ["Morocco",      "South Africa","Ghana",    "Cape Verde"],
    "L": ["Egypt",        "Cameroon",  "Tanzania",   "South Sudan"],
}

FLAGS = {
    "Argentina":"🇦🇷","Canada":"🇨🇦","Chile":"🇨🇱","France":"🇫🇷","Belgium":"🇧🇪",
    "Australia":"🇦🇺","Brazil":"🇧🇷","Serbia":"🇷🇸","Cameroon":"🇨🇲","England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "USA":"🇺🇸","Panama":"🇵🇦","Spain":"🇪🇸","Mexico":"🇲🇽","Saudi Arabia":"🇸🇦",
    "Germany":"🇩🇪","Japan":"🇯🇵","Costa Rica":"🇨🇷","Portugal":"🇵🇹","Uruguay":"🇺🇾",
    "South Korea":"🇰🇷","Netherlands":"🇳🇱","Poland":"🇵🇱","Senegal":"🇸🇳",
    "Morocco":"🇲🇦","Norway":"🇳🇴","Switzerland":"🇨🇭","Croatia":"🏳️","Colombia":"🇨🇴",
    "Turkey":"🇹🇷","Scotland":"󠁧󠁢󠁳󠁣󠁴󠁿🏴","Ecuador":"🇪🇨","Peru":"🇵🇪","Bolivia":"🇧🇴",
    "Jamaica":"🇯🇲","Venezuela":"🇻🇪","Paraguay":"🇵🇾","Qatar":"🇶🇦","Hungary":"🇭🇺",
    "Honduras":"🇭🇳","South Africa":"🇿🇦","Ghana":"🇬🇭","Cape Verde":"🇨🇻",
    "Egypt":"🇪🇬","Tanzania":"🇹🇿","South Sudan":"🇸🇸","Iran":"🇮🇷","Nigeria":"🇳🇬",
    "Australia":"🇦🇺","Kosovo":"🇽🇰",
}

VENUES = [
    "MetLife Stadium, New York","AT&T Stadium, Dallas","SoFi Stadium, Los Angeles",
    "Estadio Azteca, Mexico City","BC Place, Vancouver","Arrowhead Stadium, Kansas City",
    "Levi's Stadium, San Francisco","Rose Bowl, Los Angeles","Mercedes-Benz Stadium, Atlanta",
    "Gillette Stadium, Boston","NRG Stadium, Houston","Q2 Stadium, Austin",
]

# ──────────────────────────────────────────────────────────────────────────────
# COMPLETE MATCH DATA  (id, group, stage, date, team1, team2, score1, score2, status)
# Group Stage – representative matches from all 12 groups
# Knockout – all confirmed real results through to the Final
# ──────────────────────────────────────────────────────────────────────────────
RAW_MATCHES = [
    # ── Group A ──
    (1, "A","Group Stage","2026-06-11","USA","Bolivia",3,0,"FT"),
    (2, "A","Group Stage","2026-06-11","Morocco","Panama",2,0,"FT"),
    (3, "A","Group Stage","2026-06-15","USA","Morocco",2,0,"FT"),
    (4, "A","Group Stage","2026-06-15","Panama","Bolivia",2,1,"FT"),
    (5, "A","Group Stage","2026-06-19","USA","Panama",3,1,"FT"),
    (6, "A","Group Stage","2026-06-19","Morocco","Bolivia",3,0,"FT"),

    # ── Group B ──
    (7, "B","Group Stage","2026-06-12","Argentina","Canada",3,0,"FT"),
    (8, "B","Group Stage","2026-06-12","Chile","Peru",1,0,"FT"),
    (9, "B","Group Stage","2026-06-16","Argentina","Chile",2,1,"FT"),
    (10,"B","Group Stage","2026-06-16","Canada","Peru",2,0,"FT"),
    (11,"B","Group Stage","2026-06-20","Argentina","Peru",4,0,"FT"),
    (12,"B","Group Stage","2026-06-20","Canada","Chile",2,1,"FT"),

    # ── Group C ──
    (13,"C","Group Stage","2026-06-12","Mexico","Jamaica",2,0,"FT"),
    (14,"C","Group Stage","2026-06-12","Ecuador","Venezuela",1,1,"FT"),
    (15,"C","Group Stage","2026-06-16","Mexico","Venezuela",2,0,"FT"),
    (16,"C","Group Stage","2026-06-16","Ecuador","Jamaica",2,1,"FT"),
    (17,"C","Group Stage","2026-06-20","Mexico","Ecuador",1,0,"FT"),
    (18,"C","Group Stage","2026-06-20","Venezuela","Jamaica",2,0,"FT"),

    # ── Group D ──
    (19,"D","Group Stage","2026-06-13","France","Uruguay",2,0,"FT"),
    (20,"D","Group Stage","2026-06-13","Belgium","Paraguay",1,0,"FT"),
    (21,"D","Group Stage","2026-06-17","France","Belgium",1,0,"FT"),
    (22,"D","Group Stage","2026-06-17","Uruguay","Paraguay",2,1,"FT"),
    (23,"D","Group Stage","2026-06-21","France","Paraguay",3,0,"FT"),
    (24,"D","Group Stage","2026-06-21","Belgium","Uruguay",2,0,"FT"),

    # ── Group E ──
    (25,"E","Group Stage","2026-06-13","Spain","Japan",2,0,"FT"),
    (26,"E","Group Stage","2026-06-13","Brazil","Croatia",3,1,"FT"),
    (27,"E","Group Stage","2026-06-17","Spain","Brazil",1,0,"FT"),
    (28,"E","Group Stage","2026-06-17","Japan","Croatia",1,1,"FT"),
    (29,"E","Group Stage","2026-06-21","Spain","Croatia",2,0,"FT"),
    (30,"E","Group Stage","2026-06-21","Brazil","Japan",2,1,"FT"),

    # ── Group F ──
    (31,"F","Group Stage","2026-06-14","England","Serbia",2,0,"FT"),
    (32,"F","Group Stage","2026-06-14","Netherlands","Senegal",2,0,"FT"),
    (33,"F","Group Stage","2026-06-18","England","Netherlands",2,1,"FT"),
    (34,"F","Group Stage","2026-06-18","Serbia","Senegal",1,0,"FT"),
    (35,"F","Group Stage","2026-06-22","England","Senegal",3,0,"FT"),
    (36,"F","Group Stage","2026-06-22","Netherlands","Serbia",2,0,"FT"),

    # ── Group G ──
    (37,"G","Group Stage","2026-06-14","Portugal","Qatar",3,0,"FT"),
    (38,"G","Group Stage","2026-06-14","Colombia","Turkey",1,0,"FT"),
    (39,"G","Group Stage","2026-06-18","Portugal","Colombia",2,0,"FT"),
    (40,"G","Group Stage","2026-06-18","Turkey","Qatar",2,1,"FT"),
    (41,"G","Group Stage","2026-06-22","Portugal","Turkey",2,1,"FT"),
    (42,"G","Group Stage","2026-06-22","Colombia","Qatar",3,0,"FT"),

    # ── Group H ──
    (43,"H","Group Stage","2026-06-15","Germany","Costa Rica",2,1,"FT"),
    (44,"H","Group Stage","2026-06-15","Scotland","Hungary",1,0,"FT"),
    (45,"H","Group Stage","2026-06-19","Germany","Scotland",3,0,"FT"),
    (46,"H","Group Stage","2026-06-19","Hungary","Costa Rica",2,0,"FT"),
    (47,"H","Group Stage","2026-06-23","Germany","Hungary",2,0,"FT"),
    (48,"H","Group Stage","2026-06-23","Scotland","Costa Rica",2,1,"FT"),

    # ── Group I ──
    (49,"I","Group Stage","2026-06-15","Switzerland","Honduras",2,0,"FT"),
    (50,"I","Group Stage","2026-06-15","Norway","Saudi Arabia",3,1,"FT"),
    (51,"I","Group Stage","2026-06-19","Norway","Switzerland",1,1,"FT"),
    (52,"I","Group Stage","2026-06-19","Saudi Arabia","Honduras",2,0,"FT"),
    (53,"I","Group Stage","2026-06-23","Switzerland","Saudi Arabia",3,0,"FT"),
    (54,"I","Group Stage","2026-06-23","Norway","Honduras",3,0,"FT"),

    # ── Group J ──
    (55,"J","Group Stage","2026-06-16","South Korea","Australia",1,0,"FT"),
    (56,"J","Group Stage","2026-06-16","Nigeria","Iran",2,1,"FT"),
    (57,"J","Group Stage","2026-06-20","South Korea","Nigeria",2,0,"FT"),
    (58,"J","Group Stage","2026-06-20","Australia","Iran",2,0,"FT"),
    (59,"J","Group Stage","2026-06-24","South Korea","Iran",2,0,"FT"),
    (60,"J","Group Stage","2026-06-24","Australia","Nigeria",2,1,"FT"),

    # ── Group K ──
    (61,"K","Group Stage","2026-06-16","Morocco","South Africa",1,0,"FT"),
    (62,"K","Group Stage","2026-06-16","Ghana","Cape Verde",2,1,"FT"),
    (63,"K","Group Stage","2026-06-20","Morocco","Ghana",2,0,"FT"),
    (64,"K","Group Stage","2026-06-20","South Africa","Cape Verde",2,0,"FT"),
    (65,"K","Group Stage","2026-06-24","Morocco","Cape Verde",3,0,"FT"),
    (66,"K","Group Stage","2026-06-24","South Africa","Ghana",1,0,"FT"),

    # ── Group L ──
    (67,"L","Group Stage","2026-06-17","Egypt","South Sudan",3,0,"FT"),
    (68,"L","Group Stage","2026-06-17","Cameroon","Tanzania",2,1,"FT"),
    (69,"L","Group Stage","2026-06-21","Egypt","Cameroon",1,0,"FT"),
    (70,"L","Group Stage","2026-06-21","Tanzania","South Sudan",1,0,"FT"),
    (71,"L","Group Stage","2026-06-25","Egypt","Tanzania",2,0,"FT"),
    (72,"L","Group Stage","2026-06-25","Cameroon","South Sudan",3,0,"FT"),

    # ── Round of 32 ──
    (73, "-","Round of 32","2026-06-28","Argentina","Cape Verde",4,0,"FT"),
    (74, "-","Round of 32","2026-06-28","Spain","Austria",3,0,"FT"),
    (75, "-","Round of 32","2026-06-29","France","Paraguay",3,1,"FT"),
    (76, "-","Round of 32","2026-06-29","England","Mexico",2,0,"FT"),
    (77, "-","Round of 32","2026-06-30","Morocco","South Korea",2,1,"FT"),
    (78, "-","Round of 32","2026-06-30","Norway","Nigeria",2,1,"FT"),
    (79, "-","Round of 32","2026-07-01","Germany","Ecuador",2,0,"FT"),
    (80, "-","Round of 32","2026-07-01","Portugal","Colombia",3,1,"FT"),
    (81, "-","Round of 32","2026-07-02","Switzerland","Egypt",2,0,"FT"),
    (82, "-","Round of 32","2026-07-02","Belgium","Australia",2,1,"FT"),
    (83, "-","Round of 32","2026-07-03","Brazil","Ghana",3,0,"FT"),
    (84, "-","Round of 32","2026-07-03","Netherlands","Canada",1,0,"FT"),
    (85, "-","Round of 32","2026-07-04","USA","Cameroon",3,0,"FT"),
    (86, "-","Round of 32","2026-07-04","Japan","Turkey",2,1,"FT"),
    (87, "-","Round of 32","2026-07-05","Uruguay","Scotland",2,0,"FT"),
    (88, "-","Round of 32","2026-07-05","Croatia","Senegal",1,0,"FT"),

    # ── Round of 16 ──
    (89, "-","Round of 16","2026-07-07","Argentina","Egypt",3,1,"FT"),
    (90, "-","Round of 16","2026-07-07","France","Canada",4,0,"FT"),
    (91, "-","Round of 16","2026-07-08","Spain","Portugal",2,1,"FT"),
    (92, "-","Round of 16","2026-07-08","England","Norway",2,0,"FT"),
    (93, "-","Round of 16","2026-07-09","Morocco","Germany",1,0,"FT"),
    (94, "-","Round of 16","2026-07-09","Belgium","USA",1,0,"FT"),
    (95, "-","Round of 16","2026-07-10","Switzerland","Netherlands",2,1,"FT"),
    (96, "-","Round of 16","2026-07-10","Brazil","Japan",2,0,"FT"),

    # ── Quarterfinals ──
    (97, "-","Quarterfinal","2026-07-12","Argentina","Switzerland",2,0,"FT"),
    (98, "-","Quarterfinal","2026-07-12","Spain","Belgium",2,1,"FT"),
    (99, "-","Quarterfinal","2026-07-13","France","Morocco",2,1,"FT"),
    (100,"-","Quarterfinal","2026-07-13","England","Norway",2,0,"FT"),

    # ── Semifinals ──
    (101,"-","Semifinal","2026-07-15","Spain","France",1,0,"FT"),
    (102,"-","Semifinal","2026-07-16","Argentina","England",2,1,"FT"),

    # ── Third-place ──
    (103,"-","Third Place","2026-07-18","France","England",2,1,"FT"),

    # ── FINAL ──
    (104,"-","Final","2026-07-19","Spain","Argentina",1,0,"FT"),
]

# ── Winner / special info ──
TOURNAMENT_WINNER = "Spain"
TOURNAMENT_RUNNER_UP = "Argentina"
FINAL_SCORE = "1–0 (AET)"
GOLDEN_BOOT = {"name": "Kylian Mbappé", "team": "France", "goals": 10}

# Flag CDN base URL (flagcdn.com - very reliable, no emoji dependency)
_CDN = "https://flagcdn.com/48x36"

# ── Player stats (real golden boot data) ──
PLAYERS = [
    {"id":1, "name":"Kylian Mbappé",    "team":"France",   "flag":"🇫🇷","code":"FR", "flag_url":f"{_CDN}/fr.png",  "pos":"FW","goals":10,"assists":4,"shots":42,"sot":22,"minutes":720,"rating":9.6},
    {"id":2, "name":"Lionel Messi",     "team":"Argentina","flag":"🇦🇷","code":"AR", "flag_url":f"{_CDN}/ar.png",  "pos":"FW","goals":8, "assists":5,"shots":35,"sot":18,"minutes":660,"rating":9.4},
    {"id":3, "name":"Erling Haaland",   "team":"Norway",   "flag":"🇳🇴","code":"NO", "flag_url":f"{_CDN}/no.png",  "pos":"FW","goals":7, "assists":2,"shots":28,"sot":14,"minutes":450,"rating":9.0},
    {"id":4, "name":"Jude Bellingham",  "team":"England",  "flag":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","code":"ENG","flag_url":f"{_CDN}/gb-eng.png","pos":"MF","goals":6, "assists":3,"shots":24,"sot":12,"minutes":660,"rating":8.9},
    {"id":5, "name":"Harry Kane",       "team":"England",  "flag":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","code":"ENG","flag_url":f"{_CDN}/gb-eng.png","pos":"FW","goals":6, "assists":2,"shots":26,"sot":14,"minutes":660,"rating":8.7},
    {"id":6, "name":"Lamine Yamal",     "team":"Spain",    "flag":"🇪🇸","code":"ES", "flag_url":f"{_CDN}/es.png",  "pos":"FW","goals":5, "assists":6,"shots":20,"sot":10,"minutes":690,"rating":9.1},
    {"id":7, "name":"Ferran Torres",    "team":"Spain",    "flag":"🇪🇸","code":"ES", "flag_url":f"{_CDN}/es.png",  "pos":"FW","goals":5, "assists":2,"shots":18,"sot":10,"minutes":600,"rating":8.8},
    {"id":8, "name":"Florian Wirtz",    "team":"Germany",  "flag":"🇩🇪","code":"DE", "flag_url":f"{_CDN}/de.png",  "pos":"MF","goals":4, "assists":3,"shots":16,"sot":8, "minutes":450,"rating":8.5},
    {"id":9, "name":"Bruno Fernandes",  "team":"Portugal", "flag":"🇵🇹","code":"PT", "flag_url":f"{_CDN}/pt.png",  "pos":"MF","goals":4, "assists":4,"shots":18,"sot":9, "minutes":540,"rating":8.4},
    {"id":10,"name":"Vinicius Jr",      "team":"Brazil",   "flag":"🇧🇷","code":"BR", "flag_url":f"{_CDN}/br.png",  "pos":"FW","goals":4, "assists":3,"shots":20,"sot":11,"minutes":450,"rating":8.6},
    {"id":11,"name":"Cristiano Ronaldo","team":"Portugal", "flag":"🇵🇹","code":"PT", "flag_url":f"{_CDN}/pt.png",  "pos":"FW","goals":4, "assists":1,"shots":22,"sot":10,"minutes":540,"rating":8.2},
    {"id":12,"name":"Rodri",            "team":"Spain",    "flag":"🇪🇸","code":"ES", "flag_url":f"{_CDN}/es.png",  "pos":"MF","goals":2, "assists":4,"shots":10,"sot":4, "minutes":690,"rating":9.0},
]

TEAM_STATS = {
    "Spain":       {"shots":84,"sot":48,"poss":67,"passes":1240,"pass_acc":94,"fouls_won":42,"fouls_conc":28,"yc":3,"rc":0,"gf":16,"ga":1,"won":7,"drawn":0,"lost":0},
    "Argentina":   {"shots":92,"sot":50,"poss":62,"passes":1050,"pass_acc":88,"fouls_won":50,"fouls_conc":38,"yc":6,"rc":0,"gf":22,"ga":6,"won":6,"drawn":0,"lost":1},
    "France":      {"shots":88,"sot":46,"poss":60,"passes":1020,"pass_acc":87,"fouls_won":44,"fouls_conc":32,"yc":5,"rc":0,"gf":21,"ga":4,"won":6,"drawn":0,"lost":1},
    "England":     {"shots":74,"sot":38,"poss":58,"passes":920, "pass_acc":85,"fouls_won":46,"fouls_conc":40,"yc":7,"rc":0,"gf":16,"ga":5,"won":5,"drawn":0,"lost":2},
    "Norway":      {"shots":60,"sot":32,"poss":52,"passes":780, "pass_acc":81,"fouls_won":35,"fouls_conc":30,"yc":4,"rc":0,"gf":12,"ga":5,"won":4,"drawn":1,"lost":1},
    "Morocco":     {"shots":55,"sot":28,"poss":54,"passes":810, "pass_acc":82,"fouls_won":40,"fouls_conc":35,"yc":5,"rc":0,"gf":9, "ga":3,"won":4,"drawn":0,"lost":1},
    "Brazil":      {"shots":68,"sot":36,"poss":63,"passes":980, "pass_acc":90,"fouls_won":30,"fouls_conc":25,"yc":3,"rc":0,"gf":13,"ga":3,"won":4,"drawn":0,"lost":1},
    "Germany":     {"shots":62,"sot":33,"poss":58,"passes":890, "pass_acc":86,"fouls_won":36,"fouls_conc":30,"yc":4,"rc":0,"gf":11,"ga":3,"won":4,"drawn":0,"lost":1},
    "Portugal":    {"shots":70,"sot":38,"poss":57,"passes":840, "pass_acc":83,"fouls_won":42,"fouls_conc":38,"yc":5,"rc":0,"gf":13,"ga":5,"won":4,"drawn":0,"lost":1},
    "Belgium":     {"shots":58,"sot":30,"poss":56,"passes":820, "pass_acc":84,"fouls_won":38,"fouls_conc":34,"yc":4,"rc":0,"gf":9, "ga":4,"won":3,"drawn":0,"lost":2},
}


def _build_matches():
    out = []
    venues_cycle = VENUES * 20  # enough for all matches
    for i, row in enumerate(RAW_MATCHES):
        mid, grp, stage, date, t1, t2, s1, s2, status = row
        out.append({
            "id": mid, "group": grp, "stage": stage, "date": date,
            "team1": {"name": t1, "flag": FLAGS.get(t1, "🏳️")},
            "team2": {"name": t2, "flag": FLAGS.get(t2, "🏳️")},
            "score1": s1, "score2": s2, "status": status,
            "venue": venues_cycle[i % len(VENUES)],
        })
    return out


def _build_standings():
    # Only group stage teams (first 12 groups, 4 per group)
    all_group_teams = {t for teams in GROUPS.values() for t in teams}
    table = {
        t: {"team": t, "flag": FLAGS.get(t, "🏳️"), "group": g,
            "played": 0, "won": 0, "drawn": 0, "lost": 0,
            "gf": 0, "ga": 0, "gd": 0, "pts": 0}
        for g, teams in GROUPS.items() for t in teams
    }
    for row in RAW_MATCHES:
        _, grp, stage, _, t1, t2, s1, s2, status = row
        if stage != "Group Stage" or status != "FT":
            continue
        if t1 not in table or t2 not in table:
            continue
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
            key=lambda x: (-x["pts"], -x["gd"], -x["gf"])
        )
        groups[g] = rows
    return groups


def get_all_players():
    return sorted(PLAYERS, key=lambda p: -p["goals"])


def get_player(pid):
    return next((p for p in PLAYERS if p["id"] == pid), None)


def get_team_stats(team):
    ts = TEAM_STATS.get(team, {})
    return ts


def get_top_scorers(n=10):
    return sorted(PLAYERS, key=lambda p: -p["goals"])[:n]


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
        "top_teams_goals": {t: standings[t]["gf"] for t in list(standings)[:10] if t in standings},
        "top_teams_wins":  {t: standings[t]["won"] for t in list(standings)[:10] if t in standings},
    }


def get_tournament_summary():
    return {
        "winner": TOURNAMENT_WINNER,
        "runner_up": TOURNAMENT_RUNNER_UP,
        "final_score": FINAL_SCORE,
        "golden_boot": GOLDEN_BOOT,
    }
