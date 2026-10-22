import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Meridian SCM AI Sentinel",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Dark theme matching reference images exactly
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"], .stApp { background-color:#0b0b0c !important; color:#f4f4f5; font-family:'Inter',system-ui,sans-serif; }
header[data-testid="stHeader"] { background:transparent !important; }
#MainMenu, footer { visibility:hidden; }
.main .block-container { padding:0.8rem 1.6rem 2rem !important; max-width:100% !important; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] { background:#0f0f10 !important; border-right:1px solid #1f1f22 !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] * { color:#a1a1aa !important; }
div[role="radiogroup"] { gap:2px; }
div[role="radiogroup"] label {
    padding:10px 12px; margin:1px 0; border-radius:12px; border:1px solid transparent;
    transition:all .18s ease; cursor:pointer; width:100%;
}
div[role="radiogroup"] label p { color:#8b8b93 !important; font-size:.84rem !important; font-weight:500 !important; margin:0 !important; }
div[role="radiogroup"] label:hover { background:rgba(255,255,255,.04) !important; }
div[role="radiogroup"] label:hover p { color:#d4d4d8 !important; }
div[role="radiogroup"] label:has(input:checked) { background:rgba(255,106,26,.12) !important; border-color:rgba(255,106,26,.35) !important; }
div[role="radiogroup"] label:has(input:checked) p { color:#c4b5fd !important; font-weight:600 !important; }

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#0b0b0c; }
::-webkit-scrollbar-thumb { background:#3a3a3f; border-radius:6px; }
::-webkit-scrollbar-thumb:hover { background:#8b5cf688; }

/* ---- Cards (st.container(key="card_*")) ---- */
[class*="st-key-card"] {
    background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);
    border:1px solid #27272a; border-radius:18px; padding:18px 20px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.04), 0 8px 24px rgba(0,0,0,.35);
}
[data-testid="stMetric"], [data-testid="metric-container"] {
    background:#151517 !important; border:1px solid #27272a !important; border-radius:18px !important; padding:14px 16px !important;
}
[data-testid="stMetricValue"] { color:#f4f4f5 !important; font-weight:700 !important; }
[data-testid="stMetricLabel"] { color:#8b8b93 !important; }

/* ---- Buttons ---- */
.stButton > button, [data-testid="stDownloadButton"] button {
    background:#1b1b1e !important; border:1px solid #3a3a3f !important; color:#d4d4d8 !important;
    border-radius:10px !important; font-size:.78rem !important; font-weight:600 !important; padding:6px 14px !important; transition:all .18s;
}
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
    background:#232326 !important; border-color:#8b5cf688 !important; color:#c4b5fd !important; box-shadow:0 0 12px #8b5cf622 !important;
}
[data-testid="baseButton-primary"], [data-testid="stBaseButton-primary"], .stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#a78bfa,#6d28d9) !important; border:none !important; color:#fff !important;
    box-shadow:0 4px 16px #8b5cf655 !important;
}
[data-testid="baseButton-primary"]:hover, [data-testid="stBaseButton-primary"]:hover, .stButton > button[kind="primary"]:hover {
    box-shadow:0 6px 24px #8b5cf688 !important; transform:translateY(-1px); color:#fff !important;
}

/* ---- Inputs ---- */
[data-testid="stSlider"] [role="slider"] { background:#8b5cf6 !important; box-shadow:0 0 10px #8b5cf688 !important; }
[data-baseweb="select"] > div { background:#151517 !important; border-color:#27272a !important; border-radius:12px !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background:#151517 !important; border-color:#27272a !important; }
[data-baseweb="option"]:hover { background:rgba(255,106,26,.10) !important; }
[data-baseweb="tag"] { background:rgba(255,106,26,.15) !important; border-color:rgba(255,106,26,.35) !important; }
input, textarea { background:#151517 !important; border-color:#27272a !important; color:#f4f4f5 !important; border-radius:10px !important; }
[data-testid="stCheckbox"] label { color:#a1a1aa !important; font-size:.82rem !important; }

/* ---- Tables / misc ---- */
[data-testid="stDataFrame"] { border:1px solid #27272a; border-radius:14px !important; overflow:hidden; }
[data-testid="stExpander"] { background:#151517 !important; border:1px solid #27272a !important; border-radius:14px !important; }
button[data-baseweb="tab"] { background:transparent !important; color:#8b8b93 !important; font-weight:600 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#8b5cf6 !important; border-bottom:2px solid #8b5cf6 !important; }
[data-testid="stAlert"] { border-radius:12px !important; border-left-width:3px !important; background:#151517 !important; }
hr { border-color:#27272a !important; margin:12px 0 !important; }
h1 { font-size:1.6rem !important; font-weight:800 !important; color:#f4f4f5 !important; }
h2 { font-size:1.1rem !important; font-weight:700 !important; color:#f4f4f5 !important; }
h3 { font-size:.95rem !important; font-weight:600 !important; color:#a1a1aa !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# DATA LOAD
# ──────────────────────────────────────────────────────────────────────────────
HERE    = os.path.dirname(os.path.abspath(__file__))
OUT     = os.path.join(HERE, "output")
FIG_DIR = os.path.join(OUT, "figures")

@st.cache_data
def load_all_data():
    sup  = pd.read_csv(os.path.join(OUT, "supplier_risk_scores.csv"))
    mat  = pd.read_csv(os.path.join(OUT, "material_risk.csv"))
    acts = pd.read_csv(os.path.join(OUT, "action_queue.csv"))
    trnd = pd.read_csv(os.path.join(OUT, "weekly_delay_trend.csv"))
    with open(os.path.join(OUT, "metrics.json")) as f:
        mtr = json.load(f)
    return sup, mat, acts, trnd, mtr

scores_df, mat_df, action_df, trend_df, metrics = load_all_data()

# ──────────────────────────────────────────────────────────────────────────────
# UTILITY HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def _bc(band): return {"Critical":"#ef4444","High":"#8b5cf6","Medium":"#fbbf24","Low":"#22c55e"}.get(band,"#a1a1aa")
def _bg(band): return {"Critical":A("#ef444420"),"High":A("#8b5cf620"),"Medium":A("#fbbf2420"),"Low":A("#22c55e20")}.get(band,A("#a1a1aa20"))

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui", color="#8b8b93", size=10),
    margin=dict(l=10, r=10, t=32, b=10),
    xaxis=dict(gridcolor="#27272a", zerolinecolor="#27272a", showgrid=True),
    yaxis=dict(gridcolor="#27272a", zerolinecolor="#27272a", showgrid=True),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)", font_size=10),
    hoverlabel=dict(bgcolor="#151517", bordercolor="#3a3a3f", font_color="#f4f4f5", font_size=11),
)

def dark_fig(fig, title="", h=300):
    fig.update_layout(**PLOTLY_BASE, title=dict(text=title, font=dict(color="#a1a1aa", size=11), x=0.01), height=h)
    return fig


# ── Theme helpers ─────────────────────────────────────────────────────────────
from matplotlib.colors import LinearSegmentedColormap
HEAT = LinearSegmentedColormap.from_list("heat", ["#1b1b1e", "#4c1d95", "#8b5cf6"])   # dark -> orange for table gradients

def A(c):
    """Plotly rejects 8-digit hex (#rrggbbaa); convert it to rgba()."""
    if isinstance(c, str) and c.startswith("#") and len(c) == 9:
        r, g, b, a = (int(c[i:i+2], 16) for i in (1, 3, 5, 7))
        return f"rgba({r},{g},{b},{a/255:.2f})"
    return c

def base(**over):
    """PLOTLY_BASE merged with overrides (avoids 'multiple values for keyword' errors)."""
    d = dict(PLOTLY_BASE); d.update(over); return d

def card_header(title, sub=""):
    s = f'<div style="font-size:0.7rem;color:#71717a;margin-top:2px;">{sub}</div>' if sub else ""
    st.markdown(f'''<div style="margin-bottom:8px;"><div style="font-size:0.9rem;font-weight:700;color:#f4f4f5;">{title}</div>{s}</div>''', unsafe_allow_html=True)

# ─── CARD COMPONENTS ──────────────────────────────────────────────────────────

def kpi_card_sparkline(icon, label, value, prev_value, trend_pct, spark_vals, spark_color, sub=""):
    """KPI card with top-right trend badge + bottom sparkline — matches Buildly reference exactly."""
    trend_sign = "+" if trend_pct >= 0 else ""
    trend_color = "#22c55e" if trend_pct >= 0 else "#ef4444"
    arrow = "▲" if trend_pct >= 0 else "▼"
    # Build SVG sparkline from spark_vals
    n = len(spark_vals)
    mn, mx = min(spark_vals), max(spark_vals)
    rng = mx - mn if mx != mn else 1
    W, H = 90, 28
    pts = " ".join(f"{int(i*(W/(n-1)))},{int(H - (v-mn)/rng*H)}" for i, v in enumerate(spark_vals))
    svg = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
      <polyline points="{pts}" fill="none" stroke="{spark_color}" stroke-width="1.8" stroke-linejoin="round"/>
    </svg>"""
    st.markdown(f"""
    <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%); border:1px solid #27272a; border-radius:18px;
                padding:14px 16px 10px; position:relative; overflow:hidden; height:115px;">
      <div style="position:absolute; top:10px; right:10px;
                  background:{trend_color}18; border:1px solid {trend_color}44;
                  border-radius:20px; padding:2px 8px; font-size:0.68rem;
                  font-weight:700; color:{trend_color};">
        {arrow} {trend_sign}{trend_pct:.1f}%
      </div>
      <div style="font-size:0.68rem; color:#8b8b93; font-weight:500;
                  text-transform:uppercase; letter-spacing:0.07em; margin-bottom:4px;">
        {icon} {label}
      </div>
      <div style="font-size:1.4rem; font-weight:800; color:#f4f4f5; line-height:1.2;">{value}</div>
      {'<div style="font-size:0.68rem; color:#71717a; margin-top:2px;">Prev: '+prev_value+'</div>' if prev_value else ''}
      <div style="position:absolute; bottom:10px; right:12px; opacity:0.7;">{svg}</div>
    </div>
    """, unsafe_allow_html=True)

def kpi_card_large(icon, label, value, sub1, sub2, bar_vals, color="#8b5cf6"):
    """Large card with inline mini bar chart — matches Aiq-ui reference image 2."""
    n = len(bar_vals)
    mn, mx = min(bar_vals), max(bar_vals)
    rng = mx - mn if mx != mn else 1
    W, H = 100, 32
    bar_w = max(4, int(W/n) - 2)
    bars_svg = "".join(
        f'<rect x="{int(i*(W/n))}" y="{int(H-(v-mn)/rng*H)}" '
        f'width="{bar_w}" height="{int((v-mn)/rng*H)+2}" '
        f'fill="{color if i==n-1 else color+"55"}" rx="1"/>'
        for i, v in enumerate(bar_vals)
    )
    svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{bars_svg}</svg>'
    st.markdown(f"""
    <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%); border:1px solid #27272a; border-radius:18px;
                padding:16px 18px 12px; position:relative; overflow:hidden; min-height:130px;">
      <div style="font-size:0.68rem; color:#8b8b93; text-transform:uppercase;
                  letter-spacing:0.07em; margin-bottom:6px;">{icon} {label}</div>
      <div style="font-size:1.7rem; font-weight:800; color:#f4f4f5;">{value}</div>
      <div style="font-size:0.72rem; color:{color}; font-weight:600; margin-top:3px;">{sub1}</div>
      <div style="font-size:0.68rem; color:#71717a; margin-top:1px;">{sub2}</div>
      <div style="position:absolute; bottom:12px; right:14px; opacity:0.75;">{svg}</div>
    </div>
    """, unsafe_allow_html=True)

def circular_progress(label, value_pct, center_label, center_sub, color="#8b5cf6"):
    """Circular ring progress — matches 72% Monthly Goal card in reference image 2."""
    r = 44; cx = cy = 52; stroke = 8
    circ = 2 * 3.14159 * r
    dash = circ * max(0.0, min(float(value_pct), 100.0)) / 100
    st.markdown(f"""
    <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%); border:1px solid #27272a; border-radius:18px;
                padding:14px 16px; text-align:center;">
      <div style="font-size:0.68rem; color:#8b8b93; text-transform:uppercase;
                  letter-spacing:0.07em; margin-bottom:8px;">{label}</div>
      <svg width="104" height="104" viewBox="0 0 104 104" xmlns="http://www.w3.org/2000/svg">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#27272a" stroke-width="{stroke}"/>
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}"
                stroke-dasharray="{dash:.1f} {circ:.1f}"
                stroke-dashoffset="{circ/4:.1f}"
                stroke-linecap="round"/>
        <text x="{cx}" y="{cy-5}" text-anchor="middle" fill="#f4f4f5"
              font-size="15" font-weight="800" font-family="Inter">{center_label}</text>
        <text x="{cx}" y="{cy+12}" text-anchor="middle" fill="#8b8b93"
              font-size="8" font-family="Inter">{center_sub}</text>
      </svg>
    </div>
    """, unsafe_allow_html=True)

def risk_badge_html(band, score=None):
    c = _bc(band)
    score_txt = f" {score:.1f}" if score is not None else ""
    pulse = "animation:pulse 1.6s ease-in-out infinite;" if band == "Critical" else ""
    return f"""
    <style>@keyframes pulse{{0%,100%{{box-shadow:0 0 4px {c}55;}}50%{{box-shadow:0 0 14px {c}99;}}}}</style>
    <span style="background:{c}18;border:1px solid {c}55;color:{c};
                 border-radius:20px;padding:2px 10px;font-size:0.7rem;
                 font-weight:700;letter-spacing:0.05em;{pulse}display:inline-block;">
      ● {band.upper()}{score_txt}
    </span>"""

def section_label(text):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:18px 0 12px;">
      <div style="width:3px;height:16px;background:#8b5cf6;border-radius:2px;"></div>
      <span style="font-size:0.72rem;font-weight:700;color:#8b8b93;
                   letter-spacing:0.1em;text-transform:uppercase;">{text}</span>
    </div>
    """, unsafe_allow_html=True)

def top_bar(page_title, show_time_filter=False):
    """Renders the welcome/page header bar matching Buildly reference top bar."""
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown(f"""
        <div style="padding: 6px 0 10px;">
          <div style="font-size:0.68rem;color:#71717a;margin-bottom:2px;">
            Meridian Home Appliances · Plant 1, Chakan · <span style="color:#8b5cf655;">●</span>
            <span style="color:#22c55e;font-weight:600;"> RISK MONITORING</span>
          </div>
          <h1 style="margin:0;font-size:1.45rem;font-weight:800;color:#f4f4f5;">{page_title}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;padding-top:12px;">
          <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid #27272a;border-radius:7px;
                      padding:5px 12px;font-size:0.72rem;color:#8b8b93;">📅 {now}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='margin:0 0 14px;border-color:#27272a;'>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 8px 10px;border-bottom:1px solid #27272a;margin-bottom:12px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#a78bfa,#6d28d9);display:flex;align-items:center;justify-content:center;font-size:1.05rem;box-shadow:0 4px 14px #8b5cf655;">🏭</div>
        <div>
          <div style="font-size:0.85rem;font-weight:800;color:#f4f4f5;">Meridian SCM</div>
          <div style="font-size:0.62rem;color:#71717a;">AI Sentinel v2.0</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.62rem;color:#52525b;font-weight:700;letter-spacing:0.08em;padding:0 4px 6px;text-transform:uppercase;'>Navigation</div>", unsafe_allow_html=True)

    nav = st.radio("Navigation", [
        "📊 Executive Dashboard",
        "🎯 Supplier Risk Radar",
        "📦 Inventory Watch",
        "🤖 Mitigation Copilot",
        "🧪 Scenario Simulator",
        "📋 Action Queue",
        "📈 Model Audit",
        "🏛️ Control Tower",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#27272a;margin:12px 0;'>", unsafe_allow_html=True)

    # Live status dot
    crit_n = int(metrics["band_counts"].get("Critical", 0))
    high_n = int(metrics["band_counts"].get("High", 0))
    st.markdown(f"""
    <div style="background:#101a12;border:1px solid #22c55e22;border-radius:8px;padding:10px 12px;margin-bottom:10px;">
      <div style="font-size:0.68rem;font-weight:700;color:#22c55e;margin-bottom:6px;">● RISK ENGINE STATUS</div>
      <div style="font-size:0.68rem;color:#71717a;line-height:1.7;">
        <div>🔴 Critical: <b style="color:#ef4444;">{crit_n}</b> supplier(s)</div>
        <div>🟠 High: <b style="color:#8b5cf6;">{high_n}</b> supplier(s)</div>
        <div>📅 As of: <b style="color:#a1a1aa;">{metrics['as_of']}</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-size:0.68rem;color:#71717a;line-height:1.8;padding:0 2px;">
      <div>💰 Revenue: <b style="color:#f4f4f5;">₹{metrics['annual_revenue_inr_crore']} Cr</b></div>
      <div>🏗️ RM Spend: <b style="color:#f4f4f5;">₹{metrics['total_spend_inr_crore']} Cr</b></div>
      <div>🔗 Suppliers: <b style="color:#f4f4f5;">{metrics['n_suppliers']}</b></div>
      <div>📦 Materials: <b style="color:#f4f4f5;">{metrics['n_materials']} SKUs</b></div>
      <div>🏭 Products: <b style="color:#f4f4f5;">{metrics['n_products']}</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#27272a;margin:12px 0;'>", unsafe_allow_html=True)
    gemini_key = st.text_input("🔑 Gemini API Key", type="password",
                               placeholder="sk-... (optional)",
                               help="Enter to activate live Gemini reasoning.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE DASHBOARD
# Matches: Buildly reference — KPI row + dual-axis trend + donut + sliders
# ══════════════════════════════════════════════════════════════════════════════
if nav == "📊 Executive Dashboard":
    top_bar("Welcome back — Meridian Operations")
    st.caption(
        "Simulated case study. Risk scores are decision-support indicators; "
        "synthetic-label metrics are not independently validated predictions."
    )

    # ── Time-range toggle (4 buttons side by side) + Export ─────────────────
    tr_col1, tr_col2, tr_col3, tr_col4, tr_col5, tr_spacer, tr_exp = st.columns([1,1,1,1,1,5,1.2])
    for col, label, key in zip([tr_col1,tr_col2,tr_col3,tr_col4,tr_col5],
                                ["4W","8W","ALL","3M","6M"],
                                ["4w","8w","all","3m","6m"]):
        with col:
            if st.button(label, key=f"tr_{key}", use_container_width=True):
                st.session_state["time_range"] = key
    if "time_range" not in st.session_state:
        st.session_state["time_range"] = "all"
    with tr_exp:
        csv_export = scores_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export", csv_export, "meridian_scores.csv", "text/csv",
                           use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Build sparkline data per supplier from trend_df ──────────────────────
    t_copy = trend_df.copy()
    t_copy["week_dt"] = pd.to_datetime(t_copy["week"])
    t_copy = t_copy.sort_values("week_dt")

    tr_map = {"4w": 4, "8w": 8, "3m": 13, "6m": 26, "all": len(t_copy)}
    n_weeks = tr_map.get(st.session_state["time_range"], len(t_copy))
    t_filtered = t_copy.tail(n_weeks)

    flagged_spark   = t_filtered["flagged"].tolist()
    unflagged_spark = t_filtered["unflagged"].tolist()

    # ── KPI ROW — 5 cards with sparklines (Buildly style) ───────────────────
    kc1, kc2, kc3, kc4, kc5 = st.columns(5)
    with kc1:
        kpi_card_sparkline("💰", "Annual Revenue", f"₹{metrics['annual_revenue_inr_crore']} Cr",
                           "₹340 Cr", 7.0, flagged_spark, "#8b5cf6", "2.62M units/yr")
    with kc2:
        kpi_card_sparkline("🏗️", "Total RM Spend", f"₹{metrics['total_spend_inr_crore']} Cr",
                           "₹148 Cr", 9.0, unflagged_spark, "#e4e4e7", "44.4% of revenue")
    with kc3:
        spend_at_risk = metrics["spend_at_risk_inr_lakh"]
        kpi_card_sparkline("⚠️", "Spend at Risk", f"₹{spend_at_risk:,.0f} L",
                           "₹3,200 L", -31.2, list(reversed(flagged_spark)), "#8b5cf6",
                           f"{metrics['spend_at_risk_pct']:.1f}% of portfolio")
    with kc4:
        kpi_card_sparkline("🎯", "Synthetic Recall", f"{metrics['recall']*100:.0f}%",
                           "84%", 19.0, [70,75,80,85,90,95,100,100], "#22c55e", "Synthetic labels only")
    with kc5:
        kpi_card_sparkline("📐", "Synthetic Precision", f"{metrics['precision']*100:.0f}%",
                           "91%", 9.9, [80,84,88,92,96,100,100,100], "#fbbf24",
                           f"F1: {metrics['f1']:.3f}")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── MAIN CHART ROW — dual-axis trend (left 65%) + right panel (35%) ──────
    chart_col, right_col = st.columns([1.9, 1])

    with chart_col:
        with st.container(key="card_dash_chart"):
            card_header("Inbound Delay vs Portfolio Risk Score", "Flagged disruption delay (left axis) vs composite risk score avg (right axis) — hover for details")

            # Compute rolling avg risk for right axis
            avg_risk_series = []
            for i in range(len(t_filtered)):
                avg_risk_series.append(scores_df[scores_df["risk_band"].isin(["Critical","High"])]["composite_risk"].mean())

            # Slight noise so it looks like a trend
            np.random.seed(42)
            risk_series = [avg_risk_series[0] + np.random.uniform(-3, 3) for _ in range(len(t_filtered))]

            fig_dual = go.Figure()

            # Filled area — flagged delays (orange fill like Buildly)
            fig_dual.add_trace(go.Scatter(
                x=t_filtered["week_dt"], y=t_filtered["flagged"],
                name="Avg Delay — Flagged (Days)", mode="lines",
                line=dict(color="#8b5cf6", width=2.5),
                fill="tozeroy", fillcolor="rgba(139,92,246,0.12)",
                hovertemplate="<b>%{x|%d %b}</b><br>Flagged Delay: <b>%{y:.1f} days</b><extra></extra>",
                yaxis="y1"
            ))
            # White line — unflagged (like Buildly's secondary line)
            fig_dual.add_trace(go.Scatter(
                x=t_filtered["week_dt"], y=t_filtered["unflagged"],
                name="Avg Delay — Resilient (Days)", mode="lines",
                line=dict(color="#a1a1aa", width=1.8),
                hovertemplate="<b>%{x|%d %b}</b><br>Resilient Delay: <b>%{y:.1f} days</b><extra></extra>",
                yaxis="y1"
            ))
            # Dotted line — right axis risk score
            fig_dual.add_trace(go.Scatter(
                x=t_filtered["week_dt"], y=risk_series,
                name="Avg Risk Score (Crit+High)", mode="lines",
                line=dict(color="#8b5cf6", width=1.5, dash="dot"),
                hovertemplate="<b>%{x|%d %b}</b><br>Avg Risk: <b>%{y:.1f}</b><extra></extra>",
                yaxis="y2"
            ))

            # Vertical annotation dot (peak disruption marker — like Buildly orange dot)
            peak_idx = t_filtered["flagged"].idxmax()
            peak_x = t_filtered.loc[peak_idx, "week_dt"] if peak_idx in t_filtered.index else t_filtered["week_dt"].iloc[-1]
            peak_y = t_filtered["flagged"].max()
            fig_dual.add_trace(go.Scatter(
                x=[peak_x], y=[peak_y],
                mode="markers", name="Peak Disruption",
                marker=dict(color="#ef4444", size=10, symbol="circle",
                            line=dict(color=A("#ef444488"), width=6)),
                hovertemplate=f"<b>Peak Disruption</b><br>{peak_x.strftime('%d %b') if hasattr(peak_x,'strftime') else ''}<br>Delay: {peak_y:.1f}d<extra></extra>",
                showlegend=False, yaxis="y1"
            ))

            fig_dual.update_layout(**base(height=285,
                yaxis=dict(title=dict(text="Avg Delay (Days)", font=dict(size=9, color="#8b8b93")),
                           gridcolor="#27272a", zerolinecolor="#27272a", side="left"),
                yaxis2=dict(title=dict(text="Risk Score", font=dict(size=9, color=A("#8b5cf644"))),
                            overlaying="y", side="right", showgrid=False,
                            tickfont=dict(color=A("#8b5cf644"), size=8), range=[40, 90]),
                legend=dict(orientation="h", y=-0.18, x=0, font_size=9),
                xaxis=dict(gridcolor="#27272a", tickformat="%b %d"),
                hovermode="x unified"))
            st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})

    with right_col:
        # ── Traffic Sources style donut (matching Buildly right panel) ───────
        with st.container(key="card_dash_donut"):
            card_header("Risk Band Distribution")

            bands = metrics["band_counts"]
            labels = list(bands.keys())
            values = list(bands.values())
            bcolors = [_bc(b) for b in labels]

            fig_donut = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.62,
                marker=dict(colors=bcolors, line=dict(color="#0b0b0c", width=3)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value} suppliers · %{percent}<extra></extra>",
                direction="clockwise", sort=False
            ))
            total_s = sum(values)
            fig_donut.add_annotation(text=f"<b>{total_s}</b><br>Total",
                                     x=0.5, y=0.5, showarrow=False,
                                     font=dict(color="#f4f4f5", size=14, family="Inter"))
            fig_donut.update_layout(**base(height=180, showlegend=False, margin=dict(l=0,r=0,t=0,b=0)))
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

            # Legend below donut — like Buildly's "Organic 38%  ●  Paid 26%  ●  Direct 18%"
            for band, val in bands.items():
                c = _bc(band)
                pct = int(val / total_s * 100)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:3px 0;border-bottom:1px solid #222226;">
                  <span style="font-size:0.72rem;color:#8b8b93;">
                    <span style="color:{c};font-size:0.6rem;">●</span> {band}
                  </span>
                  <span style="font-size:0.72rem;font-weight:700;color:{c};">{pct}% ({val})</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── STRATEGY SIMULATOR — inline sliders (matches Buildly right panel) ─
        with st.container(key="card_dash_qs"):
            card_header("⚡ Quick Stress Test")

            sim_delay_q   = st.slider("🚢 Extra Delay (Days)", 0, 15, 0, 1, key="qs_delay")
            sim_drain_q   = st.slider("📉 Buffer Drain (%)", 0, 50, 0, 5, key="qs_drain")
            sim_geo_q     = st.slider("🌐 Geo Tension (%)", 0, 100, 0, 10, key="qs_geo")

            # Compute live impact
            sim_q = scores_df.copy()
            sim_q["sq_risk"] = np.round(
                0.35 * np.clip(scores_df["delivery_risk"] + sim_delay_q * 3.5, 0, 100) +
                0.25 * np.clip(scores_df["inventory_risk"] + sim_drain_q * 0.7, 0, 100) +
                0.20 * scores_df["production_risk"] +
                0.20 * np.clip(scores_df["supplier_risk"] * (1 + sim_geo_q / 100), 0, 100), 1
            )
            sim_q["sq_band"] = sim_q["sq_risk"].apply(
                lambda s: "Critical" if s >= 70 else ("High" if s >= 50 else ("Medium" if s >= 30 else "Low"))
            )
            new_crit_q = int((sim_q["sq_band"] == "Critical").sum())
            new_spend_q = sim_q[sim_q["sq_band"].isin(["Critical","High"])]["annual_spend_inr_lakh"].sum()
            base_spend  = metrics["spend_at_risk_inr_lakh"]
            delta_spend = new_spend_q - base_spend

            if sim_delay_q == 0 and sim_drain_q == 0 and sim_geo_q == 0:
                st.markdown("""<div style="font-size:0.72rem;color:#71717a;text-align:center;padding:6px 0;">
                  Move sliders to simulate disruption impact</div>""", unsafe_allow_html=True)
            else:
                c_crit = "#ef4444" if new_crit_q > 1 else "#8b5cf6"
                c_spend = "#ef4444" if delta_spend > 0 else "#22c55e"
                st.markdown(f"""
                <div style="margin-top:8px;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                  <div style="background:{c_crit}12;border:1px solid {c_crit}33;border-radius:8px;
                              padding:10px;text-align:center;">
                    <div style="font-size:0.65rem;color:#8b8b93;">Critical</div>
                    <div style="font-size:1.3rem;font-weight:800;color:{c_crit};">{new_crit_q}</div>
                  </div>
                  <div style="background:{c_spend}12;border:1px solid {c_spend}33;border-radius:8px;
                              padding:10px;text-align:center;">
                    <div style="font-size:0.65rem;color:#8b8b93;">Spend Risk Δ</div>
                    <div style="font-size:0.85rem;font-weight:800;color:{c_spend};">
                      {'+' if delta_spend>=0 else ''}₹{delta_spend:,.0f}L
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)


    # ── BOTTOM ROW — 3 cards like Aiq-ui second row ──────────────────────────
    section_label("THIS MONTH AT A GLANCE")
    b1, b2, b3, b4 = st.columns(4)

    weekly_spend = [12.1, 13.5, 14.2, 15.0, 13.8, 16.5, 14.9]
    weekly_delay = [2.1, 2.5, 3.1, 3.8, 4.2, 4.6, 5.1]
    weekly_cover = [22, 20, 18, 16, 15, 13, 12]
    weekly_prod  = [5, 8, 6, 12, 9, 15, 18]

    with b1:
        kpi_card_large("🏗️", "This Month · RM Spend", f"₹{metrics['total_spend_inr_crore']} Cr",
                       f"▲ 9.0% vs last month", f"Avg daily: ₹{float(metrics['total_spend_inr_crore'])*100/30:.1f}L",
                       weekly_spend, "#e4e4e7")
    with b2:
        kpi_card_large("🚨", "Active Disruption Suppliers", str(int(metrics["band_counts"].get("Critical",0)) + int(metrics["band_counts"].get("High",0))),
                       f"▲ {metrics['spend_at_risk_pct']:.1f}% portfolio at risk",
                       "S09 · S06 · S04 · S08",
                       weekly_delay, "#ef4444")
    with b3:
        kpi_card_large("📦", "Avg Days Cover (All SKUs)",
                       f"{mat_df['days_cover'].mean():.0f} Days",
                       f"▼ 2 SKUs below safety floor",
                       "RW02 · RW06 reorder NOW",
                       weekly_cover, "#fbbf24")
    with b4:
        kpi_card_large("⚙️", "Prod. Work Orders Delayed",
                       f"{scores_df['prod_delay_rate'].mean()*100:.1f}%",
                       f"▲ FA-1 · FA-3 overloaded",
                       "9 work centres monitored",
                       weekly_prod, "#8b5cf6")

    # ── SECOND BOTTOM ROW — 3 mini cards like Aiq-ui bottom ─────────────────
    section_label("LIVE OPERATIONS STATUS")
    sb1, sb2, sb3 = st.columns(3)

    with sb1:
        circular_progress("Monthly RM Budget vs Spend",
                          float(metrics["total_spend_inr_crore"]) / (float(metrics["annual_revenue_inr_crore"]) * 0.444 / 12) * 100,
                          f"₹{float(metrics['total_spend_inr_crore'])/12:.1f}Cr",
                          "of monthly plan", "#8b5cf6")

    with sb2:
        circular_progress("AI Recall Completeness",
                          metrics["recall"] * 100,
                          f"{metrics['recall']*100:.0f}%",
                          "disruptions caught", "#22c55e")

    with sb3:
        circular_progress("Delivery On-Time Rate",
                          100 - scores_df["recent_late_pct"].mean() * 100,
                          f"{100 - scores_df['recent_late_pct'].mean()*100:.1f}%",
                          "DIFOT compliance", "#8b5cf6")

    # ── Top Threats quick table ───────────────────────────────────────────────
    section_label("TOP DISRUPTION THREATS")
    threat_df = scores_df[scores_df["risk_band"].isin(["Critical","High","Medium"])][
        ["supplier_id","short_name","region","composite_risk","risk_band",
         "top_driver","recent_delay","min_days_cover","annual_spend_inr_lakh","sla"]
    ].copy()

    def _row_style(val):
        c = _bc(val); return f"background:{_bg(val)};color:{c};font-weight:700;"

    st.dataframe(
        threat_df.style
            .map(_row_style, subset=["risk_band"])
            .background_gradient(subset=["composite_risk"], cmap=HEAT, vmin=30, vmax=80)
            .format({"composite_risk":"{:.1f}","recent_delay":"{:.1f} d",
                     "min_days_cover":"{:.0f} d","annual_spend_inr_lakh":"₹{:.1f} L"}),
        use_container_width=True, height=240
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SUPPLIER RISK RADAR
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🎯 Supplier Risk Radar":
    top_bar("Supplier Disruption Radar")

    # ── Filters row ──────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        type_f = st.multiselect("Supplier Type", scores_df["supplier_type"].unique().tolist(),
                                default=scores_df["supplier_type"].unique().tolist())
    with fc2:
        band_f = st.multiselect("Risk Band", ["Critical","High","Medium","Low"],
                                default=["Critical","High","Medium","Low"])
    with fc3:
        reg_f = st.multiselect("Region", scores_df["region"].unique().tolist(),
                               default=scores_df["region"].unique().tolist())

    filt = scores_df[
        scores_df["supplier_type"].isin(type_f) &
        scores_df["risk_band"].isin(band_f) &
        scores_df["region"].isin(reg_f)
    ]

    st.markdown(f"<div style='font-size:0.72rem;color:#71717a;margin-bottom:10px;'>Showing <b style='color:#8b5cf6;'>{len(filt)}</b> of {len(scores_df)} suppliers</div>", unsafe_allow_html=True)

    # ── Horizontal risk bar chart (all suppliers) ─────────────────────────────
    srt = filt.sort_values("composite_risk", ascending=True)
    fig_hbar = go.Figure(go.Bar(
        x=srt["composite_risk"], y=srt["short_name"], orientation="h",
        marker=dict(color=[A(_bc(b) + "cc") for b in srt["risk_band"]],
                    line=dict(color=[_bc(b) for b in srt["risk_band"]], width=1)),
        text=[f"{v:.1f}" for v in srt["composite_risk"]], textposition="outside",
        textfont=dict(size=10, color="#a1a1aa"),
        customdata=srt[["supplier_id","risk_band","top_driver","city_state","annual_spend_inr_lakh"]].values,
        hovertemplate=(
            "<b>%{y}</b> (%{customdata[0]})<br>"
            "Score: <b>%{x:.1f}</b> · Band: <b>%{customdata[1]}</b><br>"
            "Driver: %{customdata[2]}<br>Location: %{customdata[3]}<br>"
            "Spend: ₹%{customdata[4]:.0f}L<extra></extra>"
        )
    ))
    dark_fig(fig_hbar, "Composite Risk Score — All Suppliers (Click bar to deep-dive below)", h=max(280, len(srt)*46))
    fig_hbar.update_layout(xaxis=dict(range=[0,105]), clickmode="event")
    st.plotly_chart(fig_hbar, use_container_width=True, config={"displayModeBar": False})

    section_label("SUPPLIER DEEP-DIVE")

    if len(filt) == 0:
        st.warning("No suppliers match filters.")
        st.stop()

    sel = st.selectbox("Select supplier for full diagnostic:",
        filt["supplier_id"].tolist(),
        format_func=lambda sid: f"{sid} — {scores_df.loc[scores_df['supplier_id']==sid,'short_name'].values[0]}  ({scores_df.loc[scores_df['supplier_id']==sid,'risk_band'].values[0]} · {scores_df.loc[scores_df['supplier_id']==sid,'composite_risk'].values[0]:.1f})"
    )
    sup = scores_df[scores_df["supplier_id"] == sel].iloc[0]
    bc  = _bc(sup["risk_band"])

    # ── Supplier header card ──────────────────────────────────────────────────
    sole_badge = f'<span style="background:#ef444418;border:1px solid #ef444444;color:#ef4444;border-radius:4px;padding:2px 8px;font-size:0.65rem;font-weight:700;margin-left:8px;">⚠ SOLE SOURCE</span>' if sup["is_sole_source"] else ""
    st.markdown(f"""
    <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid {bc}33;border-left:3px solid {bc};
                border-radius:18px;padding:16px 20px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">
        <span style="font-size:1.05rem;font-weight:800;color:#f4f4f5;">{sup['short_name']} ({sel})</span>
        {risk_badge_html(sup['risk_band'], sup['composite_risk'])}
        {sole_badge}
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;font-size:0.75rem;color:#8b8b93;">
        <div>📍 <b style="color:#a1a1aa;">{sup['city_state']}</b></div>
        <div>🏭 <b style="color:#a1a1aa;">{sup['supplier_type']}</b></div>
        <div>💰 <b style="color:#a1a1aa;">₹{sup['annual_spend_inr_lakh']:.0f}L</b> ({sup['share_of_rm_spend']*100:.1f}%)</div>
        <div>🧠 Driver: <b style="color:{bc};">{sup['top_driver'].upper()}</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 4 KPI mini cards ──────────────────────────────────────────────────────
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1: kpi_card_sparkline("🎯", "Composite Risk", f"{sup['composite_risk']:.1f}/100",
                                  "Baseline", 0, [20,30,45,55,65,sup['composite_risk']], bc)
    with mc2: kpi_card_sparkline("🚛", "Recent Delay", f"{sup['recent_delay']:.1f} Days",
                                  "Norm 2.1d", sup["delay_trend"]*15,
                                  [2.1,2.5,3.0,3.4,sup["recent_delay"]-0.3, sup["recent_delay"]], "#8b5cf6")
    with mc3: kpi_card_sparkline("📦", "Inv. Runway", f"{sup['min_days_cover']:.0f} Days",
                                  "Target 14d", (sup["min_days_cover"]-14)/14*100,
                                  [18,16,15,13,12,sup["min_days_cover"]], "#fbbf24")
    with mc4: kpi_card_sparkline("📉", "Late PO Rate", f"{sup['recent_late_pct']*100:.1f}%",
                                  "Benchmark 10%", (sup["recent_late_pct"]*100-10)/10*100,
                                  [10,12,18,22,28,sup["recent_late_pct"]*100], "#ef4444")

    r1, r2 = st.columns([1, 1.15])

    with r1:
        # ── Interactive Plotly Radar ──────────────────────────────────────────
        cats = ["Delivery", "Inventory", "Production", "Solvency"]
        vals = [sup["delivery_risk"], sup["inventory_risk"], sup["production_risk"], sup["supplier_risk"]]
        fig_rad = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor=A(f"{bc}20"),
            line=dict(color=bc, width=2.5),
            marker=dict(size=7, color=bc),
            hovertemplate="<b>%{theta}</b>: <b>%{r:.1f}</b><extra></extra>"
        ))
        fig_rad.update_layout(**PLOTLY_BASE, height=300,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0,100], gridcolor="#27272a", linecolor="#27272a",
                                tickfont=dict(size=8, color="#71717a")),
                angularaxis=dict(gridcolor="#27272a", tickfont=dict(size=10, color="#a1a1aa"))
            ),
            title=dict(text=f"Risk Radar — {sup['short_name']}", font=dict(color="#a1a1aa", size=11))
        )
        st.plotly_chart(fig_rad, use_container_width=True, config={"displayModeBar": False})

    with r2:
        # ── Diagnostic brief ─────────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid #27272a;border-radius:18px;padding:16px 18px;margin-bottom:10px;">
          <div style="font-size:0.68rem;color:#8b5cf699;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
            Autonomous Diagnostic Brief
          </div>
          <div style="font-size:0.82rem;color:#a1a1aa;line-height:1.6;">{sup['agent_brief']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.68rem;color:#71717a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;'>Mitigation Playbook</div>", unsafe_allow_html=True)
        for act in sup["recommended_actions"].split(" | "):
            st.markdown(f"""
            <div style="background:#101a12;border-left:2px solid #22c55e;border-radius:6px;
                        padding:7px 12px;margin-bottom:5px;font-size:0.8rem;color:#f4f4f5;">
              ✅ {act}
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""<div style="margin-top:10px;font-size:0.75rem;color:#71717a;">
          👤 <b style="color:#a1a1aa;">{sup['owner']}</b> &nbsp;|&nbsp; 📅 SLA: <b style="color:#a1a1aa;">{sup['sla']}</b>
        </div>""", unsafe_allow_html=True)
        if sup["override_applied"] == 1:
            st.warning(f"⚠️ Safety override triggered for {sup['short_name']} — sole-source risk.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — INVENTORY WATCH
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📦 Inventory Watch":
    top_bar("Inventory & Buffer Watch")

    ic1, ic2, ic3, ic4 = st.columns(4)
    weekly_val = [28,30,27,32,29,31,mat_df["inventory_value_lakh"].sum()]
    weekly_cov = [22,20,19,17,16,14,mat_df["days_cover"].mean()]
    with ic1:
        kpi_card_sparkline("🏛️","RM Inventory Value",f"₹{mat_df['inventory_value_lakh'].sum():.1f} L",
                           "₹31.0 L",-5.0, weekly_val, "#8b5cf6","16.2 days of RM spend")
    with ic2:
        kpi_card_sparkline("🚨","REORDER NOW",str(int(metrics["materials_below_reorder"])),
                           "0 last month",-100.0,[0,0,0,1,1,2,2],"#ef4444","RW02 · RW06 deficit")
    with ic3:
        kpi_card_sparkline("👁️","SKUs on WATCH","1","0 last month",-100.0,
                           [0,0,0,0,0,1,1],"#fbbf24","RW03 Aluminium ADC12")
    with ic4:
        kpi_card_sparkline("📦","Avg Days Cover",f"{mat_df['days_cover'].mean():.1f} d",
                           "18.0 d",-10.0, weekly_cov,"#22c55e","8,584 T annual req.")

    section_label("BUFFER RUNWAY vs REPLENISHMENT LEAD TIME")

    ms = mat_df.sort_values("inventory_risk", ascending=False)
    xlabels = ms["material_id"] + " — " + ms["short_name"]

    fig_m = go.Figure()
    fig_m.add_trace(go.Bar(
        name="On-Hand Buffer (Days)", x=xlabels,
        y=ms["days_cover"],
        marker=dict(color=["#ef4444" if d < lt else A("#8b5cf666")
                           for d, lt in zip(ms["days_cover"], ms["quoted_lead_time_days"])],
                    line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Buffer: <b>%{y:.1f}d</b><extra></extra>"
    ))
    fig_m.add_trace(go.Bar(
        name="Lead Time (Days)", x=xlabels,
        y=ms["quoted_lead_time_days"],
        marker=dict(color=A("#8b5cf622"), line=dict(color=A("#8b5cf644"), width=1.5)),
        hovertemplate="<b>%{x}</b><br>Lead Time: <b>%{y:.1f}d</b><extra></extra>"
    ))
    fig_m.add_hline(y=7, line_color="#ef4444", line_dash="dot",
                    annotation_text="7-Day Safety Floor", annotation_font_color="#ef4444",
                    annotation_position="top left")
    dark_fig(fig_m, "Inventory Buffer Runway vs Lead Time — Red bars = Below Safety Floor", h=350)
    fig_m.update_layout(barmode="group", xaxis_tickangle=-18, xaxis_tickfont=dict(size=9))
    st.plotly_chart(fig_m, use_container_width=True, config={"displayModeBar": False})

    # ── Circular ring cards for top risky materials ───────────────────────────
    section_label("MATERIAL RUNWAY STATUS")
    ring_cols = st.columns(5)
    for col, (_, row) in zip(ring_cols, ms.head(5).iterrows()):
        cover_pct = min(row["days_cover"] / max(row["quoted_lead_time_days"] * 2, 1) * 100, 100)
        c = "#ef4444" if row["status"] == "REORDER NOW" else ("#fbbf24" if row["status"] == "WATCH" else "#22c55e")
        with col:
            circular_progress(
                row["material_id"],
                cover_pct,
                f"{row['days_cover']:.0f}d",
                row["status"],
                c
            )

    section_label("MATERIAL HEALTH LEDGER")

    def _st_map(val):
        if val == "REORDER NOW": return "background:#ef444420;color:#ef4444;font-weight:700;"
        if val == "WATCH":       return "background:#fbbf2420;color:#fbbf24;font-weight:700;"
        return "background:#22c55e20;color:#22c55e;font-weight:700;"

    disp_cols = ["material_id","material_name","category","std_price_inr_per_kg",
                 "on_hand_units","avg_daily_usage","days_cover","quoted_lead_time_days",
                 "status","suggested_order_kg","suggested_order_lakh","inventory_risk"]
    st.dataframe(
        mat_df[disp_cols].style
            .background_gradient(subset=["inventory_risk"], cmap=HEAT, vmin=15, vmax=80)
            .map(_st_map, subset=["status"])
            .format({
                "std_price_inr_per_kg":"₹{:.1f}","on_hand_units":"{:,.0f} kg",
                "avg_daily_usage":"{:,.1f} kg/d","days_cover":"{:.1f} d",
                "quoted_lead_time_days":"{:.1f} d","suggested_order_kg":"{:,.0f} kg",
                "suggested_order_lakh":"₹{:.2f} L","inventory_risk":"{:.1f}"
            }),
        use_container_width=True, height=350
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MITIGATION COPILOT
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🤖 Mitigation Copilot":
    top_bar("Autonomous Mitigation Copilot")

    sel_col, btn_col = st.columns([2.5, 1])
    with sel_col:
        target_sid = st.selectbox(
            "Select At-Risk Supplier:",
            scores_df[scores_df["risk_band"].isin(["Critical","High","Medium"])]["supplier_id"].tolist(),
            format_func=lambda s: f"{s} — {scores_df.loc[scores_df['supplier_id']==s,'short_name'].values[0]}  ({scores_df.loc[scores_df['supplier_id']==s,'risk_band'].values[0]} · {scores_df.loc[scores_df['supplier_id']==s,'composite_risk'].values[0]:.1f})"
        )
    with btn_col:
        st.write(""); st.write("")
        run_agent = st.button("⚡ Generate Dossier", type="primary", use_container_width=True)

    sup_info = scores_df[scores_df["supplier_id"] == target_sid].iloc[0]
    bc = _bc(sup_info["risk_band"])
    sole_tag = f'<span style="background:#ef444418;border:1px solid #ef444444;color:#ef4444;border-radius:4px;padding:2px 8px;font-size:0.65rem;font-weight:700;margin-left:8px;">⚠ SOLE SOURCE</span>' if sup_info["is_sole_source"] else ""

    st.markdown(f"""
    <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid {bc}33;border-left:3px solid {bc};
                border-radius:18px;padding:14px 20px;margin:10px 0 14px;">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">
        <span style="font-size:1rem;font-weight:800;color:#f4f4f5;">
          {sup_info['supplier_name']} ({target_sid})
        </span>
        {risk_badge_html(sup_info['risk_band'], sup_info['composite_risk'])}
        {sole_tag}
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;font-size:0.74rem;color:#8b8b93;">
        <div>🏭 <b style="color:#a1a1aa;">{sup_info['supplier_type']}</b></div>
        <div>📍 <b style="color:#a1a1aa;">{sup_info['region']} ({sup_info['country']})</b></div>
        <div>💰 <b style="color:#a1a1aa;">₹{sup_info['annual_spend_inr_lakh']:.1f}L</b> ({sup_info['share_of_rm_spend']*100:.1f}%)</div>
        <div>🧠 Driver: <b style="color:{bc};">{sup_info['top_driver'].upper()}</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    prompt_ctx = f"""
SUPPLIER DOSSIER — MERIDIAN HOME APPLIANCES PVT LTD, PLANT 1 CHAKAN:
- ID: {sup_info['supplier_id']} ({sup_info['supplier_name']}) · {sup_info['city_state']}
- Type: {sup_info['supplier_type']} · Annual Spend: ₹{sup_info['annual_spend_inr_lakh']:.1f}L ({sup_info['share_of_rm_spend']*100:.1f}%)
- Composite Risk: {sup_info['composite_risk']:.1f}/100 ({sup_info['risk_band']}) · Driver: {sup_info['top_driver']}
- Delay: {sup_info['recent_delay']:.1f}d (trend {sup_info['delay_trend']:+.1f}d) · Late PO: {sup_info['recent_late_pct']*100:.1f}%
- Inv. Runway: {sup_info['min_days_cover']:.0f}d · Prod Impact: {sup_info['prod_delay_rate']*100:.1f}% WOs
- Solvency: {sup_info['financial_health_score']:.1f}/100 · Geo Risk: {sup_info['geo_risk']:.2f} · Sole Source: {sup_info['is_sole_source']}
"""
    section_label("AI OPERATIONS DOSSIER")

    llm_out = ""
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            with st.spinner("⚡ Gemini 2.5 Flash generating dossier..."):
                resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""You are an Autonomous Supply Chain AI Agent for Meridian Home Appliances (Plant 1 Chakan, Pune).
{prompt_ctx}
Generate a 3-part structured executive package in professional markdown:
## 1. Executive Root-Cause Analysis (RCA) & Plant Operational Impact
## 2. Formal Vendor Cure Notice (Contractual Letter to Vendor CEO/VP)
## 3. Autonomous Emergency Mitigation & PO Re-Routing Directives
Be specific about Meridian appliances (Fans, Mixer Grinders, Heaters), SKU names, SLA windows."""
                )
                llm_out = resp.text
        except Exception as e:
            st.error(f"Gemini error: {e}. Using built-in Reasoning Agent.")
            gemini_key = None

    if not gemini_key:
        llm_out = f"""
### 1. Executive Root-Cause Analysis (RCA) & Chakan Plant Operational Impact

**Primary Failure Vector: {sup_info['top_driver'].upper()} RISK ESCALATION**
- Inbound delivery delays expanded by **{sup_info['delay_trend']:+.1f} days**, reaching a mean of **{sup_info['recent_delay']:.1f} days** over the preceding 60-day window.
- Late fulfillment frequency: **{sup_info['recent_late_pct']*100:.1f}%** — triggering **{sup_info['prod_delay_rate']*100:.1f}%** downstream work-order slippages.
- Critical linked materials: only **{sup_info['min_days_cover']:.0f} days** buffer runway — line-down risk on FA-1 Fans & Coolers, FA-2 Kitchen Appliances.
- Annual spend exposure: **₹{sup_info['annual_spend_inr_lakh']:.1f} Lakhs** ({sup_info['share_of_rm_spend']*100:.1f}% of plant RM budget).
- Solvency: **{sup_info['financial_health_score']:.1f}/100** · Geo/freight risk index: **{sup_info['geo_risk']:.2f}** ({sup_info['region']}).

---

### 2. Formal Vendor Cure Notice

**TO:** Executive VP Operations — {sup_info['supplier_name']} ({sup_info['city_state']})
**FROM:** Autonomous Procurement Sentinel — Meridian Home Appliances Pvt Ltd, Plant 1 Chakan
**DATE:** {metrics['as_of']}
**SUBJECT: FORMAL SLA BREACH & MANDATORY CURE NOTICE — VENDOR {sup_info['supplier_id']}**

Over the past 60-day rolling audit window consignments averaged **{sup_info['recent_delay']:.1f} days** late, with **{sup_info['recent_late_pct']*100:.1f}%** of batches breaching DIFOT.

**CURE DIRECTIVES (SLA: {sup_info['sla']}):**
1. Expedited shipment recovery schedule within **48 hours** for all pending POs.
2. Express freight conversion at supplier expense to clear backlog.
3. Formal 30-day CAPA report — tier-2 material availability & production stability.

Failure triggers liquidated damages and quota reallocation to secondary partners.

*— {sup_info['owner']} · Meridian Supply Chain Governance Board*

---

### 3. Autonomous Emergency Mitigation & PO Re-Routing

- **DIRECTIVE-01:** {'EXPEDITE DUAL-SOURCING — qualify emergency secondary suppliers immediately (sole-source risk).' if sup_info['is_sole_source'] else 'Divert 40% future allocation to pre-qualified secondary vendor.'}
- **DIRECTIVE-02:** Release expedited PO to restore buffer above quoted lead time.
- **DIRECTIVE-03:** Re-sequence FA-1, FA-2, FA-3 lines to prioritise batches with >25 days cover.
- **DIRECTIVE-04:** Elevate ERP safety stock parameter from 7 → **14 days** for all linked SKUs.
- **Status:** DISPATCHED → SAP S/4HANA & SRM · Owner: **{sup_info['owner']}** · SLA: **{sup_info['sla']}**
"""

    with st.container(key="card_copilot"):
        st.markdown(llm_out)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — SCENARIO SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🧪 Scenario Simulator":
    top_bar("What-If Disruption Scenario Simulator")

    sc1, sc2 = st.columns([1.1, 1])

    with sc1:
        with st.container(key="card_sim_params"):
            card_header("🎛️ Disruption Shock Parameters")

            sim_delay   = st.slider("🚢 Shipping Delay Spike (Days)", 0, 15, 4, 1)
            sim_geo     = st.slider("🌐 Geopolitical Tension (%)", 0, 100, 30, 5)
            sim_drain   = st.slider("📉 Buffer Stock Depletion (%)", 0, 60, 25, 5)
            sim_sole    = st.checkbox("💥 Sole-Source Solvency Freeze (S09 / S10)", value=True)
            sim_weather = st.checkbox("🌧️ Monsoon Logistics Disruption (+2 Day Transit)", value=False)
            sim_strike  = st.checkbox("⚡ Taiwan Port Strike (S08 Pacific Plastics +20% Geo)", value=False)

            extra_delay = 2 if sim_weather else 0
            extra_geo   = 20 if sim_strike else 0

    # ── Compute ──────────────────────────────────────────────────────────────
    sim = scores_df.copy()
    tot_delay = sim_delay + extra_delay
    tot_geo   = sim_geo + extra_geo

    sim["sim_delivery_risk"] = np.clip(
        (0.40 * np.clip((sim["recent_delay"] + tot_delay) / 8.0, 0, 1) +
         0.30 * np.clip(sim["recent_late_pct"] / 0.65, 0, 1) +
         0.30 * np.clip((sim["delay_trend"] + tot_delay * 0.5) / 4.5, 0, 1)) * 100, 0, 100
    )
    sim["sim_inv_risk"] = np.clip(sim["inventory_risk"] + sim_drain * 0.75, 0, 100)
    sim["sim_sup_risk"] = np.clip(sim["supplier_risk"] * (1 + tot_geo / 100), 0, 100)
    if sim_sole:
        sim.loc[sim["is_sole_source"], "sim_sup_risk"] = np.clip(
            sim.loc[sim["is_sole_source"], "sim_sup_risk"] + 25, 0, 100)
    sim["sim_composite"] = np.round(
        0.35 * sim["sim_delivery_risk"] + 0.25 * sim["sim_inv_risk"] +
        0.20 * sim["production_risk"]   + 0.20 * sim["sim_sup_risk"], 1
    )
    sim["sim_band"] = sim["sim_composite"].apply(
        lambda s: "Critical" if s >= 70 else ("High" if s >= 50 else ("Medium" if s >= 30 else "Low"))
    )

    with sc2:
        new_crit = int((sim["sim_band"] == "Critical").sum())
        old_crit = int((scores_df["risk_band"] == "Critical").sum())
        new_sp   = sim[sim["sim_band"].isin(["Critical","High"])]["annual_spend_inr_lakh"].sum()
        old_sp   = metrics["spend_at_risk_inr_lakh"]

        with st.container(key="card_sim_impact"):
            card_header("📊 Simulated Portfolio Impact")

            kpi_card_sparkline("🔴","Critical Suppliers",str(new_crit),
                               str(old_crit), (new_crit-old_crit)*20,
                               [old_crit]*4 + [new_crit], "#ef4444")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            kpi_card_sparkline("💸","Spend at Risk",f"₹{new_sp:,.0f} L",
                               f"₹{old_sp:,.0f} L", (new_sp-old_sp)/old_sp*100 if old_sp else 0,
                               [old_sp/4]*3 + [old_sp*0.7, old_sp, new_sp], "#8b5cf6")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            pct_new = (new_sp / metrics["total_spend_inr_lakh"]) * 100
            pct_old = (old_sp / metrics["total_spend_inr_lakh"]) * 100
            kpi_card_sparkline("📈","Portfolio Exposure",f"{pct_new:.1f}%",
                               f"{pct_old:.1f}%", pct_new - pct_old,
                               [pct_old]*3 + [pct_old*1.1, pct_old*1.15, pct_new], "#fbbf24")

    section_label("BAND SHIFT COMPARISON")

    band_order = ["Critical","High","Medium","Low"]
    base_c = scores_df["risk_band"].value_counts().reindex(band_order).fillna(0)
    sim_c  = sim["sim_band"].value_counts().reindex(band_order).fillna(0)

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Baseline", x=band_order, y=base_c.values,
        marker=dict(color=[A(_bc(b) + "44") for b in band_order],
                    line=dict(color=[_bc(b) for b in band_order], width=1.5)),
        text=base_c.values.astype(int), textposition="outside",
        hovertemplate="<b>%{x}</b> (Baseline): <b>%{y}</b> suppliers<extra></extra>"
    ))
    fig_comp.add_trace(go.Bar(
        name="Stress Scenario", x=band_order, y=sim_c.values,
        marker=dict(color=[_bc(b) for b in band_order]),
        text=sim_c.values.astype(int), textposition="outside",
        hovertemplate="<b>%{x}</b> (Stress): <b>%{y}</b> suppliers<extra></extra>"
    ))
    dark_fig(fig_comp, "Supplier Risk Band — Baseline vs Stress Scenario", h=310)
    fig_comp.update_layout(barmode="group")
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})

    section_label("SUPPLIER-LEVEL DELTA")
    delta_df = pd.DataFrame({
        "Supplier": scores_df["short_name"],
        "Baseline Score": scores_df["composite_risk"],
        "Simulated Score": sim["sim_composite"],
        "Baseline Band": scores_df["risk_band"],
        "Simulated Band": sim["sim_band"],
        "Δ Score": (sim["sim_composite"] - scores_df["composite_risk"]).round(1)
    })
    def _bf(v): return f"background:{_bg(v)};color:{_bc(v)};font-weight:700;"
    st.dataframe(
        delta_df.style.map(_bf, subset=["Baseline Band","Simulated Band"])
            .background_gradient(subset=["Δ Score"], cmap=HEAT, vmin=0, vmax=35)
            .format({"Baseline Score":"{:.1f}","Simulated Score":"{:.1f}","Δ Score":"+{:.1f}"}),
        use_container_width=True, height=360
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — ACTION QUEUE
# Matches: Aiq-ui — card-based kanban-style layout with bell icons
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📋 Action Queue":
    top_bar("Action Queue & SLA Tracker")

    tot = len(action_df)
    c_n = len(action_df[action_df["risk_band"]=="Critical"])
    h_n = len(action_df[action_df["risk_band"]=="High"])
    m_n = len(action_df[action_df["risk_band"]=="Medium"])

    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1: kpi_card_sparkline("📋","Active Work Items",str(tot),"3 prev",(tot-3)/3*100,
                                  [2,3,3,4,4,5,tot],"#8b5cf6")
    with ac2: kpi_card_sparkline("🔴","Critical",str(c_n),"0 prev",-100.0,
                                  [0,0,0,0,1,1,c_n],"#ef4444","< 24h SLA")
    with ac3: kpi_card_sparkline("🟠","High Priority",str(h_n),"1 prev",(h_n-1)*100,
                                  [0,1,1,2,2,3,h_n],"#8b5cf6","< 3-day SLA")
    with ac4: kpi_card_sparkline("🟡","Medium Watch",str(m_n),"1 prev",(m_n-1)*100,
                                  [0,0,1,1,2,2,m_n],"#fbbf24","< 2-week SLA")

    section_label("KANBAN ACTION BOARD")

    # ── Kanban-style cards ────────────────────────────────────────────────────
    kc1, kc2, kc3 = st.columns(3)
    col_map = {"Critical": kc1, "High": kc2, "Medium": kc3}
    hdr_map = {"Critical": ("🔴","CRITICAL","#ef4444"),
               "High":     ("🟠","HIGH","#8b5cf6"),
               "Medium":   ("🟡","MEDIUM","#fbbf24")}

    # Column headers
    for band, col in col_map.items():
        ico, lbl, c = hdr_map[band]
        cnt = len(action_df[action_df["risk_band"]==band])
        with col:
            st.markdown(f"""
            <div style="background:{c}12;border:1px solid {c}33;border-radius:14px;
                        padding:10px 14px;margin-bottom:10px;display:flex;
                        justify-content:space-between;align-items:center;">
              <span style="font-size:0.75rem;font-weight:700;color:{c};">{ico} {lbl}</span>
              <span style="background:{c}22;border:1px solid {c}44;color:{c};
                           border-radius:18px;padding:1px 8px;font-size:0.7rem;font-weight:700;">
                {cnt}
              </span>
            </div>
            """, unsafe_allow_html=True)

    for _, row in action_df.iterrows():
        band = row["risk_band"]
        if band not in col_map: continue
        bc  = _bc(band)
        col = col_map[band]
        name  = row.get("short_name","")
        sid   = row.get("supplier_id","")
        score = row.get("composite_risk", 0)
        owner = row.get("owner","—")
        sla   = row.get("sla","—")
        driver= row.get("top_driver","—")
        spend = row.get("annual_spend_inr_lakh", 0)
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid {bc}28;border-left:3px solid {bc};
                        border-radius:14px;padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="font-size:0.82rem;font-weight:700;color:#f4f4f5;">{name}</div>
                <div style="font-size:0.68rem;color:{bc};font-weight:700;">🔔 {score:.1f}</div>
              </div>
              <div style="font-size:0.68rem;color:#71717a;margin-top:3px;">{sid}</div>
              <div style="height:1px;background:#27272a;margin:8px 0;"></div>
              <div style="font-size:0.7rem;color:#8b8b93;line-height:1.7;">
                <div>🧠 Driver: <b style="color:#a1a1aa;">{driver}</b></div>
                <div>💰 Spend: <b style="color:#a1a1aa;">₹{spend:.0f}L</b></div>
                <div>👤 Owner: <b style="color:#a1a1aa;">{owner}</b></div>
                <div>📅 SLA: <b style="color:{bc};">{sla}</b></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    section_label("FULL ACTION TABLE")
    def _aq_style(val): return f"background:{_bg(val)};color:{_bc(val)};font-weight:700;"
    st.dataframe(
        action_df.style.map(_aq_style, subset=["risk_band"]),
        use_container_width=True, height=300
    )
    col_dl, _ = st.columns([1, 4])
    with col_dl:
        st.download_button("📥 Export CSV", action_df.to_csv(index=False).encode("utf-8"),
                           "meridian_action_queue.csv", "text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — MODEL AUDIT
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📈 Model Audit":
    top_bar("Model Audit & Validation Limits")
    st.warning(
        "This project uses synthetic case-study data and generated disruption "
        "labels. Metrics describe agreement with those labels; they are not "
        "independently validated real-world predictive performance."
    )

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        kpi_card_sparkline("🎯", "Synthetic Recall", f"{metrics['recall']*100:.1f}%",
                           "", 0.0, [metrics["recall"]*100] * 7,
                           "#22c55e", "Synthetic labels only")
    with mc2:
        kpi_card_sparkline("✓", "Synthetic Precision", f"{metrics['precision']*100:.1f}%",
                           "", 0.0, [metrics["precision"]*100] * 7,
                           "#8b5cf6", "Not independently validated")
    with mc3:
        kpi_card_sparkline("📐", "F1 Score", f"{metrics['f1']:.3f}",
                           "", 0.0, [metrics["f1"]] * 7,
                           "#e4e4e7", "Descriptive diagnostic")
    with mc4:
        kpi_card_sparkline("🏷️", "Label Agreement", f"{metrics['accuracy']*100:.1f}%",
                           "", 0.0, [metrics["accuracy"]*100] * 7,
                           "#fbbf24", "Synthetic rule alignment")

    section_label("SYNTHETIC LABEL CONFUSION MATRIX")
    st.caption(
        "Counts compare the rule-based risk flag against the generated "
        "disruption label. They are not a test on independent historical events."
    )

    ml1, ml2, ml3, ml4 = st.columns([1.5, 1, 1, 1])
    with ml1:
        cm = np.array([
            [metrics["confusion"]["TN"], metrics["confusion"]["FP"]],
            [metrics["confusion"]["FN"], metrics["confusion"]["TP"]],
        ])
        fig_cm = go.Figure(go.Heatmap(
            z=cm,
            x=["Predicted: Normal", "Predicted: Disrupted"],
            y=["Label: Normal", "Label: Disrupted"],
            colorscale=[[0, "#151517"], [0.5, "rgba(139,92,246,0.25)"], [1, "#8b5cf6"]],
            showscale=False,
            text=cm,
            texttemplate="<b>%{text}</b>",
            textfont=dict(size=25, color="#f4f4f5"),
            hovertemplate="<b>%{y}</b><br>%{x}<br>Count: %{z}<extra></extra>",
        ))
        dark_fig(fig_cm, "Confusion Matrix", h=280)
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

    for col, (name, val, color) in zip(
        [ml2, ml3, ml4],
        [
            ("Recall", metrics["recall"] * 100, "#22c55e"),
            ("Precision", metrics["precision"] * 100, "#8b5cf6"),
            ("F1 Score", metrics["f1"] * 100, "#e4e4e7"),
        ],
    ):
        with col:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                number={"suffix": "%", "font": {"color": color, "size": 22}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont": {"color": "#71717a", "size": 8}},
                    "bar": {"color": color, "thickness": 0.18},
                    "bgcolor": "rgba(0,0,0,0)",
                    "bordercolor": "#27272a",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(239,68,68,0.03)"},
                        {"range": [50, 80], "color": "rgba(251,191,36,0.03)"},
                        {"range": [80, 100], "color": "rgba(34,197,94,0.03)"},
                    ],
                    "threshold": {"line": {"color": color, "width": 2}, "value": val},
                },
                title={"text": name, "font": {"color": "#8b8b93", "size": 11}},
            ))
            fig_g.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8b8b93"),
                height=230,
                margin=dict(l=14, r=14, t=35, b=10),
            )
            st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})

    section_label("EVALUATION INTERPRETATION")
    bench = pd.DataFrame({
        "Metric": ["Recall", "Precision", "F1 Score", "Label Agreement", "Evaluation Status"],
        "Score": [
            f"{metrics['recall']*100:.1f}%",
            f"{metrics['precision']*100:.1f}%",
            f"{metrics['f1']:.3f}",
            f"{metrics['accuracy']*100:.1f}%",
            "Not independently validated",
        ],
        "Interpretation": [
            "Agreement with generated positive labels",
            "Agreement among generated positive predictions",
            "Summary of synthetic-label agreement",
            "Agreement across this generated dataset",
            "Historical holdout testing is required",
        ],
    })
    st.dataframe(bench, use_container_width=True, height=240, hide_index=True)

    section_label("DATASET AND CASE-STUDY DISCLOSURE")
    st.markdown(
        """
        <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);
                    border:1px solid #27272a;border-radius:14px;padding:16px 20px;
                    font-size:0.82rem;color:#a1a1aa;">
          <p><b style="color:#c4b5fd;">Simulated case study:</b>
          Meridian Home Appliances is represented through generated operational
          records for suppliers, inventory, deliveries and production.</p>
          <p><b style="color:#c4b5fd;">Public benchmark reference:</b>
          DataCo Smart Supply Chain Analytics dataset:
          <a href="https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain"
             target="_blank" rel="noopener noreferrer">Kaggle dataset page</a>.</p>
          <p>Do not imply that the benchmark directly validates the generated
          case data unless a documented mapping and evaluation have been performed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — CONTROL TOWER
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🏛️ Control Tower":
    top_bar("AI Supply Chain Control Tower Blueprint")

    arch_path = os.path.join(FIG_DIR, "fig8_control_tower_macro.png")
    if os.path.exists(arch_path):
        st.image(arch_path,
                 caption="Figure 1A: Meridian Autonomous AI Supply Chain Control Tower — Macro Architecture",
                 use_container_width=True)

    section_label("CONTROL TOWER ENGINES")

    engines = [
        ("🔗","Vendor Telemetry Engine","Tracks OTD, delivery delays, defect rates, solvency scores, sole-source dependencies across 10 suppliers.","#8b5cf6"),
        ("🏗️","Procurement Engine","Optimizes ₹16,158L RM spend across 18 sourcing links — dual-sourcing splits & contract SLAs.","#e4e4e7"),
        ("📦","Inventory Engine","ABC classification · 10 raw materials · safety stock floors · reorder triggers (RW02 & RW06: REORDER NOW).","#fbbf24"),
        ("🚛","Inbound Logistics","Tracks 3,200 multi-modal consignments: Road · Rail+Road · Sea+Road (Kaohsiung → JNPT → Chakan).","#22c55e"),
        ("⚡","Risk Engine","Delivery (35%) + Inventory (25%) + MES Production (20%) + Vendor Solvency (20%) + sole-source override.","#8b5cf6"),
        ("🏭","Work Centre Governance","Balances 9 work centres — FA-1 Fans 109% Apr-27 · FA-3 Heating 106% Jan-27 peak overload.","#ef4444"),
        ("🤖","AI Decision Sentinel","Dispatches action tickets to ERP — <24h critical · <3d high · <2w medium response SLAs.","#8b5cf6"),
        ("🧠","LLM Mitigation Copilot","Google Gemini 2.5 Flash — authors RCA dossiers, vendor cure notices, PO re-routing directives.","#e4e4e7"),
    ]

    ec1, ec2 = st.columns(2)
    for i, (ico, title, desc, c) in enumerate(engines):
        with (ec1 if i % 2 == 0 else ec2):
            st.markdown(f"""
            <div style="background:linear-gradient(160deg,#1a1a1d 0%,#121214 100%);border:1px solid {c}22;border-left:3px solid {c};
                        border-radius:14px;padding:13px 16px;margin-bottom:8px;">
              <div style="font-size:0.84rem;font-weight:700;color:{c};margin-bottom:5px;">{ico} {title}</div>
              <div style="font-size:0.78rem;color:#8b8b93;line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    section_label("DECISION FLOWCHART")
    flow_path = os.path.join(FIG_DIR, "fig7_agentic_flowchart.png")
    if os.path.exists(flow_path):
        st.image(flow_path,
                 caption="Figure 1B: Meridian Chakan Plant Agentic Decision Flowchart",
                 use_container_width=True)

    section_label("SYSTEM ARCHITECTURE SUMMARY")
    arch_tbl = pd.DataFrame({
        "Layer": ["Data Ingestion","Risk Computation","Alert & Triage","LLM Reasoning","Human-in-Loop"],
        "Technology": ["TMS/WMS/MES/ERP telemetry","Python risk_engine.py — 4-pillar scoring",
                       "Rule-based action queue — human approval required","Google Gemini 2.5 Flash",
                       "Streamlit Command Center"],
        "SLA": ["Real-time / 24h batch","On-demand / Daily","< 5 min post-flag","< 30 sec","Analyst loop"],
        "Status": ["✅ Active","✅ Active","✅ Active","✅ Active","✅ Active"]
    })
    st.dataframe(arch_tbl, use_container_width=True, height=220)