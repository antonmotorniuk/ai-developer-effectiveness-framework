Install AI Developer Effectiveness Framework into this repository.

Goal:
Set up a tool-agnostic framework for evaluating completed AI-assisted development sessions. The framework should work with this AI client if supported, but the core data format and scripts must remain client-agnostic.

Source:
Use the official repository:
https://github.com/antonmotorniuk/ai-developer-effectiveness-framework

If the repository is not available from this environment, create the files from the structure and contents available in the current context, and clearly list any placeholders that still need to be replaced.

Installation scope:
- Install the core framework files.
- Install the adapter for the current AI client if supported.
- Keep the workflow explicit: the developer asks the agent to close a completed session.
- Do not add hooks, wrappers, background automation, reporting surfaces, or manager analytics.
- Do not modify application code.

Safety rules:
- Do not overwrite existing project instructions blindly.
- If AGENTS.md, CLAUDE.md, Cursor rules, or similar instruction files already exist, preserve their content and append the AI effectiveness section between clear markers.
- Do not store secrets, tokens, credentials, private customer data, raw private chat transcripts, or large code snippets.
- This framework is for coaching and self-improvement, not employee surveillance, ranking, compensation, or performance punishment.
- Show me a summary of planned changes before making them if anything looks risky.

Expected core files:
- .ai-effectiveness/config.json
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md
- tools/ai-effectiveness/save_retro.py

Expected adapter behavior:
- If this is Codex, install or update the Codex adapter:
  - append the marked AI effectiveness section to AGENTS.md, preserving any existing content;
  - install ~/.agents/skills/ai-effectiveness-coach/SKILL.md only if user-level skills are available in this environment.
- If this is Claude Code, install or propose the Claude Code adapter if supported by the current repository and client.
- If this is Cursor, install or propose the Cursor rules adapter if supported by the current repository and client.
- If the current client cannot be detected, install core only and explain how to add an adapter later.

Implementation requirements:
1. Inspect the repository structure.
2. Detect existing instruction files.
3. Create missing .ai-effectiveness files.
4. Add the universal save script at tools/ai-effectiveness/save_retro.py.
5. Make the script executable if the environment supports it.
6. Add or update the current AI client adapter without removing existing instructions.
7. Run a basic validation:
   - verify expected files exist;
   - verify save_retro.py is syntactically valid;
   - if possible, run python3 -m py_compile tools/ai-effectiveness/save_retro.py.
8. Show the final list of created or modified files.
9. Explain how I should close my first AI-assisted session.

After installation, I should be able to finish a task and ask:

$ai-effectiveness-coach close the session for task "..."

The framework should then save:
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md
