import streamlit as st
import requests
import time
import re
import os
import threading

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="FinFraud Investigation Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── DARK THEME CSS ───────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #080d19 !important; color: #e2e8f0 !important; }
.block-container { padding: 0 2.5rem 3rem 2.5rem !important; max-width: 1360px !important; }

/* ── hide chrome ── */
#MainMenu, footer, header,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stHeader"],
div[data-testid="stStatusWidget"],
.stDeployButton,
div[data-testid="collapsedControl"],
section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }

/* ── reset spacing ── */
div[data-testid="stEmpty"] { display: none !important; min-height: 0 !important; height: 0 !important; padding: 0 !important; margin: 0 !important; }
div[data-testid="stHorizontalBlock"] { margin-top: 0 !important; padding-top: 0 !important; }
div[data-testid="column"] > div:empty { display: none !important; }
.main .block-container { padding-top: 0 !important; margin-top: 0 !important; }
div[data-testid="stAppViewBlockContainer"] { padding-top: 0 !important; }
div[data-testid="stVerticalBlock"] > div:empty { display: none !important; min-height: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }
div[data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }
.element-container { margin: 0 !important; padding: 0 !important; }

/* ── header action pill buttons ── */
[data-testid="column"]:nth-child(2) .stButton > button,
[data-testid="column"]:nth-child(3) .stButton > button {
    background: transparent !important;
    color: #f87171 !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    box-shadow: none !important;
    font-size: 0.74rem !important;
    padding: 0.45rem 0.9rem !important;
    margin-top: 1.2rem !important;
    font-weight: 600 !important;
    width: auto !important;
    border-radius: 20px !important;
}
[data-testid="column"]:nth-child(2) .stButton > button:hover,
[data-testid="column"]:nth-child(3) .stButton > button:hover {
    background: rgba(248,113,113,0.08) !important;
    box-shadow: none !important;
    transform: none !important;
}           

/* ── selectbox ── */
div[data-testid="stSelectbox"] > div > div {
    background: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] .st-emotion-cache-ue6h4q { display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }
