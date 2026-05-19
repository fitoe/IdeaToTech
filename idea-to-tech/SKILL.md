---
name: IdeaToTech
description: Use when product features, page behaviors, existing project constraints, APIs, dependencies, state management, mocks, or verification strategy need to be converted into an implementation-ready technical blueprint before coding.
---

# IdeaToTech

## Overview

Turn product ideas, feature behavior, existing repository constraints, and integration facts into a compact technical implementation blueprint.

This skill is not a UI designer and not a coding executor. It decides **how functionality should be implemented** so implementation agents can move quickly without choosing libraries, state shape, API boundaries, mock strategy, file locations, or verification strategy during coding.

Default outcome:
- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- optional `api-contracts.json`, `state-management-plan.json`, `mock-to-real-plan.json`, `integration-plan.json`, and `technical-spikes/*`
- checker-passing `technical_gate`

Standalone rule:
- this skill can be used directly or routed by `PlanToDelivery`
- `idea-to-design` may provide product/page/interaction/visual inputs
- `design-to-code` consumes outputs during implementation

## Kanban Provider Mode

Use this mode when invoked through a `kanban-capability-task/v1` envelope, a provider registry entry, or Javis/PlanToDelivery kanban dispatch. In this mode, `IdeaToTech` is a technical planning provider, not the global orchestrator and not the coding executor.

Advertised capabilities:
- `technical_blueprint`: implementation-ready technical decisions, architecture seams, file map, state/API/mock/platform decisions, and risk classification;
- `implementation_planning`: ordered feature recipes, dependency boundaries, mock-to-real path, and implementation sequence for the active slice;
- `verification_strategy`: verification matrix that distinguishes mock, local interaction, real API, edge/regression, blocking failures, and waivers.

Provider rules:
- consume the task envelope's active slice, capability, input artifact refs, target output root, and verification expectations;
- inspect only the project evidence needed for that slice: project profile, nearby patterns, relevant package/config files, and referenced design/product artifacts;
- output schema-valid artifacts under the requested output root when provided, otherwise under `project-state/tech/`;
- return a `kanban-capability-result/v1`-shaped manifest with `capability`, `result`, `changed_files`, `produced_artifacts`, `evidence`, `blockers`, `debts`, `review_required`, and `next_recommended_task`;
- do not mark global technical gates passed; recommend gate updates and let the orchestrator record them;
- use `review_required: true` for hard/high decisions, dependency additions, mock-to-real boundaries, safety-sensitive verification, or assumptions that need orchestrator/human review; do not label these as `blocked` unless missing facts prevent a safe plan.

Result semantics:
- `completed`: the requested technical capability is ready for orchestrator review and downstream implementation;
- `partial`: useful plan artifacts exist, but specific decisions, spikes, or verification rows remain;
- `blocked`: required API/auth/product/security facts, repo access, or non-waivable technical constraints are missing.

Keep the user-facing summary compact. Put detailed decisions, recipes, matrices, spike logs, and evidence references in files, then return manifest paths and the next recommended capability.

Core rule:
- prefer existing project conventions, nearby patterns, and installed dependencies before new architecture
- front-load only decisions that affect speed, consistency, dependencies, data flow, API integration, state, platform compatibility, risk, or verification
- keep tiny local details lightweight; do not produce architecture documents for a button click
- risky or uncertain approaches require a small spike before locking the decision
- mock is allowed as planned delivery; fake completion is not
- keep outputs machine-readable and compact; long prose is traceability, not default implementation input

## When to Use

Use when:
- implementation would otherwise need to choose libraries, architecture, state, API seams, or verification during coding
- features need API, state, mock, permission, streaming, upload, charting, map, form, cache, platform, or performance strategy
- `design-to-code` needs functional/technical inputs in addition to visual blueprint
- `PlanToDelivery` needs a technical gate before execution

Do not use when:
- the task is only visual style exploration
- the feature is tiny and the existing project pattern is obvious
- no meaningful implementation decision exists
- the task is backend-only architecture beyond the current milestone

## Low-Context Technical Blueprint Mode

When routed by `PlanToDelivery`, this skill should plan only the active slice named in the invocation brief. Do not re-plan the whole application unless the active gate explicitly says the project profile or global architecture is stale.

Rules:
- read `project-state/execution-progress.json` and `artifact-manifest.json` only enough to resolve `active_task`, `scope`, and `input_artifact_refs`;
- inspect only nearby patterns needed for the current feature slice; avoid broad repo scans after enough evidence exists;
- output JSON artifacts under `project-state/tech/` and reference large spikes/logs by path;
- do not paste full contracts, recipes, package dumps, or spike transcripts into the chat;
- for L0/R0 or obvious L1 work, return `defer_to_implementation` with a short rationale instead of writing a full blueprint;
- for each decision, include evidence paths/line refs rather than copied source content;
- return a compact delta response for `PlanToDelivery`, not a long architectural narrative.

