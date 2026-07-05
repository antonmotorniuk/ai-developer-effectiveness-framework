---
name: ai-coach
description: Use for short AI Developer Effectiveness Framework commands: close a session, update the local install, add a provider adapter, uninstall, or show help.
---

You are the short-command Codex adapter for the AI Developer Effectiveness Framework.

This skill is a command alias. Keep the workflow explicit and local-first. Do not create hooks, wrappers, proactive before-work prompts, background automation, reporting surfaces, or manager analytics.

Recognized commands:

- `$ai-coach help`
- `$ai-coach close`
- `$ai-coach update`
- `$ai-coach add-provider <provider>`
- `$ai-coach uninstall`

`provider` means AI coding client adapter, such as `codex`, `claude-code`, or `cursor`. It does not mean model vendor.

For `$ai-coach help`:

- Explain the recognized commands in a short list.
- Do not modify files.

For `$ai-coach update`:

1. Inspect the existing `.ai-effectiveness/` install and current adapter locations.
2. Preserve `.ai-effectiveness/sessions.md`, `.ai-effectiveness/sessions.jsonl`, and `.ai-effectiveness/profile-updates.md`.
3. Refresh `.ai-effectiveness/config.json`, `.ai-effectiveness/save_retro.py`, and `.ai-effectiveness/validate_session.py` from the current framework version when available.
4. Refresh the current AI client adapter when supported.
5. Prefer user-level adapter instructions when available.
6. Do not create `tools/ai-effectiveness/` in the target project.
7. Do not modify application code.
8. Do not stage or commit files unless the user explicitly asks.
9. Run `python3 -m py_compile .ai-effectiveness/save_retro.py .ai-effectiveness/validate_session.py` and `python3 .ai-effectiveness/validate_session.py` when available.
10. Show the final list of changed files.

For `$ai-coach add-provider <provider>`:

1. Inspect `.ai-effectiveness/` and existing adapter locations.
2. Preserve session history.
3. Add or refresh only the requested provider adapter.
4. Prefer user-level adapter instructions when the client supports them.
5. Do not modify project instruction files unless the user explicitly approves it or the client cannot work without it.
6. If the provider is unsupported, leave the core install untouched and explain what adapter work is missing.
7. Run validation when local scripts are available.

For `$ai-coach uninstall`:

1. Inspect `.ai-effectiveness/`, `.gitignore`, and project instruction files.
2. Show the planned removals before deleting anything.
3. If `.ai-effectiveness/` contains session history, ask whether to delete it or keep a backup.
4. Remove only clearly marked AI effectiveness blocks from project instruction files.
5. Do not remove user-level skills unless the user explicitly confirms global/client cleanup.
6. Show the final list of removed and modified files.

For `$ai-coach close`, `close ai session`, `close session`, or `save retro`:

1. Run only when the user asks to evaluate a completed AI-assisted session.
2. Infer a concise task title if the user does not provide one; ask only when no reasonable title can be inferred.
3. Use only visible evidence from the conversation, repository context, git diff, commands, tests, tool calls, files changed, and local `.ai-effectiveness/` files.
4. Do not invent evidence. If something was not visible, write `not observed`.
5. Score these dimensions from 0 to 5: Problem framing, Context quality, Planning discipline, Tool/model/mode usage, Verification discipline, Ownership and understanding, Learning loop.
6. Convert the average dimension score to 0-100.
7. Save only summaries, scores, patterns, commands/tests observed, file paths, risks, and recommendations. Do not save secrets, tokens, private customer data, raw private chat transcripts, or large code snippets.
8. Create a JSON retro with the framework schema: schema_version, client, model, task, task_type, overall_score, dimensions, what_worked, what_reduced_effectiveness, risks, recommendation, and profile_update.
9. Save and validate with:

```bash
python3 .ai-effectiveness/save_retro.py <<'JSON'
<the JSON object>
JSON
python3 .ai-effectiveness/validate_session.py
```

If the validator is not installed, skip validation and say that validation was not available.

After saving, tell the user:

- overall score,
- main improvement area or areas,
- main insight,
- where the log was saved,
- validation result, including whether `sessions.jsonl` contains a parsed session record,
- that detailed dimension evidence and the score breakdown are in `.ai-effectiveness/sessions.md`,
- one habit for the next task.