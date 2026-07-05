# AI Developer Effectiveness Framework

A tool-agnostic framework for evaluating and improving how software developers use AI during real engineering work.

The goal is not to measure “how much AI was used”. The goal is to understand whether AI was used effectively: with clear problem framing, useful context, appropriate planning, careful verification, and real engineering ownership.

## Why this exists

AI coding tools are becoming normal in software development, but the quality of AI usage varies a lot.

Two developers can use the same tool and get very different outcomes:

- one improves delivery speed while keeping quality high;
- another creates hidden technical debt, weak tests, review bottlenecks, or code they do not fully understand.

This framework helps developers turn AI-assisted work into a feedback loop.

## Recommended installation: ask your AI agent

The primary installation flow is **agent-led setup**.

Open your target project in Codex, Claude Code, Cursor, or another AI coding assistant and paste the prompt from:

```text
install/agent-install-prompt.md
```

The agent will install the framework as a local, project-scoped `.ai-effectiveness/` folder, adapt it to the current AI client if supported, and show the final list of changed files.

By default, the installed framework is personal/local. You can ignore the whole `.ai-effectiveness/` folder in Git. If another developer wants the framework, they can run the same agent-led install prompt in their own workspace.

This MVP intentionally does **not** provide a manual quick-start guide in the README. The intended user experience is:

```text
Open project in AI coding agent
→ paste the install prompt
→ review changed files
→ work normally
→ ask the agent to close the session when a task is done
```

## Minimal prompt

If you do not want to open the full prompt file, paste this into your AI coding agent:

```text
Install AI Developer Effectiveness Framework into this repository.

Use the official repository:
https://github.com/antonmotorniuk/ai-developer-effectiveness-framework

Requirements:
- install the core framework locally under `.ai-effectiveness/`;
- install the adapter for the current AI client if supported;
- install only the explicit completed-session retro flow;
- do not add hooks, wrappers, management reporting, or background automation;
- do not modify application code;
- preserve existing instruction files unless I explicitly approve adapter changes;
- offer to ignore `.ai-effectiveness/` in Git for personal/local use;
- show the final list of created or modified files;
- explain how I should close my first AI-assisted session.

Use install/agent-install-prompt.md as the full installation contract.
```

## Usage after installation

Work normally in your AI coding assistant.

At the end of a completed task, ask the agent to close the AI effectiveness session.

For Codex, use the short form:

```text
close ai session
```

or:

```text
$ai-coach close
```

The longer skill name remains supported:

```text
$ai-effectiveness-coach close
```

A task name is optional. If you do not provide one, the agent should infer a concise task title from the session and ask only when it cannot reasonably infer one.

You can still provide an explicit task name when useful:

```text
$ai-effectiveness-coach close for task "Fix login redirect bug"
```

## Agent commands

After installation, these are prompts to your AI coding agent, not terminal commands:

```text
$ai-coach help
$ai-coach close
$ai-coach update
$ai-coach add-provider codex
$ai-coach uninstall
```

`provider` means AI coding client adapter, such as `codex`, `claude-code`, or `cursor`.

The command behavior is intentionally explicit:

- `close` evaluates and saves a completed AI-assisted session.
- `update` refreshes local runtime files and the current adapter while preserving session history.
- `add-provider <provider>` adds or refreshes an adapter for another AI coding client when supported.
- `uninstall` removes the local project integration and asks before deleting session history or user-level skills.
- `help` explains the available commands without modifying files.

For other clients, use the equivalent adapter instruction. If no adapter exists yet, ask the agent to produce a session retro JSON and pass it to:

```text
.ai-effectiveness/save_retro.py
```

## What this framework evaluates

Each AI-assisted development session is evaluated across seven dimensions:

1. Problem framing
2. Context quality
3. Planning discipline
4. Tool/model/mode usage
5. Verification discipline
6. Ownership and understanding
7. Learning loop

Each dimension is scored from `0` to `5`. The overall score is calculated as a weighted average so small, low-risk tasks are not punished for skipping heavy planning or tests that do not fit the work.

## What gets installed into a target project

After agent-led installation, the target project should contain one local folder:

```text
.ai-effectiveness/
  config.json
  save_retro.py
  validate_session.py
  sessions.md
  sessions.jsonl
  profile-updates.md
```

For personal use, this whole folder can be added to `.gitignore`:

```gitignore
.ai-effectiveness/
```

Client adapters should prefer user-level instructions when available. Project instruction files such as `AGENTS.md`, `CLAUDE.md`, or Cursor rules should only be changed when the user approves that adapter behavior or the client requires it.

## Local files

After installation, `.ai-effectiveness/` contains runtime files and personal session outputs.

Runtime files:

```text
.ai-effectiveness/config.json
.ai-effectiveness/save_retro.py
.ai-effectiveness/validate_session.py
```

Session output files:

```text
.ai-effectiveness/sessions.md
.ai-effectiveness/sessions.jsonl
.ai-effectiveness/profile-updates.md
```

- `config.json` describes the methodology and scoring dimensions.
- `save_retro.py` saves completed-session retros.
- `validate_session.py` checks saved JSONL records.
- `sessions.md` is a human-readable log.
- `sessions.jsonl` is structured data for scripts, reports, and future personal analysis.
- `profile-updates.md` stores repeated patterns, strengths, weaknesses, and coaching recommendations.

## Example Session Record

