# Adapters

The framework is tool-agnostic. AI coding clients are adapters.

## Core

The core is:

```text
.ai-effectiveness/
  config.json
  save_retro.py
  validate_session.py
  sessions.md
  sessions.jsonl
  profile-updates.md
```

Any AI agent can use the framework if it can:

1. evaluate a completed session;
2. produce a JSON retro object;
3. pass that JSON to `.ai-effectiveness/save_retro.py`.

Target-project installs are local-first. Keep runtime files and session outputs inside `.ai-effectiveness/`; project instruction files should be optional adapter surface, not required core storage.

## Codex adapter

The Codex adapter contains:

```text
adapters/codex/AGENTS.example.md
adapters/codex/skills/ai-effectiveness-coach/SKILL.md
```

## Claude Code adapter

Planned.

Expected files:

```text
adapters/claude-code/CLAUDE.example.md
adapters/claude-code/commands/ai-retro.md
```

## Cursor adapter

Planned.

Expected files:

```text
adapters/cursor/rules/ai-effectiveness.mdc
```

## Explicit session closing

This project intentionally evaluates completed sessions only.

Session closing is explicit: the user asks the agent to close, evaluate, and save the session.
