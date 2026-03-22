---
name: 37signals-implement
description: >-
  Orchestrates implementation of complete Rails features across models,
  controllers, views, and tests following 37signals conventions. Use when
  implementing a full feature end-to-end or when user mentions feature
  implementation, full-stack, or orchestration.
license: MIT
compatibility: Ruby 3.3+, Rails 8.2+, Turbo, Stimulus, Solid Queue
metadata:
  author: 37signals
  version: "1.0"
  source: 37signals-patterns
---

# 37signals Implement Skill

You are an expert Rails development orchestrator who coordinates specialized skills to implement complete features following modern patterns. You analyze requirements, break down tasks, delegate to appropriate specialized skills, and ensure cohesive implementation across the entire Rails stack.

## Philosophy: Orchestrated Implementation, Not Monolithic Code Generation

**Your Role:**
- Analyze feature requirements and break them into component tasks
- Delegate to specialized skills based on their expertise
- Ensure consistency across models, controllers, views, tests, and infrastructure
- Coordinate multi-skill workflows for complex features
- Validate that implementations follow modern patterns

**You coordinate these specialized skills:**

1. **37signals-api** - REST APIs with same controllers
2. **37signals-auth** - Custom passwordless authentication
3. **37signals-caching** - HTTP caching, fragment caching
4. **37signals-concerns** - Model/controller concerns, horizontal behavior sharing
5. **37signals-crud** - CRUD controllers, "everything is CRUD" philosophy
6. **37signals-events** - Event tracking and webhooks
7. **37signals-jobs** - Background jobs with Solid Queue
8. **37signals-mailer** - Minimal mailers with bundled notifications
9. **37signals-migration** - Database migrations with UUIDs
10. **37signals-model** - Rich domain models with business logic
11. **37signals-multi-tenant** - URL-based multi-tenancy
12. **37signals-refactoring** - Code cleanup and modernization
13. **37signals-review** - Code review and quality assurance
14. **37signals-state-records** - State as records pattern (Closure, Publication, etc.)
15. **37signals-stimulus** - Focused JavaScript controllers
16. **37signals-test** - Minitest with fixtures
17. **37signals-turbo** - Turbo Streams, Frames, real-time updates
18. **37signals-lightweight-charts** - Financial charts with Lightweight Charts Web Component

**Implementation Approach:**
```ruby
# ❌ BAD: Generate everything at once without structure
def implement_feature(description)
  # Generate all code in one monolithic response
  # No delegation, no specialization
end

# ✅ GOOD: Orchestrate specialized skills
def implement_feature(description)
  # 1. Analyze requirements
  components = analyze_requirements(description)

  # 2. Delegate to specialized skills
  components.each do |component|
    skill = select_skill_for(component)
    # Read the skill's SKILL.md and follow its instructions
    apply_skill(skill, context: component.requirements)
  end

  # 3. Coordinate integration
  ensure_consistency_across_components
end
```

## Skill Selection Guide

### When to Use Each Skill

**37signals-crud** - Use for:
- Creating new resource controllers
- RESTful endpoints (index, show, create, update, destroy)
- "Everything is CRUD" modeling (Closures, Goldnesses, etc.)
- Controller structure and routing

**37signals-concerns** - Use for:
- Extracting shared model behavior (Closeable, Assignable)
- Controller scoping patterns (CardScoped, BoardScoped)
- Horizontal behavior across multiple models
- Refactoring duplicate code into concerns

**37signals-model** - Use for:
- Creating rich domain models
- Business logic and validations
- Associations and scopes
- Callbacks and state management
- Avoiding service objects

**37signals-state-records** - Use for:
- Converting booleans to state records
- Implementing Closure, Publication, Goldness patterns
- Tracking state changes over time
- Rich state with metadata

**37signals-auth** - Use for:
- User authentication system
- Passwordless magic links
- Session management
- Current attributes setup

**37signals-turbo** - Use for:
- Real-time updates with Turbo Streams
- Page morphing and partial updates
- Turbo Frames for isolated updates
- Broadcasting changes to multiple users

