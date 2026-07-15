---
paths:
  - "app/jobs/**/*.rb"
  - "spec/jobs/**/*.rb"
---

# Background Job Conventions

- Use Solid Queue (database-backed, Rails 8 default)
- Jobs must be idempotent -- safe to retry
- Pass IDs, not full objects (serialization safety)
- Use `discard_on ActiveRecord::RecordNotFound` for deleted records
- Use `retry_on` with specific exceptions and limits
- Keep jobs focused: one job, one responsibility
- Test enqueue-side behavior with `have_enqueued_job` matcher

## Sanctioned exception: streaming consumer

- `LiveCandleStreamJob` is a deliberate long-running exception (one per enabled exchange): it holds a Binance WebSocket kline connection open and runs an event loop. It runs on the dedicated `streaming` queue (own worker in `config/queue.yml`) so it never occupies `default` workers. Do not "fix" it into a short job. See docs/features/01.mvp-binance-realtime-chart.md 4-B.
- Its liveness model is supervision, not retry: `LiveCandleStreamSupervisorJob` (recurring 30s, `config/recurring.yml`) re-enqueues it when `exchanges.stream_heartbeat_at` is >60s stale. Solid Queue does not auto-retry crashed executions, so the supervisor is the primary recovery path; `retry_on` is secondary.
- Do not treat `limits_concurrency` as a hard singleton guarantee for it (the semaphore expires after `duration`; use `on_conflict: :discard`). Idempotent upserts make accidental duplicates data-safe.
- Never run a long-running/looping job to completion in specs (`perform_now` / `perform_enqueued_jobs` will hang). Structure the job so the loop body is extractable and test one iteration: stub `Binance::KlineStreamClient` (specs must never open real WebSocket connections), then assert heartbeat updates, pair-rescan SUBSCRIBE/UNSUBSCRIBE deltas, in-progress throttling (1/sec/pair, close events immediate), and `LiveCandles::IngestService` invocations.
