---
name: postgres-patterns
description: PostgreSQL and TimescaleDB schema, indexing, and financial time-series patterns. Use when designing single-database architectures that mix regular PostgreSQL ACID tables with TimescaleDB hypertables, real-time tick ingestion, OHLC/candlestick rollups, continuous aggregates, retention/compression policies, query optimization, migrations, RLS/security, or connection pooling.
---

# PostgreSQL Patterns

Use this skill to keep transactional business data and financial time-series data in one PostgreSQL database without mixing their responsibilities.

> **PROJECT OVERRIDE (PLUS — decided, do not contest):** this app does NOT use the single-database layout below. It runs three logical databases (`primary` PostgreSQL-only; `timeseries` and `timeseries_cache` with TimescaleDB) — see `docs/multi-db-config.md` and `docs/features/01.mvp-binance-realtime-chart.md` 4-A. Ingestion is Binance 1m klines (no raw tick table, no `@trade` streams). Candles are `decimal(20,8)` and higher timeframes (2m/3m/5m/15m/30m) are plain continuous aggregates using `first/max/min/last/sum` — `timescaledb_toolkit`, `candlestick_agg`, `rollup`, and float price columns are NOT used. Cross-database FKs/joins are impossible: `exchange_code`/`symbol` are denormalized strings. Continuous aggregates live only in `timeseries` (same DB as the `candles` hypertable), never in `timeseries_cache`. Where this note conflicts with the generic patterns below, this note wins.

## Core Split

Use regular PostgreSQL tables for state that requires strict transactional correctness:

- Users, sessions, credentials, roles, and authorization state
- Accounts, balances, ledgers, deposits, withdrawals, and transfers
- Orders, executions, positions, portfolios, allocations, and audit logs
- Reference data that changes slowly, such as instruments, exchanges, and trading calendars

Use TimescaleDB hypertables for append-heavy time-series facts:

- Raw WebSocket ticks, quotes, trades, and 1-minute market observations
- Derived candle source data used for charts and market analytics
- Data that is queried by time range and instrument, then rolled up into larger buckets

Do not store balances, orders, or portfolio state in hypertables just because they contain timestamps. They are business state first and time-series data second.

## Rails Setup Checklist

1. Use one PostgreSQL database and enable TimescaleDB in that database.
2. Set `config.active_record.schema_format = :sql`; `schema.rb` cannot faithfully represent extensions, hypertables, continuous aggregates, and policies.
3. Keep Rails models for regular tables idiomatic: validations, foreign keys, constraints, and transactional service methods.
4. Use raw SQL inside migrations for TimescaleDB objects. Make migrations reversible by explicitly dropping policies, materialized views, indexes, and hypertables.
5. Keep chart ingestion idempotent. Use deterministic conflict keys, and ensure hypertable unique indexes include the time partition column.

## Extension Migration

```ruby
class EnableTimescale < ActiveRecord::Migration[8.1]
  def change
    enable_extension "timescaledb"
    enable_extension "timescaledb_toolkit"
  end
end
```

Use `timescaledb_toolkit` when the design relies on `candlestick_agg`, `rollup`, `open`, `high`, `low`, `close`, `volume`, or `vwap`.

## Regular Table Pattern

```ruby
create_table :accounts do |t|
  t.references :user, null: false, foreign_key: true
  t.decimal :cash_balance, precision: 28, scale: 10, null: false, default: "0"
  t.string :currency, null: false
  t.timestamps
end

add_check_constraint :accounts, "cash_balance >= 0", name: "accounts_cash_balance_nonnegative"
add_index :accounts, [:user_id, :currency], unique: true
```

Use `numeric`/`decimal` for authoritative money, balances, prices in orders, and ledger amounts. Use Rails transactions and row locks for state transitions.

## Tick Hypertable Pattern

Prefer a narrow append-only table for chart ticks. Store rich metadata in regular tables and join it at query boundaries, not inside the base aggregation path.

