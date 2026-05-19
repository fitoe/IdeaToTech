# Technical Result Manifest v1

IdeaToTech returns `kanban-capability-result/v1` manifests.

## Artifact Types

- `technical_decisions`
- `architecture_notes`
- `api_contracts`
- `state_model`
- `feature_recipes`
- `affected_file_map`
- `verification_matrix`
- `risk_register`
- `mock_to_real_plan`

## Example

```json
{
  "schema_version": "kanban-capability-result/v1",
  "task_id": "kb_tech_001",
  "correlation_id": "home-implementation-tech",
  "capability": "technical_blueprint",
  "status": "completed",
  "summary": "Architecture and verification gates are ready for review.",
  "artifacts": [
    {"type": "technical_decisions", "path": "project-state/tech/technical-decisions.json"},
    {"type": "verification_matrix", "path": "project-state/tech/verification-matrix.json"}
  ],
  "changed_files": [],
  "evidence": [],
  "review_required": true,
  "blocked": false,
  "blockers": [],
  "debt": [],
  "next_tasks": [
    {"capability": "visual_implementation", "reason": "Implement approved visual slices"},
    {"capability": "test_implementation", "reason": "Add tests from verification matrix"}
  ]
}
```

## Semantics

- Architecture/technical gate approval is `review_required=true`, not `blocked=true`.
- Missing credentials, unreachable required APIs, contradictory requirements, or absent required artifacts may be `blocked=true`.
- Downstream recommendations use capability names, not provider-specific implementation details.
