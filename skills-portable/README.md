# Portable skills (strategy-codex)

**Purpose:** Vendor-neutral **skill cores** you can copy into other hosts (ChatGPT custom instructions, Copilot skill packs, another Cursor repo) without dragging strategy-codex-only paths into the default body.

**Discovery layer:** [catalog.md](catalog.md) - short human-readable cards for selected promoted and draft skills. Derivative only; canonical method remains in each `SKILL.md`.

**Canonical layout**

| Path | Role |
|------|------|
| `skills-portable/<skill-name>/SKILL.md` | Portable core: frontmatter + methodology (minimal instance paths) |
| `.cursor/skills/<skill-name>/CURSOR_APPENDIX.md` | **Host-only:** repo paths, script commands, internal doc links |
| `.cursor/skills/<skill-name>/SKILL.md` | **Generated** — do not hand-edit; run sync (see below) |

**Canonical source:** For every manifest-listed skill, **`skills-portable/<skill-name>/SKILL.md`** is the **only** hand-edited methodology body. Edits under `.cursor/skills/*/SKILL.md` **without** syncing are **drift** — the next `sync_portable_skills.py` overwrites them. After changing a portable core or appendix, always run **`python3 scripts/sync_portable_skills.py`** (and `--verify` before commit when unsure).

## Portable core principles

Portable skills should reflect the same core boundary rules that govern the repo:

- **Host-equivalents, not assumed files.** `self-llm.txt` currently proves that some hosts may not have `self.md` or `self-knowledge.md` at all. Portable cores should ask for host equivalents or placeholders, not assume a Grace-Mar-shaped Record tree.
- **Propose or stage only; never merge.** A portable skill may help draft approval packets or stage-only review material, but it must not imply direct Record editing or approval bypass.
- **Grounded before elegant.** If a skill cannot point to operator-provided assets, current receipts, or source-bound material, it should narrow the claim or say the evidence is thin.
- **No duplicate-lane sprawl.** When a similar lane, note, or asset already exists, the skill should prefer reuse, extension, or explicit comparison over silently spawning a near-duplicate.
- **Human pass stays load-bearing.** Approval, publication, execution, and canonization remain human acts even when the skill produces polished text quickly.
- **Surface class must stay explicit.** Archive-grounded `daily` and `monthly` synthesis skills may stay visibly speaker-shelf based and quote-bearing; synthetic intelligence-essay skills should use the archive as substrate rather than visible scaffolding.
- **Month route must stay explicit.** Month-scale work should choose whether the artifact is a `closure-audit`, `watchlist`, or `benchmark` before drafting; do not let one month surface silently perform all three jobs at once.

See [skills-portable-drift-audit-2026-05-22.md](skills-portable-drift-audit-2026-05-22.md) for the current inventory, drift analysis, and before/after examples.

**In-repo examples:** `politics-massie` (content skill) · `jurisdiction-campaign-history` (work-politics framing) · `portable-skills-sync` (pipeline skill — use when changing this layout).

**Regenerate Cursor skill files**

```bash
python3 scripts/sync_portable_skills.py
python3 scripts/sync_portable_skills.py --dry-run
python3 scripts/sync_portable_skills.py --verify
```

**Consume outside strategy-codex**

1. Copy `skills-portable/<skill>/SKILL.md` (and optional `examples/` if present).
2. Add your own appendix: paths to *your* policy docs, account rules, and compliance notes.
3. Keep `description` as **one line** (many hosts break multi-line YAML).

**Spec:** [_schema.md](_schema.md) · **Manifest:** [manifest.yaml](manifest.yaml) · **Validate:** `python3 scripts/validate_skills.py` (default check after skill edits).

**Skill cards (derived):** Compact JSON/Markdown for faster session context — [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md). Build: `python3 scripts/build_skill_cards.py --markdown`.

---

## Discovery ladder (capture → ship)

Goal: **skills are discovered** from repeated success; the repo makes capture **low cost**.

| Step | Where | Action |
|------|--------|--------|
| **1 — Pointer** | [skill-candidates.md](skill-candidates.md) | One table row: date, working name, trigger phrase, pointer (commit / “this thread”). |
| **2 — Draft** | [_drafts/](_drafts/) | Full near-final portable `SKILL.md`; no manifest yet. |
| **3 — Listed** | `skills-portable/<skill>/` + `manifest.yaml` | Portable core + appendix path; run `sync_portable_skills.py`. |

**Triggers (assistant):** After a substantive **EXECUTE** / **EXECUTE_LOCAL** / **DOCSYNC** ship (commit, push when requested), offer **one optional** skill-capture line unless a **fixed session menu** (e.g. **`coffee`** **A–G**; legacy **hey**) applies or the operator said **no menu**. **Skills / meta:** say **skills** or **meta** with **coffee B — Build** (or after **Build**), not an extra letter beyond **A–G**. See [.cursor/rules/operator-style.mdc](../../.cursor/rules/operator-style.mdc) and [docs/operator-agent-lanes.md](../docs/operator-agent-lanes.md).
