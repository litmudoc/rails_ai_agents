# Specification Document Hierarchy

A reference map of the documents that govern an agentic SDLC workflow — what each one answers, who owns it, and when it is written.

---

## The Core Question Each Document Answers

```
What should we build, and why?   →  Product Requirements Document (PRD)
How should we build it?          →  Technical Design Document (TDD) / RFC
Why did we decide this way?      →  Architecture Decision Record (ADR)
How should it look and behave?   →  UI/UX Design Specification
How do services talk to each other? →  API Specification (OpenAPI)
```

---

## Document Map

| Document | Answers | Primary Author | AI Agent Use |
|---|---|---|---|
| [PRD](./prd-best-practices.md) | What + Why | Product / Tech Lead | Generates features, user stories, acceptance criteria |
| [TDD / RFC](./technical-design-document.md) | How (system) | Engineering Lead | Drives code generation, component scaffolding |
| [ADR](./technical-design-document.md#architecture-decision-records) | Why this approach | Any engineer | Context for constraint-aware code generation |
| [Design Spec](./design-specification.md) | How (UI/UX) | Designer / Frontend Lead | Token extraction, component generation, a11y validation |
| [API Spec](./design-specification.md#api-specification) | How (contracts) | Backend Lead | Tool/function schemas, MCP server generation, contract testing |

---

## Lifecycle Order

```
Discovery → Planning → Design → Implementation → Review
    │            │        │            │             │
   PRD          TDD    Design       ADRs           RFCs
               RFC      Spec      (ongoing)     (as needed)
                        API Spec
```

Documents are not strictly sequential — ADRs and RFCs are written whenever a significant decision or proposal arises.

---

## What Belongs Where

**PRD** — user-facing scope only. No implementation details, no technology choices.

**TDD / RFC** — system internals: data models, component breakdown, infrastructure, algorithms. No UI copy, no business rationale.

**ADR** — a single decision, immutable once accepted. Not a design document; not a meeting note.

**Design Spec** — visual and interaction contracts: component states, design tokens, accessibility requirements. Not a wireframe tool; not a copy deck.

**API Spec** — the machine-readable contract between services: endpoints, schemas, error codes. Not a tutorial; not internal implementation detail.

---

## Deeper Reading

- [PRD Best Practices](./prd-best-practices.md)
- [Technical Design Document, ADRs & RFCs](./technical-design-document.md)
- [UI/UX Design Spec & API Specification](./design-specification.md)