Default delta response:

```json
{
  "result": "completed | partial | blocked",
  "changed_files": [],
  "produced_artifacts": [],
  "suggested_manifest_entries": [],
  "suggested_progress_updates": [],
  "suggested_blockers": [],
  "suggested_gate_updates": [],
  "evidence": [],
  "largest_remaining_gaps": [],
  "next_recommended_task": ""
}
```

The user-facing summary should be at most: real this milestone, mock this milestone, new dependencies, blockers, implementation order, and maturity target.

## Planning Levels

Use the lightest sufficient output.

Default planning unit is a feature slice, not a page widget. Plan technical boundaries that affect implementation direction, consistency, risk, architecture, API, platform support, security, performance, or verification. Do not plan routine button handlers, local modal toggles, simple tab switches, helper names, minor CSS/animation, or internal component splits unless they affect one of those risks.

Use three levels of detail:
- must plan: architecture/cross-module decisions such as API, store, service, adapter, auth, mock-to-real, dependency, platform, performance, and verification
- briefly plan: page or feature responsibilities, main states, dependent services/stores, maturity target, demo path, and real completion path
- do not plan: ordinary click handlers, local variables, helper names, minor hover/transition details, and disposable component internals

Complexity:
- `L0`: local UI interaction; follow existing pattern, no full blueprint
- `L1`: single-page function; short feature recipe
- `L2`: cross-component or cross-page state; recipe + state/file map
- `L3`: real API, permissions, upload, streaming, charts, maps, complex forms, or platform differences; decisions + contracts + verification
- `L4`: high-risk capability: payments, destructive operations, auth/security, production data, real-time collaboration; safety gate and spike/approval

Risk:
- `R0`: pure display or local state
- `R1`: ordinary form/list/filter
- `R2`: real API/auth/pagination/cache
- `R3`: upload/streaming/charts/maps/complex interaction/performance
- `R4`: payment/permission/security/delete/production side effects

Functional maturity:
- `F0`: mock shape exists
- `F1`: UI consumes mock service
- `F2`: local interaction works
- `F3`: real adapter seam wired, mock-to-real path clear
- `F4`: real API verified for happy path
- `F5`: edge cases, permissions, errors, retries, and regressions verified

Report progress with both visual and functional maturity. UI visible is not functionally complete. Mock working is not real API verified.

## Required Intake

Before choosing technology, form a compact `project_profile`:
- framework and platform targets
- package manager
- request layer
- state layer
- UI/styling layer
- routing pattern
- test layer
- mock layer
- env/config pattern
- existing directories for pages, services, stores, composables, components, types, mocks, tests

Also collect `nearby_patterns`: similar implemented files to copy. Near pattern beats new architecture.

## Decision Classes

Classify each decision:
- `lock_now`: safe from repo conventions and known requirements
- `spike_first`: needs a minimal experiment
- `defer_to_implementation`: too small/local to plan
- `blocked`: missing product/API/security facts

Also record:
- `source_confidence`: `confirmed`, `inferred`, `mocked`, or `unknown`
- `reversibility`: `easy`, `medium`, or `hard`
- `decision_cost`: `low`, `medium`, or `high`
- evidence from package.json, existing code, docs, API, user requirement, or spike

Hard/high decisions should not be guessed. Use a spike or block.

## Dependency Rule

Default order:
1. existing project code and nearby patterns
2. installed dependency
3. mature new dependency
4. custom implementation

Add a new dependency only when at least one is true:
- self-build cost is clearly high
- a mature library reduces risk
- feature is complex: virtual list, charts, drag/drop, rich text, upload, map, streaming, form validation
- same ecosystem dependency already exists
- multiple features will reuse it

Record alternatives, install command, usage boundary, fallback, and must-not-do items such as “do not introduce axios if project uses alova”.

## Feature Recipes

Each feature recipe should be concise and executable:
- `complexity`, `risk`, `functional_maturity_target`
- `file_map`: pages, components, services, adapters, stores, composables, types, mocks, tests
- `implementation_order`: types -> mock -> adapter/service -> store/composable -> UI binding -> states -> real API -> tests
- `demo_path`: route, user steps, success signal
- `real_completion_path`: conditions required before claiming real completion
- state/data/service boundaries
- loading/empty/error/permission/offline states
- mock-to-real seam and honest labels
- config requirements by variable name only; never value
- platform differences and fallback behavior
- performance budget when relevant
- testability: mockable boundaries and stable selectors
- `must_not_do`
- `technical_debt`

## API, State, Mock, and Platform Rules

API unknowns have three levels:
- known API: write real contract
- API unknown but business shape known: create adapter + mock contract
- API and business both unclear: mark blocker

