import os
from typing import List, Optional

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://postgres:password@localhost/postgres",
)

app = FastAPI(title="MindsEye Agentic API (Timescale Fork Demo)")


class MindsEyeEventIn(BaseModel):
    actor_id: Optional[str] = None
    actor_type: Optional[str] = None
    source: Optional[str] = "api"
    channel: Optional[str] = None
    label: Optional[str] = None
    tags: Optional[List[str]] = None
    payload: Optional[dict] = None
    importance: Optional[float] = None
    confidence: Optional[float] = None
    similarity_text: Optional[str] = None


@app.get("/health")
def health():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/events")
def create_event(event: MindsEyeEventIn):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO mindseye_events
                (
                    actor_id, actor_type, source, channel,
                    label, tags, payload, importance,
                    confidence, similarity_text
                )
                VALUES
                (
                    %(actor_id)s, %(actor_type)s, %(source)s, %(channel)s,
                    %(label)s, %(tags)s, %(payload)s, %(importance)s,
                    %(confidence)s, %(similarity_text)s
                )
                RETURNING id, created_at;
                """,
                {
                    "actor_id": event.actor_id,
                    "actor_type": event.actor_type,
                    "source": event.source,
                    "channel": event.channel,
                    "label": event.label,
                    "tags": event.tags or [],
                    "payload": event.payload,
                    "importance": event.importance,
                    "confidence": event.confidence,
                    "similarity_text": event.similarity_text,
                },
            )
            row = cur.fetchone()
            conn.commit()

    return {"id": row[0], "created_at": row[1]}


@app.get("/events/recent")
def list_recent(limit: int = 50):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT *
                FROM mindseye_events_last_24h
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            rows = cur.fetchall()
    return {"events": rows}
