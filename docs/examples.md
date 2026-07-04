# Examples

## Closing a session in Codex

```text
$ai-effectiveness-coach close the session for task "Fix login redirect bug"
```

## Expected result

The adapter produces a retro, then saves it through:

```bash
python3 tools/ai-effectiveness/save_retro.py <<'JSON'
{ ... }
JSON
```

The framework updates:

```text
.ai-effectiveness/sessions.md
.ai-effectiveness/sessions.jsonl
.ai-effectiveness/profile-updates.md
```
