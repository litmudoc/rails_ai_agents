# Context Level 3

# Feature Specification Template

> Use this template to document a new feature BEFORE developing it.
> This document will guide the AI agent (or developers) in the implementation.

## Agent Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    📋 SPECIFICATION PHASE                        │
├─────────────────────────────────────────────────────────────────┤
│ 1. @feature_specification_agent → generates this document        │
│                         ↓                                        │
│ 2. @feature_reviewer_agent → review (score X/10)                │
│                         ↓                                        │
│    [If score < 7 or critical issues: revise]                    │
│                         ↓                                        │
│ 3. @feature_planner_agent → implementation plan                 │
├─────────────────────────────────────────────────────────────────┤
│                    🔴 RED PHASE (per PR)                         │
├─────────────────────────────────────────────────────────────────┤
│ 4. @tdd_red_agent → tests failing (Gherkin → RSpec)             │
├─────────────────────────────────────────────────────────────────┤
│                    🟢 GREEN PHASE (per PR)                       │
├─────────────────────────────────────────────────────────────────┤
│ 5. Specialist agents → minimal implementation                    │
│    • @model_agent, @migration_agent (database)                  │
│    • @service_agent, @form_agent (business logic)               │
│    • @policy_agent (authorization)                              │
│    • @controller_agent (endpoints)                              │
│    • @view_component_agent (UI components)                      │
│    • @tailwind_agent (styling with Tailwind CSS)                │
│    • @mailer_agent, @job_agent (async)                          │
├─────────────────────────────────────────────────────────────────┤
│                    🔵 REFACTOR PHASE (per PR)                    │
├─────────────────────────────────────────────────────────────────┤
│ 6. @tdd_refactoring_agent → improve code (tests green)          │
│                         ↓                                        │
│ 7. @lint_agent → fix style (Rubocop)                            │
├─────────────────────────────────────────────────────────────────┤
│                    ✅ REVIEW PHASE (per PR)                      │
├─────────────────────────────────────────────────────────────────┤
│ 8. @review_agent → code quality (SOLID, patterns)               │
│                         ↓                                        │
│ 9. @security_agent → security audit (Brakeman, vulnerabilities) │
│                         ↓                                        │
│    [If issues: return to step 5 or 6]                           │
├─────────────────────────────────────────────────────────────────┤
│                    🚀 MERGE & DEPLOY                             │
├─────────────────────────────────────────────────────────────────┤
│ 10. Merge PR → integration branch                               │
│                         ↓                                        │
│     [Repeat 4-10 for each PR step]                              │
│                         ↓                                        │
│ 11. Merge feature branch → main                                 │
│                         ↓                                        │
│ 12. Deploy → production                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Summary by Phase

| Phase | Agent(s) | Objective | Validation |
|-------|----------|-----------|------------|
| **Spec** | @feature_specification_agent | Create spec | - |
| **Review Spec** | @feature_reviewer_agent | Validate spec | Score ≥ 7/10 |
| **Plan** | @feature_planner_agent | Plan implementation | - |
| **RED** | @tdd_red_agent | Write failing tests | Tests red |
| **GREEN** | Specialist agents | Minimal code | Tests green |
| **REFACTOR** | @tdd_refactoring_agent | Improve code | Tests green |
| **LINT** | @lint_agent | Style & formatting | Rubocop clean |
| **REVIEW** | @review_agent | Code quality | No HIGH/CRITICAL issues |
| **SECURITY** | @security_agent | Security audit | Brakeman clean |
| **MERGE** | Developer | Integrate code | CI green |

---

## 📋 General Information

**Feature Name:** `[Short descriptive name]`

**Ticket/Issue:** `#[number]`

**Priority:** `[High / Medium / Low]`

**Estimation:** `[Small / Medium / Large]` or `[X days]`

---

## 🎯 Objective

**Problem to solve:**
> Describe in 2-3 sentences the business or user problem this feature solves.
> Example: "Users cannot filter restaurants by cuisine type, which makes searching difficult when they have a specific craving."

**Value provided:**
> What concrete benefit for the user or business?
> Example: "Improved user experience and 15% increase in conversion rate."

**Success criteria:**
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
- [ ] Measurable criterion 3

---

## 👤 Personas Involved

