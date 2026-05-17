"""
Normalize ATA chapter codes into human-readable system group labels.

Input:  data/processed/sdr_clean.csv
Output: data/processed/sdr_normalized.csv

Joins each event's ata_chapter to a built-in ATA reference table,
adding ata_description and system_group columns for grouping in SQL and Power BI.
No external file dependency — reference table is embedded here and written to
data/processed/dim_component.csv for use in the SQL schema.
"""
import pandas as pd
from pathlib import Path

IN_FILE = Path("data/processed/sdr_clean.csv")
OUT_FILE = Path("data/processed/sdr_normalized.csv")
DIM_COMPONENT_OUT = Path("data/processed/dim_component.csv")

# ATA 100 chapter reference — covers all 50 chapters observed in the SDR dataset.
# Source: ATA iSpec 2200 public chapter list.
ATA_REFERENCE = [
    ("05", "Time Limits / Maintenance Checks",      "Airworthiness"),
    ("06", "Dimensions and Areas",                  "Airworthiness"),
    ("07", "Lifting and Shoring",                   "Airworthiness"),
    ("08", "Leveling and Weighing",                 "Airworthiness"),
    ("09", "Towing and Taxiing",                    "Airworthiness"),
    ("10", "Parking, Mooring, Storage",             "Airworthiness"),
    ("11", "Placards and Markings",                 "Airworthiness"),
    ("12", "Servicing",                             "Airworthiness"),
    ("20", "Standard Practices — Airframe",         "Airframe"),
    ("21", "Air Conditioning",                      "Environmental"),
    ("22", "Auto Flight",                           "Avionics"),
    ("23", "Communications",                        "Avionics"),
    ("24", "Electrical Power",                      "Electrical"),
    ("25", "Equipment / Furnishings",               "Cabin & Furnishings"),
    ("26", "Fire Protection",                       "Safety Systems"),
    ("27", "Flight Controls",                       "Flight Controls"),
    ("28", "Fuel",                                  "Fuel System"),
    ("29", "Hydraulic Power",                       "Hydraulics"),
    ("30", "Ice and Rain Protection",               "Environmental"),
    ("31", "Instruments",                           "Avionics"),
    ("32", "Landing Gear",                          "Landing Gear"),
    ("33", "Lights",                                "Electrical"),
    ("34", "Navigation",                            "Avionics"),
    ("35", "Oxygen",                                "Safety Systems"),
    ("36", "Pneumatic",                             "Environmental"),
    ("37", "Vacuum",                                "Environmental"),
    ("38", "Water / Waste",                         "Cabin & Furnishings"),
    ("45", "Central Maintenance System",            "Avionics"),
    ("46", "Information Systems",                   "Avionics"),
    ("49", "Airborne Auxiliary Power",              "Propulsion"),
    ("51", "Standard Practices — Structures",       "Airframe"),
    ("52", "Doors",                                 "Airframe"),
    ("53", "Fuselage",                              "Airframe"),
    ("54", "Nacelles / Pylons",                     "Airframe"),
    ("55", "Stabilizers",                           "Airframe"),
    ("56", "Windows",                               "Airframe"),
    ("57", "Wings",                                 "Airframe"),
    ("61", "Propellers",                            "Propulsion"),
    ("62", "Main Rotor",                            "Propulsion"),
    ("63", "Main Rotor Drive",                      "Propulsion"),
    ("64", "Tail Rotor",                            "Propulsion"),
    ("65", "Tail Rotor Drive",                      "Propulsion"),
    ("67", "Rotors Flight Control",                 "Flight Controls"),
    ("71", "Power Plant",                           "Propulsion"),
    ("72", "Engine — Turbine / Turboprop",          "Propulsion"),
    ("73", "Engine Fuel and Control",               "Propulsion"),
    ("74", "Ignition",                              "Propulsion"),
    ("75", "Air",                                   "Propulsion"),
    ("76", "Engine Controls",                       "Propulsion"),
    ("77", "Engine Indicating",                     "Propulsion"),
    ("78", "Exhaust",                               "Propulsion"),
    ("79", "Oil",                                   "Propulsion"),
    ("80", "Starting",                              "Propulsion"),
    ("14", "Hardware",                              "Airworthiness"),
    ("81", "Turbines (Reciprocating Engines)",      "Propulsion"),
    ("82", "Water Injection",                       "Propulsion"),
    ("83", "Accessory Gearboxes",                   "Propulsion"),
    ("85", "Fuel Cell Systems",                     "Propulsion"),
]

ATA_LOOKUP = pd.DataFrame(ATA_REFERENCE, columns=["ata_chapter", "ata_description", "system_group"])


def main():
    print(f"Reading {IN_FILE}...")
    df = pd.read_csv(IN_FILE, low_memory=False)
    print(f"  Input rows: {len(df):,}")

    df["ata_chapter"] = df["ata_chapter"].astype(str).str.zfill(2)
    before_chapters = df["ata_chapter"].nunique()
    df = df.merge(ATA_LOOKUP, on="ata_chapter", how="left")

    unmatched = df["ata_description"].isna().sum()
    if unmatched:
        unmatched_chapters = df.loc[df["ata_description"].isna(), "ata_chapter"].unique()
        print(f"  WARNING: {unmatched:,} rows have unrecognized ATA chapters: {sorted(unmatched_chapters)}")
        df["ata_description"] = df["ata_description"].fillna("Unknown")
        df["system_group"] = df["system_group"].fillna("Unknown")

    after_chapters = df["ata_chapter"].nunique()
    print(f"  ATA chapters in data: {before_chapters} | matched to reference: {after_chapters - (1 if unmatched else 0)}")
    print(f"  System groups: {sorted(df['system_group'].unique())}")

    # Write dim_component for SQL schema population
    dim = ATA_LOOKUP.copy()
    dim.insert(0, "component_id", "ATA-" + dim["ata_chapter"])
    dim.to_csv(DIM_COMPONENT_OUT, index=False)
    print(f"  dim_component written → {DIM_COMPONENT_OUT}")

    df.to_csv(OUT_FILE, index=False)
    print(f"\nNormalized output: {len(df):,} rows → {OUT_FILE}")


if __name__ == "__main__":
    main()