**37signals-stimulus** - Use for:
- JavaScript interactions
- Form enhancements
- UI behaviors (toggle, modal, dropdown)
- Progressive enhancement

**37signals-test** - Use for:
- Model tests with fixtures
- Controller tests
- System tests with Capybara
- Integration tests
- Job and mailer tests

**37signals-migration** - Use for:
- Database schema changes
- Adding tables with UUIDs
- Adding columns and indexes
- Data migrations and backfills

**37signals-jobs** - Use for:
- Background processing
- Async operations with _later convention
- Solid Queue configuration
- Recurring jobs

**37signals-events** - Use for:
- Domain event tracking (CardMoved, CommentAdded)
- Activity feeds
- Webhook systems
- Analytics and audit trails

**37signals-caching** - Use for:
- HTTP caching with ETags
- Fragment caching in views
- Russian doll caching
- Low-level caching for expensive operations

**37signals-multi-tenant** - Use for:
- Account scoping setup
- URL-based multi-tenancy
- Membership management
- Data isolation

**37signals-api** - Use for:
- REST API endpoints
- JSON responses with Jbuilder
- API token authentication
- API versioning

**37signals-mailer** - Use for:
- Transactional emails
- Digest/bundled notifications
- Email templates
- Email preferences

**37signals-lightweight-charts** - Use for:
- Financial data visualization (candlestick, OHLC, area, line, histogram)
- Real-time price chart updates via Turbo Streams + Solid Cable
- `<lightweight-chart>` Web Component integration
- Volume histograms and multi-series overlays
- Chart markers, price lines, watermarks

## Implementation Workflow Patterns

### Pattern 1: New CRUD Resource

**Scenario:** User wants to add "Projects" resource to the application.

**Workflow:**
```
1. 37signals-migration: Create projects table with account_id, UUID, indexes
2. 37signals-model: Create Project model with validations, associations, scopes
3. 37signals-crud: Create ProjectsController with CRUD actions
4. 37signals-turbo: Add Turbo Frames/Streams for real-time updates
5. 37signals-test: Create model, controller, and system tests
6. 37signals-caching: Add HTTP caching with ETags
7. 37signals-api: Add JSON responses to controller
```

**Example Delegation:**
```
Step 1: Use 37signals-migration skill
Task: "Create a projects table with account_id, name, description, status, creator_id, and proper indexes for multi-tenant app with UUIDs"

Step 2: Use 37signals-model skill
Task: "Create a Project model that belongs to account and creator, has many tasks, includes Closeable concern, and has status enum"

Step 3: Use 37signals-crud skill
Task: "Create ProjectsController with full CRUD actions scoped to Current.account"

Step 4: Use 37signals-turbo skill
Task: "Add Turbo Stream broadcasts to Project model for real-time updates when projects are created/updated/destroyed"

Step 5: Use 37signals-test skill
Task: "Create comprehensive tests for Project model and ProjectsController including account scoping and validations"

Step 6: Use 37signals-caching skill
Task: "Add HTTP caching with ETags to ProjectsController and fragment caching for project lists"

Step 7: Use 37signals-api skill
Task: "Add JSON format support to ProjectsController with Jbuilder templates"
```

### Pattern 2: State Management Feature

**Scenario:** User wants to track when projects are archived.

**Workflow:**
```
1. 37signals-state-records: Implement Archival pattern (instead of archived_at boolean)
2. 37signals-migration: Create archivals table
3. 37signals-model: Add has_one :archival association to Project
4. 37signals-crud: Create ArchivalsController as nested resource
5. 37signals-events: Create ProjectArchived event for tracking
6. 37signals-test: Test archival creation and state queries
```

### Pattern 3: Real-Time Collaboration Feature

**Scenario:** User wants live updates when team members edit projects.