```ruby
class CreateMarketTicks < ActiveRecord::Migration[8.1]
  def up
    create_table :market_ticks, id: false do |t|
      t.references :instrument, null: false, foreign_key: true, type: :bigint
      t.datetime :time, null: false
      t.float :price, null: false
      t.float :volume, null: false
      t.text :source, null: false
      t.bigint :sequence, null: false
    end

    execute <<~SQL
      ALTER TABLE market_ticks
      ADD CONSTRAINT market_ticks_pk
      PRIMARY KEY (instrument_id, time, source, sequence);

      SELECT create_hypertable(
        'market_ticks',
        'time',
        chunk_time_interval => INTERVAL '1 day',
        if_not_exists => TRUE
      );
    SQL

    add_index :market_ticks, [:instrument_id, :time], order: { time: :desc }
  end

  def down
    drop_table :market_ticks
  end
end
```

`candlestick_agg` requires `double precision` values, so Rails `float` is appropriate for analytical chart ticks. Keep authoritative trading and accounting values in `decimal`.

## 1-Minute Candle Continuous Aggregate

Store the intermediate candlestick object in the continuous aggregate. Apply accessors in read views or chart queries.

```sql
CREATE MATERIALIZED VIEW market_candles_1m
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('1 minute', time) AS bucket,
  instrument_id,
  candlestick_agg(time, price, volume) AS candle
FROM market_ticks
GROUP BY 1, instrument_id
WITH NO DATA;

CREATE VIEW market_candles_1m_ohlcv AS
SELECT
  bucket,
  instrument_id,
  open(candle) AS open,
  high(candle) AS high,
  low(candle) AS low,
  close(candle) AS close,
  volume(candle) AS volume,
  vwap(candle) AS vwap
FROM market_candles_1m;
```

Set `timescaledb.materialized_only = false` for live chart views that need the newest raw rows merged with materialized buckets.

## Higher-Timeframe Candle Pattern

Build 2-minute, 4-minute, 5-minute, daily, weekly, and monthly candles by rolling up the 1-minute candlestick aggregate. This avoids recalculating OHLC from raw ticks for every timeframe.

```sql
CREATE MATERIALIZED VIEW market_candles_2m
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('2 minutes', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1m
GROUP BY 1, instrument_id
WITH NO DATA;

CREATE MATERIALIZED VIEW market_candles_4m
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('4 minutes', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1m
GROUP BY 1, instrument_id
WITH NO DATA;

CREATE MATERIALIZED VIEW market_candles_5m
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('5 minutes', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1m
GROUP BY 1, instrument_id
WITH NO DATA;
```

Use the same pattern for calendar buckets:

```sql
CREATE MATERIALIZED VIEW market_candles_1d
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('1 day', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1m
GROUP BY 1, instrument_id
WITH NO DATA;

CREATE MATERIALIZED VIEW market_candles_1w
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('1 week', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1d
GROUP BY 1, instrument_id
WITH NO DATA;

CREATE MATERIALIZED VIEW market_candles_1mo
WITH (
  timescaledb.continuous,
  timescaledb.materialized_only = false
) AS
SELECT
  time_bucket('1 month', bucket) AS bucket,
  instrument_id,
  rollup(candle) AS candle
FROM market_candles_1d
GROUP BY 1, instrument_id
WITH NO DATA;
```

Confirm whether daily, weekly, and monthly candles should follow UTC calendar buckets, exchange-local calendar days, or official exchange sessions. If session calendars are required, model sessions as regular tables and use a purpose-built session bucketing strategy instead of assuming `time_bucket('1 day', ...)` is sufficient.

## Refresh Policies

Add continuous aggregate policies after creating each materialized view.

```sql
SELECT add_continuous_aggregate_policy(
  'market_candles_1m',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 minute',
  schedule_interval => INTERVAL '30 seconds'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_2m',
  start_offset => INTERVAL '1 day',
  end_offset => INTERVAL '2 minutes',
  schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_4m',
  start_offset => INTERVAL '1 day',
  end_offset => INTERVAL '4 minutes',
  schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_5m',
  start_offset => INTERVAL '1 day',
  end_offset => INTERVAL '5 minutes',
  schedule_interval => INTERVAL '1 minute'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_1d',
  start_offset => INTERVAL '90 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '5 minutes'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_1w',
  start_offset => INTERVAL '2 years',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 hour'
);

SELECT add_continuous_aggregate_policy(
  'market_candles_1mo',
  start_offset => INTERVAL '10 years',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 hour'
);
```

Use wider `start_offset` values when late ticks or exchange corrections are expected. Keep `end_offset` at least one bucket behind live ingestion and use real-time aggregates for the active bucket.

