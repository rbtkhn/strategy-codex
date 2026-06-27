# Civilization memory - strategy-codex satellite (`docs/civilization-memory/`)

## Terminology (binding in this workspace)

**When you say "civ-mem" while working in strategy-codex, that means the
complete [`civilization_memory`](../../research/repos/civilization_memory)
corpus tracked in this repo** - MEM files, CIV-CORE, CIV-STATE, CIV-SCHOLAR,
ARC, templates, governance, tools: the full local corpus at
`research/repos/civilization_memory/`.

**This folder** (`docs/civilization-memory/`) is **not** a second copy of that
corpus. It holds **strategy-codex-owned** material versioned with this
workspace:

- **Essays and long-form** you edit here (theses, book drafts, panels).
- **Notes** (concepts, polyphony, face/category/blade, research briefs).
- **`minds/`** - **No mind files here.** Canonical **CIV-MIND** profiles for
  strategy work live only under
  [`docs/skill-work/work-strategy/minds/`](../skill-work/work-strategy/minds/README.md)
  (self-contained; **do not require** civ-mem). See [minds/README.md](minds/README.md).

Do not treat `docs/civilization-memory/` as the civ-mem corpus itself; treat it
as **satellite prose** (essays, book, notes). **civ-mem** = full
`research/repos/civilization_memory`; **minds** do not depend on it. Snapshot
provenance lives in
`research/repos/civilization_memory/STRATEGY-CODEX-PROVENANCE.md`.

---

## Purpose

Civilization memory has **no monetary purpose**. Its purpose is **pure
understanding of history** - patterns, causes, and lessons of civilizations,
institutions, and coordination over time - as a resource for reflection and
judgment, not for revenue. Content here deepens how we read the past so present
decisions can be wiser.

---

| Path | Role |
|------|------|
| **`essays/`** | Operator essays (Simple Condition, Coordination Hypothesis, index). Edit in place. |
| **`notes/`** | Short conceptual notes (face/category/blade, polyphony, scripture-as-test, etc.). |
| **`minds/`** | **Redirect only** - canonical minds are under **work-strategy -> strategy-notebook -> minds**. See [minds/README.md](minds/README.md). |
| **`book/`** | Manuscript and applied-theology harvest artifacts tied to the book project. |
| **`content/`** | Optional - chunked or expanded material later (large regen may mirror here). |

---

## Tooling (this tree only)

**Encyclopedia regen (essays):**

```bash
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only
```

**In-repo search index** (when full civ-mem checkout is unavailable; indexes
**this** folder):

```bash
python3 scripts/build_civmem_inrepo_index.py build
```

Index: `docs/civilization-memory/.cache/inrepo_index.json`. Default `--cmc` is
`docs/civilization-memory/`; override only if you fork layout.

---

## Provenance

Initial `essays/*.md` copied from civilization_memory (2026-03); subsequent
edits are strategy-codex commits unless the local snapshot is refreshed from
upstream intentionally. Snapshot source and imported SHA are recorded in
`research/repos/civilization_memory/STRATEGY-CODEX-PROVENANCE.md`.
