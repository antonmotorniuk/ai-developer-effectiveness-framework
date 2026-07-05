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

The agent will install the framework into the current repository, adapt it to the current AI client if supported, and show the final list of changed files.

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
- install the core framework;
- install the adapter for the current AI client if supported;
- install only the explicit completed-session retro flow;
- do not add hooks, wrappers, management reporting, or background automation;
- do not modify application code;
- preserve existing instruction files;
- show the final list of created or modified files;
- explain how I should close my first AI-assisted session.

Use install/agent-install-prompt.md as the full installation contract.
```

## Usage after installation

Work normally in your AI coding assistant.

At the end of a completed task, ask the agent to close the AI effectiveness session.

For Codex, the command is usually:

```text
$ai-effectiveness-coach close the session for task "Fix login redirect bug"
```

For other clients, use the equivalent adapter instruction. If no adapter exists yet, ask the agent to produce a session retro JSON and pass it to:

```text
tools/ai-effectiveness/save_retro.py
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

Each dimension is scored from `0` to `5`. The overall score is converted to a `0–100` scale.

## What gets installed into a target project

After agent-led installation, the target project should contain:

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

Client adapters may add extra instruction files, for example:

```text
AGENTS.md
~/.agents/skills/ai-effectiveness-coach/SKILL.md
```

for Codex.

## Output files

After closing a session, the framework updates:

```text
.ai-effectiveness/sessions.md
.ai-effectiveness/sessions.jsonl
.ai-effectiveness/profile-updates.md
```

- `sessions.md` is a human-readable log.
- `sessions.jsonl` is structured data for scripts, reports, and future personal analysis.
- `profile-updates.md` stores repeated patterns, strengths, weaknesses, and coaching recommendations.
- `config.json` describes the methodology and scoring dimensions.

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
- [ ] Privacy-preserving aggregate learning notes
- [ ] Public article with first results

## Development checks

```bash
python3 -m py_compile tools/ai-effectiveness/save_retro.py tools/ai-effectiveness/validate_session.py
python3 -m unittest discover -s tests
```

## Publishing this project to GitHub

This repository includes a helper script for publishing the framework to GitHub via GitHub CLI:

```bash
scripts/publish_to_github.sh ai-developer-effectiveness-framework --public
```

You can also ask your AI coding agent to publish the project using:

```text
install/agent-publish-prompt.md
```

## License

MIT
