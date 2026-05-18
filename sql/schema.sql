-- Reference schema for the final analyst-facing tables loaded by sql/load_db.py.
-- The loader imports Power BI-ready CSV exports with the same column names shown here.

CREATE TABLE IF NOT EXISTS dim_aircraft (
    [Aircraft ID]      TEXT PRIMARY KEY,
    [Make]             TEXT,
    [Model]            TEXT,
    [First Seen Year]  INTEGER,
    [Last Seen Year]   INTEGER,
    [Total Events]     INTEGER
);

CREATE TABLE IF NOT EXISTS dim_date (
    [Year]          INTEGER,
    [Month Number]  INTEGER,
    [Date ID]       INTEGER PRIMARY KEY,
    [Quarter]       INTEGER,
    [Month Label]   TEXT
);

CREATE TABLE IF NOT EXISTS dim_component (
    [Component ID]     TEXT PRIMARY KEY,
    [ATA Chapter]      TEXT,
    [ATA Description]  TEXT,
    [System Group]     TEXT
);

CREATE TABLE IF NOT EXISTS fact_readiness (
    [Aircraft ID]               TEXT,
    [Date ID]                   INTEGER,
    [Year]                      INTEGER,
    [Month]                     INTEGER,
    [Failure Count]             INTEGER,
    [Repeat Count]              INTEGER,
    [Downtime Hours]            REAL,
    [Top ATA Chapter]           TEXT,
    [Top System Group]          TEXT,
    [Total Hours]               REAL,
    [Available Hours]           REAL,
    [Availability Rate]         REAL,
    [Repeat Discrepancy Rate]   REAL
);

CREATE TABLE IF NOT EXISTS events_detail (
    [Aircraft ID]             TEXT,
    [Event Date]              TEXT,
    [Year]                    INTEGER,
    [ATA Chapter]             TEXT,
    [ATA Description]         TEXT,
    [System Group]            TEXT,
    [Condition]               TEXT,
    [Part Condition]          TEXT,
    [Part Name]               TEXT,
    [Make]                    TEXT,
    [Model]                   TEXT,
    [Is Repeat]               INTEGER,
    [Days Since Last Event]   REAL,
    [Stage of Operation]      TEXT,
    [How Discovered]          TEXT
);
