# IdeaToTech Provider Collaboration v2

IdeaToTech is the bounded technical planning provider in the Javis/PlanToDelivery V2 provider system. It turns approved product/design/repository evidence into technical artifacts for the active slice, but it does not own orchestration, design decisions, or final coding.

## Capability boundary

| Capability | Owned by IdeaToTech | Not owned by IdeaToTech |
|---|---|---|
| `technical_blueprint` | project profile, architecture seams, API/state/mock/dependency decisions, file map, risk classification | visual direction, final code changes, canonical gate mutation |
| `implementation_planning` | ordered recipes, implementation sequence, dependency boundaries, mock-to-real path | direct code execution, visual parity acceptance |
| `verification_strategy` | mock/local/real/edge verification matrix, waivers, blockers, evidence expectations | running every test as a completion claim, hiding skipped checks as passed |

## Upstream / downstream handoff

```text
PlanToDelivery/Javis
  -> kanban-capability-task/v1(technical_blueprint | implementation_planning | verification_strategy)
  -> IdeaToTech
  -> kanban-capability-result/v1 + technical artifacts
  -> PlanToDelivery review/gate decision
  -> DesignToCode or implementation worker when approved
```

Expected upstream inputs:

- active slice, product/design artifact refs, repository root, and constraints;
- known API/auth facts and permitted mock/real boundary;
- explicit expected outputs, verification expectations, allowed side effects, and review policy.

Expected downstream outputs:

- `technical-decisions.json`, `feature-recipes.json`, `verification-matrix.json`, and optional API/state/mock/integration plans;
- maturity labels for mock/local/real functionality (`F0`-`F5`);
- blockers when API/auth/security facts are missing or unsafe;
- result manifest with recommended next capability and evidence paths.

## Gate discipline

- IdeaToTech may recommend `suggested_gate_updates`, but PlanToDelivery alone records canonical gates.
- Architecture approval, dependency additions, mock-to-real boundaries, and high-risk verification assumptions are `review_required: true`, not generic `blocked`.
- Use `blocked` for missing credentials, inaccessible systems, contradictory requirements, or unsafe technical constraints.
- Skipped/waived verification must remain `skipped` or `waived`; never convert it to `passed`.
- Do not let downstream implementation invent architecture that should have been locked here; explicitly classify decisions as `lock_now`, `spike_first`, `defer_to_implementation`, or `blocked`.

## Registry references

- Provider manifest: `contracts/provider-manifest.json`
- Task contracts: `contracts/technical-blueprint-task-v1.md`, `contracts/implementation-planning-task-v1.md`, `contracts/verification-strategy-task-v1.md`
- Result contract: `contracts/technical-result-manifest-v1.md`
- Runtime skill: `idea-to-tech/SKILL.md`
