import streamlit as st
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Megfelelőség-vizsgáló",
    page_icon="🇪🇺",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background: #f8f9fa; }
    .stApp { max-width: 800px; margin: auto; }
    .risk-box {
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .risk-unacceptable { background: #ffe0e0; border-left: 6px solid #d32f2f; color: #b71c1c; }
    .risk-high         { background: #fff3e0; border-left: 6px solid #f57c00; color: #e65100; }
    .risk-limited      { background: #fffde7; border-left: 6px solid #fbc02d; color: #f57f17; }
    .risk-minimal      { background: #e8f5e9; border-left: 6px solid #388e3c; color: #1b5e20; }
    .obligation-item {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
    }
    .linkedin-box {
        background: #f3f6fb;
        border: 1px solid #0a66c2;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        white-space: pre-wrap;
        font-size: 0.93rem;
        line-height: 1.6;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a237e;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Rules engine ──────────────────────────────────────────────────────────────
UNACCEPTABLE_TRIGGERS = [
    "social_scoring",
    "realtime_biometric_public",
    "subliminal_manipulation",
    "exploit_vulnerability",
]

HIGH_RISK_SECTORS = [
    "critical_infrastructure",
    "education_vocational",
    "employment_hr",
    "essential_services",
    "law_enforcement",
    "migration_asylum",
    "justice_democracy",
    "medical_devices",
    "safety_components",
]

OBLIGATIONS_BY_RISK = {
    "unacceptable": [
        "🚫 Az AI rendszer TILOS az EU-ban – az EU AI Act 5. cikke alapján.",
        "🚫 Az ilyen rendszerek fejlesztése, forgalmazása vagy üzemeltetése jogsértés.",
        "📋 Azonnali jogi tanácsadás javasolt.",
    ],
    "high": [
        "📋 Kötelező kockázatkezelési rendszer (Art. 9)",
        "📊 Magas minőségű adatirányítás és dokumentáció (Art. 10)",
        "📝 Technikai dokumentáció elkészítése (Art. 11)",
        "📒 Automatikus naplózás / audittrail (Art. 12)",
        "👁️ Átláthatóság és felhasználói tájékoztatás (Art. 13)",
        "🧑‍💼 Emberi felügyelet biztosítása (Art. 14)",
        "🎯 Pontosság, robusztusság, kiberbiztonság (Art. 15)",
        "✅ Megfelelőségi értékelés (conformity assessment) elvégzése",
        "🏷️ CE-jelölés és EU megfelelőségi nyilatkozat",
        "📬 Regisztráció az EU AI adatbázisban",
    ],
    "limited": [
        "💬 Chatbot / AI interakció esetén kötelező tájékoztatás az AI jellegről (Art. 50)",
        "🖼️ Deepfake tartalom jelölése kötelező (Art. 50)",
        "📢 Átláthatósági kötelezettségek betartása",
    ],
    "minimal": [
        "✅ Nincs speciális kötelező előírás az EU AI Act alatt",
        "💡 Önkéntes magatartási kódexek követése ajánlott",
        "🔍 Általános GDPR és fogyasztóvédelmi szabályok alkalmazandók",
    ],
}

def classify_risk(answers: dict) -> tuple[str, str]:
    """Return (risk_level, explanation)."""
    
    # Unacceptable check
    for t in UNACCEPTABLE_TRIGGERS:
        if answers.get(t):
            return "unacceptable", "A rendszer tiltott AI-gyakorlatnak minősül (EU AI Act 5. cikk)."
    
    # High risk check
    if answers.get("sector") in HIGH_RISK_SECTORS:
        return "high", f"A(z) **{answers.get('sector_label', '')}** szektor magas kockázatú (III. melléklet)."
    
    if answers.get("safety_critical"):
        return "high", "A rendszer biztonsági szempontból kritikus termék vagy komponense."
    
    # Limited risk
    if answers.get("interacts_with_humans") or answers.get("generates_content"):
        return "limited", "Az AI közvetlen emberi interakciót folytat vagy szintetikus tartalmat generál."
    
    # Minimal
    return "minimal", "Az AI rendszer minimális kockázatú kategóriába sorolható."

def generate_linkedin_post(answers: dict, risk: str, explanation: str) -> str:
    risk_labels = {
        "unacceptable": "🚫 TILTOTT",
        "high": "🔴 MAGAS KOCKÁZATÚ",
        "limited": "🟡 KORLÁTOZOTT KOCKÁZATÚ",
        "minimal": "🟢 MINIMÁLIS KOCKÁZATÚ",
    }
    now = datetime.now().strftime("%Y. %B %d.")
    
    post = f"""🇪🇺 EU AI Act megfelelőségi eredmény – {now}

Elvégeztem az EU AI Act szerinti kockázatbesorolást.

📌 Rendszer neve: {answers.get('system_name', 'AI rendszer')}
📂 Szektor: {answers.get('sector_label', 'Általános')}

🏷️ Besorolás: {risk_labels.get(risk, risk.upper())}

{explanation}

📋 Főbb kötelezettségek:
"""
    for ob in OBLIGATIONS_BY_RISK.get(risk, [])[:4]:
        post += f"• {ob}\n"
    
    post += f"""
💡 Az EU AI Act 2026-tól teljes körűen alkalmazandó. A megfelelőség nem opció – jogszabályi kötelezettség.

👉 Ingyenes megfelelőség-vizsgáló tool: github.com/eu-ai-act-checker

#EUAIAct #AICompliance #AIGovernance #MesterségesIntelligencia #Megfelelőség #AIRegulation #TechLaw"""
    return post

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("# 🇪🇺 EU AI Act Megfelelőség-vizsgáló")
st.markdown("Töltsd ki az alábbi kérdéseket, és azonnal megkapod az AI rendszered kockázati besorolását és kötelezettségeit.")
st.divider()

with st.form("assessment_form"):
    st.markdown('<div class="section-header">1. Az AI rendszer alapadatai</div>', unsafe_allow_html=True)
    
    system_name = st.text_input("Az AI rendszer neve / megnevezése", placeholder="pl. HR-szűrő algoritmus")
    
    sector_options = {
        "general": "Általános / Egyéb",
        "critical_infrastructure": "Kritikus infrastruktúra (energia, víz, közlekedés)",
        "education_vocational": "Oktatás, szakképzés",
        "employment_hr": "Foglalkoztatás, HR, munkaerő-kezelés",
        "essential_services": "Alapvető szolgáltatások (hitel, biztosítás)",
        "law_enforcement": "Bűnüldözés",
        "migration_asylum": "Migráció, menekültügy, határellenőrzés",
        "justice_democracy": "Igazságszolgáltatás, demokratikus folyamatok",
        "medical_devices": "Orvostechnikai eszközök / egészségügy",
        "safety_components": "Biztonsági komponensek (gépek, jármű, repülés)",
    }
    
    sector = st.selectbox(
        "Melyik szektorban alkalmazzák?",
        options=list(sector_options.keys()),
        format_func=lambda x: sector_options[x],
    )
    
    st.markdown('<div class="section-header">2. Tiltott alkalmazások ellenőrzése</div>', unsafe_allow_html=True)
    
    social_scoring = st.checkbox("Társadalmi pontozás (social scoring) közhatóságok által")
    realtime_biometric = st.checkbox("Valós idejű biometrikus azonosítás nyilvános térben (kivéve törvényi kivételek)")
    subliminal = st.checkbox("Tudatküszöb alatti manipuláció alkalmazása")
    exploit_vuln = st.checkbox("Sérülékeny csoportok (gyermekek, fogyatékossággal élők) kihasználása")
    
    st.markdown('<div class="section-header">3. Magas kockázat további ellenőrzése</div>', unsafe_allow_html=True)
    
    safety_critical = st.checkbox("Biztonsági szempontból kritikus termék vagy annak komponense")
    
    st.markdown('<div class="section-header">4. Korlátozott kockázat ellenőrzése</div>', unsafe_allow_html=True)
    
    interacts_humans = st.checkbox("Az AI közvetlenül kommunikál emberekkel (pl. chatbot, virtuális asszisztens)")
    generates_content = st.checkbox("Az AI szintetikus tartalmat generál (szöveg, kép, hang, videó – deepfake)")
    
    submitted = st.form_submit_button("🔍 Kockázatbesorolás elvégzése", use_container_width=True)

if submitted:
    answers = {
        "system_name": system_name or "AI rendszer",
        "sector": sector,
        "sector_label": sector_options[sector],
        "social_scoring": social_scoring,
        "realtime_biometric_public": realtime_biometric,
        "subliminal_manipulation": subliminal,
        "exploit_vulnerability": exploit_vuln,
        "safety_critical": safety_critical,
        "interacts_with_humans": interacts_humans,
        "generates_content": generates_content,
    }
    
    risk, explanation = classify_risk(answers)
    
    risk_display = {
        "unacceptable": ("🚫 TILTOTT ALKALMAZÁS", "risk-unacceptable"),
        "high": ("🔴 MAGAS KOCKÁZATÚ", "risk-high"),
        "limited": ("🟡 KORLÁTOZOTT KOCKÁZATÚ", "risk-limited"),
        "minimal": ("🟢 MINIMÁLIS KOCKÁZATÚ", "risk-minimal"),
    }
    label, css_class = risk_display[risk]
    
    st.divider()
    st.markdown("## 📊 Eredmény")
    
    st.markdown(f'<div class="risk-box {css_class}">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"**Indoklás:** {explanation}")
    
    st.markdown("### 📋 Kötelezettségek és teendők")
    for ob in OBLIGATIONS_BY_RISK[risk]:
        st.markdown(f'<div class="obligation-item">{ob}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 💼 LinkedIn poszt generálása")
    st.markdown("Másold ki és oszd meg az eredményt LinkedIn-en!")
    
    linkedin_text = generate_linkedin_post(answers, risk, explanation)
    st.markdown(f'<div class="linkedin-box">{linkedin_text}</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Poszt letöltése (.txt)",
        data=linkedin_text,
        file_name=f"eu_ai_act_{system_name or 'eredmeny'}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    
    # JSON report
    report = {
        "generated_at": datetime.now().isoformat(),
        "system_name": answers["system_name"],
        "sector": answers["sector_label"],
        "risk_level": risk,
        "explanation": explanation,
        "obligations": OBLIGATIONS_BY_RISK[risk],
    }
    st.download_button(
        label="📥 Megfelelőségi riport letöltése (.json)",
        data=json.dumps(report, ensure_ascii=False, indent=2),
        file_name=f"eu_ai_act_report_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption("⚠️ Ez az eszköz tájékoztató jellegű, nem minősül jogi tanácsadásnak. Az EU AI Act (2024/1689/EU) alapján készült. | Verzió: 1.0")
