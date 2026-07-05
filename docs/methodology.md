# Methodology

AI Developer Effectiveness Framework evaluates completed AI-assisted software development sessions.

It is designed to answer:

> Did the developer use AI effectively for this specific work session?

It does not evaluate the developer as a person. It evaluates the workflow pattern visible in a particular session.

## Session

A session is one completed unit of AI-assisted work, such as:

- bugfix;
- feature implementation;
- refactor;
- test writing;
- documentation;
- investigation;
- code review;
- debugging.

## Task Profile

Before scoring, classify the task shape:

- `complexity`: `small`, `medium`, `large`, or `unknown`;
- `risk_level`: `low`, `medium`, `high`, or `unknown`;
- `change_type`: docs, script, app code, config, infra, research, review, or another useful label;
- `codebase_familiarity`: `low`, `medium`, `high`, or `unknown`;
- `ai_role`: assistant, pair, reviewer, researcher, or other;
- `change_surface`: the high-level files, modules, systems, or docs touched.

The task profile prevents false precision. A small README wording change should not be scored as if it were a production payment-flow migration.

## Evaluation Dimensions

1. Problem framing
2. Context quality
3. Planning discipline
4. Tool/model/mode usage
5. Verification discipline
6. Ownership and understanding
7. Learning loop

Each dimension is scored from `0` to `5`.

Each dimension also gets an applicability level and weight:

- `core`: essential for the task shape, default weight `1.25`;
- `important`: normally relevant, default weight `1.0`;
- `optional`: useful but lightweight evidence is enough, default weight `0.5`;
- `not_applicable`: not meaningful for the task, weight `0`.

The overall score is the weighted dimension average converted to a 0-100 scale:

```text
sum(score * weight) / sum(weight) / 5 * 100
```

If no adaptive weights are provided, older v0.1 records can still keep their supplied overall score for backward compatibility.

## Flexible Expectations

Score the fit between the workflow and the task, not the amount of ceremony performed.

Small, low-risk documentation tasks may only need clear framing, relevant context, and a quick consistency check. Heavy planning, unit tests, or broad regression checks can be marked `optional` or `not_applicable` when they genuinely do not fit.

Complex or high-risk work should raise the weight of planning, verification, and ownership. Examples include payment logic, auth, migrations, infra, release work, security-sensitive code, or broad refactors.

## Verification Expectations

Verification should be appropriate to the task:

- docs: rendered text, links, examples, and consistency checks;
- scripts/tooling: syntax checks plus a fixture, sample, dry run, or smoke test when possible;
- app code: focused tests, type/lint checks, manual scenario checks, or a documented reason checks could not run;
- high-risk changes: stronger test evidence, rollback thinking, and explicit review of assumptions.

Skipping irrelevant checks should not reduce the score. Skipping checks that reasonably fit the task should reduce the score.

## Evidence Rule

The evaluator must use only evidence available in the session:

- conversation;
- visible repository context;
- diffs;
- commands run;
- test/lint/typecheck results;
- files changed;
- explicit user messages.

If evidence is missing, write `not observed`.

## Score Confidence

The evaluator should record score confidence as `low`, `medium`, or `high`.

Confidence is lower when evidence is incomplete, the session started before the evaluator joined, commands were not visible, or the task outcome cannot be inspected. Confidence is higher when the prompt, context gathering, diff, verification, and final state are visible.

## Learning Loop

The learning loop dimension measures whether the session produced reusable learning without expanding the task unnecessarily.

A task can be complete and still produce a future improvement note. That should usually be scored as a positive learning signal, not as a failure, when the recommendation is concrete and grounded in observed workflow.

## Intended Use

The intended use is coaching and self-improvement:

- find repeated anti-patterns;
- improve prompt/context quality;
- improve verification discipline;
- improve planning and ownership;
- support research and public writing.

## Excluded Use

This framework should not be used for:

- surveillance;
- compensation decisions;
- promotion decisions;
- stack ranking;
- punishment;
- forcing AI usage.
