# Methodology

AI Developer Effectiveness Framework evaluates completed AI-assisted software development sessions.

It is designed to answer:

> Did the developer use AI effectively during this work session?

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

## Evaluation dimensions

1. Problem framing
2. Context quality
3. Planning discipline
4. Tool/model/mode usage
5. Verification discipline
6. Ownership and understanding
7. Learning loop

Each dimension is scored from `0` to `5`.

The overall score is the average dimension score converted to a 0–100 scale.

## Evidence rule

The evaluator must use only evidence available in the session:

- conversation;
- visible repository context;
- diffs;
- commands run;
- test/lint/typecheck results;
- files changed;
- explicit user messages.

If evidence is missing, write `not observed`.

## Intended use

The intended use is coaching and self-improvement:

- find repeated anti-patterns;
- improve prompt/context quality;
- improve verification discipline;
- improve planning and ownership;
- support research and public writing.

## Excluded use

This framework should not be used for:

- surveillance;
- compensation decisions;
- promotion decisions;
- stack ranking;
- punishment;
- forcing AI usage.
