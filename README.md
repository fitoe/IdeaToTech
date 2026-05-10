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
