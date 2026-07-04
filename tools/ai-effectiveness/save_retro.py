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


def md_escape(value: Any) -> str:
    return sanitize_text(value, 500).replace("|", "\\|").replace("\n", " ")


def normalize_session(data: dict[str, Any]) -> dict[str, Any]:
    data = sanitize(data)

    data["schema_version"] = data.get("schema_version", "ai-effectiveness-retro-v0.1")
    data["created_at"] = data.get("created_at") or datetime.now(timezone.utc).isoformat()
    data["client"] = sanitize_text(data.get("client", "unknown"), 80)
    data["model"] = sanitize_text(data.get("model", "unknown"), 120)
    data["task"] = sanitize_text(data.get("task", "Untitled task"), 300)

    task_type = sanitize_text(data.get("task_type", "other"), 80)
    data["task_type"] = task_type if task_type in ALLOWED_TASK_TYPES else "other"

    try:
        score = float(data.get("overall_score", 0))
    except (TypeError, ValueError):
        score = 0.0
    data["overall_score"] = max(0.0, min(100.0, score))

    if not isinstance(data.get("dimensions"), list):
        data["dimensions"] = []

    normalized_dimensions = []
    for dim in data["dimensions"]:
        if not isinstance(dim, dict):
            continue
        try:
            dim_score = float(dim.get("score", 0))
        except (TypeError, ValueError):
            dim_score = 0.0
        normalized_dimensions.append(
            {
                "name": sanitize_text(dim.get("name", "unknown"), 120),
                "score": max(0.0, min(5.0, dim_score)),
                "evidence": sanitize_text(dim.get("evidence", "not observed"), 800),
                "improvement": sanitize_text(dim.get("improvement", ""), 800),
            }
        )
    data["dimensions"] = normalized_dimensions

    for key in ["what_worked", "what_reduced_effectiveness", "risks"]:
        if not isinstance(data.get(key), list):
            data[key] = []
        data[key] = [sanitize_text(item, 600) for item in data[key]]

    data["recommendation"] = sanitize_text(data.get("recommendation", ""), 800)

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
        f.write(f"**Overall score:** {data['overall_score']:.0f}/100\n\n")

        f.write("### Dimension scores\n\n")
        f.write("| Dimension | Score | Evidence | Improvement |\n")
        f.write("|---|---:|---|---|\n")

        for d in data["dimensions"]:
            f.write(
                f"| {md_escape(d.get('name', 'unknown'))} "
                f"| {md_escape(d.get('score', 'n/a'))} "
                f"| {md_escape(d.get('evidence', 'not observed'))} "
                f"| {md_escape(d.get('improvement', ''))} |\n"
            )

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
