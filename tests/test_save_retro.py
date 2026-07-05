from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "tools" / "ai-effectiveness" / "save_retro.py"
SOURCE_VALIDATOR = ROOT / "tools" / "ai-effectiveness" / "validate_session.py"
INSTALLED_SCRIPT = Path(".ai-effectiveness") / "save_retro.py"
INSTALLED_VALIDATOR = Path(".ai-effectiveness") / "validate_session.py"


def base_payload() -> dict:
    return {
        "schema_version": "ai-effectiveness-retro-v0.2",
        "created_at": "2026-01-01T00:00:00+00:00",
        "client": "codex",
        "model": "unknown",
        "task": "Add login redirect test",
        "task_type": "test",
        "task_profile": {
            "complexity": "medium",
            "risk_level": "medium",
            "change_type": "app_code",
            "codebase_familiarity": "medium",
            "ai_role": "assistant",
            "change_surface": ["auth flow", "tests"],
        },
        "overall_score": 0,
        "score_confidence": {
            "level": "medium",
            "reason": "The focused change and test evidence were visible.",
        },
        "dimensions": [
            {
                "name": "Problem framing",
                "score": 4,
                "applicability": "important",
                "weight": 1.0,
                "weight_reason": "The task was narrow but still needed expected behavior.",
                "evidence": "Goal and expected behavior were stated.",
                "improvement": "Add explicit edge cases before implementation.",
            },
            {
                "name": "Verification discipline",
                "score": 3,
                "applicability": "core",
                "weight": 1.25,
                "weight_reason": "A test task depends heavily on verification evidence.",
                "evidence": "A focused test was added.",
                "improvement": "Run the broader regression suite when available.",
            },
        ],
        "expected_verification": [
            {
                "check": "Focused login redirect test",
                "status": "done",
                "evidence": "The new test was observed.",
            },
            {
                "check": "Broader auth regression suite",
                "status": "skipped",
                "evidence": "Not observed in this session.",
            },
        ],
        "scoring_notes": "Verification was weighted as core because this was a test task.",
        "positive_signals": ["small_batch_changes", "expected_checks_run"],
        "anti_pattern_flags": ["unclear_acceptance_criteria"],
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


def install_framework_scripts(project: Path) -> None:
    out_dir = project / ".ai-effectiveness"
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_SCRIPT, project / INSTALLED_SCRIPT)
    shutil.copyfile(SOURCE_VALIDATOR, project / INSTALLED_VALIDATOR)


def run_save_retro(cwd: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    install_framework_scripts(cwd)
    return subprocess.run(
        [sys.executable, str(INSTALLED_SCRIPT)],
        input=json.dumps(payload),
        text=True,
        cwd=cwd,
        capture_output=True,
        check=False,
    )


def run_validator(cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLED_VALIDATOR)],
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

            self.assertTrue((out_dir / "save_retro.py").exists())
            self.assertTrue((out_dir / "validate_session.py").exists())
            self.assertTrue(jsonl_path.exists())
            self.assertTrue(sessions_md_path.exists())
            self.assertTrue(profile_path.exists())

            saved = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(saved["task"], "Add login redirect test")
            self.assertEqual(saved["task_type"], "test")
            self.assertEqual(saved["schema_version"], "ai-effectiveness-retro-v0.2")
            self.assertAlmostEqual(saved["overall_score"], 68.9)
            self.assertEqual(saved["score_calculation"]["method"], "weighted_dimension_average")
            self.assertEqual(saved["score_calculation"]["total_weight"], 2.25)
            self.assertEqual(saved["task_profile"]["risk_level"], "medium")
            self.assertEqual(saved["expected_verification"][0]["status"], "done")
            self.assertEqual(len(saved["dimensions"]), 2)
            self.assertEqual(saved["dimensions"][1]["applicability"], "core")
            self.assertEqual(saved["dimensions"][1]["weight"], 1.25)

            sessions_md = sessions_md_path.read_text(encoding="utf-8")
            self.assertIn("Add login redirect test", sessions_md)
            self.assertIn("Score calculation", sessions_md)
            self.assertIn("| Verification discipline | 3.0 | core | 1.25 |", sessions_md)
            self.assertIn("Expected verification", sessions_md)

            profile_md = profile_path.read_text(encoding="utf-8")
            self.assertIn("Ask for acceptance criteria", profile_md)

            validation = run_validator(project)
            self.assertEqual(validation.returncode, 0, validation.stderr)
            self.assertIn("Validation passed: 1 session(s).", validation.stdout)

    def test_normalizes_scores_task_type_and_sensitive_text_for_legacy_payloads(self) -> None:
        payload = base_payload()
        payload["schema_version"] = "ai-effectiveness-retro-v0.1"
        payload["task_type"] = "unsupported"
        payload["overall_score"] = 999
        payload["recommendation"] = "Use api_key=abc123 in the prompt."
        payload["what_worked"] = ["No secret here", "Token looked like sk-live-secret"]
        for dimension in payload["dimensions"]:
            dimension.pop("applicability", None)
            dimension.pop("weight", None)
            dimension.pop("weight_reason", None)
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
            self.assertEqual(saved["score_calculation"]["method"], "provided_overall_score")
            self.assertEqual(saved["dimensions"][0]["score"], 0.0)
            self.assertEqual(saved["dimensions"][0]["evidence"], "[REDACTED: possible secret]")
            self.assertEqual(saved["recommendation"], "[REDACTED: possible secret]")
            self.assertEqual(saved["what_worked"][1], "[REDACTED: possible secret]")

    def test_not_applicable_dimensions_do_not_affect_adaptive_score(self) -> None:
        payload = base_payload()
        payload["dimensions"].append(
            {
                "name": "Planning discipline",
                "score": 0,
                "applicability": "not_applicable",
                "weight": 2.0,
                "weight_reason": "No separate plan was needed for this tiny follow-up.",
                "evidence": "not observed",
                "improvement": "not applicable",
            }
        )

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = run_save_retro(project, payload)

            self.assertEqual(result.returncode, 0, result.stderr)

            jsonl_path = project / ".ai-effectiveness" / "sessions.jsonl"
            saved = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertAlmostEqual(saved["overall_score"], 68.9)
            self.assertEqual(saved["dimensions"][2]["weight"], 0.0)
            self.assertEqual(saved["score_calculation"]["total_weight"], 2.25)


if __name__ == "__main__":
    unittest.main()
