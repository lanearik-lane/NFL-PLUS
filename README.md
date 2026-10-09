# 🏈 NFL Plus Predictor

AI-powered NFL moneyline, spread & total points predictor — auto-follows the 2026–27 season.

---

## 📁 Files in This Download

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app (all logic inside) |
| `requirements.txt` | Python packages to install |
| `run_windows.bat` | Double-click launcher for Windows |
| `run_mac_linux.sh` | One-click launcher for Mac / Linux |
| `README.md` | This file |

---

## 🚀 Quick Start

### Windows
1. Install Python 3.10+ from https://python.org (check "Add to PATH")
2. Double-click `run_windows.bat`
3. Browser opens at http://localhost:8501

### Mac / Linux
```bash
chmod +x run_mac_linux.sh
./run_mac_linux.sh
```

### Manual (any OS)
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Features

- Auto-detects current NFL week from today's date (pre/regular/playoffs)
- Live schedule pulled from ESPN API each launch
- Moneyline, spread, O/U picks + A-D grades for every game
- Live injury reports via ESPN Core API
- Matchup analyzer for any two teams
- All 32 team power rankings

## How Grades Work

| Grade | Meaning |
|-------|---------|
| A+/A | Strong edge, high confidence |
| B+/B | Moderate edge |
| C | Lean, close matchup |
| D | Coin flip — avoid |

## Data Sources

- ESPN scoreboard API (free, no key)
- ESPN injuries API (free, no key)
- 2025 final stats + 2026 preseason rankings

## Disclaimer
For entertainment only. Not financial advice.
