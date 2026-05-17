"""
Export final Power BI-ready CSVs from the processed fact and dimension tables.

Input:  data/processed/fact_readiness_proxy.csv
        data/processed/dim_aircraft.csv
        data/processed/dim_date.csv
        data/processed/dim_component.csv
        data/processed/sdr_normalized.csv  (for event-level detail table)

Output: data/processed/powerbi_fact_readiness.csv
        data/processed/powerbi_dim_aircraft.csv
        data/processed/powerbi_dim_date.csv
        data/processed/powerbi_dim_component.csv
        data/processed/powerbi_events_detail.csv

Design notes:
  - Column names use spaces (not underscores) for cleaner Power BI field labels
  - Rates are exported as decimals (0.0–1.0); format as % inside Power BI
  - date_id (YYYYMM integer) is the join key between fact and dim_date
  - powerbi_events_detail is the event-level table for drill-through pages
"""
import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")
OUT_DIR   = Path("data/processed")


def export(df: pd.DataFrame, name: str):
    path = OUT_DIR / f"powerbi_{name}.csv"
    df.to_csv(path, index=False)
    print(f"  → {path.name:45s} {len(df):>8,} rows  |  {df.shape[1]} columns")


def prep_fact(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "synthetic_aircraft_id": "Aircraft ID",
        "date_id":               "Date ID",
        "report_year":           "Year",
        "report_month":          "Month",
        "failure_count":         "Failure Count",
        "repeat_count":          "Repeat Count",
        "downtime_hours":        "Downtime Hours",
        "total_hours":           "Total Hours",
        "available_hours":       "Available Hours",
        "availability_rate":     "Availability Rate",
        "repeat_disc_rate":      "Repeat Discrepancy Rate",
        "top_ata_chapter":       "Top ATA Chapter",
        "top_system_group":      "Top System Group",
    })


def prep_dim_aircraft(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "synthetic_aircraft_id": "Aircraft ID",
        "aircraft_make":         "Make",
        "aircraft_model":        "Model",
        "first_seen_year":       "First Seen Year",
        "last_seen_year":        "Last Seen Year",
        "total_events":          "Total Events",
    })


def prep_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "date_id":      "Date ID",
        "report_year":  "Year",
        "report_month": "Month Number",
        "quarter":      "Quarter",
        "month_label":  "Month Label",
    })


def prep_dim_component(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "component_id":   "Component ID",
        "ata_chapter":    "ATA Chapter",
        "ata_description":"ATA Description",
        "system_group":   "System Group",
    })


def prep_events_detail(df: pd.DataFrame) -> pd.DataFrame:
    keep = [
        "synthetic_aircraft_id", "DifficultyDate", "source_year",
        "ata_chapter", "ata_description", "system_group",
        "condition_label", "PartCondition", "PartName",
        "AircraftMake", "AircraftModel",
        "is_repeat", "days_since_last",
        "StageOfOperationCode", "HowDiscoveredCode",
    ]
    keep = [c for c in keep if c in df.columns]
    out = df[keep].copy()
    out["DifficultyDate"] = pd.to_datetime(out["DifficultyDate"], errors="coerce").dt.date
    return out.rename(columns={
        "synthetic_aircraft_id": "Aircraft ID",
        "DifficultyDate":        "Event Date",
        "source_year":           "Year",
        "ata_chapter":           "ATA Chapter",
        "ata_description":       "ATA Description",
        "system_group":          "System Group",
        "condition_label":       "Condition",
        "PartCondition":         "Part Condition",
        "PartName":              "Part Name",
        "AircraftMake":          "Make",
        "AircraftModel":         "Model",
        "is_repeat":             "Is Repeat",
        "days_since_last":       "Days Since Last Event",
        "StageOfOperationCode":  "Stage of Operation",
        "HowDiscoveredCode":     "How Discovered",
    })


def main():
    print("Loading processed files...")
    fact      = pd.read_csv(PROCESSED / "fact_readiness_proxy.csv", low_memory=False)
    dim_ac    = pd.read_csv(PROCESSED / "dim_aircraft.csv",         low_memory=False)
    dim_date  = pd.read_csv(PROCESSED / "dim_date.csv",             low_memory=False)
    dim_comp  = pd.read_csv(PROCESSED / "dim_component.csv",        low_memory=False)
    events    = pd.read_csv(PROCESSED / "sdr_normalized.csv",       low_memory=False)

    print("\nExporting Power BI CSVs...")
    export(prep_fact(fact),               "fact_readiness")
    export(prep_dim_aircraft(dim_ac),     "dim_aircraft")
    export(prep_dim_date(dim_date),       "dim_date")
    export(prep_dim_component(dim_comp),  "dim_component")
    export(prep_events_detail(events),    "events_detail")

    print("\nDone. Import these files into Power BI Desktop via Get Data → Text/CSV.")
    print("Join key: 'Aircraft ID' links fact ↔ dim_aircraft")
    print("          'Date ID'     links fact ↔ dim_date")
    print("          'ATA Chapter' links events_detail ↔ dim_component")


if __name__ == "__main__":
    main()
