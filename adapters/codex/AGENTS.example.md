<!-- ai-effectiveness:start -->
## AI effectiveness experiment

This repository uses `.ai-effectiveness/` to track AI-assisted development effectiveness.

The methodology is tool-agnostic. Codex is only one client adapter.

When the user explicitly asks to close, review, evaluate, or save an AI-assisted work session, use the AI Developer Effectiveness Framework.

Use these files:

- `.ai-effectiveness/config.json`
- `.ai-effectiveness/save_retro.py`
- `.ai-effectiveness/validate_session.py`
- `.ai-effectiveness/sessions.md`
- `.ai-effectiveness/sessions.jsonl`
- `.ai-effectiveness/profile-updates.md`

Rules:

- Save retros with `.ai-effectiveness/save_retro.py` and validate with `.ai-effectiveness/validate_session.py` when available.
- Run only when the user explicitly asks to close, review, evaluate, or save an AI-assisted work session.
- Accept short requests such as `close ai session`, `close session`, `save retro`, `$ai-coach close`, or `$ai-effectiveness-coach close`.
- Infer a concise task title when the user does not provide one; ask only if it cannot be reasonably inferred.
- Keep session closing explicit.
- Do not use or create hooks of any kind for this framework.
- Do not interrupt normal development workflow.
- Do not invent evidence.
- If something was not visible in the session, write `not observed`.
- Classify task complexity, risk, change type, codebase familiarity, AI role, and change surface before scoring.
- Use adaptive scoring: mark each dimension as core, important, optional, or not applicable, then weight it by fit to the task.
- Do not penalize small low-risk tasks for skipping heavy planning or tests that do not fit; do penalize missing planning or verification for risky or complex work.
- Do not save secrets, tokens, credentials, private customer data, or large code snippets.
- The goal is coaching and self-improvement, not performance evaluation or surveillance.
<!-- ai-effectiveness:end -->
