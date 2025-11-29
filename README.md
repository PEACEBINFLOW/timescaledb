## MindsEye Cognition Layer (Fork Note)

This fork of `timescaledb` is used as the storage and time engine for **MindsEye Cognition** — a time-labeled event layer for agentic systems.

On top of the core TimescaleDB extension, this fork adds:

- A **MindsEye schema** (`mindseye/sql/mindseye_events_schema.sql`)  
- **Cognitive aggregates & views** (`mindseye/sql/mindseye_views.sql`)  
- A small **reference API example** (`mindseye/api/mindseye_api_example.py`)  

These additions are *additive only*: they don’t modify the TimescaleDB extension itself.  
You can still pull upstream changes from `timescale/timescaledb`, while using this fork as:

- the storage backend for **MindsEye Agentic** (time-labeled cognitive events), and  
- a lab for time-aware AI systems using hypertables, `time_bucket()`, and similarity search.
