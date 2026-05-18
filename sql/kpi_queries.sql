-- KPI Queries for the final SQLite analytics layer

-- Fleet availability proxy by year
SELECT
    Year,
    ROUND(AVG([Availability Rate]), 3) AS avg_availability_proxy
FROM fact_readiness
GROUP BY Year
ORDER BY Year;

-- Lowest-performing aircraft by average availability proxy
SELECT
    [Aircraft ID],
    Make,
    Model,
    avg_availability_rate,
    total_failures,
    total_downtime_hours
FROM v_aircraft_summary
ORDER BY avg_availability_rate ASC
LIMIT 10;

-- ATA chapters with the heaviest recurring burden
SELECT
    [ATA Chapter],
    [ATA Description],
    [System Group],
    total_events,
    repeat_events,
    repeat_rate
FROM v_ata_burden
ORDER BY repeat_events DESC
LIMIT 10;

-- Repeat-discrepancy rate by system group
SELECT
    [System Group],
    COUNT(*) AS total_events,
    SUM([Is Repeat]) AS repeat_events,
    ROUND(AVG(CAST([Is Repeat] AS REAL)), 4) AS repeat_rate
FROM events_detail
GROUP BY [System Group]
ORDER BY repeat_rate DESC;

-- Monthly maintenance trend
SELECT
    Year,
    Month,
    total_failures,
    total_repeats,
    total_downtime_hours,
    avg_availability_rate
FROM v_fleet_monthly
ORDER BY Year, Month;
