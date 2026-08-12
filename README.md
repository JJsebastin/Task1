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

## 📸 Analytic Features

The platform provides an array of interactive analytical features to explore tournament data deeply:

### 1. Advanced Analytics Dashboard (`/visualization`)
- **Animated Team Attack Chart**: Jitter-inspired horizontal bar chart animating attacking metrics (Goals, Shots, SOT, Corners) across top teams.
- **Team Comparison Radar**: A spider chart comparing Spain and Argentina across key metrics (Goals, Possession, Shots on Target, Crosses, Clean Sheets).
- **Golden Boot Race**: Bar chart representing the tournament's top scorers.
- **Tournament Progression**: Line charts mapping out the top teams by wins and total goals per group.
- **Match Insights**: Doughnut charts for possession splits in key matches.

### 2. Player Performance Analytics (`/players`)
- **Position-Aware Radar Charts**: Interactive spider charts tailored to a player's position:
  - **Forwards (FW)**: Evaluated on Goals, Assists, Shots on Target, Fouls Won, Crosses, and Impact.
  - **Midfielders (MF)**: Evaluated on Goals, Assists, Crosses, Tackles Won, Fouls Won, and Impact.
  - **Defenders (DF)**: Evaluated on Tackles Won, Interceptions, Fouls Won, Clearances, and Goals.
  - **Goalkeepers (GK)**: Evaluated on Saves, Save %, Clean Sheets, Wins, and Distribution.
- **Normalized Data**: Values are normalized (0-100) against the tournament's top performers for fair visual comparison.
- **Metric Breakdown**: Deep dive into individual player stats (minutes played, cards, passing accuracy, defensive actions) in detailed bar charts.

### 3. Team & Match Insights (`/stats` & `/matches`)
- **Dynamic Group Standings**: Computes and renders real-time points, goal differences, and W/D/L for all 12 groups.
- **Match-level Deep Dives**: Clicking any match reveals side-by-side analytical bars for attacking metrics (Shots, Corners) and defensive actions (Saves, Interceptions).
- **Team Aggregation**: Computes overall performance for any team (e.g., total possession, total shots vs. shots on target) across the entire tournament.

---

## 📊 Parameters Used (Data Structure)

The platform evaluates teams and players using highly detailed parameters spanning multiple facets of the game.

### Team & Match Parameters
- **Basic Match Info**: `score`, `round`, `date`, `venue`, `attendance`
- **Control & Attacking**: `home_possession`, `away_possession`, `total_shots`, `shots_on_target`, `corners`, `crosses`
- **Defending & Discipline**: `saves`, `fouls`, `interceptions`, `offsides`, `cards_yellow`, `cards_red`

### Player Parameters
Over 1,200 players are evaluated across 70+ columns. Key parameters include:
- **Identity & Playtime**: `position`, `age`, `games_starts`, `minutes`, `minutes_per_90`
- **Offensive Output**: `goals`, `assists`, `goals_per90`, `shots`, `shots_on_target_pct`
- **Defensive Actions**: `tackles_won`, `interceptions`, `clearances`, `blocks`
- **Discipline & Impact**: `fouls`, `fouled`, `cards_yellow`, `plus_minus_per90`
- **Goalkeeping**: `gk_saves`, `gk_save_pct`, `gk_clean_sheets`, `gk_goals_against`

---

## 🚀 How to Run Locally (From GitHub)

Follow these detailed steps to download the repository from GitHub, deploy it, and view it on your local machine.

### Prerequisites
- You need **Git** installed on your machine (to download the repository).
- You need **Python 3.9+** installed. (Download from [python.org](https://www.python.org/downloads/))

### Step-by-Step Deployment Instructions

#### 1. Download (Clone) the Repository
Open your terminal (Command Prompt, PowerShell, or macOS/Linux Terminal) and run:
```bash
git clone https://github.com/your-username/your-repo-name.git
```
*(Replace the URL with the actual link to your GitHub repository.)*

Navigate into the newly downloaded project folder:
```bash
cd your-repo-name
```

#### 2. Set Up a Virtual Environment (Recommended)
A virtual environment keeps the project dependencies separate from your system Python.
```bash
# Create the virtual environment named "venv"
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
Once the virtual environment is activated, install the required packages (like Flask):
```bash
pip install -r requirements.txt
```
*(If `requirements.txt` is missing, you can install flask directly: `pip install flask`)*

#### 4. Run the Application
Start the Flask web server:
```bash
python app.py
```

#### 5. View in Your Browser
The terminal will display a message like `* Running on http://127.0.0.1:5000`. 
Open your web browser (Chrome, Firefox, Safari, Edge) and navigate to:

👉 **http://127.0.0.1:5000**

You can now freely explore all the analytics, matches, and visualizations! 
*(To stop the server, go back to your terminal and press `CTRL + C`.)*

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
