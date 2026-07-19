---
paths:
  - "spec/**/*.rb"
---

# Testing Conventions

- TDD approach: RED (failing test) -> GREEN (minimal implementation) -> REFACTOR
- Use `subject { build(:entity) }` for validation specs
- Prefer explicit setup in each test for clarity over `let!`
- Use `let` (lazy) by default; avoid `let!` unless records must exist before the example runs (e.g., scope tests)
- One behavior per `it` block
- Use `context` blocks to group by scenario
- Use FactoryBot: `build` over `create` when persistence isn't needed
- Request specs (`spec/requests/`) over controller specs
- Test authentication AND authorization in request specs (MVP exception: auth is out of scope per docs/req/01.mvp.md — skip these assertions and assert routes are publicly reachable until auth lands)
- Use Shoulda Matchers for validations and associations
- Run `bundle exec rubocop -a` after writing specs

## Multi-Database Tests (timeseries / timeseries_cache)

- The test environment defines `timeseries` and `timeseries_cache` entries (see docs/multi-db-config.md). These use `schema_dump: false`, so `RAILS_ENV=test bin/rails db:prepare` creates them and runs their migrations (TimescaleDB extension, hypertables, continuous aggregates) — never hand-create these in specs. The primary database loads from `db/schema.rb` (default :ruby format); rails_helper auto-recovers the schema-less databases when a test-schema reload purges them.
- Rails transactional tests wrap every configured database connection, so `Candle` / `ActiveCandle` writes roll back between examples like primary-DB writes. If a spec must commit outside the wrapping transaction, delete from `candles` / `active_candles` explicitly in an `after` block.
- Continuous-aggregate models (`Candle2m`…`Candle30m`) are readonly real-time aggregates (`materialized_only = false`): in specs, insert 1m rows into `candles` and query the aggregate model directly. Do not attempt to trigger refresh policies — TimescaleDB background workers do not run during tests.

## ActionCable / Streaming Jobs

- Channel specs use `type: :channel`: `subscribe` then `expect(subscription).to have_stream_from("chart:candles")`; assert broadcasts with `have_broadcasted_to("chart:candles").with(hash_including(candle: ...))`. `ChartChannel` payloads are direct JSON — do not apply Turbo Stream assertions (`assert_turbo_stream`, `text/vnd.turbo-stream.html`) to it.
- Never run long-running/looping jobs to completion in specs (`perform_now` / `perform_enqueued_jobs` on `LiveCandleStreamJob` will hang) — test one loop iteration with `Binance::KlineStreamClient` stubbed. Specs must never open real WebSocket connections or call Binance.
