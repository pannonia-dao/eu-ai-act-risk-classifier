"""
EU AI Act Compliance Checker  ·  v3.0
Built on Regulation (EU) 2024/1689 — the EU Artificial Intelligence Act
Official text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
"""

import streamlit as st
import json
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Compliance Checker",
    page_icon="🇪🇺",
    layout="centered",
    menu_items={
        "Get Help": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
        "Report a bug": "https://github.com",
        "About": "EU AI Act Compliance Checker v3.0 — built on Regulation (EU) 2024/1689",
    },
)

# ──────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM  —  clean light professional
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp { background: #F7F8FA; }
.main .block-container {
    max-width: 820px;
    padding: 2.5rem 2rem 4rem 2rem;
}

/* ── Hero header ── */
.hero-wrap {
    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 60%, #1D4ED8 100%);
    border-radius: 20px;
    padding: 2.4rem 2.6rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-kicker {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #93C5FD;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 0.6rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #BFDBFE;
    line-height: 1.6;
    max-width: 540px;
}
.hero-badges {
    margin-top: 1.2rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: #E0F2FE;
}

/* ── How it works panel ── */
.how-panel {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.8rem;
}
.how-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 1rem;
}
.how-steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
}
.how-step {
    text-align: center;
    padding: 0.6rem 0.3rem;
}
.how-num {
    width: 30px; height: 30px;
    background: #EFF6FF;
    border: 2px solid #BFDBFE;
    border-radius: 50%;
    font-size: 0.8rem;
    font-weight: 800;
    color: #2563EB;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem auto;
}
.how-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #374151;
    line-height: 1.35;
}
.how-desc {
    font-size: 0.72rem;
    color: #9CA3AF;
    margin-top: 0.2rem;
    line-height: 1.3;
}

/* ── Section header ── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.8rem 0 0.8rem 0;
}
.sec-num {
    background: #2563EB;
    color: white;
    font-size: 0.7rem;
    font-weight: 800;
    width: 22px; height: 22px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.sec-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: 0.01em;
}
.sec-ref {
    margin-left: auto;
    font-size: 0.7rem;
    color: #9CA3AF;
}
.sec-ref a {
    color: #2563EB !important;
    text-decoration: none;
    font-weight: 600;
}
.sec-ref a:hover { text-decoration: underline; }

/* ── Form card ── */
.form-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
}
.warn-note {
    background: #FEF3C7;
    border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 0.9rem;
    font-size: 0.8rem;
    color: #92400E;
    margin-bottom: 0.8rem;
    font-weight: 500;
}

/* ── Submit button ── */
div[data-testid="stFormSubmitButton"] > button {
    background: #2563EB !important;
    color: white !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.02em;
    transition: all 0.15s ease;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #1D4ED8 !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px);
}

/* ── Result ── */
.result-wrap { margin-top: 2rem; }

.risk-card {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
}
.risk-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    opacity: 0.8;
}
.risk-label {
    font-size: 1.6rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.4rem;
}
.risk-desc {
    font-size: 0.88rem;
    line-height: 1.5;
    opacity: 0.85;
    max-width: 520px;
}
.score-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-top: 1.2rem;
}
.score-label { font-size: 0.75rem; font-weight: 600; opacity: 0.7; white-space: nowrap; }
.score-track {
    flex: 1;
    height: 8px;
    background: rgba(0,0,0,0.12);
    border-radius: 4px;
    overflow: hidden;
}
.score-fill { height: 100%; border-radius: 4px; }
.score-val { font-size: 0.8rem; font-weight: 800; opacity: 0.85; white-space: nowrap; }

