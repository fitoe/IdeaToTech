# IdeaToTech

IdeaToTech is an Agent Skill for converting product functionality, feature behavior, project constraints, API facts, dependency choices, state management, mock strategy, and verification expectations into an implementation-ready technical blueprint.

It sits between product/visual planning and implementation:

```text
idea-to-design -> IdeaToTech -> design-to-code
        \          ^          /
         \         |         /
          PlanToDelivery orchestration
```

Core outputs:

- `technical-decisions.json`
- `feature-recipes.json`
- `verification-matrix.json`
- optional API/state/mock/integration plans

The skill is intentionally narrow: it does not design visuals and does not write final implementation code.

## Javis / PlanToDelivery V2 provider mode

IdeaToTech is also a Javis/Kanban V2 technical planning provider kernel. It exposes these capabilities through `contracts/provider-manifest.json`:

- `technical_blueprint`
- `implementation_planning`
- `verification_strategy`

In provider mode, PlanToDelivery sends a `kanban-capability-task/v1` envelope and IdeaToTech returns a `kanban-capability-result/v1` manifest plus technical artifacts. PlanToDelivery owns provider registry routing, canonical gates, review, and progress. IdeaToTech owns only the active-slice technical artifacts and recommendations.

Provider files:

- [idea-to-tech/SKILL.md](idea-to-tech/SKILL.md) — runtime skill kernel
- [contracts/provider-manifest.json](contracts/provider-manifest.json) — provider manifest
- [contracts/technical-blueprint-task-v1.md](contracts/technical-blueprint-task-v1.md) — `technical_blueprint` task contract
- [contracts/implementation-planning-task-v1.md](contracts/implementation-planning-task-v1.md) — `implementation_planning` task contract
- [contracts/verification-strategy-task-v1.md](contracts/verification-strategy-task-v1.md) — `verification_strategy` task contract
- [contracts/technical-result-manifest-v1.md](contracts/technical-result-manifest-v1.md) — result manifest contract
- [docs/provider-collaboration-v2.md](docs/provider-collaboration-v2.md) — cross-provider boundaries and gate discipline
- [docs/plans/2026-05-20-kanban-provider.md](docs/plans/2026-05-20-kanban-provider.md) — V2 provider redesign plan
