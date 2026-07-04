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

## Overall score

The overall score is:

```text
average_dimension_score / 5 * 100
```

Example:

```text
average = 3.6 / 5
overall = 72 / 100
```

## Dimension details

### Problem framing

How clearly was the task stated?

Look for:

- goal;
- expected outcome;
- constraints;
- acceptance criteria;
- business or product context.

### Context quality

Did the AI have enough context?

Look for:

- relevant files;
- errors/logs;
- stack information;
- architecture constraints;
- examples;
- edge cases.

### Planning discipline

Was there a plan before implementation?

Look for:

- implementation plan;
- assumptions;
- alternatives;
- risks;
- test plan.

### Tool/model/mode usage

Was the AI tool used appropriately?

Look for:

- chat vs agent vs autocomplete;
- exploration vs implementation;
- code review;
- tests;
- repo search;
- appropriate model/tool choice where observable.

### Verification discipline

Was the result validated?

Look for:

- tests;
- lint;
- typecheck;
- manual checks;
- diff review;
- security/performance sanity checks.

### Ownership and understanding

Did the developer appear to understand and own the result?

Look for:

- clarifying questions;
- asking for explanations;
- rejecting or adjusting AI output;
- reviewing assumptions;
- not blindly accepting changes.

### Learning loop

Did the session produce reusable learning?

Look for:

- updated rules;
- repeated anti-patterns identified;
- prompts improved;
- recommendations captured;
- profile updates.
