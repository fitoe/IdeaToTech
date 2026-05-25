---
name: IdeaToTech
description: Use when a Javis/Kanban card needs technical planning, architecture seams, API/state/mock boundaries, implementation sequencing, risk classification, or verification strategy before coding.
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [technical-planning, architecture, verification, kanban-worker]
    related_skills: [PlanToDelivery, idea-to-design, design-to-code]
---

# IdeaToTech — Technical Specialist Worker

## Overview

IdeaToTech is a bounded technical planning specialist for Javis/Kanban. It turns a single active slice into decisions, implementation sequence, and verification expectations.

It does not own the project board, global gates, product/design approval, or implementation code. It may suggest Kanban updates; Javis decides and records them.

## When to Use

Use this skill when a card asks for technical blueprinting, implementation planning, API/state/mock strategy, dependency decisions, file-map planning, risk classification, or verification strategy.

Do not use it for visual exploration, design generation, routine CSS tweaks, or direct coding.

## Input Contract

Expect a Kanban card or equivalent handoff with:

```yaml
goal:
scope:
inputs:
allowed_changes:
acceptance:
evidence_required:
execution_mode: fast | controlled | strict
```

If the task arrives through strict P2D provider mode, honor the provided envelope/digest/permit/prewrite guard. Otherwise use the lightweight card contract and produce artifacts only in the permitted output path.

## Outputs

Return concise evidence that Javis can ingest:

```json
{
  "provider": "IdeaToTech",
  "result": "completed | partial | blocked | failed",
  "produced_artifacts": [],
  "decisions": [],
  "risks": [],
  "verification": [],
  "blockers": [],
  "suggested_kanban_updates": [],
  "review_required": false
}
```

Use files for heavy artifacts when needed:

- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- `api-contracts.json`
- `state-management-plan.json`
- `mock-to-real-plan.json`

## Planning Rules

1. Inspect nearby repo patterns before proposing new architecture.
2. Lock only decisions that affect dependencies, API seams, state shape, platform behavior, verification, or downstream sequencing.
3. Mark trivial local implementation choices as `defer_to_implementation`.
4. Classify each decision: `lock_now`, `spike_first`, `defer_to_implementation`, or `blocked`.
5. Distinguish mock/local/real maturity: F0 mock shape, F1 UI consumes mock, F2 local interaction, F3 adapter seam, F4 real happy path, F5 errors/permissions/regressions.
6. Never persist secret values; record variable names and setup requirements only.
7. If design/source approval is missing, suggest an `idea-to-design` card instead of inventing visuals.
8. If code must change, suggest a downstream implementation card instead of editing code here.

## Mode Behavior

| Mode | Behavior |
|---|---|
| `fast` | short decisions + file map + minimal checks |
| `controlled` | explicit decision table, risk list, verification matrix, downstream dependencies |
| `strict` | follow P2D envelope/digest/permit/prewrite/audit requirements exactly |

## Suggested Kanban Updates

Suggest a new card or gate when technical facts affect downstream start:

```yaml
title:
type: tech | implementation | verification | gate
reason:
depends_on:
acceptance:
evidence_required:
```

Do not create, complete, or approve project-level gates yourself.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Acting as architect for the whole project | Stay inside active slice unless global reconciliation is requested |
| Planning every tiny handler | Defer routine details to implementation |
| Hiding unknown API/auth | Emit blocker or mock-to-real plan with maturity label |
| Reporting mocks as real | Use F0-F5 labels and evidence |
| Choosing libraries without evidence | Prefer existing dependencies and local patterns |

## Verification Checklist

- [ ] Scope is the active card only.
- [ ] Decisions are classified and evidence-backed.
- [ ] API/auth/mock unknowns are explicit.
- [ ] Verification distinguishes mock/local/real/edge checks.
- [ ] Suggested Kanban updates are advisory and dependency-ready.
