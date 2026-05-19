# Technical Blueprint Task v1

Capability: `technical_blueprint`

## Purpose

Create implementation-ready architecture decisions from requirements, approved design artifacts, and existing code context.

## Required Inputs

- `project_path`
- `requirements`
- `acceptance_criteria`
- at least one of `design_artifacts` or `existing_code_context`

## Optional Inputs

- `constraints`
- `known_integrations`
- `api_preferences`
- `deployment_context`

## Blocker Conditions

Return `blocked=true` for missing project path, inaccessible required artifacts, missing credentials for required live API discovery, or contradictory requirements.

## Review Conditions

Return `review_required=true` for architecture approval, irreversible tradeoff decisions, or multiple viable implementation strategies.

## Example

```json
{
  "schema_version": "kanban-capability-task/v1",
  "task_id": "kb_tech_001",
  "correlation_id": "home-implementation-tech",
  "capability": "technical_blueprint",
  "objective": "Create architecture for approved homepage implementation",
  "inputs": {
    "project_path": "/abs/project",
    "requirements": ["H5 responsive page"],
    "design_artifacts": ["project-state/design/design-spec.md"],
    "acceptance_criteria": ["implementation slices are clear"]
  },
  "orchestration": {"origin": "kanban", "review_policy": "technical_gate_required"}
}
```
