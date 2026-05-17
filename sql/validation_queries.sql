-- Post-ETL data validation

-- Availability rate must be between 0 and 1
SELECT aircraft_id, date_id, availability_rate
FROM fact_readiness_proxy
WHERE availability_rate < 0 OR availability_rate > 1;

-- Downtime cannot exceed total hours in period
SELECT aircraft_id, date_id, downtime_hours, total_hours
FROM fact_readiness_proxy
WHERE downtime_hours > total_hours + 0.01;

-- Repeat count cannot exceed failure count
SELECT aircraft_id, date_id, repeat_count, failure_count
FROM fact_readiness_proxy
WHERE repeat_count > failure_count;

-- No negative downtime on individual events
SELECT event_id, aircraft_id, downtime_hours
FROM fact_maintenance_events
WHERE downtime_hours < 0 OR downtime_hours IS NULL;

-- Orphaned events (no matching aircraft)
SELECT e.aircraft_id
FROM fact_maintenance_events e
LEFT JOIN dim_aircraft a ON e.aircraft_id = a.aircraft_id
WHERE a.aircraft_id IS NULL;

-- Orphaned events (no matching component)
SELECT e.component_id
FROM fact_maintenance_events e
LEFT JOIN dim_component c ON e.component_id = c.component_id
WHERE c.component_id IS NULL;
