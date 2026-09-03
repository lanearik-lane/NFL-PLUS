import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NFL Plus",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0d0d0d;color:#f0f0f0}
.stApp{background:#0d0d0d}
footer,#MainMenu,header{display:none!important;visibility:hidden!important}
.nfl-header{display:flex;align-items:center;justify-content:space-between;
  padding:14px 24px;background:#111;border-bottom:2px solid #1e1e1e;margin-bottom:18px}
.logo-text{font-size:22px;font-weight:900;letter-spacing:-.5px;color:#fff}
.logo-text .nfl{color:#013369}.logo-text .plus{color:#d50a0a;font-style:normal}
.badge{background:#d50a0a;color:#fff;font-size:9px;font-weight:700;padding:2px 7px;
  border-radius:3px;letter-spacing:.5px;margin-left:8px;vertical-align:middle}
.season-tag{font-size:11px;color:#555;margin-top:2px}
.live-dot{color:#4cff80;font-size:11px}

/* week selector */
.week-pill{display:inline-flex;align-items:center;gap:6px;background:#111;
  border:1px solid #1e1e1e;border-radius:8px;padding:6px 14px;
  font-size:12px;font-weight:700;color:#aaa;margin-right:6px;cursor:pointer}
.week-pill.active{background:#013369;border-color:#013369;color:#fff}

/* game card */
.game-card{background:#111;border:1px solid #1e1e1e;border-radius:10px;
  padding:14px 18px;margin-bottom:8px;transition:border-color .15s}
.game-card:hover{border-color:#333}
.team-row{display:flex;align-items:center;gap:10px}
.tlogo{width:36px;height:36px;object-fit:contain}
.tname{font-size:13px;font-weight:700;color:#ddd;flex:1}
.trecord{font-size:10px;color:#555}
.score{font-size:22px;font-weight:900;color:#fff;min-width:28px;text-align:right}
.score.winner{color:#4cff80}
.game-meta{text-align:center;padding:0 12px}
.gtime{font-size:11px;color:#888;white-space:nowrap}
.gnet{font-size:10px;color:#555}
.glive{font-size:10px;font-weight:700;color:#ff4444;animation:pulse 1.2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.gfinal{font-size:10px;color:#555}
.gvenue{font-size:9px;color:#444;margin-top:2px}

/* pick strip */
.pick-strip{display:flex;gap:8px;margin-top:10px}
.pchip{flex:1;border-radius:7px;padding:8px 10px}
.pchip.ml{background:#1a0a0a;border:1px solid #3a1010}
.pchip.sp{background:#0a0a1a;border:1px solid #10103a}
.pchip.ou{background:#0a1a0a;border:1px solid #103a10}
.pchip-lbl{font-size:8px;font-weight:700;letter-spacing:.8px;margin-bottom:3px}
.pchip.ml .pchip-lbl{color:#ff6b6b}
.pchip.sp .pchip-lbl{color:#6b8fff}
.pchip.ou .pchip-lbl{color:#6bff9e}
.pchip-val{font-size:13px;font-weight:800;color:#fff}
.pchip-sub{font-size:9px;color:#666;margin-top:2px;line-height:1.4}
.grade{width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;
  justify-content:center;font-size:9px;font-weight:900;float:right;margin-top:-2px}
.gA{background:#1a3d1a;color:#4cff80;border:1.5px solid #4cff80}
.gB{background:#1a2a3d;color:#4ca8ff;border:1.5px solid #4ca8ff}
.gC{background:#3d3a1a;color:#ffc84c;border:1.5px solid #ffc84c}
.gD{background:#3d1a1a;color:#ff6b4c;border:1.5px solid #ff6b4c}

/* section */
.sec-hdr{font-size:10px;font-weight:700;letter-spacing:1.5px;color:#444;
  text-transform:uppercase;margin:16px 0 8px;display:flex;align-items:center;gap:8px}
.sec-hdr::after{content:'';flex:1;height:1px;background:#1a1a1a}

/* status bar */
.status-bar{background:#161616;border:1px solid #222;border-radius:7px;
  padding:8px 16px;margin-bottom:12px;font-size:11px;color:#777;
  display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.status-bar b{color:#bbb}

/* tabs */
.stTabs [data-baseweb="tab-list"]{background:#111;border-radius:8px;padding:4px;border:1px solid #1e1e1e}
.stTabs [data-baseweb="tab"]{color:#777;font-weight:600;font-size:13px}
.stTabs [aria-selected="true"]{color:#fff!important;background:#1e1e1e!important;border-radius:6px}

div.stButton>button{background:#013369;color:#fff;border:none;border-radius:8px;
  font-weight:700;font-size:13px;padding:8px 20px;width:100%}
div.stButton>button:hover{background:#0050a0}
.stSelectbox label,.stSlider label{color:#777!important;font-size:12px!important}

/* spinner override */
.stSpinner>div{border-top-color:#d50a0a!important}

/* team stats table */
.ts-row{display:flex;align-items:center;gap:12px;padding:7px 12px;
  background:#111;border:1px solid #1a1a1a;border-radius:7px;margin-bottom:3px}
.ts-rank{width:24px;text-align:center;font-size:12px;font-weight:700;color:#444}
.ts-bar{flex:1;height:5px;background:#1a1a1a;border-radius:3px;overflow:hidden}
.ts-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,#013369,#d50a0a)}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
ESPN_WEB  = "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NFLPlus/1.0)"}

TEAM_META = {
    "ARI":{"name":"Arizona Cardinals",    "stadium":"State Farm Stadium",        "cap":63400, "surf":"Grass",    "loc":"Glendale, AZ",       "roof":"Retractable"},
    "ATL":{"name":"Atlanta Falcons",       "stadium":"Mercedes-Benz Stadium",     "cap":71000, "surf":"FieldTurf","loc":"Atlanta, GA",         "roof":"Retractable"},
    "BAL":{"name":"Baltimore Ravens",      "stadium":"M&T Bank Stadium",          "cap":71008, "surf":"Grass",    "loc":"Baltimore, MD",       "roof":"Open"},
    "BUF":{"name":"Buffalo Bills",         "stadium":"Highmark Stadium",          "cap":71870, "surf":"AstroTurf","loc":"Orchard Park, NY",    "roof":"Open"},
    "CAR":{"name":"Carolina Panthers",     "stadium":"Bank of America Stadium",   "cap":74455, "surf":"Grass",    "loc":"Charlotte, NC",       "roof":"Open"},
    "CHI":{"name":"Chicago Bears",         "stadium":"Soldier Field",             "cap":61500, "surf":"Grass",    "loc":"Chicago, IL",         "roof":"Open"},
    "CIN":{"name":"Cincinnati Bengals",    "stadium":"Paycor Stadium",            "cap":65515, "surf":"Grass",    "loc":"Cincinnati, OH",      "roof":"Open"},
    "CLE":{"name":"Cleveland Browns",      "stadium":"Huntington Bank Field",     "cap":67895, "surf":"Grass",    "loc":"Cleveland, OH",       "roof":"Open"},
    "DAL":{"name":"Dallas Cowboys",        "stadium":"AT&T Stadium",              "cap":80000, "surf":"FieldTurf","loc":"Arlington, TX",       "roof":"Retractable"},
    "DEN":{"name":"Denver Broncos",        "stadium":"Empower Field",             "cap":76125, "surf":"Grass",    "loc":"Denver, CO",          "roof":"Open"},
    "DET":{"name":"Detroit Lions",         "stadium":"Ford Field",                "cap":65000, "surf":"FieldTurf","loc":"Detroit, MI",         "roof":"Dome"},
    "GB": {"name":"Green Bay Packers",     "stadium":"Lambeau Field",             "cap":81441, "surf":"Grass",    "loc":"Green Bay, WI",       "roof":"Open"},
    "HOU":{"name":"Houston Texans",        "stadium":"NRG Stadium",               "cap":72220, "surf":"Grass",    "loc":"Houston, TX",         "roof":"Retractable"},
    "IND":{"name":"Indianapolis Colts",    "stadium":"Lucas Oil Stadium",         "cap":67000, "surf":"FieldTurf","loc":"Indianapolis, IN",    "roof":"Retractable"},
    "JAX":{"name":"Jacksonville Jaguars",  "stadium":"EverBank Stadium",          "cap":69132, "surf":"Grass",    "loc":"Jacksonville, FL",    "roof":"Open"},
    "KC": {"name":"Kansas City Chiefs",    "stadium":"GEHA Field at Arrowhead",   "cap":76416, "surf":"Grass",    "loc":"Kansas City, MO",     "roof":"Open"},
    "LV": {"name":"Las Vegas Raiders",     "stadium":"Allegiant Stadium",         "cap":65000, "surf":"Grass",    "loc":"Las Vegas, NV",       "roof":"Dome"},
    "LAC":{"name":"Los Angeles Chargers",  "stadium":"SoFi Stadium",              "cap":70240, "surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered"},
    "LAR":{"name":"Los Angeles Rams",      "stadium":"SoFi Stadium",              "cap":70240, "surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered"},
    "MIA":{"name":"Miami Dolphins",        "stadium":"Hard Rock Stadium",         "cap":65326, "surf":"Grass",    "loc":"Miami Gardens, FL",   "roof":"Open"},
    "MIN":{"name":"Minnesota Vikings",     "stadium":"U.S. Bank Stadium",         "cap":66860, "surf":"FieldTurf","loc":"Minneapolis, MN",     "roof":"Dome"},
    "NE": {"name":"New England Patriots",  "stadium":"Gillette Stadium",          "cap":65878, "surf":"FieldTurf","loc":"Foxborough, MA",      "roof":"Open"},
    "NO": {"name":"New Orleans Saints",    "stadium":"Caesars Superdome",         "cap":73208, "surf":"PolyTurf", "loc":"New Orleans, LA",     "roof":"Dome"},
    "NYG":{"name":"New York Giants",       "stadium":"MetLife Stadium",           "cap":82500, "surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open"},
    "NYJ":{"name":"New York Jets",         "stadium":"MetLife Stadium",           "cap":82500, "surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open"},
    "PHI":{"name":"Philadelphia Eagles",   "stadium":"Lincoln Financial Field",   "cap":69596, "surf":"Grass",    "loc":"Philadelphia, PA",    "roof":"Open"},
    "PIT":{"name":"Pittsburgh Steelers",   "stadium":"Acrisure Stadium",          "cap":68400, "surf":"Grass",    "loc":"Pittsburgh, PA",      "roof":"Open"},
    "SF": {"name":"San Francisco 49ers",   "stadium":"Levi's Stadium",            "cap":68500, "surf":"Grass",    "loc":"Santa Clara, CA",     "roof":"Open"},
    "SEA":{"name":"Seattle Seahawks",      "stadium":"Lumen Field",               "cap":72000, "surf":"FieldTurf","loc":"Seattle, WA",         "roof":"Open"},
    "TB": {"name":"Tampa Bay Buccaneers",  "stadium":"Raymond James Stadium",     "cap":69218, "surf":"Grass",    "loc":"Tampa, FL",           "roof":"Open"},
    "TEN":{"name":"Tennessee Titans",      "stadium":"Nissan Stadium",            "cap":69143, "surf":"Grass",    "loc":"Nashville, TN",       "roof":"Open"},
    "WSH":{"name":"Washington Commanders", "stadium":"Northwest Stadium",         "cap":67617, "surf":"Grass",    "loc":"Landover, MD",        "roof":"Open"},
}

# 2026 preseason power ratings
RATINGS = {
    "SEA":{"off_ppg":29.1,"def_ppg":20.2,"rating":88,"off_rank":5, "def_rank":6, "trend":"↑"},
    "HOU":{"off_ppg":25.8,"def_ppg":18.4,"rating":84,"off_rank":10,"def_rank":2, "trend":"↑"},
    "DEN":{"off_ppg":26.1,"def_ppg":18.9,"rating":83,"off_rank":9, "def_rank":3, "trend":"↑"},
    "NE": {"off_ppg":27.0,"def_ppg":20.8,"rating":83,"off_rank":7, "def_rank":7, "trend":"↑"},
    "BUF":{"off_ppg":28.2,"def_ppg":21.5,"rating":82,"off_rank":3, "def_rank":9, "trend":"→"},
    "KC": {"off_ppg":26.4,"def_ppg":22.8,"rating":82,"off_rank":8, "def_rank":12,"trend":"→"},
    "PHI":{"off_ppg":27.9,"def_ppg":20.1,"rating":81,"off_rank":4, "def_rank":5, "trend":"→"},
    "CHI":{"off_ppg":27.8,"def_ppg":22.0,"rating":80,"off_rank":6, "def_rank":10,"trend":"↑"},
    "JAX":{"off_ppg":25.5,"def_ppg":19.2,"rating":80,"off_rank":11,"def_rank":4, "trend":"↑"},
    "LAR":{"off_ppg":31.2,"def_ppg":22.4,"rating":79,"off_rank":1, "def_rank":10,"trend":"↑"},
    "BAL":{"off_ppg":24.8,"def_ppg":21.2,"rating":77,"off_rank":14,"def_rank":8, "trend":"→"},
    "LAC":{"off_ppg":25.1,"def_ppg":22.5,"rating":77,"off_rank":12,"def_rank":11,"trend":"↑"},
    "MIN":{"off_ppg":23.8,"def_ppg":21.0,"rating":74,"off_rank":17,"def_rank":7, "trend":"→"},
    "DET":{"off_ppg":28.3,"def_ppg":24.2,"rating":74,"off_rank":2, "def_rank":16,"trend":"→"},
    "SF": {"off_ppg":24.9,"def_ppg":23.1,"rating":75,"off_rank":13,"def_rank":14,"trend":"→"},
    "CLE":{"off_ppg":20.2,"def_ppg":17.8,"rating":67,"off_rank":28,"def_rank":1, "trend":"→"},
    "WSH":{"off_ppg":22.8,"def_ppg":25.5,"rating":66,"off_rank":21,"def_rank":22,"trend":"↑"},
    "PIT":{"off_ppg":22.5,"def_ppg":23.5,"rating":69,"off_rank":22,"def_rank":15,"trend":"→"},
    "IND":{"off_ppg":23.0,"def_ppg":24.8,"rating":68,"off_rank":20,"def_rank":18,"trend":"→"},
    "CIN":{"off_ppg":24.0,"def_ppg":24.5,"rating":71,"off_rank":16,"def_rank":17,"trend":"↑"},
    "GB": {"off_ppg":23.5,"def_ppg":23.0,"rating":72,"off_rank":18,"def_rank":13,"trend":"→"},
    "NYG":{"off_ppg":21.5,"def_ppg":24.9,"rating":65,"off_rank":25,"def_rank":19,"trend":"↑"},
    "NYJ":{"off_ppg":21.8,"def_ppg":25.2,"rating":65,"off_rank":23,"def_rank":21,"trend":"→"},
    "DAL":{"off_ppg":24.2,"def_ppg":28.9,"rating":63,"off_rank":15,"def_rank":30,"trend":"↓"},
    "MIA":{"off_ppg":23.2,"def_ppg":25.0,"rating":68,"off_rank":19,"def_rank":20,"trend":"↓"},
    "TB": {"off_ppg":21.2,"def_ppg":26.0,"rating":63,"off_rank":24,"def_rank":24,"trend":"→"},
    "ATL":{"off_ppg":20.8,"def_ppg":25.8,"rating":62,"off_rank":26,"def_rank":23,"trend":"→"},
    "NO": {"off_ppg":20.5,"def_ppg":26.2,"rating":60,"off_rank":27,"def_rank":25,"trend":"↓"},
    "TEN":{"off_ppg":19.5,"def_ppg":26.5,"rating":57,"off_rank":29,"def_rank":26,"trend":"↓"},
    "ARI":{"off_ppg":18.9,"def_ppg":26.8,"rating":55,"off_rank":30,"def_rank":27,"trend":"→"},
    "CAR":{"off_ppg":18.2,"def_ppg":27.2,"rating":52,"off_rank":31,"def_rank":28,"trend":"→"},
    "LV": {"off_ppg":17.5,"def_ppg":28.0,"rating":50,"off_rank":32,"def_rank":29,"trend":"↓"},
}

LOGO = "https://a.espncdn.com/i/teamlogos/nfl/500/{}.png"

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_season_year():
    now = datetime.now()
    return now.year if now.month >= 8 else now.year - 1

def get_current_week_info():
    """Return (season_year, season_type, week_num) based on today's date."""
    now = datetime.now()
    year = get_season_year()
    # 2026 season: preseason Aug, regular Sep 9 – Jan 10
    pre_start  = datetime(year, 8, 1)
    reg_start  = datetime(year, 9, 9)   # first Wed opener
    playoffs_start = datetime(year + 1, 1, 16)
    offseason_end  = datetime(year, 8, 1)

    if now < pre_start:
        return year, 1, 1   # preseason hasn't started
    elif now < reg_start:
        weeks_in = max(1, (now - pre_start).days // 7 + 1)
        return year, 1, min(weeks_in, 4)
    elif now < playoffs_start:
        weeks_in = max(1, (now - reg_start).days // 7 + 1)
        return year, 2, min(weeks_in, 18)
    else:
        wk = (now - playoffs_start).days // 7 + 1
        return year + 1, 3, min(wk, 4)

@st.cache_data(ttl=120)
def fetch_schedule(year, season_type, week):
    """Pull live schedule from ESPN for a given week."""
    try:
        url = (f"{ESPN_BASE}/scoreboard"
               f"?dates={year}&seasontype={season_type}&week={week}&limit=25")
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    # fallback: try web variant
    try:
        url2 = (f"{ESPN_WEB}/scoreboard"
                f"?dates={year}&seasontype={season_type}&week={week}&limit=25")
        r2 = requests.get(url2, headers=HEADERS, timeout=10)
        if r2.status_code == 200:
            return r2.json()
    except Exception:
        pass
    return {}

@st.cache_data(ttl=60)
def fetch_live_scoreboard():
    """Current live/today scores."""
    try:
        url = f"{ESPN_BASE}/scoreboard"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}

@st.cache_data(ttl=300)
def fetch_injuries(team_id):
    try:
        url = f"{ESPN_CORE}/teams/{team_id}/injuries"
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            return []
        items = r.json().get("items", [])
        out = []
        for item in items[:8]:
            ref = item.get("$ref", "")
            if not ref:
                continue
            dr = requests.get(ref, headers=HEADERS, timeout=5)
            if dr.status_code != 200:
                continue
            d = dr.json()
            status = d.get("status", "Questionable")
            athlete_ref = d.get("athlete", {}).get("$ref", "")
            if athlete_ref:
                ar = requests.get(athlete_ref, headers=HEADERS, timeout=5)
                if ar.status_code == 200:
                    ad = ar.json()
                    out.append({
                        "name": ad.get("displayName", "Unknown"),
                        "pos":  ad.get("position", {}).get("abbreviation", "?"),
                        "status": status,
                    })
        return out
    except Exception:
        return []

def parse_games(data):
    """Extract game objects from ESPN scoreboard JSON."""
    games = []
    for event in data.get("events", []):
        try:
            comp = event["competitions"][0]
            competitors = comp["competitors"]
            home = next(c for c in competitors if c["homeAway"] == "home")
            away = next(c for c in competitors if c["homeAway"] == "away")

            home_abbr = home["team"]["abbreviation"]
            away_abbr = away["team"]["abbreviation"]

            status_obj = event["status"]
            state = status_obj["type"]["state"]          # pre / in / post
            status_name = status_obj["type"]["shortDetail"]

            venue = comp.get("venue", {})
            venue_name = venue.get("fullName", "")
            venue_loc  = (venue.get("address", {}).get("city", "") + ", " +
                          venue.get("address", {}).get("state", "")).strip(", ")

            broadcasts = comp.get("broadcasts", [])
            network = ""
            if broadcasts:
                meds = broadcasts[0].get("media", {})
                network = meds.get("shortName", "") or meds.get("callLetters", "")

            date_str = event.get("date", "")
            dt_obj = None
            if date_str:
                try:
                    dt_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except Exception:
                    pass

            home_score = home.get("score", "")
            away_score = away.get("score", "")

            home_record = home.get("records", [{}])[0].get("summary", "") if home.get("records") else ""
            away_record = away.get("records", [{}])[0].get("summary", "") if away.get("records") else ""

            games.append({
                "id":          event["id"],
                "name":        event.get("name", ""),
                "short_name":  event.get("shortName", ""),
                "home_abbr":   home_abbr,
                "away_abbr":   away_abbr,
                "home_id":     home["team"]["id"],
                "away_id":     away["team"]["id"],
                "home_logo":   home["team"].get("logo", LOGO.format(home_abbr.lower())),
                "away_logo":   away["team"].get("logo", LOGO.format(away_abbr.lower())),
                "home_name":   home["team"].get("displayName", home_abbr),
                "away_name":   away["team"].get("displayName", away_abbr),
                "home_score":  home_score,
                "away_score":  away_score,
                "home_record": home_record,
                "away_record": away_record,
                "state":       state,
                "status":      status_name,
                "network":     network,
                "venue":       venue_name or TEAM_META.get(home_abbr, {}).get("stadium", ""),
                "venue_loc":   venue_loc or TEAM_META.get(home_abbr, {}).get("loc", ""),
                "dt":          dt_obj,
            })
        except Exception:
            continue
    return games

# ── Prediction engine ─────────────────────────────────────────────────────────
INJ_IMPACT = {"QB":9.5,"RB":4.0,"WR":3.5,"TE":3.0,"OT":3.5,"OG":2.5,
              "C":2.5,"DE":4.0,"DT":3.5,"LB":3.5,"CB":4.0,"S":3.0,"K":2.0,"P":1.0}

def predict(away_abbr, home_abbr, away_injuries=None, home_injuries=None):
    ar = RATINGS.get(away_abbr, {"rating":65,"off_ppg":22.0,"def_ppg":24.0,"off_rank":20,"def_rank":20})
    hr = RATINGS.get(home_abbr, {"rating":65,"off_ppg":22.0,"def_ppg":24.0,"off_rank":20,"def_rank":20})

    away_proj = ar["off_ppg"] * 0.55 + (33 - hr["def_ppg"]) * 0.45
    home_proj = hr["off_ppg"] * 0.55 + (33 - ar["def_ppg"]) * 0.45 + 2.5

    def inj_penalty(injuries):
        pen = 0
        for inj in (injuries or []):
            mult = {"Out":1.0,"IR":1.0,"Doubtful":0.8,"Questionable":0.4,"Probable":0.1}.get(inj.get("status","Q"), 0.4)
            pen += INJ_IMPACT.get(inj.get("pos","WR"), 2.5) * mult * 0.1
        return pen

    away_proj = max(10, away_proj - inj_penalty(away_injuries))
    home_proj = max(10, home_proj - inj_penalty(home_injuries))

    total = away_proj + home_proj
    rating_diff = (hr["rating"] - ar["rating"]) + 3
    home_wp = 1 / (1 + np.exp(-rating_diff / 12))
    away_wp = 1 - home_wp

    if home_wp > 0.5:
        home_ml = int(-home_wp / (1 - home_wp) * 100)
        away_ml = int((1 - home_wp) / home_wp * 100)
    else:
        away_ml = int(-away_wp / (1 - away_wp) * 100)
        home_ml = int((1 - away_wp) / away_wp * 100)

    diff = home_proj - away_proj
    spread = round(diff / 2.5) * 0.5
    total_line = round(total * 2) / 2
    ou = "OVER" if total > total_line + 0.3 else "UNDER"

    conf = abs(rating_diff)
    grade = "A+" if conf>20 else "A" if conf>15 else "B+" if conf>10 else "B" if conf>6 else "C" if conf>3 else "D"
    ml_g  = "A" if abs(home_ml)>160 else "B" if abs(home_ml)>120 else "C" if abs(home_ml)>105 else "D"
    rl_g  = "A" if abs(spread)>=7 else "B" if abs(spread)>=4 else "C" if abs(spread)>=2 else "D"
    ou_g  = grade

    return {
        "away_proj": round(away_proj,1), "home_proj": round(home_proj,1),
        "total": round(total,1), "total_line": total_line, "ou": ou,
        "home_wp": round(home_wp*100,1), "away_wp": round(away_wp*100,1),
        "home_ml": home_ml, "away_ml": away_ml, "spread": spread,
        "pick_ml": home_abbr if home_wp>0.5 else away_abbr,
        "grade": grade, "ml_g": ml_g, "rl_g": rl_g, "ou_g": ou_g,
    }

def gclass(g):
    if g.startswith("A"): return "gA"
    if g.startswith("B"): return "gB"
    if g.startswith("C"): return "gC"
    return "gD"

def ml_fmt(v):
    return f"+{v}" if v > 0 else str(v)

def spread_str(away_abbr, home_abbr, spread):
    if spread == 0: return "PK"
    if spread > 0:  return f"{home_abbr} -{abs(spread):.1f}"
    return f"{away_abbr} -{abs(spread):.1f}"

# ── Header ────────────────────────────────────────────────────────────────────
sy, st_type, cur_week = get_current_week_info()
season_label = {1:"Preseason", 2:"Regular Season", 3:"Playoffs"}.get(st_type, "Season")

st.markdown(f"""
<div class="nfl-header">
  <div>
    <div class="logo-text">🏈 <span class="nfl">NFL</span><em class="plus">+</em> PREDICTOR
      <span class="badge">LIVE</span></div>
    <div class="season-tag">{sy}–{str(sy+1)[2:]} NFL Season · ESPN API · Picks Auto-Update Each Week</div>
  </div>
  <div style="text-align:right;font-size:11px;color:#555">
    {season_label} · Week {cur_week}<br>
    <span class="live-dot">● Auto-tracking season</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main Tabs ─────────────────────────────────────────────────────────────────
tab_sched, tab_predict, tab_stats = st.tabs(
    ["📅  Live Schedule & Picks", "🔍  Matchup Analyzer", "📊  Power Rankings"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE SCHEDULE (auto follows season)
# ══════════════════════════════════════════════════════════════════════════════
with tab_sched:

    # ── Week / season type controls ───────────────────────────────────────────
    col_st, col_wk, col_yr, col_ref = st.columns([2, 2, 2, 1])
    with col_st:
        stype_map = {"Preseason (Aug)":1, "Regular Season":2, "Playoffs":3}
        stype_default = {1:"Preseason (Aug)", 2:"Regular Season", 3:"Playoffs"}.get(st_type, "Regular Season")
        sel_stype = st.selectbox("Season Phase", list(stype_map.keys()),
                                 index=list(stype_map.keys()).index(stype_default))
    with col_wk:
        max_wk = {1:4, 2:18, 3:4}.get(stype_map[sel_stype], 18)
        sel_week = st.slider("Week", 1, max_wk, cur_week if stype_map[sel_stype]==st_type else 1)
    with col_yr:
        sel_year = st.selectbox("Season Year", [sy, sy-1], index=0)
    with col_ref:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        refresh = st.button("↻ Refresh", use_container_width=True)

    if refresh:
        st.cache_data.clear()

    # ── Fetch games ───────────────────────────────────────────────────────────
    with st.spinner(f"Fetching Week {sel_week} games from ESPN…"):
        raw = fetch_schedule(sel_year, stype_map[sel_stype], sel_week)

    games = parse_games(raw)

    # Pull week/season context from response
    season_resp = raw.get("season", {})
    week_resp   = raw.get("week", {})
    week_label  = week_resp.get("text", f"Week {sel_week}")

    # Status bar
    live_ct = sum(1 for g in games if g["state"] == "in")
    final_ct = sum(1 for g in games if g["state"] == "post")
    pre_ct   = sum(1 for g in games if g["state"] == "pre")
    st.markdown(f"""
    <div class="status-bar">
      <b>📡 ESPN Live Feed</b> ·
      <span>{len(games)} games · {season_resp.get('displayName','2026 NFL')}</span> ·
      <span style="color:#ff4444">● {live_ct} Live</span> ·
      <span style="color:#888">{final_ct} Final · {pre_ct} Upcoming</span>
    </div>
    """, unsafe_allow_html=True)

    if not games:
        st.markdown("""
        <div style="background:#161616;border:1px solid #222;border-radius:10px;
          padding:40px;text-align:center;color:#444;font-size:14px;margin-top:20px;">
          No games found for this week. ESPN may not have posted the schedule yet,
          or try a different week/season type above.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sec-hdr">{week_label} · {len(games)} Games</div>', unsafe_allow_html=True)

        for g in games:
            p = predict(g["away_abbr"], g["home_abbr"])
            away_m = TEAM_META.get(g["away_abbr"], {})
            home_m = TEAM_META.get(g["home_abbr"], {})

            # Determine winner for post-game coloring
            away_win = home_win = False
            if g["state"] == "post" and g["home_score"] and g["away_score"]:
                try:
                    away_win = int(g["away_score"]) > int(g["home_score"])
                    home_win = not away_win
                except Exception:
                    pass

            # Format kickoff time
            time_disp = g["status"]
            if g["state"] == "pre" and g["dt"]:
                try:
                    local_dt = g["dt"].astimezone()
                    time_disp = local_dt.strftime("%-m/%-d · %-I:%M %p").replace("  ", " ")
                except Exception:
                    pass

            sp = spread_str(g["away_abbr"], g["home_abbr"], p["spread"])
            ou_color = "#4cff80" if p["ou"] == "OVER" else "#ff6b6b"

            st.markdown(f"""
<div class="game-card">
  <div style="display:flex;align-items:center;gap:12px;">

    <!-- Away -->
    <div style="flex:1">
      <div class="team-row" style="margin-bottom:6px">
        <img src="{g['away_logo']}" class="tlogo"
             onerror="this.src='{LOGO.format(g['away_abbr'].lower())}'">
        <span class="tname">{g['away_name']}</span>
        <span class="trecord">{g['away_record']}</span>
        <span class="score {'winner' if away_win else ''}">{g['away_score'] if g['state']!='pre' else ''}</span>
      </div>
      <div class="team-row">
        <img src="{g['home_logo']}" class="tlogo"
             onerror="this.src='{LOGO.format(g['home_abbr'].lower())}'">
        <span class="tname">{g['home_name']}</span>
        <span class="trecord">{g['home_record']}</span>
        <span class="score {'winner' if home_win else ''}">{g['home_score'] if g['state']!='pre' else ''}</span>
      </div>
    </div>

    <!-- Meta -->
    <div class="game-meta" style="min-width:110px">
      {'<div class="glive">⬤ LIVE</div>' if g["state"]=="in" else ''}
      {'<div class="gfinal">FINAL</div>' if g["state"]=="post" else ''}
      <div class="gtime">{time_disp}</div>
      {'<div class="gnet">📺 ' + g["network"] + '</div>' if g["network"] else ''}
      <div class="gvenue">🏟 {g['venue']}</div>
    </div>

    <!-- Win prob (pre/live only) -->
    {'<div style="min-width:80px;text-align:center"><div style="font-size:9px;color:#555;margin-bottom:4px">WIN PROB</div><div style="font-size:12px;font-weight:700;color:#6b8fff">' + g["away_abbr"] + ' ' + str(p["away_wp"]) + '%</div><div style="font-size:10px;color:#444">vs</div><div style="font-size:12px;font-weight:700;color:#ff6b6b">' + g["home_abbr"] + ' ' + str(p["home_wp"]) + '%</div></div>' if g["state"] != "post" else ''}

  </div>

  <!-- Pick strip -->
  <div class="pick-strip">
    <div class="pchip ml">
      <span class="pchip-lbl">💰 MONEYLINE</span>
      <div class="grade {gclass(p['ml_g'])}">{p['ml_g']}</div>
      <div class="pchip-val">{p['pick_ml']}</div>
      <div class="pchip-sub">{g['away_abbr']} {ml_fmt(p['away_ml'])} | {g['home_abbr']} {ml_fmt(p['home_ml'])}</div>
    </div>
    <div class="pchip sp">
      <span class="pchip-lbl">🏈 SPREAD</span>
      <div class="grade {gclass(p['rl_g'])}">{p['rl_g']}</div>
      <div class="pchip-val">{sp}</div>
      <div class="pchip-sub">Proj {p['away_proj']}–{p['home_proj']} · margin {abs(p['home_proj']-p['away_proj']):.1f}pts</div>
    </div>
    <div class="pchip ou">
      <span class="pchip-lbl">🎯 TOTAL</span>
      <div class="grade {gclass(p['ou_g'])}">{p['ou_g']}</div>
      <div class="pchip-val" style="color:{ou_color}">{p['ou']} {p['total_line']}</div>
      <div class="pchip-sub">Proj {p['total']} pts · {g['away_abbr']} O: {RATINGS.get(g['away_abbr'],{}).get('off_ppg',22):.1f} | {g['home_abbr']} D: {RATINGS.get(g['home_abbr'],{}).get('def_ppg',24):.1f}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MATCHUP ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab_predict:
    all_abbrs = sorted(TEAM_META.keys())
    all_names = [TEAM_META[a]["name"] for a in all_abbrs]

    c1, c2, c3 = st.columns([2, 0.5, 2])
    with c1:
        st.markdown('<div style="font-size:10px;color:#555;margin-bottom:4px">AWAY TEAM</div>', unsafe_allow_html=True)
        away_sel = st.selectbox("Away", all_names, index=all_names.index("New England Patriots"),
                                label_visibility="collapsed")
    with c2:
        st.markdown('<div style="text-align:center;font-size:22px;font-weight:900;color:#444;padding-top:22px">@</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div style="font-size:10px;color:#555;margin-bottom:4px">HOME TEAM</div>', unsafe_allow_html=True)
        home_sel = st.selectbox("Home", all_names, index=all_names.index("Seattle Seahawks"),
                                label_visibility="collapsed")

    away_abbr2 = all_abbrs[all_names.index(away_sel)]
    home_abbr2 = all_abbrs[all_names.index(home_sel)]

    if away_abbr2 == home_abbr2:
        st.warning("Pick two different teams.")
        st.stop()

    cb1, cb2, cb3 = st.columns([1,2,1])
    with cb2:
        do_analyze = st.button("🔍  Fetch Live Injuries & Analyze", use_container_width=True)

    away_inj = home_inj = []
    if do_analyze:
        with st.spinner("Pulling live injury reports from ESPN…"):
            away_inj = fetch_injuries(TEAM_META[away_abbr2].get("id", ""))
            home_inj = fetch_injuries(TEAM_META[home_abbr2].get("id", ""))

    p2 = predict(away_abbr2, home_abbr2, away_inj, home_inj)
    hm = TEAM_META.get(home_abbr2, {})
    am = TEAM_META.get(away_abbr2, {})
    hr2 = RATINGS.get(home_abbr2, {})
    ar2 = RATINGS.get(away_abbr2, {})

    ou_color2 = "#4cff80" if p2["ou"]=="OVER" else "#ff6b6b"

    # Hero card
    st.markdown(f"""
<div class="game-card" style="padding:20px 24px;margin-top:8px">
  <div style="display:flex;align-items:center">
    <div style="flex:1;text-align:center">
      <img src="{LOGO.format(away_abbr2.lower())}" style="width:72px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))"
           onerror="this.style.opacity=.3">
      <div style="font-size:13px;font-weight:700;color:#aaa;margin-top:8px">{away_sel}</div>
      <div style="font-size:30px;font-weight:900;color:#fff">{p2['away_wp']}%</div>
      <div style="font-size:10px;color:#555">Win Probability</div>
      <div style="font-size:12px;color:#6b8fff;font-weight:700;margin-top:4px">
        Proj {p2['away_proj']} pts &nbsp;·&nbsp; ML {ml_fmt(p2['away_ml'])}
      </div>
    </div>
    <div style="flex:0 0 140px;text-align:center">
      <div style="font-size:10px;color:#444">2026 NFL SEASON</div>
      <div style="font-size:20px;font-weight:900;color:#333;margin:4px 0">@</div>
      <div style="font-size:15px;font-weight:800;color:#fff">{p2['away_proj']} – {p2['home_proj']}</div>
      <div style="font-size:10px;color:#555">Projected Final</div>
      <div style="display:inline-block;background:#1a2e1a;color:#4cff80;font-size:10px;font-weight:700;
        padding:3px 10px;border-radius:12px;margin-top:6px">O/U {p2['total_line']}</div>
    </div>
    <div style="flex:1;text-align:center">
      <img src="{LOGO.format(home_abbr2.lower())}" style="width:72px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))"
           onerror="this.style.opacity=.3">
      <div style="font-size:13px;font-weight:700;color:#aaa;margin-top:8px">{home_sel}</div>
      <div style="font-size:30px;font-weight:900;color:#fff">{p2['home_wp']}%</div>
      <div style="font-size:10px;color:#555">Win Probability</div>
      <div style="font-size:12px;color:#ff6b6b;font-weight:700;margin-top:4px">
        Proj {p2['home_proj']} pts &nbsp;·&nbsp; ML {ml_fmt(p2['home_ml'])}
      </div>
    </div>
  </div>

  <!-- Stadium -->
  <div style="background:#161616;border:1px solid #1e1e1e;border-radius:7px;
    padding:8px 16px;margin:14px 0 14px;font-size:11px;color:#777;
    display:flex;flex-wrap:wrap;gap:6px 18px">
    <span>🏟️ <b style="color:#bbb">{hm.get('stadium','')}</b></span>
    <span>📍 {hm.get('loc','')}</span>
    <span>🏠 Cap. {hm.get('cap',0):,}</span>
    <span>🌿 {hm.get('surf','')}</span>
    <span>🔲 {hm.get('roof','')}</span>
  </div>

  <!-- Picks -->
  <div class="pick-strip">
    <div class="pchip ml">
      <span class="pchip-lbl">💰 MONEYLINE</span>
      <div class="grade {gclass(p2['ml_g'])}">{p2['ml_g']}</div>
      <div class="pchip-val">{TEAM_META.get(p2['pick_ml'],{{}}).get('name', p2['pick_ml']).split()[-1]}</div>
      <div class="pchip-sub">{away_abbr2} {ml_fmt(p2['away_ml'])} | {home_abbr2} {ml_fmt(p2['home_ml'])}<br>
        {away_abbr2} {p2['away_wp']}% / {home_abbr2} {p2['home_wp']}%</div>
    </div>
    <div class="pchip sp">
      <span class="pchip-lbl">🏈 SPREAD</span>
      <div class="grade {gclass(p2['rl_g'])}">{p2['rl_g']}</div>
      <div class="pchip-val">{spread_str(away_abbr2, home_abbr2, p2['spread'])}</div>
      <div class="pchip-sub">Proj: {away_abbr2} {p2['away_proj']} – {home_abbr2} {p2['home_proj']}<br>
        Margin {abs(p2['home_proj']-p2['away_proj']):.1f} pts</div>
    </div>
    <div class="pchip ou">
      <span class="pchip-lbl">🎯 TOTAL POINTS</span>
      <div class="grade {gclass(p2['ou_g'])}">{p2['ou_g']}</div>
      <div class="pchip-val" style="color:{ou_color2}">{p2['ou']} {p2['total_line']}</div>
      <div class="pchip-sub">Proj {p2['total']} pts total<br>
        {away_abbr2} O {ar2.get('off_ppg',22):.1f} | {home_abbr2} D {hr2.get('def_ppg',24):.1f} allowed</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Stats + Injuries side by side
    st.markdown('<div class="sec-hdr">Team Comparison</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)

    with sc1:
        rows = [
            ("Power Rating", ar2.get("rating","–"), hr2.get("rating","–")),
            ("Off PPG",      ar2.get("off_ppg","–"), hr2.get("off_ppg","–")),
            ("Def PPG Allowed", ar2.get("def_ppg","–"), hr2.get("def_ppg","–")),
            ("Off Rank",     f"#{ar2.get('off_rank','–')}", f"#{hr2.get('off_rank','–')}"),
            ("Def Rank",     f"#{ar2.get('def_rank','–')}", f"#{hr2.get('def_rank','–')}"),
            ("2026 Trend",   ar2.get("trend","→"), hr2.get("trend","→")),
        ]
        html = f"""<div style="background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:14px 16px">
          <div style="display:flex;justify-content:space-between;font-size:10px;font-weight:700;
            padding-bottom:6px;border-bottom:1px solid #1e1e1e;margin-bottom:4px">
            <span style="color:#555">STAT</span>
            <span style="color:#6b8fff">{away_abbr2}</span>
            <span style="color:#ff6b6b">{home_abbr2}</span>
          </div>"""
        for label, av, hv in rows:
            html += f"""<div style="display:flex;justify-content:space-between;padding:5px 0;
              border-bottom:1px solid #111;font-size:12px">
              <span style="color:#666">{label}</span>
              <span style="color:#6b8fff;font-weight:700">{av}</span>
              <span style="color:#ff6b6b;font-weight:700">{hv}</span>
            </div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    with sc2:
        st.markdown('<div style="font-size:10px;color:#555;font-weight:700;margin-bottom:6px">🚑 INJURY REPORT</div>', unsafe_allow_html=True)
        if away_inj or home_inj:
            for inj in (away_inj or []):
                sc = {"Out":"status-out","IR":"status-out","Doubtful":"status-out",
                      "Questionable":"status-quest","Probable":"status-prob"}.get(inj.get("status",""), "status-quest")
                st.markdown(f"""<div style="background:#161616;border:1px solid #222;border-radius:6px;
                  padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center">
                  <div><span style="font-size:12px;font-weight:700;color:#fff">{inj['name']}</span>
                  <span style="font-size:10px;color:#666;margin-left:8px">{inj['pos']} · {away_abbr2}</span></div>
                  <span style="font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;
                    background:#3d2e10;color:#ffc84c">{inj['status']}</span>
                </div>""", unsafe_allow_html=True)
            for inj in (home_inj or []):
                st.markdown(f"""<div style="background:#161616;border:1px solid #222;border-radius:6px;
                  padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center">
                  <div><span style="font-size:12px;font-weight:700;color:#fff">{inj['name']}</span>
                  <span style="font-size:10px;color:#666;margin-left:8px">{inj['pos']} · {home_abbr2}</span></div>
                  <span style="font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;
                    background:#3d2e10;color:#ffc84c">{inj['status']}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#161616;border:1px solid #222;border-radius:8px;
              padding:24px;text-align:center;color:#444;font-size:12px">
              Click <b style="color:#888">Fetch Live Injuries & Analyze</b><br>to pull real-time ESPN injury data
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — POWER RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown('<div class="sec-hdr">2026 Preseason Power Ratings · All 32 Teams</div>', unsafe_allow_html=True)

    sorted_r = sorted(RATINGS.items(), key=lambda x: x[1]["rating"], reverse=True)
    for rank, (abbr, r) in enumerate(sorted_r, 1):
        meta = TEAM_META.get(abbr, {})
        trend_col = "#4cff80" if r["trend"]=="↑" else "#ff6b6b" if r["trend"]=="↓" else "#666"
        bar_pct = r["rating"]

        st.markdown(f"""
<div class="ts-row">
  <div class="ts-rank">#{rank}</div>
  <img src="{LOGO.format(abbr.lower())}" style="width:28px;height:28px;object-fit:contain"
       onerror="this.style.opacity=.2">
  <div style="flex:1;min-width:0">
    <div style="font-size:12px;font-weight:700;color:#ddd;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
      {meta.get('name', abbr)}</div>
    <div style="font-size:10px;color:#444">{meta.get('stadium','')}</div>
  </div>
  <div style="min-width:48px;text-align:center">
    <div style="font-size:9px;color:#555">OFF</div>
    <div style="font-size:12px;font-weight:700;color:#6b8fff">{r['off_ppg']}</div>
  </div>
  <div style="min-width:48px;text-align:center">
    <div style="font-size:9px;color:#555">DEF</div>
    <div style="font-size:12px;font-weight:700;color:#ff6b6b">{r['def_ppg']}</div>
  </div>
  <div style="min-width:40px;text-align:center">
    <div style="font-size:9px;color:#555">RTG</div>
    <div style="font-size:16px;font-weight:900;color:#fff">{r['rating']}</div>
  </div>
  <div style="font-size:16px;color:{trend_col};min-width:20px;text-align:center">{r['trend']}</div>
  <div class="ts-bar" style="min-width:80px">
    <div class="ts-fill" style="width:{bar_pct}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-top:16px;padding:10px 14px;background:#111;border:1px solid #1e1e1e;
  border-radius:7px;font-size:10px;color:#444">
  📊 Data: ESPN API (live schedule/injuries) · 2025 final stats · 2026 preseason rankings (ESPN, NBC Sports)<br>
  ⚠️ For entertainment only. Predictions update each week as the season progresses.
</div>
""", unsafe_allow_html=True)
