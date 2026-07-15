---
paths:
  - "app/queries/**/*.rb"
  - "spec/queries/**/*.rb"
---

# Query Object Conventions

- Single responsibility: one query concern per class
- Accept context via constructor (`account:` or `user:` for multi-tenancy)
- Return `ActiveRecord::Relation` for chainability, or `Hash` for aggregations
- Public method: `#call` with optional filter parameters
- Always use `includes`/`preload`/`eager_load` to prevent N+1 queries
- Never modify data in queries -- read-only
- Sanitize user input: `sanitize_sql_like()`, parameterized queries
- Simple one-liner queries should stay as model scopes
- Test multi-tenant isolation: account A cannot see account B data

## Time-series query objects (timeseries / timeseries_cache DBs)

- Query objects over `Candle`/`Candle{N}m`/`ActiveCandle` select the source MODEL by timeframe (1m -> `Candle`, 2m/3m/5m/15m/30m -> the matching readonly aggregate model) — this cross-source dispatch is the decided pattern (`Candles::HistoryQuery`).
- These models have no associations: `includes`/`preload` do not apply, and joins to `exchanges`/`trading_pairs` are impossible cross-database — filter by denormalized `exchange_code` + `symbol` strings instead.
- Bound results to the most recent N rows (`ORDER BY time DESC LIMIT 500`) and reverse to ascending before returning; serialize `time` as UTC epoch-seconds integers for chart consumers.
- Multi-tenancy does not apply to these query objects in the MVP (no auth).
