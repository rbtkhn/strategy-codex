WORK only; not Record.

# Civ-lens speaker profile template

Purpose: single **shape contract** for `statecraft/civ-lens/<speaker>/<speaker>-profile.md` after migration. Placement law lives in [README.md § Speaker profile law](README.md#speaker-profile-law). Upstream minimal scaffold: [strategy-codex-template-profile.md](../../../codex/strategy-codex-template-profile.md).

**Exemplars:**

- **Full:** [barnes/barnes-profile.md](barnes/barnes-profile.md)
- **Seed:** [weichert/weichert-profile.md](weichert/weichert-profile.md) · [pape/pape-profile.md](pape/pape-profile.md)

**Host profiles** (`statecraft/hosts/<host>/<host>-profile.md`) reuse the same spine; swap shelf pointers and role framing for host-law / guest-transformation jobs. Exemplar: [../hosts/davis/davis-profile.md](../hosts/davis/davis-profile.md).

---

## What a profile is (and is not)

A civ-lens profile is the **identity-and-voice hub**:

- expert_id, role, pairing tags, voice tier, convergence/tension stubs
- signature mechanisms and failure modes (when mature)
- public **Links** hub and ingest routing notes

It is **not**:

- transcript provenance (→ `*-source-index.md`, archive)
- arc motion (→ `*-arc.md`)
- task routing (→ `*-routing.md`)
- load-bearing synthesis (→ `statecraft/notes/`, daily, essays)

---

## Required sections (all migrated profiles)

| Section | Required | Notes |
|---|---|---|
| Title + `expert_id` | yes | `# Strategy expert — <Name> (\`<expert_id>\`)` |
| Fence | yes | `WORK only; not Record.` |
| Canonical pointers | yes | **Canonical profile**, **Canonical shelf**, **Canonical index** (commentator-threads row when applicable) |
| `## Introduction` | yes | Short orienting paragraph — who, what lane, why reused |
| `## Identity` | yes | Table: Name, expert_id, Role, Default grep tags, Typical pairings, Notebook-use tags |
| `## Voice fingerprint (compact)` | yes | Tier + last-reviewed; anchor `id="voice-fingerprint-compact"` |
| `## Convergence fingerprint` | yes | Full prose or explicit seed stub |
| `## Tension fingerprint` | yes | Full prose or explicit seed stub |
| `## Links` | yes | `### Social media`, `### Substack`, `### Other links` |

---

## Recommended sections (mature or seed-stubbed)

| Section | When |
|---|---|
| `## Signature mechanisms` | Always stub or fill — mechanism vocabulary is load-bearing |
| `## Failure modes / overreads` | When analyst-tier claims need verify discipline |
| `## Active weave cues` | When same-week pairings are routine |
| `## Ingest note` | When intake family is non-obvious (Nawfal, Substack mix, etc.) |
| `## Statecraft / AI` or bounded notes table | When thematic notes live under `statecraft/notes/` |
| `## Seed` | When automation mirrors commentator index rows |
| Tri-mind pointer block | When `strategy-expert-<id>-mind.md` or CIV-MIND exists |
| Intake receipt links (footer) | When Nawfal/archive captures are the profile's anchor set |

**Seed maturity:** mark thin sections with `*Seed profile — operator extends when upgraded.*` rather than omitting the heading.

---

## File scaffold (copy and replace)

```md
# Strategy expert — <Full name> (`<expert_id>`)
<!-- word_count: <n> -->

WORK only; not Record.

**Canonical profile:** this file.
**Canonical shelf:** [README.md](README.md) · [index.md](index.md)
**Canonical index:** [strategy-commentator-threads.md](../../../codex/strategy-commentator-threads.md) — **`<expert_id>`** lane.

---

## Introduction

<One short paragraph: who this speaker is, what translation job they perform, primary recurring surface(s).>

## Identity

| Field | Value |
|-------|-------|
| **Name** | <Name> (`@handle` when stable) |
| **expert_id** | `<expert_id>` |
| **Role** | <One-line lane job> |
| **Default grep tags** | `<tags>` |
| **Typical pairings** | × `<expert>`, … |
| **Notebook-use tags** | `validate`, `orient`, … |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint — last reviewed** | `YYYY-MM` |

Promotion and refresh defaults: [civ-lens-profile-template.md](civ-lens-profile-template.md#voice-fingerprint-compact).

## Convergence fingerprint

*Seed profile — operator extends when upgraded.*

## Tension fingerprint

*Seed profile — operator extends when upgraded.*

## Signature mechanisms

- **<mechanism label>:** <one-line definition>
- …

## Failure modes / overreads

- <claim class that needs wire verify or abstention>

## Active weave cues

- Pair **<speaker>** × **<speaker>** when <condition>.

## Ingest note

- Primary intake family: `<source-archive pattern>`
- Standalone X/Substack: `thread:<expert_id>` — verify operational claims.

## Links

### Social media

- <URL or `- None currently tracked.`>

### Substack

- <URL or `- None currently tracked.`>

### Other links

- <institution / site / archive URLs>
```

Optional footer when captures anchor the profile:

```md
---

**Intake receipts:** [capture slug](<archive-path>) · …
```

---

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — template law

- **Tier `B`** is the default for migrated civ-lens profiles until a full mind pass promotes register evidence.
- **Last reviewed** = month of last operator or assistant pass on voice table + mechanisms.
- Long-form voice for tri-mind lives in `strategy-expert-<id>-mind.md` / CIV-MIND — **not** duplicated in full inside the profile.
- Do not merge wire-grade operational claims into voice fingerprint; keep those in failure modes or ingest notes.

---

## Migration checklist

When promoting `codex/profiles/<speaker>-profile.md` → `statecraft/civ-lens/<speaker>/<speaker>-profile.md`:

1. Copy corpus to civ-lens SSOT; replace codex path with a **redirect stub** only.
2. Normalize header pointers (**Canonical profile / shelf / index**).
3. Ensure required sections exist (stub acceptable).
4. List profile first in shelf `README.md` **Open first** and `index.md`.
5. Add row to [codex/profiles/README.md](../../../codex/profiles/README.md) migrated table.
6. Add speaker to **Current migrated profiles** in [README.md § Speaker profile law](README.md#speaker-profile-law).
7. When `*-source-index.md` exists: register in [INDEX.md](INDEX.md) and [repo-map.yaml](../../../repo-map.yaml).

---

## Boundary

- One SSOT profile per speaker shelf — no duplicate full copies under `codex/profiles/`.
- Profile shape compliance is operator-maintained until a validator is added; this file is the contract reference.