Check the impacted personas:
- [ ] Visitor (not authenticated)
- [ ] Logged-in User
- [ ] Resource Owner (Entity Owner)
- [ ] Administrator

> 📋 **For each checked persona**, document permissions in the Policies section below.

### Authorization Matrix

| Action | Visitor | User | Owner | Admin |
|--------|---------|------|-------|-------|
| View | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Create | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Edit | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Delete | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

---

## 📝 User Stories

### Main Story
```
As a [persona],
I want to [action],
So that [benefit].
```

**Acceptance Criteria:**
- [ ] Criterion 1 (measurable, verifiable by yes/no)
- [ ] Criterion 2 (measurable, verifiable by yes/no)
- [ ] Criterion 3 (measurable, verifiable by yes/no)

> ⚠️ **Note:** Criteria must be testable and avoid subjective terms like "good", "fast", "intuitive".

### Gherkin Scenarios (Acceptance Criteria)

> 📋 These scenarios will serve as the basis for acceptance tests with `@tdd_red_agent`.

```gherkin
Feature: [Feature name]

  Background:
    Given [common context]

  # Happy Path
  Scenario: [Main success scenario]
    Given [precondition]
    When [user action]
    Then [expected result]
    And [additional verification]

  # Validation
  Scenario: [Data validation]
    Given [precondition]
    When [action with invalid data]
    Then [error message displayed]
    And [data preserved in form]

  # Authorization
  Scenario: [Access control]
    Given [unauthorized user]
    When [attempting protected action]
    Then [redirect or error message]
```

### Secondary Stories (optional)
> If the feature is complex, list other stories with their own Gherkin scenarios.

---

## ⚠️ Edge Cases & Error Handling

> 🔴 **MANDATORY:** Document at least 3 edge cases.

### Identified Edge Cases

| # | Type | Scenario | Expected Behavior | Error Message |
|---|------|----------|-------------------|---------------|
| 1 | Invalid input | [Description] | [Behavior] | [Message] |
| 2 | Unauthorized access | [Description] | [Behavior] | [Message] |
| 3 | Empty/null state | [Description] | [Behavior] | [Message] |
| 4 | Network/system error | [Description] | [Behavior] | [Message] |
| 5 | Concurrent operation | [Description] | [Behavior] | [Message] |

### Gherkin Scenarios for Edge Cases

```gherkin
  # Edge Case: Invalid Input
  Scenario: User submits invalid data
    Given [precondition]
    When [action with invalid data]
    Then [expected behavior]
    And [specific error message]

  # Edge Case: Unauthorized Access
  Scenario: Unauthorized user attempts action
    Given I am logged in as [unauthorized persona]
    When I attempt to [protected action]
    Then I should see "[error message]"
    And I should be redirected to [destination]

  # Edge Case: Empty State
  Scenario: No data available
    Given [no data exists]
    When I visit [page]
    Then I should see "[empty state message]"
    And I should see [call to action]
```

---

## 🔄 Incremental PR Breakdown

> ⚠️ **IMPORTANT**: Never one-shot a large feature in a single PR.
>
> This section is **mandatory** for any feature estimated at more than one day of development.

### Integration Branch

**Branch name:** `feature/[feature-name]`

This branch will contain the entire feature but will only be merged into `main` once all incremental PRs are validated.

### Breakdown Plan

> Break down your feature into **5-10 small PRs** maximum (ideally 3-5).
> Each PR must:
> - Be less than 400 lines (ideally 50-200)
> - Have a single, clear objective
> - Be functional and tested (even if feature incomplete)
> - Target the integration branch (not main)

#### Step 1: [Short Title]
**Branch:** `feature/[name]-step-1-[description]`

**Objective:**
> 1-sentence description of what this PR does.
> Example: "Add migration and cuisine_type column to restaurants table"

**Content:**
- [ ] Migration `add_cuisine_type_to_restaurants`
- [ ] Index on column
- [ ] Migration tests (up/down)

**Estimation:** 30 min dev + 15 min review

**Tests included:**
- [ ] Reversible migration
- [ ] Index created correctly

---

#### Step 2: [Short Title]
**Branch:** `feature/[name]-step-2-[description]`

**Objective:**
> Example: "Add validations and filtering scope to Restaurant model"

