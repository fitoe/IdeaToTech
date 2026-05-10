#!/usr/bin/env python3
"""Minimal IdeaToTech handoff checker."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = [
    "technical-decisions.json",
    "feature-recipes.json",
    "verification-matrix.json",
]
VALID_STATUSES = {"lock_now", "spike_first", "defer_to_implementation", "blocked"}


def load_json(path: Path, blockers: list[str]):
    if not path.exists():
        blockers.append(f"missing {path.name}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"invalid JSON in {path.name}: {exc}")
        return None
    if not isinstance(value, dict):
        blockers.append(f"{path.name} must be a JSON object")
        return None
    return value


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    blockers: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED:
        if not (root / name).exists():
            blockers.append(f"missing {name}")

    decisions_doc = load_json(root / "technical-decisions.json", blockers)
    recipes_doc = load_json(root / "feature-recipes.json", blockers)
    verification_doc = load_json(root / "verification-matrix.json", blockers)

    if decisions_doc:
        gate = decisions_doc.get("technical_gate", {})
        if not isinstance(gate, dict):
            blockers.append("technical_gate must be an object")
        elif gate.get("status") != "open":
            blockers.append("technical_gate.status is not open")
        decisions = decisions_doc.get("decisions")
        if not isinstance(decisions, list) or not decisions:
            blockers.append("technical-decisions.json decisions must be a non-empty list")
        else:
            for idx, item in enumerate(decisions):
                if not isinstance(item, dict):
                    blockers.append(f"decision[{idx}] must be an object")
                    continue
                for key in ["id", "feature", "selected", "status", "reason", "usage_boundary"]:
                    if key not in item:
                        blockers.append(f"decision[{idx}] missing {key}")
                status = item.get("status")
                if status not in VALID_STATUSES:
                    blockers.append(f"decision[{idx}] invalid status {status!r}")
                if status in {"spike_first", "blocked"} and not item.get("fallback"):
                    warnings.append(f"decision[{idx}] is {status} without fallback")

    feature_ids = set()
    if recipes_doc:
        features = recipes_doc.get("features")
        if not isinstance(features, list) or not features:
            blockers.append("feature-recipes.json features must be a non-empty list")
        else:
            for idx, feature in enumerate(features):
                if not isinstance(feature, dict):
                    blockers.append(f"feature[{idx}] must be an object")
                    continue
                for key in ["id", "title", "status", "maturity_target", "data_source", "states", "verification_refs"]:
                    if key not in feature:
                        blockers.append(f"feature[{idx}] missing {key}")
                if feature.get("id"):
                    feature_ids.add(feature["id"])
                if not feature.get("services") and not feature.get("stores") and not feature.get("composables"):
                    warnings.append(f"feature[{idx}] has no service/store/composable boundary")

    if verification_doc:
        items = verification_doc.get("items")
        if not isinstance(items, list) or not items:
            blockers.append("verification-matrix.json items must be a non-empty list")
        else:
            for idx, item in enumerate(items):
                if not isinstance(item, dict):
                    blockers.append(f"verification[{idx}] must be an object")
                    continue
                for key in ["id", "feature_id", "risk", "unit", "integration", "e2e_or_manual"]:
                    if key not in item:
                        blockers.append(f"verification[{idx}] missing {key}")
                fid = item.get("feature_id")
                if feature_ids and fid not in feature_ids:
                    warnings.append(f"verification[{idx}] references unknown feature_id {fid!r}")

    if blockers:
        print("IdeaToTech handoff check: BLOCKED")
        for item in blockers:
            print(f"- {item}")
        if warnings:
            print("Warnings:")
            for item in warnings:
                print(f"- {item}")
        return 1

    print("IdeaToTech handoff check: PASS")
    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
