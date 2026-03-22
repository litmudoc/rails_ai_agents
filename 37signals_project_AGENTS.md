# rails Project Guide

## Overview
Modern Rails 8 application using the Solid trifecta (Cache, Queue, Cable) with SQLite, Hotwire frontend, and Kamal deployment.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Rails 8.2.0.alpha |
| Ruby | 3.3.6 |
| Database | SQLite 3 |
| Time-series DB | TimescaleDB |
| Frontend | Hotwire (Turbo + Stimulus) |
| Styling | Tailwind CSS |
| Assets | Propshaft + Import Maps |
| Testing | Minitest + Capybara |
| Linting | RuboCop (omakase) |
| Deployment | Kamal + Docker |
| Jobs | Solid Queue |
| Cache | Solid Cache |
| WebSockets | Solid Cable |

## Project Structure

```
app/
├── controllers/     # Request handling
├── models/          # Business logic & data
├── views/           # ERB templates
├── helpers/         # View helpers
├── jobs/            # Background jobs (Solid Queue)
├── mailers/         # Email sending
├── channels/        # ActionCable channels
└── javascript/
    └── controllers/ # Stimulus controllers

config/
├── routes.rb        # URL routing
├── database.yml     # Database config (SQLite)
├── deploy.yml       # Kamal deployment
├── importmap.rb     # JavaScript imports
└── initializers/    # App initialization

test/
├── models/          # Unit tests
├── controllers/     # Controller tests
├── integration/     # Integration tests
├── system/          # Browser tests (Capybara)
└── fixtures/        # Test data
```

## Development Commands

```bash
# current directory with run to create a Rails app that should satisfy most development environments.
rails new . --master --css=tailwind --javascript=importmap --database=sqlite3  # Create a new Rails application in the current directory.

# Setup
bin/setup              # Initialize development environment

# Development
bin/dev                # Start dev server (Rails + Tailwind watch)
bin/rails server       # Rails only
bin/rails console      # Rails console

# Testing
bin/rails test         # Run unit/integration tests
bin/rails test:system  # Run browser tests
bin/ci                 # Full CI suite locally

# Code Quality
bin/rubocop            # Check Ruby style
bin/rubocop -a         # Auto-fix style issues
bin/brakeman           # Security scan

# Database
bin/rails db:migrate   # Run migrations
bin/rails db:seed      # Seed data
bin/rails db:reset     # Reset database (CAREFUL!)

# Deployment
kamal setup            # Initial server setup
kamal deploy           # Deploy to production
kamal app logs         # View production logs
```

## Conventions

### Controllers
- Keep actions thin (< 10 lines ideally)
- Use before_action for auth/setup
- Respond with Turbo Streams for dynamic updates
- Use strong parameters

```ruby
# Good
def create
  @post = Post.new(post_params)
  if @post.save
    redirect_to @post, notice: "Created!"
  else
    render :new, status: :unprocessable_entity
  end
end

private

def post_params
  params.require(:post).permit(:title, :body)
end
```

### Models
- Validations at the top
- Associations after validations
- Scopes before methods
- Extract complex queries to scopes
- Use callbacks sparingly

```ruby
class Post < ApplicationRecord
  # Validations
  validates :title, presence: true, length: { maximum: 255 }
  validates :body, presence: true

  # Associations
  belongs_to :user
  has_many :comments, dependent: :destroy

  # Scopes
  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc) }

  # Methods
  def publish!
    update!(published: true, published_at: Time.current)
  end
end
```

### Views
- Use partials for reusable components
- Prefix partials with underscore (_partial.html.erb)
- Use Turbo Frames for partial page updates
- Use Turbo Streams for real-time updates

```erb
<%# Turbo Frame for in-place editing %>
<%= turbo_frame_tag @post do %>
  <h1><%= @post.title %></h1>
  <%= link_to "Edit", edit_post_path(@post) %>
<% end %>
```

### Stimulus Controllers
- One controller per behavior
- Use data attributes for configuration
- Keep controllers small and focused

```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]

  toggle() {
    this.contentTarget.classList.toggle("hidden")
  }
}
```

### Testing
- Test behavior, not implementation
- Use fixtures for test data
- System tests for critical user flows
- Run tests before committing

```ruby
# test/models/post_test.rb
class PostTest < ActiveSupport::TestCase
  test "requires title" do
    post = Post.new(body: "content")
    assert_not post.valid?
    assert_includes post.errors[:title], "can't be blank"
  end
end
```

## Security

### Credentials
- Use `bin/rails credentials:edit` to manage secrets
- Never commit config/master.key
- Use environment-specific credentials for staging/production

```ruby
# Access credentials
Rails.application.credentials.secret_api_key
Rails.application.credentials.dig(:aws, :access_key_id)
```

### Environment Variables
- Use .env for local development (never commit)
- Copy .env.example to .env and fill values
- Kamal uses .kamal/secrets for deployment

### Protected Files (NEVER read/output)
- .env, .env.*
- config/master.key
- config/credentials.yml.enc
- .kamal/secrets
- storage/*.sqlite3

## Deployment

### Kamal Commands
```bash
kamal setup            # First-time server setup
kamal deploy           # Deploy latest code
kamal rollback         # Rollback to previous version
kamal app logs         # View application logs
kamal app console      # Rails console on server
```

### Pre-deployment Checklist
1. All tests passing: `bin/rails test && bin/rails test:system`
2. No security issues: `bin/brakeman`
3. No vulnerable gems: `bundle audit`
4. Assets precompile: `bin/rails assets:precompile`

## 37signals AI Skills Framework

This project utilizes a specialized ecosystem of AI skills located in `skills/`. You **must** leverage these skills for code generation and feature planning instead of relying on generic Rails knowledge.

### The Master Orchestrator
When asked to implement a new feature or complex logic, **ALWAYS read and follow `skills/37signals-implement/SKILL.md` first.**
- It acts as the primary feature planner.
- It enforces a strict `RED -> GREEN -> REFACTOR -> REVIEW` TDD workflow.
- It guides you in breaking down massive tasks into small (50-200 line) Pull Requests.

### Key Specialized Skills
You should delegate tasks to these specialized skills during the `GREEN` phase of implement orchestration:
- `37signals-crud` - RESTful state-change controllers
- `37signals-model` - Rich domain models (avoid service objects)
- `37signals-turbo` & `37signals-stimulus` - Hotwire frontend interactions
- `37signals-test` - Testing utilizing Minitest + Fixtures
- `37signals-lightweight-charts` - Financial data charts and real-time updates

## Notes for OpenCode

### Do
- **Follow the 37signals skills framework (`skills/*`) for all code generation.**
- Start any new feature implementation by referencing `skills/37signals-implement/SKILL.md`.
- Follow existing patterns in the codebase
- Write tests for new functionality using Minitest
- Use Rails conventions and Hotwire
- Keep methods small and focused

### Don't
- Read or expose any files in "Protected Files" section
- Commit directly to main branch
- Skip the TDD testing phase (RED phase)
- Generate generic, monolithic PRs
- Add unnecessary gems
- Over-engineer solutions