**Content:**
- [ ] Constant `CUISINE_TYPES`
- [ ] Validation `inclusion` on `cuisine_type`
- [ ] Scope `by_cuisine`
- [ ] Model unit tests

**Estimation:** 1h dev + 30 min review

**Tests included:**
- [ ] Validation tests
- [ ] Scope tests
- [ ] Edge cases (nil, invalid value)

---

#### Step 3: [Short Title]
**Branch:** `feature/[name]-step-3-[description]`

**Objective:**
> Example: "Modify controller to accept cuisine filter"

**Content:**
- [ ] Modification of `RestaurantsController#index`
- [ ] Add `cuisine` parameter in strong params
- [ ] Request specs tests

**Estimation:** 1h dev + 30 min review

**Tests included:**
- [ ] Controller tests with/without filter
- [ ] Authorization tests if applicable

---

#### Step 4: [Short Title]
**Branch:** `feature/[name]-step-4-[description]`

**Objective:**
> Example: "Add filtering user interface"

**Content:**
- [ ] Filter form in `index.html.erb`
- [ ] Turbo Frame for dynamic reloading
- [ ] Tailwind styling

**Estimation:** 2h dev + 1h review

**Tests included:**
- [ ] Feature tests with Capybara
- [ ] JavaScript tests if complex interactions

---

#### Step 5: [Short Title] (optional)
**Branch:** `feature/[name]-step-5-[description]`

**Objective:**
> Example: "End-to-end integration tests and documentation"

**Content:**
- [ ] Complete integration tests
- [ ] Updated documentation
- [ ] Updated seeds

**Estimation:** 1h dev + 30 min review

**Tests included:**
- [ ] Complete user scenario
- [ ] Regression tests

---

### Merge Strategy

```bash
# 1. Create the integration branch
git checkout -b feature/[feature-name]
git push -u origin feature/[feature-name]

# 2. For each step:
git checkout feature/[feature-name]
git checkout -b feature/[name]-step-X-[description]
# ... develop ...
git commit -m "feat: step X description"
git push -u origin feature/[name]-step-X-[description]

# 3. Create a PR to the integration branch
gh pr create --base feature/[feature-name] \
  --title "[Step X/Y] Short description" \
  --body "Part of #[issue]. Detailed description."

# 4. Review + merge the step
# 5. Repeat for each step

# 6. Once all steps are merged:
gh pr create --base main \
  --title "Feature: [Full feature name]" \
  --body "Closes #[issue]. All incremental PRs reviewed and merged."
```

### Breakdown Checklist

- [ ] Feature is broken down into **3-10 steps maximum**
- [ ] Each step is **less than 400 lines**
- [ ] Each step is **autonomous and tested**
- [ ] Step order is **logical** (dependencies respected)
- [ ] Each step has a **time estimation**
- [ ] **Complete plan** is documented before starting

### Breakdown Rules

#### ✅ Good Breakdown
- Migration alone (step 1)
- Model + validations (step 2)
- Controller + routes (step 3)
- Views + components (step 4)
- Integration tests (step 5)

#### ❌ Bad Breakdown
- Migration + model + controller + views (too big)
- Just validations without tests (incomplete)
- Half of controller (not autonomous)
- All tests at the end (risky)

### For Coding Agents

When using a coding agent (Claude Code, GitHub Copilot, etc.):

**❌ Don't ask:**
```
"Completely implement the [name] feature"
```

**✅ Rather ask:**
```
"Implement Step 1 of feature spec [name]: [step 1 description]"
```

Then once Step 1 is reviewed and merged:
```
"Implement Step 2 of feature spec [name]: [step 2 description]"
```

And so on.

**Advantages:**
- 🎯 Focused context → fewer errors
- ✅ Quick review → immediate feedback
- 🔁 Easy correction → no total overhaul
- 📈 Visible progress → team confidence

---

## 🏗️ Technical Scope

### Impacted Models

#### New Models
```ruby
# If creating a new model
class NewModel < ApplicationRecord
  # Main attributes
  # - attribute_name: type (constraints)

  # Associations
  # belongs_to :xxx
  # has_many :yyy

  # Main validations
  # validates :xxx, presence: true
end
```

#### Existing Model Modifications
**Model:** `ExistingModel`

