# External Codex Explorer (grace-mar)

**Status:** Active
**Scope:** WORK-only (`work-dev`)
**Purpose:** Produce **derived structural explorer receipts** (neighborhood adjacency + family clusters) for paths inside a checked-out **`civilization_memory`** tree (default: [`research/repos/civilization_memory`](../../../research/repos/civilization_memory)) â€” without editing upstream, without expanding Record authority.

**Last updated:** 2026-04-28

---

## What this is

CLIs build **JSON** reports using deterministic filesystem adjacency â€” plus optional **human-readable Markdown companions**. Reports describe layout-first exploration inside an external checkout â€” **not** doctrinal entailment.

- **Neighborhood (Phase 1b):** Paths adjacent to **one subject** (`neighbors`, group `section`s, `suggested_next_inspection`).
- **Family (Phase 1c):** All member files matching a **selector**, plus **`connection_count`** among cluster peers (`dominant_*`, `suggested_entry_points`).

Detail schemas:

**Machine-readable artifact:** JSON is the stable record (`neighbors`, â€¦ for neighborhood; `members`, â€¦ for family).

**Human-readable derivative:** Markdown **summarizes** deterministic facts (`*.neighborhood.md`, `*.family.md`). Safe as WORK exploration, not doctrine.

**SSOT artifact schemas:** [`external-codex-neighborhood-report.v1.json`](../../../schemas/registry/external-codex-neighborhood-report.v1.json), [`external-codex-family-report.v1.json`](../../../schemas/registry/external-codex-family-report.v1.json)

**Outputs:** [`runtime/artifacts/external-codex/`](../../../runtime/artifacts/external-codex/README.md) (rebuildable; default generated artifacts may be gitignored â€” see bucket README).

---

## Markdown companion report (Phase 1b)

When you pass **`--write-md`**, the builder emits **`{stem}.neighborhood.md`** beside the JSON (same `{stem}` as the JSON basename unless overridden).

Intended shape (deterministic, **no** LLM prose):

| Section | Contents |
|---------|-----------|
| **Subject** | Path; optional first `#` title line from file; civilization guess (`content/civilizations/<ID>/â€¦`); filename-class guess (`MEM--`, `CIV--STATE--`, etc.). |
| **Likely family** | Mechanical bullets: inferred civilization / file-class guesses; dominant **edge** among neighbors (`same_directory` vs `parent_directory`). Marked non-authoritative. |
| **Structural neighbors** | Grouped under fixed headings (`same_civilization`, `same_file_class`, index/core/scholar, governance/template, other). Each neighbor lists **path**, **edge**, **reason** (template strings only). |
| **Suggested next inspection targets** | Up to **5** neighbors ranked by a fixed scoring rule (edge weights + civilizational/class/section bonuses; ties broken by path sort). |
| **Notes** | Reminders: derived; does not edit upstream; heuristics only; use upstream governance for canonical answers. |

**Neither JSON nor Markdown** is canonical truth for the external repo **nor** for Grace-Mar Record.

---

## Family-level summary reports (Phase 1c)

Where **neighborhood** answers â€œwhat sits beside **this one** path?â€, **family** answers â€œwhat **cluster** of files shares a **selector**, and how densely do those files link **to each other** using the **same structural sweep** as neighborhood (same-directory + parent-directory peers), restricted to **files** that match the selector?â€

**Selectors (implemented):**

| `--selector-type` | `--selector-value` example | Membership rule |
|-------------------|------------------------------|-----------------|
| `civilization` | `ROME` | Relative path contains `content/civilizations/<VALUE>/` |
| `file_class` | `memory_spine` | `infer_file_class(basename)` equals **VALUE** (same strings as neighborhood: `memory_spine`, `civ_state`, â€¦) |

**Future extension:** optional **`path_prefix`** (substring / prefix filter on relative paths) â€” documented only until shipped in CLI.

**Firewall (same as neighborhood):** receipts are **derived**, **non-authoritative**, **no upstream edits**. Do **not** merge JSON/Markdown into Record or substitute structural graphs for MEM grounding / verify tier.

**SSOT schema:** [`schemas/registry/external-codex-family-report.v1.json`](../../../schemas/registry/external-codex-family-report.v1.json)

**Builder:** [`scripts/build_external_codex_family_report.py`](../../../scripts/build_external_codex_family_report.py). Default JSON (`--output-json` omitted) lives under **`runtime/artifacts/external-codex/families/`** (gitignored).

JSON highlights: **`members[].connection_count`**, **`dominant_file_classes`**, **`dominant_civilizations`**, **`suggested_entry_points`** (top paths by `(-connection_count, path)`).

