<!-- ai-effectiveness:start -->
## AI effectiveness experiment

This repository uses `.ai-effectiveness/` to track AI-assisted development effectiveness.

The methodology is tool-agnostic. Codex is only one client adapter.

When the user explicitly asks to close, review, evaluate, or save an AI-assisted work session, use the AI Developer Effectiveness Framework.

Use these files:

- `.ai-effectiveness/config.json`
- `.ai-effectiveness/sessions.md`
- `.ai-effectiveness/sessions.jsonl`
- `.ai-effectiveness/profile-updates.md`
- `tools/ai-effectiveness/save_retro.py`

Rules:

- Run only when the user explicitly asks to close, review, evaluate, or save an AI-assisted work session.
- Keep session closing explicit.
- Do not use or create hooks of any kind for this framework.
- Do not interrupt normal development workflow.
- Do not invent evidence.
- If something was not visible in the session, write `not observed`.
- Do not save secrets, tokens, credentials, private customer data, or large code snippets.
- The goal is coaching and self-improvement, not performance evaluation or surveillance.
<!-- ai-effectiveness:end -->
