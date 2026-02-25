import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="EU AI Act Megfelelőség-vizsgáló",
    page_icon="🇪🇺",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: #0d1117; color: #e6edf3; }
    .main .block-container { max-width: 860px; padding-top: 2rem; }

    /* Header */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #7b61ff 50%, #ff3d6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    .hero-sub {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Section headers */
    .section-pill {
        display: inline-block;
        background: linear-gradient(135deg, #1c2333, #21262d);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 0.35rem 1rem;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #7b61ff;
        margin: 1.2rem 0 0.6rem 0;
    }

    /* Risk result cards */
    .risk-card {
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin: 1.2rem 0;
        position: relative;
        overflow: hidden;
    }
    .risk-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 16px;
        pointer-events: none;
    }
    .risk-title { font-size: 1.5rem; font-weight: 900; margin-bottom: 0.3rem; }
    .risk-subtitle { font-size: 0.9rem; opacity: 0.85; }

    .card-unacceptable {
        background: linear-gradient(135deg, #3d0000 0%, #1a0000 100%);
        border: 2px solid #ff1744;
        box-shadow: 0 0 40px rgba(255,23,68,0.25), inset 0 1px 0 rgba(255,100,100,0.1);
    }
    .card-unacceptable .risk-title { color: #ff6b6b; }
    .card-unacceptable .risk-subtitle { color: #ff8a8a; }

    .card-high {
        background: linear-gradient(135deg, #2d1500 0%, #1a0d00 100%);
        border: 2px solid #ff6d00;
        box-shadow: 0 0 40px rgba(255,109,0,0.25), inset 0 1px 0 rgba(255,160,50,0.1);
    }
    .card-high .risk-title { color: #ff9d3a; }
    .card-high .risk-subtitle { color: #ffb86c; }

    .card-limited {
        background: linear-gradient(135deg, #1e1a00 0%, #141000 100%);
        border: 2px solid #ffd600;
        box-shadow: 0 0 40px rgba(255,214,0,0.2), inset 0 1px 0 rgba(255,230,80,0.08);
    }
    .card-limited .risk-title { color: #ffe566; }
    .card-limited .risk-subtitle { color: #ffec99; }

    .card-minimal {
        background: linear-gradient(135deg, #001a0d 0%, #000f07 100%);
        border: 2px solid #00e676;
        box-shadow: 0 0 40px rgba(0,230,118,0.2), inset 0 1px 0 rgba(50,255,140,0.08);
    }
    .card-minimal .risk-title { color: #69ffb3; }
    .card-minimal .risk-subtitle { color: #9dffcc; }

    /* Score meter */
    .score-bar-wrap {
        background: #21262d;
        border-radius: 8px;
        height: 10px;
        margin: 0.8rem 0;
        overflow: hidden;
    }
    .score-bar { height: 100%; border-radius: 8px; transition: width 0.6s ease; }
    .bar-unacceptable { background: linear-gradient(90deg, #ff1744, #d50000); }
    .bar-high         { background: linear-gradient(90deg, #ff6d00, #e65100); }
    .bar-limited      { background: linear-gradient(90deg, #ffd600, #ff8f00); }
    .bar-minimal      { background: linear-gradient(90deg, #00e676, #00b248); }

    /* Obligation cards */
    .ob-group {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin: 0.5rem 0;
    }
    .ob-group-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #7b61ff;
        margin-bottom: 0.6rem;
    }
    .ob-item {
        color: #c9d1d9;
        font-size: 0.9rem;
        padding: 0.3rem 0;
        border-bottom: 1px solid #21262d;
        line-height: 1.5;
    }
    .ob-item:last-child { border-bottom: none; }
    .ob-badge {
        display: inline-block;
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 0 0.4rem;
        font-size: 0.7rem;
        font-weight: 700;
        color: #8b949e;
        margin-left: 0.5rem;
        vertical-align: middle;
    }

    /* Flags / warnings */
    .flag-box {
        background: #1c2333;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        margin: 0.4rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
    }
    .flag-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 0.1rem; }
    .flag-text { font-size: 0.88rem; color: #c9d1d9; line-height: 1.5; }
    .flag-warn  { border-left: 3px solid #ff6d00; }
    .flag-error { border-left: 3px solid #ff1744; }
    .flag-info  { border-left: 3px solid #7b61ff; }
    .flag-ok    { border-left: 3px solid #00e676; }

    /* Streamlit overrides */
    .stSelectbox > div > div { background: #161b22 !important; border-color: #30363d !important; color: #e6edf3 !important; }
    .stTextInput > div > div > input { background: #161b22 !important; border-color: #30363d !important; color: #e6edf3 !important; }
    .stCheckbox label { color: #c9d1d9 !important; }
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #7b61ff, #00d4ff) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        padding: 0.7rem !important;
        transition: opacity 0.2s;
    }
    div[data-testid="stFormSubmitButton"] > button:hover { opacity: 0.88; }
    .stDownloadButton > button {
        background: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    hr { border-color: #21262d !important; }
    .stCaption { color: #484f58 !important; }
    h2, h3 { color: #e6edf3 !important; }

    /* Timeline */
    .timeline-item {
        display: flex;
        gap: 1rem;
        margin-bottom: 0.6rem;
        align-items: flex-start;
    }
    .tl-dot {
        width: 12px; height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 0.3rem;
    }
    .tl-text { font-size: 0.85rem; color: #8b949e; line-height: 1.5; }
    .tl-date { font-weight: 700; color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RULES ENGINE – Összetett AI Act logika
# ══════════════════════════════════════════════════════════════════════════════

# Art. 5 – Tiltott gyakorlatok (teljes lista)
PROHIBITED_PRACTICES = {
    "social_scoring":           "Társadalmi pontozás hatóságok által (Art. 5(1)(c))",
    "realtime_biometric":       "Valós idejű biometrikus azonosítás nyilvános térben (Art. 5(1)(d))",
    "subliminal_manipulation":  "Szublimináris technikák – tudatos döntés aláásása (Art. 5(1)(a))",
    "exploit_vulnerability":    "Sérülékeny csoportok kihasználása (Art. 5(1)(b))",
    "emotion_recognition_work": "Érzelmi állapot felismerése munkahelyen / oktatásban (Art. 5(1)(f))",
    "biometric_categorization": "Biometrikus kategorizálás érzékeny adatok alapján (Art. 5(1)(e))",
    "predictive_policing":      "Prediktív rendőrségi profilalkotás bűntett-megelőzés nélkül (Art. 5(1)(g))",
    "facial_scraping":          "Arckép-adatbázis tömeges vakarása (Art. 5(1)(h))",
}

# Annex III – Magas kockázatú szektorok részletes use-case-ekkel
ANNEX_III = {
    "critical_infrastructure":  {"label": "Kritikus infrastruktúra", "annex": "Annex III §2"},
    "education_vocational":     {"label": "Oktatás, szakképzés", "annex": "Annex III §3"},
    "employment_hr":            {"label": "Foglalkoztatás, HR", "annex": "Annex III §4"},
    "essential_services":       {"label": "Alapvető szolgáltatások (hitel, biztosítás)", "annex": "Annex III §5"},
    "law_enforcement":          {"label": "Bűnüldözés", "annex": "Annex III §6"},
    "migration_asylum":         {"label": "Migráció, menekültügy", "annex": "Annex III §7"},
    "justice_democracy":        {"label": "Igazságszolgáltatás", "annex": "Annex III §8"},
    "medical_devices":          {"label": "Orvostechnikai / egészségügy", "annex": "Annex III §1"},
    "safety_components":        {"label": "Biztonsági komponensek (jármű, gép, repülés)", "annex": "Annex III §1"},
}

# GPAI (Art. 51-55) – Általános célú AI modellek
GPAI_THRESHOLDS = {
    "systemic_risk_flops": 10**25,  # 10^25 FLOP felett szisztémikus kockázat
}

# Kötelezettség csoportok részletes cikkekkel
OBLIGATIONS = {
    "unacceptable": {
        "Jogi státusz": [
            ("🚫 Az AI rendszer az EU-ban TILOS – azonnali leállítás kötelező", "Art. 5"),
            ("⚖️ Fejlesztés, forgalmazás, üzemeltetés egyaránt jogsértés", "Art. 5"),
            ("💰 Szankció: max. 35 000 000 € vagy globális forgalom 7%-a", "Art. 99(3)"),
            ("📋 Piaci felügyeleti hatóság értesítése kötelező", "Art. 74"),
        ],
    },
    "high": {
        "Kockázatkezelés": [
            ("Kockázatkezelési rendszer kialakítása és karbantartása", "Art. 9"),
            ("Maradványkockázatok azonosítása, értékelése, mérséklése", "Art. 9(2)"),
            ("Kockázatkezelési dokumentáció naprakészen tartása", "Art. 9(6)"),
        ],
        "Adatirányítás": [
            ("Adatirányítási és adatkezelési gyakorlatok dokumentálása", "Art. 10"),
            ("Betanítási, validálási, tesztelési adatok relevanciája és minősége", "Art. 10(3)"),
            ("Adatbeli hiányosságok kezelése, adataugmentáció dokumentálása", "Art. 10(5)"),
        ],
        "Dokumentáció & Naplózás": [
            ("Technikai dokumentáció elkészítése (Annex IV séma szerint)", "Art. 11"),
            ("Automatikus naplózás (audit trail) biztosítása", "Art. 12"),
            ("Naplók minimálisan 6 hónapig megőrzendők", "Art. 12(1)"),
            ("Verziókövető nyilvántartás az életciklus alatt", "Art. 11(2)"),
        ],
        "Átláthatóság & Felügyelet": [
            ("Használói tájékoztató és instrukciók elkészítése", "Art. 13"),
            ("Emberi felügyelet lehetőségének biztosítása (override funkció)", "Art. 14"),
            ("Felügyeleti személyzet képzése kötelező", "Art. 14(4)"),
        ],
        "Pontosság & Biztonság": [
            ("Pontossági és robusztussági küszöbértékek meghatározása", "Art. 15"),
            ("Kiberbiztonság tesztelése és dokumentálása", "Art. 15(5)"),
            ("Elvárható teljesítmény-metrikák specifikálása", "Art. 15(1)"),
        ],
        "Megfelelőségi eljárás": [
            ("Conformity assessment elvégzése (harmadik fél vagy önértékelés)", "Art. 43"),
            ("CE-jelölés és EU megfelelőségi nyilatkozat kiállítása", "Art. 48"),
            ("Regisztráció az EU AI adatbázisban (EASA/Nemzeti hatóság)", "Art. 49"),
            ("Piacra hozatal előtti értesítés a felügyeleti hatóságnak", "Art. 46"),
        ],
        "Post-market & Incidensek": [
            ("Post-market monitoring rendszer bevezetése", "Art. 72"),
            ("Súlyos incidensek 15 napon belüli jelentése", "Art. 73"),
            ("Piacfelügyeleti együttműködés kötelező", "Art. 74"),
        ],
    },
    "gpai_systemic": {
        "Szisztémikus kockázat – emelt kötelezettségek": [
            ("Modellértékelés és ellenséges tesztelés (adversarial testing)", "Art. 55(1)(a)"),
            ("Szisztémikus kockázatok azonosítása és csökkentése", "Art. 55(1)(b)"),
            ("Súlyos incidensek azonnali jelentése Bizottságnak", "Art. 55(1)(c)"),
            ("Kiberbiztonság megfelelő szintjének biztosítása", "Art. 55(1)(d)"),
        ],
    },
    "gpai": {
        "Általános célú AI kötelezettségek": [
            ("Technikai dokumentáció elkészítése (Annex XI/XII)", "Art. 53(1)(a)"),
            ("Szerzői jogi transzparencia-politika közzététele", "Art. 53(1)(c)"),
            ("Összefoglalók közzététele a betanítási adatokról", "Art. 53(1)(d)"),
            ("Downstream szolgáltatóknak szükséges információk átadása", "Art. 53(1)(b)"),
        ],
    },
    "limited": {
        "Átláthatósági kötelezettségek": [
            ("Kötelező tájékoztatás az AI jellegről emberi interakciónál", "Art. 50(1)"),
            ("Deepfake / szintetikus tartalom kötelező jelölése", "Art. 50(4)"),
            ("Mesterségesen generált szöveg jelölése (kivéve szerkesztett tartalom)", "Art. 50(3)"),
            ("Érzelmi állapot felismerő rendszer esetén tájékoztatás", "Art. 50(2)"),
        ],
    },
    "minimal": {
        "Ajánlott lépések": [
            ("Nincs speciális kötelező előírás az EU AI Act alatt", "—"),
            ("Önkéntes magatartási kódex alkalmazása ajánlott (Annex IX)", "Art. 95"),
            ("Általános GDPR és fogyasztóvédelmi szabályok alkalmazandók", "2016/679 EU"),
            ("AI Literacy biztosítása a szervezeten belül", "Art. 4"),
        ],
    },
}

# Kockázati pontszám (0–100) logika
def calculate_risk_score(answers: dict) -> int:
    score = 0
    if any(answers.get(k) for k in PROHIBITED_PRACTICES): return 100
    sector = answers.get("sector", "general")
    if sector in ANNEX_III: score += 60
    if answers.get("safety_critical"): score += 20
    if answers.get("affects_fundamental_rights"): score += 15
    if answers.get("autonomous_decision"): score += 10
    if answers.get("large_scale"): score += 8
    if answers.get("interacts_with_humans"): score = max(score, 30)
    if answers.get("generates_content"): score = max(score, 25)
    if answers.get("gpai_model"): score = max(score, 35)
    return min(score, 99)

def classify_risk(answers: dict) -> tuple[str, list[str], list[str]]:
    """Return (risk_level, triggered_articles, obligations_keys)."""
    flags = []
    ob_keys = []

    # ── Tiltott alkalmazások (Art. 5) ──
    for key, label in PROHIBITED_PRACTICES.items():
        if answers.get(key):
            flags.append(label)

    if flags:
        return "unacceptable", flags, ["unacceptable"]

    # ── GPAI modell vizsgálat (Art. 51-55) ──
    is_gpai = answers.get("gpai_model", False)
    systemic_risk = answers.get("gpai_systemic_risk", False) or answers.get("gpai_large_compute", False)

    # ── Magas kockázat (Annex III) ──
    sector = answers.get("sector", "general")
    if sector in ANNEX_III:
        annex_info = ANNEX_III[sector]
        flags.append(f"{annex_info['label']} szektor – {annex_info['annex']}")
        ob_keys.append("high")

    if answers.get("safety_critical"):
        flags.append("Biztonsági szempontból kritikus komponens (Annex III §1)")
        if "high" not in ob_keys:
            ob_keys.append("high")

    if answers.get("affects_fundamental_rights") and answers.get("autonomous_decision"):
        flags.append("Alapvető jogokat érintő autonóm döntés – magas kockázat")
        if "high" not in ob_keys:
            ob_keys.append("high")

    # GPAI kötelezettségek hozzáadása
    if is_gpai:
        if systemic_risk:
            ob_keys.append("gpai_systemic")
        ob_keys.append("gpai")
        if not ob_keys or ob_keys == ["gpai_systemic", "gpai"]:
            flags.append("Általános célú AI modell (Art. 51)")

    if ob_keys and "high" in ob_keys:
        return "high", flags, list(dict.fromkeys(ob_keys))  # dedupe, preserve order

    # ── Korlátozott kockázat (Art. 50) ──
    limited_triggers = []
    if answers.get("interacts_with_humans"):
        limited_triggers.append("Közvetlen emberi interakció – chatbot/virtuális asszisztens (Art. 50(1))")
    if answers.get("generates_content"):
        limited_triggers.append("Szintetikus tartalom generálása – deepfake kockázat (Art. 50(4))")
    if answers.get("emotion_detection"):
        limited_triggers.append("Érzelmi állapot felismerés (Art. 50(2))")

    if limited_triggers or is_gpai:
        flags.extend(limited_triggers)
        ob_keys.extend(["limited"])
        if is_gpai and "gpai" not in ob_keys:
            ob_keys.append("gpai")
        return "limited", flags, list(dict.fromkeys(ob_keys))

    # ── Minimális kockázat ──
    return "minimal", ["Egyik magas/korlátozott kockázati kritérium sem teljesül"], ["minimal"]


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="hero-title">🇪🇺 EU AI Act<br>Megfelelőség-vizsgáló</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Töltsd ki a kérdőívet – az app az EU AI Act (2024/1689/EU) szabályai alapján azonnal besorolja az AI rendszeredet.</div>', unsafe_allow_html=True)

with st.form("assessment_form"):

    # ── 1. Alapadatok ──
    st.markdown('<div class="section-pill">01 · Alapadatok</div>', unsafe_allow_html=True)

    system_name = st.text_input("Az AI rendszer neve", placeholder="pl. HR-szűrő algoritmus, chatbot, képfelismerő")
    deployer_role = st.selectbox(
        "Szervezeted szerepe",
        ["provider", "deployer", "importer", "distributor"],
        format_func=lambda x: {
            "provider": "Provider (fejlesztő / piacra hozó)",
            "deployer": "Deployer (üzemeltető / felhasználó szervezet)",
            "importer": "Importer (EU-n kívülről behozó)",
            "distributor": "Distributor (forgalmazó)",
        }[x]
    )

    sector_options = {
        "general":              "Általános / Egyéb",
        "medical_devices":      "Orvostechnikai eszközök / egészségügy",
        "critical_infrastructure": "Kritikus infrastruktúra (energia, víz, közlekedés)",
        "education_vocational": "Oktatás, szakképzés",
        "employment_hr":        "Foglalkoztatás, HR, munkaerő-kezelés",
        "essential_services":   "Alapvető szolgáltatások (hitel, biztosítás, szociális ellátás)",
        "law_enforcement":      "Bűnüldözés",
        "migration_asylum":     "Migráció, menekültügy, határellenőrzés",
        "justice_democracy":    "Igazságszolgáltatás, demokratikus folyamatok",
        "safety_components":    "Biztonsági komponensek (gépek, jármű, repülés)",
    }
    sector = st.selectbox("Alkalmazási szektor", list(sector_options.keys()),
                          format_func=lambda x: sector_options[x])

    # ── 2. Tiltott gyakorlatok (Art. 5) ──
    st.markdown('<div class="section-pill">02 · Tiltott alkalmazások – Art. 5</div>', unsafe_allow_html=True)
    st.markdown('<span style="color:#8b949e;font-size:0.85rem;">Ha bármelyik igaz, a rendszer az EU-ban TILTOTT.</span>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        social_scoring      = st.checkbox("Társadalmi pontozás (social scoring)")
        subliminal          = st.checkbox("Szublimináris / manipulatív technikák")
        emotion_work        = st.checkbox("Érzelem-felismerés munkahelyen / oktatásban")
        predictive_policing = st.checkbox("Prediktív bűnözői profilalkotás")
    with col2:
        realtime_biometric  = st.checkbox("Valós idejű biometria nyilvános térben")
        exploit_vuln        = st.checkbox("Sérülékeny csoportok kihasználása")
        biometric_cat       = st.checkbox("Biometrikus kategorizálás (pl. politikai nézet)")
        facial_scraping     = st.checkbox("Arckép-adatbázis tömeges vakarása (scraping)")

    # ── 3. Magas kockázat finomítás ──
    st.markdown('<div class="section-pill">03 · Magas kockázat – további szempontok</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        safety_critical          = st.checkbox("Biztonsági szempontból kritikus termék/komponens")
        autonomous_decision      = st.checkbox("Autonóm döntés emberi felülvizsgálat nélkül")
    with col4:
        affects_fundamental_rights = st.checkbox("Alapvető jogokat (munkahely, hitel, szabadság) érintő döntés")
        large_scale              = st.checkbox("Nagy léptékű alkalmazás (1M+ érintett)")

    # ── 4. GPAI (Art. 51-55) ──
    st.markdown('<div class="section-pill">04 · Általános célú AI modell – Art. 51-55</div>', unsafe_allow_html=True)

    gpai_model         = st.checkbox("Ez egy általános célú AI modell (GPAI / foundation model / LLM)?")
    gpai_large_compute = st.checkbox("A betanítás meghaladta a 10²⁵ FLOP-ot (szisztémikus kockázat küszöb)?")
    gpai_systemic      = st.checkbox("Az EU Bizottság szisztémikus kockázatúnak minősítette?")

    # ── 5. Korlátozott kockázat ──
    st.markdown('<div class="section-pill">05 · Korlátozott kockázat – Art. 50</div>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        interacts_humans = st.checkbox("Közvetlen kommunikáció emberekkel (chatbot, asszisztens)")
        emotion_detect   = st.checkbox("Érzelmi állapot felismerés (nem munkahely/oktatás)")
    with col6:
        generates_content = st.checkbox("Szintetikus tartalom generálása (szöveg, kép, hang, videó)")

    submitted = st.form_submit_button("🔍 Kockázatbesorolás elvégzése", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# EREDMÉNY
# ══════════════════════════════════════════════════════════════════════════════

if submitted:
    answers = {
        "system_name": system_name or "AI rendszer",
        "sector": sector,
        "sector_label": sector_options[sector],
        "deployer_role": deployer_role,
        "social_scoring": social_scoring,
        "realtime_biometric": realtime_biometric,
        "subliminal_manipulation": subliminal,
        "exploit_vulnerability": exploit_vuln,
        "emotion_recognition_work": emotion_work,
        "biometric_categorization": biometric_cat,
        "predictive_policing": predictive_policing,
        "facial_scraping": facial_scraping,
        "safety_critical": safety_critical,
        "autonomous_decision": autonomous_decision,
        "affects_fundamental_rights": affects_fundamental_rights,
        "large_scale": large_scale,
        "gpai_model": gpai_model,
        "gpai_large_compute": gpai_large_compute,
        "gpai_systemic_risk": gpai_systemic,
        "interacts_with_humans": interacts_humans,
        "generates_content": generates_content,
        "emotion_detection": emotion_detect,
    }

    risk, flags, ob_keys = classify_risk(answers)
    score = calculate_risk_score(answers)

    RISK_META = {
        "unacceptable": {
            "label": "🚫 TILTOTT ALKALMAZÁS",
            "sub": "EU AI Act 5. cikk – azonnali leállítás kötelező",
            "card": "card-unacceptable",
            "bar": "bar-unacceptable",
        },
        "high": {
            "label": "🔴 MAGAS KOCKÁZATÚ",
            "sub": "Kötelező megfelelőségi értékelés és regisztráció az EU AI adatbázisban",
            "card": "card-high",
            "bar": "bar-high",
        },
        "limited": {
            "label": "🟡 KORLÁTOZOTT KOCKÁZATÚ",
            "sub": "Átláthatósági kötelezettségek – Art. 50",
            "card": "card-limited",
            "bar": "bar-limited",
        },
        "minimal": {
            "label": "🟢 MINIMÁLIS KOCKÁZATÚ",
            "sub": "Nincs speciális EU AI Act kötelezettség – önkéntes kódex ajánlott",
            "card": "card-minimal",
            "bar": "bar-minimal",
        },
    }
    meta = RISK_META[risk]

    st.divider()
    st.markdown("## Besorolás eredménye")

    # Risk card
    st.markdown(f"""
    <div class="risk-card {meta['card']}">
        <div class="risk-title">{meta['label']}</div>
        <div class="risk-subtitle">{meta['sub']}</div>
        <div style="margin-top:1rem;">
            <div style="font-size:0.75rem;color:#8b949e;margin-bottom:4px;">Kockázati pontszám: {score}/100</div>
            <div class="score-bar-wrap">
                <div class="score-bar {meta['bar']}" style="width:{score}%"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Triggered flags
    st.markdown("### Kiváltó tényezők")
    flag_icon_class = {
        "unacceptable": ("🚨", "flag-error"),
        "high": ("⚠️", "flag-warn"),
        "limited": ("ℹ️", "flag-info"),
        "minimal": ("✅", "flag-ok"),
    }
    icon, flag_cls = flag_icon_class[risk]
    for f in flags:
        st.markdown(f'<div class="flag-box {flag_cls}"><div class="flag-icon">{icon}</div><div class="flag-text">{f}</div></div>', unsafe_allow_html=True)

    # Role-specific note
    role_notes = {
        "provider":     "Provider-ként te felelős a megfelelőségi értékelésért, CE-jelölésért és dokumentációért.",
        "deployer":     "Deployer-ként a high-risk rendszereknél emberi felügyeletet és adatkezelési nyilvántartást kell biztosítanod.",
        "importer":     "Importer-ként ellenőrizned kell, hogy a provider teljesítette-e az EU AI Act kötelezettségeit.",
        "distributor":  "Distributor-ként meg kell győződnöd a conformity assessment megtörténtéről és a CE-jelölésről.",
    }
    role_label = {"provider": "Provider", "deployer": "Deployer", "importer": "Importer", "distributor": "Distributor"}
    st.markdown(f"""
    <div class="flag-box flag-info" style="margin-top:0.8rem;">
        <div class="flag-icon">💼</div>
        <div class="flag-text"><strong>{role_label[deployer_role]} megjegyzés:</strong> {role_notes[deployer_role]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Obligations
    st.markdown("### Kötelezettségek és teendők")
    for ob_key in ob_keys:
        if ob_key not in OBLIGATIONS:
            continue
        groups = OBLIGATIONS[ob_key]
        for group_name, items in groups.items():
            items_html = ""
            for text, article in items:
                badge = f'<span class="ob-badge">{article}</span>' if article and article != "—" else ""
                items_html += f'<div class="ob-item">{text}{badge}</div>'
            st.markdown(f"""
            <div class="ob-group">
                <div class="ob-group-title">{group_name}</div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)

    # Implementation timeline
    st.markdown("### ⏱️ Alkalmazási menetrend")
    timeline = [
        ("#ff6d00", "2024. augusztus 1.", "EU AI Act hatályba lépett"),
        ("#ffd600", "2025. február 2.", "Art. 5 (tiltott gyakorlatok) hatályos"),
        ("#7b61ff", "2025. augusztus 2.", "GPAI modellek (Art. 51-55) hatályos"),
        ("#00d4ff", "2026. augusztus 2.", "Magas kockázatú rendszerek – teljes körű alkalmazás"),
        ("#00e676", "2027. augusztus 2.", "Egyes Annex I berendezések – meghosszabbított határidő"),
    ]
    for color, date, desc in timeline:
        st.markdown(f"""
        <div class="timeline-item">
            <div class="tl-dot" style="background:{color};box-shadow:0 0 8px {color}60;"></div>
            <div class="tl-text"><span class="tl-date">{date}</span> – {desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # JSON download
    st.divider()
    report = {
        "generated_at": datetime.now().isoformat(),
        "system_name": answers["system_name"],
        "deployer_role": deployer_role,
        "sector": sector_options[sector],
        "risk_level": risk,
        "risk_score": score,
        "triggered_flags": flags,
        "obligations_keys": ob_keys,
        "obligations_detail": {
            k: {g: [{"text": t, "article": a} for t, a in items] for g, items in OBLIGATIONS[k].items()}
            for k in ob_keys if k in OBLIGATIONS
        },
    }
    st.download_button(
        label="📥 Megfelelőségi riport letöltése (.json)",
        data=json.dumps(report, ensure_ascii=False, indent=2),
        file_name=f"eu_ai_act_{(system_name or 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption("⚠️ Tájékoztató jellegű – nem minősül jogi tanácsadásnak. EU AI Act (2024/1689/EU) alapján. v2.0")
