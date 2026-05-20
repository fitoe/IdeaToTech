# IdeaToTech

[![Skill](https://img.shields.io/badge/agent--skill-IdeaToTech-2563eb)](#)
[![Provider](https://img.shields.io/badge/Javis%20%2F%20PlanToDelivery-Kanban%20Provider-0ea5e9)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**IdeaToTech turns product and design intent into an implementation-ready technical blueprint.**

It sits between visual/product planning and code generation. Instead of jumping from “what we want” straight into implementation, IdeaToTech captures the technical decisions that make agent-built software predictable: architecture, API assumptions, state strategy, mocks, dependencies, risks, and verification.

```text
IdeaToDesign -> IdeaToTech -> DesignToCode
        \          ^          /
         \         |         /
          PlanToDelivery Kanban orchestration
```

## Why it is useful

- Convert feature behavior into concrete technical decisions.
- Make API, state, dependency, and mock choices explicit before coding.
- Produce verification plans that implementation agents can actually run.
- Reduce drift between design intent and code delivery.
- Give multi-agent workflows a stable technical handoff layer.

## Kanban provider mode

IdeaToTech is a **Javis / PlanToDelivery V2 technical planning provider**.

Through `contracts/provider-manifest.json`, it exposes:

- `technical_blueprint`
- `implementation_planning`
- `verification_strategy`

When orchestrated by PlanToDelivery, tasks arrive as `kanban-capability-task/v1` envelopes and results return as `kanban-capability-result/v1` manifests. PlanToDelivery owns canonical Kanban gates, review, provider routing, and progress; IdeaToTech owns the active technical planning slice.

## Core outputs

- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- optional API, state, mock, dependency, and integration plans

## What is inside

- `idea-to-tech/SKILL.md` — the runtime skill kernel
- `contracts/` — provider and task contracts
- `docs/provider-collaboration-v2.md` — provider boundaries and gate discipline

## Design philosophy

IdeaToTech is intentionally narrow. It does not design visuals and does not write final code. It creates the technical agreement that lets design providers, code providers, and reviewers move fast without losing control.
