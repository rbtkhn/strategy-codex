# check-streams performance rubric


Use this rubric when the operator wants to judge how well a `check streams`
run performed as a **daily watch-aperture action**, not just whether some files
eventually got written.

This rubric exists because a `check streams` pass can succeed in one layer and
fail in another:

- discovery can be honest even when YouTube blocks full verification
- recovery can close real gaps even when the main audit path degrades
- a run can materialize transcripts while still leaving weak receipts
- a run can produce good files but poor closeout discipline
- a run can discover the requested object early and still fail by continuing into unasked-for workflow

Score each dimension separately from `0` to `3`.

## Scoring dimensions

### 1. Discovery discipline

How well did the run discover the day's real watchlist state?

- `0` - wrong scope, wrong dates, or major channel omissions
- `1` - partial discovery with obvious gaps and no stable accounting
- `2` - correct watchlist/date scope with partial gaps handled honestly
- `3` - correct scope, stable roster, and known gaps explicitly bounded

This dimension rewards **epistemic honesty**, not just completeness.

### 2. Provenance discipline

How well did the run preserve the YouTube-first truth boundary?

- `0` - secondary listings or guesses were treated as if they were captures
- `1` - provenance is mixed, fuzzy, or overclaimed
- `2` - direct YouTube URLs were kept distinct from unresolved discoveries
- `3` - every claimed capture is YouTube-grounded and every unresolved item is clearly marked

This is the anti-hallucination layer for stream capture.

### 3. Recovery / materialization quality

How well did the run turn approved or operator-supplied items into canonical raw-input?

- `0` - failed writes, stub files, or materially wrong raw-input
- `1` - partial materialization, weak metadata, or unresolved body integrity
- `2` - usable canonical raw-input with sound metadata and transcript-bearing bodies
- `3` - clean canonical raw-input plus explicit verification of body integrity and provenance

Use this dimension whether the source was fetched mechanically or supplied by operator paste.

### 4. Receipt discipline

How well did the run leave behind evidence that a later operator can audit?

- `0` - no useful receipt trail
- `1` - some evidence exists, but the operator would struggle to reconstruct what happened
- `2` - partial receipt trail exists for discovery or materialization, but not both
- `3` - durable receipts exist for discovery outcome, recovery path, and final item status

This dimension matters most when the fetch path degrades or the run becomes manual.

### 5. Closeout discipline

How well did the run close the loop with the operator and the repo?

- `0` - unclear result, overclaiming, or repo state confusion
- `1` - result is usable but scope, git state, or remaining gaps are fuzzy
- `2` - result is clearly stated and remaining gaps are named
- `3` - result is clearly stated, remaining gaps are named, and git/materialization scope is cleanly bounded

For bounded retrieval asks, this dimension also includes the **stopping rule**:

- once the requested object is in hand, answer first
- do not continue into repair, capture, dependency, or routing work unless the operator asks for the next layer

A run that finds the requested URLs quickly but keeps expanding into unasked-for workflow should score poorly here even if the deeper work is technically competent.

This is the difference between "some work happened" and "the pass is governable."

## Reading the result

Do not compress the scores into a single mood too early.

Read the profile:

- strong **discovery discipline** + weak **recovery quality** = the daily aperture saw correctly, but the write path failed
- strong **recovery quality** + weak **receipt discipline** = good files were created, but the next operator inherits fog
- strong **provenance discipline** + weak **closeout discipline** = the run stayed honest, but the summary obscured what remains open
- strong **closeout discipline** + weak **discovery discipline** = the report sounds neat, but the underlying roster may still be wrong

## Quick labels

Use these shorthand labels when helpful:

- **honest partial** = discovery discipline `2+` and provenance discipline `2+`, even if recovery is weak
- **good recovery** = recovery / materialization quality `2+`
- **auditable recovery** = receipt discipline `2+`
- **governable pass** = closeout discipline `2+`
- **fully strong run** = all five dimensions `2+`, with no `0`

## Operator standard

For this repo, the minimum acceptable `check streams` pass is usually:

- discovery discipline `2`
- provenance discipline `3`
- recovery / materialization quality `2`
- receipt discipline `2`
- closeout discipline `2`

That profile means:

- the aperture stayed honest
- transcript claims stayed bounded by real YouTube provenance or explicit operator-paste recovery
- canonical raw-input became usable
- later audits can reconstruct what happened
- the operator knows what is still unresolved

## Current lesson

The March 19-20, 2026 stream check is the model case for why this split matters:

- discovery discipline was mixed because YouTube anti-bot behavior degraded the audit path
- provenance discipline stayed strong because unresolved items were not mislabeled as captured
- recovery quality became strong once full operator-paste transcripts were supplied
- receipt discipline lagged because the recovery was more manual than ideal
- closeout discipline was strong because commits were kept narrow and gaps were named accurately

That was a **useful and honest recovery pass** before it was a **fully instrumented pass**.
