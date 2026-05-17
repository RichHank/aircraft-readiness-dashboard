"""
Extract raw FAA SDR CSV files from data/raw/ into a single staged DataFrame.

Handles multiple years (e.g. SDR-2023.csv, SDR-2024.csv, SDR-2025.csv).
Tags each row with source_year and source_file.
Output: data/processed/sdr_raw.csv
"""
import pandas as pd
from pathlib import Path
import sys

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/sdr_raw.csv")

# Only columns we actually use downstream — drop the ~50 structural geometry
# fields (FuselageStation, Stringer, WingStation, ButtLine, WaterLine) that
# are >90% null and irrelevant to maintenance burden analysis.
KEEP_COLUMNS = [
    "OperatorControlNumber",
    "DifficultyDate",
    "SubmissionDate",
    "OperatorDesignator",
    "SDRType",
    "JASCCode",
    "NatureOfConditionA",
    "NatureOfConditionB",
    "NatureOfConditionC",
    "PrecautionaryProcedureA",
    "HowDiscoveredCode",
    "StageOfOperationCode",
    "RegistryNNumber",
    "AircraftMake",
    "AircraftModel",
    "AircraftSerialNumber",
    "AircraftTotalTime",
    "AircraftTotalCycles",
    "PartName",
    "PartCondition",
    "PartLocation",
    "PartTotalTime",
    "Discrepancy",
]


def extract_file(path: Path, year: int) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False, usecols=lambda c: c in KEEP_COLUMNS)
    df["source_year"] = year
    df["source_file"] = path.name
    print(f"  {path.name}: {len(df):,} rows")
    return df


def main():
    sdr_files = sorted(RAW_DIR.glob("SDR-*.csv"))
    if not sdr_files:
        print(f"ERROR: No SDR-*.csv files found in {RAW_DIR}/", file=sys.stderr)
        sys.exit(1)

    frames = []
    for f in sdr_files:
        try:
            year = int(f.stem.split("-")[1])
        except (IndexError, ValueError):
            print(f"  Skipping {f.name} — cannot parse year from filename")
            continue
        frames.append(extract_file(f, year))

    df = pd.concat(frames, ignore_index=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"\nExtracted {len(df):,} total rows → {OUT_FILE}")
    print(f"Years: {sorted(df['source_year'].unique())}")


if __name__ == "__main__":
    main()
