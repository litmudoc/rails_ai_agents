# Claude Code Frontmatter Reference

Practical reference for YAML frontmatter in `.claude/` markdown files.
Based on official docs at [code.claude.com](https://code.claude.com/docs/en/sub-agents) (March 2026).

---

## Agents (`.claude/agents/*.md`)

Agent files define specialized subagents with custom system prompts and tool restrictions.

```yaml
---
name: my-agent                    # Required. Lowercase + hyphens
description: When to use this     # Required. Claude uses this for delegation
tools: Read, Write, Edit, Bash    # Optional. Inherits all if omitted
disallowedTools: Write, Edit      # Optional. Denylist (applied before tools)
model: sonnet                     # Optional. sonnet|opus|haiku|inherit|full-id
permissionMode: acceptEdits       # Optional. default|acceptEdits|dontAsk|bypassPermissions|plan
maxTurns: 30                      # Optional. Max agentic turns
effort: medium                    # Optional. low|medium|high|max (max = Opus only)
memory: project                   # Optional. user|project|local
skills:                           # Optional. Preloaded skill content
  - skill-name
mcpServers:                       # Optional. MCP servers for this agent
  - server-name                   #   String ref to existing server
  - custom-server:                #   Or inline definition
      type: stdio
      command: npx
      args: ["-y", "package"]
hooks:                            # Optional. Lifecycle hooks scoped to agent
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
background: false                 # Optional. Always run in background
isolation: worktree               # Optional. Run in isolated git worktree
initialPrompt: "Start by..."     # Optional. Auto-submitted first turn (--agent mode only)
---

System prompt goes here in markdown.
```

### Tool restrictions

- `tools` = allowlist. Only these tools available.
- `disallowedTools` = denylist. Removed from inherited pool.
- If both set: `disallowedTools` applied first, then `tools` resolved.
- Use `Agent(worker, researcher)` in `tools` to restrict spawnable subagents.

### Model resolution order

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
2. Per-invocation model parameter
3. Agent `model` frontmatter
4. Main conversation model

---

## Skills (`.claude/skills/*/SKILL.md`)

Skills extend Claude with reusable instructions. Invoked via `/skill-name` or auto-loaded.

```yaml
---
name: my-skill                        # Optional. Defaults to directory name
description: What and when to use     # Recommended. Truncated at 250 chars in listing
argument-hint: "[issue-number]"       # Optional. Shown in autocomplete
disable-model-invocation: true        # Optional. Only user can invoke via /name
user-invocable: false                 # Optional. Only Claude can invoke
allowed-tools: Read, Grep, Glob      # Optional. Tool allowlist when skill is active
model: sonnet                         # Optional. Model override when active
effort: high                          # Optional. low|medium|high|max
context: fork                         # Optional. Run in isolated subagent context
agent: Explore                        # Optional. Subagent type when context: fork
paths: "app/**/*.rb, spec/**/*.rb"    # Optional. Glob patterns for auto-activation
hooks:                                # Optional. Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
shell: bash                           # Optional. bash|powershell
---

Skill instructions in markdown.
Use $ARGUMENTS for passed args, $0/$1 for positional.
Use !`command` for dynamic context injection.
```

### Invocation control

| Frontmatter                      | User | Claude | Context loading                    |
|----------------------------------|------|--------|------------------------------------|
| (default)                        | Yes  | Yes    | Description always, full on invoke |
| `disable-model-invocation: true` | Yes  | No     | Not in context                     |
| `user-invocable: false`          | No   | Yes    | Description always, full on invoke |

### String substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$ARGUMENTS[N]` / `$N` | Positional argument (0-based) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing SKILL.md |

---

## Commands (`.claude/commands/**/*.md`)

Commands use the same frontmatter as skills. A file at `.claude/commands/deploy.md` creates `/deploy`.

```yaml
---
name: my-command                  # Optional
description: What this does       # Recommended
argument-hint: "[args]"           # Optional
disable-model-invocation: true    # Optional
allowed-tools: Read, Bash         # Optional
context: fork                     # Optional
agent: general-purpose            # Optional
handoffs:                         # Optional. Workflow chaining (custom convention)
  - label: Next Step
    agent: other:command
    prompt: Continue with...
    send: true
---

Command instructions with $ARGUMENTS support.
```

---

## Rules (`.claude/rules/*.md`)

Rules are auto-loaded context based on file paths being worked on.

```yaml
---
globs: "app/models/**/*.rb, spec/models/**/*.rb"   # Comma-separated glob patterns
---

Rule content loaded when Claude works with matching files.
```

### `globs` vs `paths`

The docs reference `paths` but there are known issues ([#17204](https://github.com/anthropics/claude-code/issues/17204), [#16299](https://github.com/anthropics/claude-code/issues/16299)) where YAML list format loads globally. The `globs` field with comma-separated strings is the reliable alternative. Both accept the same glob syntax.

---

## Fields NOT recognized

These fields are ignored by Claude Code and waste context tokens:

- `license` - not a frontmatter field
- `compatibility` - not a frontmatter field
- `metadata` / `author` / `version` - not frontmatter fields

---

## References

- [Subagents docs](https://code.claude.com/docs/en/sub-agents)
- [Skills docs](https://code.claude.com/docs/en/slash-commands)
- [Settings docs](https://code.claude.com/docs/en/settings)
- [Hooks docs](https://code.claude.com/docs/en/hooks)
