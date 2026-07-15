---
paths:
  - "app/services/**/*.rb"
  - "spec/services/**/*.rb"
---

# Service Object Conventions

- Single public method: `#call`
- Class-level shortcut: `self.call(...)` delegates to `new(...).call`
- Return a Result object (`Data.define(:success, :data, :error)` with `success?`/`failure?` predicates)
- Never raise exceptions for business logic failures; use `failure(message)`
- Namespace by domain: `Entities::CreateService`, `Orders::CancelService`
- Inherit from `ApplicationService` base class (`app/services/application_service.rb`)
- Inject dependencies via constructor for testability
- Wrap multi-model operations in `ActiveRecord::Base.transaction`
- Test both success and failure paths with `subject(:result)`

## Exception: client wrappers

- Classes named `*Client` under `app/services/` (e.g. `Binance::KlineStreamClient` in `app/services/binance/kline_stream_client.rb`) are external-API/connection wrappers, not service objects. They do NOT take the `Service` suffix, do NOT inherit `ApplicationService`, are not required to expose a single `#call` returning a Result, and may hold connection state and expose lifecycle methods (connect, subscribe, close, event callbacks). See docs/features/01.mvp-binance-realtime-chart.md 4-B.
- Everything else in `app/services/` follows the conventions above.
- Cross-database note: dual-writes spanning `timeseries` and `timeseries_cache` cannot be wrapped in one `ActiveRecord::Base.transaction` — use ordered idempotent upserts instead (see the feature spec).