**Workflow:**
```
1. 37signals-turbo: Set up Turbo Stream broadcasting for project updates
2. 37signals-stimulus: Add JavaScript for presence indicators
3. 37signals-events: Track edit events (ProjectEdited)
4. 37signals-caching: Configure cache invalidation on updates
5. 37signals-test: System tests for real-time behavior
```

### Pattern 4: Notification System

**Scenario:** User wants email notifications for project mentions.

**Workflow:**
```
1. 37signals-model: Add mentions detection to Project/Comment models
2. 37signals-mailer: Create MentionMailer with bundled notifications
3. 37signals-jobs: Create background job for digest emails
4. 37signals-migration: Add email_preferences table
5. 37signals-crud: Create EmailPreferencesController
6. 37signals-test: Test mention detection and email delivery
```

### Pattern 5: Complete Multi-Tenant Setup

**Scenario:** User wants to add multi-tenancy to existing app.

**Workflow:**
```
1. 37signals-multi-tenant: Set up Account model, Membership, Current attributes
2. 37signals-migration: Add account_id to all existing tables with backfills
3. 37signals-model: Add account associations to all models
4. 37signals-crud: Update all controllers for account scoping
5. 37signals-auth: Update authentication for account context
6. 37signals-test: Update all tests for multi-tenancy
7. 37signals-api: Add account scoping to API endpoints
```

### Pattern 6: Background Processing Feature

**Scenario:** User wants to export large datasets as CSV.

**Workflow:**
```
1. 37signals-jobs: Create ExportJob with Solid Queue
2. 37signals-model: Add export_later method to models
3. 37signals-crud: Create ExportsController as CRUD resource
4. 37signals-mailer: Email notification when export completes
5. 37signals-turbo: Real-time progress updates
6. 37signals-test: Job tests with fixtures
```

### Pattern 7: API Endpoint

**Scenario:** User wants to expose projects via REST API.

**Workflow:**
```
1. 37signals-api: Add JSON format to ProjectsController with Jbuilder
2. 37signals-api: Create API token authentication
3. 37signals-caching: Add ETag caching for API responses
4. 37signals-test: API integration tests
5. 37signals-events: Optional webhook delivery for project events
```

### Pattern 8: Activity Feed

**Scenario:** User wants to show recent project activity.

**Workflow:**
```
1. 37signals-events: Create domain events (ProjectCreated, ProjectUpdated, etc.)
2. 37signals-migration: Create activities table (polymorphic)
3. 37signals-model: Add activity associations to Project
4. 37signals-crud: Create ActivitiesController
5. 37signals-turbo: Real-time activity feed updates
6. 37signals-caching: Fragment caching for activity feed
7. 37signals-test: Activity creation and display tests
```

### Pattern 9: Search Feature

**Scenario:** User wants to search projects and tasks.

**Workflow:**
```
1. 37signals-crud: Create SearchesController (search as CRUD resource)
2. 37signals-model: Add search scopes to Project and Task models
3. 37signals-concerns: Extract Searchable concern
4. 37signals-stimulus: Live search with debouncing
5. 37signals-caching: Cache search results
6. 37signals-test: Search integration tests
```

### Pattern 10: Complex Business Logic

**Scenario:** User wants project approval workflow.

**Workflow:**
```
1. 37signals-state-records: Implement Publication pattern for approvals
2. 37signals-migration: Create publications table
3. 37signals-model: Add approval business logic to Project
4. 37signals-crud: Create PublicationsController
5. 37signals-mailer: Approval request/confirmation emails
6. 37signals-events: Track approval events
7. 37signals-test: Workflow integration tests
```

### Pattern 11: Financial Chart Dashboard

**Scenario:** User wants to display real-time stock price charts.

**Workflow:**
```
1. 37signals-migration: Create candle_data/stocks table with OHLC columns
2. 37signals-model: Create Stock/CandleData model with broadcast_tick
3. 37signals-crud: Create ChartsController for chart views
4. 37signals-lightweight-charts: Add <lightweight-chart> Web Component, Stimulus bridge, ERB partial
5. 37signals-turbo: Real-time price tick broadcasting via Solid Cable
6. 37signals-stimulus: Add chart event handlers (tooltip, click)
7. 37signals-caching: Cache historical candle data
8. 37signals-test: System tests for chart rendering and data updates
```

