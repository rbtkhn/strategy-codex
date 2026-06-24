---
name: speaker-shelf-maintenance
description: Compose speaker shelf hygiene, structural continuity, and relations-membrane passes for strategy-codex speaker shelves.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - check-sources
outputs:
  - bounded shelf audit memo with verdict and next fixes
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# Speaker Shelf Maintenance

## Purpose

Run repeatable **strategy-codex speaker shelf** maintenance: shape audits, cross-surface continuity checks, and cross-speaker relation membrane repairs — without treating legacy skill stubs as separate entrypoints.

## Trigger

**Operator phrases:** `runbook speaker shelf`, `runbook speaker maintenance`, `runbook speaker membrane`.

**Legacy triggers:** `speaker shelf`, `speaker membrane`, structural-continuity requests on a named speaker — route here.

**Use when:**

- auditing person arcs, routing stacks, month support, or citation hygiene
- checking whether canonical speaker surfaces still agree (route stack, month ladder, maturity labels)
- deciding whether a note belongs in one speaker shelf vs `codex/speakers/relations/`

**Do not use when:**

- live YouTube discovery or missing-episode recovery — use **`check-sources`** (legacy `check-streams` redirects there)
- transcript cleanup — use **`source-clean`** / transcript chain
- generic statecraft daily synthesis — use **`state-synthesis`**

## Skills Composed

| Mode | Focus | When |
|------|-------|------|
| **Hygiene** | Shelf shape, month maturity, repair ranking, placeholder leakage | "audit the arc", "thinnest months", "align shelves" |
| **Continuity** | Agreement across README, arc, atlas, month shelves | "surfaces disagree", "drift after month work" |
| **Membrane** | Continuity vs neutral `relations/` ownership | "A vs B", comparison living in wrong shelf |
| **Full** | Hygiene → continuity → membrane (if scope needs all three) | Major shelf migration or post-repair closeout |

Legacy skills **`speaker-shelf-hygiene`**, **`speaker-structural-continuity`**, and **`speaker-relations-membrane`** redirect to this runbook — do not invoke their bodies.

## Inputs Required

- Speaker name(s) and shelf path (`statecraft/voices/<speaker>/` and/or `codex/speakers/<speaker>/`)
- Mode: `hygiene` | `continuity` | `membrane` | `full` (default from operator phrase)
- Optional month range or comparison peer (Freeman / Parsi / Ritter, etc.)

## Canonical references (read before editing)

- [`codex/speakers/README.md`](../../codex/speakers/README.md)
- [`codex/speakers/map/open-first-routes.md`](../../codex/speakers/map/open-first-routes.md)
- [`codex/speakers/_templates/speaker-surface-orthogonality-review-template.md`](../../codex/speakers/_templates/speaker-surface-orthogonality-review-template.md)
- [`codex/speakers/relations/README.md`](../../codex/speakers/relations/README.md)

Short route rule: `front door -> support spine -> provenance bench -> compatibility last`.

## Workflow Steps

### A. Hygiene mode

1. **Map the live route stack** — wrappers, person arc, routing, raw-input bench, helix, support spine, month surfaces, compatibility residue.
2. **Classify surfaces by job** — first-open, support spine, provenance bench, comparison, compatibility-only.
3. **Audit month support** — mature retrieval vs continuity carryover; label `host-led`, `speaker-synthesis-led`, `speaker-chronology-led`, or `reinforcement-only`.
4. **Rank thin captures** (when relevant) — month status first, then repair priority using body deficit, month dependence, sequence damage, motif load, tone-preservation, shelf leverage (0–3 each).
5. **Audit source boundaries** — raw-input vs page/refined vs thread/transcript roles; statecraft-side vs codex-side authority.
6. **Audit placeholder leakage** — no unresolved `TBD` canon on primary surfaces.
7. **Repair in order** — page/manifest/raw-input truth → routing → month gaps → compatibility demotion → optional polish.

### B. Continuity mode

1. **Identify shelf class** — normalized month-ladder, cross-context exception, or host-led mature-month exception.
2. **Check outer grammar** (when statecraft-side canonical) — README, index, arc, routing, bench, helix, support spine, stream README, bounded monthly ladder, audit, themes, codex compatibility last.
3. **Run continuity tests** — front-door, route-stack, segment, status, month-ownership, thread, boundary, migration, inner-shape continuity.
4. **Verdict** — `structurally continuous` | `mostly continuous with minor seams` | `material drift present`.
5. **Smallest fix** — prefer canonical statecraft wording before widening codex residue; do not duplicate month summaries into atlas.

### C. Membrane mode

1. **Classify object** — continuity, relation, host-local arc, or helix.
2. **Ownership test** — main question `what does speaker A own?` vs `how do A and B differ?`
3. **Find footprint** — links across speaker READMEs, indexes, orthogonality reviews.
4. **Move or create** neutral note under `codex/speakers/relations/` when cross-speaker comparison is load-bearing.
5. **Rewire shelves** — both speaker READMEs, review notes, indexes; do not stop at file move alone.
6. **Verify** — no stale shelf-local paths; relations/ does not absorb arcs or helixes.

### D. Full mode closeout

After hygiene and continuity (and membrane if needed), verify entry questions resolve without rereading legacy `thread.md`:

- who is this speaker?
- where to open first?
- which months are mature and under what ownership?
- which surfaces are support vs provenance vs compatibility?

## Human Approval Points

- Before moving files into `relations/` or demoting codex compatibility fronts
- Before treating a month as chronology-owning on the speaker side

## Stop Conditions

Stop if:

- speaker canonical path is ambiguous (statecraft vs codex dual authority) — name the conflict before edits
- operator scope is discovery-only — hand off to **`check-sources`**

## Verification / Proof Standard

Do not call this runbook complete unless:

- speaker name and shelf path(s) are named
- mode (`hygiene` | `continuity` | `membrane` | `full`) is stated
- verdict or audit summary is produced (continuity verdict or hygiene success condition)
- files touched or recommended fixes are listed
- compatibility vs canonical surfaces are explicitly distinguished
- any unresolved `TBD` or VERIFY items are named

Evidence to report:

- speaker folder paths read
- month-status / ownership labels applied
- relation moves and rewired README paths (membrane mode)
- comparison verdict when multiple speakers audited

If verification cannot be completed:

- state which canonical path was not opened
- stop before broad shelf rewrite

## Outputs

- Bounded audit memo with verdict, agreements/divergences, and smallest next fix
- Optional comparison table when multiple shelves audited

## Return Paths

- [skills/runbooks/README.md](README.md)
- [docs/skill-work/work-strategy/README.md](../../docs/skill-work/work-strategy/README.md)
- [`check-sources`](../../skills/check-sources/SKILL.md) — live source discovery
