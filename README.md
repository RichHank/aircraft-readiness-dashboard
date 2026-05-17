# Aircraft Readiness Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![pandas](https://img.shields.io/badge/pandas-ETL-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **194,844 FAA Service Difficulty Reports. Three years of data. One clear finding: fuselage structural maintenance is breaking the fleet — and nobody is fixing it.**

---

## The Problem

U.S. civil aviation generates tens of thousands of maintenance discrepancy reports every year. Most of them are noise. Some of them are signals that the same aircraft, the same system, and the same failure mode keep coming back — and no one is connecting the dots at scale.

This project does exactly that.

---

## Key Findings

### Finding 1 — Fuselage (ATA 53) Dominates the Maintenance Burden

| ATA Chapter | System | Total Events | Repeat Rate |
|-------------|--------|-------------|-------------|
| **53** | **Fuselage** | **75,690** | **87.1%** |
| 57 | Wings | 16,000 | 70.4% |
| 52 | Doors | 17,492 | 40.0% |
| 55 | Stabilizers | 6,057 | 58.6% |

Nearly **9 out of every 10** fuselage maintenance events are repeat discrepancies — the same aircraft, the same airframe, within 30 days.

---

### Finding 2 — Structural Systems Repeat at 5× the Rate of Mechanical Systems

| System Group | Total Events | Repeat Rate |
|-------------|-------------|-------------|
| **Airframe** | **120,637** | **74.2%** |
| Electrical | 26,055 | 34.8% |
| Propulsion | 8,771 | 21.2% |
| Landing Gear | 4,165 | 16.8% |
| **Hydraulics** | **1,580** | **13.5%** |

Hydraulics and landing gear involve discrete component swaps — fix it, done. Structural corrosion and fatigue are progressive. You treat them incrementally. They come back.

---

### Finding 3 — Fleet Availability Is Flat. The Burden Isn't Improving.

| Year | Avg Availability Rate | Total Events |
|------|-----------------------|-------------|
| 2023 | 94.1% | 62,336 |
| 2024 | 94.0% | 65,695 |
| 2025 | 94.4% | 66,813 |

Event volume is growing year over year. Availability isn't moving. The fleet is absorbing the load — but the structural maintenance burden is not being reduced.

---

### Finding 4 — Canadair Regional Jets Cluster at the Bottom

Of the 10 worst-performing aircraft by availability proxy, 5 are Canadair CL600-series regional jets — a pattern consistent enough to warrant targeted investigation with actual labor-hour data.

---

### Finding 5 — March Is Consistently the Highest-Volume Month

March ranks #1 in event volume for both 2023 and 2025. A seasonal inspection cycle — annual or semi-annual checks timed to late winter — is the likely driver, surfacing structural discrepancies that were deferred through the fall.

---

## Why This Analysis Is Different

Most maintenance analytics stops at event counts. This project goes further:

- **Repeat discrepancy detection** — flags when the same aircraft reports the same ATA chapter within 30 days, isolating chronic failure patterns from one-time events
- **Availability proxy modeling** — estimates operational availability from SDR data alone, without access to actual utilization records
- **System-group aggregation** — rolls ATA chapters into operational categories (Airframe, Propulsion, Hydraulics, etc.) to surface strategic patterns invisible at the chapter level

---

## Architecture

```
FAA SDR Raw Data (2023–2025)
        │
        ▼
┌───────────────┐
│  ETL Pipeline │  ← Python / pandas
│  (5 scripts)  │     clean, deduplicate, anonymize, flag repeats
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  SQLite DB    │  ← Validated KPIs, analytical views
│  readiness.db │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Power BI     │  ← 3-page interactive dashboard
│  Dashboard    │     slicers: system group, aircraft type
└───────────────┘
```

---

## Project Structure

```
aircraft-readiness-dashboard/
├── data/
│   ├── raw/                        # Original FAA SDR CSVs (not tracked)
│   └── processed/
│       ├── sdr_clean.csv           # Cleaned, deduplicated event data
│       ├── powerbi_*.csv           # Star-schema exports for Power BI
│       └── readiness.db            # SQLite database
├── etl/
│   ├── stage_sdr.py                # Ingest raw FAA files
│   ├── clean_sdr.py                # Clean + flag repeats
│   ├── build_dims.py               # Build dimension tables
│   ├── build_facts.py              # Build fact tables
│   └── export_powerbi.py           # Export CSVs for Power BI
├── sql/
│   ├── views.sql                   # Analytical views
│   └── load_db.py                  # Load all tables + run KPI validation
├── powerbi/
│   ├── aircraft_readiness.pbix     # Power BI dashboard file
│   └── dax_measures.txt            # DAX measure definitions
├── docs/
│   ├── findings.md                 # Full written findings (verified against DB)
│   └── ASSUMPTIONS_AND_LIMITATIONS.md
└── data_profiling.ipynb            # EDA and data quality profiling
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | ETL pipeline, data cleaning, repeat-flag logic |
| pandas | Data transformation and aggregation |
| SQLite | Analytical database and KPI validation |
| Power BI Desktop | Interactive 3-page dashboard |
| Jupyter | Exploratory data analysis and profiling |

---

## Running the Pipeline

```bash
pip install -r requirements.txt

python etl/stage_sdr.py
python etl/clean_sdr.py
python etl/build_dims.py
python etl/build_facts.py
python etl/export_powerbi.py
python sql/load_db.py
```

---

## Data Source

**FAA Service Difficulty Reporting System (SDRS)**
- Public dataset maintained by the Federal Aviation Administration
- Years: 2023, 2024, 2025
- Records analyzed: 194,844
- Unique aircraft: 12,226
- All tail numbers anonymized via SHA-256 hash → synthetic aircraft IDs

---

## Author

**Richard Hankins**
Aviation Maintenance Team Lead — U.S. Army | BBA Candidate (4.0 GPA) | Active Secret Clearance

Six years supervising Black Hawk helicopter maintenance — tracking readiness metrics, managing $144M–$180M in aircraft assets, and translating raw maintenance logs into actionable briefings for leadership. This project applies that operational context to FAA public data at scale.

[LinkedIn](https://linkedin.com/in/richardhankinsjr) · [GitHub](https://github.com/RichHank)
