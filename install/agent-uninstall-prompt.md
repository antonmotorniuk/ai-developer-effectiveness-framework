Uninstall AI Developer Effectiveness Framework from this repository.

Goal:
Remove the local AI Developer Effectiveness Framework integration from the current repository and, if I explicitly approve it, remove client-level adapter instructions such as the Codex skill.

Default uninstall scope:
- Remove the project-local `.ai-effectiveness/` folder.
- Remove AI effectiveness blocks from project instruction files only when they are clearly marked.
- Do not modify application code.
- Do not remove unrelated AI-agent instructions.
- Do not remove user-level/client-level skills unless I explicitly approve global cleanup.

Safety rules:
- Inspect the repository first.
- Show me the planned removals before deleting anything.
- If `.ai-effectiveness/` contains session history, ask whether I want to delete it or keep a backup before removing it.
- If `.gitignore` contains an exact `.ai-effectiveness/` entry, ask whether to remove that entry. Leave broader ignore rules untouched.
- Preserve all non-framework content in AGENTS.md, CLAUDE.md, Cursor rules, or similar instruction files.
- Remove only content between exact AI effectiveness markers when present:
  - `<!-- ai-effectiveness:start -->`
  - `<!-- ai-effectiveness:end -->`

Project-local cleanup checklist:
1. Inspect `.ai-effectiveness/` and list its files.
2. Inspect `.gitignore` for an exact `.ai-effectiveness/` entry.
3. Inspect project instruction files for marked AI effectiveness blocks.
4. Ask for confirmation before deleting `.ai-effectiveness/` if it contains session logs.
5. Remove `.ai-effectiveness/` only after confirmation.
6. Remove marked AI effectiveness blocks from project instruction files if present.
7. Optionally remove the exact `.ai-effectiveness/` ignore entry if I approve it.

Optional client-level cleanup:
If I ask for global/client cleanup too, inspect and ask before removing any of these paths:
- `~/.codex/skills/ai-effectiveness-coach/`
- `~/.codex/skills/ai-coach/`
- `~/.agents/skills/ai-effectiveness-coach/`
- `~/.agents/skills/ai-coach/`
- the current Codex environment's equivalent user skill directory

Important:
User-level skill removal affects other repositories that may use the framework, so do not remove it unless I explicitly confirm global/client cleanup.

Validation after uninstall:
- Show the final list of removed and modified files.
- Run `git status --short` if available.
- Confirm whether `.ai-effectiveness/` still exists.
- Confirm whether any AI effectiveness markers remain in project instruction files.
