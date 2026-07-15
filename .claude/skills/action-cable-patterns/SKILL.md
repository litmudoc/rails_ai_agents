---
name: action-cable-patterns
description: >-
  Implements real-time features with Action Cable and WebSockets. Use when
  adding live updates, chat features, notifications, real-time dashboards,
  or when user mentions Action Cable, WebSockets, channels, or real-time.
  WHEN NOT: Simple HTTP request/response flows, REST APIs, static content,
  or features that don't need real-time updates.
paths: "app/channels/**/*.rb, app/javascript/channels/**/*.js, spec/channels/**/*.rb"
---

# Action Cable Patterns for Rails 8

## Overview

Action Cable integrates WebSockets with Rails:
- Real-time updates without polling
- Server-to-client push notifications
- Chat and messaging features
- Live dashboards and feeds
- Collaborative editing

> **PROJECT DECISIONS (MVP chart — docs/features/01.mvp-binance-realtime-chart.md 4-B):**
> - Development cable adapter must be `solid_cable`, not `async` — the candle ingestion job broadcasts from a separate `bin/jobs` process, and the async adapter only delivers in-process (see docs/multi-db-config.md).
> - `ChartChannel` is public in the MVP: no `identified_by` in `ApplicationCable::Connection`, no `reject_unauthorized_connection`. Leave `# TODO: cookies.signed-based connection auth` and do not scaffold session authentication.
> - `ChartChannel#subscribed` is just `stream_from "chart:candles"` (single global stream). Broadcasts are direct JSON via `ActionCable.server.broadcast("chart:candles", { candle: { symbol:, interval:, time:, open:, high:, low:, close:, volume: } })` from `LiveCandles::IngestService` — never HTML partials, never Turbo Streams, never model callbacks. Clients filter by `candle.symbol` + `candle.interval`. This is a documented deliberate deviation — do not convert it.

## Quick Start

Action Cable is included in Rails by default. Configure it:

```ruby
# config/cable.yml
development:
  adapter: solid_cable  # this project: async is in-process only; broadcasts come from bin/jobs

test:
  adapter: test

production:
  adapter: solid_cable  # Rails 8 default
  # OR
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") %>
```

## Project Structure

```
app/
├── channels/
│   ├── application_cable/
│   │   ├── connection.rb      # Authentication
│   │   └── channel.rb         # Base channel
│   ├── notifications_channel.rb
│   ├── events_channel.rb
│   └── chat_channel.rb
├── javascript/
│   └── channels/
│       ├── consumer.js
│       ├── notifications_channel.js
│       └── events_channel.js
spec/channels/
├── notifications_channel_spec.rb
└── events_channel_spec.rb
```

## Connection Authentication

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      # Using Rails 8 authentication
      if session_token = cookies.signed[:session_token]
        if session = Session.find_by(token: session_token)
          session.user
        else
          reject_unauthorized_connection
        end
      else
        reject_unauthorized_connection
      end
    end
  end
end
```

## Channel Patterns

Four core patterns are available. See [channel-patterns.md](references/channel-patterns.md) for full Ruby and JavaScript implementations:

- **Pattern 1: Notifications Channel** — streams per-user notifications via `stream_for current_user`
- **Pattern 2: Resource Updates Channel** — streams updates for a specific resource with authorization via `reject`
- **Pattern 3: Chat Channel** — bidirectional messaging with `speak` and `typing` actions, presence tracking
- **Pattern 4: Dashboard Live Updates** — broadcasts stats and activity feed to all account members
- **Pattern 5: Global JSON Firehose (this project's `ChartChannel`)** — `subscribed` calls only `stream_from "chart:candles"` (single global string stream, no per-resource streams, no authorization); producers broadcast raw JSON from `LiveCandles::IngestService`; clients filter by payload fields. No partial rendering, no Turbo Streams.

Each pattern follows the same structure:
1. `subscribed` — find the resource, check authorization, call `stream_for`
2. Class-level `broadcast_*` methods — render partials via `ApplicationController.renderer`
3. A matching JavaScript subscription handler with a `received(data)` switch

## Broadcasting

Broadcasting is triggered from service objects in this project (side effects never live in model callbacks — see .claude/rules/principles.md; candle broadcasts come only from `LiveCandles::IngestService`). See [broadcasting-and-stimulus.md](references/broadcasting-and-stimulus.md) for:

- **From a service object** — call `EventsChannel.broadcast_update(event)` after persistence
- **From model callbacks** — shown in references for completeness; NOT used in this project (broadcasts from callbacks are prohibited)
- **Turbo Streams integration** — use `broadcast_append_to` / `broadcast_remove_to` helpers directly on models
- **Stimulus controller** — wrap the Action Cable subscription lifecycle inside a Stimulus controller for clean connect/disconnect management
- **Performance patterns** — connection limits, selective broadcasting, debounced broadcasts

## Testing Channels

See [testing.md](references/testing.md) for full specs. Key conventions:

```ruby
# Stub connection identity
stub_connection(current_user: user)

# Assert subscription confirmed and streaming
subscribe(event_id: event.id)
expect(subscription).to be_confirmed
expect(subscription).to have_stream_for(event)

# Assert rejection for unauthorized access
expect(subscription).to be_rejected

# Assert broadcast payload
expect {
  described_class.notify(user, notification)
}.to have_broadcasted_to(user).with(hash_including(type: "notification"))
```

## Checklist

- [ ] Connection authentication configured (skip for public channels — MVP `ChartChannel` is public by design)
- [ ] Channel authorization implemented (or explicitly public, like `ChartChannel`)
- [ ] Client-side subscription set up
- [ ] Broadcasting from services (never model callbacks in this project)
- [ ] Channel specs written
- [ ] Error handling in place
- [ ] Reconnection logic on client
- [ ] Performance limits configured

## References

- [channel-patterns.md](references/channel-patterns.md) — Full implementations of Notifications, Resource Updates, Chat, and Dashboard channels (Ruby + JavaScript)
- [broadcasting-and-stimulus.md](references/broadcasting-and-stimulus.md) — Broadcasting from services/models, Turbo Streams integration, Stimulus controller, performance tips
- [testing.md](references/testing.md) — RSpec channel specs, authorization specs, and system tests
