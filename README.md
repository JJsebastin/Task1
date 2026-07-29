# 🏆 PlayStats – Sports Score Visualizer

A command-line Python tool for entering, analysing, and visualizing sports match results.

---

## Features

| Feature | Description |
|---|---|
| **Match Entry** | Add, edit, and delete match results with validation |
| **Data Persistence** | Auto-saves to CSV; import/export any CSV file |
| **Analytics** | Wins, losses, draws, average scores per team |
| **Visualizations** | Line chart (score trend) and bar chart (W/L/D) |

---

## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 2. Install dependencies

```bash
pip install pandas matplotlib
```

---

## Running the App

```bash
python Sports_visualizer.py
```

---

## Main Menu

```
══════════════════════════════════════════════════════
  🏆  PlayStats – Sports Score Visualizer
══════════════════════════════════════════════════════
  [1] Enter Match Result
  [2] View / Edit Data
  [3] Generate Charts
  [4] View Analytics
  [5] Import / Export Data
  [6] Exit
──────────────────────────────────────────────────────
```

---

## CSV Format

The CSV must have exactly these columns:

```
date,team_1,team_2,score_1,score_2
2025-01-10,Arsenal,Chelsea,2,1
2025-01-17,Liverpool,ManCity,3,3
```

---

## Project Structure

```
Task1/
├── playstats/
│   ├── __init__.py
│   ├── data_manager.py          ← CRUD + CSV I/O
│   ├── analytics_engine.py      ← Statistics
│   ├── visualization_engine.py  ← Charts (matplotlib)
│   └── cli_controller.py        ← Menu + routing
├── data/
│   └── matches.csv              ← Auto-saved data
├── exports/                     ← Manual exports go here
├── Sports_visualizer.py         ← Entry point
├── requirements.txt
└── README.md
```

---

## Dependencies

- Python 3.x
- `pandas`
- `matplotlib`
