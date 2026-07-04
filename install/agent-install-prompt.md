Install AI Developer Effectiveness Framework into this repository.

Goal:
Set up a tool-agnostic framework for evaluating AI-assisted development sessions. The framework should work with this AI client if supported, but the core data format and scripts must remain client-agnostic.

Source:
Use the official repository:
https://github.com/<OWNER>/ai-developer-effectiveness-framework

If the repository is not published yet, create the files from the structure and contents available in the current context, and clearly tell me which placeholders still need to be replaced.

Installation mode:
- Install core framework.
- Install adapter for the current AI client if supported.
- Do not enable startup advice.
- Do not enable SessionStart hooks.
- Do not enable any hooks.
- Do not enable desktop wrappers.
- Do not create dashboards.
- Do not modify application code.

Safety rules:
- Do not overwrite existing project instructions blindly.
- If AGENTS.md, CLAUDE.md, Cursor rules, or similar instruction files already exist, preserve their content and append the AI effectiveness section between clear markers.
- Do not store secrets, tokens, credentials, private customer data, or large code snippets.
- This framework is for coaching and self-improvement, not employee surveillance or performance punishment.
- Show me a summary of planned changes before making them if anything looks risky.

Expected project files:
- .ai-effectiveness/config.json
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md
- tools/ai-effectiveness/save_retro.py

Expected adapter behavior:
- If this is Codex, install or update the Codex adapter:
  - AGENTS.md project instructions
  - ~/.agents/skills/ai-effectiveness-coach/SKILL.md if global user-level skills are available
- If this is Claude Code, install or propose the Claude Code adapter if supported.
- If this is Cursor, install or propose the Cursor rules adapter if supported.
- If the current client cannot be detected, install core only and explain how to add an adapter later.

Implementation requirements:
1. Inspect the repository structure.
2. Detect existing instruction files.
3. Create missing .ai-effectiveness files.
4. Add the universal save script at tools/ai-effectiveness/save_retro.py.
5. Make the script executable if the environment supports it.
6. Add or update the current AI client adapter.
7. Do not enable startup advice.
8. Do not enable hooks of any kind.
9. Run a basic validation:
   - verify files exist;
   - verify save_retro.py is syntactically valid;
   - if possible, run python3 -m py_compile tools/ai-effectiveness/save_retro.py.
10. Show the final list of created/modified files.
11. Explain how I should close my first AI-assisted session.

After installation, I should be able to finish a task and ask:

$ai-effectiveness-coach close the session for task "..."

The framework should then save:
- .ai-effectiveness/sessions.md
- .ai-effectiveness/sessions.jsonl
- .ai-effectiveness/profile-updates.md