.card-prohibited {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 2px solid #F43F5E;
    color: #881337;
}
.card-prohibited .score-fill { background: linear-gradient(90deg, #F43F5E, #BE123C); }

.card-high {
    background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
    border: 2px solid #F97316;
    color: #7C2D12;
}
.card-high .score-fill { background: linear-gradient(90deg, #F97316, #EA580C); }

.card-limited {
    background: linear-gradient(135deg, #FEFCE8 0%, #FEF9C3 100%);
    border: 2px solid #EAB308;
    color: #713F12;
}
.card-limited .score-fill { background: linear-gradient(90deg, #EAB308, #CA8A04); }

.card-minimal {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 2px solid #22C55E;
    color: #14532D;
}
.card-minimal .score-fill { background: linear-gradient(90deg, #22C55E, #16A34A); }

/* ── Trigger flags ── */
.flags-section { margin: 1.2rem 0; }
.flag-item {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
}
.flag-item.err  { border-left: 3px solid #F43F5E; }
.flag-item.warn { border-left: 3px solid #F97316; }
.flag-item.info { border-left: 3px solid #2563EB; }
.flag-item.ok   { border-left: 3px solid #22C55E; }
.flag-ico { font-size: 1rem; flex-shrink: 0; margin-top: 0.05rem; }
.flag-body { flex: 1; }
.flag-text { font-size: 0.85rem; color: #374151; line-height: 1.5; font-weight: 500; }
.flag-link { font-size: 0.75rem; margin-top: 0.15rem; }
.flag-link a { color: #2563EB; text-decoration: none; font-weight: 600; }
.flag-link a:hover { text-decoration: underline; }

/* ── Role note ── */
.role-note {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    display: flex;
    gap: 0.7rem;
    margin: 0.8rem 0 1.2rem 0;
    align-items: flex-start;
}
.role-ico { font-size: 1rem; flex-shrink: 0; margin-top: 0.1rem; }
.role-text { font-size: 0.84rem; color: #1E40AF; line-height: 1.5; }
.role-text strong { font-weight: 700; }

/* ── Obligations ── */
.ob-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B7280;
    margin: 1.4rem 0 0.6rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #E5E7EB;
}
.ob-group-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 0.7rem;
}
.ob-group-head {
    background: #F9FAFB;
    border-bottom: 1px solid #E5E7EB;
    padding: 0.6rem 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #374151;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.ob-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 1rem;
    border-bottom: 1px solid #F3F4F6;
    gap: 1rem;
}
.ob-row:last-child { border-bottom: none; }
.ob-text { font-size: 0.85rem; color: #374151; line-height: 1.45; flex: 1; }
.ob-art {
    flex-shrink: 0;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 5px;
    padding: 0.15rem 0.5rem;
    font-size: 0.7rem;
    font-weight: 700;
    color: #2563EB;
    white-space: nowrap;
}
.ob-art a {
    color: #2563EB !important;
    text-decoration: none;
}
.ob-art a:hover { text-decoration: underline; }

/* ── Timeline ── */
.tl-wrap {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
}
.tl-row {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #F3F4F6;
}
.tl-row:last-child { border-bottom: none; }
.tl-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 0.35rem;
}
.tl-date { font-size: 0.8rem; font-weight: 700; color: #111827; min-width: 130px; }
.tl-desc { font-size: 0.82rem; color: #6B7280; line-height: 1.4; }
.tl-past .tl-desc { color: #9CA3AF; }
.tl-now .tl-date  { color: #2563EB; }
.tl-now .tl-desc  { color: #374151; font-weight: 600; }

/* ── Download ── */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
.stDownloadButton > button:hover {
    background: #F9FAFB !important;
    border-color: #2563EB !important;
    color: #2563EB !important;
}

/* ── Misc ── */
.stCheckbox label { color: #374151 !important; font-size: 0.88rem !important; }
.stSelectbox label, .stTextInput label { color: #374151 !important; font-weight: 600 !important; font-size: 0.85rem !important; }
hr { border-color: #E5E7EB !important; }
.stCaption { color: #9CA3AF !important; font-size: 0.75rem !important; }
h2 { color: #111827 !important; font-size: 1.2rem !important; font-weight: 800 !important; }
h3 { color: #374151 !important; font-size: 1rem !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ARTICLE LINKS  —  all point to official EUR-Lex
# ──────────────────────────────────────────────────────────────────────────────
BASE = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"

def art_link(label: str) -> str:
    """Return clickable article badge pointing to official text."""
    return f'<a href="{BASE}" target="_blank" rel="noopener">{label}</a>'

# ──────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE BASE
# ──────────────────────────────────────────────────────────────────────────────

PROHIBITED_PRACTICES = {
    "social_scoring":           ("Social scoring by public authorities",                   "Art. 5(1)(c)"),
    "realtime_biometric":       ("Real-time remote biometric ID in publicly accessible spaces","Art. 5(1)(d)"),
    "subliminal_manipulation":  ("Subliminal techniques bypassing conscious awareness",    "Art. 5(1)(a)"),
    "exploit_vulnerability":    ("Exploitation of vulnerability of specific groups",       "Art. 5(1)(b)"),
    "emotion_recognition_work": ("Emotion recognition in workplace or educational institutions","Art. 5(1)(f)"),
    "biometric_categorization": ("Biometric categorisation inferring sensitive attributes","Art. 5(1)(e)"),
    "predictive_policing":      ("Individual criminal risk profiling without objective facts","Art. 5(1)(g)"),
    "facial_scraping":          ("Untargeted scraping of facial images from internet/CCTV","Art. 5(1)(h)"),
}

ANNEX_III = {
    "medical_devices":          ("Medical devices / health & safety",           "Annex III §1"),
    "critical_infrastructure":  ("Critical infrastructure management",          "Annex III §2"),
    "education_vocational":     ("Education & vocational training",             "Annex III §3"),
    "employment_hr":            ("Employment, HR & worker management",          "Annex III §4"),
    "essential_services":       ("Access to essential services (credit, insurance)","Annex III §5"),
    "law_enforcement":          ("Law enforcement",                             "Annex III §6"),
    "migration_asylum":         ("Migration, asylum & border control",          "Annex III §7"),
    "justice_democracy":        ("Administration of justice & democratic processes","Annex III §8"),
    "safety_components":        ("Safety components of products (vehicles, machinery)","Annex III §1"),
}

OBLIGATIONS = {
    "unacceptable": {
        "Legal Status": [
            ("This AI system is PROHIBITED in the EU — immediate cessation required",             "Art. 5"),
            ("Development, placing on market, putting into service all constitute an infringement","Art. 5"),
            ("Maximum penalty: €35,000,000 or 7% of global annual turnover",                     "Art. 99(3)"),
            ("Notifying the relevant market surveillance authority is mandatory",                  "Art. 74"),
        ],
    },
    "high": {
        "Risk Management": [
            ("Establish, implement, document and maintain a risk management system",               "Art. 9"),
            ("Identify and analyse known and foreseeable risks throughout the lifecycle",          "Art. 9(2)"),
            ("Evaluate risks based on data from post-market monitoring",                          "Art. 9(6)"),
        ],
        "Data & Data Governance": [
            ("Implement data governance and management practices",                                 "Art. 10"),
            ("Ensure training, validation and testing datasets are relevant, representative and error-free","Art. 10(3)"),
            ("Document data gaps and apply bias mitigation measures",                             "Art. 10(5)"),
        ],
        "Technical Documentation": [
            ("Prepare technical documentation before placing on market (Annex IV template)",       "Art. 11"),
            ("Keep documentation up-to-date throughout the system's lifetime",                    "Art. 11(2)"),
            ("Provide documentation to market surveillance authorities on request",               "Art. 11(3)"),
        ],
        "Logging & Audit Trail": [
            ("Implement automatic logging capabilities for the lifetime of the system",           "Art. 12"),
            ("Logs must retain records sufficient to trace decisions post-deployment",            "Art. 12(1)"),
            ("Retain logs for at least 6 months (deployers) unless otherwise specified",         "Art. 12(2)"),
        ],
        "Transparency & Instructions": [
            ("Design for transparency enabling deployers to interpret outputs",                   "Art. 13"),
            ("Provide instructions for use including intended purpose, performance metrics, oversight measures","Art. 13(3)"),
        ],
        "Human Oversight": [
            ("Enable human operators to oversee, understand and override the system",             "Art. 14"),
            ("Ensure humans can intervene or halt the system when necessary",                     "Art. 14(4)"),
            ("Train oversight personnel appropriately for the system in use",                     "Art. 14(4)(c)"),
        ],
        "Accuracy, Robustness & Cybersecurity": [
            ("Specify accuracy metrics and maintain performance across the lifecycle",            "Art. 15"),
            ("Implement resilience against adversarial attacks and data poisoning",               "Art. 15(4)"),
            ("Apply appropriate cybersecurity measures commensurate with the risk",              "Art. 15(5)"),
        ],
        "Conformity Assessment & Market Access": [
            ("Conduct conformity assessment (self-assessment or third-party, per Annex VI/VII)",  "Art. 43"),
            ("Draw up EU declaration of conformity (Annex V template)",                          "Art. 48"),
            ("Affix CE marking before placing on the EU market",                                  "Art. 48"),
            ("Register in the EU AI public database before market launch",                       "Art. 49"),
        ],
        "Post-Market Monitoring & Incidents": [
            ("Establish a post-market monitoring plan and collect performance data",              "Art. 72"),
            ("Report serious incidents to national authority within 15 days",                    "Art. 73(2)"),
            ("Cooperate with market surveillance authorities on inspections and investigations", "Art. 74"),
        ],
    },
    "gpai_systemic": {
        "Systemic Risk — Enhanced Obligations (Art. 55)": [
            ("Perform model evaluation including adversarial testing ('red-teaming')",            "Art. 55(1)(a)"),
            ("Assess and mitigate systemic risks at EU and global level",                        "Art. 55(1)(b)"),
            ("Report serious incidents and corrective measures to the Commission without delay", "Art. 55(1)(c)"),
            ("Ensure appropriate cybersecurity protection for the model and infrastructure",     "Art. 55(1)(d)"),
            ("Report energy consumption of training and operation to the AI Office",             "Art. 55(1)(e)"),
        ],
    },
    "gpai": {
        "General-Purpose AI Model Obligations (Art. 53)": [
            ("Prepare and maintain technical documentation (Annex XI & XII templates)",          "Art. 53(1)(a)"),
            ("Provide downstream providers with information needed for their compliance",        "Art. 53(1)(b)"),
            ("Publish and maintain a copyright transparency policy",                             "Art. 53(1)(c)"),
            ("Make a sufficiently detailed summary of training data publicly available",         "Art. 53(1)(d)"),
            ("Adhere to EU copyright law including text and data mining exceptions",             "Art. 53(2)"),
        ],
    },
    "limited": {
        "Transparency Obligations (Art. 50)": [
            ("Inform users that they are interacting with an AI system (chatbots/virtual agents)","Art. 50(1)"),
            ("Disclose that content is AI-generated for synthetic audio, image, video or text",  "Art. 50(2)"),
            ("Label AI-generated or manipulated content with machine-readable marking",          "Art. 50(4)"),
            ("Inform users when emotion recognition or biometric categorisation is applied",     "Art. 50(3)"),
        ],
    },
    "minimal": {
        "Recommended Voluntary Actions": [
            ("No specific mandatory obligations under the EU AI Act apply to this system",       "—"),
            ("Consider adopting a voluntary Code of Conduct aligned with Annex IX principles",  "Art. 95"),
            ("Ensure AI literacy within your organisation as a general obligation",              "Art. 4"),
            ("Comply with applicable GDPR, consumer protection and sector-specific rules",       "2016/679 EU"),
        ],
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# CLASSIFICATION ENGINE
# ──────────────────────────────────────────────────────────────────────────────

def risk_score(a: dict) -> int:
    if any(a.get(k) for k in PROHIBITED_PRACTICES):
        return 100
    s = 0
    if a.get("sector") in ANNEX_III: s += 60
    if a.get("safety_critical"):     s += 20
    if a.get("affects_rights"):      s += 15
    if a.get("autonomous"):          s += 10
    if a.get("large_scale"):         s += 8
    if a.get("gpai_model"):          s = max(s, 35)
    if a.get("interacts_humans"):    s = max(s, 30)
    if a.get("generates_content"):   s = max(s, 25)
    return min(s, 99)

def classify(a: dict):
    """Return (risk_level, flags_list, ob_keys_list)."""
    flags, ob_keys = [], []

    # ── Prohibited (Art. 5) ──────────────────────────────────────────────────
    for key, (desc, ref) in PROHIBITED_PRACTICES.items():
        if a.get(key):
            flags.append({"text": desc, "ref": ref, "sev": "err"})
    if flags:
        return "prohibited", flags, ["unacceptable"]

    # ── High-risk (Annex III) ────────────────────────────────────────────────
    is_high = False
    sector = a.get("sector", "general")
    if sector in ANNEX_III:
        label, ref = ANNEX_III[sector]
        flags.append({"text": f"{label} sector — mandatory conformity assessment required", "ref": ref, "sev": "warn"})
        is_high = True
    if a.get("safety_critical"):
        flags.append({"text": "Safety component of regulated product", "ref": "Annex III §1", "sev": "warn"})
        is_high = True
    if a.get("affects_rights") and a.get("autonomous"):
        flags.append({"text": "Autonomous decision affecting fundamental rights — high-risk threshold met", "ref": "Art. 6(2)", "sev": "warn"})
        is_high = True
    if is_high:
        ob_keys.append("high")

    # ── GPAI (Art. 51-55) ───────────────────────────────────────────────────
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

    # ── Limited risk (Art. 50) ───────────────────────────────────────────────
    limited_triggers = []
    if a.get("interacts_humans"):
        limited_triggers.append({"text": "Direct interaction with natural persons (chatbot / virtual agent)", "ref": "Art. 50(1)", "sev": "info"})
    if a.get("generates_content"):
        limited_triggers.append({"text": "Synthetic content generation (text, image, audio, video)", "ref": "Art. 50(2)", "sev": "info"})
    if a.get("emotion_detect"):
        limited_triggers.append({"text": "Emotion recognition system (outside prohibited contexts)", "ref": "Art. 50(3)", "sev": "info"})
    if limited_triggers:
        flags.extend(limited_triggers)
        ob_keys.append("limited")
        return "limited", flags, list(dict.fromkeys(ob_keys))

    # ── Minimal ──────────────────────────────────────────────────────────────
    flags.append({"text": "No prohibited practices or Annex III triggers identified — minimal risk", "ref": "Art. 6", "sev": "ok"})
    return "minimal", flags, ["minimal"]

# ──────────────────────────────────────────────────────────────────────────────
# HERO + HOW IT WORKS
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-wrap">
    <div class="hero-kicker">Regulation (EU) 2024/1689 &nbsp;·&nbsp; AI Act Compliance Tool</div>
    <div class="hero-title">EU AI Act<br>Compliance Checker</div>
    <div class="hero-sub">
        Answer 20 questions about your AI system and receive an instant, article-level risk classification
        with all mandatory obligations — ready to attach to your compliance dossier.
    </div>
    <div class="hero-badges">
        <span class="hero-badge">🇪🇺 Reg. 2024/1689</span>
        <span class="hero-badge">Art. 5 · 6 · 50 · 51-55</span>
        <span class="hero-badge">Annex III · IV · V</span>
        <span class="hero-badge">v3.0 · 2025</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="how-panel">
    <div class="how-title">How it works</div>
    <div class="how-steps">
        <div class="how-step">
            <div class="how-num">1</div>
            <div class="how-label">Describe your system</div>
            <div class="how-desc">Role, sector, deployment context</div>
        </div>
        <div class="how-step">
            <div class="how-num">2</div>
            <div class="how-label">Check prohibited practices</div>
            <div class="how-desc">All 8 Art. 5 triggers reviewed</div>
        </div>
        <div class="how-step">
            <div class="how-num">3</div>
            <div class="how-label">Assess risk level</div>
            <div class="how-desc">Annex III · GPAI · Art. 50 logic</div>
        </div>
        <div class="how-step">
            <div class="how-num">4</div>
            <div class="how-label">Get your obligations</div>
            <div class="how-desc">Article-linked checklist + JSON report</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FORM
# ──────────────────────────────────────────────────────────────────────────────

with st.form("ai_act_form"):

    # ── Section 1: System basics ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-num">1</div>
        <div class="sec-title">System Basics</div>
        <div class="sec-ref"><a href="{BASE}" target="_blank">Art. 3 — Definitions</a></div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        system_name = st.text_input(
            "System name / identifier",
            placeholder="e.g. Recruitment screening algorithm, Medical image classifier…"
        )
        col1, col2 = st.columns(2)
        with col1:
            org_role = st.selectbox(
                "Your organisation's role",
                ["provider", "deployer", "importer", "distributor"],
                format_func=lambda x: {
                    "provider":    "Provider — develops / places on market",
                    "deployer":    "Deployer — uses under own responsibility",
                    "importer":    "Importer — brings into EU from third country",
                    "distributor": "Distributor — makes available on EU market",
                }[x]
            )
        with col2:
            sector = st.selectbox(
                "Primary deployment sector",
                ["general", "medical_devices", "critical_infrastructure", "education_vocational",
                 "employment_hr", "essential_services", "law_enforcement",
                 "migration_asylum", "justice_democracy", "safety_components"],
                format_func=lambda x: {
                    "general":              "General / Other",
                    "medical_devices":      "Medical devices & healthcare",
                    "critical_infrastructure": "Critical infrastructure (energy, water, transport)",
                    "education_vocational": "Education & vocational training",
                    "employment_hr":        "Employment, HR & workforce management",
                    "essential_services":   "Essential services (credit, insurance, social benefits)",
                    "law_enforcement":      "Law enforcement",
                    "migration_asylum":     "Migration, asylum & border control",
                    "justice_democracy":    "Administration of justice & democracy",
                    "safety_components":    "Safety components (vehicles, machinery, aviation)",
                }[x]
            )

    # ── Section 2: Prohibited practices (Art. 5) ─────────────────────────────
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-num">2</div>
        <div class="sec-title">Prohibited Practices — Article 5</div>
        <div class="sec-ref"><a href="{BASE}" target="_blank">Art. 5 full text ↗</a></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="warn-note">⚠️  If any of the following applies, the system is <strong>banned in the EU</strong> regardless of sector or purpose.</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        social_scoring      = st.checkbox("Social scoring by public authorities  [Art. 5(1)(c)]")
        subliminal          = st.checkbox("Subliminal / deceptive manipulation techniques  [Art. 5(1)(a)]")
        emotion_work        = st.checkbox("Emotion recognition at workplace or in education  [Art. 5(1)(f)]")
        predictive_policing = st.checkbox("Predictive criminal profiling without objective facts  [Art. 5(1)(g)]")
    with col_b:
        realtime_biometric  = st.checkbox("Real-time biometric ID in public spaces  [Art. 5(1)(d)]")
        exploit_vuln        = st.checkbox("Exploitation of vulnerable groups  [Art. 5(1)(b)]")
        biometric_cat       = st.checkbox("Biometric categorisation revealing sensitive attributes  [Art. 5(1)(e)]")
        facial_scraping     = st.checkbox("Mass facial image scraping from internet / CCTV  [Art. 5(1)(h)]")

    # ── Section 3: High-risk modifiers ───────────────────────────────────────
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-num">3</div>
        <div class="sec-title">High-Risk Modifiers — Annex III & Art. 6</div>
        <div class="sec-ref"><a href="{BASE}" target="_blank">Annex III ↗</a></div>
    </div>""", unsafe_allow_html=True)

    col_c, col_d = st.columns(2)
    with col_c:
        safety_critical = st.checkbox("Safety component of a regulated product (machinery, vehicle, medical device)")
        autonomous      = st.checkbox("Makes autonomous decisions without human review")
    with col_d:
        affects_rights  = st.checkbox("Affects access to employment, credit, housing, education or liberty")
        large_scale     = st.checkbox("Deployed at large scale (1M+ individuals affected)")

    # ── Section 4: GPAI (Art. 51-55) ─────────────────────────────────────────
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-num">4</div>
        <div class="sec-title">General-Purpose AI Model (GPAI) — Articles 51–55</div>
        <div class="sec-ref"><a href="{BASE}" target="_blank">Art. 51-55 ↗</a></div>
    </div>""", unsafe_allow_html=True)

    gpai_model    = st.checkbox("This is a general-purpose AI model (LLM, foundation model, multimodal model)")
    col_e, col_f = st.columns(2)
    with col_e:
        gpai_flops    = st.checkbox("Training compute ≥ 10²⁵ FLOPs (systemic risk threshold)")
    with col_f:
        gpai_systemic = st.checkbox("Designated as systemic risk model by the EU Commission")

    # ── Section 5: Limited risk (Art. 50) ────────────────────────────────────
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-num">5</div>
        <div class="sec-title">Transparency Obligations — Article 50</div>
        <div class="sec-ref"><a href="{BASE}" target="_blank">Art. 50 ↗</a></div>
    </div>""", unsafe_allow_html=True)

    col_g, col_h = st.columns(2)
    with col_g:
        interacts_humans  = st.checkbox("Directly interacts with humans (chatbot, virtual agent)")
        emotion_detect    = st.checkbox("Detects or infers emotional states of individuals")
    with col_h:
        generates_content = st.checkbox("Generates synthetic content (text, image, audio, video, code)")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("⚡  Run Compliance Assessment", use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# RESULTS
# ──────────────────────────────────────────────────────────────────────────────

if submitted:
    answers = {
        "system_name":          system_name or "AI System",
        "org_role":             org_role,
        "sector":               sector,
        "social_scoring":       social_scoring,
        "realtime_biometric":   realtime_biometric,
        "subliminal_manipulation": subliminal,
        "exploit_vulnerability":exploit_vuln,
        "emotion_recognition_work": emotion_work,
        "biometric_categorization": biometric_cat,
        "predictive_policing":  predictive_policing,
        "facial_scraping":      facial_scraping,
        "safety_critical":      safety_critical,
        "autonomous":           autonomous,
        "affects_rights":       affects_rights,
        "large_scale":          large_scale,
        "gpai_model":           gpai_model,
        "gpai_flops":           gpai_flops,
        "gpai_systemic":        gpai_systemic,
        "interacts_humans":     interacts_humans,
        "generates_content":    generates_content,
        "emotion_detect":       emotion_detect,
    }

    risk_level, flags, ob_keys = classify(answers)
    score = risk_score(answers)

    RISK_CFG = {
        "prohibited": {
            "eyebrow":  "Article 5 — Prohibited Practice",
            "label":    "🚫  Prohibited AI System",
            "desc":     "This system falls under the prohibited AI practices of Art. 5. It cannot be developed, placed on the market, put into service, or used in the EU.",
            "card":     "card-prohibited",
            "bar":      "bar-prohibited",
        },
        "high": {
            "eyebrow":  "Annex III — High-Risk AI System",
            "label":    "🔴  High-Risk AI System",
            "desc":     "This system requires a full conformity assessment, CE marking, EU AI database registration, and compliance with Art. 9–15 before market deployment.",
            "card":     "card-high",
            "bar":      "bar-high",
        },
        "limited": {
            "eyebrow":  "Article 50 — Limited Risk AI System",
            "label":    "🟡  Limited Risk AI System",
            "desc":     "Transparency obligations apply. Users must be informed they are interacting with an AI, and synthetic content must be labelled accordingly.",
            "card":     "card-limited",
            "bar":      "bar-limited",
        },
        "minimal": {
            "eyebrow":  "Article 6 — Minimal Risk AI System",
            "label":    "🟢  Minimal Risk AI System",
            "desc":     "No specific mandatory obligations under the EU AI Act. Voluntary codes of conduct and general EU law (GDPR, consumer protection) still apply.",
            "card":     "card-minimal",
            "bar":      "bar-minimal",
        },
    }
    cfg = RISK_CFG[risk_level]

    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
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
            <div class="score-track">
                <div class="score-fill {cfg['bar']}" style="width:{score}%"></div>
            </div>
            <div class="score-val">{score} / 100</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Triggered flags
    st.markdown("### Triggered Criteria")
    ico_map = {"err": "🚨", "warn": "⚠️", "info": "ℹ️", "ok": "✅"}
    for f in flags:
        ico = ico_map.get(f["sev"], "•")
        link_html = f'<div class="flag-link"><a href="{BASE}" target="_blank" rel="noopener">→ {f["ref"]}</a></div>' if f.get("ref") and f["ref"] != "—" else ""
        st.markdown(f"""
        <div class="flag-item {f['sev']}">
            <div class="flag-ico">{ico}</div>
            <div class="flag-body">
                <div class="flag-text">{f['text']}</div>
                {link_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Role-specific guidance
    role_guidance = {
        "provider":    "As <strong>Provider</strong>, you are responsible for the conformity assessment, CE marking, technical documentation (Annex IV), registration in the EU AI database, and post-market monitoring obligations.",
        "deployer":    "As <strong>Deployer</strong>, you must ensure human oversight, keep logs for at least 6 months, conduct a fundamental rights impact assessment for high-risk systems (Art. 27), and report incidents.",
        "importer":    "As <strong>Importer</strong>, you must verify the provider has completed the conformity assessment, technical documentation exists, and CE marking is in place before EU market entry.",
        "distributor": "As <strong>Distributor</strong>, verify CE marking and conformity documentation before making the system available, and cooperate with market surveillance authorities.",
    }
    st.markdown(f"""
    <div class="role-note">
        <div class="role-ico">💼</div>
        <div class="role-text">{role_guidance[org_role]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Obligations
    st.markdown("### Mandatory Obligations & Compliance Checklist")
    for ob_key in ob_keys:
        if ob_key not in OBLIGATIONS:
            continue
        for group_name, items in OBLIGATIONS[ob_key].items():
            rows_html = ""
            for text, ref in items:
                if ref and ref != "—":
                    badge = f'<span class="ob-art">{art_link(ref)}</span>'
                else:
                    badge = '<span class="ob-art" style="background:#F3F4F6;border-color:#E5E7EB;color:#9CA3AF;">—</span>'
                rows_html += f'<div class="ob-row"><div class="ob-text">{text}</div>{badge}</div>'
            st.markdown(f"""
            <div class="ob-group-card">
                <div class="ob-group-head">{group_name}</div>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)

    # Implementation timeline
    st.markdown("### ⏱ Enforcement Timeline")
    now = datetime.now()
    tl = [
        ("2024-08-01", "#6B7280", "EU AI Act entered into force"),
        ("2025-02-02", "#6B7280", "Art. 5 — Prohibited practices enforceable"),
        ("2025-08-02", "#F97316" if now < datetime(2025, 8, 2) else "#6B7280",
         "GPAI model obligations enforceable (Art. 51–55)"),
        ("2026-08-02", "#2563EB" if now < datetime(2026, 8, 2) else "#6B7280",
         "High-risk systems (Annex III) — full application"),
        ("2027-08-02", "#22C55E",
         "Annex I product safety systems — extended deadline"),
    ]
    rows_html = ""
    for date_str, color, desc in tl:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        cls = "tl-now" if abs((dt - now).days) < 60 else ("tl-past" if dt < now else "")
        rows_html += f"""
        <div class="tl-row {cls}">
            <div class="tl-dot" style="background:{color};"></div>
            <div class="tl-date">{dt.strftime("%d %b %Y")}</div>
            <div class="tl-desc">{desc}</div>
        </div>
        """
    st.markdown(f'<div class="tl-wrap">{rows_html}</div>', unsafe_allow_html=True)

    # Downloads
    st.divider()
    st.markdown("### Download Compliance Report")
    report = {
        "tool": "EU AI Act Compliance Checker v3.0",
        "regulation": "Regulation (EU) 2024/1689",
        "official_text": BASE,
        "generated_at": datetime.now().isoformat(),
        "system_name": answers["system_name"],
        "organisation_role": org_role,
        "sector": sector,
        "risk_level": risk_level,
        "risk_score": score,
        "triggered_criteria": [f["text"] for f in flags],
        "obligations": {
            k: {g: [{"obligation": t, "article": a, "source_url": BASE}
                    for t, a in items]
                for g, items in OBLIGATIONS[k].items()}
            for k in ob_keys if k in OBLIGATIONS
        },
    }
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥  Download JSON Report",
            data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name=f"eu_ai_act_{answers['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_dl2:
        md_lines = [
            f"# EU AI Act Compliance Report",
            f"**System:** {answers['system_name']}  ",
            f"**Date:** {datetime.now().strftime('%d %B %Y')}  ",
            f"**Regulation:** [EU 2024/1689]({BASE})  ",
            f"**Risk Level:** {cfg['label']}  ",
            f"**Risk Score:** {score}/100  ",
            "",
            "## Triggered Criteria",
        ]
        for f in flags:
            md_lines.append(f"- {f['text']} `{f.get('ref','')}`")
        md_lines.append("\n## Obligations")
        for k in ob_keys:
            if k not in OBLIGATIONS:
                continue
            for g, items in OBLIGATIONS[k].items():
                md_lines.append(f"\n### {g}")
                for text, ref in items:
                    md_lines.append(f"- [ ] {text} — [{ref}]({BASE})")
        md_lines.append(f"\n---\n*Generated by EU AI Act Compliance Checker v3.0 — not legal advice.*")
        st.download_button(
            "📥  Download Markdown Checklist",
            data="\n".join(md_lines),
            file_name=f"eu_ai_act_{answers['system_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "⚠️ This tool is for informational purposes only and does not constitute legal advice. "
    "Always consult a qualified legal professional for compliance decisions. "
    f"Built on [Regulation (EU) 2024/1689]({BASE}) · v3.0 · {datetime.now().year}"
)
