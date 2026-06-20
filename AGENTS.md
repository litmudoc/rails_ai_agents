# Project Configuration

## Language Rules

- **Code & documentation:** All source code, comments, commit messages, branch names, and markdown files MUST be written in **English**.
- **User communication:** When asking questions, requesting clarification, or providing status updates to the user, ALWAYS use **Korean (한국어)**.

## Tech Stack

- **Ruby** 3.3, **Rails** 8.1, **PostgreSQL**, **TimescaleDB**
- **Frontend:** Hotwire (Turbo + Stimulus), Tailwind CSS 4, ViewComponent
- **Financial Charting:** TradingView Lightweight Charts via Import Maps
- **Testing:** RSpec, FactoryBot, Shoulda Matchers, Capybara
- **Auth:** `has_secure_password` (Rails 8 built-in), Pundit (authorization)
- **Background Jobs:** Solid Queue (database-backed, no Redis)
- **Caching:** Solid Cache | **WebSockets:** Solid Cable
- **Assets:** Propshaft + Import Maps (no Node.js)
- **Deployment:** Kamal 2 + Thruster

## Architecture

```
app/
  controllers/     # Thin. Delegates to services. Renders responses.
  models/          # Persistence: validations, associations, scopes, simple predicates.
  views/           # ERB markup only. No logic.
  services/        # Business logic. Orchestrates models, APIs, side effects.
  queries/         # Complex database queries. Returns relations or hashes.
  forms/           # Multi-model form objects.
  policies/        # Pundit authorization. Default deny.
  presenters/      # View formatting (SimpleDelegator).
  components/      # ViewComponents (reusable UI with tests).
  jobs/            # Background jobs (Solid Queue). Must be idempotent.
  mailers/         # Email delivery. Always HTML + text templates.
```

## Key Commands

```bash
# Bootstrap the app (PostgreSQL primary; TimescaleDB is wired in afterwards via database.yml).
# After generation, edit config/database.yml per @docs/multi-db-config.md before first migrate.
rails new . --css=tailwind --javascript=importmap --database=postgresql

# Tests
bundle exec rspec                              # Full suite
bundle exec rspec spec/path/to_spec.rb         # Specific file
bundle exec rspec spec/path/to_spec.rb:25      # Specific line

# Linting
bundle exec rubocop -a                         # Auto-fix Ruby
bundle exec rubocop -a app/models/             # Specific directory

# Security
bin/brakeman --no-pager                        # Static analysis
bundle exec bundler-audit check --update       # Gem vulnerabilities

# Database
bin/rails db:migrate                           # Run migrations
bin/rails db:migrate:status                    # Check status
bin/rails console                              # Interactive console
```

## Development Workflow

Follow **TDD: Red -> Green -> Refactor**:
1. **RED:** Write a failing test describing desired behavior
2. **GREEN:** Write minimal code to pass the test
3. **REFACTOR:** Improve code structure while keeping tests green

## Agent Routing

Use specialist agents when a task clearly belongs to one implementation domain. When delegating with the Claude Agent tool, set `subagent_type` to the agent name listed below. Prefer the most specific agent over a general frontend agent.

| Task Type | Agent | Notes |
|-----------|-------|-------|
| Candlestick, OHLC, price, volume, market data, chart timeframe switching, or real-time financial dashboards | `lightweight-chart-agent` | Use TradingView Lightweight Charts with Stimulus, Turbo Streams, Solid Cable, and Import Maps. |
| Raw ticks, hypertables, continuous aggregates, candle rollups, chart read views, or TimescaleDB migrations | `database-reviewer` | Pair with `lightweight-chart-agent` when chart data storage or query shape changes. |
| Generic Stimulus behavior without charting | `stimulus-agent` | Use for client-side interactions that are not chart-specific. |
| Turbo Frames, Turbo Streams, and partial page updates without charting | `turbo-agent` | Use for HTML-over-the-wire interactions that are not chart-specific. |
| Reusable UI components | `viewcomponent-agent` | Pair with chart agents only when the chart shell is a reusable component. |

For Lightweight Charts work:
- Install browser dependencies with `bin/importmap pin lightweight-charts`; do not add npm, yarn, or bundler-based JavaScript tooling.
- Keep chart initialization in Stimulus controllers and keep data preparation in Rails services, queries, or presenters as appropriate.
- Query chart history from bounded, readonly PostgreSQL/TimescaleDB OHLCV views; do not compute candle buckets in JavaScript or Ruby request paths.
- Use `series.update()` for real-time ticks and reserve `series.setData()` for initial loads or full dataset replacement.
- Preserve chart DOM stability with stable IDs and `data-turbo-permanent` when Turbo morphing can affect the chart container.
- Include TradingView attribution wherever Lightweight Charts are rendered.
- Test rendered chart containers, data attributes, chart data endpoints, Turbo Stream broadcasts, and Stimulus lifecycle cleanup.

## Core Conventions

- **Skinny Everything:** Controllers orchestrate. Models persist. Services contain business logic. Views display.
- **Callbacks:** Only for data normalization (`before_validation`, `before_save`). Side effects (emails, jobs, APIs) belong in services.
- **Services:** `.call` class method, return Result objects, namespace by domain (`Entities::CreateService`).
- **No premature abstraction:** Don't extract until complexity demands it. Three similar lines > wrong abstraction.
- **Explicit > implicit:** Clear service calls over hidden callbacks. Named methods over metaprogramming.

See @docs/rails-development-principles.md for the complete development principles guide.

## Naming Conventions

| Layer | Pattern | Example |
|-------|---------|---------|
| Model | Singular PascalCase | `Entity`, `OrderItem` |
| Controller | Plural PascalCase | `EntitiesController` |
| Service | Namespaced + `Service` | `Entities::CreateService` |
| Query | Namespaced + `Query` | `Entities::SearchQuery` |
| Policy | Singular + `Policy` | `EntityPolicy` |
| Job | Descriptive + `Job` | `ProcessPaymentJob` |
| Presenter | Singular + `Presenter` | `EntityPresenter` |
| Form | Descriptive + `Form` | `EntityRegistrationForm` |
