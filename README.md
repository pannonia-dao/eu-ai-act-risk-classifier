# EU AI Act Compliance Checker

> **Production-ready Streamlit app** for instant AI system risk classification under Regulation (EU) 2024/1689.

[![Regulation](https://img.shields.io/badge/EU%20AI%20Act-2024%2F1689-003399?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJMNiAxMmgxMnoiIGZpbGw9IiNGRkQzMDAiLz48L3N2Zz4=)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

---

## Features

- **All 4 risk levels** — Prohibited · High · Limited · Minimal
- **All 8 Art. 5 prohibited practices** individually checked
- **Full Annex III** sector coverage (9 high-risk sectors)
- **GPAI obligations** (Art. 51–55) including systemic risk tier
- **Role-aware** — Provider / Deployer / Importer / Distributor
- **Clickable article citations** linking to official EUR-Lex text
- **Dual export** — JSON compliance report + Markdown checklist
- **Enforcement timeline** with live date awareness
- Clean, professional light design — ready for client demos

---

## Quick Start

### Local

```bash
git clone https://github.com/YOUR_USERNAME/eu-ai-act-checker.git
cd eu-ai-act-checker
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Community Cloud (free)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your fork · branch `main` · file `app.py`
4. Click **Deploy** — live in ~60 seconds

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"]
```

```bash
docker build -t eu-ai-act .
docker run -p 8501:8501 eu-ai-act
```

---

## Classification Logic

```
INPUT: 20 structured questions across 5 sections

Step 1 — Art. 5 screen (8 prohibited practices)
        → ANY match → PROHIBITED (immediate stop)

Step 2 — Annex III high-risk screen
        → Sector match OR safety-critical component
           OR (autonomous decision AND fundamental rights) → HIGH

Step 3 — GPAI check (Art. 51-55)
        → Is a foundation/general-purpose model?
           → ≥10²⁵ FLOPs or Commission designation → SYSTEMIC RISK tier
           → Otherwise → standard GPAI obligations

Step 4 — Art. 50 limited risk
        → Human interaction, synthetic content, emotion detection → LIMITED

Step 5 — Default → MINIMAL (voluntary codes recommended)

OUTPUT: Risk level + score (0-100) + article-linked obligation checklist
```

---

## Enforcement Dates

| Date | Milestone |
|------|-----------|
| 1 Aug 2024 | AI Act entered into force |
| 2 Feb 2025 | Art. 5 — prohibited practices enforceable |
| 2 Aug 2025 | GPAI model obligations (Art. 51-55) |
| **2 Aug 2026** | **High-risk systems — full application** |
| 2 Aug 2027 | Annex I product systems — extended deadline |

---

## Outputs

| Format | Contents |
|--------|----------|
| **JSON** | Machine-readable report with all triggered criteria, obligations per article, source URLs |
| **Markdown** | Interactive checklist with article links, ready for Notion/Confluence/GitHub |

---

## Legal Notice

This tool is for **informational purposes only** and does not constitute legal advice.  
Always consult a qualified legal professional for compliance decisions.  
Built on the official text of [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689).

---

## License

MIT © 2025 — free to use, modify, and distribute.
