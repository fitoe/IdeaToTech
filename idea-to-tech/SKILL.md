---
name: IdeaToTech
description: Use when product features, page behaviors, existing project constraints, APIs, dependencies, state management, mocks, or verification strategy need to be converted into an implementation-ready technical blueprint before coding.
---

# IdeaToTech

## Overview

Turn product ideas, feature behavior, existing repository constraints, and integration facts into a compact technical implementation blueprint.

This skill is not a UI designer and not a coding executor. It decides **how functionality should be implemented** so implementation agents can move quickly without choosing libraries, state shape, API boundaries, mock strategy, or verification strategy during coding.

Default outcome:
- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- optional `api-contracts.json`, `state-management-plan.json`, `mock-to-real-plan.json`, and `integration-plan.json`
- checker-passing `technical_gate`

Standalone rule:
- this skill can be used directly or routed by `PlanToDelivery`
- `idea-to-design` may provide product/page/interaction inputs
- `design-to-code` consumes outputs during implementation

Core rule:
- implementation-time decisions should be front-loaded when they affect speed, consistency, dependencies, data flow, API integration, state, or verification
- do not invent unsupported technology choices when the repository already has conventions
- prefer existing code, installed dependencies, and project conventions before adding libraries
- add dependencies only when the feature complexity justifies them and the decision is recorded
- risky or uncertain approaches require a small spike before locking the decision
- keep outputs machine-readable and compact; long prose is traceability, not the default implementation input

## When to Use

Use when:
- implementation would otherwise need to choose libraries or architecture during coding
- features need API, state, mock, permission, streaming, upload, charting, map, form, or cache strategy
- a project needs mock-to-real transition planning
- `design-to-code` needs functional/technical inputs in addition to visual blueprint
- `PlanToDelivery` needs a technical gate before execution

Do not use when:
- the task is only visual style exploration
- the feature is tiny and the existing project pattern is obvious
- the user only asks for final code and no meaningful technical decision exists
- the task is backend-only architecture beyond the current implementation milestone; use a system architecture skill or project-specific planning instead

## Decision Classes

Classify every technical decision:

- `lock_now`: safe to decide from current repo conventions and known requirements
- `spike_first`: needs a small experiment before locking
- `defer_to_implementation`: too small or too local to plan in advance
- `blocked`: needs missing API/credential/security/product information

Do not pretend a `spike_first` or `blocked` decision is implementation-ready.

## Workflow

### 1. Intake
Read only what is needed:
- product/feature requirements
- existing repo stack and conventions
- package manager and dependencies
- routing, state, request, component, test, and mock patterns
- known APIs and authentication constraints
- visual/page blueprint if UI implementation will follow

Output an assumption list and mark missing facts.

### 2. Dependency Decisions
Create or update `technical-decisions.json`.

For each dependency or technical approach, record:
- feature/use case
- selected approach or library
- status: `lock_now`, `spike_first`, `defer_to_implementation`, or `blocked`
- reason
- alternatives considered
- install command when needed
- usage boundary
- owned files or modules
- rollback/fallback plan

Dependency rule:
1. existing project code
2. installed dependency
3. mature new dependency
4. custom implementation

### 3. Feature Recipes
Create or update `feature-recipes.json`.

For each feature, define:
- target pages/routes/components
- service/composable/store/module boundaries
- data source and adapter plan
- loading/empty/error states
- mock behavior and real replacement source
- permission/auth considerations
- cache/persistence strategy
- user feedback and failure recovery
- verification items
- maturity target for current milestone

Recipes must be executable by an implementation agent without re-deciding architecture.

### 4. API and Integration Contracts
Create `api-contracts.json` or `integration-plan.json` when APIs or external services matter.

Record:
- endpoint or SDK method
- request shape
- response shape
- pagination/streaming/upload semantics
- auth requirements
- error codes and retries
- mock adapter shape
- adapter location
- unknowns/blockers

Never store secrets, tokens, passwords, or private connection strings. Use placeholders such as `[REDACTED]` or environment variable names.

### 5. State Management Plan
Create `state-management-plan.json` when state is non-trivial.

Classify state as:
- component local
- route/query
- store/global
- server cache
- local persistence
- real-time/subscription

Record ownership, lifecycle, reset conditions, and persistence rules.

### 6. Mock-to-Real Plan
Create `mock-to-real-plan.json` when mock/demo data will precede real integration.

Record:
- mock area
- current behavior
- real source
- replacement stage
- adapter seam
- visible label requirement
- verification needed before claiming real functionality

Mock is allowed as planned delivery. Fake completion is not.

### 7. Verification Matrix
Create `verification-matrix.json`.

For each feature/decision, define:
- unit checks
- integration checks
- E2E/manual checks
- build/type/lint expectations
- mock vs real acceptance
- risk level
- blocking vs non-blocking failures

### 8. Technical Gate
Open `technical_gate` only when:
- required decisions are `lock_now` or explicitly deferred
- `spike_first` decisions have spike results or are out of current scope
- blockers are resolved or user-waived
- required files exist
- checker passes

## Outputs

Default compact package:

```text
technical-decisions.json
feature-recipes.json
verification-matrix.json
```

Expanded package when needed:

```text
api-contracts.json
state-management-plan.json
mock-to-real-plan.json
integration-plan.json
technical-spikes/
  <decision-id>.md
```

## Handoff to DesignToCode

`design-to-code` should read:
1. visual `implementation-blueprint.json` when UI exists
2. `technical-decisions.json`
3. current-scope entries from `feature-recipes.json`
4. current-scope entries from `verification-matrix.json`
5. optional API/state/mock files only when the current feature references them

If visual and technical blueprints conflict:
- product behavior and security constraints outrank visual convenience
- approved visual layout still governs UI structure unless a change request/deviation is recorded
- record accepted deviations instead of improvising in code

## Token Budget

Keep files short and indexed.
- Use IDs and file refs instead of repeating long explanations.
- Do not load all recipes for one small feature.
- Put heavy spike notes under `technical-spikes/` and reference them.
- Prefer JSON for implementation inputs and short Markdown only for spike results.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Choosing new libraries before reading package.json | Inspect existing stack first |
| Treating guesses as decisions | Mark `spike_first` or `blocked` |
| Planning every tiny helper | Mark local details `defer_to_implementation` |
| Mock behavior reported as real | Use mock-to-real plan and verification matrix |
| API unknowns hidden in prose | Put blockers in contracts and gate |
| design-to-code picks libraries during coding | Move selection into `technical-decisions.json` first |

## Success Criteria

This skill succeeds when:
- implementation agents know which libraries and approaches to use
- feature code has clear service/store/composable/component boundaries
- mock-to-real transitions are explicit
- verification is planned before coding
- risky decisions are spiked or blocked instead of guessed
- `design-to-code` can implement without redoing technical planning
