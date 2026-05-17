-- Aircraft Readiness Analytics Schema
-- Modeled after FAA/NTSB public maintenance event reporting conventions.
-- No real military readiness data. All metrics are analytical proxies
-- derived from maintenance event records (similar to FAA SDR / ATA chapter logs).

CREATE TABLE IF NOT EXISTS dim_aircraft (
    aircraft_id     TEXT PRIMARY KEY,       -- synthetic ID (e.g. AC-001)
    aircraft_type   TEXT,                   -- e.g. "Fixed-Wing", "Rotary-Wing"
    model_series    TEXT,                   -- e.g. "Model-A", "Series-3"
    operator_code   TEXT,                   -- anonymized operator
    manufacture_year INTEGER
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id         INTEGER PRIMARY KEY,    -- YYYYMMDD
    date            TEXT,
    year            INTEGER,
    month           INTEGER,
    quarter         INTEGER,
    week_of_year    INTEGER
);

CREATE TABLE IF NOT EXISTS dim_component (
    component_id    TEXT PRIMARY KEY,
    ata_chapter     TEXT,                   -- ATA 100 chapter code (e.g. "32" = Landing Gear)
    ata_description TEXT,
    system_group    TEXT                    -- higher-level grouping (e.g. "Airframe", "Propulsion")
);

CREATE TABLE IF NOT EXISTS fact_maintenance_events (
    event_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    aircraft_id         TEXT REFERENCES dim_aircraft(aircraft_id),
    component_id        TEXT REFERENCES dim_component(component_id),
    date_id             INTEGER REFERENCES dim_date(date_id),
    event_type          TEXT,               -- e.g. "Unscheduled", "Scheduled", "Repeat"
    downtime_hours      REAL,               -- hours aircraft was out of service for this event
    is_repeat           INTEGER DEFAULT 0,  -- 1 if same component failed within 30 days
    corrective_action   TEXT,              -- free-text description of fix
    source_report       TEXT               -- e.g. "FAA-SDR", "ASRS", "Synthetic-Demo"
);

CREATE TABLE IF NOT EXISTS fact_readiness_proxy (
    proxy_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    aircraft_id         TEXT REFERENCES dim_aircraft(aircraft_id),
    date_id             INTEGER REFERENCES dim_date(date_id),
    available_hours     REAL,               -- hours aircraft was available for operations
    total_hours         REAL,               -- total hours in reporting period
    downtime_hours      REAL,               -- sum of maintenance event downtime
    failure_count       INTEGER,            -- number of maintenance events in period
    repeat_count        INTEGER,            -- number of repeat discrepancies in period
    availability_rate   REAL,               -- available_hours / total_hours (readiness proxy)
    repeat_disc_rate    REAL                -- repeat_count / failure_count
);
