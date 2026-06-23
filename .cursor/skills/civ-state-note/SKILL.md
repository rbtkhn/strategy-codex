---
name: civ-state-note
description: Promote one bounded CIV-STATE-adjacent argument from chat, daily synthesis, wire-verify, or archive intake into a reusable statecraft/notes/ object — with mandatory retrieve framing and source discipline parallel to civ-state-essay, but without public essay prose bands. Use when the operator says civ-state note, civ-state-note, promote civ-state note, or when a mechanism seam needs civilizational shelf anchors before it belongs on public/civ-state/.
preferred_activation: civ-state note
activation: civ-state note
portable: true
version: 0.1.0
category: domain-pack
status: active
scope_class: repo-governed
tags:
- operator
- work-strategy
- civ-state
- statecraft
- notes
- promotion
portable_source: skills/civ-state-note/SKILL.md
synced_by: sync_portable_skills.py
---
# CIV-STATE Note

**WORK only; not Record.**

**Activation:** `civ-state note` · `civ-state-note` · `promote civ-state note` · **`CIV-STATE note`** (when class is clear)

Procedure skill for **bounded operator notes** under `statecraft/notes/` when the argument is **CIV-STATE-adjacent** — civilizational pattern, empire/state continuity, public-shelf retrieval gap, or wire+archive seam that benefits from **`public/civ-state/`** framing before (or instead of) reader-facing essay work.

**Parallel:** [`civ-state-essay`](../civ-state-essay/SKILL.md) owns **public book prose**; **this skill** owns **WORK notes** with the same **classify → retrieve → write → QA → ship** discipline at note scale.

**Sibling (general notes):** [`state-note`](../state-note/SKILL.md) — same shelf; use **`state-note`** when no CIV-STATE retrieve pass is load-bearing. Use **`civ-state-note`** when civilizational shelf anchors or wire-bridge framing are **required**, not optional.

## Use this skill when

- promoting **one bounded mechanism** that needs **`public/civ-state/`** retrieve context (Rome civic-chain rhyme, empire pattern, theory/sources door)
- downstream of **`civ-state`** **B. Retrieve** or wire-bridge when the deliverable is a **note**, not an essay
- wire-verify or daily synthesis produced a **tierable seam** that should survive outside chat with archive + optional public shelf pointers
- comparison or citation-split work is **method-bearing** and **CIV-STATE-flavored** (legitimacy, settlement, command, civilizational carry)

## Do not use this skill when

- the job is **reader-facing essay prose** under `public/civ-state/` — use **`civ-state-essay`**
- the job is upstream **Frame / Retrieve / Promote / Review** only — use **`civ-state`**
- the object is the **whole archive day** — use **`state-synthesis`**, then promote one wedge here
- the object is **general statecraft** with **no** civilizational retrieve need — use **`state-note`**
- the object is a **stand-alone transportable thesis** — route via [`docs/prose-index.md`](../../docs/prose-index.md) toward repo-root **`essays/`**

## Prose-class router (classify first)

| Class | Target surface | Skill |
|-------|----------------|-------|
| **CIV-STATE note** (this skill) | `statecraft/notes/` | **`civ-state-note`** |
| **General statecraft note** | `statecraft/notes/` | **`state-note`** |
| **Statecraft essay** | `statecraft/` or repo-root per prose-index | **`statecraft-intelligence-essay`** / prose-index |
| **CIV-STATE essay** | `public/civ-state/volumes/{vol}/essays/` etc. | **`civ-state-essay`** |
| **Repo-root essay** | `essays/` | prose-index + essay skills |

**Local test (note vs essay):** If removing surrounding machine context **breaks** the piece → usually still a **note**. If the thesis should travel **without** parent day/month context → **essay**, not this skill.

## Note-type router (parallel to essay-class)

Pick **one** primary type before writing:

| Note type | Typical object | Required blocks |
|-----------|----------------|-----------------|
| **Mechanism** | One causal seam | Core claim · falsifiers |
| **Comparison** | Speaker-function or lens split | Shared object · **X owns here** per carrier |
| **Route** | Where to cite next | Source anchors · return paths |
| **Wire-audit** | Tier table for same-week hooks | Verdict table · CIV-STATE lane sweep summary |
| **CIV-STATE-bridge** | Live event ↔ public shelf rhyme | Retrieve posture · `public/civ-state/` pointers (no prose paste) |
| **Citation-split** | Same-day guest-pair tension | Citation hygiene · Best use |

If type is unsettled → **`civ-state` B. Retrieve** (bounded) before drafting.

## Mandatory CIV-STATE pre-pass

