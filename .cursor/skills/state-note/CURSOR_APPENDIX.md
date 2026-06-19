**strategy-codex instance notes**

- Notes shelf SSOT: [statecraft/notes/README.md](/C:/dev/strategy-codex/statecraft/notes/README.md)
- Prose-class chooser: [docs/prose-index.md](/C:/dev/strategy-codex/docs/prose-index.md)
- Multi-lens handoff source: [.cursor/skills/statecraft-multi-lens/SKILL.md](/C:/dev/strategy-codex/.cursor/skills/statecraft-multi-lens/SKILL.md) — bounded `statecraft/notes/` when comparison is method-bearing
- Daily parent (when promoting from a full day): [state-synthesis](/C:/dev/strategy-codex/.cursor/skills/state-synthesis/SKILL.md)
- **civ-state return:** when note exposes civilizational retrieval gap → [civ-state skill](../civ-state/SKILL.md) **D. Review** with named `public/civ-state/` edit target (operator appendix only — do not embed in note prose unless claim is explicitly civilizational)
- Singularity sibling: [singularity-note-promotion](/C:/dev/strategy-codex/.cursor/skills/singularity-note-promotion/SKILL.md)

**Examples (shelf-native)**

- Speaker-function comparison: [barnes-johnson-aguilar-kent-on-section-224.md](/C:/dev/strategy-codex/statecraft/notes/barnes-johnson-aguilar-kent-on-section-224.md)
- Same-day guest-pair citation split: [june-18-2026-mou-guest-pair-citation-split.md](/C:/dev/strategy-codex/statecraft/notes/june-18-2026-mou-guest-pair-citation-split.md)
- Mechanism note: [formal-sovereignty-vs-internal-carriage.md](/C:/dev/strategy-codex/statecraft/notes/formal-sovereignty-vs-internal-carriage.md)

**Archive anchor convention**

- Day index: `source-archive/statecraft/<YYYY-MM-DD>/README.md`
- Captures: `source-archive/statecraft/<YYYY-MM-DD>/source-*.md`
- After intake lands: day README already built by post-land chain; cite paths from README when promoting

**Repo notes**

- Hand-edit **only** `skills-portable/state-note/SKILL.md`; run sync before commit.
- Promotion is forward-only on the notes shelf unless operator requests cleanup migration.
- Kiev/Kharkov operator spelling applies in synthesis framing around archive quotes; preserve load-bearing verbatim in quotes per workspace rules.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill state-note
python scripts/sync_portable_skills.py --verify --skill state-note
python scripts/validate_skills.py
```