**Changes:**
- [ ] Add attribute: `new_attribute:string`
- [ ] Add relation: `has_many :new_relation`
- [ ] New validation: `validates :xxx, ...`
- [ ] New scope: `scope :by_xxx, -> { ... }`
- [ ] New method: `def calculate_xxx`

### Validation Rules

> 🔴 **MANDATORY:** For each user field, specify validation rules.

| Field | Type | Required | Validation Rules | Error Message |
|-------|------|----------|------------------|---------------|
| `name` | string | Yes | presence, length: 2..100 | "Name is required" |
| `email` | string | Yes | format: URI::MailTo::EMAIL_REGEXP | "Invalid email format" |
| `amount` | decimal | Yes | numericality: { greater_than: 0 } | "Amount must be positive" |
| `status` | string | Yes | inclusion: { in: STATUSES } | "Invalid status" |
| `description` | text | No | length: { maximum: 1000 } | "Description too long (max 1000)" |

### Migration(s)

```ruby
# db/migrate/YYYYMMDDHHMMSS_add_feature_name.rb
class AddFeatureName < ActiveRecord::Migration[8.1]
  def change
    # Add columns
    add_column :table_name, :column_name, :type, null: false, default: value

    # Add index
    add_index :table_name, :column_name

    # Create table
    create_table :new_table do |t|
      t.string :name, null: false
      t.references :parent, foreign_key: true
      t.timestamps
    end
  end
end
```

**⚠️ Migration Attention Points:**
- [ ] Reversible migration (`up`/`down` or `change` method)
- [ ] Indexes added on key columns
- [ ] Default values defined if necessary
- [ ] Foreign keys with appropriate `on_delete`

### Controllers

#### New Controllers
- `NewController` with actions: `index`, `show`, `new`, `create`, `edit`, `update`, `destroy`

#### Existing Controller Modifications
**Controller:** `ExistingController`

**Changes:**
- [ ] New action: `custom_action`
- [ ] Modify strong parameters
- [ ] Add before_action
- [ ] Modify business logic

**Strong parameters:**
```ruby
def model_params
  params.require(:model_name).permit(:attr1, :attr2, :attr3)
end
```

### Routes

```ruby
# config/routes.rb
resources :resource_name do
  # Nested routes if necessary
  resources :nested_resource, only: [:index, :create, :destroy]

  # Custom routes
  member do
    post :custom_action
  end

  collection do
    get :custom_collection_action
  end
end
```

### Services (if complex logic)

**Service:** `FeatureNameService`

**Responsibility:**
> Describe in 1-2 sentences what this service does.

**Main Methods:**
```ruby
class FeatureNameService
  def initialize(params)
    @params = params
  end

  def call
    # Complex business logic here
    # Returns a result or raises an exception
  end

  private

  def step_one
    # ...
  end
end
```

### Policies (Pundit)

**Policy:** `ModelPolicy`

**New Rules:**
```ruby
class ModelPolicy < ApplicationPolicy
  def action_name?
    # user.admin? || record.user == user
  end
end
```

### Views & Components

#### New Views
- `app/views/resource_name/index.html.erb`
- `app/views/resource_name/show.html.erb`
- `app/views/resource_name/_form.html.erb`

#### New Components
**Component:** `FeatureNameComponent`

```ruby
class FeatureNameComponent < ViewComponent::Base
  def initialize(param:)
    @param = param
  end

  def render?
    # Display condition
  end
end
```

#### Existing View Modifications
- [ ] View to modify: `path/to/view.html.erb`
- [ ] Type of modification: [Add link / New form / Data display]

### JavaScript (Stimulus)

#### New Stimulus Controllers
**Controller:** `feature_name_controller.js`

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["element"]
  static values = { param: String }

  connect() {
    // Initialization
  }

  action() {
    // Logic
  }
}
```

### Jobs (Background)

**Job:** `FeatureNameJob`

```ruby
class FeatureNameJob < ApplicationJob
  queue_as :default

  def perform(param)
    # Asynchronous processing
  end
end
```

**Trigger:**
- Where: `ModelName#method_name`
- When: `after_commit :enqueue_job`

---

## 🧪 Test Strategy

### Model Tests (RSpec)

**File:** `spec/models/model_name_spec.rb`

