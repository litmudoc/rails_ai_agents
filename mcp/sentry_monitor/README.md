# Sentry Monitor MCP Server

A Python MCP server that exposes Sentry production error data as tools for Claude Code. Query issues, inspect stack traces, track new errors, and map crashes to your local source files — all from within Claude Code.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- A Sentry account with an API auth token

## Setup

### 1. Install dependencies

```bash
cd mcp/sentry_monitor
uv sync --all-extras
```

### 2. Configure Sentry credentials

Create a `.env` file in this directory:

```
SENTRY_AUTH_TOKEN=sntryu_your_token_here
SENTRY_ORG=your-org-slug
SENTRY_PROJECT=your-default-project-slug
```

Your token needs scopes: `project:read`, `project:write`, `event:read`, `org:read`.

### 3. Register with Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "sentry-monitor": {
      "type": "stdio",
      "command": "/path/to/rails_ai_agents/mcp/sentry_monitor/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "PYTHONPATH": "/path/to/rails_ai_agents/mcp/sentry_monitor"
      }
    }
  }
}
```

Replace `/path/to/` with the actual absolute path. Then restart Claude Code.

### 4. Verify

```bash
# Test with MCP Inspector
uv run mcp dev mcp_server/server.py

# Or in Claude Code
/mcp  # should show sentry-monitor as connected
```

## Tools

### `list_issues`

List unresolved Sentry issues with filtering and pagination.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `project_slug` | from `.env` | Override the default project |
| `query` | `is:unresolved` | Sentry search syntax |
| `sort_by` | `date` | `date`, `freq`, `new`, `priority` |
| `environment` | all | Filter by environment (e.g., `production`) |
| `date_range` | `14d` | `24h` or `14d` |
| `page_size` | 25 | Max 100 |
| `cursor` | — | Pagination cursor from previous response |

### `get_issue_detail`

Get detailed info on a specific issue including stack trace, tags, and exception data.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `issue_id` | required | Sentry issue ID |
| `include_pii` | `false` | Include user context, request headers/body, local variables |

PII is **redacted by default**: user object, request headers/data, cookies, local variables, and breadcrumb data are stripped. Pass `include_pii=true` when you need full context for diagnosis.

### `map_stacktrace`

Map a Sentry stack trace to local repository files.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `issue_id` | required | Sentry issue ID |
| `repo_root` | cwd | Local repository root path |

Returns each frame with a confidence level:
- **exact** — full path matches a local file
- **partial** — filename found in a different directory
- **unmapped** — no local file found

Strips common deploy prefixes (`/app/`, `/home/*/`, `/var/www/`) before matching.

### `check_new_errors`

Check for new errors since the last poll. Maintains persistent state in `.claude/sentry-monitor-state.json` to avoid duplicate notifications across sessions.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `project_slug` | from `.env` | Override the default project |
| `environment` | all | Filter by environment |
| `state_file` | `.claude/sentry-monitor-state.json` | Path to state file |

State is pruned of entries older than 30 days. Corrupted state files are reset with a warning.

### `resolve_issue`

Update the status of a Sentry issue (resolve, ignore, or reopen). This is the only write operation — all other tools are read-only.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `issue_id` | required | Sentry issue ID |
| `status` | `resolved` | `resolved`, `ignored`, or `unresolved` |
| `in_next_release` | `false` | Resolve in the next release |
| `in_commit` | — | Commit SHA to resolve in (requires `in_repository`) |
| `in_repository` | — | Repository as `org/repo` for commit-based resolution |
| `ignore_duration` | `0` | Minutes to ignore the issue |

Requires `project:write` token scope.

### `get_server_status`

Health check — verifies Sentry connection, token validity, and state file status. No parameters.

## Monitoring multiple projects

The default project is set in `.env`, but every tool accepts a `project_slug` parameter. Just ask Claude naturally:

```
"List errors from project my-api"
"Check new errors in frontend-app"
```

## Companion skills

These Claude Code skills (installed separately in your project's `.claude/skills/`) orchestrate the MCP tools into workflows:

| Skill | Purpose |
|-------|---------|
| `/sentry:monitor` | Single monitoring cycle: detect new errors, analyze stack traces, propose fixes |
| `/sentry:fix-error` | Launch a background agent in an isolated git worktree to implement a fix |
| `/sentry:fix-status` | List active fix branches, merge or discard completed ones |
| `/sentry:resolve` | Resolve, ignore, or reopen a Sentry issue after a fix is deployed |
| `/sentry:report` | Generate a markdown error summary for standups, PRs, or sprint reviews |

Usage:
```
/loop 10m /sentry:monitor          # Check for new errors every 10 minutes
/sentry:fix-error 12345 Add nil check in payment_service.rb
/sentry:fix-status                 # Review and manage fix branches
/sentry:report 7d production        # Error summary for standups/PRs
/loop --cancel              # Stop the fix-error loop
```

## Project structure

```
mcp_server/
├── server.py           # FastMCP entry point, 6 tool definitions
├── sentry_client.py    # Async Sentry REST API client (httpx)
├── redactor.py         # PII field redaction
├── path_mapper.py      # Stack trace path → local file mapping
├── state.py            # Persistent already-seen issue tracking (JSON)
└── config.py           # Configuration from .env / environment variables

tests/
├── conftest.py         # Shared fixtures, mock Sentry API responses
├── test_sentry_client.py
├── test_redactor.py
├── test_path_mapper.py
├── test_state.py
└── test_tools.py       # MCP tool integration tests
```

## Testing

```bash
uv run pytest              # Run all 65 tests
uv run pytest -x           # Stop on first failure
uv run pytest -v           # Verbose output
uv run ruff check .        # Lint
uv run ruff format .       # Format
```

## Architecture

- **Transport**: stdio (Claude Code spawns the server as a subprocess)
- **HTTP client**: `httpx` (async, matches FastMCP's async tool model)
- **MCP SDK**: `mcp[cli]` with FastMCP high-level API
- **State**: Single JSON file for already-seen tracking, gitignored
- **PII**: Blocklist-based redaction with opt-in full context flag