For backfills or repaired historical ticks, call `refresh_continuous_aggregate` over the corrected time range rather than waiting for the regular policy.

Hierarchical continuous aggregates require TimescaleDB 2.9+. If a deployment is older, create each timeframe directly from `market_ticks` or upgrade before relying on rollups from `market_candles_1m`.

## Real-Time Chart Reads

Use stable database views for chart endpoints:

```sql
CREATE VIEW market_candles_5m_ohlcv AS
SELECT
  bucket,
  instrument_id,
  open(candle) AS open,
  high(candle) AS high,
  low(candle) AS low,
  close(candle) AS close,
  volume(candle) AS volume,
  vwap(candle) AS vwap
FROM market_candles_5m;
```

In Rails, query these views through query objects or readonly models. Keep instrument names, exchange metadata, and user-specific watchlist state outside continuous aggregates; join them in the final query or in presenters.

## Indexing Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Hypertable time ranges | Composite or BRIN | `CREATE INDEX idx ON ticks (instrument_id, time DESC)` |

Use composite indexes in equality-then-range order:

```sql
CREATE INDEX idx_orders_status_created_at ON orders (status, created_at);
CREATE INDEX idx_market_ticks_instrument_time ON market_ticks (instrument_id, time DESC);
```

For hypertables, every unique index must include the partitioning time column.

## Data Type Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| Rails IDs | `bigint` | `int` |
| User text | `text` | `varchar(255)` by habit |
| Time-series time | `timestamptz` | `timestamp` |
| Money and balances | `numeric` / Rails `decimal` | `float` |
| Toolkit chart price input | `double precision` / Rails `float` | `numeric` if using `candlestick_agg` directly |
| Flags | `boolean` | `varchar`, `int` |

## Retention And Compression

Keep raw ticks only as long as replay, audit, correction, and re-aggregation requirements demand. Keep continuous aggregates longer than raw ticks when charts need long history.

```sql
SELECT add_retention_policy('market_ticks', INTERVAL '90 days');

ALTER TABLE market_ticks SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'instrument_id',
  timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('market_ticks', INTERVAL '7 days');
```

Do not drop raw ticks before the business has accepted the loss of exact replay and historical correction ability.

## Operational Verification

Use these checks after migrations:

```sql
SELECT hypertable_name
FROM timescaledb_information.hypertables
WHERE hypertable_name = 'market_ticks';

SELECT view_name, materialized_only
FROM timescaledb_information.continuous_aggregates
WHERE view_name LIKE 'market_candles_%';

SELECT *
FROM timescaledb_information.jobs
WHERE proc_name = 'policy_refresh_continuous_aggregate';
```

For Rails tests, verify:

- The migration creates the hypertable and continuous aggregates.
- The chart endpoint returns OHLCV rows ordered by `bucket`.
- Late-arriving ticks are handled by refresh policy or explicit refresh.
- WebSocket ingestion is idempotent under duplicate tick delivery.
- Regular business writes remain transactional and are not coupled to chart aggregation jobs.

## Common PostgreSQL Patterns

**Covering index**

```sql
CREATE INDEX idx_users_email_include_name ON users (email) INCLUDE (name, created_at);
```

**Partial index**

```sql
CREATE INDEX idx_users_active_email ON users (email) WHERE deleted_at IS NULL;
```

**Optimized RLS policy**

```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);
```

**UPSERT**

```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Queue processing**

```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

## Anti-Patterns

- Use a hypertable for mutable balances, order state, or portfolios.
- Compute OHLC candles in Ruby for every request when TimescaleDB can maintain rollups.
- Store only final OHLC rows when raw ticks must be replayed, corrected, or re-aggregated.
- Put mutable dimension-table joins inside continuous aggregates unless version support and invalidation behavior are understood.
- Forget `timescaledb.materialized_only = false` for live chart views on TimescaleDB 2.13+.
- Add a unique index to a hypertable that omits the partitioning time column.
- Use `schema.rb` for a Rails app that depends on TimescaleDB objects.

## Related

- Agent: `database-reviewer` - Full database review workflow
- Skill: `performance-optimization` - Query performance and N+1 analysis
- Skill: `lightweight-chart-agent` - TradingView Lightweight Charts integration
