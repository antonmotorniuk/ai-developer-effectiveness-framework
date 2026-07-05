#!/usr/bin/env python3

"""Basic validation for AI Effectiveness JSONL logs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".ai-effectiveness/sessions.jsonl")

    if not path.exists():
        print(f"Missing file: {path}")
        return 1

    errors = 0
    count = 0

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        count += 1
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"Line {line_no}: invalid JSON: {exc}")
            errors += 1
            continue

        for key in ["schema_version", "client", "task", "task_type", "overall_score", "dimensions"]:
            if key not in item:
                print(f"Line {line_no}: missing key {key}")
                errors += 1

    if errors:
        print(f"Validation failed: {errors} error(s) across {count} session(s).")
        return 1

    print(f"Validation passed: {count} session(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
