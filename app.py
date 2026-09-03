import streamlit as st
import requests
import numpy as np
from datetime import datetime

st.set_page_config(page_title="NFL Plus · Predictions", page_icon="🏈",
                   layout="wide", initial_sidebar_state="collapsed")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & base ── */
*{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{
  font-family:'Inter',sans-serif;
  background:#0a0c10;
  color:#e8eaf0;
  -webkit-font-smoothing:antialiased;
}
.stApp{background:#0a0c10}
footer,#MainMenu,header{display:none!important;visibility:hidden!important}
section[data-testid="stSidebar"]{display:none}
div[data-testid="stToolbar"]{display:none}

/* ── Top nav bar ── */
.topbar{
  position:sticky;top:0;z-index:100;
  background:#0d1117;
  border-bottom:1px solid #1c2130;
  padding:0 28px;
  display:flex;align-items:center;justify-content:space-between;
  height:56px;
  margin:-1rem -1rem 0;
}
.brand{display:flex;align-items:center;gap:10px}
.brand-icon{
  width:34px;height:34px;border-radius:8px;
  background:linear-gradient(135deg,#013369 0%,#d50a0a 100%);
  display:flex;align-items:center;justify-content:center;
  font-size:18px;font-weight:900;color:#fff;
  font-family:'Oswald',sans-serif;letter-spacing:-1px;
}
.brand-name{
  font-family:'Oswald',sans-serif;font-size:20px;
  font-weight:700;letter-spacing:.5px;color:#fff;
}
.brand-name span{color:#d50a0a}
.brand-tag{
  font-size:9px;font-weight:700;letter-spacing:1.5px;
  color:#4cffaa;text-transform:uppercase;
  background:#0a2218;border:1px solid #0d4030;
  border-radius:4px;padding:2px 7px;margin-left:8px;
}
.nav-right{display:flex;align-items:center;gap:16px}
.nav-item{font-size:11px;color:#5a6480;font-weight:500;cursor:pointer}
.nav-season{
  font-size:11px;font-weight:700;color:#7b8aaa;
  background:#141c2e;border:1px solid #1c2a42;
  border-radius:20px;padding:4px 12px;
}
.live-badge{
  display:flex;align-items:center;gap:5px;
  font-size:10px;font-weight:700;color:#ff3b3b;
  background:#1a0808;border:1px solid #3d1010;
  border-radius:20px;padding:4px 10px;
  letter-spacing:.5px;
}
.live-dot{
  width:6px;height:6px;border-radius:50%;background:#ff3b3b;
  animation:blink 1.2s ease-in-out infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}

/* ── Week selector strip ── */
.week-strip{
  background:#0d1117;
  border-bottom:1px solid #1c2130;
  padding:0 28px;margin:0 -1rem;
  display:flex;align-items:center;gap:0;
  overflow-x:auto;scrollbar-width:none;
}
.week-strip::-webkit-scrollbar{display:none}
.week-tab{
  padding:12px 18px;font-size:12px;font-weight:600;
  color:#4a556e;cursor:pointer;white-space:nowrap;
  border-bottom:2px solid transparent;
  transition:.15s;
}
.week-tab:hover{color:#8a96b4}
.week-tab.active{color:#fff;border-bottom:2px solid #d50a0a}

/* ── Page layout ── */
.page{padding:24px 0}
.section-title{
  font-family:'Oswald',sans-serif;
  font-size:13px;font-weight:600;letter-spacing:2px;
  text-transform:uppercase;color:#3a4460;
  margin:0 0 14px;
  display:flex;align-items:center;gap:10px;
}
.section-title::after{content:'';flex:1;height:1px;background:#141c2e}

/* ── Status pill bar ── */
.status-row{
  display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;
}
.stat-pill{
  background:#0d1117;border:1px solid #1c2130;
  border-radius:8px;padding:8px 14px;
  display:flex;align-items:center;gap:8px;
}
.stat-pill-val{font-size:18px;font-weight:800;color:#fff}
.stat-pill-lbl{font-size:10px;color:#3a4460;font-weight:500}
.stat-pill-live .stat-pill-val{color:#4cffaa}

/* ── Game card ── */
.gcard{
  background:#0d1117;
  border:1px solid #1c2130;
  border-radius:12px;
  margin-bottom:10px;
  overflow:hidden;
  transition:border-color .2s;
}
.gcard:hover{border-color:#2a3550}
.gcard-inner{padding:16px 20px}

/* Team rows */
.team-section{flex:1;min-width:0}
.team-row{
  display:flex;align-items:center;gap:12px;
  padding:6px 0;
}
.team-row+.team-row{border-top:1px solid #0f1520}
.team-logo{
  width:36px;height:36px;object-fit:contain;
  filter:drop-shadow(0 1px 4px rgba(0,0,0,.5));
  flex-shrink:0;
}
.team-info{flex:1;min-width:0}
.team-name{
  font-size:14px;font-weight:700;color:#d8dde8;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.team-record{font-size:11px;color:#2e3850;font-weight:500;margin-top:1px}
.team-score{
  font-family:'Oswald',sans-serif;
  font-size:26px;font-weight:700;color:#fff;
  min-width:36px;text-align:right;
}
.team-score.win{color:#4cffaa}
.team-score.lose{color:#4a5570}

/* Center meta col */
.game-center{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:0 20px;min-width:120px;
}
.game-status-live{
  font-size:10px;font-weight:700;color:#ff3b3b;
  letter-spacing:1px;margin-bottom:4px;
}
.game-status-final{font-size:10px;color:#2e3850;font-weight:600;letter-spacing:1px;margin-bottom:4px}
.game-status-pre{font-size:10px;color:#4a5570;font-weight:500;margin-bottom:4px}
.game-time{font-size:13px;font-weight:700;color:#7b8aaa;margin-bottom:2px}
.game-network{
  font-size:10px;color:#3a4460;background:#0f1520;
  border:1px solid #1c2130;border-radius:4px;padding:2px 7px;margin-bottom:4px;
}
.game-venue{font-size:10px;color:#2e3850;text-align:center;margin-top:2px}
.game-at{font-family:'Oswald',sans-serif;font-size:16px;color:#1c2540;font-weight:700}

/* Win probability bar */
.wp-section{
  display:flex;flex-direction:column;align-items:center;
  min-width:90px;padding:0 12px;
}
.wp-label{font-size:9px;color:#2e3850;font-weight:600;letter-spacing:.8px;margin-bottom:6px}
.wp-bar-wrap{
  width:100%;height:6px;background:#141c2e;
  border-radius:3px;overflow:hidden;margin-bottom:6px;
}
.wp-bar-fill{height:100%;border-radius:3px}
.wp-teams{
  width:100%;display:flex;justify-content:space-between;
}
.wp-away{font-size:11px;font-weight:700;color:#7b8aaa}
.wp-home{font-size:11px;font-weight:700;color:#fff}

/* Odds strip */
.odds-strip{
  display:flex;border-top:1px solid #0f1520;
  background:#080c14;
}
.odds-cell{
  flex:1;padding:10px 14px;
  border-right:1px solid #0f1520;
  cursor:pointer;transition:background .15s;
}
.odds-cell:last-child{border-right:none}
.odds-cell:hover{background:#0d1520}
.odds-type{
  font-size:9px;font-weight:700;color:#2e3850;
  letter-spacing:1px;text-transform:uppercase;margin-bottom:5px;
}
.odds-main{
  font-family:'Oswald',sans-serif;
  font-size:17px;font-weight:600;color:#fff;margin-bottom:2px;
}
.odds-main.over{color:#4cffaa}
.odds-main.under{color:#ff6b6b}
.odds-sub{font-size:10px;color:#3a4460}
.odds-grade{
  float:right;width:20px;height:20px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-size:8px;font-weight:800;margin-top:-2px;
}
.gA{background:#0d2a1a;color:#4cffaa;border:1px solid #1a5a30}
.gAp{background:#0d2a1a;color:#4cffaa;border:1px solid #1a5a30}
.gBp{background:#0d1a2e;color:#5aa8ff;border:1px solid #1a3d6a}
.gB{background:#0d1a2e;color:#5aa8ff;border:1px solid #1a3d6a}
.gC{background:#201e0a;color:#ffc840;border:1px solid #4a4010}
.gD{background:#200a0a;color:#ff6b40;border:1px solid #4a1010}

/* ── Matchup analyzer ── */
.analyzer-hero{
  background:#0d1117;border:1px solid #1c2130;
  border-radius:12px;overflow:hidden;
  margin-bottom:16px;
}
.analyzer-header{
  background:#080c14;border-bottom:1px solid #1c2130;
  padding:14px 20px;
  display:flex;align-items:center;justify-content:space-between;
}
.analyzer-title{
  font-family:'Oswald',sans-serif;font-size:12px;
  font-weight:600;letter-spacing:2px;color:#3a4460;text-transform:uppercase;
}
.analyzer-body{padding:24px 28px}
.matchup-row{
  display:flex;align-items:center;justify-content:space-between;gap:20px;
}
.matchup-team{flex:1;text-align:center}
.matchup-logo{width:80px;height:80px;object-fit:contain;margin:0 auto 10px}
.matchup-name{font-size:14px;font-weight:700;color:#7b8aaa;margin-bottom:4px}
.matchup-wp{
  font-family:'Oswald',sans-serif;font-size:42px;font-weight:700;color:#fff;
  line-height:1;margin-bottom:4px;
}
.matchup-wp-sub{font-size:10px;color:#2e3850;font-weight:500}
.matchup-proj{
  font-size:13px;font-weight:600;color:#5aa8ff;
  margin-top:8px;
}
.matchup-ml{font-size:12px;color:#3a4460;margin-top:3px}
.matchup-vs{
  display:flex;flex-direction:column;align-items:center;gap:6px;
}
.vs-label{
  font-family:'Oswald',sans-serif;font-size:22px;
  font-weight:700;color:#1c2540;
}
.proj-score{
  background:#080c14;border:1px solid #1c2130;
  border-radius:8px;padding:8px 16px;text-align:center;
}
.proj-score-num{
  font-family:'Oswald',sans-serif;font-size:20px;
  font-weight:700;color:#fff;
}
.proj-score-lbl{font-size:9px;color:#2e3850;margin-top:2px}
.ou-line{
  background:#0d2216;border:1px solid #1a4028;
  border-radius:20px;padding:4px 12px;
  font-size:11px;font-weight:700;color:#4cffaa;
}

/* Odds cards */
.odds-cards{display:flex;gap:10px;padding:0 28px 20px}
.ocard{
  flex:1;background:#080c14;border:1px solid #1c2130;
  border-radius:10px;padding:14px 16px;
}
.ocard-type{
  font-size:9px;font-weight:700;letter-spacing:1.5px;
  text-transform:uppercase;color:#2e3850;margin-bottom:10px;
}
.ocard-pick{font-size:16px;font-weight:800;color:#fff;margin-bottom:4px}
.ocard-pick.green{color:#4cffaa}.ocard-pick.red{color:#ff6b6b}
.ocard-odds{font-size:12px;color:#3a4460;margin-bottom:8px}
.ocard-sub{font-size:10px;color:#2a3450;line-height:1.6}
.ocard-grade{
  width:28px;height:28px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:10px;font-weight:800;float:right;margin-top:-4px;
}

/* Stadium card */
.stadium-card{
  background:#080c14;border:1px solid #1c2130;
  border-radius:10px;padding:14px 18px;margin:0 28px 20px;
  display:flex;align-items:center;gap:20px;flex-wrap:wrap;
}
.stadium-name{font-size:14px;font-weight:700;color:#7b8aaa}
.stadium-meta{display:flex;gap:20px;flex-wrap:wrap}
.smeta{font-size:11px;color:#2e3850;display:flex;align-items:center;gap:5px}
.smeta b{color:#4a5570}

/* Stats table */
.stat-table{
  background:#0d1117;border:1px solid #1c2130;
  border-radius:10px;overflow:hidden;
}
.stat-thead{
  background:#080c14;border-bottom:1px solid #1c2130;
  display:flex;padding:9px 16px;
  font-size:9px;font-weight:700;color:#2e3850;letter-spacing:1px;text-transform:uppercase;
}
.stat-thead .sc{flex:1;text-align:right}
.stat-thead .sc:first-child{text-align:left;color:#3a4460}
.stat-row-d{
  display:flex;align-items:center;padding:10px 16px;
  border-bottom:1px solid #0a0e18;
  transition:background .1s;
}
.stat-row-d:hover{background:#0a0e18}
.stat-row-d:last-child{border-bottom:none}
.stat-lbl{flex:1.5;font-size:12px;color:#4a5570;font-weight:500}
.stat-away{flex:1;text-align:right;font-size:13px;font-weight:700;color:#5aa8ff}
.stat-home{flex:1;text-align:right;font-size:13px;font-weight:700;color:#ff6b6b}
.stat-bar-wrap{flex:2;height:4px;background:#0f1520;border-radius:2px;margin:0 12px;position:relative}
.stat-bar-a{position:absolute;right:50%;top:0;height:100%;background:#5aa8ff;border-radius:2px}
.stat-bar-h{position:absolute;left:50%;top:0;height:100%;background:#ff6b6b;border-radius:2px}

/* Injury list */
.inj-list{background:#0d1117;border:1px solid #1c2130;border-radius:10px;overflow:hidden}
.inj-row{
  display:flex;align-items:center;gap:12px;
  padding:10px 16px;border-bottom:1px solid #0a0e18;
}
.inj-row:last-child{border-bottom:none}
.inj-pos-badge{
  width:28px;height:28px;border-radius:6px;
  background:#141c2e;border:1px solid #1c2a42;
  display:flex;align-items:center;justify-content:center;
  font-size:9px;font-weight:800;color:#4a5570;flex-shrink:0;
}
.inj-name{font-size:13px;font-weight:700;color:#c8cfe0;flex:1}
.inj-team{font-size:10px;color:#2e3850;margin-top:1px}
.inj-status{
  font-size:9px;font-weight:700;padding:3px 9px;border-radius:4px;
  letter-spacing:.5px;text-transform:uppercase;
}
.s-out{background:#1a0808;color:#ff4444;border:1px solid #3d1010}
.s-d{background:#1a0a04;color:#ff8844;border:1px solid #3d1e08}
.s-q{background:#1a1600;color:#ffc040;border:1px solid #3d3200}
.s-p{background:#0a1a0a;color:#44cc44;border:1px solid #1a3d1a}

/* Rankings table */
.rank-row{
  display:flex;align-items:center;gap:12px;
  padding:10px 16px;border-bottom:1px solid #0a0e18;
  background:#0d1117;border-radius:0;transition:background .1s;
}
.rank-row:hover{background:#0f1420}
.rank-row:first-child{border-radius:10px 10px 0 0}
.rank-row:last-child{border-bottom:none;border-radius:0 0 10px 10px}
.rank-num{
  width:28px;font-family:'Oswald',sans-serif;
  font-size:15px;font-weight:700;color:#1c2540;text-align:center;
}
.rank-logo{width:32px;height:32px;object-fit:contain;flex-shrink:0}
.rank-info{flex:1;min-width:0}
.rank-name{font-size:13px;font-weight:700;color:#c8cfe0}
.rank-sub{font-size:10px;color:#2e3850;margin-top:1px}
.rank-stat{min-width:48px;text-align:right}
.rank-stat-val{font-size:13px;font-weight:700}
.rank-stat-lbl{font-size:9px;color:#2e3850;margin-top:1px}
.rank-diff{
  min-width:44px;text-align:right;
  font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;
}
.rank-bar{min-width:80px;height:4px;background:#0f1520;border-radius:2px;overflow:hidden}
.rank-bar-fill{height:100%;border-radius:2px}
.trend-up{color:#4cffaa}.trend-dn{color:#ff4444}.trend-eq{color:#3a4460}

/* Streamlit overrides */
.stSelectbox>div>div{
  background:#0d1117!important;border:1px solid #1c2130!important;
  color:#c8cfe0!important;border-radius:8px!important;
}
.stSlider [data-baseweb="slider"]{padding:0 4px}
div.stButton>button{
  background:#013369;color:#fff;border:none;border-radius:8px;
  font-weight:700;font-size:13px;padding:10px 24px;
  letter-spacing:.3px;transition:.15s;
}
div.stButton>button:hover{background:#0050a0;transform:translateY(-1px)}
.stTabs [data-baseweb="tab-list"]{
  background:#0d1117;border-radius:0;padding:0;border:none;
  border-bottom:1px solid #1c2130;gap:0;
}
.stTabs [data-baseweb="tab"]{
  color:#3a4460;font-weight:600;font-size:13px;
  padding:14px 22px;border-bottom:2px solid transparent;
  border-radius:0!important;background:none!important;
}
.stTabs [aria-selected="true"]{
  color:#fff!important;border-bottom:2px solid #d50a0a!important;
  background:none!important;border-radius:0!important;
}
.stTabs [data-baseweb="tab-panel"]{padding:24px 0 0}
.stSelectbox label,.stSlider label{color:#3a4460!important;font-size:11px!important;font-weight:600!important;letter-spacing:.5px!important}
div[data-testid="stHorizontalBlock"]{gap:10px}
.stSpinner>div{border-top-color:#d50a0a!important}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ESPN      = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_WEB  = "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
HDR = {"User-Agent":"Mozilla/5.0 (compatible; NFLPlus/2.0)"}
LOGO = "https://a.espncdn.com/i/teamlogos/nfl/500/{}.png"

FALLBACK = {
  "ARI":{"off":18.9,"def":26.8,"ydg_off":320,"ydg_def":378,"to_diff":-8,"win_pct":.41,"streak":0,"sos":.48},
  "ATL":{"off":20.8,"def":25.8,"ydg_off":331,"ydg_def":362,"to_diff":-4,"win_pct":.53,"streak":1,"sos":.50},
  "BAL":{"off":24.8,"def":21.2,"ydg_off":358,"ydg_def":318,"to_diff":5,"win_pct":.59,"streak":1,"sos":.52},
  "BUF":{"off":28.2,"def":21.5,"ydg_off":381,"ydg_def":322,"to_diff":7,"win_pct":.65,"streak":2,"sos":.51},
  "CAR":{"off":18.2,"def":27.2,"ydg_off":305,"ydg_def":385,"to_diff":-11,"win_pct":.29,"streak":-3,"sos":.47},
  "CHI":{"off":27.8,"def":22.0,"ydg_off":372,"ydg_def":330,"to_diff":4,"win_pct":.59,"streak":2,"sos":.50},
  "CIN":{"off":24.0,"def":24.5,"ydg_off":352,"ydg_def":348,"to_diff":1,"win_pct":.53,"streak":0,"sos":.50},
  "CLE":{"off":20.2,"def":17.8,"ydg_off":298,"ydg_def":282,"to_diff":2,"win_pct":.53,"streak":1,"sos":.49},
  "DAL":{"off":24.2,"def":28.9,"ydg_off":355,"ydg_def":398,"to_diff":-6,"win_pct":.47,"streak":-2,"sos":.51},
  "DEN":{"off":26.1,"def":18.9,"ydg_off":362,"ydg_def":290,"to_diff":8,"win_pct":.65,"streak":3,"sos":.52},
  "DET":{"off":28.3,"def":24.2,"ydg_off":385,"ydg_def":345,"to_diff":5,"win_pct":.65,"streak":2,"sos":.51},
  "GB": {"off":23.5,"def":23.0,"ydg_off":345,"ydg_def":335,"to_diff":3,"win_pct":.59,"streak":1,"sos":.50},
  "HOU":{"off":25.8,"def":18.4,"ydg_off":360,"ydg_def":288,"to_diff":9,"win_pct":.65,"streak":3,"sos":.53},
  "IND":{"off":23.0,"def":24.8,"ydg_off":340,"ydg_def":352,"to_diff":0,"win_pct":.47,"streak":0,"sos":.49},
  "JAX":{"off":25.5,"def":19.2,"ydg_off":358,"ydg_def":295,"to_diff":6,"win_pct":.59,"streak":2,"sos":.50},
  "KC": {"off":26.4,"def":22.8,"ydg_off":365,"ydg_def":332,"to_diff":5,"win_pct":.59,"streak":1,"sos":.52},
  "LV": {"off":17.5,"def":28.0,"ydg_off":295,"ydg_def":390,"to_diff":-12,"win_pct":.29,"streak":-4,"sos":.48},
  "LAC":{"off":25.1,"def":22.5,"ydg_off":355,"ydg_def":330,"to_diff":4,"win_pct":.59,"streak":1,"sos":.50},
  "LAR":{"off":31.2,"def":22.4,"ydg_off":398,"ydg_def":328,"to_diff":8,"win_pct":.65,"streak":3,"sos":.51},
  "MIA":{"off":23.2,"def":25.0,"ydg_off":342,"ydg_def":355,"to_diff":-2,"win_pct":.47,"streak":-1,"sos":.50},
  "MIN":{"off":23.8,"def":21.0,"ydg_off":348,"ydg_def":315,"to_diff":4,"win_pct":.59,"streak":1,"sos":.49},
  "NE": {"off":27.0,"def":20.8,"ydg_off":368,"ydg_def":312,"to_diff":6,"win_pct":.65,"streak":4,"sos":.53},
  "NO": {"off":20.5,"def":26.2,"ydg_off":325,"ydg_def":368,"to_diff":-5,"win_pct":.41,"streak":-1,"sos":.49},
  "NYG":{"off":21.5,"def":24.9,"ydg_off":330,"ydg_def":355,"to_diff":-3,"win_pct":.47,"streak":0,"sos":.50},
  "NYJ":{"off":21.8,"def":25.2,"ydg_off":332,"ydg_def":358,"to_diff":-4,"win_pct":.41,"streak":-1,"sos":.49},
  "PHI":{"off":27.9,"def":20.1,"ydg_off":375,"ydg_def":305,"to_diff":7,"win_pct":.65,"streak":2,"sos":.52},
  "PIT":{"off":22.5,"def":23.5,"ydg_off":338,"ydg_def":342,"to_diff":2,"win_pct":.53,"streak":0,"sos":.50},
  "SF": {"off":24.9,"def":23.1,"ydg_off":355,"ydg_def":338,"to_diff":4,"win_pct":.59,"streak":1,"sos":.51},
  "SEA":{"off":29.1,"def":20.2,"ydg_off":388,"ydg_def":308,"to_diff":9,"win_pct":.71,"streak":5,"sos":.53},
  "TB": {"off":21.2,"def":26.0,"ydg_off":328,"ydg_def":365,"to_diff":-3,"win_pct":.47,"streak":-1,"sos":.49},
  "TEN":{"off":19.5,"def":26.5,"ydg_off":312,"ydg_def":372,"to_diff":-9,"win_pct":.35,"streak":-3,"sos":.47},
  "WSH":{"off":22.8,"def":25.5,"ydg_off":338,"ydg_def":360,"to_diff":-2,"win_pct":.47,"streak":0,"sos":.50},
}

TEAM_META = {
  "ARI":{"name":"Arizona Cardinals",    "city":"Arizona",       "stadium":"State Farm Stadium",      "cap":63400,"surf":"Grass",    "loc":"Glendale, AZ",       "roof":"Retractable","id":"22","dome":False},
  "ATL":{"name":"Atlanta Falcons",       "city":"Atlanta",       "stadium":"Mercedes-Benz Stadium",   "cap":71000,"surf":"FieldTurf","loc":"Atlanta, GA",         "roof":"Retractable","id":"1", "dome":True},
  "BAL":{"name":"Baltimore Ravens",      "city":"Baltimore",     "stadium":"M&T Bank Stadium",        "cap":71008,"surf":"Grass",    "loc":"Baltimore, MD",       "roof":"Open","id":"33","dome":False},
  "BUF":{"name":"Buffalo Bills",         "city":"Buffalo",       "stadium":"Highmark Stadium",        "cap":71870,"surf":"AstroTurf","loc":"Orchard Park, NY",    "roof":"Open","id":"2", "dome":False},
  "CAR":{"name":"Carolina Panthers",     "city":"Carolina",      "stadium":"Bank of America Stadium", "cap":74455,"surf":"Grass",    "loc":"Charlotte, NC",       "roof":"Open","id":"29","dome":False},
  "CHI":{"name":"Chicago Bears",         "city":"Chicago",       "stadium":"Soldier Field",           "cap":61500,"surf":"Grass",    "loc":"Chicago, IL",         "roof":"Open","id":"3", "dome":False},
  "CIN":{"name":"Cincinnati Bengals",    "city":"Cincinnati",    "stadium":"Paycor Stadium",          "cap":65515,"surf":"Grass",    "loc":"Cincinnati, OH",      "roof":"Open","id":"4", "dome":False},
  "CLE":{"name":"Cleveland Browns",      "city":"Cleveland",     "stadium":"Huntington Bank Field",   "cap":67895,"surf":"Grass",    "loc":"Cleveland, OH",       "roof":"Open","id":"5", "dome":False},
  "DAL":{"name":"Dallas Cowboys",        "city":"Dallas",        "stadium":"AT&T Stadium",            "cap":80000,"surf":"FieldTurf","loc":"Arlington, TX",       "roof":"Retractable","id":"6","dome":True},
  "DEN":{"name":"Denver Broncos",        "city":"Denver",        "stadium":"Empower Field",           "cap":76125,"surf":"Grass",    "loc":"Denver, CO",          "roof":"Open","id":"7", "dome":False},
  "DET":{"name":"Detroit Lions",         "city":"Detroit",       "stadium":"Ford Field",              "cap":65000,"surf":"FieldTurf","loc":"Detroit, MI",         "roof":"Dome","id":"8","dome":True},
  "GB": {"name":"Green Bay Packers",     "city":"Green Bay",     "stadium":"Lambeau Field",           "cap":81441,"surf":"Grass",    "loc":"Green Bay, WI",       "roof":"Open","id":"9", "dome":False},
  "HOU":{"name":"Houston Texans",        "city":"Houston",       "stadium":"NRG Stadium",             "cap":72220,"surf":"Grass",    "loc":"Houston, TX",         "roof":"Retractable","id":"34","dome":True},
  "IND":{"name":"Indianapolis Colts",    "city":"Indianapolis",  "stadium":"Lucas Oil Stadium",       "cap":67000,"surf":"FieldTurf","loc":"Indianapolis, IN",    "roof":"Retractable","id":"11","dome":True},
  "JAX":{"name":"Jacksonville Jaguars",  "city":"Jacksonville",  "stadium":"EverBank Stadium",        "cap":69132,"surf":"Grass",    "loc":"Jacksonville, FL",    "roof":"Open","id":"30","dome":False},
  "KC": {"name":"Kansas City Chiefs",    "city":"Kansas City",   "stadium":"GEHA Field at Arrowhead", "cap":76416,"surf":"Grass",    "loc":"Kansas City, MO",     "roof":"Open","id":"12","dome":False},
  "LV": {"name":"Las Vegas Raiders",     "city":"Las Vegas",     "stadium":"Allegiant Stadium",       "cap":65000,"surf":"Grass",    "loc":"Las Vegas, NV",       "roof":"Dome","id":"13","dome":True},
  "LAC":{"name":"Los Angeles Chargers",  "city":"Los Angeles",   "stadium":"SoFi Stadium",            "cap":70240,"surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered","id":"24","dome":False},
  "LAR":{"name":"Los Angeles Rams",      "city":"Los Angeles",   "stadium":"SoFi Stadium",            "cap":70240,"surf":"Grass",    "loc":"Inglewood, CA",       "roof":"Covered","id":"14","dome":False},
  "MIA":{"name":"Miami Dolphins",        "city":"Miami",         "stadium":"Hard Rock Stadium",       "cap":65326,"surf":"Grass",    "loc":"Miami Gardens, FL",   "roof":"Open","id":"15","dome":False},
  "MIN":{"name":"Minnesota Vikings",     "city":"Minnesota",     "stadium":"U.S. Bank Stadium",       "cap":66860,"surf":"FieldTurf","loc":"Minneapolis, MN",     "roof":"Dome","id":"16","dome":True},
  "NE": {"name":"New England Patriots",  "city":"New England",   "stadium":"Gillette Stadium",        "cap":65878,"surf":"FieldTurf","loc":"Foxborough, MA",      "roof":"Open","id":"17","dome":False},
  "NO": {"name":"New Orleans Saints",    "city":"New Orleans",   "stadium":"Caesars Superdome",       "cap":73208,"surf":"PolyTurf", "loc":"New Orleans, LA",     "roof":"Dome","id":"18","dome":True},
  "NYG":{"name":"New York Giants",       "city":"NY Giants",     "stadium":"MetLife Stadium",         "cap":82500,"surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open","id":"19","dome":False},
  "NYJ":{"name":"New York Jets",         "city":"NY Jets",       "stadium":"MetLife Stadium",         "cap":82500,"surf":"FieldTurf","loc":"East Rutherford, NJ", "roof":"Open","id":"20","dome":False},
  "PHI":{"name":"Philadelphia Eagles",   "city":"Philadelphia",  "stadium":"Lincoln Financial Field", "cap":69596,"surf":"Grass",    "loc":"Philadelphia, PA",    "roof":"Open","id":"21","dome":False},
  "PIT":{"name":"Pittsburgh Steelers",   "city":"Pittsburgh",    "stadium":"Acrisure Stadium",        "cap":68400,"surf":"Grass",    "loc":"Pittsburgh, PA",      "roof":"Open","id":"23","dome":False},
  "SF": {"name":"San Francisco 49ers",   "city":"San Francisco", "stadium":"Levi's Stadium",          "cap":68500,"surf":"Grass",    "loc":"Santa Clara, CA",     "roof":"Open","id":"25","dome":False},
  "SEA":{"name":"Seattle Seahawks",      "city":"Seattle",       "stadium":"Lumen Field",             "cap":72000,"surf":"FieldTurf","loc":"Seattle, WA",         "roof":"Open","id":"26","dome":False},
  "TB": {"name":"Tampa Bay Buccaneers",  "city":"Tampa Bay",     "stadium":"Raymond James Stadium",   "cap":69218,"surf":"Grass",    "loc":"Tampa, FL",           "roof":"Open","id":"27","dome":False},
  "TEN":{"name":"Tennessee Titans",      "city":"Tennessee",     "stadium":"Nissan Stadium",          "cap":69143,"surf":"Grass",    "loc":"Nashville, TN",       "roof":"Open","id":"10","dome":False},
  "WSH":{"name":"Washington Commanders", "city":"Washington",    "stadium":"Northwest Stadium",       "cap":67617,"surf":"Grass",    "loc":"Landover, MD",        "roof":"Open","id":"28","dome":False},
}

INJ_IMPACT = {"QB":10.0,"RB":4.5,"WR":4.0,"TE":3.5,"OT":4.0,"OG":3.0,"C":3.0,
               "DE":4.5,"DT":4.0,"LB":4.0,"CB":4.5,"S":3.5,"K":2.5,"P":1.5}
INJ_MULT = {"Out":1.0,"IR":1.0,"Doubtful":0.85,"Questionable":0.45,"Probable":0.1}

def h(s): st.markdown(s, unsafe_allow_html=True)
def logo(abbr): return LOGO.format(abbr.lower())
def mlf(v): return f"+{v}" if v>0 else str(v)
def pct_bar(pct, color="#5aa8ff"): return f'style="width:{pct:.0f}%;background:{color}"'

def gc(g):
    return {"A+":"gAp","A":"gA","B+":"gBp","B":"gB","C":"gC"}.get(g,"gD")

def get_season():
    now=datetime.now(); year=now.year if now.month>=8 else now.year-1
    pre=datetime(year,8,1); reg=datetime(year,9,9); play=datetime(year+1,1,16)
    if now<pre: return year,1,1
    if now<reg: return year,1,max(1,min((now-pre).days//7+1,4))
    if now<play: return year,2,max(1,min((now-reg).days//7+1,18))
    return year+1,3,max(1,min((now-play).days//7+1,4))

def spread_label(aa, ha, sp):
    if abs(sp)<0.5: return "PK","PK"
    if sp>0: return f"{ha} -{abs(sp):.1f}", f"+{abs(sp):.1f} {aa}"
    return f"{aa} -{abs(sp):.1f}", f"+{abs(sp):.1f} {ha}"

@st.cache_data(ttl=3600)
def fetch_team_stats(team_id, year, stype=2):
    try:
        r=requests.get(f"{ESPN_CORE}/seasons/{year}/types/{stype}/teams/{team_id}/statistics",
                       headers=HDR,timeout=10)
        if r.status_code!=200: return None
        stats={}
        for cat in r.json().get("splits",{}).get("categories",[]):
            for s in cat.get("stats",[]):
                stats[s.get("name","")]=s.get("value",0)
        return stats
    except: return None

@st.cache_data(ttl=3600)
def fetch_record(team_id, year):
    try:
        r=requests.get(f"{ESPN_CORE}/seasons/{year}/types/2/teams/{team_id}/record",
                       headers=HDR,timeout=8)
        if r.status_code==200:
            for item in r.json().get("items",[]):
                if item.get("type","")=="total":
                    st={s["name"]:s["value"] for s in item.get("stats",[])}
                    return {"summary":item.get("summary",""),
                            "wins":int(st.get("wins",0)),"losses":int(st.get("losses",0)),
                            "pct":float(st.get("winPercent",0.5))}
    except: pass
    return None

@st.cache_data(ttl=600)
def team_profile(abbr, year):
    meta=TEAM_META.get(abbr,{}); tid=meta.get("id","")
    fb=FALLBACK.get(abbr,{"off":22,"def":24,"ydg_off":330,"ydg_def":350,"to_diff":0,"win_pct":.5,"streak":0,"sos":.5})
    stats=fetch_team_stats(tid,year) or fetch_team_stats(tid,year-1)
    rec=fetch_record(tid,year) or fetch_record(tid,year-1)
    if stats:
        off=float(stats.get("pointsPerGame",stats.get("totalPointsPerGame",fb["off"])))
        dfn=float(stats.get("opponentPointsPerGame",stats.get("opponentTotalPointsPerGame",fb["def"])))
        yoff=float(stats.get("totalYardsPerGame",fb["ydg_off"]))
        ydef=float(stats.get("opponentTotalYardsPerGame",fb["ydg_def"]))
        tod=float(stats.get("turnovers",0))
        toa=(float(stats.get("interceptions",0))+float(stats.get("fumblesRecovered",0)))
        to_diff=toa-tod
    else:
        off=fb["off"];dfn=fb["def"];yoff=fb["ydg_off"];ydef=fb["ydg_def"];to_diff=fb["to_diff"]
    wins=rec["wins"] if rec else int(fb["win_pct"]*17)
    losses=rec["losses"] if rec else 17-wins
    pct=rec["pct"] if rec else fb["win_pct"]
    return {"abbr":abbr,"off":round(off,1),"def":round(dfn,1),"yoff":round(yoff,1),
            "ydef":round(ydef,1),"to_diff":round(to_diff,1),"win_pct":round(pct,3),
            "wins":wins,"losses":losses,"record":rec["summary"] if rec else f"{wins}-{losses}",
            "streak":fb.get("streak",0),"sos":fb.get("sos",.5),"live":stats is not None}

@st.cache_data(ttl=120)
def fetch_schedule(year, stype, week):
    for base in [ESPN, ESPN_WEB]:
        try:
            r=requests.get(f"{base}/scoreboard?dates={year}&seasontype={stype}&week={week}&limit=25",
                           headers=HDR,timeout=10)
            if r.status_code==200: return r.json()
        except: pass
    return {}

@st.cache_data(ttl=300)
def fetch_injuries(tid):
    try:
        r=requests.get(f"{ESPN_CORE}/teams/{tid}/injuries",headers=HDR,timeout=8)
        if r.status_code!=200: return []
        out=[]
        for item in r.json().get("items",[])[:12]:
            ref=item.get("$ref","")
            if not ref: continue
            dr=requests.get(ref,headers=HDR,timeout=5)
            if dr.status_code!=200: continue
            d=dr.json(); status=d.get("status","Questionable")
            ar=d.get("athlete",{}).get("$ref","")
            if ar:
                arr=requests.get(ar,headers=HDR,timeout=5)
                if arr.status_code==200:
                    ad=arr.json()
                    out.append({"name":ad.get("displayName","?"),
                                "pos":ad.get("position",{}).get("abbreviation","?"),
                                "status":status})
        return out
    except: return []

def parse_games(data):
    games=[]
    for event in data.get("events",[]):
        try:
            comp=event["competitions"][0]
            hm=next(c for c in comp["competitors"] if c["homeAway"]=="home")
            aw=next(c for c in comp["competitors"] if c["homeAway"]=="away")
            ha,aa=hm["team"]["abbreviation"],aw["team"]["abbreviation"]
            state=event["status"]["type"]["state"]
            net=""
            bc=comp.get("broadcasts",[])
            if bc:
                m=bc[0].get("media",{}); net=m.get("shortName","") or m.get("callLetters","")
            dt=None
            try: dt=datetime.fromisoformat(event.get("date","").replace("Z","+00:00"))
            except: pass
            games.append({"ha":ha,"aa":aa,"hid":hm["team"]["id"],"aid":aw["team"]["id"],
                "hname":hm["team"].get("displayName",TEAM_META.get(ha,{}).get("name",ha)),
                "aname":aw["team"].get("displayName",TEAM_META.get(aa,{}).get("name",aa)),
                "hs":hm.get("score",""),"as":aw.get("score",""),
                "hr":(hm.get("records",[{}])[0].get("summary","") if hm.get("records") else ""),
                "ar":(aw.get("records",[{}])[0].get("summary","") if aw.get("records") else ""),
                "state":state,"status":event["status"]["type"]["shortDetail"],"net":net,
                "venue":comp.get("venue",{}).get("fullName","") or TEAM_META.get(ha,{}).get("stadium",""),
                "dt":dt})
        except: continue
    return games

def inj_penalty(injuries):
    pen=0
    for i in (injuries or []):
        pen+=INJ_IMPACT.get(i.get("pos","WR"),3)*INJ_MULT.get(i.get("status","Q"),.45)*0.09
    return min(pen,8.0)

def predict(aa, ha, year, ainj=None, hinj=None):
    ap=team_profile(aa,year); hp=team_profile(ha,year)
    dome=TEAM_META.get(ha,{}).get("dome",False)
    hfa=3.0 if dome else 2.5
    a_raw=ap["off"]*0.50+(32-hp["def"])*0.50
    h_raw=hp["off"]*0.50+(32-ap["def"])*0.50
    ydg_a=(ap["yoff"]-hp["ydef"])*0.008
    ydg_h=(hp["yoff"]-ap["ydef"])*0.008
    a_proj=max(10,a_raw+ydg_a+ap["to_diff"]*0.4-inj_penalty(ainj))
    h_proj=max(10,h_raw+ydg_h+hp["to_diff"]*0.4+hfa-inj_penalty(hinj))
    a_rtg=(ap["off"]-ap["def"])+ap["to_diff"]*0.8+(ap["win_pct"]-.5)*20+(ap["sos"]-.5)*10
    h_rtg=(hp["off"]-hp["def"])+hp["to_diff"]*0.8+(hp["win_pct"]-.5)*20+(hp["sos"]-.5)*10
    a_rtg+=max(-3,min(3,ap["streak"]))*0.5; h_rtg+=max(-3,min(3,hp["streak"]))*0.5
    a_rtg-=inj_penalty(ainj)*0.8; h_rtg-=inj_penalty(hinj)*0.8
    diff=(h_rtg-a_rtg)+hfa*0.5
    hwp=1/(1+np.exp(-diff/8)); awp=1-hwp
    if hwp>0.5: hml=-int(round(hwp/(1-hwp)*100/5)*5); aml=int(round(awp/hwp*100/5)*5)
    else: aml=-int(round(awp/(1-awp)*100/5)*5); hml=int(round(hwp/awp*100/5)*5)
    margin=h_proj-a_proj
    spread=round(margin/0.5)*0.5; total=a_proj+h_proj; tl=round(total/0.5)*0.5
    ou="OVER" if total>tl+0.25 else "UNDER"
    c=abs(diff)
    grade="A+" if c>18 else "A" if c>12 else "B+" if c>8 else "B" if c>5 else "C" if c>2 else "D"
    mg="A" if abs(hml)>180 else "B" if abs(hml)>130 else "C" if abs(hml)>110 else "D"
    rg="A" if abs(spread)>=7.5 else "B" if abs(spread)>=4 else "C" if abs(spread)>=2 else "D"
    ug="A" if abs(total-tl)>1.5 else "B" if abs(total-tl)>.7 else "C"
    return {"ap":round(a_proj,1),"hp":round(h_proj,1),"tot":round(total,1),"tl":tl,"ou":ou,
            "hwp":round(hwp*100,1),"awp":round(awp*100,1),"hml":hml,"aml":aml,"spread":spread,
            "pick":ha if hwp>.5 else aa,"grade":grade,"mg":mg,"rg":rg,"ug":ug,
            "ap_":ap,"hp_":hp}

# ── Header ────────────────────────────────────────────────────────────────────
sy,stype,cur_wk=get_season()
phase_label={1:"Preseason",2:"Regular Season",3:"Playoffs"}.get(stype,"Season")

h(f'''<div class="topbar">
  <div class="brand">
    <div class="brand-icon">N+</div>
    <div class="brand-name">NFL<span>+</span></div>
    <div class="brand-tag">● Live</div>
  </div>
  <div class="nav-right">
    <div class="nav-season">{sy}–{str(sy+1)[2:]} · {phase_label} · Week {cur_wk}</div>
    <div class="live-badge"><div class="live-dot"></div>ESPN LIVE</div>
  </div>
</div>''')

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1,tab2=st.tabs(["🏂  Schedule & Picks","🏆  Power Rankings"])

# ══ TAB 1 — SCHEDULE ══════════════════════════════════════════════════════════
with tab1:
    cc1,cc2,cc3,cc4=st.columns([2,2,1,1])
    pm={"Preseason":1,"Regular Season":2,"Playoffs":3}
    pd={1:"Preseason",2:"Regular Season",3:"Playoffs"}.get(stype,"Regular Season")
    with cc1: sel_p=st.selectbox("SEASON PHASE",list(pm.keys()),index=list(pm.keys()).index(pd))
    with cc2:
        mw={1:4,2:18,3:4}.get(pm[sel_p],18)
        sel_w=st.slider("WEEK",1,mw,min(cur_wk if pm[sel_p]==stype else 1,mw))
    with cc3: sel_y=st.selectbox("YEAR",[sy,sy-1],index=0)
    with cc4:
        st.markdown("<div style='height:26px'></div>",unsafe_allow_html=True)
        if st.button("↻ Refresh",use_container_width=True):
            st.cache_data.clear(); st.rerun()

    with st.spinner(""):
        raw=fetch_schedule(sel_y,pm[sel_p],sel_w)
    games=parse_games(raw)
    wt=raw.get("week",{}).get("text",f"Week {sel_w}")
    sn=raw.get("season",{}).get("displayName",f"{sel_y} NFL")
    live_ct=sum(1 for g in games if g["state"]=="in")
    fin_ct=sum(1 for g in games if g["state"]=="post")
    pre_ct=sum(1 for g in games if g["state"]=="pre")

    # stat pills
    pills=""
    if live_ct:
        pills+=f'<div class="stat-pill stat-pill-live"><div class="stat-pill-val">{live_ct}</div><div class="stat-pill-lbl">Live Now</div></div>'
    pills+=f'<div class="stat-pill"><div class="stat-pill-val">{len(games)}</div><div class="stat-pill-lbl">Total Games</div></div>'
    pills+=f'<div class="stat-pill"><div class="stat-pill-val">{fin_ct}</div><div class="stat-pill-lbl">Final</div></div>'
    pills+=f'<div class="stat-pill"><div class="stat-pill-val">{pre_ct}</div><div class="stat-pill-lbl">Upcoming</div></div>'
    pills+=f'<div class="stat-pill"><div style="font-size:11px;font-weight:600;color:#2e3850">{sn} · {wt}</div></div>'
    h(f'<div class="status-row">{pills}</div>')

    if not games:
        h('<div style="background:#0d1117;border:1px solid #1c2130;border-radius:12px;'
          'padding:60px;text-align:center;color:#2e3850;font-size:14px">'
          'No games scheduled for this week. Try a different week or season phase.</div>')
    else:
        h(f'<div class="section-title">{wt} · {len(games)} Games</div>')
        for g in games:
            p=predict(g["aa"],g["ha"],sel_y)
            state=g["state"]
            a_score=g["as"] if state!="pre" else ""
            h_score=g["hs"] if state!="pre" else ""
            a_win=state=="post" and a_score and h_score and int(a_score or 0)>int(h_score or 0)
            h_win=state=="post" and a_score and h_score and int(h_score or 0)>int(a_score or 0)
            a_sc=f'<span class="team-score {"win" if a_win else ("lose" if h_win and state=="post" else "")}">{a_score}</span>'
            h_sc=f'<span class="team-score {"win" if h_win else ("lose" if a_win and state=="post" else "")}">{h_score}</span>'

            # Date + time strings — must be computed before st_html
            game_date = ""
            game_time = ""
            if g["dt"]:
                try:
                    local_dt = g["dt"].astimezone()
                    game_date = local_dt.strftime("%a, %b %-d")
                    game_time = local_dt.strftime("%-I:%M %p %Z")
                except:
                    pass
            if not game_date:
                game_date = g["status"]
            if not game_time and state == "pre":
                game_time = "TBD"
            if state == "in":
                game_time = g["status"]
            elif state == "post":
                game_time = ""
            net_html = f'<div class="game-network">{g["net"]}</div>' if g["net"] else ""
            venue_short = g["venue"].replace(" Stadium","").replace(" Field","").replace(" at ",", ")

            # Status label
            if state == "in":
                st_html = f'<div class="game-status-live">● LIVE</div>'
            elif state == "post":
                st_html = '<div class="game-status-final">FINAL</div>'
            else:
                st_html = f'<div class="game-status-pre">{game_date}</div>' 

            # win prob bar
            hwp=p["hwp"]; awp=p["awp"]
            a_bar=f'<div class="stat-bar-a" style="width:{min(awp/2,50):.0f}%"></div>'
            h_bar=f'<div class="stat-bar-h" style="width:{min(hwp/2,50):.0f}%"></div>'

            # odds
            sl,_=spread_label(g["aa"],g["ha"],p["spread"])
            ou_cls="over" if p["ou"]=="OVER" else "under"
            ao=mlf(p["aml"]); ho_str=mlf(p["hml"])

            # Build every piece as a plain string variable first
            a_logo_s   = '<img src="' + logo(g["aa"]) + '" class="team-logo" onerror="this.style.opacity=.2">'
            h_logo_s   = '<img src="' + logo(g["ha"]) + '" class="team-logo" onerror="this.style.opacity=.2">'
            a_info_s   = '<div class="team-name">' + g["aname"] + '</div><div class="team-record">' + g["ar"] + '</div>'
            h_info_s   = '<div class="team-name">' + g["hname"] + '</div><div class="team-record">' + g["hr"] + '</div>'
            venue_s    = '<div class="game-venue">🏟 ' + venue_short + '</div>'
            time_s     = ('<div class="game-time">' + game_time + '</div>') if game_time else ""
            wp_bars_s  = '<div style="position:relative;height:100%">' + a_bar + h_bar + '</div>'
            wp_away_s  = '<span class="wp-away">' + g["aa"] + ' ' + str(awp) + '%</span>'
            wp_home_s  = '<span class="wp-home">' + str(hwp) + '% ' + g["ha"] + '</span>'
            ml_grade_s = '<span class="odds-grade ' + gc(p["mg"]) + '">' + p["mg"] + '</span>'
            sp_grade_s = '<span class="odds-grade ' + gc(p["rg"]) + '">' + p["rg"] + '</span>'
            ou_grade_s = '<span class="odds-grade ' + gc(p["ug"]) + '">' + p["ug"] + '</span>'
            ml_sub_s   = g["aa"] + ' ' + ao + ' / ' + g["ha"] + ' ' + ho_str
            sp_sub_s   = 'Proj ' + str(p["ap"]) + ' - ' + str(p["hp"]) + ' · ' + str(round(abs(p["hp"]-p["ap"]),1)) + ' pt margin'
            ou_val_s   = p["ou"] + ' ' + str(p["tl"])
            ou_cls_s   = 'odds-main ' + ou_cls
            ou_sub_s   = 'Proj ' + str(p["tot"]) + ' pts · Line ' + str(p["tl"])

            card = (
                '<div class="gcard">'
                + '<div class="gcard-inner" style="display:flex;align-items:center;gap:0">'
                + '<div class="team-section">'
                + '<div class="team-row">'
                + a_logo_s
                + '<div class="team-info">' + a_info_s + '</div>'
                + a_sc
                + '</div>'
                + '<div class="team-row">'
                + h_logo_s
                + '<div class="team-info">' + h_info_s + '</div>'
                + h_sc
                + '</div>'
                + '</div>'
                + '<div class="game-center">'
                + st_html + time_s + net_html + venue_s
                + '</div>'
                + '<div class="wp-section">'
                + '<div class="wp-label">WIN PROB</div>'
                + '<div class="wp-bar-wrap">' + wp_bars_s + '</div>'
                + '<div class="wp-teams">' + wp_away_s + wp_home_s + '</div>'
                + '</div>'
                + '</div>'
                + '<div class="odds-strip">'
                + '<div class="odds-cell">'
                + '<div class="odds-type">MONEYLINE ' + ml_grade_s + '</div>'
                + '<div class="odds-main">' + p["pick"] + '</div>'
                + '<div class="odds-sub">' + ml_sub_s + '</div>'
                + '</div>'
                + '<div class="odds-cell">'
                + '<div class="odds-type">SPREAD ' + sp_grade_s + '</div>'
                + '<div class="odds-main">' + sl + '</div>'
                + '<div class="odds-sub">' + sp_sub_s + '</div>'
                + '</div>'
                + '<div class="odds-cell">'
                + '<div class="odds-type">TOTAL O/U ' + ou_grade_s + '</div>'
                + '<div class="' + ou_cls_s + '">' + ou_val_s + '</div>'
                + '<div class="odds-sub">' + ou_sub_s + '</div>'
                + '</div>'
                + '</div>'
                + '</div>'
            )
            h(card)


# ══ TAB 2 — POWER RANKINGS ════════════════════════════════════════════════════
with tab2:
    h('<div class="section-title">2026 Power Rankings · Live ESPN Stats</div>')
    with st.spinner("Loading team data…"):
        all_p={a:team_profile(a,sy) for a in TEAM_META}

    live_n=sum(1 for p in all_p.values() if p["live"])
    h(f'<div class="status-row">'
      f'<div class="stat-pill"><div class="stat-pill-val">{live_n}</div><div class="stat-pill-lbl">Live Data</div></div>'
      f'<div class="stat-pill"><div class="stat-pill-val">{32-live_n}</div><div class="stat-pill-lbl">Preseason Est.</div></div>'
      f'<div class="stat-pill"><div style="font-size:11px;color:#2e3850">Ranked by scoring differential</div></div>'
      f'</div>')

    sorted_t=sorted(all_p.items(),key=lambda x:x[1]["off"]-x[1]["def"],reverse=True)
    max_off=max(p["off"] for _,p in sorted_t); max_def=max(p["def"] for _,p in sorted_t)

    rows_html=""
    for rank,(abbr,prof) in enumerate(sorted_t,1):
        meta=TEAM_META.get(abbr,{})
        diff=prof["off"]-prof["def"]
        diff_col="#4cffaa" if diff>0 else "#ff4444"
        ds=f'+{diff:.1f}' if diff>0 else f'{diff:.1f}'
        bar_pct=int(prof["off"]/max_off*100)
        bar_col="#013369" if diff>3 else "#4a5570" if diff>0 else "#5a2020"
        live_dot=f'<span style="width:5px;height:5px;border-radius:50%;background:#4cffaa;display:inline-block;margin-left:5px;vertical-align:middle"></span>' if prof["live"] else ""
        tc="trend-up" if prof["off"]>prof["def"] else "trend-dn" if prof["off"]<prof["def"] else "trend-eq"

        rows_html+=(f'<div class="rank-row">'
            f'<div class="rank-num">#{rank}</div>'
            f'<img src="{logo(abbr)}" class="rank-logo" onerror="this.style.opacity=.2">'
            f'<div class="rank-info">'
            f'<div class="rank-name">{meta.get("name",abbr)}{live_dot}</div>'
            f'<div class="rank-sub">{prof["record"]}  ·  {meta.get("stadium","")}</div></div>'
            f'<div class="rank-stat"><div class="rank-stat-val" style="color:#5aa8ff">{prof["off"]}</div><div class="rank-stat-lbl">OFF PPG</div></div>'
            f'<div class="rank-stat"><div class="rank-stat-val" style="color:#ff6b6b">{prof["def"]}</div><div class="rank-stat-lbl">DEF PPG</div></div>'
            f'<div class="rank-diff {tc}">{ds}</div>'
            f'<div class="rank-bar"><div class="rank-bar-fill" style="width:{bar_pct}%;background:{bar_col}"></div></div>'
            f'</div>')

    h(f'<div style="border:1px solid #1c2130;border-radius:10px;overflow:hidden">{rows_html}</div>')
    h('<div style="margin-top:12px;font-size:10px;color:#1c2540;text-align:center">'
      'Stats auto-fetched from ESPN Core API · For entertainment only</div>')
