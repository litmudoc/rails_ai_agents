---
name: solid-queue-setup
description: >-
  Configures Solid Queue for background jobs in Rails 8. Use when setting up
  background processing, creating background jobs, configuring job queues,
  or migrating from Sidekiq to Solid Queue. WHEN NOT: Synchronous in-request
  processing, browser-facing real-time push (use Action Cable; upstream
  WebSocket stream consumers like LiveCandleStreamJob DO run as Solid Queue
  jobs), or simple operations that don't need background execution.
paths: "app/jobs/**/*.rb, config/queue.yml, spec/jobs/**/*.rb"
---

# Solid Queue Setup for Rails 8

## Overview

Solid Queue is Rails 8's default Active Job backend:
- Database-backed (no Redis required)
- Built-in concurrency controls
- Supports priorities and multiple queues
- Mission-critical job processing
- Web UI available via Mission Control

## Quick Start

### Installation

```bash
# Add to Gemfile (included in Rails 8 by default)
bundle add solid_queue

# Install Solid Queue
bin/rails solid_queue:install

# Run migrations
bin/rails db:migrate
```

### Configuration

```yaml
# config/queue.yml   (Rails 8 reads queue.yml — NOT solid_queue.yml)
default: &default
  dispatchers:
    - polling_interval: 1
      batch_size: 500
  workers:
    - queues: "*"
      threads: 3
      processes: 1
      polling_interval: 0.1

development:
  <<: *default

production:
  <<: *default
  workers:
    - queues: [critical, default]
      threads: 5
      processes: 2
    - queues: [low]
      threads: 2
      processes: 1
    # This project: dedicated worker for the long-running LiveCandleStreamJob
    # - queues: streaming
    #   threads: 2
```

### Set as Active Job Adapter

```ruby
# config/application.rb
config.active_job.queue_adapter = :solid_queue

# Or per environment
# config/environments/production.rb
config.active_job.queue_adapter = :solid_queue
```

## Workflow Checklist

```
Solid Queue Setup:
- [ ] Add solid_queue gem
- [ ] Run solid_queue:install
- [ ] Run migrations
- [ ] Configure queues in config/queue.yml
- [ ] Set queue adapter in config
- [ ] Create first job with spec
- [ ] Test job execution
- [ ] Configure recurring jobs (if needed)
```

## Creating Jobs

### Basic Job

```ruby
# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end
```

### Job with Retries

```ruby
# app/jobs/process_payment_job.rb
class ProcessPaymentJob < ApplicationJob
  queue_as :critical

  # Retry on specific errors
  retry_on PaymentGatewayError, wait: :polynomially_longer, attempts: 5

  # Don't retry on these
  discard_on ActiveRecord::RecordNotFound

  # Custom error handling
  rescue_from(StandardError) do |exception|
    ErrorNotifier.notify(exception)
    raise # Re-raise to trigger retry
  end

  def perform(order_id)
    order = Order.find(order_id)
    PaymentService.new.charge(order)
  end
end
```

### Job with Priority

```ruby
class UrgentNotificationJob < ApplicationJob
  queue_as :critical

  # Lower number = higher priority
  # Default is 0
  def priority
    -10
  end

  def perform(notification_id)
    # Process urgent notification
  end
end
```

## Enqueueing Jobs

```ruby
# Enqueue immediately
SendWelcomeEmailJob.perform_later(user.id)

# Enqueue with delay
SendReminderJob.set(wait: 1.hour).perform_later(user.id)

# Enqueue at specific time
SendReportJob.set(wait_until: Date.tomorrow.noon).perform_later

# Enqueue on specific queue
ProcessJob.set(queue: :low).perform_later(data)

# Perform immediately (skips queue - use sparingly)
SendWelcomeEmailJob.perform_now(user.id)
```

## Concurrency Limits

```ruby
class LiveCandleStreamJob < ApplicationJob
  queue_as :streaming
  limits_concurrency to: 1, key: ->(exchange_code) { exchange_code },
                     duration: 5.minutes, on_conflict: :discard
end
```

Honest semantics: the concurrency semaphore is held only for `duration` and then
expires. For short jobs this is a reliable mutual-exclusion guard; for
long-running jobs it is best-effort only — after `duration` a duplicate can run.
The default conflict behavior BLOCKS the conflicting enqueue and runs it after
the semaphore expires (a delayed duplicate); use `on_conflict: :discard` when a
supervisor re-enqueues periodically. Never use `limits_concurrency` as the sole
singleton guarantee for a long-running job; pair it with an application-level
liveness check (this project: supervisor + `exchanges.stream_heartbeat_at`
freshness) and idempotent writes so duplicates are harmless.

## Recurring Jobs

```yaml
# config/recurring.yml
production:
  daily_report:
    class: GenerateDailyReportJob
    schedule: every day at 6am
    queue: low

  cleanup:
    class: CleanupOldRecordsJob
    schedule: every sunday at 2am

  sync:
    class: SyncExternalDataJob
    schedule: every 15 minutes
```

## Testing Jobs

### Job Spec Template

```ruby
# spec/jobs/send_welcome_email_job_spec.rb
require 'rails_helper'

RSpec.describe SendWelcomeEmailJob, type: :job do
  let(:user) { create(:user) }

  describe '#perform' do
    it 'sends welcome email' do
      expect {
        described_class.perform_now(user.id)
      }.to have_enqueued_mail(UserMailer, :welcome)
    end
  end

  describe 'enqueueing' do
    it 'enqueues the job' do
      expect {
        described_class.perform_later(user.id)
      }.to have_enqueued_job(described_class)
        .with(user.id)
        .on_queue('default')
    end
  end

  describe 'retry behavior' do
    it 'retries on PaymentGatewayError' do
      expect(described_class).to have_retry_on(PaymentGatewayError)
    end
  end
end
```

### Test Helpers

```ruby
# spec/rails_helper.rb
RSpec.configure do |config|
  config.include ActiveJob::TestHelper
end

# In specs
it 'processes all jobs' do
  perform_enqueued_jobs do
    UserSignupService.call(user_params)
  end
  expect(user.reload.welcome_email_sent?).to be true
end

it 'enqueues multiple jobs' do
  expect {
    BatchProcessor.process(items)
  }.to have_enqueued_job(ProcessItemJob).exactly(items.count).times
end
```

## Running Solid Queue

```bash
# Development (runs in separate terminal)
bin/jobs   # Rails 8 binstub (equivalent: bin/rails solid_queue:start)

# Via Procfile.dev (this project's convention — docs/features/01.mvp-binance-realtime-chart.md 4-B)
# Procfile.dev
web: bin/rails server
jobs: bin/jobs
```

## Monitoring

### Mission Control (Web UI)

```ruby
# Gemfile
gem "mission_control-jobs"

# config/routes.rb
mount MissionControl::Jobs::Engine, at: "/jobs"
```

### Console Queries

```ruby
# Check pending jobs
SolidQueue::Job.where(finished_at: nil).count

# Check failed jobs
SolidQueue::FailedExecution.count

# Retry failed job
SolidQueue::FailedExecution.last.retry

# Clear old completed jobs
SolidQueue::Job.where('finished_at < ?', 1.week.ago).delete_all
```

## Migration from Sidekiq

| Sidekiq | Solid Queue |
|---------|-------------|
| `perform_async(args)` | `perform_later(args)` |
| `perform_in(5.minutes, args)` | `set(wait: 5.minutes).perform_later(args)` |
| `sidekiq_options queue: 'critical'` | `queue_as :critical` |
| `sidekiq_retry_in` | `retry_on` with `wait:` |
