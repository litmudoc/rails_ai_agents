---
name: performance-optimization
description: >-
  Identifies and fixes Rails performance issues including N+1 queries, slow
  queries, memory problems, large payloads, and PostgreSQL/TimescaleDB-backed
  chart endpoints. Use when optimizing queries, fixing N+1 issues, improving
  response times, tuning financial candle endpoints, reducing real-time update
  load, or when user mentions performance, slow, optimization, Bullet gem,
  EXPLAIN, continuous aggregates, or chart lag. WHEN NOT: Caching-specific
  patterns (use caching-strategies), adding new features, or general code
  quality improvements unrelated to speed.
---

# Performance Optimization for Rails 8

## Overview

Performance optimization focuses on:
- N+1 query detection and prevention
- Query optimization
- Memory management
- Response time improvements
- Database indexing
- Financial chart endpoint and TimescaleDB continuous aggregate performance

## Quick Start

```ruby
# Gemfile
group :development, :test do
  gem 'bullet'           # N+1 detection
  gem 'rack-mini-profiler' # Request profiling
  gem 'memory_profiler'  # Memory analysis
end
```

## N+1 Query Detection and Prevention

N+1 queries occur when code loads a collection then makes a separate query for each associated record. The Bullet gem detects these automatically. Fix them with eager loading via `includes`, `preload`, or `eager_load`.

### Eager Loading Decision Table

| Method | Use When |
|--------|----------|
| `includes` | Most cases (Rails chooses best strategy) |
| `preload` | Forcing separate queries, large datasets |
| `eager_load` | Filtering on association, need single query |
| `joins` | Only need to filter, don't need association data |

Key patterns: Bullet configuration, eager loading methods, scoped eager loading, counter caches, N+1 specs with query count assertions.

See [references/n-plus-one.md](references/n-plus-one.md) for all code examples and patterns.

## Query Optimization

Optimize queries by selecting only needed columns, using batch processing for large datasets, and choosing efficient existence checks.

### Key Patterns

| Pattern | Bad | Good |
|---------|-----|------|
| Column selection | `User.all.map(&:name)` | `User.pluck(:name)` |
| Large iterations | `Event.all.each { ... }` | `Event.find_each { ... }` |
| Existence checks | `.any?` / `.present?` | `.exists?` |
| Collection size | `.length` (loads all) | `.size` (smart) |

### Database Indexing

Add indexes for: foreign keys, columns in WHERE/ORDER BY/JOIN clauses, and unique constraints. Use composite indexes for multi-column queries. Use partial indexes for filtered subsets.

### Query Analysis

Use `Event.where(...).explain(:analyze)` to inspect query plans. Set up slow query logging via `ActiveSupport::Notifications` to catch queries over a threshold.

See [references/query-optimization.md](references/query-optimization.md) for all code examples and patterns.

## Financial Chart and TimescaleDB Performance

For OHLC/candlestick chart endpoints, prefer querying bounded readonly views backed by TimescaleDB continuous aggregates instead of scanning raw ticks in request paths. Use `series.setData()` only for initial/range loads and `series.update()` for real-time updates.

Key patterns: hypertable indexes by instrument/time, payload bounds, visible-range pagination, continuous aggregate refresh policy checks, real-time aggregate settings, late tick/backfill refreshes, and avoiding Ruby/JavaScript OHLC recomputation.

See [references/financial-timeseries.md](references/financial-timeseries.md) for chart endpoint and TimescaleDB performance patterns.

## Memory Management and Profiling

Use `memory_profiler` to detect memory issues. Prefer `pluck` over loading full AR objects, use `find_each` for streaming, and use `update_all` / `in_batches` for bulk operations.

### Rack Mini Profiler

Provides per-request profiling in development. Shows query count, timing, and flamegraphs (with `stackprof` gem). Access via the profiler badge or `?pp=flamegraph`.

See [references/memory-and-profiling.md](references/memory-and-profiling.md) for all code examples and patterns.

## Quick Fixes Reference

| Problem | Solution |
|---------|----------|
| N+1 on belongs_to | `includes(:association)` |
| N+1 on has_many | `includes(:association)` |
| Slow COUNT | Add counter_cache |
| Loading all columns | Use `select` or `pluck` |
| Large dataset iteration | Use `find_each` |
| Missing index on FK | Add index on `*_id` columns |
| Slow WHERE clause | Add index on filtered column |
| Loading unused associations | Remove from `includes` |
| Slow candle chart endpoint | Query continuous aggregate OHLCV view with bounded time range |
| Chart lag during live updates | Throttle broadcasts and use `series.update()` |
| Raw tick scan for candles | Add or fix TimescaleDB continuous aggregate |

## Performance Checklist

- [ ] Bullet enabled in development/test
- [ ] No N+1 queries in critical paths
- [ ] Foreign keys have indexes
- [ ] Counter caches for frequent counts
- [ ] Eager loading in controllers
- [ ] Batch processing for large datasets
- [ ] Query analysis for slow endpoints
- [ ] Chart endpoints use bounded time ranges and return only OHLCV columns
- [ ] TimescaleDB continuous aggregate policies are active for chart timeframes
- [ ] Real-time chart updates are throttled and avoid full dataset replacement

## Workflow

1. **Detect** -- Enable Bullet, run specs, check Rack Mini Profiler
2. **Analyze** -- Use `explain(:analyze)`, check slow query logs, profile memory
3. **Fix** -- Apply the appropriate pattern from the reference files
4. **Verify** -- Re-run specs, confirm query counts, check profiler

## Reference Files

- [references/n-plus-one.md](references/n-plus-one.md) -- N+1 detection, eager loading methods, Bullet config, counter caches, testing patterns
- [references/query-optimization.md](references/query-optimization.md) -- Column selection, batch processing, indexing strategies, EXPLAIN analysis, slow query logging
- [references/memory-and-profiling.md](references/memory-and-profiling.md) -- Memory profiler usage, memory-efficient patterns, Rack Mini Profiler setup, deployment checklist
- [references/financial-timeseries.md](references/financial-timeseries.md) -- TimescaleDB continuous aggregates, chart endpoint payloads, real-time update tuning, and verification queries
