# 37signals AI Skills for Rails

A specialized ecosystem of AI skills for Ruby on Rails development, focused on the Basecamp/HEY (37signals) philosophy. Drop them into your project and your AI coding assistant instantly knows Minitest, Hotwire, Fat Models, and production patterns used by 37signals.

Works with Opencode, Mistral Vibe, Claude Code, GitHub Copilot, Cursor, Gemini CLI, and [30+ other tools](https://agentskills.io/specification) that support the Agent Skills standard.

## What's Inside

The `37signals_skills/` directory contains skills following the Basecamp/HEY philosophy. Key differences from standard Rails conventions include:

| Area | 37signals Pattern |
|---|---|
| Business logic | Fat models (avoid service objects) |
| Tests | Minitest + fixtures |
| Shared behavior | Concerns everywhere |
| Request context | `Current` attributes |
| State | State as records |
| IDs | UUIDs |
| Multi-tenancy | URL-based with `Current.account` |

### Included Skills

Here is the complete list of 37signals-style skills available in this collection:

| Skill | Description |
|---|---|
| `37signals-api` | Builds REST APIs using respond_to blocks with Jbuilder templates following the 37signals same-controllers-different-formats philosophy. Use when adding API endpoints, JSON responses, token authentication, or when user mentions API, JSON, REST, or Jbuilder. |
| `37signals-auth` | Implements custom passwordless authentication without Devise. Use when setting up authentication, login flows, session management, password resets, or when user mentions auth, login, passwordless, or sessions. |
| `37signals-caching` | Implements HTTP caching with ETags, fresh_when, stale?, and fragment caching. Use when optimizing performance, adding caching layers, or when user mentions ETags, HTTP caching, fresh_when, stale?, cache keys, or Russian doll caching. |
| `37signals-concerns` | Creates and refactors model and controller concerns for shared behavior following 37signals patterns. Use when extracting shared code, organizing models with horizontal concerns, DRYing up controllers, or when user mentions concerns, mixins, modules, or shared behavior. |
| `37signals-crud` | Generates RESTful controllers following the 37signals everything-is-CRUD philosophy. Maps any action to CRUD by creating new resources instead of custom actions. Use when adding features, creating controllers, or when user mentions REST, routing, controllers, or state-change resources. |
| `37signals-events` | Builds event tracking and activity systems with webhooks following 37signals patterns. Use when implementing audit trails, activity feeds, event sourcing, or when user mentions events, tracking, webhooks, or activity logs. |
| `37signals-implement` | Orchestrates implementation of complete Rails features across models, controllers, views, and tests following 37signals conventions. Use when implementing a full feature end-to-end or when user mentions feature implementation, full-stack, or orchestration. |
| `37signals-jobs` | Implements shallow background jobs with _later/_now conventions using Solid Queue. Use when adding background processing, async operations, scheduled tasks, or when user mentions jobs, queues, Solid Queue, or background workers. |
| `37signals-lightweight-charts` | Builds high-performance financial charts using TradingView Lightweight Charts wrapped in a <lightweight-chart> Web Component custom element, integrated with Stimulus bridge controllers and Turbo Streams for real-time updates. Use when adding candlestick charts, price charts, financial data visualization, or when user mentions Lightweight Charts, trading charts, OHLC, or real-time prices. |
| `37signals-mailer` | Creates minimal Action Mailer classes with bundled notification patterns following 37signals conventions. Use when sending emails, creating notification systems, or when user mentions mailers, emails, notifications, or transactional messages. |
| `37signals-migration` | Creates database migrations with UUIDs, account scoping, and no foreign key constraints following 37signals patterns. Use when creating tables, adding columns, modifying schema, or when user mentions migrations, database structure, or schema changes. |
| `37signals-model` | Builds rich domain models with business logic, concerns, and proper associations following the 37signals fat-models-over-service-objects philosophy. Use when creating models, adding validations, scopes, callbacks, or business logic methods. |
| `37signals-multi-tenant` | Implements URL-based multi-tenancy with account scoping following 37signals patterns. Use when setting up multi-tenant architecture, account isolation, tenant scoping, or when user mentions multi-tenancy, accounts, or tenant separation. |
| `37signals-refactoring` | Orchestrates refactoring of Rails codebases toward 37signals patterns and modern conventions. Use when refactoring existing code, improving architecture, migrating to modern Rails patterns, or when user mentions refactoring, code improvement, or technical debt. |
| `37signals-review` | Reviews code for adherence to 37signals Rails patterns and conventions. Checks for rich models, CRUD controllers, proper concerns, and Hotwire usage. Use when requesting code review, architecture audit, or quality analysis. |
| `37signals-state-records` | Implements the state-as-records-not-booleans pattern for rich state tracking following 37signals conventions. Use when modeling state changes, replacing boolean flags with record-based state, or when user mentions state records, closures, publications, or state tracking. |
| `37signals-stimulus` | Builds focused, single-purpose Stimulus controllers for progressive enhancement following 37signals patterns. Use when adding JavaScript behavior, UI interactions, form enhancements, or when user mentions Stimulus, JavaScript controllers, or sprinkles. |
| `37signals-test` | Writes Minitest tests with integration tests and fixtures following 37signals conventions. Uses Minitest (not RSpec) and fixtures (not factories). Use when writing tests, adding test coverage, or when user mentions testing, Minitest, fixtures, or integration tests. |
| `37signals-turbo` | Creates Turbo Streams, Turbo Frames, and morphing patterns for real-time UI updates following 37signals conventions. Use when adding real-time updates, page navigation, form submissions, or when user mentions Turbo, Streams, Frames, Drive, or morphing. |

## Opencode Configuration

To properly configure these skills to work with **Opencode**, you need to set up the appropriate `AGENT.md` files:

1. **Global Configuration**
   Copy `37signals_global_AGENTS.md` to your Opencode global agent settings:
   ```bash
   mkdir -p ~/.config/opencode
   cp 37signals_global_AGENTS.md ~/.config/opencode/AGENT.md
   ```

2. **Project Configuration**
   Copy `37signals_project_AGENTS.md` and `37signals_project_AGENTS.local.md` to your project's root directory:
   ```bash
   cp 37signals_project_AGENTS.md /path/to/your-rails-app/AGENT.md
   cp 37signals_project_AGENTS.local.md /path/to/your-rails-app/AGENT.local.md
   ```

### Understanding the Agent Files

- **`~/.config/opencode/AGENT.md`**: Enforces absolute global rules across all your projects (secrets protection, dangerous operations) and establishes your developer identity.
- **`AGENT.md` (Project Level)**: Contains the project-specific tech stack (Rails 8, SQLite, Solid trifecta, Hotwire), structure conventions, and strictly directs the AI to use the `skills/` directory.
- **`AGENT.local.md` (Project Local)**: Contains your personal development overrides (e.g., verbose test output, displaying SQL queries) that should not be committed to version control.

## Typical Workflow

When asking Opencode to implement a feature, it will automatically:
1. Reference the master orchestration skill (`skills/37signals-implement/SKILL.md`).
2. Follow a strict **RED -> GREEN -> REFACTOR -> REVIEW** TDD workflow using Minitest.
3. Break down massive tasks into small (50-200 line) Pull Requests.
4. Delegate tasks to specialized skills like `37signals-crud`, `37signals-model`, and `37signals-turbo`.

## Installation for Other Tools

Copy the `37signals_skills/` directory to `.agents/skills/` in your Rails application:

```bash
cp -r 37signals_skills/ /path/to/your-rails-app/.agents/skills/
```

## License

MIT
