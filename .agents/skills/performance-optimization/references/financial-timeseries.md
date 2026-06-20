# Financial Time-Series Performance Patterns

Use these patterns when a Rails endpoint feeds TradingView Lightweight Charts from PostgreSQL/TimescaleDB.

## Endpoint Rules

- Query readonly OHLCV views backed by continuous aggregates.
- Always require `instrument_id`, `timeframe`, `from`, and `to` for historical loads.
- Return only chart columns: `time`, `open`, `high`, `low`, `close`, and optional `volume`.
- Convert intraday `bucket` values to UTC seconds for Lightweight Charts.
- Cap result count per request; use visible-range pagination for history.
- Join instrument metadata outside the continuous aggregate path.

```ruby
class Charts::CandlesQuery
  TIMEFRAME_VIEWS = {
    "1m" => "market_candles_1m_ohlcv",
    "2m" => "market_candles_2m_ohlcv",
    "4m" => "market_candles_4m_ohlcv",
    "5m" => "market_candles_5m_ohlcv",
    "1d" => "market_candles_1d_ohlcv",
    "1w" => "market_candles_1w_ohlcv",
    "1mo" => "market_candles_1mo_ohlcv"
  }.freeze

  def self.call(instrument_id:, timeframe:, from:, to:, limit: 2_000)
    view_name = TIMEFRAME_VIEWS.fetch(timeframe)

    ActiveRecord::Base.connection.exec_query(
      <<~SQL.squish,
        SELECT
          EXTRACT(EPOCH FROM bucket)::bigint AS time,
          open,
          high,
          low,
          close,
          volume
        FROM #{view_name}
        WHERE instrument_id = $1
          AND bucket >= $2
          AND bucket < $3
        ORDER BY bucket ASC
        LIMIT $4
      SQL
      "Charts::CandlesQuery",
      [
        [nil, instrument_id],
        [nil, from],
        [nil, to],
        [nil, limit]
      ]
    )
  end
end
```

Only interpolate `view_name` from a frozen allowlist. Bind all user-provided values.

## Database Checks

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT bucket, open, high, low, close, volume
FROM market_candles_5m_ohlcv
WHERE instrument_id = 42
  AND bucket >= now() - INTERVAL '7 days'
ORDER BY bucket ASC
LIMIT 2000;

SELECT view_name, materialized_only
FROM timescaledb_information.continuous_aggregates
WHERE view_name LIKE 'market_candles_%';

SELECT *
FROM timescaledb_information.jobs
WHERE proc_name = 'policy_refresh_continuous_aggregate';
```

Look for large raw tick scans, missing time/instrument filters, sort spills, and disabled refresh jobs.

## Real-Time Update Tuning

- Broadcast the current bucket candle, not every raw tick, unless the UI explicitly needs tick-by-tick display.
- Throttle outbound chart updates to a practical interval, commonly 100-500ms.
- Use Lightweight Charts `series.update()` for live candles.
- Use `setData()` only for initial loads, timeframe changes, or visible-range replacement.
- Keep Turbo Stream payloads small; send one candle update per instrument/timeframe whenever possible.

## Continuous Aggregate Pitfalls

- Missing `timescaledb.materialized_only = false` can hide the newest bucket on TimescaleDB 2.13+.
- Narrow refresh windows can miss late ticks or exchange corrections.
- Historical backfills require explicit `refresh_continuous_aggregate` over the affected range.
- Daily, weekly, and monthly candles may need exchange-session calendars; UTC `time_bucket` can be wrong for market-specific sessions.

## Verification Checklist

- [ ] Endpoint p95 latency is measured with realistic candle counts.
- [ ] Payload size is bounded and does not grow with full instrument history.
- [ ] Query plan uses the continuous aggregate view and instrument/time filters.
- [ ] Real-time path does not call `setData()` for each update.
- [ ] Late-arriving tick tests verify aggregate refresh behavior.
