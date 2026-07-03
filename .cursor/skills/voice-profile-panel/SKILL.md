---
name: voice-profile-panel
description: 'QA voice profiles through solo smoke lines and sequential fictional roundtables: read Tier A statecraft/voices profiles, enforce orthogonality via Family 8 tables, run spot-checks, and apply anti-AI panel checklist. Triggers: voice profile panel, voice panel, profile smoke test, triad roundtable demo. Not tri-mind; not Record merge.'
preferred_activation: voice profile panel
activation: voice profile panel
portable: true
version: 0.1.0
category: product-narrative
status: active
scope_class: repo-governed
tags:
- statecraft
- voices
- qa
- emulation
portable_source: skills/voice-profile-panel/SKILL.md
synced_by: sync_portable_skills.py
---
# Voice profile panel

**Preferred activation:** **`voice profile panel`**, **`voice panel`**, **`profile smoke test`**, or **`triad roundtable demo`** on a named live object.

**Scope:** WORK-only **voice QA** — test whether Tier A profiles support authentic generation and **orthogonal** multi-voice panels. Default **Think** (chat). **Ship** only when operator names an explicit path (e.g. `runtime/artifacts/voice-qa/…`); no default repo scratch directory.

**Not in scope:**

- **`tri-mind` / tri-frame choreography** — deprecated; use **`state-synthesis`** comparison subroutine or a **named single speaker** for analytic comparison (`statecraft-multi-lens` archived), not A/B/C menu revival.
- **Record merge** or wire-grade fact promotion.
- **Substituting mind-file précis** for profile-grounded speech — read profiles + host **minds-authentic-voice** rule when a mapped mind is named.

## SSOT surfaces

| Surface | Role |
|---------|------|
| `statecraft/voices/<speaker>/<speaker>-profile.md` | Per-speaker Tier A/B contract; B×M×Me orthogonality in Family 8 when triad |
| `statecraft/voices/voice-profile-template.md` | Shape + Family 1–8 law |
| Archive captures linked from profiles | Quote bank for spot-checks |

**Tier gate:** Panel demos default to **Tier A** profiles only (compact table `A` + filled Family 8). Tier B → solo stub smoke or promote profile first.

## Modes

| Mode | When | Output |
|------|------|--------|
| **Solo smoke** | One profile after intake or promotion | 3–5 in-voice lines on a named object + Family 8 mini table |
| **Sequential panel** | 2–3 mapped voices on same object | Rounds × speakers; **chain law** below |
| **Audit pass** | After panel or pasted simulation | Orthogonality table + **§8 anti-AI scorecard** |

Operator may combine: e.g. **panel then audit**.

## Sequential panel law

1. **Fixed turn order within a round** — e.g. Mercouris → Barnes → Mearsheimer; do not reorder mid-demo unless operator requests.
2. **Chain law:** Each speaker responds to the **immediately prior turn** in the room, not a neutral summary of all prior speakers.
3. **Orthogonality fence:** Each turn must stay on that platform/profile's **primary unit** (person / theater / state per triad §4). Flag collapse in audit if two speakers share the same opening move and payoff.
4. **Host frame (optional):** Fictional Duran-style host may set object once; host is not a fourth analytic voice unless operator names a host profile.
5. **Fact fence:** Live-object claims stay **tier-D in speech** unless wire-verified; panel tests **register**, not news truth.

## Solo smoke procedure

1. Read target `*-profile.md` — at minimum **Voice fingerprint (compact)**, **Family 8**, failure modes.
2. Name one **bounded object** (date + 2–4 load-bearing clauses).
3. Emit **3–5 paragraphs** in authentic register (no "X would say…").
4. Append **Family 8 spot-check** (3–4 rows): sounds-like / not-like vs triad peers when applicable.

## Panel procedure (default 3 × 3)

1. **Frame:** Object + host one-liner + round question.
2. **Round 1:** Each voice answers the **same** opening question (sequential chain).
3. **Round 2–3:** Cross-talk on one fork (e.g. upfront funds, one-text rule, Lebanon gate).
4. **Close:** Family 8 scorecard + orthogonality pass/fail vs triad §5 collapse-risk rows.
5. **Optional audit:** Run §8 checklist; score ~1–5 pass-as-transcript; list reruns needed.

