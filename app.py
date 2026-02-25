"""
EU AI Act Compliance Checker · v4.0 — Final
Regulation (EU) 2024/1689
https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
"""

import streamlit as st
import json
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Compliance Checker",
    page_icon="🇪🇺",
    layout="centered",
    menu_items={
        "Get Help": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
        "About": "EU AI Act Compliance Checker v4.0 — Regulation (EU) 2024/1689",
    },
)

BASE = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ── CSS — full CSS-variable theme system ──────────────────────────────────────
def get_css(dark: bool) -> str:
    if dark:
        v = {
            "--bg":           "#0F1117",
            "--bg-card":      "#1A1D27",
            "--bg-card2":     "#21263A",
            "--bg-input":     "#1A1D27",
            "--border":       "#2E3349",
            "--border2":      "#3A3F5C",
            "--text-primary": "#F0F2FC",
            "--text-sec":     "#9BA3C0",
            "--text-muted":   "#5C6382",
            "--accent":       "#4F8EF7",
            "--accent-hover": "#3B7AE8",
            "--accent-bg":    "#1A2540",
            "--accent-border":"#2A4070",
            # warn note
            "--warn-bg":      "#2A1F00",
            "--warn-border":  "#F59E0B",
            "--warn-text":    "#FCD34D",
            # flag items
            "--flag-bg":      "#1A1D27",
            "--flag-border":  "#2E3349",
            # role note
            "--role-bg":      "#1A2540",
            "--role-border":  "#2A4070",
            "--role-text":    "#93C5FD",
            # how panel
            "--how-bg":       "#1A1D27",
            "--how-num-bg":   "#1A2540",
            "--how-num-border":"#2A4070",
            # ob
            "--ob-head-bg":   "#21263A",
            "--ob-row-border":"#2E3349",
            "--ob-art-bg":    "#1A2540",
            "--ob-art-border":"#2A4070",
            # tl
            "--tl-bg":        "#1A1D27",
            "--tl-row-border":"#2E3349",
            "--tl-date":      "#F0F2FC",
            "--tl-desc":      "#9BA3C0",
            "--tl-past-desc": "#5C6382",
            "--tl-now-badge-bg":  "#1A2540",
            "--tl-now-badge-border": "#4F8EF7",
            "--tl-now-badge-text":   "#93C5FD",
            # risk cards — dark variants keep vivid colors
            "--card-proh-bg":     "#1A0010",
            "--card-proh-border": "#F43F5E",
            "--card-proh-text":   "#FDA4AF",
            "--card-proh-sub":    "#FB7185",
            "--card-high-bg":     "#1A0D00",
            "--card-high-border": "#FB923C",
            "--card-high-text":   "#FED7AA",
            "--card-high-sub":    "#FDBA74",
            "--card-lim-bg":      "#1A1600",
            "--card-lim-border":  "#FACC15",
            "--card-lim-text":    "#FEF08A",
            "--card-lim-sub":     "#FDE68A",
            "--card-min-bg":      "#001A0D",
            "--card-min-border":  "#4ADE80",
            "--card-min-text":    "#BBF7D0",
            "--card-min-sub":     "#86EFAC",
            "--score-track":      "#2E3349",
            "--score-label":      "#9BA3C0",
            "--score-val":        "#F0F2FC",
            # download btn
            "--dl-bg":      "#21263A",
            "--dl-border":  "#3A3F5C",
            "--dl-text":    "#9BA3C0",
        }
    else:
        v = {
            "--bg":           "#F4F6FB",
            "--bg-card":      "#FFFFFF",
            "--bg-card2":     "#F9FAFC",
            "--bg-input":     "#FFFFFF",
            "--border":       "#E2E8F0",
            "--border2":      "#CBD5E1",
            "--text-primary": "#0F172A",
            "--text-sec":     "#475569",
            "--text-muted":   "#94A3B8",
            "--accent":       "#2563EB",
            "--accent-hover": "#1D4ED8",
            "--accent-bg":    "#EFF6FF",
            "--accent-border":"#BFDBFE",
            "--warn-bg":      "#FFFBEB",
            "--warn-border":  "#F59E0B",
            "--warn-text":    "#92400E",
            "--flag-bg":      "#FFFFFF",
            "--flag-border":  "#E2E8F0",
            "--role-bg":      "#EFF6FF",
            "--role-border":  "#BFDBFE",
            "--role-text":    "#1E40AF",
            "--how-bg":       "#FFFFFF",
            "--how-num-bg":   "#EFF6FF",
            "--how-num-border":"#BFDBFE",
            "--ob-head-bg":   "#F8FAFC",
            "--ob-row-border":"#F1F5F9",
            "--ob-art-bg":    "#EFF6FF",
            "--ob-art-border":"#BFDBFE",
            "--tl-bg":        "#FFFFFF",
            "--tl-row-border":"#F1F5F9",
            "--tl-date":      "#0F172A",
            "--tl-desc":      "#475569",
            "--tl-past-desc": "#94A3B8",
            "--tl-now-badge-bg":  "#EFF6FF",
            "--tl-now-badge-border": "#2563EB",
            "--tl-now-badge-text":   "#1E40AF",
            "--card-proh-bg":     "#FFF1F2",
            "--card-proh-border": "#F43F5E",
            "--card-proh-text":   "#881337",
            "--card-proh-sub":    "#BE123C",
            "--card-high-bg":     "#FFF7ED",
            "--card-high-border": "#F97316",
            "--card-high-text":   "#7C2D12",
            "--card-high-sub":    "#C2410C",
            "--card-lim-bg":      "#FEFCE8",
            "--card-lim-border":  "#EAB308",
            "--card-lim-text":    "#713F12",
            "--card-lim-sub":     "#A16207",
            "--card-min-bg":      "#F0FDF4",
            "--card-min-border":  "#22C55E",
            "--card-min-text":    "#14532D",
            "--card-min-sub":     "#166534",
            "--score-track":      "#E2E8F0",
            "--score-label":      "#64748B",
            "--score-val":        "#0F172A",
            "--dl-bg":      "#FFFFFF",
            "--dl-border":  "#E2E8F0",
            "--dl-text":    "#374151",
        }

    vars_css = ":root {\n" + "".join(f"  {k}: {val};\n" for k, val in v.items()) + "}\n"

    return vars_css + """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp { background: var(--bg) !important; }
.main .block-container {
    max-width: 840px;
    padding: 2rem 1.8rem 5rem 1.8rem;
}

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(140deg, #1B3A6B 0%, #2563EB 55%, #3B82F6 100%);
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 0.2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.06); border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute; bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.03); border-radius: 50%;
}
.hero-kicker {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #93C5FD; margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 1.95rem; font-weight: 800; color: #fff;
    line-height: 1.2; margin-bottom: 0.55rem;
}
.hero-sub { font-size: 0.92rem; color: #BFDBFE; line-height: 1.6; max-width: 520px; }
.hero-badges { margin-top: 1.1rem; display: flex; gap: 0.45rem; flex-wrap: wrap; }
.hero-badge {
    background: rgba(255,255,255,0.13); border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px; padding: 0.18rem 0.7rem;
    font-size: 0.68rem; font-weight: 600; color: #E0F2FE;
}

/* ── Theme toggle row ── */
.toggle-row {
    display: flex; justify-content: flex-end; align-items: center;
    gap: 0.5rem; margin: 0.7rem 0 1.4rem 0;
}
.toggle-label {
    font-size: 0.78rem; font-weight: 600;
    color: var(--text-sec);
}

/* ── How it works ── */
.how-panel {
    background: var(--how-bg);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 1.3rem 1.5rem; margin-bottom: 1.6rem;
}
.how-title {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.13em;
    text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.9rem;
}
.how-steps { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.7rem; }
.how-step { text-align: center; padding: 0.5rem 0.2rem; }
.how-num {
    width: 28px; height: 28px;
    background: var(--how-num-bg); border: 2px solid var(--how-num-border);
    border-radius: 50%; font-size: 0.75rem; font-weight: 800; color: var(--accent);
    display: flex; align-items: center; justify-content: center; margin: 0 auto 0.45rem;
}
.how-label { font-size: 0.75rem; font-weight: 600; color: var(--text-primary); line-height: 1.35; }
.how-desc  { font-size: 0.68rem; color: var(--text-muted); margin-top: 0.2rem; line-height: 1.3; }

/* ── Section header ── */
.sec-header {
    display: flex; align-items: center; gap: 0.55rem;
    margin: 1.7rem 0 0.75rem 0;
}
.sec-num {
    background: var(--accent); color: #fff; font-size: 0.65rem; font-weight: 800;
    width: 20px; height: 20px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.sec-title { font-size: 0.83rem; font-weight: 700; color: var(--text-primary); }
.sec-ref   { margin-left: auto; font-size: 0.68rem; }
.sec-ref a { color: var(--accent) !important; text-decoration: none; font-weight: 600; }
.sec-ref a:hover { text-decoration: underline; }

/* ── Warning note ── */
.warn-note {
    background: var(--warn-bg); border-left: 4px solid var(--warn-border);
    border-radius: 0 8px 8px 0; padding: 0.55rem 0.9rem;
    font-size: 0.78rem; color: var(--warn-text); margin-bottom: 0.75rem; font-weight: 500;
}

/* ── Submit button ── */
div[data-testid="stFormSubmitButton"] > button {
    background: var(--accent) !important;
    color: #fff !important; font-size: 0.92rem !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    padding: 0.72rem 2rem !important; letter-spacing: 0.02em;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
    transition: all 0.15s ease;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--accent-hover) !important;
    box-shadow: 0 6px 22px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px);
}

/* ── Risk cards ── */
.risk-card { border-radius: 16px; padding: 1.7rem 1.9rem; margin-bottom: 1.2rem; }
.risk-eyebrow {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; margin-bottom: 0.35rem; opacity: 0.75;
}
.risk-label { font-size: 1.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 0.35rem; }
.risk-desc  { font-size: 0.86rem; line-height: 1.55; opacity: 0.88; max-width: 500px; }
.score-row  { display: flex; align-items: center; gap: 0.75rem; margin-top: 1.1rem; }
.score-label { font-size: 0.72rem; font-weight: 600; color: var(--score-label); white-space: nowrap; }
.score-track { flex: 1; height: 7px; background: var(--score-track); border-radius: 4px; overflow: hidden; }
.score-fill  { height: 100%; border-radius: 4px; }
.score-val   { font-size: 0.78rem; font-weight: 800; color: var(--score-val); white-space: nowrap; }

.card-prohibited {
    background: var(--card-proh-bg); border: 2px solid var(--card-proh-border);
    color: var(--card-proh-text);
}
.card-prohibited .score-fill { background: linear-gradient(90deg,#F43F5E,#E11D48); }

.card-high {
    background: var(--card-high-bg); border: 2px solid var(--card-high-border);
    color: var(--card-high-text);
}
.card-high .score-fill { background: linear-gradient(90deg,#F97316,#EA580C); }

.card-limited {
    background: var(--card-lim-bg); border: 2px solid var(--card-lim-border);
    color: var(--card-lim-text);
}
.card-limited .score-fill { background: linear-gradient(90deg,#EAB308,#CA8A04); }

.card-minimal {
    background: var(--card-min-bg); border: 2px solid var(--card-min-border);
    color: var(--card-min-text);
}
.card-minimal .score-fill { background: linear-gradient(90deg,#22C55E,#16A34A); }

/* ── Trigger flags ── */
.flag-item {
    display: flex; align-items: flex-start; gap: 0.65rem;
    background: var(--flag-bg); border: 1px solid var(--flag-border);
    border-radius: 10px; padding: 0.75rem 0.95rem; margin: 0.35rem 0;
}
.flag-item.err  { border-left: 3px solid #F43F5E; }
.flag-item.warn { border-left: 3px solid #F97316; }
.flag-item.info { border-left: 3px solid var(--accent); }
.flag-item.ok   { border-left: 3px solid #22C55E; }
.flag-ico  { font-size: 0.95rem; flex-shrink: 0; margin-top: 0.05rem; }
.flag-body { flex: 1; }
.flag-text { font-size: 0.83rem; color: var(--text-primary); line-height: 1.5; font-weight: 500; }
.flag-link { font-size: 0.72rem; margin-top: 0.12rem; }
.flag-link a { color: var(--accent) !important; text-decoration: none; font-weight: 600; }
.flag-link a:hover { text-decoration: underline; }

/* ── Role note ── */
.role-note {
    background: var(--role-bg); border: 1px solid var(--role-border);
    border-radius: 10px; padding: 0.85rem 1.05rem;
    display: flex; gap: 0.65rem; margin: 0.75rem 0 1.1rem;
}
.role-ico  { font-size: 0.95rem; flex-shrink: 0; margin-top: 0.1rem; }
.role-text { font-size: 0.82rem; color: var(--role-text); line-height: 1.55; }
.role-text strong { font-weight: 700; }

/* ── Obligations ── */
.ob-group-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden; margin-bottom: 0.65rem;
}
.ob-group-head {
    background: var(--ob-head-bg); border-bottom: 1px solid var(--border);
    padding: 0.55rem 0.95rem;
    font-size: 0.7rem; font-weight: 700; color: var(--text-sec);
    letter-spacing: 0.07em; text-transform: uppercase;
}
.ob-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.62rem 0.95rem; border-bottom: 1px solid var(--ob-row-border); gap: 0.9rem;
}
.ob-row:last-child { border-bottom: none; }
.ob-text { font-size: 0.83rem; color: var(--text-primary); line-height: 1.45; flex: 1; }
.ob-art  {
    flex-shrink: 0; background: var(--ob-art-bg); border: 1px solid var(--ob-art-border);
    border-radius: 5px; padding: 0.13rem 0.45rem;
    font-size: 0.67rem; font-weight: 700; color: var(--accent); white-space: nowrap;
}
.ob-art a { color: var(--accent) !important; text-decoration: none; }
.ob-art a:hover { text-decoration: underline; }

/* ── Enforcement Timeline ── */
.tl-section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.13em;
    text-transform: uppercase; color: var(--text-muted);
    margin: 1.4rem 0 0.7rem 0; padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}
.tl-wrap {
    background: var(--tl-bg); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
}
.tl-row {
    display: grid;
    grid-template-columns: 12px 130px 1fr auto;
    align-items: center;
    gap: 0.85rem;
    padding: 0.9rem 1.1rem;
    border-bottom: 1px solid var(--tl-row-border);
    transition: background 0.1s;
}
.tl-row:last-child { border-bottom: none; }
.tl-row:hover { background: var(--bg-card2); }
.tl-dot {
    width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}
.tl-date {
    font-size: 0.8rem; font-weight: 700;
    color: var(--tl-date); white-space: nowrap;
}
.tl-desc {
    font-size: 0.82rem; color: var(--tl-desc); line-height: 1.4;
}
.tl-past .tl-date,
.tl-past .tl-desc { color: var(--tl-past-desc); }
.tl-badge {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; white-space: nowrap;
    padding: 0.18rem 0.5rem; border-radius: 20px;
}
.tl-badge-past {
    background: var(--bg-card2); border: 1px solid var(--border2);
    color: var(--text-muted);
}
.tl-badge-now {
    background: var(--tl-now-badge-bg); border: 1px solid var(--tl-now-badge-border);
    color: var(--tl-now-badge-text);
}
.tl-badge-future {
    background: var(--bg-card2); border: 1px solid var(--border);
    color: var(--text-sec);
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: var(--dl-bg) !important;
    color: var(--dl-text) !important;
    border: 1.5px solid var(--dl-border) !important;
    border-radius: 8px !important; font-weight: 600 !important; font-size: 0.82rem !important;
}
.stDownloadButton > button:hover {
    background: var(--bg-card2) !important;
    border-color: var(--accent) !important; color: var(--accent) !important;
}

/* ── Misc Streamlit overrides ── */
.stCheckbox label { color: var(--text-primary) !important; font-size: 0.86rem !important; }
.stSelectbox label, .stTextInput label { color: var(--text-primary) !important; font-weight: 600 !important; font-size: 0.83rem !important; }
div[data-baseweb="select"] > div {
    background: var(--bg-input) !important; border-color: var(--border2) !important;
    color: var(--text-primary) !important;
}
.stTextInput > div > div > input {
    background: var(--bg-input) !important; border-color: var(--border2) !important;
    color: var(--text-primary) !important;
}
hr { border-color: var(--border) !important; }
.stCaption p { color: var(--text-muted) !important; font-size: 0.72rem !important; }
h2 { color: var(--text-primary) !important; font-size: 1.15rem !important; font-weight: 800 !important; }
h3 { color: var(--text-primary) !important; font-size: 0.97rem !important; font-weight: 700 !important; }
p  { color: var(--text-sec) !important; }
"""

