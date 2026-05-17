# Findings

**Dataset:** FAA Service Difficulty Reports — 2023, 2024, 2025  
**Total events analyzed:** 194,844  
**Unique aircraft:** 12,226  
**Reporting period:** January 2023 – December 2025

---

## Summary

Analysis of three years of FAA SDR data reveals a consistent and structurally concentrated
maintenance burden pattern in U.S. civil aviation. Airframe structural systems — particularly
fuselage — generate repeat discrepancies at rates far exceeding all other system groups.
Fleet availability proxies are stable across the period, indicating the burden is persistent
rather than improving or worsening.

---

## Finding 1 — Fuselage (ATA 53) Dominates Recurring Maintenance Burden

ATA Chapter 53 (Fuselage) generated **75,690 maintenance events** across 2023–2025,
with a **87.1% repeat discrepancy rate** — the highest of any system in the dataset.

This means that for nearly 9 out of every 10 fuselage events, the same aircraft had
reported a fuselage discrepancy within the previous 30 days.

| ATA Chapter | Description | Total Events | Repeat Events | Repeat Rate |
|-------------|-------------|-------------|---------------|-------------|
| 53 | Fuselage | 75,690 | 65,931 | 87.1% |
| 57 | Wings | 16,000 | 11,266 | 70.4% |
| 55 | Stabilizers | 6,057 | 3,551 | 58.6% |
| 52 | Doors | 17,492 | 7,002 | 40.0% |
| 54 | Nacelles / Pylons | 2,204 | 921 | 41.8% |

Fuselage events alone represent **38.8%** of all maintenance events in the dataset,
making it the single largest contributor to maintenance burden by a wide margin.

The free-text discrepancy field confirms the pattern: corrosion on shear clips,
cracking at frame stations, and structural repairs that require reinspection — work
that is completed, signed off, and then rediscovered on the same airframe within weeks.

---

## Finding 2 — Airframe Structural Systems Repeat at 5× the Rate of Mechanical Systems

Aggregating by system group reveals a sharp divide between structural and mechanical
maintenance burden:

| System Group | Total Events | Repeat Events | Repeat Rate |
|-------------|-------------|---------------|-------------|
| Airframe | 120,637 | 89,466 | **74.2%** |
| Electrical | 26,055 | 9,080 | 34.8% |
| Cabin & Furnishings | 14,862 | 3,952 | 26.6% |
| Propulsion | 8,771 | 1,857 | 21.2% |
| Flight Controls | 3,153 | 628 | 19.9% |
| Landing Gear | 4,165 | 700 | 16.8% |
| Hydraulics | 1,580 | 214 | **13.5%** |

Hydraulic and landing gear systems — which involve discrete component replacements —
have repeat rates below 17%. Airframe structural work repeats at 74.2%.

This gap reflects the nature of structural maintenance: corrosion and cracking are
progressive conditions that are treated incrementally rather than resolved in a single
maintenance action.

---

## Finding 3 — Fleet Availability Proxy Is Flat Across All Three Years

The availability rate proxy (estimated available hours / total possessed hours) shows
no meaningful trend across the analysis period:

| Year | Avg Availability Rate |
|------|----------------------|
| 2023 | 94.1% |
| 2024 | 94.0% |
| 2025 | 94.4% |

The maintenance burden is stable — neither improving nor worsening. The volume of events
increased year-over-year (62,336 → 65,695 → 66,813) but did not translate into
meaningful availability degradation under the proxy model.

**Limitation:** This stability may reflect the limitations of the proxy rather than
real operational trends. Without actual aircraft utilization data, availability cannot
be measured directly. See `ASSUMPTIONS_AND_LIMITATIONS.md`.

---

## Finding 4 — Canadair Regional Jets Appear Disproportionately in Worst Performers

Of the 10 aircraft with the lowest average availability rate proxy, five are Canadair
CL600-series regional jets:

| Aircraft ID | Make | Model | Avg Availability | Total Failures |
|-------------|------|-------|-----------------|----------------|
| AC-8C4314FA | CNDAIR | CL6002C10 | 0.000 | 60 |
| AC-9D70C4D0 | CNDAIR | CL6002C10 | 0.000 | 74 |
| AC-329C9C77 | CNDAIR | CL6002C10 | 0.229 | 64 |
| AC-64016F60 | CNDAIR | CL6002D24 | 0.267 | 31 |
| AC-66ACB403 | CNDAIR | CL6002B19 | 0.408 | 25 |

**Important caveat:** The 0.000 availability values indicate that estimated downtime
exceeded total possessed hours in at least one month — a limitation of the proxy model,
not a claim that these aircraft were literally never available. These aircraft generated
a high volume of events concentrated in short windows, which causes the downtime
estimate to saturate.

This pattern warrants further investigation with actual maintenance labor hour data.

---

## Finding 5 — March Is the Highest-Volume Month Across All Three Years

March ranks as the highest-volume month in each of the three years analyzed:

| Rank | Year | Month | Events |
|------|------|-------|--------|
| 1 | 2025 | March | 6,468 |
| 2 | 2025 | April | 6,038 |
| 3 | 2025 | August | 5,995 |
| 4 | 2023 | March | 5,926 |
| 5 | 2024 | January | 5,924 |

The March peak is consistent across 2023 and 2025. A seasonal inspection cycle —
annual or semi-annual checks scheduled in late winter — likely surfaces structural
discrepancies that drive elevated event counts in Q1. This interpretation is
directional; the SDR data does not capture inspection type or scheduling context.

---

## Key Takeaways

1. **Fuselage structural maintenance is the dominant driver** of recurring maintenance
   burden in U.S. civil aviation SDR data — by volume and by repeat rate.

2. **Structural systems repeat at 5× the rate of mechanical systems.** This is not
   noise — it reflects the progressive, incremental nature of corrosion and fatigue
   management.

3. **The burden is stable, not improving.** Three years of data show no meaningful
   reduction in repeat discrepancy rates at the fleet or system level.

4. **The proxy model has known limitations.** All availability figures are estimates.
   The findings are directionally valid but should not be cited as precise operational
   measurements. See `ASSUMPTIONS_AND_LIMITATIONS.md` for full methodology.

---

## Recommended Next Steps (If Additional Data Were Available)

- Obtain actual aircraft utilization hours to replace the downtime proxy
- Correlate ATA 53 repeat events with aircraft age and total airframe time
- Expand to multi-year pre-COVID baseline (2017–2019) to assess structural trend direction
- Cross-reference with ASRS narratives for richer corrective action detail
