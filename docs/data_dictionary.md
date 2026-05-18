# Data Dictionary

This dictionary documents the final analyst-facing tables exported for Power BI and loaded into SQLite.

## `fact_readiness`

One row per synthetic aircraft per reporting month.

| Field | Description |
| --- | --- |
| `Aircraft ID` | Stable synthetic aircraft identifier |
| `Date ID` | Month key in `YYYYMM` format |
| `Year` | Reporting year |
| `Month` | Reporting month number |
| `Failure Count` | Maintenance events observed for the aircraft-month |
| `Repeat Count` | Events flagged as repeat discrepancies |
| `Downtime Hours` | Estimated monthly downtime hours |
| `Top ATA Chapter` | Most frequent ATA chapter for the aircraft-month |
| `Top System Group` | Most frequent system group for the aircraft-month |
| `Total Hours` | Assumed possessed hours in the month |
| `Available Hours` | `Total Hours - Downtime Hours` |
| `Availability Rate` | Availability proxy for the aircraft-month |
| `Repeat Discrepancy Rate` | `Repeat Count / Failure Count` |

## `dim_aircraft`

| Field | Description |
| --- | --- |
| `Aircraft ID` | Stable synthetic aircraft identifier |
| `Make` | Aircraft manufacturer |
| `Model` | Aircraft model |
| `First Seen Year` | First year observed in the dataset |
| `Last Seen Year` | Last year observed in the dataset |
| `Total Events` | Total event count for the aircraft |

## `dim_date`

| Field | Description |
| --- | --- |
| `Year` | Reporting year |
| `Month Number` | Reporting month number |
| `Date ID` | Month key in `YYYYMM` format |
| `Quarter` | Calendar quarter |
| `Month Label` | Display label such as `Jan 2025` |

## `dim_component`

| Field | Description |
| --- | --- |
| `Component ID` | Component key such as `ATA-53` |
| `ATA Chapter` | ATA chapter code |
| `ATA Description` | Human-readable ATA chapter name |
| `System Group` | Higher-level grouping such as Airframe or Hydraulics |

## `events_detail`

Event-level table used for drill-down analysis.

| Field | Description |
| --- | --- |
| `Aircraft ID` | Stable synthetic aircraft identifier |
| `Event Date` | Date of the maintenance event |
| `Year` | Source year |
| `ATA Chapter` | ATA chapter code |
| `ATA Description` | Human-readable ATA chapter name |
| `System Group` | Higher-level system grouping |
| `Condition` | Standardized condition label |
| `Part Condition` | Original part-condition field from SDR |
| `Part Name` | Part name from SDR |
| `Make` | Aircraft manufacturer |
| `Model` | Aircraft model |
| `Is Repeat` | `1` when flagged as a repeat discrepancy |
| `Days Since Last Event` | Days since the prior same-aircraft / same-ATA event |
| `Stage of Operation` | SDR stage-of-operation code |
| `How Discovered` | SDR discovery-method code |

## Notes

- Real registration numbers are not exposed downstream.
- All aircraft IDs are synthetic hashes generated during cleaning.
- `Availability Rate` is a documented proxy, not an official operational-readiness metric.
