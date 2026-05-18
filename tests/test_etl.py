import pandas as pd

from etl.build_fact_table import build_fact
from etl.clean_sdr import deduplicate, flag_repeats


def test_deduplicate_uses_operator_control_number():
    df = pd.DataFrame(
        {
            "OperatorControlNumber": ["A", "A", "B"],
            "value": [1, 2, 3],
        }
    )

    result = deduplicate(df)

    assert len(result) == 2
    assert set(result["OperatorControlNumber"]) == {"A", "B"}


def test_flag_repeats_marks_same_aircraft_same_ata_within_30_days():
    df = pd.DataFrame(
        {
            "synthetic_aircraft_id": ["AC-1", "AC-1", "AC-1", "AC-2"],
            "ata_chapter": ["53", "53", "53", "53"],
            "DifficultyDate": pd.to_datetime(
                ["2025-01-01", "2025-01-20", "2025-03-01", "2025-01-10"]
            ),
        }
    )

    result = flag_repeats(df)

    assert result["is_repeat"].tolist() == [0, 1, 0, 0]


def test_build_fact_outputs_expected_monthly_metrics():
    df = pd.DataFrame(
        {
            "synthetic_aircraft_id": ["AC-1", "AC-1", "AC-2"],
            "report_year": [2025, 2025, 2025],
            "report_month": [1, 1, 1],
            "OperatorControlNumber": ["A", "B", "C"],
            "is_repeat": [0, 1, 0],
            "ata_chapter": ["53", "53", "32"],
            "system_group": ["Airframe", "Airframe", "Landing Gear"],
        }
    )

    result = build_fact(df).sort_values("synthetic_aircraft_id").reset_index(drop=True)

    ac1 = result.iloc[0]
    assert ac1["failure_count"] == 2
    assert ac1["repeat_count"] == 1
    assert ac1["downtime_hours"] == 30.0
    assert ac1["repeat_disc_rate"] == 0.5
    assert 0 <= ac1["availability_rate"] <= 1
