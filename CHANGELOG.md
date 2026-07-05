# Changelog

## Unreleased

- switched target-project installs to a local-first `.ai-effectiveness/` layout;
- added `.ai-effectiveness/validate_session.py` to installed core files;
- updated Codex closeout wording to use main improvement area language;
- added validation reporting to the Codex close-session flow;
- removed GitHub publishing helper files from the MVP surface;
- added an agent-led uninstall prompt for local and optional client-level cleanup;
- added an agent-led update prompt that preserves session history;
- made task names optional for close-session requests and documented shorter close commands.

## 0.1.0

Initial MVP:

- core framework structure;
- JSONL and Markdown storage;
- universal `save_retro.py`;
- Codex adapter MVP;
- agent-led installation prompt;
- explicit completed-session retro workflow;
- no background automation.
