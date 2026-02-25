"""
EU AI Act Compliance Checker · v5.0
Regulation (EU) 2024/1689
"""

import streamlit as st
import json
from datetime import datetime

BASE = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"

st.set_page_config(
    page_title="EU AI Act Compliance Checker",
    page_icon="🇪🇺",
    layout="centered",
    menu_items={"Get Help": BASE, "About": "EU AI Act Compliance Checker v5.0"},
)

if "dark" not in st.session_state:
    st.session_state.dark = False

# ── Design tokens ─────────────────────────────────────────────────────────────
def css(dark: bool) -> str:
    if dark:
        t = dict(
            bg="#111318", surface="#1C1F29", border="#2A2D3A",
            text="#ECEEF5", sub="#8B90A8", muted="#50546A", border2="#3A3F5C",
            accent="#5B8DF6", accent_dim="#1A2440", accent_hover="#4070E8",
            red="#F26B7A",   red_dim="#2A0F14",
            orange="#F5924A",orange_dim="#2A1400",
            yellow="#E8C54A",yellow_dim="#261F00",
            green="#4FC87A", green_dim="#07200F",
        )
    else:
        t = dict(
            bg="#F8F9FC", surface="#FFFFFF", border="#E4E7EF",
            text="#1A1D2E", sub="#5A6080", muted="#9BA3BF", border2="#C8CDDE",
            accent="#2B5CE6", accent_dim="#EEF3FD", accent_hover="#1E4ED8",
            red="#D93553",   red_dim="#FDF0F2",
            orange="#D9680A",orange_dim="#FFF5EC",
            yellow="#9A7A05",yellow_dim="#FEFCE8",
            green="#1A7A40", green_dim="#F0FDF4",
        )
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, [class*="css"] {{ font-family: 'Inter', system-ui, sans-serif; }}

.stApp {{ background: {t['bg']} !important; }}
.main .block-container {{ max-width: 760px; padding: 2.5rem 1.5rem 5rem; }}

/* headings */
h1,h2,h3 {{ color: {t['text']} !important; font-weight: 700 !important; letter-spacing: -0.02em; }}
h2 {{ font-size: 1.25rem !important; margin-bottom: 0.1rem !important; }}
h3 {{ font-size: 0.95rem !important; margin: 1.5rem 0 0.5rem !important; }}
p  {{ color: {t['sub']} !important; margin: 0; }}

/* page title */
.page-title {{ font-size: 1.6rem; font-weight: 700; color: {t['text']}; letter-spacing: -0.03em; margin-bottom: 0.2rem; }}
.page-sub   {{ font-size: 0.88rem; color: {t['sub']}; line-height: 1.6; margin-bottom: 2rem; }}

/* toggle */
.top-row {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }}

