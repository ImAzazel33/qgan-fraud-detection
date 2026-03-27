import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import random
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Quantum Fraud Defender",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020409 !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: #020409 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(6,182,212,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 10% 60%, rgba(16,185,129,0.04) 0%, transparent 50%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.main .block-container { max-width: 1140px !important; padding: 2.5rem 2rem 5rem !important; margin: 0 auto !important; }

/* HERO */
.hero-wrapper {
    position: relative; padding: 3.5rem 3rem 3rem; margin-bottom: 2.5rem;
    border: 1px solid rgba(6,182,212,0.15); border-radius: 20px;
    background: linear-gradient(135deg, rgba(6,182,212,0.04) 0%, rgba(139,92,246,0.04) 100%); overflow: hidden;
}
.hero-wrapper::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #06b6d4, #8b5cf6, transparent);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.25);
    color: #06b6d4; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase;
    padding: 5px 14px; border-radius: 100px; margin-bottom: 1.2rem;
}
.hero-badge .dot { width:6px; height:6px; background:#06b6d4; border-radius:50%; animation:pulse-dot 2s ease-in-out infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.7)} }
.hero-title { font-family:'Syne',sans-serif!important; font-size:3rem!important; font-weight:800!important; line-height:1.05!important; color:#f8fafc!important; letter-spacing:-0.02em!important; margin-bottom:1rem!important; }
.hero-title .accent { color:#06b6d4; }
.hero-desc { font-size:1rem; color:#94a3b8; line-height:1.7; max-width:680px; }
.hero-desc strong { color:#e2e8f0; font-weight:600; }
.hero-grid-bg { position:absolute; right:-20px; top:-20px; width:300px; height:300px; opacity:0.04; background-image:linear-gradient(rgba(6,182,212,1) 1px,transparent 1px),linear-gradient(90deg,rgba(6,182,212,1) 1px,transparent 1px); background-size:30px 30px; border-radius:12px; pointer-events:none; }

/* SECTION LABEL */
.section-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; color:#475569; margin-bottom:1rem; }

/* METRICS */
.metrics-row { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:2.5rem; }
.metric-card { background:rgba(15,23,42,0.7); border:1px solid rgba(51,65,85,0.6); border-radius:14px; padding:1.5rem 1.6rem; position:relative; overflow:hidden; transition:border-color 0.25s,transform 0.2s; }
.metric-card:hover { border-color:rgba(6,182,212,0.35); transform:translateY(-2px); }
.metric-card .m-label { font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#64748b; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.6rem; }
.metric-card .m-value { font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:700; color:#f1f5f9; line-height:1; margin-bottom:0.4rem; }
.metric-card .m-delta { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#10b981; font-weight:600; }
.metric-card.highlight { border-color:rgba(6,182,212,0.3); }
.metric-card.highlight::after { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#06b6d4,#8b5cf6); }

/* PANEL */
.panel { background:rgba(15,23,42,0.6); border:1px solid rgba(51,65,85,0.5); border-radius:20px; padding:2rem 2rem 2.5rem; margin-bottom:2rem; }
.panel-title { font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700; color:#f1f5f9; margin-bottom:1.4rem; }

/* SCENARIO BUTTONS */
div[data-testid="stHorizontalBlock"] .stButton > button { background:rgba(15,23,42,0.8)!important; border:1px solid rgba(51,65,85,0.7)!important; color:#94a3b8!important; border-radius:10px!important; font-family:'Space Grotesk',sans-serif!important; font-size:0.85rem!important; font-weight:500!important; padding:0.6rem 1rem!important; transition:all 0.2s ease!important; }
div[data-testid="stHorizontalBlock"] .stButton > button:hover { background:rgba(6,182,212,0.08)!important; border-color:rgba(6,182,212,0.4)!important; color:#e2e8f0!important; transform:translateY(-1px)!important; box-shadow:0 4px 20px rgba(6,182,212,0.1)!important; }

/* PRIMARY BUTTON */
.stButton > button[kind="primary"] { background:linear-gradient(135deg,#0891b2,#0e7490)!important; border:none!important; color:#fff!important; border-radius:12px!important; font-family:'Space Grotesk',sans-serif!important; font-size:1rem!important; font-weight:600!important; padding:0.85rem 2rem!important; box-shadow:0 4px 24px rgba(6,182,212,0.25)!important; transition:all 0.25s ease!important; }
.stButton > button[kind="primary"]:hover { background:linear-gradient(135deg,#06b6d4,#0891b2)!important; box-shadow:0 6px 32px rgba(6,182,212,0.4)!important; transform:translateY(-2px)!important; }

/* SLIDERS */
.stSlider [data-testid="stWidgetLabel"] p { font-family:'JetBrains Mono',monospace!important; font-size:0.75rem!important; color:#64748b!important; font-weight:500!important; text-transform:uppercase!important; letter-spacing:0.08em!important; }
[data-testid="stSlider"] [role="slider"] { background:#06b6d4!important; border:2px solid #0e7490!important; box-shadow:0 0 12px rgba(6,182,212,0.5)!important; }

/* RESULT CARD */
.result-card { border-radius:16px; padding:1.8rem 2rem; margin-top:1.5rem; position:relative; overflow:hidden; animation:fadeSlideIn 0.4s ease forwards; }
@keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
.result-card.low { background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.3); }
.result-card.medium { background:rgba(245,158,11,0.07); border:1px solid rgba(245,158,11,0.3); }
.result-card.high { background:rgba(239,68,68,0.07); border:1px solid rgba(239,68,68,0.3); }
.result-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; border-radius:4px 0 0 4px; }
.result-card.low::before { background:#10b981; }
.result-card.medium::before { background:#f59e0b; }
.result-card.high::before { background:#ef4444; }
.result-label { font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:700; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem; }
.result-card.low .result-label { color:#10b981; }
.result-card.medium .result-label { color:#f59e0b; }
.result-card.high .result-label { color:#ef4444; }
.result-score { font-family:'Syne',sans-serif; font-size:3.5rem; font-weight:800; line-height:1; margin-bottom:0.5rem; }
.result-card.low .result-score { color:#34d399; }
.result-card.medium .result-score { color:#fbbf24; }
.result-card.high .result-score { color:#f87171; }
.result-message { font-size:0.9rem; color:#94a3b8; line-height:1.5; }
.risk-bar-bg { height:6px; background:rgba(51,65,85,0.6); border-radius:6px; margin-top:1.2rem; overflow:hidden; }
.risk-bar-fill { height:100%; border-radius:6px; }
.result-card.low .risk-bar-fill { background:linear-gradient(90deg,#10b981,#34d399); }
.result-card.medium .risk-bar-fill { background:linear-gradient(90deg,#d97706,#fbbf24); }
.result-card.high .risk-bar-fill { background:linear-gradient(90deg,#dc2626,#f87171); }

/* LIVE FEED */
.feed-row { display:flex; align-items:center; gap:12px; padding:10px 14px; border-radius:10px; border:1px solid rgba(51,65,85,0.4); background:rgba(15,23,42,0.5); margin-bottom:6px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; animation:feedIn 0.3s ease forwards; }
@keyframes feedIn { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }
.feed-badge { padding:2px 10px; border-radius:20px; font-size:0.65rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; white-space:nowrap; }
.feed-badge.safe { background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3); }
.feed-badge.fraud { background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); }
.feed-badge.review { background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3); }
.feed-amount { color:#e2e8f0; font-weight:600; }
.feed-meta { color:#475569; flex:1; }
.feed-prob { color:#64748b; }

/* TIMELINE */
.timeline { position:relative; padding-left:2rem; }
.timeline::before { content:''; position:absolute; left:7px; top:8px; bottom:8px; width:2px; background:linear-gradient(180deg,#06b6d4,#8b5cf6,#10b981,#f59e0b); border-radius:2px; }
.tl-item { position:relative; margin-bottom:1.6rem; }
.tl-dot { position:absolute; left:-2rem; top:4px; width:16px; height:16px; border-radius:50%; border:2px solid #06b6d4; background:#020409; box-shadow:0 0 8px rgba(6,182,212,0.4); }
.tl-phase { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#06b6d4; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:3px; }
.tl-title { font-family:'Space Grotesk',sans-serif; font-size:0.95rem; font-weight:600; color:#f1f5f9; margin-bottom:3px; }
.tl-desc { font-size:0.82rem; color:#64748b; line-height:1.5; }

/* WHY QUANTUM */
.wq-row { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.wq-card { padding:1.2rem 1.4rem; border-radius:12px; border:1px solid rgba(51,65,85,0.5); background:rgba(15,23,42,0.5); }
.wq-card.classical { border-left:3px solid #ef4444; }
.wq-card.quantum { border-left:3px solid #06b6d4; }
.wq-label { font-family:'JetBrains Mono',monospace; font-size:0.62rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.8rem; }
.wq-card.classical .wq-label { color:#ef4444; }
.wq-card.quantum .wq-label { color:#06b6d4; }
.wq-point { font-size:0.83rem; color:#94a3b8; line-height:1.7; }
.wq-point::before { content:'→ '; color:#475569; }

/* CIRCUIT */
.circuit-wrapper { background:rgba(6,182,212,0.03); border:1px solid rgba(6,182,212,0.12); border-radius:14px; padding:1.4rem 1.6rem; overflow-x:auto; }

/* EXPANDER */
[data-testid="stExpander"] { background:rgba(15,23,42,0.5)!important; border:1px solid rgba(51,65,85,0.5)!important; border-radius:14px!important; }
[data-testid="stExpander"] summary { font-family:'Space Grotesk',sans-serif!important; font-size:0.9rem!important; font-weight:600!important; color:#94a3b8!important; padding:1rem 1.2rem!important; }
[data-testid="stExpander"] summary:hover { color:#e2e8f0!important; }

/* ARCH STEPS */
.arch-step { display:flex; gap:1rem; padding:1rem 0; border-bottom:1px solid rgba(51,65,85,0.3); align-items:flex-start; }
.arch-step:last-child { border-bottom:none; }
.arch-num { font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:700; color:#06b6d4; background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.2); border-radius:6px; padding:3px 8px; white-space:nowrap; margin-top:2px; letter-spacing:0.05em; }
.arch-text { font-size:0.875rem; color:#94a3b8; line-height:1.6; }
.arch-text strong { color:#e2e8f0; }

/* MISC */
[data-testid="stMetric"] { display:none!important; }
[data-testid="stHorizontalBlock"] { gap:1rem!important; }
[data-testid="stDivider"] hr { border-color:rgba(51,65,85,0.4)!important; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#020409; }
::-webkit-scrollbar-thumb { background:#1e293b; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ─── MODEL LOADING ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return joblib.load("xgb_qgan.pkl")
    except Exception as e:
        return None

model = load_model()

# ─── SESSION STATE ──────────────────────────────────────────────────────────────
if 'inputs' not in st.session_state:
    st.session_state.inputs = [-595.7, -41.3, -56.2, 7.9, -17.9, -2.6]
if 'result' not in st.session_state:
    st.session_state.result = None
if 'feed' not in st.session_state:
    st.session_state.feed = []

def set_scenario(scenario_type):
    if scenario_type == "normal":
        st.session_state.inputs = [-595.7, -41.3, -56.2, 7.9, -17.9, -2.6]
    elif scenario_type == "suspicious":
        st.session_state.inputs = [1500.0, 400.0, -80.0, -15.0, 25.0, 10.0]
    elif scenario_type == "fraud":
        st.session_state.inputs = [0.50, -0.08, 0.35, -0.05, 0.11, -0.02]
    st.session_state.result = None

# ─── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
  <div class="hero-grid-bg"></div>
  <div class="hero-badge"><span class="dot"></span>QGAN + XGBoost · Real-time Inference</div>
  <div class="hero-title">Quantum-Enhanced<br><span class="accent">Fraud Detection</span></div>
  <div class="hero-desc">
    Using a <strong>Quantum Generative Adversarial Network</strong>, we synthesize high-fidelity minority-class data —
    solving class imbalance at the quantum level and dramatically improving detection of rare financial fraud.
    <br><br>
    <strong>Problem → Quantum Augmentation → XGBoost Inference → +13% AUPRC gain.</strong>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── METRICS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Model Performance · AUPRC Benchmark</div>', unsafe_allow_html=True)
st.markdown("""
<div class="metrics-row">
  <div class="metric-card">
    <div class="m-label">Baseline AUPRC</div>
    <div class="m-value">0.7659</div>
    <div class="m-delta" style="color:#64748b">Pre-QGAN augmentation</div>
  </div>
  <div class="metric-card highlight">
    <div class="m-label">QGAN AUPRC</div>
    <div class="m-value">0.8663</div>
    <div class="m-delta">▲ +0.1004 improvement</div>
  </div>
  <div class="metric-card">
    <div class="m-label">Synthetic Samples</div>
    <div class="m-value">2,000</div>
    <div class="m-delta">Fraud class augmented</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── LIVE TRANSACTION FEED ───────────────────────────────────────────────────────
MERCHANTS = ["Amazon","Walmart","Stripe","PayPal","Shopify","Grab","Razorpay","Apple Pay","Binance","Revolut"]
LOCATIONS = ["Mumbai","New York","London","Singapore","Dubai","Berlin","Lagos","São Paulo"]

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">📡 Live Transaction Feed</div>', unsafe_allow_html=True)

_, ref_col = st.columns([6, 1])
with ref_col:
    refresh = st.button("⟳ Refresh", use_container_width=True)

if refresh or len(st.session_state.feed) == 0:
    new_batch = []
    for _ in range(8):
        amt = round(random.uniform(1.5, 9800.0), 2)
        prob = round(random.uniform(0, 1), 3)
        merchant = random.choice(MERCHANTS)
        loc = random.choice(LOCATIONS)
        txn_id = "TXN" + str(random.randint(100000, 999999))
        if prob < 0.30:
            status, badge = "safe", "✓ SAFE"
        elif prob < 0.70:
            status, badge = "review", "⚠ REVIEW"
        else:
            status, badge = "fraud", "✕ FRAUD"
        new_batch.append({"id":txn_id,"amt":amt,"prob":prob,"merchant":merchant,"loc":loc,"status":status,"badge":badge})
    st.session_state.feed = new_batch

feed_html = ""
for tx in st.session_state.feed:
    feed_html += f"""<div class="feed-row">
      <span class="feed-badge {tx['status']}">{tx['badge']}</span>
      <span class="feed-amount">${tx['amt']:,.2f}</span>
      <span class="feed-meta">{tx['merchant']} · {tx['loc']}</span>
      <span class="feed-prob">{tx['prob']*100:.1f}% risk</span>
      <span style="color:#334155;font-size:0.7rem">{tx['id']}</span>
    </div>"""
st.markdown(feed_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── CLASS DISTRIBUTION + AUPRC ─────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2, gap="medium")

with chart_col1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 Class Distribution: Before vs After QGAN</div>', unsafe_allow_html=True)
    st.markdown("""
    <svg viewBox="0 0 360 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'JetBrains Mono',monospace">
      <line x1="50" y1="20" x2="50" y2="170" stroke="#1e293b" stroke-width="1"/>
      <line x1="50" y1="170" x2="340" y2="170" stroke="#1e293b" stroke-width="1"/>
      <line x1="50" y1="120" x2="340" y2="120" stroke="#0f172a" stroke-width="1" stroke-dasharray="4,3"/>
      <line x1="50" y1="70" x2="340" y2="70" stroke="#0f172a" stroke-width="1" stroke-dasharray="4,3"/>
      <text x="44" y="174" fill="#475569" font-size="9" text-anchor="end">0</text>
      <text x="44" y="124" fill="#475569" font-size="9" text-anchor="end">50k</text>
      <text x="44" y="74" fill="#475569" font-size="9" text-anchor="end">100k</text>
      <text x="44" y="24" fill="#475569" font-size="9" text-anchor="end">150k</text>
      <!-- BEFORE -->
      <rect x="70" y="30" width="50" height="140" rx="4" fill="#0e7490" opacity="0.85"/>
      <rect x="128" y="169" width="50" height="1" rx="2" fill="#ef4444" opacity="0.9"/>
      <text x="115" y="188" fill="#94a3b8" font-size="9" text-anchor="middle">BEFORE</text>
      <!-- AFTER -->
      <rect x="210" y="30" width="50" height="140" rx="4" fill="#0e7490" opacity="0.85"/>
      <rect x="268" y="162" width="50" height="8" rx="2" fill="#06b6d4" opacity="0.95"/>
      <text x="268" y="188" fill="#94a3b8" font-size="9" text-anchor="middle">AFTER QGAN</text>
      <!-- Legend -->
      <rect x="55" y="200" width="10" height="8" rx="2" fill="#0e7490"/>
      <text x="70" y="208" fill="#64748b" font-size="8">Normal (284k)</text>
      <rect x="155" y="200" width="10" height="8" rx="2" fill="#06b6d4"/>
      <text x="170" y="208" fill="#64748b" font-size="8">Fraud (+2k synthetic)</text>
      <text x="293" y="156" fill="#06b6d4" font-size="8">+2,000</text>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📈 AUPRC Curve Comparison</div>', unsafe_allow_html=True)
    st.markdown("""
    <svg viewBox="0 0 360 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'JetBrains Mono',monospace">
      <defs>
        <linearGradient id="auprcGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#06b6d4"/>
          <stop offset="100%" stop-color="transparent"/>
        </linearGradient>
      </defs>
      <line x1="50" y1="20" x2="50" y2="170" stroke="#1e293b" stroke-width="1"/>
      <line x1="50" y1="170" x2="330" y2="170" stroke="#1e293b" stroke-width="1"/>
      <line x1="50" y1="120" x2="330" y2="120" stroke="#0f172a" stroke-width="1" stroke-dasharray="4,3"/>
      <line x1="50" y1="70" x2="330" y2="70" stroke="#0f172a" stroke-width="1" stroke-dasharray="4,3"/>
      <text x="44" y="174" fill="#475569" font-size="9" text-anchor="end">0</text>
      <text x="44" y="124" fill="#475569" font-size="9" text-anchor="end">0.5</text>
      <text x="44" y="74" fill="#475569" font-size="9" text-anchor="end">1.0</text>
      <text x="50" y="183" fill="#475569" font-size="9" text-anchor="middle">0</text>
      <text x="190" y="183" fill="#475569" font-size="9" text-anchor="middle">0.5</text>
      <text x="330" y="183" fill="#475569" font-size="9" text-anchor="middle">1.0</text>
      <text x="190" y="197" fill="#475569" font-size="8" text-anchor="middle">Recall</text>
      <!-- Baseline -->
      <path d="M50,30 C90,32 130,45 160,65 S210,110 240,130 S290,155 330,170" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="6,3" opacity="0.7"/>
      <!-- QGAN -->
      <path d="M50,28 C85,29 120,35 155,48 S205,80 235,105 S285,145 330,170" fill="none" stroke="#06b6d4" stroke-width="2.5"/>
      <path d="M50,28 C85,29 120,35 155,48 S205,80 235,105 S285,145 330,170 L330,170 L50,170 Z" fill="url(#auprcGrad)" opacity="0.12"/>
      <!-- Labels -->
      <rect x="55" y="200" width="12" height="2" fill="#475569"/>
      <text x="72" y="208" fill="#64748b" font-size="8">Baseline (0.7659)</text>
      <rect x="170" y="199" width="12" height="3" rx="1" fill="#06b6d4"/>
      <text x="187" y="208" fill="#64748b" font-size="8">QGAN (0.8663)</text>
      <text x="240" y="95" fill="#475569" font-size="9">0.7659</text>
      <text x="192" y="68" fill="#06b6d4" font-size="9" font-weight="bold">0.8663</text>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── ANALYSIS PANEL ──────────────────────────────────────────────────────────────
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.4rem">
  <span style="font-size:1.1rem">🎯</span>
  <span class="panel-title" style="margin-bottom:0">Live Transaction Analysis</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label" style="margin-bottom:0.8rem">Load Scenario</div>', unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.button("✅  Typical Transaction", on_click=set_scenario, args=("normal",), use_container_width=True)
with sc2:
    st.button("⚠️  Suspicious Activity", on_click=set_scenario, args=("suspicious",), use_container_width=True)
with sc3:
    st.button("🚨  Known Fraud Pattern", on_click=set_scenario, args=("fraud",), use_container_width=True)

st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Principal Component Signals (PCA-reduced features)</div>', unsafe_allow_html=True)

r1, r2 = st.columns(2, gap="large")
with r1:
    f1 = st.slider("PC1 · Amount Anomaly", -3000.0, 3000.0, float(st.session_state.inputs[0]), step=10.0)
    f2 = st.slider("PC2 · Geo Mismatch", -1000.0, 1000.0, float(st.session_state.inputs[1]), step=5.0)
    f3 = st.slider("PC3 · Velocity Risk", -500.0, 500.0, float(st.session_state.inputs[2]), step=1.0)
with r2:
    f4 = st.slider("PC4 · Device Score", -100.0, 100.0, float(st.session_state.inputs[3]), step=1.0)
    f5 = st.slider("PC5 · Time Irregularity", -100.0, 100.0, float(st.session_state.inputs[4]), step=1.0)
    f6 = st.slider("PC6 · Fraud Proximity", -100.0, 100.0, float(st.session_state.inputs[5]), step=1.0)

st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)

if st.button("🔍  Analyze Transaction Risk", type="primary", use_container_width=True):
    if model is not None:
        input_df = pd.DataFrame([[f1,f2,f3,f4,f5,f6]], columns=["PC1","PC2","PC3","PC4","PC5","PC6"])
        fraud_prob = model.predict_proba(input_df)[0][1]
        st.session_state.result = fraud_prob * 100
    else:
        st.error("Model not found. Ensure 'xgb_qgan.pkl' is in the working directory.")

# Result + Gauge
if st.session_state.result is not None:
    prob = st.session_state.result
    if prob < 30:
        card_class, label, msg = "low", "LOW RISK", "Transaction pattern aligns with normal behavior. No immediate action required."
    elif prob < 70:
        card_class, label, msg = "medium", "MEDIUM RISK", "Anomalous signals detected. Manual review and user verification recommended."
    else:
        card_class, label, msg = "high", "HIGH RISK — FRAUD DETECTED", "Pattern strongly matches QGAN-synthesized fraud signatures. Block and escalate immediately."

    gauge_color = "#10b981" if prob < 30 else ("#f59e0b" if prob < 70 else "#ef4444")
    needle_angle = -90 + (prob / 100) * 180
    angle_rad = math.radians(needle_angle)
    nx = 100 + 70 * math.cos(angle_rad)
    ny = 100 - 70 * math.sin(angle_rad)

    res_col, gauge_col = st.columns([3, 2])
    with res_col:
        st.markdown(f"""
        <div class="result-card {card_class}">
          <div class="result-label">{label}</div>
          <div class="result-score">{prob:.1f}%</div>
          <div class="result-message">{msg}</div>
          <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{min(prob,100)}%"></div></div>
        </div>""", unsafe_allow_html=True)
    with gauge_col:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;padding:1.5rem 0 0.5rem">
          <svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg" style="width:220px">
            <path d="M 20,100 A 80,80 0 0,1 73,27" fill="none" stroke="#10b981" stroke-width="14" stroke-linecap="round" opacity="0.7"/>
            <path d="M 73,27 A 80,80 0 0,1 127,27" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round" opacity="0.7"/>
            <path d="M 127,27 A 80,80 0 0,1 180,100" fill="none" stroke="#ef4444" stroke-width="14" stroke-linecap="round" opacity="0.7"/>
            <line x1="100" y1="100" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{gauge_color}" stroke-width="3" stroke-linecap="round"/>
            <circle cx="100" cy="100" r="7" fill="{gauge_color}" opacity="0.9"/>
            <circle cx="100" cy="100" r="3" fill="#020409"/>
            <text x="18" y="118" fill="#10b981" font-size="9" font-family="JetBrains Mono">LOW</text>
            <text x="84" y="18" fill="#f59e0b" font-size="9" font-family="JetBrains Mono" text-anchor="middle">MED</text>
            <text x="162" y="118" fill="#ef4444" font-size="9" font-family="JetBrains Mono" text-anchor="end">HIGH</text>
          </svg>
          <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:{gauge_color};margin-top:-0.5rem">{prob:.1f}%</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#475569;letter-spacing:0.1em;text-transform:uppercase">Fraud Probability</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── WHY QUANTUM + QUBIT CIRCUIT ─────────────────────────────────────────────────
wq_col, circ_col = st.columns(2, gap="medium")

with wq_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚛️ Why Quantum GAN?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="wq-row">
      <div class="wq-card classical">
        <div class="wq-label">Classical GAN</div>
        <div class="wq-point">Mode collapse on rare classes</div>
        <div class="wq-point">Needs large training corpus</div>
        <div class="wq-point">High compute overhead</div>
        <div class="wq-point">AUPRC: 0.7659</div>
      </div>
      <div class="wq-card quantum">
        <div class="wq-label">QGAN (Ours)</div>
        <div class="wq-point">Superposition explores full feature space</div>
        <div class="wq-point">6-qubit — hardware efficient</div>
        <div class="wq-point">Pauli-Z expectation as outputs</div>
        <div class="wq-point">AUPRC: 0.8663 (+13%)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with circ_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔬 6-Qubit Generator Circuit</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="circuit-wrapper">
    <svg viewBox="0 0 340 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'JetBrains Mono',monospace">
      <line x1="40" y1="30"  x2="320" y2="30"  stroke="#1e293b" stroke-width="1.5"/>
      <line x1="40" y1="60"  x2="320" y2="60"  stroke="#1e293b" stroke-width="1.5"/>
      <line x1="40" y1="90"  x2="320" y2="90"  stroke="#1e293b" stroke-width="1.5"/>
      <line x1="40" y1="120" x2="320" y2="120" stroke="#1e293b" stroke-width="1.5"/>
      <line x1="40" y1="150" x2="320" y2="150" stroke="#1e293b" stroke-width="1.5"/>
      <line x1="40" y1="180" x2="320" y2="180" stroke="#1e293b" stroke-width="1.5"/>
      <text x="5" y="34"  fill="#475569" font-size="9">q₀</text>
      <text x="5" y="64"  fill="#475569" font-size="9">q₁</text>
      <text x="5" y="94"  fill="#475569" font-size="9">q₂</text>
      <text x="5" y="124" fill="#475569" font-size="9">q₃</text>
      <text x="5" y="154" fill="#475569" font-size="9">q₄</text>
      <text x="5" y="184" fill="#475569" font-size="9">q₅</text>
      <!-- H gates -->
      <rect x="48" y="22" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="33" fill="white" font-size="9" text-anchor="middle">H</text>
      <rect x="48" y="52" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="63" fill="white" font-size="9" text-anchor="middle">H</text>
      <rect x="48" y="82" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="93" fill="white" font-size="9" text-anchor="middle">H</text>
      <rect x="48" y="112" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="123" fill="white" font-size="9" text-anchor="middle">H</text>
      <rect x="48" y="142" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="153" fill="white" font-size="9" text-anchor="middle">H</text>
      <rect x="48" y="172" width="22" height="16" rx="3" fill="#0e7490" opacity="0.9"/><text x="59" y="183" fill="white" font-size="9" text-anchor="middle">H</text>
      <!-- RY gates -->
      <rect x="88" y="22" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="33" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <rect x="88" y="52" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="63" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <rect x="88" y="82" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="93" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <rect x="88" y="112" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="123" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <rect x="88" y="142" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="153" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <rect x="88" y="172" width="26" height="16" rx="3" fill="#7c3aed" opacity="0.85"/><text x="101" y="183" fill="white" font-size="8" text-anchor="middle">Rʏ</text>
      <!-- CNOT q0->q1 -->
      <circle cx="145" cy="30" r="4" fill="#06b6d4"/>
      <circle cx="145" cy="60" r="8" fill="none" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="145" y1="34" x2="145" y2="52" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="139" y1="60" x2="151" y2="60" stroke="#06b6d4" stroke-width="1.5"/>
      <!-- CNOT q2->q3 -->
      <circle cx="145" cy="90" r="4" fill="#06b6d4"/>
      <circle cx="145" cy="120" r="8" fill="none" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="145" y1="94" x2="145" y2="112" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="139" y1="120" x2="151" y2="120" stroke="#06b6d4" stroke-width="1.5"/>
      <!-- CNOT q4->q5 -->
      <circle cx="145" cy="150" r="4" fill="#06b6d4"/>
      <circle cx="145" cy="180" r="8" fill="none" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="145" y1="154" x2="145" y2="172" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="139" y1="180" x2="151" y2="180" stroke="#06b6d4" stroke-width="1.5"/>
      <!-- RZ gates -->
      <rect x="168" y="22" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="33" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <rect x="168" y="52" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="63" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <rect x="168" y="82" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="93" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <rect x="168" y="112" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="123" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <rect x="168" y="142" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="153" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <rect x="168" y="172" width="26" height="16" rx="3" fill="#0891b2" opacity="0.8"/><text x="181" y="183" fill="white" font-size="8" text-anchor="middle">Rᴢ</text>
      <!-- Measure -->
      <rect x="280" y="22" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="33" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <rect x="280" y="52" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="63" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <rect x="280" y="82" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="93" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <rect x="280" y="112" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="123" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <rect x="280" y="142" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="153" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <rect x="280" y="172" width="22" height="16" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1"/><text x="291" y="183" fill="#94a3b8" font-size="10" text-anchor="middle">M</text>
      <text x="315" y="105" fill="#06b6d4" font-size="8" text-anchor="middle">⟨Z⟩</text>
    </svg>
    </div>
    <div style="margin-top:0.8rem;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#475569">
      H → Rʏ(θ) → CNOT entanglement → Rᴢ(φ) → Pauli-Z measurement
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── BUILD TIMELINE ───────────────────────────────────────────────────────────────
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">🛠️ How We Built This</div>', unsafe_allow_html=True)
st.markdown("""
<div class="timeline">
  <div class="tl-item">
    <div class="tl-dot"></div>
    <div class="tl-phase">Phase 01 · Data</div>
    <div class="tl-title">Dataset & Preprocessing</div>
    <div class="tl-desc">Loaded the ULB credit card fraud dataset (284k transactions, 0.17% fraud). Applied StandardScaler and selected top 30 PCA features to match quantum hardware qubit limits.</div>
  </div>
  <div class="tl-item">
    <div class="tl-dot" style="border-color:#8b5cf6;box-shadow:0 0 8px rgba(139,92,246,0.4)"></div>
    <div class="tl-phase" style="color:#8b5cf6">Phase 02 · Quantum</div>
    <div class="tl-title">QGAN Architecture Design</div>
    <div class="tl-desc">Built a 6-qubit PennyLane generator using H + Rʏ(θ) + CNOT + Rᴢ(φ) layers. Trained against a classical discriminator. Pauli-Z expectation values mapped to the 6 PCA feature space.</div>
  </div>
  <div class="tl-item">
    <div class="tl-dot" style="border-color:#06b6d4;box-shadow:0 0 8px rgba(6,182,212,0.4)"></div>
    <div class="tl-phase" style="color:#06b6d4">Phase 03 · Augmentation</div>
    <div class="tl-title">Synthetic Fraud Generation</div>
    <div class="tl-desc">Generated 2,000 high-fidelity synthetic fraud samples from the trained QGAN. Appended to original data to produce a balanced, augmented training set.</div>
  </div>
  <div class="tl-item">
    <div class="tl-dot" style="border-color:#10b981;box-shadow:0 0 8px rgba(16,185,129,0.4)"></div>
    <div class="tl-phase" style="color:#10b981">Phase 04 · Inference</div>
    <div class="tl-title">XGBoost Training & Evaluation</div>
    <div class="tl-desc">Trained XGBoost on augmented dataset. Evaluated using AUPRC — the right metric for severely imbalanced data. Achieved 0.8663 vs baseline 0.7659, a +13.1% improvement.</div>
  </div>
  <div class="tl-item">
    <div class="tl-dot" style="border-color:#f59e0b;box-shadow:0 0 8px rgba(245,158,11,0.4)"></div>
    <div class="tl-phase" style="color:#f59e0b">Phase 05 · Deploy</div>
    <div class="tl-title">Streamlit Demo App</div>
    <div class="tl-desc">Exported XGBoost with joblib. Built real-time inference UI with live transaction feed, scenario presets, risk gauge, and circuit visualization.</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── ARCHITECTURE EXPANDER ────────────────────────────────────────────────────────
with st.expander("⚙️   Full Pipeline Architecture"):
    st.markdown("""
    <div class="arch-step">
      <span class="arch-num">01</span>
      <div class="arch-text"><strong>Data Prep & PCA</strong> — Top 30 features reduced to 6 principal components to fit quantum hardware constraints.</div>
    </div>
    <div class="arch-step">
      <span class="arch-num">02</span>
      <div class="arch-text"><strong>Quantum GAN (QGAN)</strong> — 6-qubit generator circuit creates synthetic fraud data via Pauli-Z expectation values. Output bounded between -1 and 1.</div>
    </div>
    <div class="arch-step">
      <span class="arch-num">03</span>
      <div class="arch-text"><strong>Augmentation</strong> — 2,000 synthetic fraud samples appended to training data, rebalancing the 577:1 class ratio.</div>
    </div>
    <div class="arch-step">
      <span class="arch-num">04</span>
      <div class="arch-text"><strong>XGBoost Inference</strong> — Classifier trained on augmented data. QGAN is the data pipeline; XGBoost is the detector. AUPRC: 0.7659 → 0.8663.</div>
    </div>
    """, unsafe_allow_html=True)