## Anti-AI panel checklist (§8)

Full checklist is in **Anti-AI panel checklist (§8)** below. Before claiming panel pass, scan generated text for:

| Tell | Fail if |
|------|---------|
| Mechanical openers | Every turn starts with "I hear you…" / "I don't dispute… but" |
| Grant-and-pivot symmetry | Each speaker concedes then pivots in identical grammar |
| Outline closes | Round 3 ends optimist / skeptic / escalation template |
| Third-person self | Barnes (or any voice) refers to self in third person |
| Paragraph symmetry | All speakers ~same length every turn |
| Equal courtesy | Uniform praise before disagreement |

**Rerun law:** Operator may request **single-round rerun** with §8 bans enforced; do not silently rewrite Round 1 when only R2/R3 failed audit.

## Contrast with related skills

| Skill | Role |
|-------|------|
| **state-synthesis** / **primary-overhearing-analysis** | Analytic comparison on one object — not fictional transcript (`statecraft-multi-lens` archived) |
| **minds-authentic-voice** | Register law when CIV-MIND / strategy-expert mind files ground output |
| **wire-verify / fact-check** | Claim truth — run **before** treating panel hooks as settled fact |

## Ship (explicit)

When operator names a file:

- Demo transcript + audit → operator-named path under `runtime/artifacts/voice-qa/` (e.g. `triad-roundtable-demo-<YYYY-MM-DD>.md`)
- Do not paste full panel into `days.md` or Record surfaces.

## Guardrails

- Do not revive **`tri-mind`** menus or **`ab+c`** litigator-close.
- Do not homogenize voices into one "analyst voice."
- Preserve **tension** — premature synthesis is a panel failure mode.
- Chat-only demos are valid; disk write is optional unless Ship named.

## Cursor / strategy-codex instance

Strategy-codex routing and SSOT paths for voice-profile-panel.

## Triggers

- **`voice profile panel`**, **`voice panel`**, **`profile smoke test`**, **`triad roundtable demo`**
- Default **Think** (chat); **Ship** only when operator names an explicit path (e.g. `runtime/artifacts/voice-qa/…`)

## SSOT (read before panel)

| Surface | Path |
|---------|------|
| Voice template | [statecraft/voices/voice-profile-template.md](../../../statecraft/voices/voice-profile-template.md) |
| Mercouris profile | [statecraft/voices/mercouris/mercouris-profile.md](../../../statecraft/voices/mercouris/mercouris-profile.md) |
| Barnes profile | [statecraft/voices/barnes/barnes-profile.md](../../../statecraft/voices/barnes/barnes-profile.md) |
| Mearsheimer profile | [statecraft/voices/mearsheimer/mearsheimer-profile.md](../../../statecraft/voices/mearsheimer/mearsheimer-profile.md) |
| Authentic voice rule | [.cursor/rules/minds-authentic-voice.mdc](../../rules/minds-authentic-voice.mdc) |
| TRI-MIND deprecated | [docs/archive/skill-work-legacy/work-strategy/TRI-MIND-DEPRECATED.md](../../../docs/archive/skill-work-legacy/work-strategy/TRI-MIND-DEPRECATED.md) |

## Related skills

| Skill | When |
|-------|------|
| [state-synthesis](../state-synthesis/SKILL.md) / [primary-overhearing-analysis](../primary-overhearing-analysis/SKILL.md) | Analytic comparison — not fictional roundtable (`statecraft-multi-lens` archived) |
| [wire-verify](../wire-verify/SKILL.md) | Grade MOU/wire hooks before treating panel claims as settled |

## Ship path (explicit)

- `runtime/artifacts/voice-qa/triad-roundtable-demo-<YYYY-MM-DD>.md` (or operator-named equivalent) when disk save is required

## Boundary

- non-authoritative; not Record merge
- Tier A profiles required for triad panel default
