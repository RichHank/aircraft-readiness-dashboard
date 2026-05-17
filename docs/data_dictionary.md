# Data Dictionary

All data is sourced from public FAA/ASRS records or clearly labeled synthetic demo data.
No real military readiness figures or sensitive operational data are used.

---

## fact_maintenance_events

| Field | Type | Description |
|-------|------|-------------|
| event_id | INTEGER | Surrogate primary key |
| aircraft_id | TEXT | FK → dim_aircraft |
| component_id | TEXT | FK → dim_component (ATA chapter) |
| date_id | INTEGER | FK → dim_date (YYYYMMDD) |
| event_type | TEXT | "Unscheduled", "Scheduled", or "Repeat" |
| downtime_hours | REAL | Hours aircraft was out of service for this event |
| is_repeat | INTEGER | 1 if same component failed within 30 days of prior event |
| corrective_action | TEXT | Description of corrective action taken |
| source_report | TEXT | Origin: "FAA-SDR", "ASRS", or "Synthetic-Demo" |

---

## fact_readiness_proxy

One row per aircraft per reporting period. Derived from `fact_maintenance_events`.

| Field | Type | Description |
|-------|------|-------------|
| proxy_id | INTEGER | Surrogate primary key |
| aircraft_id | TEXT | FK → dim_aircraft |
| date_id | INTEGER | FK → dim_date |
| available_hours | REAL | Hours available for operations (total − downtime) |
| total_hours | REAL | Total hours in reporting period |
| downtime_hours | REAL | Sum of maintenance event downtime for the period |
| failure_count | INTEGER | Number of maintenance events in the period |
| repeat_count | INTEGER | Number of repeat discrepancy events |
| availability_rate | REAL | available_hours / total_hours — primary readiness proxy |
| repeat_disc_rate | REAL | repeat_count / failure_count |

---

## dim_aircraft

| Field | Type | Description |
|-------|------|-------------|
| aircraft_id | TEXT | Synthetic ID (e.g. AC-001); not a real tail number |
| aircraft_type | TEXT | "Fixed-Wing" or "Rotary-Wing" |
| model_series | TEXT | Generic series label (e.g. "Model-A") — not a real MDS |
| operator_code | TEXT | Anonymized operator code |
| manufacture_year | INTEGER | Year of manufacture |

---

## dim_component

| Field | Type | Description |
|-------|------|-------------|
| component_id | TEXT | Unique component identifier |
| ata_chapter | TEXT | ATA 100 chapter code (e.g. "32" = Landing Gear) |
| ata_description | TEXT | Human-readable ATA chapter name |
| system_group | TEXT | High-level grouping: "Airframe", "Propulsion", "Avionics", "Hydraulics", etc. |

---

## dim_date

| Field | Type | Description |
|-------|------|-------------|
| date_id | INTEGER | YYYYMMDD surrogate key |
| date | TEXT | ISO date string |
| year | INTEGER | Calendar year |
| month | INTEGER | Month (1–12) |
| quarter | INTEGER | Calendar quarter (1–4) |
| week_of_year | INTEGER | ISO week number |

---

## Event Type Definitions

| Value | Meaning |
|-------|---------|
| Unscheduled | Maintenance event not on the planned schedule |
| Scheduled | Routine/planned maintenance |
| Repeat | Same component/discrepancy within 30 days of prior fix |

---

## ATA Chapter Reference (partial)

| Chapter | System |
|---------|--------|
| 21 | Air Conditioning |
| 24 | Electrical Power |
| 27 | Flight Controls |
| 28 | Fuel |
| 29 | Hydraulic Power |
| 32 | Landing Gear |
| 34 | Navigation |
| 71–80 | Propulsion |