```json
{
  "schema_version": "ai-effectiveness-retro-v0.2",
  "client": "codex",
  "model": "unknown",
  "task": "Fix login redirect bug",
  "task_type": "bugfix",
  "task_profile": {
    "complexity": "medium",
    "risk_level": "medium",
    "change_type": "app_code",
    "codebase_familiarity": "medium",
    "ai_role": "assistant",
    "change_surface": ["auth flow", "tests"]
  },
  "overall_score": 0,
  "score_confidence": {
    "level": "medium",
    "reason": "The prompt, touched files, and focused verification were visible; broader production behavior was not fully exercised."
  },
  "dimensions": [
    {
      "name": "Problem framing",
      "score": 4,
      "applicability": "important",
      "weight": 1.0,
      "weight_reason": "Clear framing mattered, but the task was already narrow.",
      "evidence": "The task and expected outcome were stated.",
      "improvement": "Add explicit acceptance criteria before implementation."
    },
    {
      "name": "Verification discipline",
      "score": 3,
      "applicability": "core",
      "weight": 1.25,
      "weight_reason": "A login redirect bug needs direct verification evidence.",
      "evidence": "A focused check was run.",
      "improvement": "Run the broader regression suite or record why it was skipped."
    }
  ],
  "expected_verification": [
    {
      "check": "Focused login redirect scenario",
      "status": "done",
      "evidence": "A targeted check was observed."
    }
  ],
  "scoring_notes": "Planning and verification were weighted for a medium-risk app-code bugfix.",
  "positive_signals": ["repo_conventions_checked", "small_batch_changes"],
  "anti_pattern_flags": ["unclear_acceptance_criteria"],
  "what_worked": ["The task stayed narrow."],
  "what_reduced_effectiveness": ["Acceptance criteria were implicit."],
  "risks": ["Edge cases may remain uncovered."],
  "recommendation": "Before implementation, ask the agent to list assumptions, edge cases, and verification steps appropriate to task risk.",
  "profile_update": {
    "strengths_observed": ["Good at narrowing down bugs with AI."],
    "weaknesses_or_antipatterns": ["Sometimes starts implementation before clarifying acceptance criteria."],
    "suggested_memory_or_rule": "Before implementation, list assumptions, edge cases, and verification steps appropriate to task risk."
  }
}
```

When adaptive weights are present, `save_retro.py` recalculates `overall_score` from the weighted dimension average and records the calculation in `sessions.md`.

## What this is not

This project is not intended for:

- employee surveillance;
- compensation decisions;
- stack ranking developers;
- punishing people for not using AI;
- measuring productivity by accepted AI-generated lines of code.

The intended use is coaching, self-improvement, research, and team-level learning.

## What is intentionally not included

This MVP does **not** include:

- lifecycle hooks or background automation;
- proactive prompts before work begins;
- desktop wrappers;
- management reporting surfaces;
- automatic chat transcript extraction.

The first version focuses only on closing completed AI-assisted sessions and saving structured retrospectives.

## Privacy principles

The framework should not store:

- secrets;
- API keys;
- access tokens;
- passwords;
- private customer data;
- large code snippets;
- confidential business context.

It should store:

- summaries;
- scores;
- patterns;
- recommendations;
- task type;
- observed verification steps;
- high-level risks;
- coaching notes.

## Supported clients

Current adapter:

- Codex

Planned adapters:

- Claude Code
- Cursor
- Continue
- Aider
- Other AI coding agents and IDE assistants

The methodology, schema, and scripts are tool-agnostic. Client-specific integrations are adapters.

## Adding another provider

To add an adapter for another AI coding client to an existing local install, ask your AI agent:

```text
$ai-coach add-provider claude-code
```

or paste:

```text
install/agent-add-provider-prompt.md
```

Unsupported providers should leave the core `.ai-effectiveness/` files untouched and explain what adapter work is still missing.

## Roadmap

- [x] Core session schema
- [x] Adaptive task-profile and weighted scoring model
- [x] Markdown + JSONL storage
- [x] `save_retro.py`
- [x] Codex adapter MVP
- [x] Agent-led installation prompt
- [x] Agent-led update prompt
- [x] Agent-led uninstall prompt
- [x] Agent-led add-provider prompt
- [ ] Claude Code adapter
- [ ] Cursor adapter
- [ ] Weekly review command
- [ ] Markdown report generator
- [ ] Charts from `sessions.jsonl`
- [ ] Privacy-preserving aggregate learning notes
- [ ] Public article with first results

## Development checks

```bash
python3 -m py_compile tools/ai-effectiveness/save_retro.py tools/ai-effectiveness/validate_session.py
python3 -m unittest discover -s tests
```

The source repository keeps maintainer copies of the scripts under `tools/ai-effectiveness/`. Agent-led installation copies them into the target project's `.ai-effectiveness/` folder.

## Updating

To update an existing local install without deleting session history, open the target project in your AI coding assistant and paste:

```text
install/agent-update-prompt.md
```

After the Codex adapter is installed, you can also ask:

```text
$ai-coach update
```

The update flow refreshes `.ai-effectiveness/config.json`, `.ai-effectiveness/save_retro.py`, `.ai-effectiveness/validate_session.py`, and the current client adapter while preserving `sessions.md`, `sessions.jsonl`, and `profile-updates.md`.

## Uninstalling

To remove the framework from a target project, open that project in your AI coding assistant and paste:

```text
install/agent-uninstall-prompt.md
```

After the Codex adapter is installed, you can also ask:

```text
$ai-coach uninstall
```

The uninstall flow removes the local `.ai-effectiveness/` folder, cleans marked project instruction blocks, and asks before removing any user-level AI client skill because that can affect other repositories.

## License

MIT
