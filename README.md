# AI Developer Effectiveness Framework

A tool-agnostic framework for evaluating and improving how software developers use AI during real engineering work.

The goal is not to measure “how much AI was used”. The goal is to understand whether AI was used effectively: with clear problem framing, useful context, appropriate planning, careful verification, and real engineering ownership.

## Why this exists

AI coding tools are becoming normal in software development, but the quality of AI usage varies a lot.

Two developers can use the same tool and get very different outcomes:

- one improves delivery speed while keeping quality high;
- another creates hidden technical debt, weak tests, review bottlenecks, or code they do not fully understand.

This framework helps developers turn AI-assisted work into a feedback loop.

## What this framework evaluates

Each AI-assisted development session is evaluated across seven dimensions:

1. Problem framing
2. Context quality
3. Planning discipline
4. Tool/model/mode usage
5. Verification discipline
6. Ownership and understanding
7. Learning loop

Each dimension is scored from `0` to `5`. The overall score is converted to a `0–100` scale.

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

- SessionStart hooks;
- startup advice shown before work starts;
- desktop wrappers;
- dashboards;
- team analytics;
- automatic chat transcript extraction.

The first version focuses only on closing completed AI-assisted sessions and saving structured retrospectives.

## Core files in an instrumented project

After installation, a target project contains:

```text
.ai-effectiveness/
  config.json
  sessions.md
  sessions.jsonl
  profile-updates.md

tools/
  ai-effectiveness/
    save_retro.py
```

- `sessions.md` is a human-readable log.
- `sessions.jsonl` is structured data for scripts, reports, dashboards, and future analysis.
- `profile-updates.md` stores repeated patterns, strengths, weaknesses, and coaching recommendations.
- `config.json` describes the methodology and scoring dimensions.

## Recommended installation: agent-led setup

Open your project in Codex, Claude Code, Cursor, or another AI coding assistant.

Copy the prompt from:

```text
install/agent-install-prompt.md
```

Paste it into your AI agent and let it install the framework into the current repository.

The agent should:

- install the core framework;
- install the adapter for the current AI client if supported;
- avoid modifying application code;
- avoid SessionStart hooks;
- avoid startup advice;
- preserve existing instruction files;
- show the final list of changed files.

## Quick start for Codex

This repository currently includes a Codex adapter.

### 1. Install core files into your project

Copy:

```text
.ai-effectiveness/config.json
tools/ai-effectiveness/save_retro.py
```

from `examples/sample-project/` and `tools/` into your target project, or use the agent-led install prompt.

Create empty log files:

```bash
mkdir -p .ai-effectiveness
mkdir -p tools/ai-effectiveness

touch .ai-effectiveness/sessions.md
touch .ai-effectiveness/sessions.jsonl
touch .ai-effectiveness/profile-updates.md
chmod +x tools/ai-effectiveness/save_retro.py
```

### 2. Add Codex project instructions

Copy:

```text
adapters/codex/AGENTS.example.md
```

into the target project as:

```text
AGENTS.md
```

If `AGENTS.md` already exists, append only the AI effectiveness section.

### 3. Install the Codex skill adapter

Copy:

```text
adapters/codex/skills/ai-effectiveness-coach/
```

to:

```text
~/.agents/skills/ai-effectiveness-coach/
```

Restart Codex.

### 4. Work normally

Use your AI coding assistant as usual.

At the end of a task, ask Codex:

```text
$ai-effectiveness-coach close the session for task "Fix login redirect bug"
```

The skill asks the model to evaluate the session and save the result using the project-local script.

## Output files

After closing a session, the framework updates:

```text
.ai-effectiveness/sessions.md
.ai-effectiveness/sessions.jsonl
.ai-effectiveness/profile-updates.md
```

## Example session record

```json
{
  "schema_version": "ai-effectiveness-retro-v0.1",
  "client": "codex",
  "model": "unknown",
  "task": "Fix login redirect bug",
  "task_type": "bugfix",
  "overall_score": 72,
  "dimensions": [
    {
      "name": "Problem framing",
      "score": 4,
      "evidence": "The user described the bug and expected outcome.",
      "improvement": "Add explicit acceptance criteria before implementation."
    },
    {
      "name": "Verification discipline",
      "score": 3,
      "evidence": "Some tests were discussed, but full test execution was not observed.",
      "improvement": "Run regression tests or document why they were not available."
    }
  ],
  "what_worked": [
    "The task was narrowed down quickly.",
    "The diff was reviewed before finalizing.",
    "The assistant was asked to explain the approach."
  ],
  "what_reduced_effectiveness": [
    "Acceptance criteria were not explicit.",
    "Edge cases were considered late.",
    "Verification evidence was incomplete."
  ],
  "risks": [
    "AI-generated changes may miss edge cases.",
    "Test coverage was not fully observed."
  ],
  "recommendation": "Before implementation, ask the AI to list assumptions, edge cases, and test cases.",
  "profile_update": {
    "strengths_observed": [
      "Good at narrowing down bugs with AI."
    ],
    "weaknesses_or_antipatterns": [
      "Sometimes starts implementation before clarifying acceptance criteria."
    ],
    "suggested_memory_or_rule": "Before implementation, list assumptions, edge cases, and test cases."
  }
}
```

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

## Roadmap

- [x] Core session schema
- [x] Markdown + JSONL storage
- [x] `save_retro.py`
- [x] Codex adapter MVP
- [x] Agent-led installation prompt
- [ ] Claude Code adapter
- [ ] Cursor adapter
- [ ] Weekly review command
- [ ] Markdown report generator
- [ ] Charts from `sessions.jsonl`
- [ ] Team-level anonymized insights
- [ ] Public article with first results

## License

MIT

## Publishing this project to GitHub

This repository includes a helper script for publishing the framework to GitHub via GitHub CLI.

```bash
scripts/publish_to_github.sh ai-developer-effectiveness-framework --public
```

Requirements:

- `git`
- GitHub CLI `gh`
- authenticated GitHub CLI session via `gh auth login`

You can also ask your AI coding agent to publish the project using:

```text
install/agent-publish-prompt.md
```

