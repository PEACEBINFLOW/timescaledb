-- Events in the last 24 hours
CREATE OR REPLACE VIEW mindseye_events_last_24h AS
SELECT *
FROM mindseye_events
WHERE created_at >= NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- Hourly buckets per channel/label
CREATE MATERIALIZED VIEW IF NOT EXISTS mindseye_events_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket(INTERVAL '1 hour', created_at) AS bucket,
    channel,
    label,
    COUNT(*)              AS event_count,
    AVG(importance)       AS avg_importance,
    AVG(confidence)       AS avg_confidence
FROM mindseye_events
GROUP BY bucket, channel, label;

-- Optional: continuous aggregate policy (refresh window)
-- SELECT add_continuous_aggregate_policy(
--     'mindseye_events_hourly',
--     start_offset => INTERVAL '7 days',
--     end_offset   => INTERVAL '1 hour',
--     schedule_interval => INTERVAL '15 minutes'
-- );

-- Simple actor timeline view (per actor_id)
CREATE OR REPLACE VIEW mindseye_actor_timeline AS
SELECT
    actor_id,
    actor_type,
    created_at,
    channel,
    label,
    importance,
    similarity_text
FROM mindseye_events
ORDER BY actor_id, created_at;
