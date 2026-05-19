# Implementation Planning Task v1

Capability: `implementation_planning`

## Purpose

Convert accepted technical direction into executable slices that downstream implementation workers can perform.

## Required Inputs

- `technical_decisions`
- `target_features`
- `project_path`
- `acceptance_criteria`

## Expected Outputs

- feature recipes;
- task dependency list;
- affected file map;
- migration plan if needed;
- mock-to-real plan if needed;
- downstream capability recommendations.

## Blocker Conditions

Return `blocked=true` when accepted technical direction is absent or target features are contradictory.

## Review Conditions

Return `review_required=true` when task slicing or dependency order needs approval before execution.
