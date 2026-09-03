import streamlit as st
import requests
import numpy as np
from datetime import datetime

st.set_page_config(page_title="NFL Plus", page_icon="🏈", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0d0d0d;color:#f0f0f0}
.stApp{background:#0d0d0d}
footer,#MainMenu,header{display:none!important;visibility:hidden!important}
.nfl-hdr{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:#111;border-bottom:2px solid #1e1e1e;margin-bottom:18px}
.logo{font-size:22px;font-weight:900;letter-spacing:-.5px;color:#fff}
.logo .n{color:#013369}.logo .p{color:#d50a0a}
.badge{background:#d50a0a;color:#fff;font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px;margin-left:8px}
.stag{font-size:11px;color:#555;margin-top:2px}
.ldot{color:#4cff80;font-size:11px}
.gc{background:#111;border:1px solid #1e1e1e;border-radius:10px;padding:12px 14px;margin-bottom:7px}
.gc:hover{border-color:#2a2a2a}
.tr{display:flex;align-items:center;gap:8px;margin-bottom:5px}
.tl{width:28px;height:28px;object-fit:contain}
.tn{font-size:12px;font-weight:700;color:#ccc;flex:1}
.trec{font-size:9px;color:#444}
.sc{font-size:18px;font-weight:900;color:#fff;min-width:24px;text-align:right}
.sc.win{color:#4cff80}
.gm{min-width:100px;text-align:center;padding:0 8px}
.glv{font-size:9px;font-weight:700;color:#ff4444}
.gfn{font-size:9px;color:#555}
.gt{font-size:10px;color:#777;margin:2px 0}
.gn{font-size:9px;color:#444}
.gv{font-size:8px;color:#333;margin-top:3px}
.wpc{min-width:72px;text-align:center}
.picks{display:flex;gap:6px;margin-top:10px}
.pml{flex:1;border-radius:7px;padding:8px 9px;background:#1a0a0a;border:1px solid #3a1010}
.psp{flex:1;border-radius:7px;padding:8px 9px;background:#0a0a1a;border:1px solid #10103a}
.pou{flex:1;border-radius:7px;padding:8px 9px;background:#0a1a0a;border:1px solid #103a10}
.pl{font-size:7px;font-weight:700;letter-spacing:.8px;margin-bottom:3px}
.pml .pl{color:#ff6b6b}.psp .pl{color:#6b8fff}.pou .pl{color:#6bff9e}
.pv{font-size:12px;font-weight:800;color:#fff;margin-bottom:2px}
.ps{font-size:8px;color:#555;line-height:1.4}
.gr{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:900;float:right;margin-top:-2px}
.grA{background:#1a3d1a;color:#4cff80;border:1.5px solid #4cff80}
.grB{background:#1a2a3d;color:#4ca8ff;border:1.5px solid #4ca8ff}
.grC{background:#3d3a1a;color:#ffc84c;border:1.5px solid #ffc84c}
.grD{background:#3d1a1a;color:#ff6b4c;border:1.5px solid #ff6b4c}
.sh{font-size:10px;font-weight:700;letter-spacing:1.5px;color:#444;text-transform:uppercase;margin:16px 0 8px;display:flex;align-items:center;gap:8px}
.sh::after{content:'';flex:1;height:1px;background:#1a1a1a}
.sb{background:#161616;border:1px solid #1e1e1e;border-radius:7px;padding:8px 14px;margin-bottom:10px;font-size:10px;color:#666;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.stTabs [data-baseweb="tab-list"]{background:#111;border-radius:8px;padding:4px;border:1px solid #1e1e1e}
.stTabs [data-baseweb="tab"]{color:#777;font-weight:600;font-size:13px}
.stTabs [aria-selected="true"]{color:#fff!important;background:#1e1e1e!important;border-radius:6px}
div.stButton>button{background:#013369;color:#fff;border:none;border-radius:8px;font-weight:700;font-size:13px;padding:8px 20px;width:100%}
div.stButton>button:hover{background:#0050a0}
.stSelectbox label,.stSlider label{color:#777!important;font-size:12px!important}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
ESPN_WEB  = "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl"
HDR = {"User-Agent": "Mozilla/5.0"}
LOGO = "https://a.espncdn.com/i/teamlogos/nfl/500/{}.png"

TEAM_META = {
    "ARI":{"name":"Arizona Cardinals",    "stadium":"State Farm Stadium",        "cap":63400,"surf":"Grass",    "loc":"Glendale, AZ",       "roof":"Retractable"},
    "ATL":{"name":"Atlanta Falcons",       "stadium":"Mercedes-Benz Stadium",     "cap":71000,"surf":"FieldTurf","loc":"Atlanta, GA",         "roof":"Retractable"},
    "BAL":{"name":"Baltimore Ravens",      "stadium":"M&T Bank Stadium",          "cap":71008,"surf":"Grass",    "loc":"Baltimore, MD",       "roof":"Open"},
    "BUF":{"name":"Buffalo Bills",         "stadium":"Highmark Stadium",          "cap":71870,"surf":"AstroTurf","loc":"Orchard Park, NY",    "roof":"Open"},
    "CAR":{"name":"Carolina Panthers",     "stadium":"Bank of America Stadium",   "cap":74455,"surf":"Grass",    "loc":"Charlotte, NC",       "roof":"Open"},
    "CHI":{"name":"Chicago Bears",         "stadium":"Soldier Field",             "cap":61500,"surf":"Grass",    "loc":"Chicago, IL",         "roof":"Open"},
    "CIN":{"name":"Cincinnati Bengals",    "stadium":"Paycor Stadium",            "cap":65515,"surf":"Grass",    "loc":"Cincinnati, OH",      "roof":"Open"},
    "CLE":{"name":"Cleveland Browns",      "stadium":"Huntington Bank Field",     "cap":67895,"surf":"Grass",    "loc":"Cleveland, OH",       "roof":"Open"},
    "DAL":{"name":"Dallas Cowboys",        "stadium":"AT&T Stadium",              "cap":80000,"surf":"FieldTurf","loc":"Arlington, TX",       "roof":"Retractable"},
    "DEN":{"name":"Denver Broncos",        "stadium":"Empower Field",             "cap":76125,"surf":"Grass",    "loc":"Denver, CO",          "roof":"Open"},
    "DET":{"name":"Detroit Lions",         "stadium":"Ford Field",                "cap":65000,"surf":"FieldTurf","loc":"Detroit, MI",         "roof":"Dome"},
    "GB": {"name":"Green Bay Packers",     "stadium":"Lambeau Field",             "cap":81441,"surf":"Grass",    "loc":"Green Bay, WI",       "roof":"Open"},
    "HOU":{"name":"Houston Texans",        "stadium":"NRG Stadium",               "cap":72220,"surf":"Grass",    "loc":"Houston, TX",         "roof":"Retractable"},
    "IND":{"name":"Indianapolis Colts",    "stadium":"Lucas Oil Stadium",         "cap":67000,"surf":"FieldTurf","loc":"Indianapolis, IN",    "roof":"Retractable"},
    "JAX":{"name":"Jacksonville Jaguars",  "stadium":"EverBank Stadium",          "cap":69132,"surf":"Grass",    "loc":"Jacksonville, FL",    "roof":"Open"},
    "KC": {"name":"Kansas City Chiefs",    "stadium":"GEHA Field at Arrowhead",   "cap":76416,"surf":"Grass",    "loc":"Kansas City, MO",     "roof":"Open"},
    "LV": {"name":"Las Vegas Raiders",     "stadium":"Allegiant Stadium",         "cap":65000,"surf":"Grass",    "loc":"Las Vegas, NV",       "roof":"Dome"},
    "LAC":{"name":"Los Angeles Chargers",  "stadium":"SoFi Stadium",              "cap":70240,"surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered"},
    "LAR":{"name":"Los Angeles Rams",      "stadium":"SoFi Stadium",              "cap":70240,"surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered"},
    "MIA":{"name":"Miami Dolphins",        "stadium":"Hard Rock Stadium",         "cap":65326,"surf":"Grass",    "loc":"Miami Gardens, FL",   "roof":"Open"},
    "MIN":{"name":"Minnesota Vikings",     "stadium":"U.S. Bank Stadium",         "cap":66860,"surf":"FieldTurf","loc":"Minneapolis, MN",     "roof":"Dome"},
    "NE": {"name":"New England Patriots",  "stadium":"Gillette Stadium",          "cap":65878,"surf":"FieldTurf","loc":"Foxborough, MA",      "roof":"Open"},
    "NO": {"name":"New Orleans Saints",    "stadium":"Caesars Superdome",         "cap":73208,"surf":"PolyTurf", "loc":"New Orleans, LA",     "roof":"Dome"},
    "NYG":{"name":"New York Giants",       "stadium":"MetLife Stadium",           "cap":82500,"surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open"},
    "NYJ":{"name":"New York Jets",         "stadium":"MetLife Stadium",           "cap":82500,"surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open"},
    "PHI":{"name":"Philadelphia Eagles",   "stadium":"Lincoln Financial Field",   "cap":69596,"surf":"Grass",    "loc":"Philadelphia, PA",    "roof":"Open"},
    "PIT":{"name":"Pittsburgh Steelers",   "stadium":"Acrisure Stadium",          "cap":68400,"surf":"Grass",    "loc":"Pittsburgh, PA",      "roof":"Open"},
    "SF": {"name":"San Francisco 49ers",   "stadium":"Levi's Stadium",            "cap":68500,"surf":"Grass",    "loc":"Santa Clara, CA",     "roof":"Open"},
    "SEA":{"name":"Seattle Seahawks",      "stadium":"Lumen Field",               "cap":72000,"surf":"FieldTurf","loc":"Seattle, WA",         "roof":"Open"},
    "TB": {"name":"Tampa Bay Buccaneers",  "stadium":"Raymond James Stadium",     "cap":69218,"surf":"Grass",    "loc":"Tampa, FL",           "roof":"Open"},
    "TEN":{"name":"Tennessee Titans",      "stadium":"Nissan Stadium",            "cap":69143,"surf":"Grass",    "loc":"Nashville, TN",       "roof":"Open"},
    "WSH":{"name":"Washington Commanders", "stadium":"Northwest Stadium",         "cap":67617,"surf":"Grass",    "loc":"Landover, MD",        "roof":"Open"},
}

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
    "SF": {"off_ppg":24.9,"def_ppg":23.1,"rating":75,"off_rank":13,"def_rank":14,"trend":"→"},
    "DET":{"off_ppg":28.3,"def_ppg":24.2,"rating":74,"off_rank":2, "def_rank":16,"trend":"→"},
    "MIN":{"off_ppg":23.8,"def_ppg":21.0,"rating":74,"off_rank":17,"def_rank":7, "trend":"→"},
    "GB": {"off_ppg":23.5,"def_ppg":23.0,"rating":72,"off_rank":18,"def_rank":13,"trend":"→"},
    "CIN":{"off_ppg":24.0,"def_ppg":24.5,"rating":71,"off_rank":16,"def_rank":17,"trend":"↑"},
    "PIT":{"off_ppg":22.5,"def_ppg":23.5,"rating":69,"off_rank":22,"def_rank":15,"trend":"→"},
    "CLE":{"off_ppg":20.2,"def_ppg":17.8,"rating":67,"off_rank":28,"def_rank":1, "trend":"→"},
    "WSH":{"off_ppg":22.8,"def_ppg":25.5,"rating":66,"off_rank":21,"def_rank":22,"trend":"↑"},
    "MIA":{"off_ppg":23.2,"def_ppg":25.0,"rating":68,"off_rank":19,"def_rank":20,"trend":"↓"},
    "IND":{"off_ppg":23.0,"def_ppg":24.8,"rating":68,"off_rank":20,"def_rank":18,"trend":"→"},
    "NYG":{"off_ppg":21.5,"def_ppg":24.9,"rating":65,"off_rank":25,"def_rank":19,"trend":"↑"},
    "NYJ":{"off_ppg":21.8,"def_ppg":25.2,"rating":65,"off_rank":23,"def_rank":21,"trend":"→"},
    "DAL":{"off_ppg":24.2,"def_ppg":28.9,"rating":63,"off_rank":15,"def_rank":30,"trend":"↓"},
    "TB": {"off_ppg":21.2,"def_ppg":26.0,"rating":63,"off_rank":24,"def_rank":24,"trend":"→"},
    "ATL":{"off_ppg":20.8,"def_ppg":25.8,"rating":62,"off_rank":26,"def_rank":23,"trend":"→"},
    "NO": {"off_ppg":20.5,"def_ppg":26.2,"rating":60,"off_rank":27,"def_rank":25,"trend":"↓"},
    "TEN":{"off_ppg":19.5,"def_ppg":26.5,"rating":57,"off_rank":29,"def_rank":26,"trend":"↓"},
    "ARI":{"off_ppg":18.9,"def_ppg":26.8,"rating":55,"off_rank":30,"def_rank":27,"trend":"→"},
    "CAR":{"off_ppg":18.2,"def_ppg":27.2,"rating":52,"off_rank":31,"def_rank":28,"trend":"→"},
    "LV": {"off_ppg":17.5,"def_ppg":28.0,"rating":50,"off_rank":32,"def_rank":29,"trend":"↓"},
}

INJ_IMPACT = {"QB":9.5,"RB":4.0,"WR":3.5,"TE":3.0,"OT":3.5,"OG":2.5,
              "C":2.5,"DE":4.0,"DT":3.5,"LB":3.5,"CB":4.0,"S":3.0,"K":2.0,"P":1.0}

# ── Helpers ───────────────────────────────────────────────────────────────────
def logo_url(abbr):
    return LOGO.format(abbr.lower())

def ml_fmt(v):
    return f"+{v}" if v > 0 else str(v)

def spread_str(away, home, sp):
    if sp == 0: return "PK"
    return f"{home} -{abs(sp):.1f}" if sp > 0 else f"{away} -{abs(sp):.1f}"

def gc(g):
    return "grA" if g.startswith("A") else "grB" if g.startswith("B") else "grC" if g.startswith("C") else "grD"

def get_season():
    now = datetime.now()
    year = now.year if now.month >= 8 else now.year - 1
    pre  = datetime(year, 8, 1)
    reg  = datetime(year, 9, 9)
    play = datetime(year+1, 1, 16)
    if now < pre:   return year, 1, 1
    if now < reg:   return year, 1, max(1, min((now-pre).days//7+1, 4))
    if now < play:  return year, 2, max(1, min((now-reg).days//7+1, 18))
    return year+1, 3, max(1, min((now-play).days//7+1, 4))

@st.cache_data(ttl=120)
def fetch_schedule(year, stype, week):
    for base in [ESPN_BASE, ESPN_WEB]:
        try:
            url = f"{base}/scoreboard?dates={year}&seasontype={stype}&week={week}&limit=25"
            r = requests.get(url, headers=HDR, timeout=10)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
    return {}

@st.cache_data(ttl=300)
def fetch_injuries(team_id):
    try:
        r = requests.get(f"{ESPN_CORE}/teams/{team_id}/injuries", headers=HDR, timeout=8)
        if r.status_code != 200: return []
        out = []
        for item in r.json().get("items", [])[:8]:
            ref = item.get("$ref","")
            if not ref: continue
            dr = requests.get(ref, headers=HDR, timeout=5)
            if dr.status_code != 200: continue
            d = dr.json()
            status = d.get("status","Questionable")
            ar_url = d.get("athlete",{}).get("$ref","")
            if ar_url:
                ar = requests.get(ar_url, headers=HDR, timeout=5)
                if ar.status_code == 200:
                    ad = ar.json()
                    out.append({"name":ad.get("displayName","?"),
                                "pos":ad.get("position",{}).get("abbreviation","?"),
                                "status":status})
        return out
    except Exception:
        return []

def parse_games(data):
    games = []
    for event in data.get("events", []):
        try:
            comp = event["competitions"][0]
            home = next(c for c in comp["competitors"] if c["homeAway"]=="home")
            away = next(c for c in comp["competitors"] if c["homeAway"]=="away")
            ha, aa = home["team"]["abbreviation"], away["team"]["abbreviation"]
            state = event["status"]["type"]["state"]
            status_txt = event["status"]["type"]["shortDetail"]
            venue = comp.get("venue",{})
            broadcasts = comp.get("broadcasts",[])
            net = ""
            if broadcasts:
                m = broadcasts[0].get("media",{})
                net = m.get("shortName","") or m.get("callLetters","")
            dt_obj = None
            try:
                dt_obj = datetime.fromisoformat(event.get("date","").replace("Z","+00:00"))
            except Exception:
                pass
            games.append({
                "id":       event["id"],
                "ha":ha, "aa":aa,
                "home_id":  home["team"]["id"],
                "away_id":  away["team"]["id"],
                "home_name":home["team"].get("displayName", TEAM_META.get(ha,{}).get("name",ha)),
                "away_name":away["team"].get("displayName", TEAM_META.get(aa,{}).get("name",aa)),
                "hs": home.get("score",""), "as": away.get("score",""),
                "hr": (home.get("records",[{}])[0].get("summary","") if home.get("records") else ""),
                "ar": (away.get("records",[{}])[0].get("summary","") if away.get("records") else ""),
                "state": state, "status": status_txt,
                "net": net,
                "venue": venue.get("fullName","") or TEAM_META.get(ha,{}).get("stadium",""),
                "dt": dt_obj,
            })
        except Exception:
            continue
    return games

def predict(aa, ha, ainj=None, hinj=None):
    ar = RATINGS.get(aa, {"rating":65,"off_ppg":22.0,"def_ppg":24.0})
    hr = RATINGS.get(ha, {"rating":65,"off_ppg":22.0,"def_ppg":24.0})
    ap = ar["off_ppg"]*0.55 + (33-hr["def_ppg"])*0.45
    hp = hr["off_ppg"]*0.55 + (33-ar["def_ppg"])*0.45 + 2.5
    def pen(inj):
        p=0
        for i in (inj or []):
            m={"Out":1.0,"IR":1.0,"Doubtful":0.8,"Questionable":0.4,"Probable":0.1}.get(i.get("status","Q"),0.4)
            p+=INJ_IMPACT.get(i.get("pos","WR"),2.5)*m*0.1
        return p
    ap=max(10,ap-pen(ainj)); hp=max(10,hp-pen(hinj))
    tot=ap+hp
    diff=(hr["rating"]-ar["rating"])+3
    hwp=1/(1+np.exp(-diff/12)); awp=1-hwp
    hml=int(-hwp/(1-hwp)*100) if hwp>0.5 else int((1-hwp)/hwp*100)
    aml=int(-awp/(1-awp)*100) if awp>0.5 else int((1-awp)/awp*100)
    sp=round((hp-ap)/2.5)*0.5
    tl=round(tot*2)/2
    ou="OVER" if tot>tl+0.3 else "UNDER"
    c=abs(diff)
    g="A+" if c>20 else "A" if c>15 else "B+" if c>10 else "B" if c>6 else "C" if c>3 else "D"
    mg="A" if abs(hml)>160 else "B" if abs(hml)>120 else "C" if abs(hml)>105 else "D"
    rg="A" if abs(sp)>=7 else "B" if abs(sp)>=4 else "C" if abs(sp)>=2 else "D"
    return {"ap":round(ap,1),"hp":round(hp,1),"tot":round(tot,1),"tl":tl,"ou":ou,
            "hwp":round(hwp*100,1),"awp":round(awp*100,1),"hml":hml,"aml":aml,"sp":sp,
            "pick":ha if hwp>0.5 else aa,"grade":g,"mg":mg,"rg":rg}

def html(s):
    """Render HTML string safely."""
    st.markdown(s, unsafe_allow_html=True)

def render_game_card(g):
    p = predict(g["aa"], g["ha"])
    ar = RATINGS.get(g["aa"], {})
    hr = RATINGS.get(g["ha"], {})

    # Pre-compute every dynamic value — NO logic inside HTML string
    a_logo   = logo_url(g["aa"])
    h_logo   = logo_url(g["ha"])
    a_name   = g["away_name"]
    h_name   = g["home_name"]
    a_rec    = g["ar"]
    h_rec    = g["hr"]
    state    = g["state"]
    net      = g["net"]
    venue    = g["venue"]

    a_score  = g["as"] if state != "pre" else ""
    h_score  = g["hs"] if state != "pre" else ""
    a_win    = state=="post" and a_score and h_score and int(a_score or 0)>int(h_score or 0)
    h_win    = state=="post" and a_score and h_score and int(h_score or 0)>int(a_score or 0)
    a_sc_cls = "sc win" if a_win else "sc"
    h_sc_cls = "sc win" if h_win else "sc"

    live_html  = '<div class="glv">LIVE</div>' if state=="in" else ""
    final_html = '<div class="gfn">FINAL</div>' if state=="post" else ""
    net_html   = f'<div class="gn">TV: {net}</div>' if net else ""

    # Time display
    time_disp = g["status"]
    if state == "pre" and g["dt"]:
        try:
            local = g["dt"].astimezone()
            time_disp = local.strftime("%-m/%-d · %-I:%M %p")
        except Exception:
            pass

    # Win prob block
    if state != "post":
        wp_html = (f'<div class="wpc">'
                   f'<div style="font-size:9px;color:#555;margin-bottom:4px">WIN PROB</div>'
                   f'<div style="font-size:12px;font-weight:700;color:#6b8fff">{g["aa"]} {p["awp"]}%</div>'
                   f'<div style="font-size:10px;color:#333">vs</div>'
                   f'<div style="font-size:12px;font-weight:700;color:#ff6b6b">{g["ha"]} {p["hwp"]}%</div>'
                   f'</div>')
    else:
        wp_html = ""

    sp     = spread_str(g["aa"], g["ha"], p["sp"])
    ou_col = "#4cff80" if p["ou"]=="OVER" else "#ff6b6b"
    ao     = ml_fmt(p["aml"]); ho = ml_fmt(p["hml"])
    a_off  = ar.get("off_ppg",22)
    h_def  = hr.get("def_ppg",24)

    card = (
        f'<div class="gc">'
        f'<div style="display:flex;align-items:center;gap:12px">'

        # Away row
        f'<div style="flex:1">'
        f'<div class="tr" style="margin-bottom:5px">'
        f'<img src="{a_logo}" class="tl" onerror="this.style.opacity=.3">'
        f'<span class="tn">{a_name}</span>'
        f'<span class="trec">{a_rec}</span>'
        f'<span class="{a_sc_cls}">{a_score}</span>'
        f'</div>'
        # Home row
        f'<div class="tr">'
        f'<img src="{h_logo}" class="tl" onerror="this.style.opacity=.3">'
        f'<span class="tn">{h_name}</span>'
        f'<span class="trec">{h_rec}</span>'
        f'<span class="{h_sc_cls}">{h_score}</span>'
        f'</div>'
        f'</div>'

        # Meta
        f'<div class="gm">'
        f'{live_html}{final_html}'
        f'<div class="gt">{time_disp}</div>'
        f'{net_html}'
        f'<div class="gv">&#127967; {venue}</div>'
        f'</div>'

        # Win prob
        f'{wp_html}'
        f'</div>'

        # Pick strip
        f'<div class="picks">'
        f'<div class="pml"><span class="pl">MONEYLINE</span>'
        f'<div class="gr {gc(p["mg"])}">{p["mg"]}</div>'
        f'<div class="pv">{p["pick"]}</div>'
        f'<div class="ps">{g["aa"]} {ao} | {g["ha"]} {ho}</div></div>'

        f'<div class="psp"><span class="pl">SPREAD</span>'
        f'<div class="gr {gc(p["rg"])}">{p["rg"]}</div>'
        f'<div class="pv">{sp}</div>'
        f'<div class="ps">Proj {p["ap"]}&ndash;{p["hp"]} &middot; margin {abs(p["hp"]-p["ap"]):.1f}pts</div></div>'

        f'<div class="pou"><span class="pl">TOTAL</span>'
        f'<div class="gr {gc(p["grade"])}">{p["grade"]}</div>'
        f'<div class="pv" style="color:{ou_col}">{p["ou"]} {p["tl"]}</div>'
        f'<div class="ps">Proj {p["tot"]} pts &middot; Off {a_off} | Def {h_def} allowed</div></div>'
        f'</div>'
        f'</div>'
    )
    html(card)

# ── Header ────────────────────────────────────────────────────────────────────
sy, stype, cur_wk = get_season()
phase_label = {1:"Preseason",2:"Regular Season",3:"Playoffs"}.get(stype,"Season")

html(f'''<div class="nfl-hdr">
  <div>
    <div class="logo">&#127944; <span class="n">NFL</span><span class="p">+</span> PREDICTOR
      <span class="badge">LIVE</span></div>
    <div class="stag">{sy}&ndash;{str(sy+1)[2:]} NFL Season &middot; ESPN API &middot; Picks Auto-Update Each Week</div>
  </div>
  <div style="text-align:right;font-size:11px;color:#555">
    {phase_label} &middot; Week {cur_wk}<br>
    <span class="ldot">&#11044; Auto-tracking season</span>
  </div>
</div>''')

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📅  Live Schedule & Picks", "🔍  Matchup Analyzer", "📊  Power Rankings"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1,c2,c3,c4 = st.columns([2,2,2,1])
    phase_map = {"Preseason (Aug)":1,"Regular Season":2,"Playoffs":3}
    phase_def = {1:"Preseason (Aug)",2:"Regular Season",3:"Playoffs"}.get(stype,"Regular Season")
    with c1:
        sel_phase = st.selectbox("Season Phase", list(phase_map.keys()),
                                 index=list(phase_map.keys()).index(phase_def))
    with c2:
        max_wk = {1:4,2:18,3:4}.get(phase_map[sel_phase],18)
        default_wk = cur_wk if phase_map[sel_phase]==stype else 1
        sel_wk = st.slider("Week", 1, max_wk, min(default_wk, max_wk))
    with c3:
        sel_yr = st.selectbox("Season Year", [sy, sy-1], index=0)
    with c4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("↻ Refresh"):
            st.cache_data.clear()

    with st.spinner(f"Fetching Week {sel_wk} from ESPN…"):
        raw = fetch_schedule(sel_yr, phase_map[sel_phase], sel_wk)
    games = parse_games(raw)

    season_name = raw.get("season",{}).get("displayName", f"{sel_yr} NFL")
    week_txt    = raw.get("week",{}).get("text", f"Week {sel_wk}")
    live_ct  = sum(1 for g in games if g["state"]=="in")
    final_ct = sum(1 for g in games if g["state"]=="post")
    pre_ct   = sum(1 for g in games if g["state"]=="pre")

    live_span = f'<span style="color:#ff4444;font-weight:700">&#11044; {live_ct} Live</span>' if live_ct else ""
    html(f'<div class="sb"><b style="color:#aaa">&#128225; ESPN Live Feed</b>'
         f'&nbsp;&middot;&nbsp;{len(games)} games &middot; {season_name}'
         f'&nbsp;&middot;&nbsp;{live_span}'
         f'&nbsp;<span style="color:#555">{final_ct} Final &middot; {pre_ct} Upcoming</span></div>')

    if not games:
        html('<div style="background:#161616;border:1px solid #222;border-radius:10px;'
             'padding:40px;text-align:center;color:#444;font-size:14px;margin-top:20px">'
             'No games found. ESPN may not have posted this week yet — try a different week or phase.</div>')
    else:
        html(f'<div class="sh">{week_txt} &middot; {len(games)} Games</div>')
        for g in games:
            render_game_card(g)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MATCHUP ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    abbrs = sorted(TEAM_META.keys())
    names = [TEAM_META[a]["name"] for a in abbrs]

    ca, cb, cc = st.columns([2,0.4,2])
    with ca:
        html('<div style="font-size:10px;color:#555;margin-bottom:4px">AWAY TEAM</div>')
        away_sel = st.selectbox("Away",names,index=names.index("New England Patriots"),
                                label_visibility="collapsed")
    with cb:
        html('<div style="text-align:center;font-size:22px;font-weight:900;color:#333;padding-top:22px">@</div>')
    with cc:
        html('<div style="font-size:10px;color:#555;margin-bottom:4px">HOME TEAM</div>')
        home_sel = st.selectbox("Home",names,index=names.index("Seattle Seahawks"),
                                label_visibility="collapsed")

    aa2 = abbrs[names.index(away_sel)]
    ha2 = abbrs[names.index(home_sel)]

    if aa2 == ha2:
        st.warning("Pick two different teams.")
        st.stop()

    d1,d2,d3 = st.columns([1,2,1])
    with d2:
        do_inj = st.button("🔍  Fetch Live Injuries & Analyze", use_container_width=True)

    ainj = hinj = []
    if do_inj:
        with st.spinner("Pulling injury data from ESPN…"):
            ainj = fetch_injuries(TEAM_META[aa2].get("id",""))
            hinj = fetch_injuries(TEAM_META[ha2].get("id",""))

    p2   = predict(aa2, ha2, ainj, hinj)
    hm   = TEAM_META.get(ha2,{})
    ar2  = RATINGS.get(aa2,{})
    hr2  = RATINGS.get(ha2,{})

    # Pre-compute everything
    a_logo2  = logo_url(aa2); h_logo2 = logo_url(ha2)
    sp2      = spread_str(aa2, ha2, p2["sp"])
    ou_col2  = "#4cff80" if p2["ou"]=="OVER" else "#ff6b6b"
    ao2      = ml_fmt(p2["aml"]); ho2 = ml_fmt(p2["hml"])
    cap_fmt  = f'{hm.get("cap",0):,}'

    html(f'''<div class="gc" style="padding:20px 24px;margin-top:8px">
<div style="display:flex;align-items:center">
  <div style="flex:1;text-align:center">
    <img src="{a_logo2}" style="width:72px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))" onerror="this.style.opacity=.3">
    <div style="font-size:13px;font-weight:700;color:#aaa;margin-top:8px">{away_sel}</div>
    <div style="font-size:30px;font-weight:900;color:#fff">{p2["awp"]}%</div>
    <div style="font-size:10px;color:#555">Win Probability</div>
    <div style="font-size:12px;color:#6b8fff;font-weight:700;margin-top:4px">
      Proj {p2["ap"]} pts &nbsp;&middot;&nbsp; ML {ao2}
    </div>
  </div>
  <div style="flex:0 0 140px;text-align:center">
    <div style="font-size:10px;color:#333">2026 NFL SEASON</div>
    <div style="font-size:20px;font-weight:900;color:#222;margin:4px 0">@</div>
    <div style="font-size:15px;font-weight:800;color:#fff">{p2["ap"]} &ndash; {p2["hp"]}</div>
    <div style="font-size:10px;color:#555">Projected Final</div>
    <div style="display:inline-block;background:#1a2e1a;color:#4cff80;font-size:10px;
      font-weight:700;padding:3px 10px;border-radius:12px;margin-top:6px">O/U {p2["tl"]}</div>
  </div>
  <div style="flex:1;text-align:center">
    <img src="{h_logo2}" style="width:72px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))" onerror="this.style.opacity=.3">
    <div style="font-size:13px;font-weight:700;color:#aaa;margin-top:8px">{home_sel}</div>
    <div style="font-size:30px;font-weight:900;color:#fff">{p2["hwp"]}%</div>
    <div style="font-size:10px;color:#555">Win Probability</div>
    <div style="font-size:12px;color:#ff6b6b;font-weight:700;margin-top:4px">
      Proj {p2["hp"]} pts &nbsp;&middot;&nbsp; ML {ho2}
    </div>
  </div>
</div>
<div style="background:#161616;border:1px solid #1e1e1e;border-radius:7px;
  padding:8px 16px;margin:14px 0;font-size:11px;color:#777;display:flex;flex-wrap:wrap;gap:6px 18px">
  <span>&#127967; <b style="color:#bbb">{hm.get("stadium","")}</b></span>
  <span>&#128205; {hm.get("loc","")}</span>
  <span>&#127968; Cap. {cap_fmt}</span>
  <span>&#127807; {hm.get("surf","")}</span>
  <span>&#11036; {hm.get("roof","")}</span>
</div>
<div class="picks">
  <div class="pml"><span class="pl">MONEYLINE</span>
    <div class="gr {gc(p2["mg"])}">{p2["mg"]}</div>
    <div class="pv">{p2["pick"]}</div>
    <div class="ps">{aa2} {ao2} | {ha2} {ho2}<br>{aa2} {p2["awp"]}% / {ha2} {p2["hwp"]}%</div>
  </div>
  <div class="psp"><span class="pl">SPREAD</span>
    <div class="gr {gc(p2["rg"])}">{p2["rg"]}</div>
    <div class="pv">{sp2}</div>
    <div class="ps">Proj {aa2} {p2["ap"]} &ndash; {ha2} {p2["hp"]}<br>
      Margin {abs(p2["hp"]-p2["ap"]):.1f} pts</div>
  </div>
  <div class="pou"><span class="pl">TOTAL POINTS</span>
    <div class="gr {gc(p2["grade"])}">{p2["grade"]}</div>
    <div class="pv" style="color:{ou_col2}">{p2["ou"]} {p2["tl"]}</div>
    <div class="ps">Proj {p2["tot"]} pts total<br>
      Off {ar2.get("off_ppg",22)} | Def {hr2.get("def_ppg",24)} allowed</div>
  </div>
</div>
</div>''')

    # Stats + Injuries
    html('<div class="sh">Team Comparison</div>')
    s1, s2 = st.columns(2)

    with s1:
        rows = [
            ("Power Rating",      ar2.get("rating","–"),   hr2.get("rating","–")),
            ("Off PPG",           ar2.get("off_ppg","–"),  hr2.get("off_ppg","–")),
            ("Def PPG Allowed",   ar2.get("def_ppg","–"),  hr2.get("def_ppg","–")),
            ("Offense Rank",      f'#{ar2.get("off_rank","–")}', f'#{hr2.get("off_rank","–")}'),
            ("Defense Rank",      f'#{ar2.get("def_rank","–")}', f'#{hr2.get("def_rank","–")}'),
            ("2026 Trend",        ar2.get("trend","→"),    hr2.get("trend","→")),
        ]
        rows_html = "".join(
            f'<div style="display:flex;justify-content:space-between;padding:5px 0;'
            f'border-bottom:1px solid #111;font-size:12px">'
            f'<span style="color:#555">{lbl}</span>'
            f'<span style="color:#6b8fff;font-weight:700">{av}</span>'
            f'<span style="color:#ff6b6b;font-weight:700">{hv}</span></div>'
            for lbl,av,hv in rows
        )
        html(f'<div style="background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:14px 16px">'
             f'<div style="display:flex;justify-content:space-between;font-size:10px;font-weight:700;'
             f'padding-bottom:6px;border-bottom:1px solid #1e1e1e;margin-bottom:4px">'
             f'<span style="color:#444">STAT</span>'
             f'<span style="color:#6b8fff">{aa2}</span>'
             f'<span style="color:#ff6b6b">{ha2}</span></div>'
             f'{rows_html}</div>')

    with s2:
        html('<div style="font-size:10px;color:#555;font-weight:700;margin-bottom:6px">INJURY REPORT</div>')
        if ainj or hinj:
            for inj in (ainj or []):
                html(f'<div style="background:#161616;border:1px solid #222;border-radius:6px;'
                     f'padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center">'
                     f'<div><span style="font-size:12px;font-weight:700;color:#fff">{inj["name"]}</span>'
                     f'<span style="font-size:10px;color:#555;margin-left:8px">{inj["pos"]} &middot; {aa2}</span></div>'
                     f'<span style="font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;'
                     f'background:#3d2e10;color:#ffc84c">{inj["status"]}</span></div>')
            for inj in (hinj or []):
                html(f'<div style="background:#161616;border:1px solid #222;border-radius:6px;'
                     f'padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center">'
                     f'<div><span style="font-size:12px;font-weight:700;color:#fff">{inj["name"]}</span>'
                     f'<span style="font-size:10px;color:#555;margin-left:8px">{inj["pos"]} &middot; {ha2}</span></div>'
                     f'<span style="font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;'
                     f'background:#3d2e10;color:#ffc84c">{inj["status"]}</span></div>')
        else:
            html('<div style="background:#161616;border:1px solid #222;border-radius:8px;'
                 'padding:24px;text-align:center;color:#444;font-size:12px">'
                 'Click <b style="color:#888">Fetch Live Injuries</b> to pull ESPN injury data</div>')

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — POWER RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    html('<div class="sh">2026 Preseason Power Ratings &middot; All 32 Teams</div>')
    for rank, (abbr, r) in enumerate(sorted(RATINGS.items(), key=lambda x:x[1]["rating"], reverse=True), 1):
        meta = TEAM_META.get(abbr,{})
        tc = "#4cff80" if r["trend"]=="↑" else "#ff6b6b" if r["trend"]=="↓" else "#555"
        html(f'<div style="display:flex;align-items:center;gap:10px;padding:7px 12px;'
             f'background:#111;border:1px solid #1a1a1a;border-radius:7px;margin-bottom:3px">'
             f'<div style="width:24px;text-align:center;font-size:11px;font-weight:700;color:#333">#{rank}</div>'
             f'<img src="{logo_url(abbr)}" style="width:26px;height:26px;object-fit:contain" onerror="this.style.opacity=.2">'
             f'<div style="flex:1;min-width:0">'
             f'<div style="font-size:12px;font-weight:700;color:#ccc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{meta.get("name",abbr)}</div>'
             f'<div style="font-size:9px;color:#333">{meta.get("stadium","")}</div></div>'
             f'<div style="min-width:44px;text-align:center"><div style="font-size:8px;color:#333">OFF</div>'
             f'<div style="font-size:12px;font-weight:700;color:#6b8fff">{r["off_ppg"]}</div></div>'
             f'<div style="min-width:44px;text-align:center"><div style="font-size:8px;color:#333">DEF</div>'
             f'<div style="font-size:12px;font-weight:700;color:#ff6b6b">{r["def_ppg"]}</div></div>'
             f'<div style="min-width:36px;text-align:center"><div style="font-size:8px;color:#333">RTG</div>'
             f'<div style="font-size:15px;font-weight:900;color:#fff">{r["rating"]}</div></div>'
             f'<div style="font-size:16px;color:{tc};min-width:18px">{r["trend"]}</div>'
             f'<div style="min-width:70px;background:#1a1a1a;border-radius:3px;height:4px;overflow:hidden">'
             f'<div style="width:{r["rating"]}%;background:linear-gradient(90deg,#013369,#d50a0a);height:100%"></div></div>'
             f'</div>')

    html('<div style="margin-top:14px;padding:10px 14px;background:#111;border:1px solid #1e1e1e;'
         'border-radius:7px;font-size:10px;color:#444">'
         'Data: ESPN API (live) &middot; 2025 final stats &middot; 2026 preseason rankings. For entertainment only.</div>')
