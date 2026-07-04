# Privacy and safety principles

This framework is designed for coaching and self-improvement.

## Do not store

Do not store:

- secrets;
- API keys;
- access tokens;
- passwords;
- private customer data;
- large code snippets;
- confidential business context;
- raw private chat transcripts unless explicitly intended and reviewed.

## Store only summaries

Prefer storing:

- task type;
- high-level task summary;
- scores;
- observed verification steps;
- workflow risks;
- recommendations;
- strengths and anti-patterns;
- file paths only when safe.

## Human validation

AI-generated evaluation should be treated as a coaching signal, not a final judgement.

Developers should be able to correct the evaluation when the AI did not observe something, such as tests run outside the chat.

## Manager and team usage

If used in a team, prefer aggregate patterns over individual ranking.

Good team-level use:

- common verification gaps;
- repeated context quality issues;
- shared coaching opportunities;
- team-level AI workflow maturity.

Bad use:

- ranking developers by AI score;
- compensation decisions;
- surveillance;
- punishing people for low AI usage;
- rewarding accepted AI-generated lines of code.
