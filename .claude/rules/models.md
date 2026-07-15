---
paths:
  - "app/models/**/*.rb"
  - "spec/models/**/*.rb"
  - "spec/factories/**/*.rb"
---

# Model Conventions

- Keep models thin: data, validations, associations, scopes, simple predicates only
- Complex business logic goes in service objects (`app/services/`)
- Use callbacks only for data normalization (`before_validation`) and defaults (`after_initialize`)
- Side effects (emails, API calls, job enqueueing) belong in services, not callbacks
- Always specify `dependent:` on `has_many`/`has_one` associations
- Use `enum :status, { draft: 0, published: 1 }` (hash syntax with explicit integers)
- Validate presence at both model and database level (`null: false` in migration)
- Use scopes for reusable queries; use query objects (`app/queries/`) for complex ones
- Every model must have a factory in `spec/factories/` with traits for each state
- Test with Shoulda Matchers: `validate_presence_of`, `belong_to`, `have_many`

## Project-specific exceptions (decided — do not "correct")

- `Exchange.exchange_type`/`network`, `TradingPair.status`, and candle `interval` are string columns validated with `inclusion` — do NOT convert them to integer-backed `enum`.
- `ApiCredential` uses `belongs_to :user, optional: true` with `user_id` `not null, default: 1` and NO database-level foreign key (minimal placeholder `User`, seed id=1). Do not add a FK constraint or make the association required.
- Time-series models inherit from `TimeseriesRecord` / `TimeseriesCacheRecord` (abstract `connects_to` classes), not `ApplicationRecord`. Continuous-aggregate models (`Candle2m`..`Candle30m`) declare `def readonly? = true`, have no factories/traits, and are never written from Ruby.
- No ActiveRecord associations between primary-DB models and time-series models — cross-database joins are impossible; `exchange_code`/`symbol` are denormalized strings, correlated in the service layer.
- Never put `after_commit` broadcast callbacks on time-series models — broadcasting happens in `LiveCandles::IngestService`.
