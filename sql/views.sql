-- Analytical views — column names match the Power BI CSV exports

CREATE VIEW IF NOT EXISTS v_fleet_monthly AS
SELECT
    f.Year,
    f.Month,
    d.[Month Label],
    d.Quarter,
    COUNT(DISTINCT f.[Aircraft ID])                                         AS aircraft_count,
    SUM(f.[Failure Count])                                                  AS total_failures,
    SUM(f.[Repeat Count])                                                   AS total_repeats,
    SUM(f.[Downtime Hours])                                                 AS total_downtime_hours,
    ROUND(AVG(f.[Availability Rate]), 4)                                    AS avg_availability_rate,
    ROUND(CAST(SUM(f.[Repeat Count]) AS REAL)
          / NULLIF(SUM(f.[Failure Count]), 0), 4)                          AS fleet_repeat_disc_rate
FROM fact_readiness f
JOIN dim_date d ON f.[Date ID] = d.[Date ID]
GROUP BY f.Year, f.Month;


CREATE VIEW IF NOT EXISTS v_ata_burden AS
SELECT
    c.[ATA Chapter],
    c.[ATA Description],
    c.[System Group],
    COUNT(*)                                                                AS total_events,
    SUM(e.[Is Repeat])                                                      AS repeat_events,
    ROUND(AVG(CAST(e.[Is Repeat] AS REAL)), 4)                             AS repeat_rate
FROM events_detail e
JOIN dim_component c ON e.[ATA Chapter] = c.[ATA Chapter]
GROUP BY c.[ATA Chapter];


CREATE VIEW IF NOT EXISTS v_aircraft_summary AS
SELECT
    f.[Aircraft ID],
    a.Make,
    a.Model,
    ROUND(AVG(f.[Availability Rate]), 4)                                    AS avg_availability_rate,
    ROUND(AVG(f.[Repeat Discrepancy Rate]), 4)                             AS avg_repeat_disc_rate,
    SUM(f.[Failure Count])                                                  AS total_failures,
    SUM(f.[Repeat Count])                                                   AS total_repeats,
    ROUND(SUM(f.[Downtime Hours]), 1)                                       AS total_downtime_hours,
    COUNT(*)                                                                AS reporting_periods
FROM fact_readiness f
JOIN dim_aircraft a ON f.[Aircraft ID] = a.[Aircraft ID]
GROUP BY f.[Aircraft ID];