st.markdown(f"<style>{get_css(st.session_state.dark_mode)}</style>", unsafe_allow_html=True)

# ── Knowledge base ─────────────────────────────────────────────────────────────

PROHIBITED_PRACTICES = {
    "social_scoring":           ("Social scoring by public authorities",                        "Art. 5(1)(c)"),
    "realtime_biometric":       ("Real-time remote biometric ID in publicly accessible spaces", "Art. 5(1)(d)"),
    "subliminal_manipulation":  ("Subliminal techniques bypassing conscious awareness",         "Art. 5(1)(a)"),
    "exploit_vulnerability":    ("Exploitation of vulnerability of specific groups",            "Art. 5(1)(b)"),
    "emotion_recognition_work": ("Emotion recognition in workplace or educational institutions","Art. 5(1)(f)"),
    "biometric_categorization": ("Biometric categorisation inferring sensitive attributes",     "Art. 5(1)(e)"),
    "predictive_policing":      ("Individual criminal risk profiling without objective facts",  "Art. 5(1)(g)"),
    "facial_scraping":          ("Untargeted scraping of facial images from internet/CCTV",     "Art. 5(1)(h)"),
}

ANNEX_III = {
    "medical_devices":         ("Medical devices & healthcare",                         "Annex III §1"),
    "critical_infrastructure": ("Critical infrastructure management",                   "Annex III §2"),
    "education_vocational":    ("Education & vocational training",                      "Annex III §3"),
    "employment_hr":           ("Employment, HR & workforce management",                "Annex III §4"),
    "essential_services":      ("Access to essential services (credit, insurance)",     "Annex III §5"),
    "law_enforcement":         ("Law enforcement",                                      "Annex III §6"),
    "migration_asylum":        ("Migration, asylum & border control",                   "Annex III §7"),
    "justice_democracy":       ("Administration of justice & democratic processes",     "Annex III §8"),
    "safety_components":       ("Safety components of regulated products",              "Annex III §1"),
}

