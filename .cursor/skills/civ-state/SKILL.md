---
name: civ-state
preferred_activation: civ-state
description: Open CIV-STATE as the upstream analysis bench for frame judgment, retrieval, membrane promotion, and review. Use when the operator says civ-state, statecraft civ-state, or needs a fixed A-D CIV-STATE menu with a live recommendation rather than explicit book-writing.
portable: true
version: 0.2.0
tags:
- operator
- statecraft
- civ-state
- architecture
portable_source: skills-portable/civ-state/SKILL.md
synced_by: sync_portable_skills.py
---
# CIV-STATE

**WORK only; not Record.**

**Activation:** `civ-state` · `statecraft civ-state` *(legacy alias)*

`civ-state` is the exact command door for CIV-STATE as an analysis-and-retrieval bench.

It is not a generic bookshelf opener, not a coffee replacement, not a lane-drafting surface, and not default book-authoring mode.

Short doctrine:

- `civ-state` opens upstream judgment
- the menu stays fixed
- only the recommendation moves
- retrieval should follow the CIV-STATE switchboard, not jump straight into broad chapter prose

## Public corpus influence (one-way)

\\	ext
public/civ-state/  ──influences──▶  civ-state skill
public/civ-state/  ◀──never contains──  operator skill body
\
- **Canonical retrieval SSOT** is the staged public book tree (host appendix paths).
- Operator substrates inform **when** to open public surfaces — not **what** they say.
- Publish only when operator says **ship**, **publish**, or **VERSION** — not on every Retrieve or Review close.

## Operator workflow modes

| Mode | Signals | Recommendation bias |
|------|---------|---------------------|
| **Pre-lane** | Before lane ownership | **A** if term unsettled; **B** if term clear, shelf not |
| **Live wire** | Verified event, crisis object | Wire-bridge → **A** or **B** |
| **Book maint** | Rome hex, theory/sources gaps | **D** if review-queue residue; else **B** |
| **Post-synthesis** | After state-synthesis | **D** or **B**; public edit target |

De-weight **C. Promote** unless operator names membrane explicitly.

## Wire-bridge (contextual sequence)

When entry is **live wire**, use object-shape router (no parallel reads):

| Object shape | Sequence bias |
|--------------|---------------|
| **carrier-obvious** | Case → term → primary shelf |
| **mechanism-abstract** | Term → case scan → shelf |
| **comparative-unsettled** | Cross-case + one term winner → narrow |
| **evidence-trouble** | Primary → secondary → widen |

**Rome vs live wire:** one recommendation + runner-up — no fixed priority. **Archive thin:** hand back to state synthesis (appendix).

## Boundary

- Use this command when the real question is upstream CIV-STATE orientation, not downstream statecraft drafting.
- Keep explicit CIV-STATE book work out of the default path unless the operator asks for it directly.
- Do not replace deploy routing, lane skills, framework diagnosis, or explicit volume-authoring skills.
- Do not widen into a dynamic repo dashboard or unrelated worktree audit.
- On cold threads: one bounded skill read first; no parallel shell (host appendix).

## What This Command Owns

`civ-state` owns four action families:

- `Frame`
- `Retrieve`
- `Promote`
- `Review`

These are stable. The operator should learn that the CIV-STATE command always opens the same four doors.

What changes from turn to turn is the live recommendation and the explanation for why that recommendation is the most productive next move now.

## Allowed Dynamic Inputs

**Public corpus first:** theory, skills, sources, volumes, essays, docs under the staged public book tree.

**Operator substrates second:** speaker/bridge state, PH-CIV membrane docs, promotion ledger, review queue.

Do not use:

- coffee cadence or dream cadence
- broad worktree dirt
- unrelated lane activity
- generic repo heat outside speaker-state and CIV-STATE membrane/review residue

*(Instance paths: host appendix.)*

## Recommendation Rules

Recommend exactly one path:

- recommend `A. Frame` when the live pressure is `what governing term or rhythm/time placement actually carries this object?`
- recommend `B. Retrieve` when the live pressure is `which CIV-STATE surface should I open now?`
- recommend `C. Promote` when the live pressure is `should this speaker-state or PH-CIV pattern cross the membrane into CIV-STATE?`
- recommend `D. Review` when the live pressure is `what CIV-STATE residue is ready for tightening, correction, or hardening?`

If more than one path is plausible, still choose one recommendation and name the runner-up briefly in the menu wording if helpful.

Also:

1. Detect entry mode (pre-lane, live wire, book maint, post-synthesis).
2. If wire-shaped → object-shape router → map to A or B.
3. **B. Retrieve** must name Retrieval posture + **public path** (host-relative).
4. **Rome vs live wire:** when both plausible, one pick + runner-up — no fixed priority.

## Action Families

### A. Frame

Use when the object is still interpretively unstable.

Route toward public theory + reader entry cards first; operator framework/checklist only if blocked (appendix).

