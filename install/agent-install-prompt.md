Install AI Developer Effectiveness Framework into this repository.

Goal:
Set up a local, tool-agnostic framework for evaluating completed AI-assisted development sessions. The framework should work with this AI client if supported, but the core data format and scripts must remain client-agnostic.

Source:
Use the official repository:
https://github.com/antonmotorniuk/ai-developer-effectiveness-framework

If the repository is not available from this environment, create the files from the structure and contents available in the current context, and clearly list any placeholders that still need to be replaced.

Installation scope:
- Install the core framework files under `.ai-effectiveness/` only.
- Do not create `tools/ai-effectiveness/` in the target project.
- Install the adapter for the current AI client if supported.
- Prefer user-level adapter instructions when the client supports them.
- Do not modify project instruction files such as AGENTS.md, CLAUDE.md, or Cursor rules unless I explicitly approve it or the client cannot work without it.
- Keep the workflow explicit: the developer asks the agent to close a completed session.
- Do not add hooks, wrappers, background automation, reporting surfaces, or manager analytics.
- Do not modify application code.

Git behavior:
- Treat this as a personal/local install by default.
- Offer to add `.ai-effectiveness/` to `.gitignore`.
- If `.ai-effectiveness/` is already ignored, leave it alone.
- Do not stage or commit framework files unless I explicitly ask.

Safety rules:
- Do not overwrite existing project instructions blindly.
- If project instruction files must be changed, preserve their content and append the AI effectiveness section between clear markers.
- Do not store secrets, tokens, credentials, private customer data, raw private chat transcripts, or large code snippets.
- This framework is for coaching and self-improvement, not employee surveillance, ranking, compensation, or performance punishment.
- Show me a summary of planned changes before making them if anything looks risky.

Expected local files:
- .ai-effectiveness/config.json
- .ai-effectiveness/save_retro.py
- .ai-effectiveness/validate_session.py
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md

Expected adapter behavior:
- If this is Codex, install or update the Codex user-level skill if available:
  - ~/.codex/skills/ai-effectiveness-coach/SKILL.md
  - or the current Codex environment's equivalent user skill directory.
- If a user-level skill directory is not available, place adapter instructions under `.ai-effectiveness/adapters/codex/` and explain how to install them manually.
- If this is Claude Code, install or propose the Claude Code adapter if supported by the current repository and client.
- If this is Cursor, install or propose the Cursor rules adapter if supported by the current repository and client.
- If the current client cannot be detected, install core only and explain how to add an adapter later.

Implementation requirements:
1. Inspect the repository structure.
2. Detect existing instruction files and `.gitignore`.
3. Create missing `.ai-effectiveness/` files.
4. Add the universal save script at `.ai-effectiveness/save_retro.py`.
5. Add the validator at `.ai-effectiveness/validate_session.py`.
6. Make scripts executable if the environment supports it.
7. Add or update the current AI client adapter without removing existing instructions.
8. Run a basic validation:
   - verify expected files exist;
   - verify save_retro.py and validate_session.py are syntactically valid;
   - if possible, run `python3 -m py_compile .ai-effectiveness/save_retro.py .ai-effectiveness/validate_session.py`.
9. Show the final list of created or modified files.
10. Explain how I should close my first AI-assisted session.

After installation, I should be able to finish a task and ask either:

close ai session

or:

$ai-effectiveness-coach close

The task name is optional. If I do not provide one, infer a concise task title from the session and ask only when the task cannot be reasonably inferred.

The framework should then save:
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md
