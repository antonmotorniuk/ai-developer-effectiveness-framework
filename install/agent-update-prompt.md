Update AI Developer Effectiveness Framework in this repository.

Goal:
Refresh an existing local AI Developer Effectiveness Framework install without deleting session history.

Source:
Use the official repository:
https://github.com/antonmotorniuk/ai-developer-effectiveness-framework

Default update scope:
- Update runtime files inside `.ai-effectiveness/`.
- Preserve existing session history.
- Update the adapter for the current AI client if supported.
- Prefer user-level adapter instructions when the client supports them.
- Do not create `tools/ai-effectiveness/` in the target project.
- Do not modify application code.
- Do not stage or commit files unless I explicitly ask.

Preserve these files unless I explicitly ask to reset history:
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md

Refresh these files from the current framework version:
- .ai-effectiveness/config.json
- .ai-effectiveness/save_retro.py
- .ai-effectiveness/validate_session.py

Adapter update behavior:
- If this is Codex, update the Codex user-level skills if available:
  - ~/.codex/skills/ai-effectiveness-coach/SKILL.md
  - ~/.codex/skills/ai-coach/SKILL.md
  - or the current Codex environment's equivalent user skill directory.
- If adapter instructions are stored under `.ai-effectiveness/adapters/`, refresh those copies too.
- Do not modify project instruction files such as AGENTS.md, CLAUDE.md, or Cursor rules unless I explicitly approve it or the client cannot work without it.
- If marked AI effectiveness blocks already exist in project instruction files, update only the marked block and preserve everything else.

Safety rules:
- Inspect the existing install first.
- Show me the planned updates before overwriting runtime files.
- Do not delete session logs.
- Do not store secrets, tokens, credentials, private customer data, raw private chat transcripts, or large code snippets.
- This framework is for coaching and self-improvement, not employee surveillance, ranking, compensation, or performance punishment.

Implementation requirements:
1. Inspect `.ai-effectiveness/` and current adapter locations.
2. Verify which files will be preserved and which files will be refreshed.
3. Refresh `.ai-effectiveness/config.json`, `.ai-effectiveness/save_retro.py`, and `.ai-effectiveness/validate_session.py`.
4. Make scripts executable if the environment supports it.
5. Refresh the current AI client adapter if available.
6. Run validation:
   - `python3 -m py_compile .ai-effectiveness/save_retro.py .ai-effectiveness/validate_session.py`
   - `python3 .ai-effectiveness/validate_session.py`
7. Show the final list of changed files.
8. Remind me that I can close a session with `close ai session`, `$ai-coach close`, or `$ai-effectiveness-coach close`.
9. Remind me that `$ai-coach help` lists update, add-provider, and uninstall commands.
