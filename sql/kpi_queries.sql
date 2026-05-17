-- KPI Queries

-- Fleet availability rate (current month)
SELECT fleet_availability_rate, fleet_repeat_disc_rate, total_failure_count
FROM v_fleet_availability_monthly
WHERE year = strftime('%Y', 'now')
  AND month = CAST(strftime('%m', 'now') AS INTEGER);


-- Aircraft with availability rate below threshold (e.g. < 0.80)
SELECT aircraft_id, model_series, operator_code,
       avg_availability_rate, total_downtime_hours, total_failures
FROM v_aircraft_summary
WHERE avg_availability_rate < 0.80
ORDER BY avg_availability_rate ASC;


-- Top 10 highest-downtime components (failure trend leaders)
SELECT ata_chapter, ata_description, system_group,
       total_events, total_downtime_hours, repeat_rate
FROM v_component_failure_trends
ORDER BY total_downtime_hours DESC
LIMIT 10;


-- Repeat discrepancy rate by system group
SELECT
    c.system_group,
    COUNT(*)                                                AS total_events,
    SUM(e.is_repeat)                                        AS repeat_events,
    ROUND(SUM(e.is_repeat) / NULLIF(CAST(COUNT(*) AS REAL), 0), 4) AS repeat_disc_rate
FROM fact_maintenance_events e
JOIN dim_component c ON e.component_id = c.component_id
GROUP BY c.system_group
ORDER BY repeat_disc_rate DESC;


-- Monthly downtime trend
SELECT d.year, d.month,
       SUM(e.downtime_hours)   AS monthly_downtime_hours,
       COUNT(*)                AS event_count
FROM fact_maintenance_events e
JOIN dim_date d ON e.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