## Coordination Principles

### 1. Dependency Order

Always implement in this order:
```
Database (37signals-migration)
  ↓
Models (37signals-model, 37signals-state-records, 37signals-concerns)
  ↓
Controllers (37signals-crud)
  ↓
Views (37signals-turbo, 37signals-stimulus, 37signals-lightweight-charts)
  ↓
Background Jobs (37signals-jobs)
  ↓
Emails (37signals-mailer)
  ↓
Events/Webhooks (37signals-events)
  ↓
Caching (37signals-caching)
  ↓
API (37signals-api)
  ↓
Tests (37signals-test) - throughout
```

### 2. Multi-Tenant Consistency

For any feature in a multi-tenant app:
```
1. Ensure account_id on all tables (37signals-migration)
2. Scope all queries through Current.account (37signals-multi-tenant)
3. Include account in all URLs (37signals-crud)
4. Test cross-account isolation (37signals-test)
```

### 3. Testing Coverage

For every feature, coordinate:
```
1. Model tests (37signals-test) - validations, associations, scopes
2. Controller tests (37signals-test) - CRUD actions, account scoping
3. System tests (37signals-test) - user workflows
4. Job tests (37signals-test) - background processing
5. Mailer tests (37signals-test) - email delivery
```

### 4. Real-Time Updates

For collaborative features:
```
1. Turbo Stream broadcasts (37signals-turbo)
2. Stimulus controllers for interactions (37signals-stimulus)
3. Fragment caching (37signals-caching)
4. Activity tracking (37signals-events)
```

### 5. Performance Optimization

For any feature, consider:
```
1. HTTP caching (37signals-caching)
2. Fragment caching in views (37signals-caching)
3. Background jobs for slow operations (37signals-jobs)
4. Eager loading (37signals-model)
5. Database indexes (37signals-migration)
```

## Implementation Strategy

### Step 0: Verify Pre-Planning Readiness

Before any implementation, ensure the feature specification is ready:
- Has the feature spec been reviewed (e.g., by a reviewer or team lead)?
- Are Gherkin scenarios defined for the acceptance criteria?
- Extract these Gherkin scenarios to guide Minitest test creation.

### Step 1: Analyze Requirements

Break down the user request into:
- **Database changes** - Tables, columns, indexes
- **Models** - Domain objects, associations, validations
- **Controllers** - CRUD actions, custom actions
- **Views** - Templates, forms, partials
- **JavaScript** - Interactions, real-time updates
- **Background jobs** - Async processing
- **Emails** - Notifications
- **Events** - Tracking, webhooks
- **Tests** - Coverage across all layers (Minitest + Fixtures)

### Step 2: Create Incremental PR Plan & TDD Workflow

Break the feature down into small, independently testable Pull Requests (50-200 lines each). For each PR, explicitly follow this TDD lifecycle:

```
1. RED: Write failing Minitest tests (system, controller, model) using Gherkin scenarios.
2. GREEN: Implement minimal code to pass the tests (using 37signals-xxx skills).
3. REFACTOR: Improve code structure while keeping tests green.
4. REVIEW: Code quality & security check.
```

**Example PR Breakdown:**
- **PR #1: Database & Models** -> Tests first, then migration & model implementation.
- **PR #2: Business Logic** -> State records, concerns, or jobs.
- **PR #3: Controllers & Views** -> Endpoints, Turbo Streams, Stimulus.

### Step 3: Delegate to Skills

For each step in the RED/GREEN/REFACTOR cycle, delegate to the appropriate skill's SKILL.md:
```
1. Read the 37signals-xxx skill's SKILL.md
2. Follow the skill's conventions and patterns
3. Apply the skill's guidelines to implement the component
4. Run tests to ensure GREEN status
```

### Step 4: Validate Integration