OBLIGATIONS = {
    "unacceptable": {
        "Legal Status": [
            ("This AI system is PROHIBITED in the EU — immediate cessation of all activities required",    "Art. 5"),
            ("Development, placing on market, and operation all constitute an infringement",               "Art. 5"),
            ("Maximum penalty: €35,000,000 or 7% of total global annual turnover",                       "Art. 99(3)"),
            ("Notifying the relevant national market surveillance authority is mandatory",                  "Art. 74"),
        ],
    },
    "high": {
        "Risk Management System": [
            ("Establish, implement, document and continuously maintain a risk management system",           "Art. 9"),
            ("Identify and analyse all known and foreseeable risks throughout the entire lifecycle",       "Art. 9(2)"),
            ("Update risk management based on data from post-market monitoring",                           "Art. 9(6)"),
        ],
        "Data & Data Governance": [
            ("Implement data governance and data management practices",                                    "Art. 10"),
            ("Ensure training, validation and test datasets are relevant, representative and error-free", "Art. 10(3)"),
            ("Document data gaps, apply bias mitigation, and manage data augmentation",                   "Art. 10(5)"),
        ],
        "Technical Documentation": [
            ("Prepare technical documentation before placing on market — follow Annex IV template",        "Art. 11"),
            ("Keep all documentation up-to-date throughout the system's operational lifetime",            "Art. 11(2)"),
            ("Provide documentation to market surveillance authorities upon request",                     "Art. 11(3)"),
        ],
        "Logging & Audit Trail": [
            ("Implement automatic event logging capabilities for the full system lifetime",               "Art. 12"),
            ("Logs must retain sufficient records to trace decisions made post-deployment",               "Art. 12(1)"),
            ("Deployers must retain logs for a minimum of 6 months unless otherwise specified",          "Art. 12(2)"),
        ],
        "Transparency & Instructions for Use": [
            ("Design for transparency enabling deployers to interpret and understand outputs",             "Art. 13"),
            ("Provide instructions for use including purpose, metrics, and oversight measures",           "Art. 13(3)"),
        ],
        "Human Oversight": [
            ("Enable qualified persons to oversee, understand and override the system at all times",     "Art. 14"),
            ("Ensure operators can intervene or halt the system in real time when necessary",            "Art. 14(4)"),
            ("Train all oversight personnel appropriately for the specific system in use",               "Art. 14(4)(c)"),
        ],
        "Accuracy, Robustness & Cybersecurity": [
            ("Define accuracy metrics and maintain consistent performance throughout the lifecycle",      "Art. 15"),
            ("Implement resilience against adversarial attacks, data poisoning and model evasion",       "Art. 15(4)"),
            ("Apply cybersecurity measures proportionate to the risks of the system",                    "Art. 15(5)"),
        ],
        "Conformity Assessment & Market Access": [
            ("Conduct conformity assessment — self-assessment or third-party per Annex VI/VII",          "Art. 43"),
            ("Draw up EU Declaration of Conformity following Annex V template",                         "Art. 48"),
            ("Affix CE marking before placing on the EU market",                                         "Art. 48"),
            ("Register in the EU AI public database before market launch",                              "Art. 49"),
        ],
        "Post-Market Monitoring & Incident Reporting": [
            ("Establish a post-market monitoring plan and actively collect real-world performance data", "Art. 72"),
            ("Report serious incidents to national authority within 15 days of becoming aware",         "Art. 73(2)"),
            ("Cooperate fully with market surveillance authorities on inspections",                     "Art. 74"),
        ],
    },
    "gpai_systemic": {
        "Systemic Risk — Enhanced Obligations": [
            ("Perform model evaluation including adversarial testing (red-teaming)",                    "Art. 55(1)(a)"),
            ("Assess and implement measures to mitigate systemic risks at EU and global level",         "Art. 55(1)(b)"),
            ("Report serious incidents and corrective measures to the EU Commission without delay",     "Art. 55(1)(c)"),
            ("Ensure appropriate cybersecurity protection for the model and its infrastructure",        "Art. 55(1)(d)"),
            ("Report energy consumption of training and operation to the AI Office",                    "Art. 55(1)(e)"),
        ],
    },
    "gpai": {
        "General-Purpose AI Model Obligations": [
            ("Prepare and maintain technical documentation — follow Annex XI and XII templates",         "Art. 53(1)(a)"),
            ("Provide downstream providers with all information needed for their own compliance",        "Art. 53(1)(b)"),
            ("Publish and maintain a copyright transparency policy",                                     "Art. 53(1)(c)"),
            ("Make a sufficiently detailed summary of training data publicly available",                 "Art. 53(1)(d)"),
            ("Adhere to EU copyright law including text and data mining exceptions",                    "Art. 53(2)"),
        ],
    },
    "limited": {
        "Transparency Obligations": [
            ("Inform users they are interacting with an AI system — applies to chatbots and virtual agents","Art. 50(1)"),
            ("Disclose that content is AI-generated for synthetic audio, image, video or text",          "Art. 50(2)"),
            ("Apply machine-readable marking or watermark to AI-generated or AI-manipulated content",   "Art. 50(4)"),
            ("Inform individuals when emotion recognition or biometric categorisation is being applied","Art. 50(3)"),
        ],
    },
    "minimal": {
        "Recommended Voluntary Actions": [
            ("No specific mandatory obligations apply to this system under the EU AI Act",               "—"),
            ("Consider adopting a voluntary Code of Conduct aligned with Annex IX principles",          "Art. 95"),
            ("Ensure AI literacy within your organisation — a general obligation for all operators",    "Art. 4"),
            ("Comply with applicable GDPR, consumer protection and sector-specific regulations",        "2016/679 EU"),
        ],
    },
}