**Tests to Write:**
- [ ] Validations (presence, format, uniqueness, etc.)
- [ ] Associations (belongs_to, has_many, etc.)
- [ ] Scopes (verify SQL queries)
- [ ] Business methods (logic, edge cases)
- [ ] Callbacks (after_save, before_destroy, etc.)

**Test Examples:**
```ruby
RSpec.describe ModelName, type: :model do
  describe "validations" do
    it { should validate_presence_of(:attribute) }
    it { should validate_uniqueness_of(:attribute) }
  end

  describe "#custom_method" do
    it "returns expected result" do
      instance = create(:model_name)
      expect(instance.custom_method).to eq(expected_value)
    end
  end
end
```

### Controller Tests (Request specs)

**File:** `spec/requests/controller_name_spec.rb`

**Tests to Write:**
- [ ] CRUD actions (index, show, create, update, destroy)
- [ ] Authorizations (logged-in user, owner, etc.)
- [ ] Redirects and flash messages
- [ ] HTTP responses (200, 302, 404, 422, etc.)

**Test Examples:**
```ruby
RSpec.describe "ResourceName", type: :request do
  let(:user) { create(:user) }
  let(:resource) { create(:resource_name, user: user) }

  describe "GET /resources/:id" do
    it "returns http success" do
      get resource_path(resource)
      expect(response).to have_http_status(:success)
    end
  end

  describe "POST /resources" do
    context "with valid params" do
      it "creates a new resource" do
        expect {
          post resources_path, params: { resource_name: valid_attributes }
        }.to change(ResourceName, :count).by(1)
      end
    end
  end
end
```

### Integration Tests (Feature specs)

**File:** `spec/features/feature_name_spec.rb`

**Scenarios to Test:**
- [ ] Complete user journey (happy path)
- [ ] Error cases (invalid form, access denied)
- [ ] JavaScript interactions (if applicable)

**Test Examples:**
```ruby
RSpec.describe "Feature Name", type: :feature do
  scenario "user completes the feature workflow" do
    user = create(:user)
    login_as(user)

    visit new_resource_path
    fill_in "Name", with: "Example"
    click_button "Create"

    expect(page).to have_content("Resource created successfully")
    expect(page).to have_current_path(resource_path(ResourceName.last))
  end
end
```

### Component Tests

**File:** `spec/components/component_name_component_spec.rb`

**Tests to Write:**
- [ ] Rendering with different params
- [ ] Display conditions (`render?`)
- [ ] Generated content

### Policy Tests

**File:** `spec/policies/policy_name_spec.rb`

**Tests to Write:**
- [ ] Permissions by role
- [ ] Edge cases

```ruby
RSpec.describe ResourcePolicy, type: :policy do
  subject { described_class.new(user, resource) }

  context "for owner" do
    let(:user) { resource.user }
    it { should permit_action(:update) }
    it { should permit_action(:destroy) }
  end

  context "for other user" do
    let(:user) { create(:user) }
    it { should_not permit_action(:update) }
  end
end
```

---

## 🔒 Security Considerations

- [ ] **Strong parameters**: all attributes are filtered
- [ ] **Pundit authorizations**: all actions are protected
- [ ] **Validations**: all user inputs are validated
- [ ] **SQL injection**: use ActiveRecord, no raw SQL
- [ ] **XSS**: use Rails helpers (sanitize, escape)
- [ ] **CSRF**: tokens present on forms
- [ ] **Mass assignment**: use `permit` correctly
- [ ] **Sensitive data**: no logs or display of secrets

---

## ⚡ Performance Considerations

- [ ] **N+1 queries**: use `includes`/`preload`/`eager_load`
- [ ] **DB indexes**: add indexes on queried columns
- [ ] **Cache**: identify data to cache
- [ ] **Background jobs**: long tasks in async
- [ ] **Pagination**: limit list results
- [ ] **Heavy queries**: optimize with `select`, `pluck`, `exists?`

---

## 📱 UI/UX Considerations

> 🔴 **MANDATORY for features with UI:** Document interactive states.

### UI/UX Checklist
- [ ] **Responsive**: design adapted for mobile/tablet/desktop
- [ ] **Accessibility**: labels, aria-labels, contrast (WCAG 2.1 AA minimum)
- [ ] **User feedback**: flash messages, loading states
- [ ] **Client-side validation**: Stimulus + HTML5 validation
- [ ] **Error handling**: clear and actionable error messages