This is for governing-term diagnosis and CIV-STATE interpretive orientation, not volume writing.

### B. Retrieve

Use when the object is stable enough that the next honest move is opening the right CIV-STATE surface.

Possible retrieval targets include public shelf-reader, era primary/secondary-sources, volumes, civilization/empire/statecraft case files, sacred grammar, and chapter-family surfaces. De-prioritize operator-only retrieval matrix unless public shelf exhausted (appendix).

This is retrieval-first, not book-authoring.

Use the switchboard law explicitly:

- stay in `primary-sources` when the civilization's own wording is the live issue
- open `secondary-sources` only when the primary shelf exposes a real interpretive difficulty
- return to `primary-sources` once the clarification has been taken
- move upward into `civilization`, `empire`, or `statecraft` only when the source problem has been resolved

### C. Promote

Use when a speaker-state or PH-CIV pattern may deserve promotion into CIV-STATE.

Route toward the PH-CIV to CIV-STATE bridge, promotion ledger, and promoter workflow.

This is membrane judgment, not silent upstream mutation. Escalated destinations must be expressible under the public book tree.

### D. Review

Use when CIV-STATE already contains residue that is ready for bounded tightening.

Route toward the review queue and a named public edit target; architecture/part-writing skills only when operator explicitly wants book work. Never mirror operator queue prose into the public book.

Default review means refinement, correction, or hardening. It does not assume the operator wants to keep authoring the CIV-STATE books.

## Book-Authoring Escape Hatch

Book-building is not part of the default four-family interpretation.

If the operator explicitly asks to work on the CIV-STATE book, route out of this command into the relevant authoring surfaces (volume architect, civilization/empire part writers, guidebook writer).

Do not hide that shift inside `Retrieve` or `Review`.

## Default Output

When the operator invokes `civ-state` without a narrower object, use exactly this output shape:

```markdown
**Statecraft CIV-STATE**
- Live recommendation:
- Why this path now:
- Current signals used:
- Retrieval posture:
- Public retrieval anchor:
- Object shape: *(wire-shaped or cross-case unsettled)*
- Sequence chosen: *(when wire-bridge ran)*

**CIV-STATE Menu - reply A-D**
A. Frame
B. Retrieve
C. Promote
D. Review
```

The menu labels stay fixed across runs.

The `Current signals used` line should name only the relevant speaker / bridge / membrane / review surfaces actually informing the recommendation.
The `Retrieval posture` line should appear when `B. Retrieve` is the live recommendation and should name the narrowest honest next move:

- `shelf-reader`
- `primary-sources`
- `secondary-sources`
- `chapter surface`

## Handoff Rule

When the operator replies with a letter after this command, execute that path rather than reprinting the menu.

- `A` = frame diagnosis
- `B` = CIV-STATE retrieval
- `C` = membrane promotion test
- `D` = residue review / hardening orientation

## Close offers (not auto-run)

Offer **one line** only when structural change actually shipped:

| After | Offer |
|-------|-------|
| Book encode / review-queue fix / wire-bridge law | *Machine law implicit — say `recursive learn` for session review.* |
| One bounded mechanism seam ready | *One mechanism seam ready — say `state-note` to promote with archive anchors.* |

Do not offer publish unless operator said **ship**, **publish**, or **VERSION**.

## Related operations

| Operation | Relationship |
|-----------|--------------|
| **state-synthesis** | Archive batch upstream; hand off **to** civ-state when civilizational layer unsettled; civ-state hands **back** when archive thin |
| **state-note** | Downstream when one mechanism seam ready; may return when public retrieval gap |
| **recursive-learn** | Post-encode machine law; close offer only |
| **statecraft-framework** | Secondary frame supplement when public theory insufficient |

## Non-Replacement Rule

`civ-state` does not replace deploy routing, lane skills, daily synthesis, transaction drafting, or explicit volume-authoring.

It is the upstream CIV-STATE command surface: frame, retrieve, promote, review — through the public book corpus first.


## Cursor / grace-mar instance

Cursor-only wiring for [civ-state/SKILL.md](../../../skills-portable/civ-state/SKILL.md). Portable SSOT body stays in `skills-portable/`.

## Cursor entry (cold thread)

On a **new thread** with no prior warmup in chat:

- `Read` the assembled skill with `limit≤80` first (first slice only)
- deliver the CIV-STATE menu in chat
- do **not** batch `harness_warmup` or other shell with the skill read
- after any tool hang: one smaller read per turn; operator `fast tools` / `read only` → strict Read/Write, zero Shell

## Public routing table