def risk_score(a: dict) -> int:
    if any(a.get(k) for k in PROHIBITED_PRACTICES): return 100
    s = 0
    if a.get("sector") in ANNEX_III:        s += 60
    if a.get("safety_critical"):             s += 20
    if a.get("affects_rights"):              s += 15
    if a.get("autonomous"):                  s += 10
    if a.get("large_scale"):                 s += 8
    if a.get("gpai_model"):                  s = max(s, 35)
    if a.get("interacts_humans"):            s = max(s, 30)
    if a.get("generates_content"):           s = max(s, 25)
    return min(s, 99)

def classify(a: dict):
    flags, ob_keys = [], []
    for key, (desc, ref) in PROHIBITED_PRACTICES.items():
        if a.get(key):
            flags.append({"text": desc, "ref": ref, "sev": "err"})
    if flags:
        return "prohibited", flags, ["unacceptable"]

    is_high = False
    sector = a.get("sector", "general")
    if sector in ANNEX_III:
        label, ref = ANNEX_III[sector]
        flags.append({"text": f"{label} — mandatory conformity assessment required", "ref": ref, "sev": "warn"})
        is_high = True
    if a.get("safety_critical"):
        flags.append({"text": "Safety component of a regulated product", "ref": "Annex III §1", "sev": "warn"})
        is_high = True
    if a.get("affects_rights") and a.get("autonomous"):
        flags.append({"text": "Autonomous decision affecting fundamental rights — high-risk threshold met", "ref": "Art. 6(2)", "sev": "warn"})
        is_high = True
    if is_high:
        ob_keys.append("high")

    if a.get("gpai_model"):
        flags.append({"text": "General-purpose AI model — GPAI obligations apply", "ref": "Art. 51", "sev": "warn" if is_high else "info"})
        if a.get("gpai_systemic") or a.get("gpai_flops"):
            flags.append({"text": "Systemic risk threshold met (≥10²⁵ FLOPs or Commission designation)", "ref": "Art. 51(2)", "sev": "warn"})
            ob_keys.append("gpai_systemic")
        ob_keys.append("gpai")
        if not is_high:
            return "limited", flags, list(dict.fromkeys(["limited"] + ob_keys))

    if is_high:
        return "high", flags, list(dict.fromkeys(ob_keys))

    limited = []
    if a.get("interacts_humans"):
        limited.append({"text": "Direct interaction with natural persons (chatbot / virtual agent)", "ref": "Art. 50(1)", "sev": "info"})
    if a.get("generates_content"):
        limited.append({"text": "Synthetic content generation (text, image, audio, video)", "ref": "Art. 50(2)", "sev": "info"})
    if a.get("emotion_detect"):
        limited.append({"text": "Emotion recognition system (outside prohibited workplace/education context)", "ref": "Art. 50(3)", "sev": "info"})
    if limited or (a.get("gpai_model") and not is_high):
        flags.extend(limited)
        ob_keys.append("limited")
        return "limited", flags, list(dict.fromkeys(ob_keys))

    flags.append({"text": "No prohibited practices or Annex III triggers identified — minimal risk", "ref": "Art. 6", "sev": "ok"})
    return "minimal", flags, ["minimal"]

