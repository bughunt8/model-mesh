# The four engineering gates - worked examples

Concrete walk-throughs of the grill (Step 1), prototype (Step 3.5), test-first (Step 4), and two-axis review (Step 4 close) gates. Each shows the trigger, the work, and the owed report line. Gate concepts adapted from matt-pocock/skills; evidence/negative-test and false-green discipline from debug-pipeline2 (see repo `THIRD_PARTY_NOTICES.md`).

Read the SKILL first; this file is the "show me" companion.

---

## Grill (Step 1) - decisions, not facts, one at a time

**Task:** "Add rate limiting to the API."

**Trigger present?** Yes - "rate limiting" hides several decisions (scope, limit, identity, over-limit behavior). Attended. Grill fires.

**Mini-orient first (resolve facts by looking, never ask):**
- List routes -> the API is `express` with an existing `middleware/` dir. (fact, found)
- Grep for an existing limiter -> none. (fact, found)
- Check for a shared store -> `redis` client already configured in `db/redis.ts`. (fact, found)

**Now the genuine decisions, one at a time, each with a recommendation:**
1. "Rate-limit all routes, or only the auth + write endpoints? *I recommend auth + writes only* - read-only GETs are cheap and limiting them hurts legit use." -> user: "auth + writes."
2. "Limit key: per-IP or per-authenticated-user? *I recommend per-user with per-IP fallback for unauthenticated routes.*" -> user: "per-user, IP fallback."
3. "Over-limit response: 429 with `Retry-After`, or silent drop? *I recommend 429 + `Retry-After`* - it's the standard and clients can back off." -> user: "429."

Stop - three decisions settled, remaining unknowns (exact numbers) are reversible config. Do not ask them; pick sane defaults and note them.

**Owed line:** `GRILL: asked 3 decisions; open decisions defaulted: limit=100/min per user (tunable via env)`

**Anti-example:** asking "does the project use Redis?" is a *fact* - you look that up, you never spend a question on it.

---

## Prototype (Step 3.5) - throwaway code answers one question

**Task:** "Let two workers claim jobs from the queue without ever double-processing one."

**Trigger present?** Yes - concurrency / race condition on state this change writes, and correctness depends on interleaving. Not answerable by reading alone. Prototype fires. (If a single `SELECT ... FOR UPDATE SKIP LOCKED` already existed and was documented, you would read it and skip.)

**The one question:** "Does `UPDATE jobs SET owner=? WHERE id=(SELECT id ... LIMIT 1) AND owner IS NULL` actually prevent two workers grabbing the same row under real interleaving?"

**Throwaway harness** (`scratch/claim_race.prototype.ts`, one command to run):
- Spawn two async "workers" against a test table seeded with one claimable job.
- Force the interleaving: both read the candidate id, then both attempt the guarded UPDATE.
- Print full state after each action; assert exactly one UPDATE reports `rowCount === 1`.

**Verdict captured (pasted into the report):**
```
worker A: candidate=42  worker B: candidate=42
worker A UPDATE rowCount=1   worker B UPDATE rowCount=0
final: job 42 owner=A ; B saw no claim -> loops for next job   OK: no double-claim
```
Decision: the guarded conditional UPDATE is sufficient; no explicit lock needed. Fold that into the plan. **Delete the prototype** (no AUTH quote to keep it). The transcript above is the primary source, so nothing is lost.

**Owed line:** `PROTO: race on job-claim - prototyped, verdict: guarded conditional UPDATE prevents double-claim (1 vs 0 rowCount)`

**Negative-gate example (do NOT prototype):** "Which of two button colors looks better?" on a reversible local style - that is a judgement, not an emergent-behavior risk; just pick one and move on.

---

## Test-first (Step 4) - seams, observed red, one slice

**Task:** the rate limiter from the grill example.

**Seam agreed:** the middleware's public behavior - "the 101st request in a window from one user gets a 429 with `Retry-After`." (Named in Step 3 / confirmed with user. Not the internal counter - that is an implementation detail.)

**Slice 1, red first:**
```
test: "allows 100 then 429s the 101st for one user"
run -> FAIL: expected 429, got 200 (no limiter exists yet)   # observed red, right reason
```
Implement the minimum: counter keyed by user in Redis, 429 past the limit.
```
run -> PASS
```
**Slice 2, red first:** "resets after the window elapses" -> run -> FAIL (no expiry) -> add TTL -> PASS.

Each expected value comes from the spec (100/min), not recomputed from the code (no tautology). No internal mock (no implementation coupling).

**Owed line:** `SEAMS: rate-limit middleware (429 past limit; window reset) - 2 red->green slices, each observed red first`

**Escape example:** the task is "bump the copyright year in the footer string" - no meaningful seam; skip TDD, verify by rendering the page. `SEAMS: none testable (static string) - verified by observation instead`.

---

## Two-axis review (Step 4 close) - Spec and Standards, kept apart

**Task:** the rate limiter, implementation complete.

1. **Materialize the diff:** `git diff --stat` -> `middleware/rateLimit.ts | 48 ++, app.ts | 3 +, middleware/rateLimit.test.ts | 40 ++`. Review that text, not memory.
2. **Two isolated passes** (as two fresh subagents given only the diff + the grill decisions + `CONTRIBUTING.md`, never told each other's verdict):
   - **Spec axis** (against the grill decisions): auth+writes only? yes. per-user + IP fallback? **IP fallback missing** - unauthenticated routes currently 500 on a null key. Finding: requirement partial. Quote: "per-user, IP fallback."
   - **Standards axis:** a magic `100` and `60000` inline -> *primitive obsession / mysterious value*; extract to named config. Duplicated key-building in two handlers -> *duplicated code*.
3. **Report, never merged:** `REVIEW: Spec 1 / Standards 2`.

The Spec-axis miss (IP fallback) is a hard miss -> route **back to Step 4**, add the fallback, re-review. The two Standards smells: establish green first (`npm test` passes), then extract the config constant and the shared key-builder on that green baseline, re-running the tests after. A refactor bigger than the fix would instead be filed as a follow-up, not done now.

**Then Step 5:** re-run the suite yourself (false-green defence - do not trust the review subagent's word that it is green), confirm the 101st-request test fails if you revert the limiter (negative check), and report outcome-first.

---

## How the gates chain (one line)

grill sharpens the ask -> evidence -> plan names seams + any design risk -> (prototype settles the risk) -> test-first builds it red->green -> two-axis review catches spec/standards misses -> verify by observation with the false-green defence -> report with the four owed lines.
