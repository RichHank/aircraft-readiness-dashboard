import pandas as pd

from etl.build_fact_table import build_fact


def test_availability_rate_never_drops_below_zero():
    df = pd.DataFrame(
        {
            "synthetic_aircraft_id": ["AC-1"] * 50,
            "report_year": [2025] * 50,
            "report_month": [1] * 50,
            "OperatorControlNumber": [f"E{i}" for i in range(50)],
            "is_repeat": [1] * 50,
            "ata_chapter": ["53"] * 50,
            "system_group": ["Airframe"] * 50,
        }
    )

    result = build_fact(df)

    assert result.loc[0, "downtime_hours"] == 720
    assert result.loc[0, "availability_rate"] == 0


def test_repeat_discrepancy_rate_is_zero_without_repeats():
    df = pd.DataFrame(
        {
            "synthetic_aircraft_id": ["AC-1", "AC-1"],
            "report_year": [2025, 2025],
            "report_month": [2, 2],
            "OperatorControlNumber": ["A", "B"],
            "is_repeat": [0, 0],
            "ata_chapter": ["29", "29"],
            "system_group": ["Hydraulics", "Hydraulics"],
        }
    )

    result = build_fact(df)

    assert result.loc[0, "repeat_disc_rate"] == 0
