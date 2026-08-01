# ⚽ PlayStats — FIFA World Cup 2026 Analytics Platform

> A full-stack Flask web application for exploring **complete FIFA World Cup 2026** match data, player statistics, group standings, and interactive visualizations — with a modern, OneFootball-inspired light-mode UI.

---

## 🏆 Tournament Result

| | |
|---|---|
| **Champion** | 🇪🇸 Spain |
| **Runner-Up** | 🇦🇷 Argentina |
| **Final Score** | 1 – 0 (After Extra Time) |
| **Winning Goal** | Ferran Torres · 106' |
| **Venue** | MetLife Stadium, East Rutherford, NJ |
| **Golden Boot** | 🇫🇷 Kylian Mbappé · 10 goals |
| **Golden Glove** | 🇪🇸 Unai Simón |
| **Total Matches** | 104 |
| **Teams** | 48 (12 Groups × 4) |

---

## 📸 Features Overview

### 🏠 Home Page
- **Champion banner** — highlights Spain's win, final score, and Mbappé's Golden Boot
- **Final match card** — full result with scorer and venue
- **Recent results** — last 8 completed matches with country flag images
- **Golden Boot race** — top 8 scorers with flag, position, goal count

### ⚽ Matches Page (`/matches`)
- **7-stage tabbed navigation** — Group Stage → Round of 32 → Round of 16 → Quarter-finals → Semi-finals → Third Place → **Final**
- **Country flag images** on every match card (via flagcdn.com, no emoji dependency)
- **Click any match** → animated stats modal appears with:
  - Possession split bar (home % vs away %)
  - **Attacking metrics** info card — Total Shots, Shots on Target, Corners, Crosses (bar rows + Chart.js grouped bar)
  - **Defence & Discipline** info card — Saves, Fouls, Interceptions, Offsides (bar rows + Chart.js grouped bar)
  - Mini metrics — Yellow Cards, Red Cards, Attendance, Match Notes
- Footer hidden automatically when modal is open

### 📊 Group Standings (`/stats`)
- All 12 groups (A–L) with full W/D/L/GD/Pts tables
- Top-2 qualification rows highlighted in green
- Clickable team names → team detail page

### 🏟️ Team Detail (`/stats/<team>`)
- Aggregated tournament stats: Shots, SOT, Possession, Corners, Fouls, Cards, Wins, Losses
- Doughnut chart (shot distribution)
- All team matches listed
- Player cards for squad members

### 👤 Players Page (`/players`)
- **1,248 players** loaded from `players.csv`
- Filter by position: All / Forwards / Midfielders / Defenders
- Player cards showing: flag image, name, country, rating bar, Goals/Assists/Shots, minutes played pill
- **Click any card** → player analytics modal:
  - **Position-aware Performance Radar** (spider chart) — axes change per position:
    - `FW` → Goals · Assists · Shots on Target · Fouls Won · Crosses · Impact +/−
    - `MF` → Goals · Assists · Crosses · Tackles Won · Fouls Won · Impact +/−
    - `DF` → Tackles Won · Interceptions · Fouls Won · Clearances · Goals
    - `GK` → Saves · Save % · Clean Sheets · Wins · Distribution
  - All values normalized 0–100 relative to the tournament-wide maximum
  - **Detailed Metrics bar chart** — raw values, individually color-coded bars

### 📈 Analytics Dashboard (`/visualization`)
- **Goals Per Group** — bar chart across all 12 groups
- **Top Teams by Wins** — line chart
- **Golden Boot — Top Scorers** — bar chart
- **🎯 Animated Team Attack Bar Chart** (Jitter-style):
  - Horizontal bars animate in with staggered 120ms delay per team
  - 4 metric buttons: Goals · Total Shots · Shots on Target · Corners
  - Country flag images painted on the Y-axis via custom Chart.js plugin
  - Value labels at the end of each bar
  - **Replay button** to re-trigger animation
- **Team Radar** — Spain vs Argentina comparison
- **Possession Doughnut** — Final match

---

## 🗂️ Project Structure

```
Task1/
├── app.py                          # Flask app factory + entry point
├── matches.csv                     # 104 matches with full per-match stats
├── players.csv                     # 1,248 players with 70+ stat columns
├── requirements.txt
│
├── web/
│   ├── __init__.py
│   ├── routes.py                   # All Flask page routes + JSON API
│   └── fifa_data.py                # Data layer — CSV parsing, standings, stats
│
├── playstats/
│   ├── analytics_engine.py         # Analytics utilities
│   ├── data_manager.py             # Data management helpers
│   ├── visualization_engine.py     # Visualization helpers
│   └── cli_controller.py           # CLI interface
│
├── templates/
│   ├── base.html                   # Shared layout (navbar, footer, CDN scripts)
│   ├── index.html                  # Home page
│   ├── matches.html                # Matches + stats modal
│   ├── stats.html                  # Group standings (12 groups)
│   ├── team_detail.html            # Per-team stats + players
│   ├── players.html                # Player grid + analytics modal
│   ├── visualization.html          # Charts dashboard
│   └── error.html                  # 404 page
│
└── static/
    ├── css/
    │   └── main.css                # Full design system (light theme, green/white)
    └── js/
        ├── main.js                 # Tilt init, mobile nav toggle
        └── charts.js               # Dashboard chart initialization
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/matches` | All 104 matches with full stats |
| `GET` | `/api/match/<id>` | Single match by ID (includes per-match stats) |
| `GET` | `/api/standings` | Group standings for all 12 groups |
| `GET` | `/api/players` | All 1,248 players sorted by goals |
| `GET` | `/api/chart-data` | Goals per group + wins per team |
| `GET` | `/api/attack-chart` | Top 10 teams' attacking metrics |
| `GET` | `/api/team/<name>` | Aggregated stats for one team |
| `GET` | `/api/tournament` | Winner, runner-up, Golden Boot |

