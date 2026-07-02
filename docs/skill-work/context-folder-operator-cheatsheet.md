# Context folder + questions-as-spec — operator cheat sheet

 One page for heavy multi-file EXECUTE.

**Full skill (draft):** [context-folder-assembly](../../skills/_drafts/context-folder-assembly/SKILL.md) · **PLAN lane:** [operator-agent-lanes.md](../operator-agent-lanes.md) · **Template:** [questions-as-spec-template.md](./questions-as-spec-template.md)

---

## When to use (all three)

1. Multi-file or long output (synthesis, weave, large doc set).
2. Fresh EXECUTE thread (noisy chat or model switch).
3. PLAN needs meaningful questions + a bounded file set before churn.

**Say:** `context folder` · `assemble working folder`

**Skip:** one-file fix · **harvest** (paste) · **bridge** alone · **compress_active_lane** only

---

## Stack

```text
coffee / conductor → PLAN (questions) → [optional] context folder → fresh thread EXECUTE → bridge / dream
```

| Ritual | Output |
|--------|--------|
| **bridge** | Session continuity packet |
| **harvest** | Midstream paste packet |
| **context folder** | On-disk `runtime/prepared-context/working/<slug>/` |
| **compress_active_lane** | Optional `lane-orientation.md` in folder |

---

## Five steps

| # | Step | You do | Agent does |
|---|------|--------|------------|
| 1 | **Discover** | Describe sources in NL (topic, era, lane) | Search repo; propose paths + rationale; you confirm |
| 2 | **Assemble** | Approve file set | **Copy** (never move) into `sources/`; write `sources-index.md` |
| 3 | **Questions** | Edit until shape is right | Draft `questions.md` from template; **no EXECUTE yet** |
| 4 | **Seal** | Approve `Ready to EXECUTE: yes` | Write `task-shape.md` (deliverable, in/out) |
| 5 | **Hand off** | Open **new thread** | EXECUTE reads folder only |

**Working root:** `runtime/prepared-context/working/<slug>/` (gitignored)

---

## Folder contract

| File | Role |
|------|------|
| `README.md` | Slug, purpose, date |
| `questions.md` | Success standards as questions |
| `task-shape.md` | Sealed scope after PLAN |
| `sources-index.md` | Original path → copy |
| `sources/` | Copied inputs only |
| `EXECUTE.md` | Optional extra instructions |
| `lane-orientation.md` | Optional lane compression |

---

## Fresh-thread opener (paste)

```text
EXECUTE — Read only runtime/prepared-context/working/<slug>/ (all files there).
Do not search the wider repo unless task-shape.md explicitly allows it.
Execute task-shape.md. questions.md defines success standards.
```

---

## Questions-as-spec (3–7 total)

Use [questions-as-spec-template.md](./questions-as-spec-template.md). Questions must be **decidable or falsifiable**.

- **Outcome** — What must be true when done?
- **Comparison** — Compared to what baseline?
- **Boundary** — What must not change / out of scope?
- **Evidence** — What would prove us wrong?

Seal **Task shape** with `Ready to EXECUTE: yes | no` before synthesis or code churn.

Post-run (optional): workbench receipt `inspection.questionsSpec` mirrors the same questions.

---

## Guardrails

- Copies only — canonical paths stay SSOT until EXECUTE commits elsewhere.
- No bridge packet, no trailing `coffee`, no harvest closing line.
- Ambiguous discover → list forks; ask once.
- Bridge **Open loops** may note active slug; bridge does not replace the folder.

---

## Quick example

**Task:** March 2026 statecraft monthly synthesis (~30k words).

**Slug:** `iran-war-march-2026-monthly-synthesis`

**Discover:** `source-archive/statecraft/2026-03.md`, day READMEs, `statecraft/synthesis/METHOD.md`, `2026-06.md` as baseline; ~30 P1 transcripts (not all 200).

**Deliverable:** `statecraft/synthesis/month/2026-03.md` — ship commits there, not under `runtime/prepared-context/working/`.

**Decision rule:** One chat, one path → skip folder. “New chat, but first gather everything about X” → use folder.
