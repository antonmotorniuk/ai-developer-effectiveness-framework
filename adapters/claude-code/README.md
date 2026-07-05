# Claude Code adapter

Planned adapter.

The core framework is already tool-agnostic. A Claude Code adapter only needs to:

1. instruct Claude Code how to evaluate a completed AI-assisted session;
2. produce the standard JSON session object;
3. call `tools/ai-effectiveness/save_retro.py`.

This MVP intentionally supports explicit session closing only.