---

## 🎨 Design System

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--green` | `#10b981` | Primary accent, bars, badges |
| `--green-dark` | `#059669` | Hover states, dark text |
| `--green-light` | `#d1fae5` | Backgrounds, highlights |
| `--bg` | `#f3f4f6` | Page background |
| `--card` | `#ffffff` | Card surfaces |
| `--text-main` | `#111827` | Primary text |
| `--muted` | `#6b7280` | Secondary text |

### Key Design Decisions
- **Light mode** — white cards on `#f3f4f6` background (OneFootball-inspired)
- **Flag images** from [flagcdn.com](https://flagcdn.com) — reliable CDN, no emoji dependency
- **3D tilt** — `vanilla-tilt.js` on all cards
- **Modal system** — `body:has(.modal-backdrop.open)` hides footer + locks scroll
- **Typography** — `Poppins` (Google Fonts), weights 300/400/600/700/800

### Frontend Libraries (CDN)
| Library | Purpose |
|---------|---------|
| Chart.js | All data visualizations |
| vanilla-tilt.js | 3D card hover effect |
| Font Awesome 6.5 | Icons throughout |
| Poppins (Google Fonts) | Typography |

---

## 📦 Data Sources

### `matches.csv` — 104 matches
Each row contains:
- `home_team`, `away_team`, `score`, `round`, `date`, `venue`, `attendance`
- `home_possession`, `away_possession`
- `home_sot`, `away_sot`, `home_total_shots`, `away_total_shots`
- `home_saves`, `away_saves`
- `home_corners`, `away_corners`, `home_crosses`, `away_crosses`
- `home_fouls`, `away_fouls`
- `home_interceptions`, `away_interceptions`, `home_offsides`, `away_offsides`
- `home_cards_yellow`, `away_cards_yellow`, `home_cards_red`, `away_cards_red`

### `players.csv` — 1,248 players, 70+ columns
Key stat groups:
- **Identity** — `player`, `team`, `position`, `age`, `club`
- **Playing time** — `games`, `games_starts`, `minutes`, `minutes_90s`
- **Goals** — `goals`, `assists`, `goals_per90`, `assists_per90`, `goals_per_shot`
- **Shooting** — `shots`, `shots_on_target`, `shots_on_target_pct`
- **Discipline** — `cards_yellow`, `cards_red`, `fouls`, `fouled`
- **Defending** — `interceptions`, `tackles_won`, `crosses`
- **Impact** — `plus_minus`, `plus_minus_per90`
- **Goalkeeper** — `gk_saves`, `gk_save_pct`, `gk_clean_sheets`, `gk_goals_against`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# 1. Clone / navigate to project
cd "g:\Stu_Projects\Task1"

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. Install Flask (core dependency)
pip install flask

# 4. Run the app
python app.py
```

The app will be available at **http://127.0.0.1:5000**

### Environment Variables (optional)
Copy `.env.example` → `.env` and set:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

---

## 🗺️ Page Routes

| URL | Page |
|-----|------|
| `/` | Home — champion banner, recent results, top scorers |
| `/matches` | All 104 matches across 7 stages |
| `/stats` | Group standings (12 groups, 48 teams) |
| `/stats/<team>` | Team detail — stats, matches, players |
| `/players` | Player grid with analytics modal |
| `/visualization` | Charts dashboard + animated bar chart |

---

## 🔧 Architecture Notes

- **Data is cached in memory** — `_matches_cache` and `_players_cache` in `fifa_data.py` are populated once on first request and reused for the lifetime of the process.
- **Standings are computed dynamically** — derived by replaying all group-stage match results from `matches.csv` rather than stored separately.
- **Team stats are computed on-demand** — `get_team_stats(team)` aggregates all matches for a team on each call.
- **Radar normalization** — all spider-chart values are normalized 0–100 against the tournament-wide maximum for each metric (e.g., goals max = 10 [Mbappé], crosses max = 54 [Messi]).
- **Flag CDN** — `https://flagcdn.com/48x36/<iso>.png` is used for all country flag images. Special cases: England → `gb-eng`, Scotland → `gb-sct`.

---

## 📋 Tournament Data Summary

| Stage | Matches |
|-------|---------|
| Group Stage | 72 (12 groups × 6) |
| Round of 32 | 16 |
| Round of 16 | 8 |
| Quarter-finals | 4 |
| Semi-finals | 2 |
| Third Place | 1 |
| **Final** | **1** |
| **Total** | **104** |

---

## 👨‍💻 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 · Flask |
| Templating | Jinja2 |
| Data | CSV (matches.csv, players.csv) |
| Frontend | Vanilla HTML5 · CSS3 · JavaScript (ES6+) |
| Charts | Chart.js |
| Animations | vanilla-tilt.js |
| Icons | Font Awesome 6.5 |
| Fonts | Google Fonts — Poppins |
| Flag Images | flagcdn.com CDN |

---

*PlayStats · FIFA World Cup 2026 · 🏆 Spain Champions · Built with Flask & Chart.js*
