# Vichar Media — Social Media Intelligence & Data Analytics Platform

**Project type:** End-to-end Data Science / Business Intelligence portfolio project  
**Platforms:** Instagram and YouTube  
**Dataset period:** Instagram audit data through 2026-11-20 (individual source rows vary); YouTube lifetime audit 2026-06-09 to 2026-11-21  
**Status:** Runnable prototype built from supplied audit summaries; not connected to live platform APIs.

## What this project does

This project turns the supplied Instagram and YouTube analytics audits into a repeatable analytics workflow:

1. **Data ingestion and ETL** — normalised CSV staging tables and SQLite database creation.
2. **Data quality validation** — checks record counts and explicitly lists source inconsistencies.
3. **Business intelligence dashboard** — interactive Streamlit dashboard for platform overview, content, time series, traffic, formats and Stories.
4. **Exploratory data analysis** — distributions, outlier impact, metric relationships and correlations.
5. **Time-series experiment** — a short-horizon trailing-mean baseline on the Instagram account daily series.
6. **NLP experiment** — TF-IDF/K-Means clustering over supplied content titles and topic labels.
7. **Machine-learning feasibility experiment** — chronological baseline model using only date and content format, with strict warnings about sample size and feature limitations.
8. **Decision-support flags** — descriptive rules identify content for further review.

## Important data integrity statement

This is a real-data project using only the values present in the supplied audits. Missing values are not filled with invented zeros. Several source totals do not reconcile, and those discrepancies are preserved in `data/processed/data_quality_issues.csv`.

- Instagram: 43 feed posts (35 Reels + 8 carousels), 32 archived Stories, and 27 supplied daily account rows. The Instagram audit labels the daily window as 28 days but only includes dates through 2026-11-19.
- YouTube: lifetime channel, format and traffic-source aggregates plus an 11-item top-content shortlist. This is **not** a complete upload inventory.
- Instagram daily account-level views are described by the source as aggregated Instagram + Facebook cross-posted views; they are not Instagram-only post-level views.
- Instagram content labels include descriptive paraphrases from the audit, not necessarily original captions.
- YouTube top content has incomplete fields in one malformed row (Manipur Short net subscribers not provided).
- No live API connection, credentials, or unauthorised account access is used.

## Quick start (Windows PowerShell)

```powershell
cd Vichar_Media_Social_Intelligence_Platform
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints (normally `http://localhost:8501`).

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Build the SQLite database

```bash
python scripts/build_database.py
```

Creates `database/vichar_media_intelligence.db` with these tables:

`content`, `stories`, `daily_metrics`, `traffic_sources`, `format_summary`, `platform_summary`, `audience_activity`, `data_quality_issues`.

## Run the analysis modules

```bash
python scripts/run_analysis.py
```

## Run tests

```bash
pytest -q
```

## Project structure

```text
Vichar_Media_Social_Intelligence_Platform/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/                 # Audit source snapshots supplied for this project
│   └── processed/           # Normalised CSV datasets
├── database/                # SQLite database created by ETL script
├── notebooks/               # Walkthrough notebook
├── reports/                 # Project report, data dictionary, quality report
├── scripts/                 # Database and analysis runners
├── src/vichar_intel/         # Reusable ETL and analytics modules
└── tests/                    # Automated checks
```

## Methodology and module descriptions

See `reports/project_report.md` for the project problem statement, architecture, methodology, results, limitations and suggested next steps. See `reports/data_dictionary.md` for field definitions and provenance.

## Academic / viva integrity

This package is a developed project prototype and a learning aid. The person presenting it should run the project, inspect the datasets, understand the code, reproduce the outputs and accurately describe their own contribution. It should not be represented as evidence of employment or work that was not actually performed.

## Next data required for a stronger version

- Instagram official CSV exports for daily account insights and full per-content insights.
- YouTube Studio Advanced Mode exports for all videos, daily metrics, retention and traffic-source dimensions.
- Original captions/descriptions and consistent content-topic labels.
- Additional pre-publication features (duration, format details, publishing metadata) to improve modelling.

## Disclaimer

This is an independent analytics prototype, not endorsed by Meta, Instagram, Google or YouTube. Platform metric definitions and availability can change; use the source audit's definitions and dates when interpreting results.