| Civ | Doorway | Era spine | Notes |
|-----|---------|-----------|-------|
| China | [volumes/china/README.md](../../../public/civ-state/volumes/china/README.md) | ancient → cybernetic | sovereignty-chain order |
| Persia | [volumes/persia/README.md](../../../public/civ-state/volumes/persia/README.md) | ancient → cybernetic | recognition / sacred grammar |
| Rome | [volumes/rome/README.md](../../../public/civ-state/volumes/rome/README.md) | ancient → cybernetic | hexagonal pilot — [essays/](../../../public/civ-state/volumes/rome/essays/README.md) |
| Russia | [volumes/russia/README.md](../../../public/civ-state/volumes/russia/README.md) | medieval → cybernetic | |
| America | [volumes/america/README.md](../../../public/civ-state/volumes/america/README.md) | medieval → cybernetic | |

Whole-work: [theory/README.md](../../../public/civ-state/theory/README.md) · [sources/source-lattice.md](../../../public/civ-state/sources/source-lattice.md) · [volumes/README.md](../../../public/civ-state/volumes/README.md) · [docs/era-spine.md](../../../public/civ-state/docs/era-spine.md)

**Rome hexagonal (book maint):** [connectivity-rome.md](../../../public/civ-state/volumes/rome/essays/connectivity-rome.md) · RLJ Rome parallel-spine ladder in [recursive-learn](../recursive-learn/SKILL.md) — link, do not duplicate table.

## P0 public skill cards → operator letters

| Public card | Default letter |
|-------------|----------------|
| [governing-term-first.md](../../../public/civ-state/skills/governing-term-first.md) | **A. Frame** |
| [civilization-first-entry.md](../../../public/civ-state/skills/civilization-first-entry.md) | **A. Frame** (case-first) |
| [source-lattice-read.md](../../../public/civ-state/skills/source-lattice-read.md) | **B. Retrieve** |

## Letter handoff recipes (bounded reads)

| Pick | Read first (limits) |
|------|---------------------|
| **A** | `public/civ-state/theory/README.md` limit 60 → `skills/governing-term-first.md` limit 40 |
| **B** | `sources/source-lattice.md` limit 50 **or** `volumes/{civ}/shelf-reader.md` limit 50 |
| **D** | [review-queue.md](../../../statecraft/states/review-queue.md) tail + one named public edit target |

## Archive-missing guard (state-synthesis handback)

When wire-bridge needs archive but `source-archive/statecraft/<day>/` batch is thin:

```text
Archive batch not ready — run state synthesis after intake, not civ-state frame loop.
```

Hand off to [state-synthesis](../state-synthesis/SKILL.md).

## Allowed dynamic inputs (instance paths)

**Public first:**

1. [public/civ-state/theory/](../../../public/civ-state/theory/)
2. [public/civ-state/skills/](../../../public/civ-state/skills/)
3. [public/civ-state/sources/](../../../public/civ-state/sources/)
4. [public/civ-state/volumes/](../../../public/civ-state/volumes/)
5. [public/civ-state/essays/](../../../public/civ-state/essays/)

**Operator second:**

6. [statecraft/voices/](../../../statecraft/voices/)
7. [statecraft/bridges/](../../../statecraft/bridges/)
8. [ph-civ-to-civ-state-bridge.md](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
9. [ph-civ-promotion-ledger.md](../../../statecraft/states/ph-civ-promotion-ledger.md)
10. [review-queue.md](../../../statecraft/states/review-queue.md)

## Action-family routes (instance)

| Family | Route toward |
|--------|----------------|
| **A. Frame** | [statecraft-framework](../statecraft-framework/SKILL.md) · public theory/skills · [six-term checklist](../../../statecraft/states/civilization-empire-faith-science-memory-entropy-retrieval-checklist.md) |
| **B. Retrieve** | public shelf-reader · primary/secondary-sources · volumes · sacred grammar · de-prioritize [source-retrieval matrix](../../../statecraft/states/indexes/source-retrieval-matrix.md) unless public exhausted |
| **C. Promote** | bridge · ledger · [ph-civ-to-civ-state-promoter](../ph-civ-to-civ-state-promoter/SKILL.md) |
| **D. Review** | review-queue · public edit target · [civ-state-volume-harden](../civ-state-volume-harden/SKILL.md) only if explicit book work |

## Publish reminder

Review resolutions **commit** to `public/civ-state/`. Mention `publish_public_civ_state.py` only when operator says **ship**, **publish**, or **VERSION** — not on every close.

## Book-authoring escape hatch

- [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md)
- [civilization-part-writer](../civilization-part-writer/SKILL.md)
- [empire-part-writer](../empire-part-writer/SKILL.md)
- [statecraft-guidebook-writer](../statecraft-guidebook-writer/SKILL.md)

## Doctrine cross-links

- [statecraft/README.md](../../../statecraft/README.md) — **`civ-state` skill retrieves through `public/civ-state/`**
- [statecraft/states/README.md](../../../statecraft/states/README.md) — command door

## Maintenance

```powershell
python3 scripts/sync_portable_skills.py --skill civ-state
python3 scripts/sync_portable_skills.py --verify --skill civ-state
python3 scripts/validate_skills.py
python3 scripts/validate_civ_state_skill_links.py
```