Use adapter seams:
`page/component -> store/composable -> service -> adapter -> real API or mock API`.

For platform targets, record differences. Example: H5 supports fetch streams; mp-weixin may need WebSocket, polling, or non-stream fallback.

## Visual Alignment

When a visual blueprint exists, technical planning must check it:
- visual element without function -> record `visual_elements_without_function`
- feature state missing from visuals -> record `missing_states_in_visual`
- technical constraint affecting UI -> record `requires_visual_deviation` or `needs_design_update`

If a GPT image invents product-like elements, do not silently implement them as real features. Route through product/visual approval.

## Verification and Handoff

`verification-matrix.json` distinguishes:
- mock acceptance
- local interaction acceptance
- real API acceptance
- edge/regression acceptance
- blocking vs non-blocking failures

Include a short user-facing Technical Plan Summary:
- real this milestone
- mock this milestone
- new dependencies
- key risks/blockers
- implementation order
- maturity target, e.g. “target F3; not claiming F5”

## Technical Gate

Open `technical_gate` only when:
- required files exist
- current-scope decisions are `lock_now` or intentionally deferred
- `spike_first` decisions have spike results or are out of current scope
- blockers are resolved or explicitly waived
- recipes define file_map and implementation_order for current scope
- verification distinguishes mock, local, and real acceptance
- checker passes
- no secrets/tokens/passwords/private connection strings are persisted

## Handoff to DesignToCode

`design-to-code` should read in this order:
1. visual `implementation-blueprint.json` when UI exists
2. `technical-decisions.json`
3. current-scope entries from `feature-recipes.json`
4. current-scope entries from `verification-matrix.json`
5. optional API/state/mock/spike files only when referenced

Do not let implementation pick competing libraries, state architecture, API seams, or mock-to-real rules unless the technical plan is blocked or user-waived.


## PlanToDelivery Project-State Collaboration

When routed by `PlanToDelivery`, consume the active task from `project-state/execution-progress.json` and the required inputs from `project-state/artifact-manifest.json`. Do not directly modify global project-state unless explicitly authorized.

Read design and product inputs from `routing.input_artifact_refs` first, especially `implementation_blueprint`, `page_matrix`, `component_blueprint`, and design debt. Produce technical artifacts, usually under `project-state/tech/`:
- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- `api-contracts.json` when API shape is known or mockable
- `state-management-plan.json` when cross-component/page state matters
- `mock-to-real-plan.json` when real integration is incomplete
- `technical-spikes/*` for risky decisions

Return compact delta suggestions to `PlanToDelivery`:
- `result`: `completed`, `partial`, or `blocked`
- `changed_files` and `produced_artifacts` for all technical artifacts created or updated
- `suggested_manifest_entries` for produced technical artifacts
- `suggested_progress_updates` for technical tasks, verification maturity, and dependencies
- technical gate recommendation with evidence, but do not mark the global gate passed yourself
- blockers for missing product facts, stale design inputs, unknown auth/API access, unsafe dependency choices, or unverified real integration
- verification evidence that distinguishes mock, local interaction, real API, and edge/regression coverage
- `next_recommended_task` when implementation can continue without another technical planning pass

If a design artifact conflicts with technical constraints, report `requires_visual_deviation` or `needs_design_update` and recommend routing back to `idea-to-design`. If implementation later disproves a core technical assumption, expect `PlanToDelivery` to route back here for a refreshed blueprint.

## Feedback Loop

If implementation finds the plan wrong:
- small safe deviation -> record accepted deviation/finding
- core technical assumption wrong -> return to IdeaToTech and refresh blueprint
- visual impact -> notify `idea-to-design`
- milestone/gate impact -> notify `PlanToDelivery`

Blueprints are living contracts, not one-time prose.

## Token Budget

Use JSON and IDs. Do not load every recipe for one feature. Put heavy experiments under `technical-spikes/` and reference them.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Choosing new libraries before reading package.json | Inspect project profile first |
| Ignoring nearby implemented patterns | Reuse similar files by default |
| Planning every tiny helper | Use L0/L1 lightweight mode |
| Planning every button, tab, and modal toggle | Plan feature slices and risky boundaries, not routine widgets |
| Mock behavior reported as real | Track F0-F5 and mock-to-real plan |
| API unknowns hidden in prose | Use contracts, source confidence, and blockers |
| Functional states missing from visuals | Record visual_alignment and route back if needed |
| design-to-code picks libraries during coding | Move choices into technical-decisions.json |
| Hard/high decisions guessed | Spike or block |

## Success Criteria

This skill succeeds when:
- implementation agents know which libraries and approaches to use
- file locations, boundaries, and order are clear
- mock-to-real transitions and real-completion criteria are explicit
- visual/functional conflicts are surfaced before coding
- platform, config, fallback, and testability risks are planned
- `design-to-code` can implement without redoing technical planning
