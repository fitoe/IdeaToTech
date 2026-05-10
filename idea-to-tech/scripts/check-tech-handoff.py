#!/usr/bin/env python3
"""IdeaToTech handoff checker."""
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
VALID_CONFIDENCE = {"confirmed", "inferred", "mocked", "unknown"}
VALID_REVERSIBILITY = {"easy", "medium", "hard"}
VALID_COST = {"low", "medium", "high"}
VALID_COMPLEXITY = {"L0", "L1", "L2", "L3", "L4"}
VALID_RISK = {"R0", "R1", "R2", "R3", "R4"}
VALID_MATURITY = {"F0", "F1", "F2", "F3", "F4", "F5"}


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


def need(obj: dict, keys: list[str], where: str, blockers: list[str]) -> None:
    for key in keys:
        if key not in obj:
            blockers.append(f"{where} missing {key}")


def nonempty_list(obj: dict, key: str, where: str, blockers: list[str], warnings: list[str], required: bool = True) -> list:
    value = obj.get(key)
    if value is None:
        if required:
            blockers.append(f"{where} missing {key}")
        return []
    if not isinstance(value, list):
        blockers.append(f"{where}.{key} must be a list")
        return []
    if required and not value:
        blockers.append(f"{where}.{key} must be non-empty")
    elif not value:
        warnings.append(f"{where}.{key} is empty")
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

        profile = decisions_doc.get("project_profile")
        if not isinstance(profile, dict):
            blockers.append("project_profile must be an object")
        else:
            for key in ["framework", "package_manager", "request_layer", "state_layer", "platform_targets", "evidence"]:
                if key not in profile:
                    blockers.append(f"project_profile missing {key}")
            if not isinstance(profile.get("evidence", []), list):
                blockers.append("project_profile.evidence must be a list")

        if "nearby_patterns" in decisions_doc and not isinstance(decisions_doc["nearby_patterns"], list):
            blockers.append("nearby_patterns must be a list")

        decisions = decisions_doc.get("decisions")
        if not isinstance(decisions, list) or not decisions:
            blockers.append("technical-decisions.json decisions must be a non-empty list")
        else:
            for idx, item in enumerate(decisions):
                where = f"decision[{idx}]"
                if not isinstance(item, dict):
                    blockers.append(f"{where} must be an object")
                    continue
                need(item, ["id", "feature", "selected", "status", "source_confidence", "evidence", "reason", "usage_boundary", "fallback", "reversibility", "decision_cost"], where, blockers)
                if item.get("status") not in VALID_STATUSES:
                    blockers.append(f"{where} invalid status {item.get('status')!r}")
                if item.get("source_confidence") not in VALID_CONFIDENCE:
                    blockers.append(f"{where} invalid source_confidence {item.get('source_confidence')!r}")
                if item.get("reversibility") not in VALID_REVERSIBILITY:
                    blockers.append(f"{where} invalid reversibility {item.get('reversibility')!r}")
                if item.get("decision_cost") not in VALID_COST:
                    blockers.append(f"{where} invalid decision_cost {item.get('decision_cost')!r}")
                if not isinstance(item.get("evidence", []), list) or not item.get("evidence"):
                    warnings.append(f"{where} has no evidence")
                if item.get("status") in {"spike_first", "blocked"} and not item.get("fallback"):
                    warnings.append(f"{where} is {item.get('status')} without fallback")
                if item.get("reversibility") == "hard" and item.get("decision_cost") == "high" and item.get("status") == "lock_now" and not item.get("evidence"):
                    blockers.append(f"{where} locks a hard/high decision without evidence")

    feature_ids = set()
    if recipes_doc:
        features = recipes_doc.get("features")
        if not isinstance(features, list) or not features:
            blockers.append("feature-recipes.json features must be a non-empty list")
        else:
            for idx, feature in enumerate(features):
                where = f"feature[{idx}]"
                if not isinstance(feature, dict):
                    blockers.append(f"{where} must be an object")
                    continue
                need(feature, ["id", "title", "status", "complexity", "risk", "functional_maturity_target", "file_map", "implementation_order", "data_source", "states", "demo_path", "real_completion_path", "mock_to_real", "visual_alignment", "testability", "must_not_do", "technical_debt", "verification_refs"], where, blockers)
                if feature.get("id"):
                    feature_ids.add(feature["id"])
                if feature.get("complexity") not in VALID_COMPLEXITY:
                    blockers.append(f"{where} invalid complexity {feature.get('complexity')!r}")
                if feature.get("risk") not in VALID_RISK:
                    blockers.append(f"{where} invalid risk {feature.get('risk')!r}")
                if feature.get("functional_maturity_target") not in VALID_MATURITY:
                    blockers.append(f"{where} invalid functional_maturity_target {feature.get('functional_maturity_target')!r}")
                if not isinstance(feature.get("file_map"), dict):
                    blockers.append(f"{where}.file_map must be an object")
                else:
                    fm = feature["file_map"]
                    if not any(fm.get(k) for k in ["pages", "components", "services", "adapters", "stores", "composables", "types", "mocks", "tests"]):
                        warnings.append(f"{where}.file_map has no file targets")
                nonempty_list(feature, "implementation_order", where, blockers, warnings)
                nonempty_list(feature, "states", where, blockers, warnings)
                if not feature.get("services") and not feature.get("stores") and not feature.get("composables"):
                    warnings.append(f"{where} has no service/store/composable boundary")
                if not isinstance(feature.get("visual_alignment"), dict):
                    blockers.append(f"{where}.visual_alignment must be an object")
                if not isinstance(feature.get("mock_to_real"), dict):
                    blockers.append(f"{where}.mock_to_real must be an object")

    if verification_doc:
        items = verification_doc.get("items")
        if not isinstance(items, list) or not items:
            blockers.append("verification-matrix.json items must be a non-empty list")
        else:
            for idx, item in enumerate(items):
                where = f"verification[{idx}]"
                if not isinstance(item, dict):
                    blockers.append(f"{where} must be an object")
                    continue
                need(item, ["id", "feature_id", "risk", "functional_maturity_target", "mock_acceptance", "local_interaction_acceptance", "real_api_acceptance", "edge_regression_acceptance", "unit", "integration", "e2e_or_manual"], where, blockers)
                if item.get("risk") not in VALID_RISK:
                    blockers.append(f"{where} invalid risk {item.get('risk')!r}")
                if item.get("functional_maturity_target") not in VALID_MATURITY:
                    blockers.append(f"{where} invalid functional_maturity_target {item.get('functional_maturity_target')!r}")
                fid = item.get("feature_id")
                if feature_ids and fid not in feature_ids:
                    warnings.append(f"{where} references unknown feature_id {fid!r}")

    optional_json = ["api-contracts.json", "state-management-plan.json", "mock-to-real-plan.json", "integration-plan.json"]
    for name in optional_json:
        p = root / name
        if p.exists():
            load_json(p, blockers)

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
