# Assumptions and Limitations

**Project:** Aircraft Maintenance Event Analytics
**Data Source:** FAA Service Difficulty Reporting (SDR) System — Public Dataset
**Last Updated:** 2026-05-15

---

## Purpose

This project analyzes publicly available FAA Service Difficulty Report (SDR) data to identify
trends in aircraft maintenance events, recurring component discrepancies, and system-level
maintenance burden indicators.

The analysis is intended for educational and portfolio purposes. It does not represent
real operational readiness data, official safety analysis, or regulatory reporting of any kind.

---

## 1. What the FAA SDR Dataset Contains

The FAA SDR dataset is a public record of maintenance difficulty reports submitted
voluntarily or mandatorily by aircraft operators, repair stations, and maintenance
organizations in the United States.

Each record captures:

- Date of occurrence
- Aircraft manufacturer and model series
- Component or part involved (classified by JASC/ATA chapter code)
- Nature of the failure or defect
- Part condition and location on aircraft
- Severity classification
- Free-text remarks from the reporting mechanic or operator

---

## 2. What the FAA SDR Dataset Does NOT Contain

The SDR dataset is a difficulty reporting system, not a readiness or operations system.
It does not include:

- Aircraft readiness status (mission capable / non-mission capable)
- Operational availability or utilization rates
- Maintenance labor hours per event
- Actual downtime duration (how long the aircraft was out of service)
- Supply chain or parts wait times
- Maintenance staffing levels
- Sortie counts or flight hours per aircraft
- Corrective action outcomes (only free-text remarks)
- Confirmation that a reported issue was actually repaired

**This distinction is critical.** Every metric derived from SDR data is a proxy
indicator — not a direct measurement of readiness or availability.

---

## 3. Metrics That Are Direct Measurements

The following are taken directly from the SDR dataset with minimal transformation:

| Metric | SDR Source Field |
|--------|-----------------|
| Maintenance event count | One row = one reported event |
| Event date | `date_of_occurrence` |
| ATA chapter classification | `jasc_ata_code` |
| Aircraft model series | `aircraft_manufacturer_model` |
| Failure description | `nature_of_condition` + `part_condition` (combined) |
| Severity classification | `severity_factor` |

---

## 4. Metrics That Are Derived or Proxy

These metrics do not exist in the raw SDR data. They are calculated during ETL or
SQL aggregation and carry the assumptions described below.

### Availability Rate (Readiness Proxy)

**Definition:** `available_hours / total_hours` per aircraft per reporting period

**How derived:** Total hours in the reporting period are assumed constant per aircraft.
Downtime hours are estimated by multiplying event count by an assumed average downtime
per event type (unscheduled, scheduled, repeat). These estimates are not sourced from
real maintenance records.

**Limitation:** This metric approximates maintenance burden, not operational availability.
Two aircraft with identical event counts may have very different actual downtime depending
on part availability, crew size, and repair complexity — none of which appear in SDR data.

### Downtime Hours

**Definition:** An estimated duration assigned to each maintenance event.

**How derived:** No downtime field exists in SDR data. Downtime is estimated using
assumed average hours per event type:

| Event Type | Assumed Average Downtime |
|------------|--------------------------|
| Scheduled | 4 hours |
| Unscheduled | 12 hours |
| Repeat Discrepancy | 18 hours |

These values are illustrative assumptions, not empirical averages. They exist to support
trend comparison across the dataset, not to claim precision about any individual event.

### Maintenance Burden Index

A weighted composite of event frequency, repeat discrepancy rate, and estimated downtime.
Intended to rank relative maintenance load across aircraft types and ATA chapters.
Not a validated index — do not cite as an authoritative measure.

---

## 5. Repeat Discrepancy Detection Logic

A maintenance event is flagged as a repeat discrepancy when:

- The same **synthetic aircraft identifier** (see Section 6)
- Reports a failure on the same **ATA chapter**
- Within a **rolling 30-day window** of a prior event on that aircraft and chapter

**Known limitations of this heuristic:**

- SDR data does not confirm whether the prior failure was actually repaired
- ATA chapter matching is coarse — two different components within the same chapter
  will be counted as a repeat even if unrelated
- The 30-day window is an arbitrary threshold with no empirical basis in the SDR system
- Under-reporting in SDR means some true repeats will not appear in the data at all

---

## 6. Synthetic Aircraft Identifiers

The FAA SDR dataset includes real aircraft registration numbers (tail numbers).
**This project does not use real tail numbers.**

During the ETL cleaning step, registration numbers are hashed and replaced with
synthetic identifiers (e.g. `AC-001`, `AC-002`). This is done to:

- Avoid profiling or implying fault against specific operators or aircraft
- Maintain analytical grouping (events can still be linked per aircraft)
- Ensure the project does not misrepresent real operational histories

Synthetic identifiers are used solely to support trend aggregation. They do not
correspond to real aircraft.

---

## 7. Data Quality Considerations

The FAA SDR dataset is real-world operational data and carries the quality issues
typical of voluntary reporting systems:

- **Inconsistent free-text remarks** — mechanic notes vary widely in detail and terminology
- **Missing fields** — severity, ATA code, and part location are frequently blank
- **Inconsistent ATA coding** — the same component type may be coded differently
  across operators or years
- **Duplicate submissions** — the same event may appear multiple times if multiple
  parties report it
- **Reporting bias** — not all maintenance events are reported; SDR captures difficulty
  events, not routine maintenance
- **Retrospective entries** — some events are logged weeks after occurrence

ETL cleaning steps address deduplication, date standardization, and ATA code normalization,
but inconsistencies remain. Results should be interpreted as directional, not precise.

---

## 8. Risks of Interpretation

**Do not interpret this analysis as:**

- Official aircraft readiness or safety reporting
- Predictive maintenance or failure forecasting
- Operational risk scoring for any real aircraft or operator
- Benchmarking of real military or commercial fleet performance
- Evidence of regulatory compliance or non-compliance

**The project is intended to demonstrate:**

- End-to-end ETL pipeline design using real public data
- Star schema modeling and SQL analytics
- Proxy metric construction when direct data is unavailable
- Power BI dashboard development
- Analytical documentation practices

Any finding in this project should be treated as a demonstration of methodology,
not a claim about real-world aircraft safety or readiness.

---

## 9. Future Improvements

The following additions would increase analytical accuracy and scope:

| Addition | What It Would Enable |
|----------|---------------------|
| Aircraft utilization data (flight hours per tail) | True availability rate instead of estimated proxy |
| Maintenance labor-hour records | Real downtime measurement |
| Component replacement interval data (OEM specs) | Predictive failure modeling |
| Supply chain / AOG records | NMC-Supply vs NMC-Maintenance breakdown |
| Weather and operating environment data | Environmental failure correlation |
| Multiple years of SDR data | Long-term trend analysis, seasonality detection |
| Voluntary ASRS maintenance reports (NASA) | Richer corrective action narratives |

These are documented here, not implemented, because the goal of this project is a
clean and credible analysis of what the available data actually supports — not a
demonstration of what could be built with better data.

---

*This document should be reviewed and updated whenever ETL logic, metric definitions,
or source data change.*
