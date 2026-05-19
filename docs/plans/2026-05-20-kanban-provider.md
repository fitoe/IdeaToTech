# Kanban-Capable IdeaToTech Provider Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task after the PlanToDelivery capability envelope is accepted. IdeaToTech is a technical blueprint provider, not the kanban orchestrator.

**Goal:** Adapt IdeaToTech so kanban can request implementation-ready technical blueprints through a neutral capability contract.

**Architecture:** IdeaToTech consumes product/design requirements and emits architecture decisions, API/state contracts, verification plans, and implementation task recipes. It returns a neutral result manifest for PlanToDelivery/Javis to review and schedule. It does not own kanban task graph, worker assignment, or downstream implementation.

**Tech Stack:** Markdown skill docs, JSON-schema-like contracts, technical decision records, API/state contract docs, verification matrix, PlanToDelivery-compatible result manifest.

---

## Capability Scope

IdeaToTech should advertise these capabilities:

```json
{
  "capabilities": [
    "technical_blueprint",
    "implementation_planning",
    "verification_strategy"
  ]
}
```

### `technical_blueprint`

Turns requirements/design specs into architecture and engineering decisions.

Expected artifacts:
- technical decisions
- architecture notes
- API contracts
- data/state model
- risk/dependency register

### `implementation_planning`

Turns accepted technical direction into executable work slices.

Expected artifacts:
- feature recipes
- task dependency list
- affected file map
- migration/mock-to-real plan

### `verification_strategy`

Turns acceptance criteria into test/build/review gates.

Expected artifacts:
- verification matrix
- smoke test plan
- integration test notes
- release gate recommendations

## Provider Boundaries

- IdeaToTech must not manage kanban states directly.
- IdeaToTech must not hard-code D2C or IdeaToDesign internals.
- It may recommend downstream capabilities such as `visual_implementation`, `backend_implementation`, or `test_implementation`.
- Architecture uncertainty should normally return `review_required=true`.
- Missing credentials, unreachable APIs, or contradictory requirements may return `blocked=true`.
- A design/architecture approval gate is not a blocker.

## Input Contract v1

```json
{
  "schema_version": "kanban-capability-task/v1",
  "capability": "technical_blueprint",
  "objective": "Create implementation-ready architecture for approved design spec",
  "inputs": {
    "project_path": "/abs/path",
    "requirements": [],
    "design_artifacts": [],
    "existing_code_context": [],
    "constraints": [],
    "known_integrations": [],
    "acceptance_criteria": []
  },
  "orchestration": {
    "origin": "kanban",
    "task_id": "kb_tech_001",
    "review_policy": "technical_gate_required"
  }
}
```

## Result Manifest v1

```json
{
  "schema_version": "kanban-capability-result/v1",
  "capability": "technical_blueprint",
  "status": "completed",
  "summary": "Architecture and verification plan drafted for review.",
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
    {"capability": "visual_implementation", "reason": "If approved design is ready"},
    {"capability": "test_implementation", "reason": "After feature slices are created"}
  ]
}
```

## Task Breakdown

### Task 1: Add provider manifest

**Objective:** Declare IdeaToTech capabilities as provider metadata.

**Files:**
- Create: `contracts/provider-manifest.json`

**Required fields:**
- `schema_version: provider-manifest/v1`
- `provider_id: idea-to-tech`
- `capabilities: technical_blueprint, implementation_planning, verification_strategy`
- `input_schema_refs`
- `result_schema_ref`
- `review_policy_notes`

**Verification:**
```bash
python3 -m json.tool contracts/provider-manifest.json >/tmp/i2t-provider-manifest.json
python3 - <<'PY'
import json
m=json.load(open('contracts/provider-manifest.json'))
assert m['schema_version']=='provider-manifest/v1'
assert 'technical_blueprint' in m['capabilities']
assert 'implementation_planning' in m['capabilities']
assert 'verification_strategy' in m['capabilities']
PY
```

**Commit:**
```bash
git add contracts/provider-manifest.json
git commit -m "docs: add IdeaToTech kanban provider manifest"
```

### Task 2: Add technical blueprint task contract

**Objective:** Define minimum input needed before technical planning can start.

**Files:**
- Create: `contracts/technical-blueprint-task-v1.md`

**Verification:**
- Lists required requirements/design/context inputs.
- Defines contradiction and missing-input blockers.
- Defines architecture review as `review_required`.

**Commit:**
```bash
git add contracts/technical-blueprint-task-v1.md
git commit -m "docs: define technical blueprint kanban task"
```

### Task 3: Add implementation planning and verification contracts

**Objective:** Define how IdeaToTech produces executable recipes and verification gates.

**Files:**
- Create: `contracts/implementation-planning-task-v1.md`
- Create: `contracts/verification-strategy-task-v1.md`

**Verification:**
- Implementation planning doc contains task dependencies and affected-file map.
- Verification strategy doc contains unit, integration, build, smoke, and review gates.

**Commit:**
```bash
git add contracts/implementation-planning-task-v1.md contracts/verification-strategy-task-v1.md
git commit -m "docs: define IdeaToTech planning contracts"
```

### Task 4: Add result manifest documentation

**Objective:** Normalize technical outputs for orchestrator scheduling.

**Files:**
- Create: `contracts/technical-result-manifest-v1.md`

**Verification:**
- Manifest includes decisions, API/state contracts, verification matrix, risk register, and next capability recommendations.
- Manifest documents `review_required` and `blocked` semantics.

**Commit:**
```bash
git add contracts/technical-result-manifest-v1.md
git commit -m "docs: define IdeaToTech result manifest"
```

### Task 5: Add kanban provider mode to skill docs

**Objective:** Teach runtime skill how to behave when invoked through kanban envelope.

**Files:**
- Modify: skill source `SKILL.md` or equivalent runtime doc after locating actual source.

**Verification:**
- Existing standalone idea-to-tech workflow remains intact.
- Kanban mode only adds contract I/O and result manifest requirements.
- No direct dependency on PlanToDelivery internals.

**Commit:**
```bash
git add SKILL.md contracts/
git commit -m "docs: document IdeaToTech kanban provider mode"
```

---

## Acceptance Criteria

- IdeaToTech can be selected by capability, not hard-coded name.
- Technical approval is represented as review, not blockage.
- Missing external prerequisites are represented as blockers.
- Downstream work is recommended by capability names and artifact paths.
- Tactical implementation skills remain outside kanban.