Before writing the note body (skip only when operator says **`skip retrieve`**):

1. **Name retrieve posture:** `shelf-reader` · `primary-sources` · `secondary-sources` · `chapter surface` (same vocabulary as **`civ-state`**).
2. **Open ≤2 public surfaces** — volume essays README, connectivity, theory/sources door, or named civic-chain slug — **bounded Read**; no repo-wide grep.
3. **Record in note header block:** `Retrieve posture:` · `Public anchors:` (paths only).
4. **Wire-bridge when live wire:** if same-week seam, run **`wire-verify`** sub-hook or cite existing daily matrix row **before** promoting claims to Supported.

Do **not** paste public essay body into the note. Do **not** duplicate civic-chain prose from `public/civ-state/`.

## Note shape (bounded)

First line: `WORK only; not Record.`

Strong **`civ-state-note`** objects usually include:

- **Purpose**
- **Core claim** or **Shared object**
- **Retrieve posture** + **Public anchors** (CIV-STATE pre-pass)
- **Why this matters** / **Best use**
- per-carrier **`X owns here`** (comparisons)
- **Source anchors** — exact `source-archive/statecraft/` paths; parent daily when promoted downstream
- **Falsifiers** / wire verdict table when tierable
- **Next use** — return to parent daily, **`civ-state-essay`** upgrade path, or **`civ-state` D. Review**

**Filename:** kebab-case, date or topic slug — e.g. `june-2026-vance-lightning-rod-rubio-optionality-note.md`.

**Geo-strategic habit (optional one paragraph):** when place or institution is load-bearing, state **constraint or incentive** — not map trivia (borrowed habit from **`civ-state-essay`**; **no** word/quote bands).

## Source discipline

| Layer | Rule |
|-------|------|
| **Archive** | Verbatim SSOT in `source-archive/` — cite paths; **no** full transcript in note |
| **Wire** | Tier-3 hooks only in falsifier blocks; tier-4 analyst voice labeled **interpretation** |
| **Public CIV-STATE** | **Pointers only** — registry slug, essay filename, theory door; not mirrored prose |
| **Quotes in note** | Short load-bearing excerpts only; preserve verbatim spelling inside quotes |

**Explicit NOT borrowed from `civ-state-essay`:** civic-chain word/quote bands, humanizing/light pass, Gibbon-in-body rules (N/A at note scale), hex-frame tables, `check_civ_state_essay_prose.py`.

## Execution order (Windows-safe)

1. **Classify** — prose-class router + note-type router.
2. **Pre-pass** — CIV-STATE retrieve (+ wire-verify when live seam).
3. **Pick exactly one** promotable object — narrow if operator brought a whole day.
4. **One note file per turn** — no parallel StrReplace/Write on multiple note paths.
5. **Write** note → **wire README** (`statecraft/notes/README.md`) in same ship when operator says **EXECUTE** / **ship**.
6. **Parent link** — if promoted from daily/multi-lens, bidirectional return link when parent exists.
7. **One hang** → narrow to single Write; no parallel shell batch (RLJ parallel-ban).

## QA gates

### All note classes

- Still **one** bounded argument (not pseudo-essay)
- `docs/prose-index.md` local test passed (note-class)
- **Retrieve posture** + **Public anchors** present when CIV-STATE pre-pass was required
- Archive paths real (day README or named captures)
- **`statecraft/notes/README.md`** entry when shipping
- Kiev/Kharkov operator spelling in framing; preserve load-bearing verbatim in quotes

### Wire-audit / live-seam notes

- Verdict vocabulary aligns with **`wire-verify`** (supported · partial · contested · unclear · contradicted)
- CIV-STATE five-lane sweep cited or **`-absent`** receipt named

### Upgrade check (optional close)

Ask once when note dense enough: *Graduate to **`civ-state-essay`** on named public file?* — **do not** auto-promote.

## Ship

1. Commit **`statecraft/notes/<file>.md`** + README index line with explicit paths.
2. **Do not** write to `public/civ-state/` unless operator upgrades to **`civ-state-essay`**.
3. **Do not** mirror publish — notes are WORK shelf only.
4. After substantive **EXECUTE** ship, offer **`recursive learn`** (do not auto-append).

## Default output (after classify)

```markdown
**CIV-STATE Note**
- Prose class: CIV-STATE note (statecraft/notes/)
- Note type:
- Retrieve posture:
- Public anchors:
- Wire pre-pass (if any):
- Target file:
- Parent daily / synthesis (if any):

**Next:** [retrieve | draft note | wire-verify sub-hook | ship | handoff → civ-state-essay]
```

## Related operations

