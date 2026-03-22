# Global OpenCode Configuration

## Identity
- GitHub: litmudoc
- Primary Language: Ruby/Rails

## ABSOLUTE RULES - NEVER VIOLATE

### Secrets Protection
- NEVER output passwords, API keys, or tokens to any file
- NEVER read or output contents of:
  - .env, .env.*, config/master.key
  - config/credentials.yml.enc (encrypted, but don't expose)
  - .kamal/secrets
  - Any *.pem, *.key files
- NEVER commit secrets to git
- NEVER hardcode credentials in source files
- ALWAYS use Rails credentials or environment variables for secrets

### Dangerous Operations
- NEVER run rm -rf on root, home, or parent directories
- NEVER force push to main, master, or production branches
- NEVER use chmod 777
- NEVER run database commands without confirmation (db:drop, db:reset in production)

### Before Every Commit
1. Run bin/rubocop to check style
2. Run bin/rails test to verify tests pass
3. Run bin/brakeman to check security
4. Verify no .env or secret files are staged

## New Project Standards

### Required Files
- .env.example (template with placeholder values)
- .gitignore (must include .env, config/master.key)
- README.md
- AGENTS.md (project-specific instructions)

### Rails Conventions
- Follow Rails conventions over configuration
- Use Rails credentials for secrets (bin/rails credentials:edit)
- Prefer Hotwire over heavy JavaScript frameworks
- Use Stimulus for JS interactivity
- Use Turbo for SPA-like navigation
- Write tests for all new functionality
- **Philosophy:** Minitest over RSpec, Fixtures over Factories, Fat models, "Everything is CRUD".

### AI Skills Integration
- **ALWAYS** check for and utilize available local skills in `skills/` or `.agents/skills/` directories before generating generic Rails code.
- Prefer orchestrator skills (like `skills/37signals-implement/SKILL.md`) when starting new features.

## Quality Gates
- Max 100 lines per controller action
- Max 50 lines per model method
- Extract service objects for complex business logic
- Use concerns for shared model/controller behavior
