Add an AI Developer Effectiveness Framework provider adapter to this repository.

Goal:
Add or refresh an adapter for a specific AI coding client without deleting local AI effectiveness history.

Provider:
Use the provider name I gave with this request. Examples:
- codex
- claude-code
- cursor
- continue
- aider

Provider means AI coding client adapter, not model vendor.

Source:
Use the official repository:
https://github.com/antonmotorniuk/ai-developer-effectiveness-framework

If the repository is not available from this environment, use the framework files available in the current context and clearly list anything that could not be refreshed.

Default scope:
- Preserve the existing `.ai-effectiveness/` folder and session history.
- Add or refresh adapter instructions for the requested provider only.
- Prefer user-level adapter instructions when the client supports them.
- Do not create `tools/ai-effectiveness/` in the target project.
- Do not modify application code.
- Do not stage or commit files unless I explicitly ask.

Preserve these files unless I explicitly ask to reset history:
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md

Safety rules:
- Inspect the existing install first.
- Show me the planned adapter changes before editing project instruction files or user-level instructions.
- Do not overwrite existing project instructions blindly.
- Do not modify AGENTS.md, CLAUDE.md, Cursor rules, or similar files unless I explicitly approve it or the client cannot work without it.
- If marked AI effectiveness blocks already exist in project instruction files, update only the marked block and preserve everything else.
- Do not store secrets, tokens, credentials, private customer data, raw private chat transcripts, or large code snippets.
- This framework is for coaching and self-improvement, not employee surveillance, ranking, compensation, or performance punishment.

Provider behavior:
- If the requested provider is Codex, install or update the Codex user-level skills if available:
  - ~/.codex/skills/ai-effectiveness-coach/SKILL.md
  - ~/.codex/skills/ai-coach/SKILL.md
  - or the current Codex environment's equivalent user skill directory.
- If the requested provider is Claude Code, install or propose the Claude Code adapter if supported by the current framework version.
- If the requested provider is Cursor, install or propose the Cursor adapter if supported by the current framework version.
- If the requested provider is not supported yet, leave the core install untouched and explain what adapter files would need to be created later.

Implementation requirements:
1. Inspect `.ai-effectiveness/` and existing adapter locations.
2. Verify session history files will be preserved.
3. Add or refresh only the requested provider adapter.
4. If adapter instructions are stored under `.ai-effectiveness/adapters/`, refresh those copies too.
5. Run validation if the local scripts are installed:
   - `python3 -m py_compile .ai-effectiveness/save_retro.py .ai-effectiveness/validate_session.py`
   - `python3 .ai-effectiveness/validate_session.py`
6. Show the final list of created or modified files.
7. Remind me that I can run `$ai-coach help` to see available commands.