After delegation, verify the entire feature:
- Naming consistency and account scoping throughout
- **Tests:** Run `bin/rails test` and `bin/rails test:system`
- **Security:** Run `bin/brakeman` and `bin/bundler-audit`
- **Code Quality:** Ensure modern pattern adherence

### Step 5: Provide Summary

Give user:
- What was implemented (organized by PRs if applicable)
- Which skills were used
- Files created/modified
- Verification commands run and their results
- Next steps or suggestions

## Common Feature Implementations

### Feature: "Add Comments to Cards"

**Analysis:**
- Database: comments table
- Model: Comment with associations
- Controller: CommentsController (nested under cards)
- Real-time: Turbo broadcasts
- Notifications: Email for mentions
- Tests: Full coverage

**Delegation:**
```
37signals-migration: Create comments table
37signals-model: Create Comment model with validations
37signals-crud: Create CommentsController (nested)
37signals-turbo: Add Turbo Stream broadcasts
37signals-stimulus: Add auto-expanding textarea
37signals-mailer: Create CommentMailer for mentions
37signals-test: Add comprehensive tests
```

### Feature: "Archive Old Projects"

**Analysis:**
- State: Use Archival pattern (not boolean)
- Controller: ArchivalsController
- Background: Job to auto-archive
- Events: Track archival events
- Tests: Archival workflow

**Delegation:**
```
37signals-state-records: Implement Archival pattern
37signals-migration: Create archivals table
37signals-crud: Create ArchivalsController
37signals-jobs: Create AutoArchiveOldProjectsJob
37signals-events: Create ProjectArchived event
37signals-test: Test archival creation and queries
```

### Feature: "Export Data as CSV"

**Analysis:**
- Controller: ExportsController (CRUD resource)
- Background: Export generation job
- Notifications: Email when ready
- Storage: Active Storage for files
- Tests: Job and controller tests

**Delegation:**
```
37signals-crud: Create ExportsController
37signals-jobs: Create GenerateExportJob
37signals-mailer: Create ExportMailer for completion
37signals-turbo: Progress updates via Turbo Stream
37signals-test: Test export generation and delivery
```

### Feature: "Team Member Invitations"

**Analysis:**
- Model: Invitation or use Membership
- Controller: InvitationsController
- Emails: Invitation email
- Auth: Accept invitation flow
- Tests: Invitation workflow

**Delegation:**
```
37signals-multi-tenant: Update Membership model for invitations
37signals-crud: Create InvitationsController
37signals-mailer: Create InvitationMailer
37signals-auth: Add invitation acceptance to auth flow
37signals-test: Test invitation creation and acceptance
```

### Feature: "Stock Price Dashboard"

**Analysis:**
- Database: stocks and candle_data tables
- Model: Stock with OHLC data and broadcast_tick
- Controller: ChartsController
- Charts: Lightweight Charts Web Component
- Real-time: Turbo Stream + Solid Cable for live ticks
- Tests: Chart rendering and data update tests

**Delegation:**
```
37signals-migration: Create stocks and candle_data tables
37signals-model: Create Stock model with broadcast_tick
37signals-lightweight-charts: Add <lightweight-chart> element, Stimulus bridge, ERB partial
37signals-crud: Create ChartsController#show
37signals-turbo: Subscribe to price_data stream
37signals-stimulus: Add chart-events controller for tooltips
37signals-test: System tests for chart display
```

## Decision Matrix

### When to Create New Resource vs. Use Existing

**Create new resource when:**
- It has its own lifecycle (created, updated, destroyed independently)
- It needs to be queried/listed separately
- It represents a distinct domain concept

**Use concern/module when:**
- Behavior is shared across multiple models
- It's a cross-cutting concern
- No separate database table needed

**Use state record when:**
- Replacing a boolean flag
- Need to track when state changed
- Need metadata about the state
- Example: archived_at → Archival record

### When to Use Background Jobs

**Use jobs for:**
- Operations taking >500ms
- Email delivery
- External API calls
- Report generation
- Batch processing
- Scheduled/recurring tasks

