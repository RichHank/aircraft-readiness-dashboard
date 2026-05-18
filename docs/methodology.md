# Methodology

## Objective

Build an end-to-end aviation maintenance analytics workflow from public FAA Service Difficulty Report data and surface recurring burden patterns through SQL and Power BI.

## Source data

- FAA Service Difficulty Reporting System public CSV exports
- reporting window: January 2023 through December 2025
- final analyzed event count: 194,844

## Pipeline

### 1. Extraction

`etl/extract_sdr.py` ingests the yearly FAA SDR CSV files, keeps only fields used downstream, and appends source-year metadata.

### 2. Cleaning

`etl/clean_sdr.py` performs the core preparation work:

- parses event dates
- extracts ATA chapters from JASC codes
- removes duplicate operator-control numbers
- hashes tail numbers into stable synthetic aircraft IDs
- caps implausible aircraft-total-time outliers
- standardizes maintenance-condition labels
- removes unusable rows
- flags repeat discrepancies

### 3. Normalization

`etl/normalize_components.py` maps ATA chapters to human-readable descriptions and higher-level system groups such as Airframe, Electrical, Hydraulics, and Propulsion.

### 4. Fact-table construction

`etl/build_fact_table.py` creates:

- a monthly aircraft-level readiness proxy fact table
- an aircraft dimension
- a date dimension
- a component dimension

### 5. Power BI / SQLite export

`etl/export_powerbi_csv.py` writes clean analyst-facing CSVs with human-readable field names.  
`sql/load_db.py` loads those exports into SQLite and applies reusable analytical views.

## Repeat-discrepancy logic

An event is marked as a repeat when the same synthetic aircraft ID reports the same ATA chapter within a rolling 30-day window of a prior event.

This is a deliberate heuristic:

- it is useful for surfacing recurring burden
- it is not proof that the exact same component failed again
- it is limited by ATA chapter granularity and SDR reporting behavior

## Availability proxy

The FAA SDR dataset does not include real utilization or downtime fields, so the project creates a documented proxy:

- each aircraft-month receives an assumed 720 possessed hours
- non-repeat events are assigned 12 estimated downtime hours
- repeat events are assigned 18 estimated downtime hours
- monthly downtime is capped at 720 hours
- availability proxy = available hours / total hours

This allows relative comparison across the dataset, but it is not a direct measure of real fleet readiness.

## Quality controls

The workflow includes:

- event deduplication
- null handling
- ATA-code normalization
- synthetic ID generation
- SQL KPI validation
- unit tests for duplicate handling, repeat logic, and metric bounds

## Interpretation standard

The analysis is strongest when used for:

- recurring-burden detection
- comparative ranking
- follow-up hypothesis generation

It should not be used for:

- official readiness reporting
- safety certification claims
- operator benchmarking
- causal conclusions without richer maintenance data

See [`ASSUMPTIONS_AND_LIMITATIONS.md`](ASSUMPTIONS_AND_LIMITATIONS.md) for the full caveat set.