| Operation | When |
|-----------|------|
| **civ-state** | Frame unsettled; retrieve before note; **D. Review** when note exposes public edit target |
| **civ-state-essay** | Note graduates to reader-facing prose on `public/civ-state/` |
| **state-note** | Same shelf, no mandatory CIV-STATE pre-pass |
| **state-synthesis** | Upstream full day; promote one wedge here |
| **wire-verify** | Same-week wire hooks before Supported claims |
| **statecraft-multi-lens** | Comparison handoff when method-bearing |
| **recursive-learn** | Post-ship machine law |

Host-specific paths, examples, and maintenance: **CURSOR_APPENDIX** (sync target).

## Verification / proof standard

**Pass when:**

1. Prose class and note type stated (or handoff named).
2. CIV-STATE pre-pass recorded when required; public anchors are paths, not pasted prose.
3. One argument; README wired on ship; parent links when applicable.
4. No civic-chain word bands or public-tree edits without **`civ-state-essay`**.

**Fail when:** note bloats into essay; public essay prose pasted; parallel multi-file note edits on Windows EXECUTE; mirror publish invoked for notes shelf.


## Cursor / strategy-codex instance

Cursor-only wiring for [civ-state-note/SKILL.md](../../../skills/civ-state-note/SKILL.md). Portable SSOT body stays in `skills/`.

## Instance paths (note + CIV-STATE SSOT)

| Topic | Path |
|-------|------|
| Notes shelf README | [statecraft/notes/README.md](../../../statecraft/notes/README.md) |
| Prose-class chooser | [docs/prose-index.md](../../../docs/prose-index.md) |
| Public book root | [public/civ-state/README.md](../../../public/civ-state/README.md) |
| Rome essays README | [public/civ-state/volumes/rome/essays/README.md](../../../public/civ-state/volumes/rome/essays/README.md) |
| Rome connectivity | [public/civ-state/volumes/rome/theory/connectivity-rome.md](../../../public/civ-state/volumes/rome/theory/connectivity-rome.md) |
| Reader guide (geo-strategic habit pointer) | [public/civ-state/docs/reader-guide.md](../../../public/civ-state/docs/reader-guide.md) |
| Archive day index | `source-archive/statecraft/<YYYY-MM-DD>/README.md` |
| Wire-verify registry | [docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md) |

## Examples (shelf-native patterns)

| Pattern | Example |
|---------|---------|
| Guest-pair citation split | [june-18-2026-mou-guest-pair-citation-split.md](../../../statecraft/notes/june-18-2026-mou-guest-pair-citation-split.md) |
| Speaker-function comparison | [barnes-johnson-aguilar-kent-on-section-224.md](../../../statecraft/notes/barnes-johnson-aguilar-kent-on-section-224.md) |
| Mechanism | [formal-sovereignty-vs-internal-carriage.md](../../../statecraft/notes/formal-sovereignty-vs-internal-carriage.md) |

## QA — note promotion (no essay prose script)

**Primary gates (manual / checklist):**

1. One argument — not whole-day dump
2. `Retrieve posture` + `Public anchors` when CIV-STATE pre-pass required
3. Archive paths from day README or named captures
4. Wire verdicts use **`wire-verify`** vocabulary when tierable
5. README index line on ship

**Optional wire pass before ship:**

```powershell
python scripts/validate_skills.py
```

**Do not run** `check_civ_state_essay_prose.py` on `statecraft/notes/` — wrong class.

## Validate public tree (only when note triggers public gap)

When the note's **Next use** names a **`public/civ-state/`** edit target, hand off to **`civ-state-essay`** or **`civ-state` D. Review** — do not patch public tree from note promotion alone.

```powershell
python scripts/validate_civilizational_statecraft_public.py public/civ-state
```

## Related skills (instance)

| Skill | When |
|-------|------|
| [civ-state](../civ-state/SKILL.md) | Retrieve / frame before note |
| [civ-state-essay](../civ-state-essay/SKILL.md) | Graduate note to public essay |
| [state-note](../state-note/SKILL.md) | General note without CIV-STATE pre-pass |
| [wire-verify](../wire-verify/SKILL.md) | Same-week wire hooks |
| [state-synthesis](../state-synthesis/SKILL.md) | Upstream daily batch |
| [validator-first](../validator-first/SKILL.md) | Menu pick = run validate same turn |

## Maintenance

```powershell
python scripts/sync_portable_skills.py --skill civ-state-note
python scripts/sync_portable_skills.py --verify --skill civ-state-note
python scripts/validate_skills.py
```

Hand-edit **only** `skills/civ-state-note/SKILL.md`; run sync before commit.
