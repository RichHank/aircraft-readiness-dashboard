"""
Load all processed CSVs into SQLite and apply schema, views, and validation.

Run from the project root:
    python sql/load_db.py

Creates: data/processed/readiness.db
"""
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH      = Path("data/processed/readiness.db")
PROCESSED    = Path("data/processed")
SQL_DIR      = Path("sql")


TABLES = {
    "dim_aircraft":       "powerbi_dim_aircraft.csv",
    "dim_date":           "powerbi_dim_date.csv",
    "dim_component":      "powerbi_dim_component.csv",
    "fact_readiness":     "powerbi_fact_readiness.csv",
    "events_detail":      "powerbi_events_detail.csv",
}


def load_tables(conn: sqlite3.Connection):
    for table, filename in TABLES.items():
        path = PROCESSED / filename
        df = pd.read_csv(path, low_memory=False)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"  Loaded {table:25s} {len(df):>8,} rows")


def apply_sql_file(conn: sqlite3.Connection, path: Path):
    sql = path.read_text(encoding="utf-8")
    # Split on semicolons, skip blanks and comments
    statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]
    for stmt in statements:
        try:
            conn.execute(stmt)
        except sqlite3.Error as e:
            print(f"  WARNING: {e}\n  Statement: {stmt[:80]}...")
    conn.commit()


def run_kpis(conn: sqlite3.Connection):
    queries = {
        "Fleet availability rate (all years)": """
            SELECT Year, ROUND(AVG([Availability Rate]), 3) AS avg_availability
            FROM fact_readiness
            GROUP BY Year
            ORDER BY Year
        """,
        "Top 10 ATA chapters by repeat events": """
            SELECT [ATA Chapter], [ATA Description], [System Group],
                   COUNT(*) AS total_events,
                   SUM([Is Repeat]) AS repeat_events,
                   ROUND(AVG(CAST([Is Repeat] AS REAL)), 3) AS repeat_rate
            FROM events_detail
            GROUP BY [ATA Chapter]
            ORDER BY repeat_events DESC
            LIMIT 10
        """,
        "Worst 10 aircraft by availability rate": """
            SELECT f.[Aircraft ID], a.Make, a.Model,
                   ROUND(AVG(f.[Availability Rate]), 3) AS avg_availability,
                   SUM(f.[Failure Count]) AS total_failures,
                   ROUND(SUM(f.[Downtime Hours]), 0) AS total_downtime
            FROM fact_readiness f
            JOIN dim_aircraft a ON f.[Aircraft ID] = a.[Aircraft ID]
            GROUP BY f.[Aircraft ID]
            ORDER BY avg_availability ASC
            LIMIT 10
        """,
        "Repeat discrepancy rate by system group": """
            SELECT [System Group],
                   COUNT(*) AS total_events,
                   SUM([Is Repeat]) AS repeat_events,
                   ROUND(AVG(CAST([Is Repeat] AS REAL)), 3) AS repeat_rate
            FROM events_detail
            GROUP BY [System Group]
            ORDER BY repeat_rate DESC
        """,
        "Monthly event trend 2023-2025": """
            SELECT Year, Month, SUM([Failure Count]) AS events
            FROM fact_readiness
            GROUP BY Year, Month
            ORDER BY Year, Month
            LIMIT 12
        """,
    }

    print("\n" + "="*60)
    print("KPI VALIDATION")
    print("="*60)

    for title, sql in queries.items():
        print(f"\n--- {title} ---")
        try:
            df = pd.read_sql_query(sql, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"  ERROR: {e}")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing {DB_PATH}")

    print(f"Creating {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)

    print("\nLoading tables...")
    load_tables(conn)

    print("\nApplying views...")
    apply_sql_file(conn, SQL_DIR / "views.sql")
    print("  views.sql applied")

    run_kpis(conn)

    conn.close()
    print(f"\nDatabase ready: {DB_PATH}")


if __name__ == "__main__":
    main()
