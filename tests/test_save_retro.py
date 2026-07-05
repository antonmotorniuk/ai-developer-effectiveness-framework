from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ai-effectiveness" / "save_retro.py"


def base_payload() -> dict:
    return {
        "schema_version": "ai-effectiveness-retro-v0.1",
        "created_at": "2026-01-01T00:00:00+00:00",
        "client": "codex",
        "model": "unknown",
        "task": "Add login redirect test",
        "task_type": "test",
        "overall_score": 72,
        "dimensions": [
            {
                "name": "Problem framing",
                "score": 4,
                "evidence": "Goal and expected behavior were stated.",
                "improvement": "Add explicit edge cases before implementation.",
            },
            {
                "name": "Verification discipline",
                "score": 3,
                "evidence": "A focused test was added.",
                "improvement": "Run the broader regression suite when available.",
            },
        ],
        "what_worked": ["The task stayed narrow."],
        "what_reduced_effectiveness": ["Acceptance criteria could be clearer."],
        "risks": ["Regression coverage may still be incomplete."],
        "recommendation": "List acceptance criteria before editing.",
        "profile_update": {
            "strengths_observed": ["Good at narrowing the task."],
            "weaknesses_or_antipatterns": ["Verification evidence was partial."],
            "suggested_memory_or_rule": "Ask for acceptance criteria before implementation.",
        },
    }


def run_save_retro(cwd: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        text=True,
        cwd=cwd,
        capture_output=True,
        check=False,
    )


class SaveRetroTests(unittest.TestCase):
    def test_writes_jsonl_markdown_and_profile_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = run_save_retro(project, base_payload())

            self.assertEqual(result.returncode, 0, result.stderr)

            out_dir = project / ".ai-effectiveness"
            jsonl_path = out_dir / "sessions.jsonl"
            sessions_md_path = out_dir / "sessions.md"
            profile_path = out_dir / "profile-updates.md"

            self.assertTrue(jsonl_path.exists())
            self.assertTrue(sessions_md_path.exists())
            self.assertTrue(profile_path.exists())

            saved = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(saved["task"], "Add login redirect test")
            self.assertEqual(saved["task_type"], "test")
            self.assertEqual(saved["overall_score"], 72.0)
            self.assertEqual(len(saved["dimensions"]), 2)

            sessions_md = sessions_md_path.read_text(encoding="utf-8")
            self.assertIn("Add login redirect test", sessions_md)
            self.assertIn("| Problem framing | 4.0 |", sessions_md)

            profile_md = profile_path.read_text(encoding="utf-8")
            self.assertIn("Ask for acceptance criteria", profile_md)

    def test_normalizes_scores_task_type_and_sensitive_text(self) -> None:
        payload = base_payload()
        payload["task_type"] = "unsupported"
        payload["overall_score"] = 999
        payload["recommendation"] = "Use api_key=abc123 in the prompt."
        payload["what_worked"] = ["No secret here", "Token looked like sk-live-secret"]
        payload["dimensions"][0]["score"] = -5
        payload["dimensions"][0]["evidence"] = "The password was pasted."

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = run_save_retro(project, payload)

            self.assertEqual(result.returncode, 0, result.stderr)

            jsonl_path = project / ".ai-effectiveness" / "sessions.jsonl"
            saved = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertEqual(saved["task_type"], "other")
            self.assertEqual(saved["overall_score"], 100.0)
            self.assertEqual(saved["dimensions"][0]["score"], 0.0)
            self.assertEqual(saved["dimensions"][0]["evidence"], "[REDACTED: possible secret]")
            self.assertEqual(saved["recommendation"], "[REDACTED: possible secret]")
            self.assertEqual(saved["what_worked"][1], "[REDACTED: possible secret]")


if __name__ == "__main__":
    unittest.main()