<div align="center">

# 🛢️ Global Oil Supply Chain & Infrastructure Dashboard

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://app-oil-supply-chain.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Platform-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://snowflake.com)
[![dbt](https://img.shields.io/badge/dbt-Data%20Transformation-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://getdbt.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**End-to-end data engineering pipeline on Snowflake — EIA Open Data API → raw ingestion → dbt staging & marts → interactive Streamlit dashboard tracking global crude oil supply, storage, production, and trade flows.**

</div>

---

## 📊 Live Dashboard

> Click the badge above to open the deployed app. No login required.

The dashboard covers five analytical domains across four tabs:

| Tab | What It Shows |
|---|---|
| **National Supply Balance** | U.S. crude supply & disposition balance — field production, refinery input, ending stocks (1920–present) |
| **Global Production** | Top-10 producer bar chart, country trend comparison, production intensity heatmap (last 10 years) |
| **Storage** | Cushing, OK weekly crude stocks — the WTI futures delivery point and bellwether for U.S. inventory pressure |
| **Trade Flows** | U.S. crude imports by origin country & grade; interregional PADD-to-PADD pipeline movement matrix |

---

## 🏗️ Architecture

```
EIA Open Data API
       │
       ▼
 Python Ingestion
 (backfill_eia.py)
 9 series × full history
       │
       ▼
 Snowflake Internal Stage
 (EIA_STAGE — raw JSON)
       │
       ▼
 RAW Schema
 9 VARIANT tables
 (~98,000 rows total)
       │
       ▼
 dbt Staging Layer
 (STAGING schema)
 JSON flattening → typed columns
       │
       ▼
 dbt Marts Layer
 (MARTS schema)
 dim_date + 9 fact tables
       │
       ├─► Streamlit-in-Snowflake (live, trial)
       └─► Streamlit Community Cloud (permanent, CSV snapshot)
```

---

## 📁 Project Structure

```
oil-supply-chain-snowflake/
│
├── streamlit_app.py          # Dashboard — reads from data/exports/ CSVs
├── requirements.txt          # streamlit, pandas
│
├── data/
│   └── exports/              # Mart snapshots (committed — powers the live app)
│       ├── fct_supply_balance.csv
│       ├── fct_global_production.csv
│       ├── fct_storage_cushing.csv
│       ├── fct_crude_imports_by_grade.csv
│       └── fct_interregional_movements.csv
│
├── oil_supply_dbt/           # dbt project
│   ├── models/
│   │   ├── staging/          # 9 staging models — flatten raw VARIANT JSON
│   │   └── marts/            # dim_date + 9 fact tables
│   ├── dbt_project.yml
│   └── profiles.yml          # (gitignored — contains credentials)
│
├── backfill_eia.py           # EIA API ingestion script
├── load_to_snowflake.py      # Stage upload & COPY INTO loader
├── oil_control.json          # Ingestion catalog — 9 EIA series definitions
├── sanity_check.py           # Row-count verification post-load
│
└── .env                      # (gitignored — EIA API key & Snowflake creds)
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Source | U.S. EIA Open Data API (free, public) |
| Cloud Platform | Snowflake (Standard, AWS ap-southeast-2) |
| Warehouse | `OIL_SUPPLY_WH` (XSMALL, auto-suspend 60s) |
| Transformation | dbt Core 1.11 + dbt-snowflake 1.11 |
| Dashboard (cloud) | Streamlit-in-Snowflake (container runtime) |
| Dashboard (public) | Streamlit Community Cloud |
| Language | Python 3.11 |

---

## 📦 Data Coverage

| Mart Table | Rows | Description |
|---|---|---|
| `fct_supply_balance` | 1,275 | Monthly U.S. crude supply & disposition (1920–2026) |
| `fct_global_production` | 624 | Annual crude production by country (TBPD) |
| `fct_global_consumption` | 556 | Annual crude consumption by country (TBPD) |
| `fct_storage_weekly` | 25,954 | Weekly PADD + national crude stocks |
| `fct_storage_cushing` | 3,525 | Monthly Cushing, OK stocks |
| `fct_refinery_utilization` | 2,970 | Weekly U.S. refinery utilization & capacity |
| `fct_interregional_movements` | 6,149 | PADD-to-PADD pipeline/tanker/barge/rail flows |
| `fct_us_imports_by_country` | 36,964 | Monthly U.S. crude imports by origin country |
| `fct_crude_imports_by_grade` | 9,159 | Monthly U.S. crude imports by origin & grade |

---

## 🚀 Run Locally

```bash
git clone https://github.com/fahadamjad009/snowflake-oil-supply-chain.git
cd snowflake-oil-supply-chain
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app reads from `data/exports/` CSVs — no Snowflake account or API keys required.

---

## 🔑 Data Source

All data is sourced from the [U.S. Energy Information Administration (EIA) Open Data API](https://www.eia.gov/opendata/) — a free public API requiring registration only for an API key. No commercial license needed.

---

## 👤 Author

**Fahad Amjad**
[GitHub](https://github.com/fahadamjad009) · [Portfolio](https://fahadamjad009.github.io)

---

<div align="center">
<i>Part of a data engineering portfolio demonstrating end-to-end pipelines across Azure, Snowflake, dbt, Python, and BI tooling.</i>
</div>