/* theme toggle button */
button[data-testid="baseButton-secondary"][kind="secondary"] {{
    background: {t['surface']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    padding: 0.35rem 0.7rem !important;
    transition: all 0.15s;
}}
button[data-testid="baseButton-secondary"][kind="secondary"]:hover {{
    border-color: {t['accent']} !important;
    background: {t['accent_dim']} !important;
}}

/* section label */
.sec-label {{
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: {t['muted']};
    border-top: 1px solid {t['border']};
    padding-top: 1.2rem; margin: 1.6rem 0 0.7rem;
}}

/* warning strip */
.warn-strip {{
    background: {t['orange_dim']}; border: 1px solid {t['border']};
    border-left: 3px solid {t['orange']};
    border-radius: 6px; padding: 0.6rem 0.85rem;
    font-size: 0.8rem; color: {t['orange']}; font-weight: 500;
    margin-bottom: 0.75rem;
}}

/* submit */
div[data-testid="stFormSubmitButton"] > button {{
    width: 100% !important; background: {t['accent']} !important;
    color: #ffffff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 1rem !important; font-weight: 700 !important;
    padding: 0.78rem 1.5rem !important; letter-spacing: 0.015em;
    box-shadow: 0 2px 16px {t['accent']}55 !important;
    transition: all 0.15s ease;
}}
div[data-testid="stFormSubmitButton"] > button:hover {{
    background: {t['accent_hover']} !important;
    box-shadow: 0 4px 22px {t['accent']}77 !important;
    transform: translateY(-1px);
}}
div[data-testid="stFormSubmitButton"] > button p {{
    color: #ffffff !important; font-size: 1rem !important; font-weight: 700 !important;
}}

/* result badge */
.badge {{
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em;
    text-transform: uppercase; border-radius: 4px; padding: 0.2rem 0.55rem;
    border: 1px solid;
}}
.badge-red    {{ color: {t['red']};    background: {t['red_dim']};    border-color: {t['red']}44; }}
.badge-orange {{ color: {t['orange']}; background: {t['orange_dim']}; border-color: {t['orange']}44; }}
.badge-yellow {{ color: {t['yellow']}; background: {t['yellow_dim']}; border-color: {t['yellow']}44; }}
.badge-green  {{ color: {t['green']};  background: {t['green_dim']};  border-color: {t['green']}44; }}
.badge-blue   {{ color: {t['accent']}; background: {t['accent_dim']}; border-color: {t['accent']}44; }}
.badge-muted  {{ color: {t['muted']};  background: {t['surface']};    border-color: {t['border']}; }}

/* result card */
.result-card {{
    border: 1px solid {t['border']}; border-radius: 10px;
    padding: 1.4rem 1.5rem; margin: 0.75rem 0 1.25rem;
    background: {t['surface']};
}}
.result-level {{ font-size: 1.35rem; font-weight: 700; letter-spacing: -0.02em; margin: 0.4rem 0 0.3rem; color: {t['text']}; }}
.result-desc  {{ font-size: 0.85rem; color: {t['sub']}; line-height: 1.6; }}

/* score bar */
.score-wrap {{ margin-top: 1.1rem; }}
.score-meta {{ display: flex; justify-content: space-between; margin-bottom: 0.3rem; }}
.score-meta span {{ font-size: 0.72rem; color: {t['muted']}; font-weight: 500; }}
.score-track {{ height: 4px; background: {t['border']}; border-radius: 2px; }}
.score-fill  {{ height: 4px; border-radius: 2px; }}

/* flag rows */
.flag-row {{
    display: flex; align-items: flex-start; gap: 0.6rem;
    padding: 0.65rem 0; border-bottom: 1px solid {t['border']};
}}
.flag-row:last-child {{ border-bottom: none; }}
.flag-icon {{ font-size: 0.85rem; flex-shrink: 0; margin-top: 0.1rem; }}
.flag-main {{ flex: 1; }}
.flag-text {{ font-size: 0.84rem; color: {t['text']}; line-height: 1.5; }}
.flag-ref  {{ font-size: 0.72rem; margin-top: 0.1rem; }}
.flag-ref a {{ color: {t['accent']} !important; text-decoration: none; font-weight: 500; }}
.flag-ref a:hover {{ text-decoration: underline; }}

/* flags container */
.flags-block {{
    border: 1px solid {t['border']}; border-radius: 8px;
    padding: 0.25rem 0.9rem; background: {t['surface']};
    margin-bottom: 0.75rem;
}}

/* role note */
.role-box {{
    background: {t['accent_dim']}; border: 1px solid {t['accent']}33;
    border-radius: 8px; padding: 0.75rem 0.9rem; margin: 0.75rem 0 1rem;
    font-size: 0.83rem; color: {t['accent']}; line-height: 1.55;
}}
.role-box strong {{ font-weight: 700; }}

/* obligation table */
.ob-table {{ border: 1px solid {t['border']}; border-radius: 8px; overflow: hidden; margin-bottom: 0.6rem; }}
.ob-head {{
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase;
    color: {t['muted']}; background: {t['surface']}; padding: 0.5rem 0.9rem;
    border-bottom: 1px solid {t['border']};
}}
.ob-row {{ display: flex; align-items: baseline; gap: 0.75rem; padding: 0.6rem 0.9rem; border-bottom: 1px solid {t['border']}; }}
.ob-row:last-child {{ border-bottom: none; }}
.ob-check {{ color: {t['muted']}; font-size: 0.75rem; flex-shrink: 0; }}
.ob-text  {{ font-size: 0.83rem; color: {t['text']}; line-height: 1.45; flex: 1; }}
.ob-art   {{ font-size: 0.7rem; font-weight: 600; color: {t['accent']}; white-space: nowrap; flex-shrink: 0; }}
.ob-art a {{ color: {t['accent']} !important; text-decoration: none; }}
.ob-art a:hover {{ text-decoration: underline; }}
.ob-art-muted {{ color: {t['muted']}; }}

/* timeline */
.tl-table {{ border: 1px solid {t['border']}; border-radius: 8px; overflow: hidden; }}
.tl-row {{
    display: grid; grid-template-columns: 8px 120px 1fr 72px;
    align-items: center; gap: 0.8rem;
    padding: 0.75rem 0.9rem; border-bottom: 1px solid {t['border']};
}}
.tl-row:last-child {{ border-bottom: none; }}
.tl-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
.tl-date {{ font-size: 0.78rem; font-weight: 600; color: {t['text']}; white-space: nowrap; }}
.tl-desc {{ font-size: 0.8rem; color: {t['sub']}; }}
.tl-past .tl-date, .tl-past .tl-desc {{ color: {t['muted']}; }}

/* download */
.stDownloadButton > button {{
    background: {t['surface']} !important; color: {t['text']} !important;
    border: 1.5px solid {t['border2']} !important; border-radius: 8px !important;
    font-size: 0.88rem !important; font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.15s ease;
}}
.stDownloadButton > button:hover {{
    background: {t['accent_dim']} !important;
    border-color: {t['accent']} !important; color: {t['accent']} !important;
}}
.stDownloadButton > button p {{
    color: {t['text']} !important; font-size: 0.88rem !important; font-weight: 600 !important;
}}
.stDownloadButton > button:hover p {{
    color: {t['accent']} !important;
}}

/* st.button (non-form) — theme toggle */
.stButton > button {{
    background: {t['surface']} !important;
    color: {t['text']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 0.8rem !important;
    transition: all 0.15s ease;
    white-space: nowrap;
}}
.stButton > button:hover {{
    border-color: {t['accent']} !important;
    color: {t['accent']} !important;
    background: {t['accent_dim']} !important;
}}
.stButton > button p {{
    color: {t['text']} !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}}
.stButton > button:hover p {{
    color: {t['accent']} !important;
}}

/* st overrides */
.stCheckbox label {{ color: {t['text']} !important; font-size: 0.85rem !important; }}
label[data-testid="stWidgetLabel"] p {{ color: {t['text']} !important; font-size: 0.83rem !important; font-weight: 600 !important; }}
div[data-baseweb="select"] > div {{ background: {t['surface']} !important; border-color: {t['border']} !important; color: {t['text']} !important; }}
.stTextInput > div > div > input {{ background: {t['surface']} !important; border-color: {t['border']} !important; color: {t['text']} !important; }}
hr {{ border-color: {t['border']} !important; margin: 1.5rem 0 !important; }}
.stCaption p {{ color: {t['muted']} !important; font-size: 0.72rem !important; }}
</style>
"""

st.markdown(css(st.session_state.dark), unsafe_allow_html=True)

# ── Knowledge base ─────────────────────────────────────────────────────────────
PROHIBITED = {
    "social_scoring":       ("Social scoring by public authorities",                        "Art. 5(1)(c)"),
    "realtime_biometric":   ("Real-time biometric ID in publicly accessible spaces",        "Art. 5(1)(d)"),
    "subliminal":           ("Subliminal techniques bypassing conscious awareness",         "Art. 5(1)(a)"),
    "exploit_vuln":         ("Exploitation of vulnerability of specific groups",            "Art. 5(1)(b)"),
    "emotion_work":         ("Emotion recognition in workplace or education",               "Art. 5(1)(f)"),
    "biometric_cat":        ("Biometric categorisation inferring sensitive attributes",     "Art. 5(1)(e)"),
    "predictive_police":    ("Criminal risk profiling without objective facts",             "Art. 5(1)(g)"),
    "facial_scrape":        ("Untargeted scraping of facial images from internet/CCTV",     "Art. 5(1)(h)"),
}

ANNEX_III = {
    "medical":        ("Medical devices & healthcare",                      "Annex III §1"),
    "infrastructure": ("Critical infrastructure",                           "Annex III §2"),
    "education":      ("Education & vocational training",                   "Annex III §3"),
    "employment":     ("Employment & HR management",                        "Annex III §4"),
    "services":       ("Essential services (credit, insurance)",            "Annex III §5"),
    "law":            ("Law enforcement",                                   "Annex III §6"),
    "migration":      ("Migration, asylum & border control",                "Annex III §7"),
    "justice":        ("Administration of justice",                         "Annex III §8"),
    "safety":         ("Safety components of regulated products",           "Annex III §1"),
}

SECTOR_LABELS = {
    "none":           "General / Other",
    "medical":        "Medical devices & healthcare",
    "infrastructure": "Critical infrastructure (energy, water, transport)",
    "education":      "Education & vocational training",
    "employment":     "Employment, HR & workforce management",
    "services":       "Essential services (credit, insurance, social)",
    "law":            "Law enforcement",
    "migration":      "Migration, asylum & border control",
    "justice":        "Administration of justice & democracy",
    "safety":         "Safety components (vehicles, machinery, aviation)",
}

OBLIGATIONS = {
    "prohibited": {"Legal status": [
        ("This AI system is PROHIBITED in the EU — cease all activities immediately",    "Art. 5"),
        ("Development, placing on market, and operation are all infringements",          "Art. 5"),
        ("Maximum fine: €35,000,000 or 7% of total global annual turnover",             "Art. 99(3)"),
        ("Notify the relevant national market surveillance authority",                   "Art. 74"),
    ]},
    "high": {
        "Risk management": [
            ("Establish, implement and maintain a risk management system",               "Art. 9"),
            ("Identify and analyse all known and foreseeable risks",                     "Art. 9(2)"),
            ("Update risk management from post-market monitoring data",                  "Art. 9(6)"),
        ],
        "Data governance": [
            ("Implement data governance and management practices",                       "Art. 10"),
            ("Ensure datasets are relevant, representative and error-free",              "Art. 10(3)"),
            ("Document data gaps and apply bias mitigation measures",                    "Art. 10(5)"),
        ],
        "Technical documentation": [
            ("Prepare technical documentation before market placement (Annex IV)",       "Art. 11"),
            ("Keep documentation updated throughout the system's lifetime",              "Art. 11(2)"),
        ],
        "Logging": [
            ("Implement automatic event logging for the full system lifetime",           "Art. 12"),
            ("Deployers must retain logs for a minimum of 6 months",                    "Art. 12(2)"),
        ],
        "Transparency & human oversight": [
            ("Design for transparency so deployers can interpret outputs",               "Art. 13"),
            ("Provide instructions for use including purpose and oversight measures",    "Art. 13(3)"),
            ("Enable qualified persons to monitor, override and halt the system",        "Art. 14"),
            ("Train oversight personnel appropriately for the specific system",          "Art. 14(4)(c)"),
        ],
        "Accuracy & security": [
            ("Define accuracy metrics and maintain performance across the lifecycle",    "Art. 15"),
            ("Implement resilience against adversarial attacks and data poisoning",      "Art. 15(4)"),
            ("Apply cybersecurity measures proportionate to risk",                       "Art. 15(5)"),
        ],
        "Conformity & market access": [
            ("Conduct conformity assessment — self-assessment or third-party",           "Art. 43"),
            ("Draw up EU Declaration of Conformity (Annex V template)",                 "Art. 48"),
            ("Affix CE marking before placing on the EU market",                        "Art. 48"),
            ("Register in the EU AI public database before launch",                     "Art. 49"),
        ],
        "Post-market monitoring": [
            ("Establish a post-market monitoring plan",                                  "Art. 72"),
            ("Report serious incidents within 15 days",                                 "Art. 73(2)"),
            ("Cooperate with market surveillance authorities",                           "Art. 74"),
        ],
    },
    "gpai_systemic": {"Systemic risk — enhanced obligations": [
        ("Perform model evaluation including adversarial testing (red-teaming)",         "Art. 55(1)(a)"),
        ("Assess and mitigate systemic risks at EU and global level",                   "Art. 55(1)(b)"),
        ("Report serious incidents to the EU Commission without delay",                 "Art. 55(1)(c)"),
        ("Ensure appropriate cybersecurity protection for the model",                   "Art. 55(1)(d)"),
        ("Report energy consumption of training and operation to the AI Office",        "Art. 55(1)(e)"),
    ]},
    "gpai": {"General-purpose AI model obligations": [
        ("Prepare technical documentation (Annex XI and XII templates)",                "Art. 53(1)(a)"),
        ("Provide downstream providers with information for their compliance",          "Art. 53(1)(b)"),
        ("Publish and maintain a copyright transparency policy",                        "Art. 53(1)(c)"),
        ("Make a summary of training data publicly available",                          "Art. 53(1)(d)"),
        ("Comply with EU copyright law including text and data mining exceptions",      "Art. 53(2)"),
    ]},
    "limited": {"Transparency obligations": [
        ("Inform users they are interacting with an AI system",                         "Art. 50(1)"),
        ("Disclose that audio, image, video or text content is AI-generated",          "Art. 50(2)"),
        ("Apply machine-readable marking to AI-generated content",                     "Art. 50(4)"),
        ("Inform individuals when emotion recognition or biometric categorisation is used", "Art. 50(3)"),
    ]},
    "minimal": {"Recommended actions": [
        ("No specific mandatory obligations under the EU AI Act apply",                 "—"),
        ("Consider adopting a voluntary Code of Conduct (Annex IX)",                   "Art. 95"),
        ("Ensure AI literacy within your organisation",                                 "Art. 4"),
        ("Comply with GDPR, consumer protection and sector-specific rules",            "2016/679 EU"),
    ]},
}

# ── Classification logic ───────────────────────────────────────────────────────
def get_score(a):
    if any(a.get(k) for k in PROHIBITED): return 100
    s = 0
    if a["sector"] in ANNEX_III:  s += 60
    if a["safety_critical"]:       s += 20
    if a["affects_rights"]:        s += 15
    if a["autonomous"]:            s += 10
    if a["large_scale"]:           s += 8
    if a["gpai"]:                  s = max(s, 35)
    if a["interacts"]:             s = max(s, 30)
    if a["generates"]:             s = max(s, 25)
    return min(s, 99)

def classify(a):
    flags, ob_keys = [], []

    for key, (text, ref) in PROHIBITED.items():
        if a.get(key):
            flags.append({"text": text, "ref": ref, "kind": "err"})
    if flags:
        return "prohibited", flags, ["prohibited"]

    is_high = False
    if a["sector"] in ANNEX_III:
        label, ref = ANNEX_III[a["sector"]]
        flags.append({"text": f"{label} — mandatory conformity assessment required", "ref": ref, "kind": "warn"})
        is_high = True
    if a["safety_critical"]:
        flags.append({"text": "Safety component of a regulated product", "ref": "Annex III §1", "kind": "warn"})
        is_high = True
    if a["affects_rights"] and a["autonomous"]:
        flags.append({"text": "Autonomous decision affecting fundamental rights", "ref": "Art. 6(2)", "kind": "warn"})
        is_high = True
    if is_high:
        ob_keys.append("high")

    if a["gpai"]:
        flags.append({"text": "General-purpose AI model — GPAI obligations apply", "ref": "Art. 51", "kind": "info"})
        if a["gpai_systemic"] or a["gpai_flops"]:
            flags.append({"text": "Systemic risk threshold met (≥10²⁵ FLOPs or Commission designation)", "ref": "Art. 51(2)", "kind": "warn"})
            ob_keys.append("gpai_systemic")
        ob_keys.append("gpai")
        if not is_high:
            return "limited", flags, list(dict.fromkeys(["limited"] + ob_keys))

    if is_high:
        return "high", flags, list(dict.fromkeys(ob_keys))

    limited = []
    if a["interacts"]:  limited.append({"text": "Direct interaction with natural persons (chatbot / virtual agent)", "ref": "Art. 50(1)", "kind": "info"})
    if a["generates"]:  limited.append({"text": "Generates synthetic content (text, image, audio, video)", "ref": "Art. 50(2)", "kind": "info"})
    if a["emotion"]:    limited.append({"text": "Detects or infers emotional states", "ref": "Art. 50(3)", "kind": "info"})
    if limited:
        flags.extend(limited)
        return "limited", flags, list(dict.fromkeys(["limited"] + ob_keys))

    flags.append({"text": "No prohibited practices or Annex III triggers found", "ref": "Art. 6", "kind": "ok"})
    return "minimal", flags, ["minimal"]

# ── Render ─────────────────────────────────────────────────────────────────────
col_title, col_toggle = st.columns([5, 1])
with col_title:
    st.markdown('<div class="page-title">🇪🇺 EU AI Act Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Risk classification under Regulation (EU) 2024/1689 — answers generate an article-linked obligations checklist.</div>', unsafe_allow_html=True)
with col_toggle:
    st.markdown('<div style="margin-top:0.5rem;text-align:right;">', unsafe_allow_html=True)
    icon = "☀️ Light" if st.session_state.dark else "🌙 Dark"
    if st.button(icon, key="toggle", help="Toggle dark / light mode", use_container_width=True):
        st.session_state.dark = not st.session_state.dark
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("form"):

    st.markdown('<div class="sec-label">System basics</div>', unsafe_allow_html=True)
    system_name = st.text_input("System name", placeholder="e.g. Recruitment screening algorithm")
    c1, c2 = st.columns(2)
    with c1:
        org_role = st.selectbox("Your role", ["provider", "deployer", "importer", "distributor"],
            format_func=lambda x: {"provider": "Provider", "deployer": "Deployer", "importer": "Importer", "distributor": "Distributor"}[x])
    with c2:
        sector = st.selectbox("Deployment sector", list(SECTOR_LABELS.keys()), format_func=lambda x: SECTOR_LABELS[x])

    st.markdown(f'<div class="sec-label">Prohibited practices — <a href="{BASE}" target="_blank" style="color:inherit;font-weight:600;">Art. 5</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="warn-strip">If any item below applies, the system is banned in the EU regardless of purpose or safeguards.</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        social_scoring   = st.checkbox("Social scoring by public authorities")
        subliminal       = st.checkbox("Subliminal / deceptive manipulation")
        emotion_work     = st.checkbox("Emotion recognition at work or in education")
        pred_policing    = st.checkbox("Predictive criminal profiling")
    with cb:
        rt_biometric     = st.checkbox("Real-time biometric ID in public spaces")
        exploit_vuln     = st.checkbox("Exploitation of vulnerable groups")
        biometric_cat    = st.checkbox("Biometric categorisation of sensitive attributes")
        facial_scrape    = st.checkbox("Mass facial image scraping")

    st.markdown(f'<div class="sec-label">High-risk modifiers — <a href="{BASE}" target="_blank" style="color:inherit;font-weight:600;">Annex III</a></div>', unsafe_allow_html=True)
    cc, cd = st.columns(2)
    with cc:
        safety_critical = st.checkbox("Safety component of a regulated product")
        autonomous      = st.checkbox("Autonomous decisions without human review")
    with cd:
        affects_rights  = st.checkbox("Affects employment, credit, housing or liberty")
        large_scale     = st.checkbox("Affects 1 million+ individuals")

    st.markdown(f'<div class="sec-label">General-purpose AI model — <a href="{BASE}" target="_blank" style="color:inherit;font-weight:600;">Art. 51–55</a></div>', unsafe_allow_html=True)
    is_gpai = st.checkbox("This is a general-purpose AI model (LLM, foundation model, multimodal)")
    ce, cf = st.columns(2)
    with ce:
        gpai_flops    = st.checkbox("Training compute ≥ 10²⁵ FLOPs")
    with cf:
        gpai_systemic = st.checkbox("Designated systemic risk by EU Commission")

    st.markdown(f'<div class="sec-label">Transparency obligations — <a href="{BASE}" target="_blank" style="color:inherit;font-weight:600;">Art. 50</a></div>', unsafe_allow_html=True)
    cg, ch = st.columns(2)
    with cg:
        interacts = st.checkbox("Interacts directly with humans (chatbot, agent)")
        emotion   = st.checkbox("Detects or infers emotional states")
    with ch:
        generates = st.checkbox("Generates synthetic content (text, image, audio, video)")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Run assessment →", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if submitted:
    a = {
        "system_name": system_name or "AI System",
        "org_role": org_role, "sector": sector,
        "social_scoring": social_scoring, "realtime_biometric": rt_biometric,
        "subliminal": subliminal, "exploit_vuln": exploit_vuln,
        "emotion_work": emotion_work, "biometric_cat": biometric_cat,
        "predictive_police": pred_policing, "facial_scrape": facial_scrape,
        "safety_critical": safety_critical, "autonomous": autonomous,
        "affects_rights": affects_rights, "large_scale": large_scale,
        "gpai": is_gpai, "gpai_flops": gpai_flops, "gpai_systemic": gpai_systemic,
        "interacts": interacts, "generates": generates, "emotion": emotion,
    }

    risk, flags, ob_keys = classify(a)
    score = get_score(a)

    RISK_META = {
        "prohibited": ("🚫  Prohibited AI System",         "This system falls under the Art. 5 prohibited practices. It cannot legally be developed, deployed or used in the EU.",               "badge-red",    "#F26B7A" if st.session_state.dark else "#D93553"),
        "high":       ("🔴  High-Risk AI System",          "A conformity assessment, CE marking, EU AI database registration and compliance with Art. 9–15 are required before deployment.",    "badge-orange", "#F5924A" if st.session_state.dark else "#D9680A"),
        "limited":    ("🟡  Limited Risk AI System",       "Transparency obligations apply. Users must be informed they are interacting with an AI, and synthetic content must be labelled.",    "badge-yellow", "#E8C54A" if st.session_state.dark else "#9A7A05"),
        "minimal":    ("🟢  Minimal Risk AI System",       "No specific mandatory EU AI Act obligations. Voluntary codes of conduct and general EU law (GDPR, consumer protection) still apply.","badge-green",  "#4FC87A" if st.session_state.dark else "#1A7A40"),
    }
    label, desc, badge_cls, bar_color = RISK_META[risk]
    risk_short = {"prohibited": "PROHIBITED", "high": "HIGH RISK", "limited": "LIMITED RISK", "minimal": "MINIMAL RISK"}[risk]

    st.divider()
    st.markdown("## Result")

    st.markdown(f"""
    <div class="result-card">
      <span class="badge {badge_cls}">{risk_short}</span>
      <div class="result-level">{label}</div>
      <div class="result-desc">{desc}</div>
      <div class="score-wrap">
        <div class="score-meta"><span>Risk score</span><span>{score} / 100</span></div>
        <div class="score-track"><div class="score-fill" style="width:{score}%;background:{bar_color};"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Flags
    st.markdown("### Triggered criteria")
    icons = {"err": "🚨", "warn": "⚠️", "info": "ℹ️", "ok": "✓"}
    rows = ""
    for f in flags:
        ref_html = f'<div class="flag-ref"><a href="{BASE}" target="_blank" rel="noopener">{f["ref"]}</a></div>' if f.get("ref") and f["ref"] != "—" else ""
        rows += f'<div class="flag-row"><div class="flag-icon">{icons[f["kind"]]}</div><div class="flag-main"><div class="flag-text">{f["text"]}</div>{ref_html}</div></div>'
    st.markdown(f'<div class="flags-block">{rows}</div>', unsafe_allow_html=True)

    # Role note
    role_notes = {
        "provider":    "<strong>Provider:</strong> You are responsible for the conformity assessment, CE marking, Annex IV technical documentation, EU AI database registration and post-market monitoring.",
        "deployer":    "<strong>Deployer:</strong> Ensure human oversight, retain logs for ≥6 months, conduct a Fundamental Rights Impact Assessment for high-risk systems (Art. 27), and report incidents.",
        "importer":    "<strong>Importer:</strong> Verify the provider has completed all conformity assessments, technical documentation exists and CE marking is affixed before EU market entry (Art. 23).",
        "distributor": "<strong>Distributor:</strong> Verify CE marking and conformity documentation before making the system available and cooperate with market surveillance authorities (Art. 24).",
    }
    st.markdown(f'<div class="role-box">{role_notes[org_role]}</div>', unsafe_allow_html=True)

    # Obligations
    st.markdown("### Obligations checklist")
    for k in ob_keys:
        if k not in OBLIGATIONS: continue
        for group, items in OBLIGATIONS[k].items():
            rows = ""
            for text, ref in items:
                if ref and ref != "—":
                    art = f'<span class="ob-art"><a href="{BASE}" target="_blank" rel="noopener">{ref}</a></span>'
                else:
                    art = '<span class="ob-art ob-art-muted">—</span>'
                rows += f'<div class="ob-row"><span class="ob-check">☐</span><span class="ob-text">{text}</span>{art}</div>'
            st.markdown(f'<div class="ob-table"><div class="ob-head">{group}</div>{rows}</div>', unsafe_allow_html=True)

    # Timeline
    st.markdown("### Enforcement timeline")
    now = datetime.now()
    tl = [
        ("2024-08-01", "#6B7280",                                              "AI Act entered into force"),
        ("2025-02-02", "#6B7280",                                              "Prohibited practices (Art. 5) enforceable"),
        ("2025-08-02", "#F5924A" if st.session_state.dark else "#D9680A",      "GPAI model obligations (Art. 51–55)"),
        ("2026-08-02", "#5B8DF6" if st.session_state.dark else "#2B5CE6",      "High-risk systems — full application"),
        ("2027-08-02", "#4FC87A" if st.session_state.dark else "#1A7A40",      "Annex I product safety systems"),
    ]
    rows = ""
    for ds, color, desc_tl in tl:
        dt = datetime.strptime(ds, "%Y-%m-%d")
        past = dt < now
        upcoming = not past and abs((dt - now).days) < 120
        row_cls  = "tl-past" if past else ""
        dot_col  = "#50546A" if past else color
        b_cls    = "badge-muted"
        b_text   = "done" if past else ("upcoming" if upcoming else "")
        if not past and upcoming:
            b_cls = "badge-blue"
        rows += (
            f'<div class="tl-row {row_cls}">'
            f'<div class="tl-dot" style="background:{dot_col};"></div>'
            f'<div class="tl-date">{dt.strftime("%d %b %Y")}</div>'
            f'<div class="tl-desc">{desc_tl}</div>'
            f'<span class="badge {b_cls}">{b_text}</span>'
            f'</div>'
        )
    st.markdown(f'<div class="tl-table">{rows}</div>', unsafe_allow_html=True)

    # Downloads
    st.divider()
    report = {
        "tool": "EU AI Act Compliance Checker v5.0",
        "regulation": "Regulation (EU) 2024/1689",
        "source": BASE,
        "generated_at": datetime.now().isoformat(),
        "system": a["system_name"],
        "role": org_role,
        "sector": SECTOR_LABELS[sector],
        "risk_level": risk,
        "risk_score": score,
        "triggered": [{"text": f["text"], "ref": f["ref"]} for f in flags],
        "obligations": {
            k: {g: [{"text": t, "article": r, "url": BASE} for t, r in items]
                for g, items in OBLIGATIONS[k].items()}
            for k in ob_keys if k in OBLIGATIONS
        },
    }
    md = [
        f"# EU AI Act Compliance Report",
        f"**System:** {a['system_name']}  |  **Date:** {datetime.now().strftime('%d %B %Y')}  |  **Risk:** {label}  |  **Score:** {score}/100",
        f"\n[Regulation (EU) 2024/1689]({BASE})\n",
        "## Triggered criteria",
    ] + [f"- {f['text']} `{f['ref']}`" for f in flags] + ["\n## Obligations checklist"]
    for k in ob_keys:
        if k not in OBLIGATIONS: continue
        for g, items in OBLIGATIONS[k].items():
            md.append(f"\n### {g}")
            for t, r in items:
                md.append(f"- [ ] {t} — [{r}]({BASE})")
    md.append(f"\n---\n*EU AI Act Compliance Checker v5.0 — informational only, not legal advice.*")

    d1, d2 = st.columns(2)
    with d1:
        st.download_button("↓  JSON report", json.dumps(report, ensure_ascii=False, indent=2),
            f"eu_ai_act_{a['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json", use_container_width=True)
    with d2:
        st.download_button("↓  Markdown checklist", "\n".join(md),
            f"eu_ai_act_{a['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            "text/markdown", use_container_width=True)

st.divider()
st.caption(f"Informational only — not legal advice. [Regulation (EU) 2024/1689]({BASE}) · v5.0 · {datetime.now().year}")
