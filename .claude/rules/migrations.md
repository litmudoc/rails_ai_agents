---
paths:
  - "db/migrate/**/*.rb"
  - "db/timeseries_migrate/**/*.rb"
  - "db/timeseries_cache_migrate/**/*.rb"
  - "db/*structure.sql"
---

# Migration Conventions

- Always reversible: prefer `change` over `up`/`down`
- Add `null: false` for required columns
- Add database-level defaults where appropriate
- Always add indexes for foreign keys and frequently queried columns
- Add unique indexes for uniqueness validations
- Use `references` with `foreign_key: true` for associations
- Never modify a migration that has already been run -- create a new one
- For zero-downtime: add column first, then backfill, then add constraint

## Multi-database / TimescaleDB (see docs/multi-db-config.md)

- Primary DB uses the default :ruby schema format — verify `db/schema.rb` diffs. The `timeseries` / `timeseries_cache` databases have no schema dump at all (`schema_dump: false`); their state is defined solely by the migrations in their `*_migrate/` directories, which `db:prepare` (re)runs.
- Migrations for the `timeseries` / `timeseries_cache` databases live in `db/timeseries_migrate/` and `db/timeseries_cache_migrate/` and use raw SQL (`execute`) with explicit `up`/`down` for hypertables, continuous aggregates, and retention/refresh policies — `change` cannot express these; explicit `up`/`down` is the convention there, not a violation of the reversibility rule.
- No foreign keys in `timeseries` / `timeseries_cache` tables: they denormalize `exchange_code` and `symbol` as plain strings (cross-database FKs are impossible). Do not add `references ... foreign_key: true` there.
- Unique indexes on hypertables must include the `time` partition column.
- `interval` is a PostgreSQL keyword — quote it as `"interval"` in raw SQL.