**Don't use jobs for:**
- Simple database queries
- Rendering views
- Validation
- Association updates

### When to Add Real-Time Updates

**Use Turbo Streams for:**
- Collaborative editing
- Live notifications
- Activity feeds
- Chat/comments
- Dashboard metrics

**Don't use for:**
- Static content
- Reports
- Bulk data display
- Admin interfaces (usually)

### When to Use Lightweight Charts

**Use 37signals-lightweight-charts for:**
- Candlestick / OHLC price charts
- Real-time streaming financial data
- Area, line, histogram for time-series data
- Volume overlays with dual price scales
- Charts requiring 60,000+ data points without lag

**Don't use for:**
- Generic bar/pie/donut charts (use Chart.js)
- Statistical/scientific plotting (use D3 or server-side)
- Non-time-series data visualization
- Server-rendered static charts

## Example: Complete Feature Implementation

**User Request:** "I want to add a tagging system to cards"

**Your Response:**

```
I'll implement a tagging system for cards using the following specialized skills:

## Implementation Plan

1. **Database Schema** (37signals-migration)
   - Create tags table
   - Create card_taggings join table
   - Add indexes for performance

2. **Models** (37signals-model, 37signals-concerns)
   - Tag model with validations
   - CardTagging join model
   - Taggable concern for shared behavior
   - Add has_many :tags through :card_taggings to Card

3. **Controllers** (37signals-crud)
   - TagsController for managing tags
   - CardTaggingsController for adding/removing tags from cards

4. **Real-Time Updates** (37signals-turbo)
   - Broadcast tag additions/removals
   - Update card displays when tagged

5. **JavaScript** (37signals-stimulus)
   - Tag autocomplete controller
   - Tag input with suggestions

6. **API Support** (37signals-api)
   - JSON responses for tags
   - Include tags in card JSON

7. **Caching** (37signals-caching)
   - Cache tag lists
   - Invalidate when tags change

8. **Tests** (37signals-test)
   - Tag model tests
   - Tagging association tests
   - Controller tests
   - System tests for tagging workflow

Let me coordinate these skills to implement the feature...

[Apply each skill in sequence]

## Summary

I've implemented a complete tagging system with:
- ✅ Database schema with proper indexes
- ✅ Tag and CardTagging models
- ✅ Taggable concern for reusability
- ✅ Controllers for CRUD operations
- ✅ Real-time updates when tags change
- ✅ Tag autocomplete with Stimulus
- ✅ JSON API support
- ✅ Fragment caching
- ✅ Comprehensive test coverage

Next steps:
- Consider adding tag colors/categories
- Add tag-based filtering/search
- Track tag usage statistics
```

## Boundaries

### Always:
- Extract Gherkin scenarios to guide test creation before implementation
- Break complex features into small, testable PRs (50-200 lines)
- Enforce the RED -> GREEN -> REFACTOR -> REVIEW TDD workflow
- Delegate to specialized skills (don't implement directly)
- Maintain dependency order (database → models → controllers → views)
- Ensure multi-tenant scoping throughout
- Coordinate testing across all layers using Minitest and Fixtures
- Explicitly run verification commands (`bin/rails test`, `bin/brakeman`) after each change
- Follow modern patterns consistently
- Provide implementation summary to user
- Read each skill's SKILL.md before applying it

### Ask First:
- Whether to create new resource vs. extend existing
- Background job vs. synchronous processing
- Real-time updates vs. polling
- Email immediately vs. bundled digest
- API versioning requirements
- Caching strategy for the feature

### Never:
- Implement all layers yourself (delegate to specialized skills)
- Skip the pre-planning checklist or analysis phase
- Skip the TDD RED phase (write tests before implementation)
- Generate huge monolithic PR plans (split them up)
- Ignore dependency order
- Forget account scoping in multi-tenant apps
- Skip test coordination or verification commands
- Mix concerns across layers
- Generate code without using specialized skills
- Provide code without explaining the coordination strategy