# ── Article link helper ────────────────────────────────────────────────────────
def art_link(label: str) -> str:
    return f'<a href="{BASE}" target="_blank" rel="noopener">{label}</a>'

# ═════════════════════════════════════════════════════════════════════════════
# RENDER
# ═════════════════════════════════════════════════════════════════════════════

# Hero
st.markdown("""
<div class="hero-wrap">
  <div class="hero-kicker">Regulation (EU) 2024/1689 &nbsp;·&nbsp; Official compliance tool</div>
  <div class="hero-title">EU AI Act<br>Compliance Checker</div>
  <div class="hero-sub">Answer 20 structured questions and receive an instant, article-level risk classification with your full mandatory obligations checklist — ready to attach to your compliance dossier.</div>
  <div class="hero-badges">
    <span class="hero-badge">🇪🇺 Reg. 2024/1689</span>
    <span class="hero-badge">Art. 5 · 6 · 50 · 51–55</span>
    <span class="hero-badge">Annex III · IV · V · XI</span>
    <span class="hero-badge">v4.0 · 2025</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Theme toggle
mode_icon = "☀️ Light mode" if st.session_state.dark_mode else "🌙 Dark mode"
col_sp, col_btn = st.columns([6, 1])
with col_btn:
    if st.button(mode_icon, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# How it works
st.markdown("""
<div class="how-panel">
  <div class="how-title">How it works</div>
  <div class="how-steps">
    <div class="how-step">
      <div class="how-num">1</div>
      <div class="how-label">Describe your system</div>
      <div class="how-desc">Role, sector &amp; deployment context</div>
    </div>
    <div class="how-step">
      <div class="how-num">2</div>
      <div class="how-label">Check Art. 5 prohibitions</div>
      <div class="how-desc">All 8 banned practices reviewed</div>
    </div>
    <div class="how-step">
      <div class="how-num">3</div>
      <div class="how-label">Assess risk level</div>
      <div class="how-desc">Annex III · GPAI · Art. 50 logic</div>
    </div>
    <div class="how-step">
      <div class="how-num">4</div>
      <div class="how-label">Get obligations</div>
      <div class="how-desc">Article-linked checklist &amp; export</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("ai_act_form"):

    # Section 1
    st.markdown(f'<div class="sec-header"><div class="sec-num">1</div><div class="sec-title">System Basics</div><div class="sec-ref"><a href="{BASE}" target="_blank">Art. 3 — Definitions ↗</a></div></div>', unsafe_allow_html=True)
    system_name = st.text_input("System name / identifier", placeholder="e.g. Recruitment screening algorithm, Medical image classifier…")
    c1, c2 = st.columns(2)
    with c1:
        org_role = st.selectbox("Your organisation's role", ["provider","deployer","importer","distributor"],
            format_func=lambda x: {"provider":"Provider — develops / places on market","deployer":"Deployer — uses under own responsibility","importer":"Importer — brings into EU from third country","distributor":"Distributor — makes available on EU market"}[x])
    with c2:
        sector = st.selectbox("Primary deployment sector",
            ["general","medical_devices","critical_infrastructure","education_vocational","employment_hr","essential_services","law_enforcement","migration_asylum","justice_democracy","safety_components"],
            format_func=lambda x: {"general":"General / Other","medical_devices":"Medical devices & healthcare","critical_infrastructure":"Critical infrastructure (energy, water, transport)","education_vocational":"Education & vocational training","employment_hr":"Employment, HR & workforce management","essential_services":"Essential services (credit, insurance, social)","law_enforcement":"Law enforcement","migration_asylum":"Migration, asylum & border control","justice_democracy":"Administration of justice & democracy","safety_components":"Safety components (vehicles, machinery, aviation)"}[x])

    # Section 2
    st.markdown(f'<div class="sec-header"><div class="sec-num">2</div><div class="sec-title">Prohibited Practices — Article 5</div><div class="sec-ref"><a href="{BASE}" target="_blank">Art. 5 full text ↗</a></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="warn-note">⚠️  If <strong>any</strong> of the following applies, the system is <strong>banned in the EU</strong> regardless of sector, purpose or safeguards.</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        social_scoring      = st.checkbox("Social scoring by public authorities  [Art. 5(1)(c)]")
        subliminal          = st.checkbox("Subliminal / deceptive manipulation techniques  [Art. 5(1)(a)]")
        emotion_work        = st.checkbox("Emotion recognition at workplace or in education  [Art. 5(1)(f)]")
        predictive_policing = st.checkbox("Predictive criminal profiling without objective facts  [Art. 5(1)(g)]")
    with cb:
        realtime_biometric  = st.checkbox("Real-time biometric ID in public spaces  [Art. 5(1)(d)]")
        exploit_vuln        = st.checkbox("Exploitation of vulnerable groups  [Art. 5(1)(b)]")
        biometric_cat       = st.checkbox("Biometric categorisation revealing sensitive attributes  [Art. 5(1)(e)]")
        facial_scraping     = st.checkbox("Mass facial image scraping from internet / CCTV  [Art. 5(1)(h)]")

    # Section 3
    st.markdown(f'<div class="sec-header"><div class="sec-num">3</div><div class="sec-title">High-Risk Modifiers — Annex III & Art. 6</div><div class="sec-ref"><a href="{BASE}" target="_blank">Annex III ↗</a></div></div>', unsafe_allow_html=True)
    cc, cd = st.columns(2)
    with cc:
        safety_critical = st.checkbox("Safety component of a regulated product (machinery, vehicle, medical device)")
        autonomous      = st.checkbox("Makes autonomous decisions without human review")
    with cd:
        affects_rights  = st.checkbox("Affects access to employment, credit, housing, education or liberty")
        large_scale     = st.checkbox("Deployed at large scale (1M+ individuals affected)")

    # Section 4
    st.markdown(f'<div class="sec-header"><div class="sec-num">4</div><div class="sec-title">General-Purpose AI Model (GPAI) — Articles 51–55</div><div class="sec-ref"><a href="{BASE}" target="_blank">Art. 51–55 ↗</a></div></div>', unsafe_allow_html=True)
    gpai_model = st.checkbox("This is a general-purpose AI model (LLM, foundation model, multimodal model)")
    ce, cf = st.columns(2)
    with ce:
        gpai_flops    = st.checkbox("Training compute ≥ 10²⁵ FLOPs (systemic risk threshold)")
    with cf:
        gpai_systemic = st.checkbox("Designated as systemic risk model by the EU Commission")

    # Section 5
    st.markdown(f'<div class="sec-header"><div class="sec-num">5</div><div class="sec-title">Transparency Obligations — Article 50</div><div class="sec-ref"><a href="{BASE}" target="_blank">Art. 50 ↗</a></div></div>', unsafe_allow_html=True)
    cg, ch = st.columns(2)
    with cg:
        interacts_humans  = st.checkbox("Directly interacts with humans (chatbot, virtual agent)")
        emotion_detect    = st.checkbox("Detects or infers emotional states of individuals")
    with ch:
        generates_content = st.checkbox("Generates synthetic content (text, image, audio, video, code)")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("⚡  Run Compliance Assessment", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if submitted:
    answers = {
        "system_name": system_name or "AI System", "org_role": org_role, "sector": sector,
        "social_scoring": social_scoring, "realtime_biometric": realtime_biometric,
        "subliminal_manipulation": subliminal, "exploit_vulnerability": exploit_vuln,
        "emotion_recognition_work": emotion_work, "biometric_categorization": biometric_cat,
        "predictive_policing": predictive_policing, "facial_scraping": facial_scraping,
        "safety_critical": safety_critical, "autonomous": autonomous,
        "affects_rights": affects_rights, "large_scale": large_scale,
        "gpai_model": gpai_model, "gpai_flops": gpai_flops, "gpai_systemic": gpai_systemic,
        "interacts_humans": interacts_humans, "generates_content": generates_content,
        "emotion_detect": emotion_detect,
    }

    risk_level, flags, ob_keys = classify(answers)
    score = risk_score(answers)

    RISK_CFG = {
        "prohibited": {"eyebrow":"Article 5 — Prohibited Practice","label":"🚫  Prohibited AI System","desc":"This system falls under the prohibited AI practices of Art. 5. It cannot be developed, placed on the market, put into service, or used anywhere in the EU.","card":"card-prohibited"},
        "high":       {"eyebrow":"Annex III — High-Risk AI System","label":"🔴  High-Risk AI System","desc":"A full conformity assessment, CE marking, EU AI database registration and compliance with Art. 9–15 are required before this system may be deployed.","card":"card-high"},
        "limited":    {"eyebrow":"Article 50 — Limited Risk AI System","label":"🟡  Limited Risk AI System","desc":"Transparency obligations apply. Users must be informed they are interacting with an AI, and all synthetic content must be clearly labelled.","card":"card-limited"},
        "minimal":    {"eyebrow":"Article 6 — Minimal Risk AI System","label":"🟢  Minimal Risk AI System","desc":"No specific mandatory obligations apply under the EU AI Act. Voluntary codes of conduct and general EU law (GDPR, consumer protection) still apply.","card":"card-minimal"},
    }
    cfg = RISK_CFG[risk_level]

    st.divider()
    st.markdown("## Assessment Result")

    # Risk card
    st.markdown(f"""
    <div class="risk-card {cfg['card']}">
      <div class="risk-eyebrow">{cfg['eyebrow']}</div>
      <div class="risk-label">{cfg['label']}</div>
      <div class="risk-desc">{cfg['desc']}</div>
      <div class="score-row">
        <div class="score-label">Risk Score</div>
        <div class="score-track"><div class="score-fill {cfg['card'].replace('card-','bar-')}" style="width:{score}%; background: {'#E11D48' if risk_level=='prohibited' else '#F97316' if risk_level=='high' else '#EAB308' if risk_level=='limited' else '#22C55E'};"></div></div>
        <div class="score-val">{score} / 100</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Triggered flags
    st.markdown("### Triggered Criteria")
    ico_map = {"err":"🚨","warn":"⚠️","info":"ℹ️","ok":"✅"}
    for f in flags:
        ico = ico_map.get(f["sev"],"•")
        link_html = f'<div class="flag-link"><a href="{BASE}" target="_blank" rel="noopener">→ {f["ref"]}</a></div>' if f.get("ref") and f["ref"] != "—" else ""
        st.markdown(f'<div class="flag-item {f["sev"]}"><div class="flag-ico">{ico}</div><div class="flag-body"><div class="flag-text">{f["text"]}</div>{link_html}</div></div>', unsafe_allow_html=True)

    # Role note
    role_guidance = {
        "provider":    "As <strong>Provider</strong>, you are responsible for the conformity assessment, CE marking, technical documentation (Annex IV), registration in the EU AI database, and post-market monitoring.",
        "deployer":    "As <strong>Deployer</strong>, you must ensure human oversight, retain logs for at least 6 months, conduct a Fundamental Rights Impact Assessment for high-risk systems (Art. 27), and report incidents.",
        "importer":    "As <strong>Importer</strong>, verify the provider has completed all conformity assessments, technical documentation exists, and CE marking is in place before EU market entry (Art. 23).",
        "distributor": "As <strong>Distributor</strong>, verify CE marking and conformity documentation before making the system available, and cooperate fully with market surveillance authorities (Art. 24).",
    }
    st.markdown(f'<div class="role-note"><div class="role-ico">💼</div><div class="role-text">{role_guidance[org_role]}</div></div>', unsafe_allow_html=True)

    # Obligations checklist
    st.markdown("### Mandatory Obligations & Compliance Checklist")
    for ob_key in ob_keys:
        if ob_key not in OBLIGATIONS: continue
        for group_name, items in OBLIGATIONS[ob_key].items():
            rows_html = ""
            for text, ref in items:
                badge = f'<span class="ob-art">{art_link(ref)}</span>' if ref and ref != "—" else '<span class="ob-art" style="opacity:0.4;">—</span>'
                rows_html += f'<div class="ob-row"><div class="ob-text">{text}</div>{badge}</div>'
            st.markdown(f'<div class="ob-group-card"><div class="ob-group-head">{group_name}</div>{rows_html}</div>', unsafe_allow_html=True)

    # Enforcement Timeline — redesigned
    st.markdown('<div class="tl-section-label">Enforcement Timeline — Regulation (EU) 2024/1689</div>', unsafe_allow_html=True)
    now = datetime.now()
    tl_entries = [
        ("2024-08-01", "#6B7280",  "EU AI Act entered into force",                              "In force"),
        ("2025-02-02", "#6B7280",  "Prohibited practices (Art. 5) enforceable",                 "Art. 5"),
        ("2025-08-02", "#F97316",  "GPAI model obligations enforceable (Art. 51–55)",            "GPAI"),
        ("2026-08-02", "#2563EB",  "High-risk systems — full application (Annex III)",           "High-risk"),
        ("2027-08-02", "#22C55E",  "Annex I product safety systems — extended deadline",         "Annex I"),
    ]
    rows_html = ""
    for date_str, dot_color, desc, tag in tl_entries:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        days_diff = (dt - now).days
        is_past   = days_diff < -30
        is_now    = abs(days_diff) <= 90  # within 3 months = "upcoming"

        cls = "tl-past" if is_past else ("tl-now" if is_now else "")
        dot_col = "#94A3B8" if is_past else dot_color

        if is_past:
            badge_html = f'<span class="tl-badge tl-badge-past">✓ Done</span>'
        elif is_now:
            badge_html = f'<span class="tl-badge tl-badge-now">⚡ Upcoming</span>'
        else:
            badge_html = f'<span class="tl-badge tl-badge-future">{tag}</span>'

        rows_html += f"""
        <div class="tl-row {cls}">
          <div class="tl-dot" style="background:{dot_col};box-shadow:{'none' if is_past else f'0 0 0 3px {dot_color}22'};"></div>
          <div class="tl-date">{dt.strftime("%d %b %Y")}</div>
          <div class="tl-desc">{desc}</div>
          {badge_html}
        </div>"""
    st.markdown(f'<div class="tl-wrap">{rows_html}</div>', unsafe_allow_html=True)

    # Downloads
    st.divider()
    st.markdown("### Download Compliance Report")

    report = {
        "tool": "EU AI Act Compliance Checker v4.0",
        "regulation": "Regulation (EU) 2024/1689",
        "official_text": BASE,
        "generated_at": datetime.now().isoformat(),
        "system_name": answers["system_name"],
        "organisation_role": org_role,
        "sector": sector,
        "risk_level": risk_level,
        "risk_score": score,
        "triggered_criteria": [{"description": f["text"], "article": f.get("ref",""), "source": BASE} for f in flags],
        "obligations": {k: {g: [{"obligation": t, "article": a, "source_url": BASE} for t, a in items] for g, items in OBLIGATIONS[k].items()} for k in ob_keys if k in OBLIGATIONS},
    }

    md_lines = [
        f"# EU AI Act Compliance Report",
        f"**System:** {answers['system_name']}",
        f"**Date:** {datetime.now().strftime('%d %B %Y')}",
        f"**Regulation:** [EU 2024/1689]({BASE})",
        f"**Risk Level:** {cfg['label']}",
        f"**Risk Score:** {score}/100",
        "", "## Triggered Criteria",
    ]
    for f in flags:
        md_lines.append(f"- {f['text']} — `{f.get('ref','')}`")
    md_lines.append("\n## Obligations")
    for k in ob_keys:
        if k not in OBLIGATIONS: continue
        for g, items in OBLIGATIONS[k].items():
            md_lines.append(f"\n### {g}")
            for text, ref in items:
                md_lines.append(f"- [ ] {text} — [{ref}]({BASE})")
    md_lines.append(f"\n---\n*Generated by EU AI Act Compliance Checker v4.0 — informational only, not legal advice.*")

    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📥  Download JSON Report", data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name=f"eu_ai_act_{answers['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json", use_container_width=True)
    with d2:
        st.download_button("📋  Download Markdown Checklist", data="\n".join(md_lines),
            file_name=f"eu_ai_act_{answers['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown", use_container_width=True)

# Footer
st.divider()
st.caption(f"⚠️ Informational purposes only — does not constitute legal advice. Always consult a qualified legal professional for compliance decisions. Built on [Regulation (EU) 2024/1689]({BASE}) · v4.0 · {datetime.now().year}")
