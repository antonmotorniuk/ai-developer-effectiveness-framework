# Scoring

Each dimension is scored from 0 to 5.

## 0

No evidence of the behavior, or the behavior was actively harmful.

## 1

Very weak. The behavior was mostly missing and created risk or rework.

## 2

Weak. Some evidence exists, but important parts were missing.

## 3

Adequate. The behavior was present but inconsistent or incomplete.

## 4

Strong. The behavior was clearly present and supported the outcome.

## 5

Excellent. The behavior was deliberate, repeatable, and clearly improved the AI-assisted workflow.

## Applicability And Weight

Each dimension gets an applicability level for the current task:

| Applicability | Default weight | Meaning |
|---|---:|---|
| `core` | 1.25 | Essential for this task shape. |
| `important` | 1.0 | Normally relevant for this task shape. |
| `optional` | 0.5 | Useful, but lightweight evidence is enough. |
| `not_applicable` | 0.0 | Does not meaningfully apply to this task. |

This keeps scoring flexible. A small docs correction should not be punished for skipping a full implementation plan or unit tests. A risky payment, auth, migration, release, or infra task should weight planning, verification, and ownership more heavily.

## Overall Score

For adaptive v0.2 records, the overall score is:

```text
sum(score * weight) / sum(weight) / 5 * 100
```

Example:

```text
Problem framing: 5.0 * 1.0 = 5.0
Planning discipline: 4.0 * 0.5 = 2.0
Verification discipline: 4.5 * 1.25 = 5.625

total weighted score = 12.625
total weight = 2.75
weighted average = 4.59 / 5
overall = 92 / 100
```

For older v0.1 records with no adaptive weights, the saver preserves the supplied overall score for backward compatibility and records the equal-weight calculation separately.

## Task Profile

Before scoring, classify the task:

- `complexity`: `small`, `medium`, `large`, or `unknown`;
- `risk_level`: `low`, `medium`, `high`, or `unknown`;
- `change_type`: docs, script, app code, config, infra, research, review, or another useful label;
- `codebase_familiarity`: `low`, `medium`, `high`, or `unknown`;
- `ai_role`: assistant, pair, reviewer, researcher, or other;
- `change_surface`: the files, modules, systems, or docs touched.

## Verification Fit

Expected verification depends on the task shape:

- docs: rendered text, links, examples, and consistency;
- scripts/tooling: syntax check plus fixture, sample, smoke test, or dry run when possible;
- app code: focused tests, type/lint checks, manual scenario checks, or documented reason checks could not run;
- high-risk work: stronger test evidence, rollback thinking, and review of assumptions.

Do not penalize a session for skipping checks that genuinely do not apply. Do penalize missing checks that should reasonably exist for the task's risk and complexity.

## Dimension Details

### Problem Framing

How clearly was the task stated?

Look for:

- goal;
- expected outcome;
- constraints;
- acceptance criteria;
- business or product context.

### Context Quality

Did the AI have enough context?

Look for:

- relevant files;
- errors/logs;
- stack information;
- architecture constraints;
- examples;
- edge cases.

### Planning Discipline

Was the amount of planning appropriate for the task?

Look for:

- implementation plan;
- assumptions;
- alternatives;
- risks;
- test plan.

For small low-risk tasks, a short mental or written plan can be enough. For complex or risky tasks, weak planning should reduce the score more strongly.

### Tool/Model/Mode Usage

Was the AI tool used appropriately?

Look for:

- chat vs agent vs autocomplete;
- exploration vs implementation;
- code review;
- tests;
- repo search;
- appropriate model/tool choice where observable.

### Verification Discipline

Was the result validated in a way that fit the task?

Look for:

- tests;
- lint;
- typecheck;
- manual checks;
- diff review;
- docs/render checks;
- security/performance sanity checks;
- a clear reason when expected checks could not run.

### Ownership And Understanding

Did the developer appear to understand and own the result?

Look for:

- clarifying questions;
- asking for explanations;
- rejecting or adjusting AI output;
- reviewing assumptions;
- not blindly accepting changes.

### Learning Loop

Did the session produce reusable learning?

Look for:

- updated rules;
- repeated anti-patterns identified;
- prompts improved;
- recommendations captured;
- profile updates.

Future-improvement notes are good learning-loop evidence when they are specific, grounded, and do not unnecessarily expand the current task.
