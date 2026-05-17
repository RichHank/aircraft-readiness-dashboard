"""
Clean and standardize the staged FAA SDR data.

Input:  data/processed/sdr_raw.csv
Output: data/processed/sdr_clean.csv

Cleaning steps applied (each documented in ASSUMPTIONS_AND_LIMITATIONS.md):
  1. Parse and validate DifficultyDate
  2. Extract ATA chapter from JASCCode (first 2 digits)
  3. Deduplicate on OperatorControlNumber
  4. Hash RegistryNNumber → synthetic aircraft ID
  5. Cap AircraftTotalTime outliers (> 200,000 hrs = data entry error)
  6. Standardize PartCondition to known categories
  7. Flag repeat discrepancies: same synthetic_aircraft_id + ata_chapter within 30 days
  8. Drop rows missing the fields required for analysis
"""
import hashlib
import pandas as pd
from pathlib import Path

IN_FILE = Path("data/processed/sdr_raw.csv")
OUT_FILE = Path("data/processed/sdr_clean.csv")

AIRCRAFT_TOTAL_TIME_CAP = 200_000  # hours — anything above is a data entry error

# NatureOfConditionA codes → human-readable labels (FAA SDR code table)
NATURE_OF_CONDITION_MAP = {
    "A": "Cracked",
    "B": "Corrosion",
    "C": "Burned",
    "D": "Collapsed",
    "E": "Dented",
    "F": "Failed",
    "G": "Fractured",
    "H": "Jammed",
    "J": "Other",
    "K": "Out of Adjustment",
    "L": "Loose",
    "M": "Missing",
    "N": "Punctured",
    "O": "Defective",
    "P": "Separated",
    "R": "Seized",
    "S": "Shorted",
    "W": "Worn",
    "Y": "Delaminated",
    "Z": "Leaking",
}


def _hash_tail(n_number: str) -> str:
    """Replace real tail number with a stable synthetic ID."""
    h = hashlib.sha256(str(n_number).strip().upper().encode()).hexdigest()[:8]
    return f"AC-{h.upper()}"


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["DifficultyDate"] = pd.to_datetime(df["DifficultyDate"], errors="coerce")
    df["report_year"] = df["DifficultyDate"].dt.year
    df["report_month"] = df["DifficultyDate"].dt.month
    df["report_date_id"] = df["DifficultyDate"].dt.strftime("%Y%m%d").astype("Int64")
    return df


def extract_ata(df: pd.DataFrame) -> pd.DataFrame:
    df["JASCCode"] = df["JASCCode"].astype(str).str.strip()
    df["ata_chapter"] = df["JASCCode"].str[:2].str.zfill(2)
    df["ata_subcode"] = df["JASCCode"].str[:4]
    return df


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["OperatorControlNumber"])
    dropped = before - len(df)
    if dropped:
        print(f"  Deduplication: removed {dropped:,} duplicate OperatorControlNumbers")
    return df


def anonymize_aircraft(df: pd.DataFrame) -> pd.DataFrame:
    df["synthetic_aircraft_id"] = df["RegistryNNumber"].apply(
        lambda x: _hash_tail(x) if pd.notna(x) else "AC-UNKNOWN"
    )
    return df


def cap_total_time(df: pd.DataFrame) -> pd.DataFrame:
    df["AircraftTotalTime"] = pd.to_numeric(df["AircraftTotalTime"], errors="coerce")
    suspect = (df["AircraftTotalTime"] > AIRCRAFT_TOTAL_TIME_CAP).sum()
    if suspect:
        print(f"  Capping {suspect:,} AircraftTotalTime values > {AIRCRAFT_TOTAL_TIME_CAP:,} hrs → NaN")
    df.loc[df["AircraftTotalTime"] > AIRCRAFT_TOTAL_TIME_CAP, "AircraftTotalTime"] = pd.NA
    return df


def standardize_condition(df: pd.DataFrame) -> pd.DataFrame:
    df["condition_label"] = df["NatureOfConditionA"].map(NATURE_OF_CONDITION_MAP).fillna("Unknown")
    return df


def flag_repeats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag is_repeat = 1 when the same synthetic_aircraft_id reports a failure
    on the same ata_chapter within 30 days of a prior event.
    See ASSUMPTIONS_AND_LIMITATIONS.md §5 for heuristic limitations.
    """
    key = ["synthetic_aircraft_id", "ata_chapter"]
    df = df.sort_values(key + ["DifficultyDate"])
    df["_prev_date"] = df.groupby(key)["DifficultyDate"].shift(1)
    df["days_since_last"] = (df["DifficultyDate"] - df["_prev_date"]).dt.days
    df["is_repeat"] = (df["days_since_last"] <= 30).astype("Int64")
    df = df.drop(columns=["_prev_date"])
    repeat_pct = df["is_repeat"].mean() * 100
    print(f"  Repeat discrepancy rate: {repeat_pct:.1f}%")
    return df


def drop_unusable(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing fields required for any downstream analysis."""
    required = ["DifficultyDate", "ata_chapter", "synthetic_aircraft_id"]
    before = len(df)
    df = df.dropna(subset=required)
    # Drop rows where tail number was missing — these all hash to AC-UNKNOWN
    # and would pollute aircraft-level analysis with a phantom aggregate aircraft.
    unknown_before = len(df)
    df = df[df["synthetic_aircraft_id"] != "AC-UNKNOWN"]
    unknown_dropped = unknown_before - len(df)
    if unknown_dropped:
        print(f"  Dropped {unknown_dropped:,} rows with missing tail number (AC-UNKNOWN)")
    dropped = before - len(df)
    if dropped:
        print(f"  Dropped {dropped:,} rows total missing required fields")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = parse_dates(df)
    df = extract_ata(df)
    df = deduplicate(df)
    df = anonymize_aircraft(df)
    df = cap_total_time(df)
    df = standardize_condition(df)
    df = drop_unusable(df)
    df = flag_repeats(df)
    return df


def main():
    print(f"Reading {IN_FILE}...")
    df = pd.read_csv(IN_FILE, low_memory=False)
    print(f"  Input rows: {len(df):,}")

    df = clean(df)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"\nClean output: {len(df):,} rows → {OUT_FILE}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()
