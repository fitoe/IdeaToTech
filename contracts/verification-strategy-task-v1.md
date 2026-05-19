# Verification Strategy Task v1

Capability: `verification_strategy`

## Purpose

Turn acceptance criteria and implementation plan into deterministic verification gates.

## Required Inputs

- `acceptance_criteria`
- `implementation_plan`
- `project_path`

## Expected Outputs

- verification matrix;
- unit/integration/build/smoke commands;
- evidence requirements;
- release gate recommendation;
- known baseline failures if any.

## Blocker Conditions

Return `blocked=true` when test environment requirements or credentials are missing and no safe fallback exists.

## Review Conditions

Return `review_required=true` when release risk or baseline failures need human/strong-model judgment.
