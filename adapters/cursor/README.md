# Cursor adapter

Planned adapter.

The core framework is already tool-agnostic. A Cursor adapter only needs to:

1. add project/user rules for session closing;
2. produce the standard JSON session object;
3. call `tools/ai-effectiveness/save_retro.py`.

This MVP intentionally does not include hooks or startup advice.