div[data-testid="stSelectbox"] svg { fill: #64748b !important; }
[data-baseweb="popover"] { background: #111827 !important; border: 1px solid #1e293b !important; }
[data-baseweb="popover"] li { color: #e2e8f0 !important; background: #111827 !important; }
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] li[aria-selected="true"] { background: #1e293b !important; }
[data-baseweb="menu"],
[data-baseweb="menu"] ul { background: #111827 !important; }
ul[role="listbox"] { background: #111827 !important; border: 1px solid #1e293b !important; }
ul[role="listbox"] li { color: #e2e8f0 !important; background: #111827 !important; }
ul[role="listbox"] li:hover { background: #1e293b !important; }
ul[role="listbox"] li[aria-selected="true"] { background: #1e293b !important; }


/* ── primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #2dd4bf, #14b8a6) !important;
    color: #021a17 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 2px 12px rgba(45,212,191,0.25) !important;
    transition: all 0.18s ease !important;
    margin-top: 0.6rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5eead4, #2dd4bf) !important;
    box-shadow: 0 4px 20px rgba(45,212,191,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── hero ── */
.hero-wrap {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-top: 2px solid #2dd4bf;
    border-radius: 16px;
    padding: 3rem 2rem 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 0 60px rgba(45,212,191,0.04);
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 120px;
    background: radial-gradient(ellipse, rgba(45,212,191,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    color: #f1f5f9;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.8rem 0;
    line-height: 1.15;
}
.hero-tagline {
    color: #64748b;
    font-size: 0.9rem;
    line-height: 1.75;
    max-width: 560px;
    margin: 0 auto 1.85rem auto;
}
.flow-container { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 0; }
.flow-node { border-radius: 8px; padding: 0.42rem 1.1rem; font-size: 0.78rem; font-weight: 600; }
.fn-teal   { background: rgba(45,212,191,0.08);  color: #2dd4bf; border: 1px solid rgba(45,212,191,0.2); }
.fn-amber  { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.fn-orange { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.flow-arrow { color: #334155; padding: 0 0.7rem; font-size: 1.1rem; font-weight: 500; }

/* ── post-investigation header ── */
.page-header {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
}
.page-breadcrumb {
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.page-breadcrumb span { color: #94a3b8; }
.header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.header-left { display: flex; align-items: center; gap: 1rem; }
.header-vendor {
    color: #f1f5f9;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.header-badge-high {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(248,113,113,0.1);
    border: 1px solid rgba(248,113,113,0.25);
    color: #f87171;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
}
.header-badge-medium {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.25);
    color: #fbbf24;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
}
.header-badge-low {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(52,199,121,0.1);
    border: 1px solid rgba(52,199,121,0.25);
    color: #34c779;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
}
.header-meta {
    color: #475569;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.header-meta .sep { color: #334155; }
.header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.header-lastrun {
    color: #64748b;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-align: right;
    line-height: 1.5;
}
.header-lastrun strong {
    display: block;
    color: #94a3b8;
    font-weight: 600;
}

/* ── metric cards ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card-dark {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.25rem 1.35rem;
    position: relative;
}
.metric-card-dark.accent-red { border-left: 3px solid #f87171; }
.metric-card-dark.accent-amber { border-left: 3px solid #fbbf24; }
.metric-card-dark.accent-green { border-left: 3px solid #34c779; }
.mc-label {
    color: #64748b;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.mc-value {
    font-size: 1.8rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
}
.mc-value.red { color: #f87171; }
.mc-value.green { color: #34c779; }
.mc-value.amber { color: #fbbf24; }
.mc-value.white { color: #f1f5f9; }
.mc-desc {
    color: #475569;
    font-size: 0.72rem;
    margin-top: 0.3rem;
}

/* ── card ── */
.card {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.6rem 1.75rem;
    margin-bottom: 2rem;
}

/* ── section label ── */
.section-label {
    color: #64748b;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── invoice card header ── */
.inv-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}
.inv-card-title-wrap {}
.inv-card-subtitle {
    color: #64748b;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.inv-card-vendor {
    color: #f1f5f9;
    font-size: 1.1rem;
    font-weight: 700;
}

/* ── field grid ── */
.field-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9rem; margin-bottom: 0.9rem; }
.field-wrap { display: flex; flex-direction: column; gap: 0.3rem; }
.field-label {
    color: #64748b;
    font-size: 0.66rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
}
.field-value {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 7px;
    padding: 0.55rem 0.85rem;
    color: #e2e8f0;
    font-size: 0.9rem;
    font-weight: 500;
}
.field-danger {
    background: rgba(248,113,113,0.06);
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 7px;
    padding: 0.55rem 0.85rem;
    color: #f87171;
    font-size: 0.9rem;
    font-weight: 600;
}
.field-danger-note {
    color: #f87171;
    font-size: 0.68rem;
    margin-top: 0.2rem;
    font-weight: 500;
}

/* ── risk banner ── */
.risk-banner { border-radius: 9px; padding: 0.8rem 1.1rem; font-weight: 700; font-size: 1rem; margin-bottom: 1.1rem; }
.rb-high   { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.rb-medium { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.rb-low    { background: rgba(52,199,121,0.08);   color: #34c779; border: 1px solid rgba(52,199,121,0.2); }

/* ── tags ── */
.tag { display: inline-block; border-radius: 20px; padding: 0.25rem 0.75rem; font-size: 0.74rem; font-weight: 600; margin: 0.15rem 0.2rem 0.15rem 0; }
.tag-red    { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.tag-amber  { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.tag-teal   { background: rgba(52,199,121,0.08);  color: #34c779; border: 1px solid rgba(52,199,121,0.2); }

/* ── dialog metrics ── */
.metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9rem; margin: 1.1rem 0; }
.metric-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1rem 0.75rem;
    text-align: center;
}
.metric-value { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; }
.metric-label { font-size: 0.64rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.25rem; }

/* ── explanation ── */
.explanation-box {
    background: rgba(45,212,191,0.04);
    border-left: 3px solid #2dd4bf;
    border-radius: 0 7px 7px 0;
    padding: 0.9rem 1.1rem;
    color: #94a3b8;
    font-size: 0.88rem;
    line-height: 1.75;
    margin-top: 1.1rem;
}

/* ── SAR ── */
.sar-outer {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.75rem 1.75rem 1.25rem 1.75rem;
    margin-top: 1.25rem;
}
.sar-header-row {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid #1e293b;
}
.sar-badge {
    background: rgba(45,212,191,0.08);
    border: 1px solid rgba(45,212,191,0.2);
    color: #2dd4bf;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    padding: 0.3rem 0.75rem; border-radius: 20px;
}
.sar-inv-id { color: #64748b; font-size: 0.75rem; }
.sar-section {
    margin-bottom: 1.5rem;
    padding: 1rem 1.25rem;
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
}
.sar-sec-title {
    color: #e2e8f0;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid #1e293b;
}
.sar-sec-body { color: #94a3b8; font-size: 0.85rem; line-height: 1.85; }
.sar-sec-body .sar-item { display: flex; gap: 0.6rem; margin-bottom: 0.65rem; align-items: flex-start; padding: 0.3rem 0; }
.sar-sec-body .sar-bullet { width: 5px; height: 5px; border-radius: 50%; background: #2dd4bf; flex-shrink: 0; margin-top: 0.5rem; }
.sar-sec-body .sar-item-label { color: #e2e8f0; font-weight: 600; font-size: 0.82rem; }
.sar-sec-body .sar-item-value { color: #94a3b8; font-size: 0.82rem; line-height: 1.7; }

/* ── trace ── */
.trace-card {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.4rem 1.25rem;
}
.trace-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 1.2rem;
}
.trace-status {
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 600;
}
.trace-step { display: flex; align-items: flex-start; gap: 0.7rem; margin-bottom: 1rem; }
.trace-dot { width: 9px; height: 9px; border-radius: 50%; margin-top: 0.26rem; flex-shrink: 0; }
.td-pending { background: #334155; border: 1px solid #475569; }
.td-active  { background: #2dd4bf; box-shadow: 0 0 10px rgba(45,212,191,0.4); }
.td-done    { background: #22c55e; box-shadow: 0 0 4px rgba(34,197,94,0.3); }
.ts-name    { font-size: 0.8rem; font-weight: 600; line-height: 1.3; }
.ts-pending { color: #475569; }
.ts-active  { color: #2dd4bf; }
.ts-done    { color: #e2e8f0; }

.tool-divider { border-top: 1px solid #1e293b; margin: 0.9rem 0; }
.tool-item {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.55rem 0.85rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-size: 0.78rem;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    background: #111827;
    border: 1px solid #1e293b;
    color: #94a3b8;
}

/* ── investigation spinner ── */
.inv-card {
    background: #0f1628;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 3.5rem 2rem;
    text-align: center;
    min-height: 360px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.inv-ring {
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 3px solid rgba(45,212,191,0.12);
    border-top-color: #2dd4bf;
    animation: spin 0.85s linear infinite;
    margin: 0 auto 1.4rem auto;
    box-shadow: 0 0 16px rgba(45,212,191,0.1);
}
@keyframes spin { to { transform: rotate(360deg); } }
.inv-label { color: #f1f5f9; font-weight: 700; font-size: 1.15rem; margin-bottom: 0.5rem; letter-spacing: -0.01em; }
.inv-msg   { color: #64748b; font-size: 0.88rem; min-height: 1.3em; }
.inv-step-dots { display: flex; gap: 0.5rem; margin-top: 1.5rem; justify-content: center; }
.inv-step-dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(45,212,191,0.15); transition: background 0.3s; }
.inv-step-dot.active { background: #2dd4bf; box-shadow: 0 0 6px rgba(45,212,191,0.3); }

/* ── dialog ── */
div[data-testid="stDialog"] > div > div {
    background: #0f1628 !important;
    border: 1px solid #1e293b !important;
    border-radius: 16px !important;
    max-width: 860px !important;
    box-shadow: 0 24px 80px rgba(0,0,0,0.5) !important;
}
div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2,
div[data-testid="stDialog"] [role="dialog"] h2,
div[data-testid="stDialog"] .st-emotion-cache-10trblm {
    color: #f1f5f9 !important;
    font-weight: 800 !important;
    font-size: 1.35rem !important;
    letter-spacing: -0.02em !important;
}

/* ── error ── */
.error-box {
    background: rgba(248,113,113,0.06);
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 8px;
    padding: 0.85rem 1rem;
    color: #f87171;
    font-size: 0.88rem;
    margin-top: 0.75rem;
}
            

</style>
""", unsafe_allow_html=True)



# ─── DATA ─────────────────────────────────────────────────────────────────────

SCENARIOS = {
    "Phantom Delivery": {
        "invoice_id": "INV-TEST-001", "vendor_id": "V-007",
        "vendor_name": "Apex Supplies", "vendor_category": "Logistics",
        "po_reference": "PO-9001", "po_amount": 50000.0, "invoice_amount": 50000.0,
        "gr_amount": 0.0, "deviation_pct": 0.0, "days_since_last_invoice": 3,
        "is_new_vendor": False, "three_way_match": False, "invoice_date": "2024-01-15",
    },
    "Borderline Overbilling": {
        "invoice_id": "INV-TEST-MED", "vendor_id": "V-012",
        "vendor_name": "MidRange Supplies Co", "vendor_category": "Supply Chain",
        "po_reference": "PO-5005", "po_amount": 10000.0, "invoice_amount": 11800.0,
        "gr_amount": 11800.0, "deviation_pct": 0.18, "days_since_last_invoice": 10,
        "is_new_vendor": False, "three_way_match": False, "invoice_date": "2024-01-18",
    },
    "Clean Invoice": {
        "invoice_id": "INV-TEST-002", "vendor_id": "V-008",
        "vendor_name": "TechParts Ltd", "vendor_category": "IT",
        "po_reference": "PO-1002", "po_amount": 5000.0, "invoice_amount": 4900.0,
        "gr_amount": 4900.0, "deviation_pct": -0.02, "days_since_last_invoice": 45,
        "is_new_vendor": False, "three_way_match": True, "invoice_date": "2024-01-20",
    },
}

AGENT_STEPS = [
    ("Validate Invoice",    "field_completeness_check"),
    ("Detect Anomalies",    "pattern_fraud_detectors"),
    ("Get ML Score",        "random_forest · confidence"),
    ("Decide Risk Level",   "threshold_evaluation"),
    ("Deep Investigation",  "llm_tool_calls"),
    ("Generate SAR",        "compiling_activity_report"),
]

TOOLS = [
    "Similar Case Lookup",
    "Vendor History Check",
    "Purchase Order Verification",
    "SAR Report Generation",
]

STATUS_MESSAGES = [
    "Scanning transaction fingerprints…",
    "Cross-referencing vendor registry…",
    "Evaluating three-way match integrity…",
    "Querying anomaly pattern database…",
    "Running ML fraud scoring model…",
    "Correlating purchase order history…",
    "Analysing goods receipt discrepancies…",
    "Profiling vendor risk signals…",
    "Compiling investigation thread…",
    "Generating compliance report…",
]

# ─── SESSION STATE ────────────────────────────────────────────────────────────

for k, v in {
    "result": None, "error": None,
    "trace_step": 0, "is_high": False, "show_tools": False,
    "show_modal": False, "is_investigating": False,
    "selected_invoice": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def fmt_cur(v):
    return f"${v:,.2f}"

def risk_css(r):
    return {"HIGH": "rb-high", "MEDIUM": "rb-medium", "LOW": "rb-low"}.get(r, "rb-low")

def risk_label(r):
    return {"HIGH": "HIGH RISK", "MEDIUM": "MEDIUM RISK", "LOW": "LOW RISK"}.get(r, r)

def risk_badge_cls(r):
    return {"HIGH": "header-badge-high", "MEDIUM": "header-badge-medium", "LOW": "header-badge-low"}.get(r, "header-badge-low")

def risk_short(r):
    return {"HIGH": "High Risk", "MEDIUM": "Medium Risk", "LOW": "Low Risk"}.get(r, r)

def anomaly_tag(flag):
    atype = flag.get("anomaly_type", flag.get("type", "unknown"))
    sev   = flag.get("severity", "HIGH").upper()
    css   = "tag-red" if sev == "HIGH" else "tag-amber" if sev == "MEDIUM" else "tag-teal"
    return f'<span class="tag {css}">{atype.replace("_", " ").title()}</span>'

def field_html(label, value, danger=False, note=""):
    cls = "field-danger" if danger else "field-value"
    note_html = f'<div class="field-danger-note">{note}</div>' if note else ""
    return (f'<div class="field-wrap">'
            f'<div class="field-label">{label}</div>'
            f'<div class="{cls}">{value}</div>'
            f'{note_html}</div>')

def invoice_grid_html(inv):
    gr_note = "Goods receipt not posted" if inv["gr_amount"] == 0 else ""
    dev_val = inv["deviation_pct"] * 100
    rows = [
        [field_html("Invoice ID",  inv["invoice_id"]),
         field_html("Vendor ID",   inv["vendor_id"]),
         field_html("Vendor Name", inv["vendor_name"])],
        [field_html("Category",     inv["vendor_category"]),
         field_html("PO Reference", inv["po_reference"]),
         field_html("Invoice Date", inv["invoice_date"])],
        [field_html("PO Amount",      fmt_cur(inv["po_amount"])),
         field_html("Invoice Amount", fmt_cur(inv["invoice_amount"])),
         field_html("GR Amount",      fmt_cur(inv["gr_amount"]),
                    danger=inv["gr_amount"] == 0,
                    note=gr_note)],
        [field_html("Deviation %",
                    f"{dev_val:.1f}%",
                    danger=abs(dev_val) > 10),
         field_html("Days Since Invoice", str(inv["days_since_last_invoice"])),
         field_html("Three-Way Match",
                    "Passed" if inv["three_way_match"] else "Failed",
                    danger=not inv["three_way_match"])],
    ]
    return "".join('<div class="field-grid">' + "".join(r) + "</div>" for r in rows)

def trace_html(steps_done, is_high=False, show_tools=False):
    # Status text
    if steps_done >= len(AGENT_STEPS):
        status = "Completed"
    elif steps_done > 0:
        status = "Running…"
    else:
        status = ""

    html = '<div class="trace-card">'
    html += '<div class="trace-header">'
    html += '<div class="section-label" style="margin-bottom:0">Agent Trace</div>'
    if status:
        html += f'<div class="trace-status">{status}</div>'
    html += '</div>'

    for i, (name, desc) in enumerate(AGENT_STEPS):
        dot  = "td-done" if i < steps_done else "td-active" if i == steps_done else "td-pending"
        ncls = "ts-done" if i < steps_done else "ts-active" if i == steps_done else "ts-pending"
        html += (f'<div class="trace-step">'
                 f'<div class="trace-dot {dot}"></div>'
                 f'<div style="flex:1"><div class="ts-name {ncls}">{name}</div>'
                 f'</div></div>')

    if show_tools and is_high:
        html += '<div class="tool-divider"></div>'
        html += '<div class="section-label" style="margin-bottom:0.65rem">Tools Invoked</div>'
        for tn in TOOLS:
            html += f'<div class="tool-item">{tn}</div>'

    return html + "</div>"

def page_header_html(inv, risk):
    badge_cls = risk_badge_cls(risk)
    return f"""
    <div class="page-header">
        <div class="page-breadcrumb">
            <span>FinFraud</span> / Investigation
        </div>
        <div class="header-row">
            <div class="header-left">
                <div>
                    <div style="display:flex;align-items:center;gap:0.8rem;">
                        <span class="header-vendor">{inv['vendor_name']}</span>
                        <span class="{badge_cls}">{risk_short(risk)}</span>
                    </div>
                    <div class="header-meta">
                        {inv['invoice_id']}
                        <span class="sep">·</span>
                        {inv['vendor_id']}
                        <span class="sep">·</span>
                        {inv['vendor_category']}
                        <span class="sep">·</span>
                        Opened {inv['invoice_date']}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def metrics_html(result, inv):
    score = result.get("ml_score", 0.0)
    flags = result.get("anomaly_flags", [])
    dev_val = abs(inv["deviation_pct"] * 100)

    sc_cls = "red" if score >= 0.7 else "amber" if score >= 0.2 else "green"
    sc_accent = "accent-red" if score >= 0.7 else "accent-amber" if score >= 0.2 else "accent-green"
    dev_cls = "red" if dev_val > 10 else "white"
    dev_accent = "accent-red" if dev_val > 10 else ""

    flag_names = ", ".join(
        f.get("anomaly_type", f.get("type", "unknown")).replace("_", " ")
        for f in flags
    ) if flags else "none detected"
    n_flags = f"{len(flags):02d}"

    return f"""
    <div class="metrics-grid">
        <div class="metric-card-dark {sc_accent}">
            <div class="mc-label">ML Risk Score</div>
            <div class="mc-value {sc_cls}">{score:.0%}</div>
            <div class="mc-desc">Above 0.70 threshold</div>
        </div>
        <div class="metric-card-dark">
            <div class="mc-label">Anomalies Detected</div>
            <div class="mc-value red">{n_flags}</div>
            <div class="mc-desc">{flag_names}</div>
        </div>
        <div class="metric-card-dark {dev_accent}">
            <div class="mc-label">Deviation</div>
            <div class="mc-value {dev_cls}">{dev_val:.1f}%</div>
            <div class="mc-desc">PO vs. invoice amount</div>
        </div>
    </div>
    """


# ─── SAR PARSING ──────────────────────────────────────────────────────────────

def parse_sar(text):
    """Parse SAR text into sections. Supports '=== TITLE' format (new prompt)
    and falls back to legacy header detection for older reports."""

    # Clean markdown artifacts
    text = re.sub(r'\*{1,2}', '', text)

    # Sections to skip (data already shown in invoice card)
    SKIP = {"Subject Information", "Details"}

    # ── Strategy 1: Lines starting with === (new prompt format) ──
    if '===' in text:
        sections = []
        cur_title, body = None, []

        def flush_new():
            nonlocal cur_title, body
            if cur_title and body and cur_title not in SKIP:
                sections.append({"title": cur_title, "body": body[:]})
            cur_title, body = None, []

        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            # Match "=== SOME TITLE" or "=== SOME TITLE ==="
            m = re.match(r'^===+\s*(.+?)\s*=*\s*$', line)
            if m:
                flush_new()
                cur_title = m.group(1).strip(':').strip().title()
            elif cur_title is not None:
                body.append(line)
        flush_new()

        if sections:
            return sections

    # ── Strategy 2: Legacy header regex (old prompt format) ──
    HEADER = re.compile(
        r'^(?:'
        r'\d+[\.\)]\s+[A-Z][A-Za-z0-9 \-/]{2,}'
        r'|[A-Z][A-Z0-9 \-/]{4,}'
        r'|(?:Subject\s+Information|Summary|Overview|Findings?|Suspicious\s+Activity|'
        r'Evidence\s+Summary|Recommended\s+Action|Conclusion|Risk\s+Assessment|Details?)'
        r')[\s:\u2014\u2014]*$',
        re.IGNORECASE,
    )
    sections, cur_title, body = [], None, []

    def flush_legacy():
        if cur_title and body and cur_title not in SKIP:
            sections.append({"title": cur_title, "body": body[:]})

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if HEADER.match(line):
            flush_legacy()
            title = re.sub(r'^\d+[\.\)]\s*', '', line)
            title = title.rstrip(':').rstrip('\u2014').rstrip('\u2014').strip().title()
            cur_title, body = title, []
        else:
            body.append(line)
    flush_legacy()

    if not sections:
        return [{"title": "Findings", "body": [l.strip() for l in text.strip().splitlines() if l.strip()]}]
    return sections


def format_sar_body(body_lines):
    """Render a list of body lines into structured HTML."""
    html = ""
    for line in body_lines:
        # Bullet line: "- Label: value" or "- text"
        m = re.match(r'^[\-\u2022]\s*(.+?):\s*(.+)$', line)
        if m:
            label, value = m.group(1).strip(), m.group(2).strip()
            html += (f'<div class="sar-item">'
                     f'<span class="sar-bullet"></span>'
                     f'<div><span class="sar-item-label">{label}:</span> '
                     f'<span class="sar-item-value">{value}</span></div>'
                     f'</div>')
        elif re.match(r'^[\-\u2022]\s+', line):
            # Bullet without label:value pattern
            text = re.sub(r'^[\-\u2022]\s+', '', line)
            html += (f'<div class="sar-item">'
                     f'<span class="sar-bullet"></span>'
                     f'<div><span class="sar-item-value">{text}</span></div>'
                     f'</div>')
        else:
            # Prose paragraph
            html += f'<div style="margin-bottom:0.6rem;line-height:1.8">{line}</div>'
    return html or '<div style="color:#475569">No details available</div>'

# ─── RESULTS MODAL ────────────────────────────────────────────────────────────

@st.dialog("Investigation Complete", width="large")
def results_modal(res):
    risk        = res.get("risk_level", "LOW")
    score       = res.get("ml_score", 0.0)
    flags       = res.get("anomaly_flags", [])
    decision    = res.get("decision", "")
    explanation = res.get("explanation", "")
    sar_text    = res.get("sar_report")
    inv_id      = res.get("invoice_id", "")

    flag_tags = "".join(anomaly_tag(f) for f in flags) if flags else \
                '<span class="tag tag-teal">No anomalies detected</span>'
    sc_color = "#f87171" if score >= 0.7 else "#fbbf24" if score >= 0.2 else "#34c779"
    dec_display = decision.replace("_", " ").title()

    st.markdown(f"""
    <div class="risk-banner {risk_css(risk)}">{risk_label(risk)}</div>
    <div style="margin-bottom:1rem">{flag_tags}</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value" style="color:{sc_color}">{score:.2%}</div>
            <div class="metric-label">ML Fraud Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#f1f5f9">{len(flags)}</div>
            <div class="metric-label">Anomalies Found</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:0.9rem;color:#f1f5f9">{dec_display}</div>
            <div class="metric-label">Decision</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if explanation:
        st.markdown(f'<div class="explanation-box">{explanation}</div>', unsafe_allow_html=True)

    if sar_text:
        sections = parse_sar(sar_text)
        st.markdown(f"""
        <div class="sar-outer">
            <div class="sar-header-row">
                <span class="sar-badge">Suspicious Activity Report</span>
                <span class="sar-inv-id">{inv_id}</span>
            </div>
        """, unsafe_allow_html=True)
        for sec in sections:
            formatted_body = format_sar_body(sec['body'])
            st.markdown(f"""
            <div class="sar-section">
                <div class="sar-sec-title">{sec['title']}</div>
                <div class="sar-sec-body">{formatted_body}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── LAYOUT ───────────────────────────────────────────────────────────────────

has_result = st.session_state.result is not None

# ── Post-investigation header + metrics (full width) ──
if has_result:
    inv = st.session_state.selected_invoice
    res = st.session_state.result
    risk = res.get("risk_level", "LOW")

    hdr_col, btn_col1, btn_col2 = st.columns([5, 0.8, 0.8])
    with hdr_col:
        st.markdown(page_header_html(inv, risk), unsafe_allow_html=True)
    with btn_col1:
        if st.button("Go Back", key="back_btn"):
            st.session_state.update({
                "result": None, "error": None,
                "trace_step": 0, "is_high": False,
                "show_tools": False, "show_modal": False,
                "is_investigating": False,
                "selected_invoice": None,
            })
            st.rerun()
    with btn_col2:
        if st.button("Re-run Agent", key="rerun_btn"):
            st.session_state.update({
                "result": None, "error": None,
                "trace_step": 0, "is_high": False,
                "show_tools": False, "show_modal": False,
                "is_investigating": True,
                "selected_invoice": st.session_state.selected_invoice,
            })
            st.rerun()

    st.markdown(metrics_html(res, inv), unsafe_allow_html=True)
else:
    # ── Hero card (pre-investigation) ──
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">FinFraud Investigation Agent</div>
        <div class="hero-tagline">
            Autonomously investigates B2B payment fraud, detects anomalies,
            and generates Suspicious Activity Reports for compliance teams.
        </div>
        <div class="flow-container">
            <div class="flow-node fn-teal">Invoice Submitted</div>
            <span class="flow-arrow">→</span>
            <div class="flow-node fn-amber">Risk Assessed</div>
            <span class="flow-arrow">→</span>
            <div class="flow-node fn-orange">Decision Made</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
# ── Two-column layout ──
col_main, col_trace = st.columns([3.6, 1], gap="large")

with col_trace:
    st.markdown(
        trace_html(
            st.session_state.trace_step,
            is_high=st.session_state.is_high,
            show_tools=st.session_state.show_tools,
        ),
        unsafe_allow_html=True,
    )

with col_main:
    if st.session_state.is_investigating:
        invoice = st.session_state.selected_invoice
        result_h, error_h = [None], [None]

        def call_api():
            for attempt in range(3):
                try:
                    r = requests.post(f"{BACKEND_URL}/investigate", json=invoice, timeout=120)
                    r.raise_for_status()
                    result_h[0] = r.json()
                    return
                except requests.exceptions.ConnectionError:
                    if attempt < 2:
                        time.sleep(3)  # wait and retry silently — spinner is already showing
                    else:
                        error_h[0] = "Backend is starting up. Please wait a few seconds and click Investigate again."
                except Exception as e:
                    error_h[0] = str(e)
                    return

        thread = threading.Thread(target=call_api, daemon=True)
        thread.start()

        spinner = st.empty()
        msg_idx = 0
        while thread.is_alive():
            dot_html = "".join(
                f'<div class="inv-step-dot{"active" if j <= msg_idx % 6 else ""}"></div>'
                for j in range(6)
            )
            spinner.markdown(f"""
            <div class="inv-card">
                <div class="inv-ring"></div>
                <div class="inv-label">Investigating</div>
                <div class="inv-msg">{STATUS_MESSAGES[msg_idx % len(STATUS_MESSAGES)]}</div>
                <div class="inv-step-dots">{dot_html}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.8)
            msg_idx += 1

        thread.join()
        spinner.empty()

        if error_h[0]:
            st.session_state.error = error_h[0]
        else:
            res     = result_h[0]
            is_high = res.get("risk_level") == "HIGH"
            st.session_state.update({
                "result": res, "trace_step": 6,
                "is_high": is_high, "show_tools": is_high,
                "show_modal": True,
            })

        st.session_state.is_investigating = False
        st.rerun()

    else:
        selected = st.selectbox("scenario", list(SCENARIOS.keys()), label_visibility="collapsed")

        invoice = SCENARIOS[selected]
        st.markdown(f"""
        <div class="card">
            <div class="section-label">Invoice under investigation</div>
            {invoice_grid_html(invoice)}
        </div>
        """, unsafe_allow_html=True)

        investigate = st.button("Investigate")

        if investigate:
            st.session_state.update({
                "result": None, "error": None,
                "trace_step": 0, "is_high": False,
                "show_tools": False, "show_modal": False,
                "is_investigating": True,
                "selected_invoice": invoice,
            })
            st.rerun()

        if st.session_state.error:       
            st.markdown(f'<div class="error-box">{st.session_state.error}</div>',
                        unsafe_allow_html=True)

        if has_result:
            if st.button("View Investigation Results →", key="view_btn"):
                st.session_state.show_modal = True
                st.rerun()
        
# ── Modal trigger ──
if st.session_state.show_modal and st.session_state.result:
    results_modal(st.session_state.result)
    st.session_state.show_modal = False