### Interactive States (Hotwire/Turbo)

| State | Description | Implementation |
|-------|-------------|----------------|
| **Loading** | During loading | Turbo Frame with spinner, `aria-busy="true"` |
| **Success** | Action succeeded | Flash notice, Turbo Stream append/replace |
| **Error** | Action failed | Flash alert, form preserved, inline errors |
| **Empty** | No data | Explanatory message + call-to-action |
| **Disabled** | Action unavailable | Disabled button + explanatory tooltip |

### User Messages

| Context | Type | Message |
|---------|------|---------|
| Creation succeeded | success | "[Resource] created successfully" |
| Update succeeded | success | "[Resource] updated" |
| Deletion succeeded | success | "[Resource] deleted" |
| Validation error | error | "Please correct the errors below" |
| Unauthorized | error | "You are not authorized to perform this action" |
| Not found | error | "[Resource] not found" |

---

## 🚀 Deployment Plan

### Prerequisites
- [ ] Migration tested (up & down)
- [ ] Seeds updated if necessary
- [ ] Assets precompiled (if CSS/JS changes)
- [ ] Environment variables added (if necessary)

### Steps
1. Deploy code
2. Run migrations: `rails db:migrate`
3. Restart workers if jobs added
4. Check logs
5. Test in production

### Rollback Plan
> How to revert if there's a problem?
```bash
# Migration rollback
rails db:rollback STEP=1

# Redeploy previous version
kamal rollback
```

---

## 📚 Documentation to Update

- [ ] `README.md`: if major feature
- [ ] `.github/project.md`: if new main functionality
- [ ] `.github/CONTRIBUTING.md`: if new conventions
- [ ] API docs: if exposed endpoints
- [ ] User guide: if user-visible feature

---

## ✅ Final Checklist Before Merge

### Code
- [ ] Code written and functional
- [ ] Rubocop passes without errors
- [ ] No commented code or `binding.pry`
- [ ] Nomenclature respected

### Tests
- [ ] All tests pass
- [ ] Coverage maintained (>90%)
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Edge cases tested

### Security
- [ ] Brakeman reports no new vulnerabilities
- [ ] Bundler Audit OK
- [ ] Policies tested
- [ ] Strong parameters verified

### Documentation
- [ ] Code commented if complex logic
- [ ] README updated if necessary
- [ ] CHANGELOG.md updated

### Review
- [ ] PR created with clear description
- [ ] Screenshots/GIF if UI changes
- [ ] Reviewer assigned
- [ ] CI/CD green

---

## 💡 Notes & Questions

> Free space to note questions, technical decisions, or specific attention points.

**Open Questions:**
-

**Technical Decisions:**
-

**Attention Points:**
-

**External Dependencies:**
-

---

**Creation Date:** `[YYYY-MM-DD]`

**Author:** `[@username]`

**Reviewers:** `[@username1, @username2]`

**Status:** `[Draft / In Review / Ready for Dev / In Progress / Completed]`

---

## 📋 Review Criteria (@feature_reviewer_agent)

> This section summarizes the criteria that `@feature_reviewer_agent` will verify.

### MUST HAVE (Blocking if absent)
- [ ] Objective and value clearly stated
- [ ] Personas identified
- [ ] Main user story documented
- [ ] Testable acceptance criteria (verifiable by yes/no)
- [ ] Gherkin scenarios for acceptance tests
- [ ] Edge cases documented (minimum 3)
- [ ] Complete authorization matrix

### SHOULD HAVE (Recommended)
- [ ] Validation rules table
- [ ] Technical components listed
- [ ] Database changes documented
- [ ] Pundit policies specified
- [ ] Integration points identified

### IF UI (Mandatory if UI feature)
- [ ] Loading/error/empty/success states documented
- [ ] User messages defined
- [ ] Responsive behavior specified
- [ ] Accessibility considered (WCAG 2.1 AA)

### IF Medium/Large (Mandatory if > 1 day)
- [ ] PR breakdown (3-10 steps)
- [ ] Each PR < 400 lines (ideally 50-200)
- [ ] Clear dependencies between PRs
- [ ] Tests included in each PR