---

## Subject-family summary

Embedded in JSON as **`likely_family`** (and echoed under **Likely family** in Markdown):

- **`subject_civilization_guess`** â€” parsed `content/civilizations/<TOKEN>/` when present.
- **`subject_file_class_guess`** â€” mechanical classification from basename prefixes (`MEM--`, `CIV--STATE--`, â€¦).
- **`dominant_edge_among_neighbors`** â€” which structural edge appears most often in the capped neighbor list.
- **`notes`** â€” fixed reminder strings (still heuristic).

No embeddings; no semantic â€œfamilyâ€ beyond path/filename tokens.

---

## Operator use

1. Ensure **`research/repos/civilization_memory`** is cloned (see CI helper below).
2. Run the CLI with **`--subject <path-relative-to-checkout>`**.
3. Open **`*.json`** for tooling / diff-friendly receipts.
4. Open **`*.neighborhood.md`** when you want a quick scan of â€œwhat else is beside this path?â€ before drilling into MEM scripts or verify-tier pulls.
5. Cite **paths + report_id** in strategy **`Links`** / **`References`** if helpful â€” never replace Â§1dâ€“Â§1h or gate merges.

---

## Non-authority reminder

- Outputs stay **WORK receipts**.
- **Do not** merge JSON/Markdown into **SELF**, **`archive/grace-mar-instance/bot/prompt.py`**, or **upstream**.
- **Do not** treat **`suggested_next_inspection`** as rankings of doctrinal importance â€” only deterministic exploration order.

---

## Governance (WORK)

- Outputs are **structural explorer receipts** only (neighborhood or family): **derived**, **non-canonical**, **no upstream mutation**.
- **Do not** substitute these reports for MEM grounding scripts (`suggest_civ_mem_from_relevance.py`, etc.), verify tier, strategy notebook **Â§1dâ€“Â§1h**, or upstream **`civilization_memory`** editorial governance.
- **Do not** treat adjacency as semantic entailment ("neighbor list proves X").

---

## Recursion-gate and self-knowledge (RECORD boundaries)

Neighborhood JSON is **lighter than** curated CIV-MEM references for Record purposes: same broad family as **[SELF-LIBRARY / CIV-MEM](../../../SELF-LIBRARY/CIV-MEM.md)** (*not* IX-A), but **more derived** â€” structural maps of upstream paths, **not** companion-endorsed world facts.

### [`recursion-gate.md`](../../../recursion-gate.md)

| Do | Donâ€™t |
|----|--------|
| Stage **`CANDIDATE-*`** only when the **companion explicitly wants** a short **workflow / preference** line merged (e.g. optional use of this builder when citing `civilization_memory`) â€” **human summary** in the candidate, **not** pasted JSON. | Auto-stage after each run; stage artifact paths as â€œknowledgeâ€; stage neighborhood content as doctrine. |

Merge discipline matches [`instance-doctrine.md`](../../../instance-doctrine.md) (script-driven merge after approval).

### [`self.md`](../../../self.md) IX-A / IX-B / IX-C

- **IX-A:** Do **not** merge **substantive** claims mined from neighborhood graphs. **Rare exception:** companion-approved **meta** one-liner about **how** they work with civ paths (**human prose**, not schema dumps).
- **IX-B:** Only if the companion **initiates** curiosity about tooling â€” **not** assistant-inferred from artifacts.
- **IX-C:** Possible home for **working-style** lines **if** approved â€” **one sentence**, no file dumps.
- **`archive/grace-mar-instance/bot/prompt.py`:** No explorer-derived injection unless the companion **explicitly** requests a minimal boundary line â€” **default: omit.**

---

## CLI

JSON only:

```bash
python3 scripts/build_external_codex_neighborhood.py \
  --checkout research/repos/civilization_memory \
  --subject content/civilizations/ROME/CIV--STATE--ROME.md \
  --out-dir runtime/artifacts/external-codex
```

JSON + Markdown companion:

```bash
python3 scripts/build_external_codex_neighborhood.py \
  --checkout research/repos/civilization_memory \
  --subject content/civilizations/ROME/CIV--STATE--ROME.md \
  --out-dir runtime/artifacts/external-codex \
  --write-md
```

