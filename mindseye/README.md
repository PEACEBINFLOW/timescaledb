# MindsEye Cognition on TimescaleDB

This directory turns the upstream `timescaledb` extension into a **time-labeled cognition backend** for MindsEye.

Conceptually:

- **TimescaleDB** gives us hypertables, `time_bucket()`, compression, retention.
- **MindsEye** defines a coherent format for **cognitive events**:
  - timestamped
  - actor / source
  - tags and labels
  - arbitrary JSON payload
  - similarity text for search (e.g. pg_trgm)

This folder provides:

- `sql/mindseye_events_schema.sql`  
  → creates the `mindseye_events` hypertable and indexes

- `sql/mindseye_views.sql`  
  → adds useful aggregates and views (last 24h, hourly buckets, actor timelines)

- `api/mindseye_api_example.py`  
  → a minimal reference API showing how to insert and query events

You can use this locally with Docker, bare-metal Postgres, or any Timescale-compatible deployment.

## Quickstart (local dev)

1. Make sure TimescaleDB is installed and enabled in your Postgres instance.

2. Run the MindsEye schema:

```bash
psql "$DATABASE_URL" -f mindseye/sql/mindseye_events_schema.sql
psql "$DATABASE_URL" -f mindseye/sql/mindseye_views.sql
