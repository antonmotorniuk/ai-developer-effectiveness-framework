#!/usr/bin/env python3

"""Save an AI Developer Effectiveness session retro.

Reads a JSON object from stdin and appends it to:
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/sessions.md
- .ai-effectiveness/profile-updates.md

This script is intentionally tool-agnostic. Codex, Claude Code, Cursor,
Continue, Aider, or any other AI coding client can call it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUSPICIOUS_MARKERS = [
    "sk-",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "password",
    "secret",
    "private_key",
    "authorization:",
    "bearer ",
]


ALLOWED_TASK_TYPES = {
    "bugfix",
    "feature",
    "refactor",
    "test",
    "docs",
    "investigation",
    "review",
    "other",
}

ALLOWED_COMPLEXITY = {"small", "medium", "large", "unknown"}
ALLOWED_RISK = {"low", "medium", "high", "unknown"}
ALLOWED_FAMILIARITY = {"low", "medium", "high", "unknown"}
ALLOWED_AI_ROLES = {"assistant", "pair", "reviewer", "researcher", "other", "unknown"}
ALLOWED_APPLICABILITY = {"core", "important", "optional", "not_applicable"}
ALLOWED_VERIFICATION_STATUS = {"done", "skipped", "blocked", "not_applicable", "not_observed"}
ALLOWED_CONFIDENCE = {"low", "medium", "high", "unknown"}

DEFAULT_WEIGHT_BY_APPLICABILITY = {
    "core": 1.25,
    "important": 1.0,
    "optional": 0.5,
    "not_applicable": 0.0,
}


def get_repo_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except Exception:
        return Path.cwd()


def sanitize_text(value: Any, max_len: int = 1200) -> str:
    if value is None:
        return ""

    text = str(value)
    lowered = text.lower()

    if any(marker in lowered for marker in SUSPICIOUS_MARKERS):
        return "[REDACTED: possible secret]"

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if len(text) > max_len:
        text = text[:max_len] + "... [truncated]"

    return text


def sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {sanitize_text(k, 200): sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if isinstance(obj, str):
        return sanitize_text(obj)
    return obj


def clamp_number(value: Any, minimum: float, maximum: float, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))


def normalize_choice(value: Any, allowed: set[str], default: str, max_len: int = 80) -> str:
    text = sanitize_text(value, max_len).lower().replace(" ", "_")
    return text if text in allowed else default


def normalize_string_list(value: Any, max_len: int = 600) -> list[str]:
    if not isinstance(value, list):
        return []
    return [sanitize_text(item, max_len) for item in value]


def md_escape(value: Any) -> str:
    return sanitize_text(value, 500).replace("|", "\\|").replace("\n", " ")


def normalize_task_profile(value: Any, task_type: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        value = {}

    change_type = sanitize_text(value.get("change_type", task_type), 80)
    if not change_type:
        change_type = task_type

    change_surface = value.get("change_surface", [])
    if isinstance(change_surface, str):
        change_surface = [change_surface]

    return {
        "complexity": normalize_choice(value.get("complexity", "unknown"), ALLOWED_COMPLEXITY, "unknown"),
        "risk_level": normalize_choice(value.get("risk_level", "unknown"), ALLOWED_RISK, "unknown"),
        "change_type": change_type,
        "codebase_familiarity": normalize_choice(
            value.get("codebase_familiarity", "unknown"),
            ALLOWED_FAMILIARITY,
            "unknown",
        ),
        "ai_role": normalize_choice(value.get("ai_role", "unknown"), ALLOWED_AI_ROLES, "unknown"),
        "change_surface": normalize_string_list(change_surface, 200),
    }


def normalize_expected_verification(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []

    checks = []
    for item in value:
        if isinstance(item, str):
            checks.append(
                {
                    "check": sanitize_text(item, 200),
                    "status": "not_observed",
                    "evidence": "",
                }
            )
            continue

        if not isinstance(item, dict):
            continue

        checks.append(
            {
                "check": sanitize_text(item.get("check", "verification check"), 200),
                "status": normalize_choice(
                    item.get("status", "not_observed"),
                    ALLOWED_VERIFICATION_STATUS,
                    "not_observed",
                ),
                "evidence": sanitize_text(item.get("evidence", ""), 600),
            }
        )

    return checks


def normalize_score_confidence(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        value = {}
    return {
        "level": normalize_choice(value.get("level", "unknown"), ALLOWED_CONFIDENCE, "unknown"),
        "reason": sanitize_text(value.get("reason", ""), 600),
    }


def normalize_dimensions(value: Any) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(value, list):
        return [], False

    normalized_dimensions = []
    uses_adaptive_scoring = False

    for dim in value:
        if not isinstance(dim, dict):
            continue

        uses_adaptive_scoring = uses_adaptive_scoring or "weight" in dim or "applicability" in dim

        dim_score = clamp_number(dim.get("score", 0), 0.0, 5.0)
        applicability = normalize_choice(
            dim.get("applicability", "important"),
            ALLOWED_APPLICABILITY,
            "important",
        )
        default_weight = DEFAULT_WEIGHT_BY_APPLICABILITY[applicability]
        weight = clamp_number(dim.get("weight", default_weight), 0.0, 2.0, default_weight)
        if applicability == "not_applicable":
            weight = 0.0

        normalized_dimensions.append(
            {
                "name": sanitize_text(dim.get("name", "unknown"), 120),
                "score": dim_score,
                "applicability": applicability,
                "weight": weight,
                "weighted_score": round(dim_score * weight, 4),
                "weight_reason": sanitize_text(dim.get("weight_reason", ""), 500),
                "evidence": sanitize_text(dim.get("evidence", "not observed"), 800),
                "improvement": sanitize_text(dim.get("improvement", ""), 800),
            }
        )

    return normalized_dimensions, uses_adaptive_scoring


def calculate_score(dimensions: list[dict[str, Any]]) -> dict[str, Any]:
    active_dimensions = [dim for dim in dimensions if dim.get("weight", 0) > 0]
    total_weight = sum(float(dim["weight"]) for dim in active_dimensions)

    if total_weight <= 0:
        weighted_average = 0.0
    else:
        weighted_average = sum(float(dim["weighted_score"]) for dim in active_dimensions) / total_weight

    calculated_overall = weighted_average / 5 * 100

    return {
        "method": "weighted_dimension_average",
        "dimension_scale": "0-5",
        "overall_scale": "0-100",
        "weighted_average": round(weighted_average, 2),
        "total_weight": round(total_weight, 2),
        "calculated_overall_score": round(calculated_overall, 1),
    }


def normalize_session(data: dict[str, Any]) -> dict[str, Any]:
    data = sanitize(data)

    data["schema_version"] = data.get("schema_version", "ai-effectiveness-retro-v0.2")
    data["created_at"] = data.get("created_at") or datetime.now(timezone.utc).isoformat()
    data["client"] = sanitize_text(data.get("client", "unknown"), 80)
    data["model"] = sanitize_text(data.get("model", "unknown"), 120)
    data["task"] = sanitize_text(data.get("task", "Untitled task"), 300)

    task_type = sanitize_text(data.get("task_type", "other"), 80)
    data["task_type"] = task_type if task_type in ALLOWED_TASK_TYPES else "other"

    data["task_profile"] = normalize_task_profile(data.get("task_profile"), data["task_type"])
    data["expected_verification"] = normalize_expected_verification(data.get("expected_verification"))
    data["score_confidence"] = normalize_score_confidence(data.get("score_confidence"))

    data["dimensions"], uses_adaptive_scoring = normalize_dimensions(data.get("dimensions"))
    score_calculation = calculate_score(data["dimensions"])
    data["score_calculation"] = score_calculation

    if uses_adaptive_scoring or data.get("overall_score") is None:
        data["overall_score"] = score_calculation["calculated_overall_score"]
    else:
        data["overall_score"] = clamp_number(data.get("overall_score", 0), 0.0, 100.0)
        data["score_calculation"]["method"] = "provided_overall_score"
        data["score_calculation"]["note"] = (
            "No adaptive weights were provided; preserved the supplied legacy overall score."
        )

    for key in ["what_worked", "what_reduced_effectiveness", "risks"]:
        data[key] = normalize_string_list(data.get(key), 600)

    data["recommendation"] = sanitize_text(data.get("recommendation", ""), 800)
    data["scoring_notes"] = sanitize_text(data.get("scoring_notes", ""), 1000)
    data["positive_signals"] = normalize_string_list(data.get("positive_signals"), 300)
    data["anti_pattern_flags"] = normalize_string_list(data.get("anti_pattern_flags"), 300)

    profile_update = data.get("profile_update")
    if not isinstance(profile_update, dict):
        profile_update = {}

    strengths = profile_update.get("strengths_observed", [])
    weaknesses = profile_update.get("weaknesses_or_antipatterns", [])

    data["profile_update"] = {
        "strengths_observed": [sanitize_text(item, 500) for item in strengths] if isinstance(strengths, list) else [],
        "weaknesses_or_antipatterns": [sanitize_text(item, 500) for item in weaknesses] if isinstance(weaknesses, list) else [],
        "suggested_memory_or_rule": sanitize_text(profile_update.get("suggested_memory_or_rule", ""), 800),
    }

    return data


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def append_markdown_session(path: Path, data: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## {data['created_at']} — {data['task']}\n\n")
        f.write(f"**Client:** {data['client']}\n\n")
        f.write(f"**Model:** {data['model']}\n\n")
        f.write(f"**Task type:** {data['task_type']}\n\n")

        task_profile = data["task_profile"]
        profile_parts = [
            f"{task_profile['complexity']} complexity",
            f"{task_profile['risk_level']} risk",
            f"{task_profile['change_type']} change",
            f"{task_profile['codebase_familiarity']} codebase familiarity",
        ]
        f.write(f"**Task profile:** {', '.join(profile_parts)}\n\n")
        if task_profile["change_surface"]:
            f.write(f"**Change surface:** {', '.join(task_profile['change_surface'])}\n\n")

        f.write(f"**Overall score:** {data['overall_score']:.0f}/100\n\n")

        calculation = data["score_calculation"]
        f.write(
            "**Score calculation:** "
            f"{calculation['method']} — weighted average "
            f"{calculation['weighted_average']:.2f}/5 across total weight "
            f"{calculation['total_weight']:.2f} = "
            f"{calculation['calculated_overall_score']:.0f}/100.\n\n"
        )
        if calculation.get("note"):
            f.write(f"**Score note:** {sanitize_text(calculation['note'], 500)}\n\n")

        confidence = data["score_confidence"]
        if confidence["level"] != "unknown" or confidence["reason"]:
            f.write(f"**Score confidence:** {confidence['level']} — {confidence['reason']}\n\n")

        if data["scoring_notes"]:
            f.write(f"**Scoring notes:** {sanitize_text(data['scoring_notes'], 1000)}\n\n")

        f.write("### Dimension scores\n\n")
        f.write("| Dimension | Score | Applicability | Weight | Evidence | Improvement |\n")
        f.write("|---|---:|---|---:|---|---|\n")

        for d in data["dimensions"]:
            f.write(
                f"| {md_escape(d.get('name', 'unknown'))} "
                f"| {md_escape(d.get('score', 'n/a'))} "
                f"| {md_escape(d.get('applicability', 'important'))} "
                f"| {md_escape(d.get('weight', 'n/a'))} "
                f"| {md_escape(d.get('evidence', 'not observed'))} "
                f"| {md_escape(d.get('improvement', ''))} |\n"
            )

        if data["expected_verification"]:
            f.write("\n### Expected verification\n\n")
            f.write("| Check | Status | Evidence |\n")
            f.write("|---|---|---|\n")
            for check in data["expected_verification"]:
                f.write(
                    f"| {md_escape(check.get('check', 'verification check'))} "
                    f"| {md_escape(check.get('status', 'not_observed'))} "
                    f"| {md_escape(check.get('evidence', ''))} |\n"
                )

        if data["positive_signals"]:
            f.write("\n### Positive workflow signals\n\n")
            for item in data["positive_signals"]:
                f.write(f"- {sanitize_text(item, 300)}\n")

        if data["anti_pattern_flags"]:
            f.write("\n### Anti-pattern flags\n\n")
            for item in data["anti_pattern_flags"]:
                f.write(f"- {sanitize_text(item, 300)}\n")

        f.write("\n### What worked well\n\n")
        for item in data["what_worked"]:
            f.write(f"- {sanitize_text(item, 500)}\n")

        f.write("\n### What reduced effectiveness\n\n")
        for item in data["what_reduced_effectiveness"]:
            f.write(f"- {sanitize_text(item, 500)}\n")

        f.write("\n### Risks observed\n\n")
        for item in data["risks"]:
            f.write(f"- {sanitize_text(item, 500)}\n")

        f.write("\n### Recommendation for next task\n\n")
        f.write(f"{sanitize_text(data['recommendation'], 800)}\n")


def append_profile_update(path: Path, data: dict[str, Any]) -> None:
    profile_update = data["profile_update"]

    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## {data['created_at']} — {data['task']}\n\n")
        f.write(f"**Client:** {data['client']}\n\n")

        f.write("### Strengths observed\n\n")
        for item in profile_update["strengths_observed"]:
            f.write(f"- {sanitize_text(item, 500)}\n")

        f.write("\n### Weaknesses / anti-patterns observed\n\n")
        for item in profile_update["weaknesses_or_antipatterns"]:
            f.write(f"- {sanitize_text(item, 500)}\n")

        f.write("\n### Suggested memory / rule\n\n")
        rule = profile_update["suggested_memory_or_rule"]
        if rule:
            f.write(f"- {sanitize_text(rule, 800)}\n")
        else:
            f.write("- not observed\n")


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception as exc:
        print(f"Failed to read valid JSON from stdin: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("Expected a JSON object", file=sys.stderr)
        return 1

    data = normalize_session(data)

    root = get_repo_root()
    out_dir = root / ".ai-effectiveness"
    out_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = out_dir / "sessions.jsonl"
    md_path = out_dir / "sessions.md"
    profile_updates_path = out_dir / "profile-updates.md"

    append_jsonl(jsonl_path, data)
    append_markdown_session(md_path, data)
    append_profile_update(profile_updates_path, data)

    print(f"Saved AI effectiveness retro to {md_path}")
    print(f"Saved structured data to {jsonl_path}")
    print(f"Saved profile update to {profile_updates_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
