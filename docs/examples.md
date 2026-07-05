# Examples

## Closing A Session In Codex

```text
close ai session
```

or:

```text
$ai-coach close
```

The longer Codex skill name remains supported:

```text
$ai-effectiveness-coach close
```

Optional explicit task name:

```text
$ai-effectiveness-coach close for task "Fix login redirect bug"
```

## Local Framework Commands

These are prompts to your AI agent, not terminal commands:

```text
$ai-coach help
$ai-coach update
$ai-coach add-provider codex
$ai-coach uninstall
```

Use `add-provider` for AI coding client adapters such as `codex`, `claude-code`, or `cursor`.

## Expected Result

The adapter produces an adaptive retro, then saves it through the local project script:

```bash
python3 .ai-effectiveness/save_retro.py <<'JSON'
{ ... }
JSON
```

The framework updates:

```text
.ai-effectiveness/sessions.md
.ai-effectiveness/sessions.jsonl
.ai-effectiveness/profile-updates.md
```

`sessions.md` contains the human-readable score explanation, including task profile, dimension applicability, weights, expected verification, and confidence.

## Adaptive Scoring Smoke Check

This repository includes a sample JSON retro at:

```text
examples/session-retro.sample.json
```

Use it as the input shape for a smoke check in any project where the framework is installed:

```bash
python3 .ai-effectiveness/save_retro.py < path/to/session-retro.sample.json
python3 .ai-effectiveness/validate_session.py
```

The sample intentionally sets `overall_score` to `0`. When adaptive dimension weights are present, `save_retro.py` recalculates the saved overall score from the weighted dimension average.
