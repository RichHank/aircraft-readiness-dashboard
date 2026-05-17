"""
Build the readiness proxy fact table.

Input:  data/processed/sdr_normalized.csv
Output: data/processed/fact_readiness_proxy.csv
        data/processed/dim_aircraft.csv
        data/processed/dim_date.csv

One row per synthetic_aircraft_id per year-month.
Computes:
  - failure_count        : total maintenance events in the period
  - repeat_count         : events flagged as repeat discrepancies
  - repeat_disc_rate     : repeat_count / failure_count
  - downtime_hours       : estimated (see ASSUMPTIONS_AND_LIMITATIONS.md §4)
  - total_hours          : assumed 720 hrs/month per aircraft (30 days × 24 hrs)
  - available_hours      : total_hours - downtime_hours
  - availability_rate    : available_hours / total_hours
"""
import pandas as pd
from pathlib import Path

IN_FILE  = Path("data/processed/sdr_normalized.csv")
FACT_OUT = Path("data/processed/fact_readiness_proxy.csv")
DIM_AC   = Path("data/processed/dim_aircraft.csv")
DIM_DATE = Path("data/processed/dim_date.csv")

# Assumed downtime hours per event type (documented in ASSUMPTIONS_AND_LIMITATIONS.md)
DOWNTIME_MAP = {
    0: 12.0,   # non-repeat unscheduled event
    1: 18.0,   # repeat discrepancy — longer to resolve
}
TOTAL_HOURS_PER_MONTH = 720  # 30 days × 24 hrs — possessed hours assumption


def build_dim_aircraft(df: pd.DataFrame) -> pd.DataFrame:
    dim = (
        df.groupby("synthetic_aircraft_id")
        .agg(
            aircraft_make=("AircraftMake", lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown"),
            aircraft_model=("AircraftModel", lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown"),
            first_seen_year=("source_year", "min"),
            last_seen_year=("source_year", "max"),
            total_events=("OperatorControlNumber", "count"),
        )
        .reset_index()
    )
    return dim


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    dates = (
        df[["report_year", "report_month"]]
        .drop_duplicates()
        .dropna()
        .copy()
    )
    dates["report_year"]  = dates["report_year"].astype(int)
    dates["report_month"] = dates["report_month"].astype(int)
    dates["date_id"] = dates["report_year"] * 100 + dates["report_month"]
    dates["quarter"] = ((dates["report_month"] - 1) // 3 + 1)
    dates["month_label"] = pd.to_datetime(
        dates["report_year"].astype(str) + "-" + dates["report_month"].astype(str).str.zfill(2) + "-01"
    ).dt.strftime("%b %Y")
    return dates.sort_values("date_id").reset_index(drop=True)


def build_fact(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["report_year", "report_month", "synthetic_aircraft_id"]).copy()
    df["report_year"]  = df["report_year"].astype(int)
    df["report_month"] = df["report_month"].astype(int)
    df["date_id"]      = df["report_year"] * 100 + df["report_month"]
    df["is_repeat"]    = df["is_repeat"].fillna(0).astype(int)
    df["downtime_est"] = df["is_repeat"].map(DOWNTIME_MAP)

    fact = (
        df.groupby(["synthetic_aircraft_id", "date_id", "report_year", "report_month"])
        .agg(
            failure_count  =("OperatorControlNumber", "count"),
            repeat_count   =("is_repeat", "sum"),
            downtime_hours =("downtime_est", "sum"),
            top_ata_chapter=("ata_chapter", lambda x: x.mode().iloc[0]),
            top_system_group=("system_group", lambda x: x.mode().iloc[0]),
        )
        .reset_index()
    )

    fact["total_hours"]       = TOTAL_HOURS_PER_MONTH
    fact["downtime_hours"]    = fact["downtime_hours"].clip(upper=TOTAL_HOURS_PER_MONTH)
    fact["available_hours"]   = fact["total_hours"] - fact["downtime_hours"]
    fact["availability_rate"] = (fact["available_hours"] / fact["total_hours"]).round(4)
    fact["repeat_disc_rate"]  = (fact["repeat_count"] / fact["failure_count"]).round(4)

    return fact


def main():
    print(f"Reading {IN_FILE}...")
    df = pd.read_csv(IN_FILE, low_memory=False)
    print(f"  Input rows: {len(df):,}")

    dim_aircraft = build_dim_aircraft(df)
    dim_date     = build_dim_date(df)
    fact         = build_fact(df)

    FACT_OUT.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(FACT_OUT, index=False)
    dim_aircraft.to_csv(DIM_AC, index=False)
    dim_date.to_csv(DIM_DATE, index=False)

    print(f"\nFact table:   {len(fact):,} rows → {FACT_OUT}")
    print(f"dim_aircraft: {len(dim_aircraft):,} rows → {DIM_AC}")
    print(f"dim_date:     {len(dim_date):,} rows → {DIM_DATE}")
    print(f"\nAvailability rate — mean: {fact['availability_rate'].mean():.3f} | min: {fact['availability_rate'].min():.3f} | max: {fact['availability_rate'].max():.3f}")
    print(f"Repeat disc rate  — mean: {fact['repeat_disc_rate'].mean():.3f} | min: {fact['repeat_disc_rate'].min():.3f} | max: {fact['repeat_disc_rate'].max():.3f}")
    print(f"Date range: {dim_date['month_label'].iloc[0]} → {dim_date['month_label'].iloc[-1]}")


if __name__ == "__main__":
    main()
