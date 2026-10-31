# Spec-readiness standard

Applies before authors start. The reviewer reads the spec cold, without the conversation that produced it. Report findings in the finding schema. A blocker stops the run.

A spec is ready when a stranger could build it, test it and tell when it is done.

1. Goal: one sentence naming who benefits and what changes for them.
2. Done criteria: each one can be checked by a command, a test or an observation. Report any that cannot.
3. Scope: what is in, what is out, and what is deferred. Report an unstated boundary.
4. Inputs and outputs: shapes, units, limits and error cases. Report any case with no stated behavior.
5. Dependencies and compatibility: what it needs, what it changes for existing users, and the rollout order.
6. Risks and unknowns: each has an owner or a check. Report unknowns written as facts.
7. Terms: every term is defined where first used, or points at a definition.
8. Traceability: every done criterion maps to a task, and every task maps to a done criterion.

Severity guide: a missing done criterion, an untestable done criterion or a contradiction is a blocker. A missing error case is major. Wording is a nit.