| Flag | Meaning |
|------|---------|
| `--checkout` | Directory relative to repo root (must exist). Default: `research/repos/civilization_memory`. |
| `--subject` | Path relative to **checkout** (required). Use forward slashes. |
| `--out-dir` | Directory for default `{stem}.json` (default: `runtime/artifacts/external-codex`). Created if missing. |
| `--output-json` | Explicit JSON output path (optional). Relative paths resolve against **repo root**. |
| `--write-md` | Write **`{stem}.neighborhood.md`** human-readable companion. |
| `--output-md` | Explicit Markdown path (requires **`--write-md`**). Relative paths resolve against **repo root**. |
| `--neighbor-limit` | Max neighbor rows (default: 250). |
| `--repo-root` | Override grace-mar repo root (default: parent of `scripts/`). |

Exit **non-zero** if checkout missing, subject escapes checkout, subject missing on disk, path traverses `..`, path resolves under `.git`, or **`--output-md`** is given without **`--write-md`**.

### Family cluster CLI (`build_external_codex_family_report.py`)

JSON only:

```bash
python3 scripts/build_external_codex_family_report.py \
  --repo-path research/repos/civilization_memory \
  --selector-type civilization \
  --selector-value ROME \
  --output-json runtime/artifacts/external-codex/families/civilization__ROME.json
```

JSON + Markdown companion (default output dir **`runtime/artifacts/external-codex/families/`** when `--output-json` is omitted):

```bash
python3 scripts/build_external_codex_family_report.py \
  --repo-path research/repos/civilization_memory \
  --selector-type file_class \
  --selector-value memory_spine \
  --write-md
```

| Flag | Meaning |
|------|---------|
| `--repo-path` | Checkout directory (required). Relative to **`--repo-root`** or absolute. |
| `--selector-type` | `civilization` or `file_class`. |
| `--selector-value` | Civilization folder id or inferred file-class label. |
| `--output-json` | Explicit JSON path (optional; default under **`runtime/artifacts/external-codex/families/`**). |
| `--write-md` | Write **`{stem}.family.md`** companion. |
| `--output-md` | Explicit Markdown path (requires **`--write-md`**). |
| `--member-limit` | Cap members enumerated (default 5000); sets **`truncated`** when hit. |
| `--repo-root` | Override grace-mar repo root (default: parent of `scripts/`). |

---

## Structural heuristics (deterministic)

### Filesystem sweep

For a **file** subject:

- **`same_directory`:** Other entries in the same directory (siblings), sorted.
- **`parent_directory`:** Entries in the parent of that directory (one level up), sorted â€” includes the directory that holds the file as orientation.

For a **directory** subject:

- **`same_directory`:** Immediate children of that directory, sorted.
- **`parent_directory`:** Sibling directories/files of that directory in its parent.

Hidden entries (names starting with `.`) except when required are skipped; **`.git`** is never traversed or listed.

### Family intra-cluster linkage (`connection_count`)

For each member **file**, neighbors are enumerated with the **same** filesystem sweep as neighborhood (same-directory then parent-directory listings). **`connection_count`** is how many neighbor paths are also **cluster members** (other files matching the selector), excluding self.

### Companion grouping (Markdown / JSON `section`)

Each neighbor row receives a **single** deterministic bucket (first match wins):

1. **same_civilization** â€” neighbor path shares `content/civilizations/<ID>/` with the subjectâ€™s inferred civilization id.
2. **same_file_class** â€” same **`infer_file_class`** label as subject when subject class is not `other`.
3. **index_core_scholar** â€” filename/path matches MEM--/INDEX/STATE/minds/scholar heuristics.
4. **governance_template** â€” path contains `templates/` or basename suggests template markers.
5. **other_structural** â€” fallback.

### Subject-family (`likely_family`)

Path tokens (`civilizations/<ID>`), basename prefixes, and dominant edge counts â€” **mechanical only**.

### Suggested inspection (`suggested_next_inspection`)

Fixed integer score from edge weight + civ/class/section bonuses; top **5** unique paths; ties broken by lexicographic **`path_relative`**.

---

## Relation to other lanes

- **`skill-write`:** Optional **preflight** context when paste-ready copy **anchors** to checkout paths â€” JSON stays WORK; see [`docs/skill-write/write-operator-preferences.md`](../../skill-write/write-operator-preferences.md).
- **`skill-strategy` / strategy-notebook:** Optional **Links / References** receipts â€” **after** MEM relevance picks when both apply; never replaces verify or Judgment authority.
- **`civilizational-strategy-surface.md`:** Thin bridge doc â€” same â€œno duplicate corpusâ€ discipline.

---

## See also

- [`runtime/artifacts/external-codex/README.md`](../../../runtime/artifacts/external-codex/README.md)
- CI checkout helper: [`scripts/ci/clone_civilization_memory.sh`](../../../scripts/ci/clone_civilization_memory.sh)

