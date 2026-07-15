# Multi-Database Configuration (PostgreSQL + TimescaleDB)

This app uses one PostgreSQL server with multiple logical databases:

| Connection | Database (dev) | Engine | Purpose |
|------------|----------------|--------|---------|
| `primary` | `plus_development` | PostgreSQL | Relational data: `users`, `exchanges`, `api_credentials`, `trading_pairs` |
| `timeseries` | `plus_timeseries_development` | PostgreSQL + TimescaleDB | Closed 1m candles hypertable (`candles`) + continuous aggregates (2m/3m/5m/15m/30m) |
| `timeseries_cache` | `plus_timeseries_cache_development` | PostgreSQL + TimescaleDB | Rolling window of recent 1m candles (`active_candles`) for chart broadcasting |
| `queue` / `cache` / `cable` | `plus_*_{queue,cache,cable}` | PostgreSQL | Solid Queue / Solid Cache / Solid Cable (production by default; `queue` also needed in development to run the candle ingestion jobs) |

Rules that follow from this topology:

- **No cross-database foreign keys or JOINs.** Time-series tables denormalize
  `exchange_code` and `symbol` as plain strings. Joins against `exchanges` /
  `trading_pairs` happen in the service layer.
- **Continuous aggregates must live in the same database as their source
  hypertable** — all aggregates live in `timeseries`. Never define continuous
  aggregates in `timeseries_cache`.
- **Dual-writes across `timeseries` and `timeseries_cache` are not atomic.**
  Every step must be an idempotent upsert (`ON CONFLICT`) so a failed step is
  repaired by the REST backfill that runs on the next stream (re)connect.

## config/database.yml

```yaml
default: &default
  adapter: postgresql
  encoding: unicode
  max_connections: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>

development:
  primary:
    <<: *default
    database: plus_development
  timeseries:
    <<: *default
    database: plus_timeseries_development
    migrations_paths: db/timeseries_migrate
  timeseries_cache:
    <<: *default
    database: plus_timeseries_cache_development
    migrations_paths: db/timeseries_cache_migrate
  queue:
    <<: *default
    database: plus_development_queue
    migrations_paths: db/queue_migrate
  cable:
    <<: *default
    database: plus_development_cable
    migrations_paths: db/cable_migrate

test:
  primary:
    <<: *default
    database: plus_test
  timeseries:
    <<: *default
    database: plus_timeseries_test
    migrations_paths: db/timeseries_migrate
  timeseries_cache:
    <<: *default
    database: plus_timeseries_cache_test
    migrations_paths: db/timeseries_cache_migrate
  queue:
    <<: *default
    database: plus_test_queue
    migrations_paths: db/queue_migrate

production:
  primary: &primary_production
    <<: *default
    database: plus_production
    username: plus
    password: <%= ENV["PLUS_DATABASE_PASSWORD"] %>
  timeseries:
    <<: *primary_production
    database: plus_timeseries_production
    migrations_paths: db/timeseries_migrate
  timeseries_cache:
    <<: *primary_production
    database: plus_timeseries_cache_production
    migrations_paths: db/timeseries_cache_migrate
  cache:
    <<: *primary_production
    database: plus_production_cache
    migrations_paths: db/cache_migrate
  queue:
    <<: *primary_production
    database: plus_production_queue
    migrations_paths: db/queue_migrate
  cable:
    <<: *primary_production
    database: plus_production_cable
    migrations_paths: db/cable_migrate
```

## Abstract connection classes

```ruby
# app/models/timeseries_record.rb
class TimeseriesRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to database: { writing: :timeseries, reading: :timeseries }
end

# app/models/timeseries_cache_record.rb
class TimeseriesCacheRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to database: { writing: :timeseries_cache, reading: :timeseries_cache }
end
```

`Candle` and `Candle{2,3,5,15,30}m` inherit from `TimeseriesRecord`
(aggregate-backed models declare `def readonly? = true`). `ActiveCandle`
inherits from `TimeseriesCacheRecord`. Everything else inherits from
`ApplicationRecord` (primary).

## Schema format

TimescaleDB objects (hypertables, continuous aggregates, retention/refresh
policies) cannot be represented in `schema.rb`:

```ruby
# config/application.rb
config.active_record.schema_format = :sql
```

Each database dumps its own `structure.sql` (`db/timeseries_structure.sql`,
etc. — Rails derives the filename from the connection name).

## TimescaleDB bootstrap

The first migration in `db/timeseries_migrate/` and
`db/timeseries_cache_migrate/` must enable the extension:

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

Hypertable notes:

- Unique indexes on hypertables **must include the partition column** (`time`).
- `add_retention_policy()` requires the table to be a hypertable —
  `active_candles` is therefore created as a hypertable even though it is small.
- `interval` is a PostgreSQL keyword (type name); quote it as `"interval"` in
  raw SQL to avoid parser ambiguity with typed literals like `INTERVAL '5 min'`.

## Development runtime for background jobs

Production already runs Solid Queue (`config/environments/production.rb`).
To run the candle ingestion jobs (`LiveCandleStreamJob`,
`LiveCandleStreamSupervisorJob`) in development:

1. `config/environments/development.rb`:
   `config.active_job.queue_adapter = :solid_queue` and
   `config.solid_queue.connects_to = { database: { writing: :queue } }`
2. Add the `queue` entry to `development:` in `config/database.yml` (above).
3. Add a jobs process to `Procfile.dev`: `jobs: bin/jobs`
4. Because the streaming consumer broadcasts from a separate process, the
   async cable adapter (in-process only) will not deliver to browsers — switch
   `config/cable.yml` development to `solid_cable`, backed by the `cable`
   database entry shown above. The async adapter is only viable in
   single-process setups where the ingestion job runs inside the web process.
5. The long-running `LiveCandleStreamJob` uses a dedicated `streaming` queue —
   add a `streaming` worker entry to `config/queue.yml` so it does not occupy
   the default-queue workers.

## Commands

```bash
bin/rails db:prepare                          # creates + migrates all configured databases
bin/rails db:migrate:timeseries               # migrate one database
bin/rails db:migrate:timeseries_cache
bin/rails db:migrate:status                   # per-database status
```
