-- Post-load validation for the final SQLite analytics layer

-- Availability proxy must remain between 0 and 1
SELECT
    [Aircraft ID],
    [Date ID],
    [Availability Rate]
FROM fact_readiness
WHERE [Availability Rate] < 0 OR [Availability Rate] > 1;

-- Downtime cannot exceed assumed total monthly hours
SELECT
    [Aircraft ID],
    [Date ID],
    [Downtime Hours],
    [Total Hours]
FROM fact_readiness
WHERE [Downtime Hours] > [Total Hours] + 0.01;

-- Repeat count cannot exceed failure count
SELECT
    [Aircraft ID],
    [Date ID],
    [Repeat Count],
    [Failure Count]
FROM fact_readiness
WHERE [Repeat Count] > [Failure Count];

-- No orphaned aircraft in the monthly fact table
SELECT
    f.[Aircraft ID]
FROM fact_readiness f
LEFT JOIN dim_aircraft a
    ON f.[Aircraft ID] = a.[Aircraft ID]
WHERE a.[Aircraft ID] IS NULL;

-- No orphaned ATA chapters in the event detail table
SELECT
    e.[ATA Chapter]
FROM events_detail e
LEFT JOIN dim_component c
    ON e.[ATA Chapter] = c.[ATA Chapter]
WHERE c.[ATA Chapter] IS NULL;
