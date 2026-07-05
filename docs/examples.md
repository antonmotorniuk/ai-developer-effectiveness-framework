# Examples

## Closing a session in Codex

```text
close ai session
```

or:

```text
$ai-effectiveness-coach close
```

Optional explicit task name:

```text
$ai-effectiveness-coach close for task "Fix login redirect bug"
```

## Expected result

The adapter produces a retro, then saves it through the local project script:

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

## Sample retro input

This repository includes a sample JSON retro at:

```text
examples/session-retro.sample.json
```

Use it as the input shape for a smoke check in any project where the framework is installed:

```bash
python3 .ai-effectiveness/save_retro.py < path/to/session-retro.sample.json
python3 .ai-effectiveness/validate_session.py
```
