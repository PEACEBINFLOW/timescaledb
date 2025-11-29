TimescaleDB is a PostgreSQL extension for high-performance real-time analytics on time-series and event data
Docs SLACK Try TimescaleDB for free

Install TimescaleDB
Install from a Docker container:

Run the TimescaleDB container:

docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg17
Connect to a database:

docker exec -it timescaledb psql -d "postgres://postgres:password@localhost/postgres"
See other installation options or try Tiger Cloud for free.

Create a hypertable
TimescaleDB's hypercore is a hybrid row-columnar store that boosts analytical query performance on your time-series and event data, while reducing data size by more than 90%. This keeps your analytics operating at lightning speed and ensures low storage costs as you scale. Data is inserted in row format in the rowstore and converted to columnar format in the columnstore based on your configuration.

-- Create a hypertable, with the columnstore from the hypercore engine
-- "time" as partitioning column and a segment by on location
CREATE TABLE conditions (
  time        TIMESTAMPTZ       NOT NULL,
  location    TEXT              NOT NULL,
  temperature DOUBLE PRECISION  NULL,
  humidity    DOUBLE PRECISION  NULL
)
WITH (
  timescaledb.hypertable,
  timescaledb.partition_column='time',
  timescaledb.segmentby='location'
);
See more:

About hypertables
API reference
About columnstore
Enable columnstore manually
API reference
Insert and query data
Insert and query data in a hypertable via regular SQL commands. For example:

Insert data into a hypertable named conditions:

INSERT INTO conditions
  VALUES
    (NOW(), 'office',   70.0, 50.0),
    (NOW(), 'basement', 66.5, 60.0),
    (NOW(), 'garage',   77.0, 65.2);
Return the number of entries written to the table conditions in the last 12 hours:

SELECT
  COUNT(*)
FROM
  conditions
WHERE
  time > NOW() - INTERVAL '12 hours';
See more:

Query data
Write data
Create time buckets
Time buckets enable you to aggregate data in hypertables by time interval and calculate summary values.

For example, calculate the average daily temperature in a table named conditions. The table has a time and temperature columns:

SELECT
  time_bucket('1 day', time) AS bucket,
  AVG(temperature) AS avg_temp
FROM
  conditions
GROUP BY
  bucket
ORDER BY
  bucket ASC;
See more:

About time buckets
API reference
All TimescaleDB features
Tutorials
Create continuous aggregates
Continuous aggregates make real-time analytics run faster on very large datasets. They continuously and incrementally refresh a query in the background, so that when you run such query, only the data that has changed needs to be computed, not the entire dataset. This is what makes them different from regular PostgreSQL materialized views, which cannot be incrementally materialized and have to be rebuilt from scratch every time you want to refresh it.

For example, create a continuous aggregate view for daily weather data in two simple steps:

Create a materialized view:

CREATE MATERIALIZED VIEW conditions_summary_daily
WITH (timescaledb.continuous) AS
SELECT
  location,
  time_bucket(INTERVAL '1 day', time) AS bucket,
  AVG(temperature),
  MAX(temperature),
  MIN(temperature)
FROM
  conditions
GROUP BY
  location,
  bucket;
Create a policy to refresh the view every hour:

SELECT
  add_continuous_aggregate_policy(
    'conditions_summary_daily',
    start_offset => INTERVAL '1 month',
    end_offset => INTERVAL '1 day',
    schedule_interval => INTERVAL '1 hour'
);
See more:

About continuous aggregates
API reference
Want TimescaleDB hosted and managed for you? Try Tiger Cloud
Tiger Cloud is the modern PostgreSQL data platform for all your applications. It enhances PostgreSQL to handle time series, events, real-time analytics, and vector search—all in a single database alongside transactional workloads. You get one system that handles live data ingestion, late and out-of-order updates, and low latency queries, with the performance, reliability, and scalability your app needs. Ideal for IoT, crypto, finance, SaaS, and a myriad other domains, Tiger Cloud allows you to build data-heavy, mission-critical apps while retaining the familiarity and reliability of PostgreSQL. See our whitepaper for a deep dive into Tiger Cloud's architecture and how it meets the needs of even the most demanding applications.

A Tiger Cloud service is a single optimized 100% PostgreSQL database instance that you use as is, or extend with capabilities specific to your business needs. The available capabilities are:

Time-series and analytics: PostgreSQL with TimescaleDB. The PostgreSQL you know and love, supercharged with functionality for storing and querying time-series data at scale for real-time analytics and other use cases. Get faster time-based queries with hypertables, continuous aggregates, and columnar storage. Save on storage with native compression, data retention policies, and bottomless data tiering to Amazon S3.
AI and vector: PostgreSQL with vector extensions. Use PostgreSQL as a vector database with purpose built extensions for building AI applications from start to scale. Get fast and accurate similarity search with the pgvector and pgvectorscale extensions. Create vector embeddings and perform LLM reasoning on your data with the pgai extension.
PostgreSQL: the trusted industry-standard RDBMS. Ideal for applications requiring strong data consistency, complex relationships, and advanced querying capabilities. Get ACID compliance, extensive SQL support, JSON handling, and extensibility through custom functions, data types, and extensions. All services include all the cloud tooling you'd expect for production use: automatic backups, high availability, read replicas, data forking, connection pooling, tiered storage, usage-based storage, and much more.
Check build status
Linux/macOS	Linux i386	Windows	Coverity	Code Coverage	OpenSSF
Build Status Linux/macOS	Build Status Linux i386	Windows build status	Coverity Scan Build Status	Code Coverage	OpenSSF Best Practices
Get involved
We welcome contributions to TimescaleDB! See Contributing and Code style guide for details.

Learn about TigerData
TigerData is the fastest PostgreSQL for transactional, analytical and agentic workloads. To learn more about the company and its products, visit tigerdata.com.
