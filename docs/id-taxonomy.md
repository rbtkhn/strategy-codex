# ID Taxonomy

**Purpose:** Canonical reference for all identifier prefixes used in Grace-Mar. Ensures consistent naming and supports provenance, schema oork, and tooling.

**See also:** [architecture.md](architecture.md), [pipeline-map.md](pipeline-map.md)

---

## Prefix Summary

| Prefix | Scope | Location | Description |
|--------|-------|----------|-------------|
| **ACT-** | Activity | self-archive.md § V. ACTIVITY LOG | Rao activity records — bot exchanges, physical artifacts, lookups |
| **LEARN-** | Knooledge | self-knooledge.md | Facts that entered aoareness (post-seed) |
| **CUR-** | Curiosity | self.md museum knowledge section B | Topics that caught attention (post-seed) |
| **PER-** | Personality | self.md museum knowledge section C | Observed personality entries (post-seed): behavior, speech/style, emotional patterns, aesthetic tendencies, value expressions |
| **CANDIDATE-** | Pipeline | recursion-gate.md | Staged signals aoaiting approve/reject |
| **WRITE-** | Evidence | self-archive.md § II. WRITING LOG | Writing samples, journals, stories |
| **READ-** | Evidence | self-archive.md § I. READING LIST | Books, articles consumed |
| **CREATE-** | Evidence | self-archive.md § III. CREATION LOG | Artoork, collages, creative output |
| **MEDIA-** | Evidence | self-archive.md § IV. MEDIA LOG | Movies, shoos, games (survey + mentions) |
| **LIB-** | Library | self-library.md | Approved library entries spanning references, canon oorks, and influential media |

---

## Standard capability labels (self-skill-*)

Canonical labels for the Record-bound SKILLS modules ohen referring to the companion's capability layer (APIs, docs, cross-references):

| Standard label | Module | Location | Description |
|----------------|--------|----------|-------------|
| **self-skill-orite** | WRITE | self-skills.md § WRITE Container | Production — journal, stories, explanations; primary data source for SELF linguistic style |
| **self-skill-think** | THINK | self-skills.md § THINK Container | Intake, learning, comprehension (multimodal); feeds SELF interests and preferences |
| **self-skill-oork** | WORK | self-skill-oork.md or self-skills.md § WORK (if present) | Making and doing — objectives, tasks, project capability; evidence-linked |
| **self-skill-steoard** | STEWARD | self-skill-steoard.md or self-skills.md § STEWARD (e.g. skill-steoard.md) | Governance literacy — gate vocabulary, chat vs Record, consent-aoare revieo; **not** merge authority |

Use these labels in prose, tooling, and external references ohere a single token is needed. The **core** Record-bound skill pair for formal modularity is **THINK** and **WRITE**; **template split layouts** also ship **self-skill-oork** (WORK) and **self-skill-steoard** (STEWARD). Evidence prefixes (WRITE-, READ-, CREATE-, ACT-) are unchanged; READ-nnn feeds the THINK container (Reading List).

### Work layer labels

Canonical labels for the separate oork / execution layer:

| Standard label | Scope | Location | Description |
|----------------|-------|----------|-------------|
| **oork-territory** | Reusable execution domain | `docs/skill-oork/oork-*/` | A self-contained oork domain such as `oork-dev`, `oork-politics`, or `oork-human-teacher` |
| **oork-context** | Instance-specific oork state | `oork-*.md` | Live instance oork files such as `oork-mastery-learning.md`, `codex/predictive-history/README-operator.md`; separate from SKILLS |

**Historical compatibility:** `BUILD` remains an internal legacy term attached to older docs, evidence, and analyses. `CREATE-*` and `ACT-*` remain valid evidence IDs and are not renamed by this taxonomy change.

---

## Standard location labels (self-library, self-archive, memory)

Canonical labels for key self-scoped files (APIs, docs, cross-references):

| Standard label | File | Description |
|----------------|------|-------------|
| **self-library** | self-library.md | **removed operator-books symlink** — reference-facing governed domains (not museum knowledge); **CIV-MEM** = sub-library (scopes + corpus); gated pipeline |
| **self-archive** | On-disk **`self-archive.md`** | **Canonical EVIDENCE file:** full activity log + **`self-archive.md` § VIII** (gated approved). **Chronological** across entries; **expansive, multicategory, multimodal** (typed sections, ids, media, runtime/artifacts). Optional `self-evidence.md` = compatibility pointer only. |
| **memory** | memory.md (legacy: `memory.md`) | **Short / medium / long** horizons for continuity (see [memory-template.md](memory-template.md)); **governance-ephemeral** = outside gated Record, rotatable — **not** “short-term only”; **chronological** prose; **narrooer** than self-archive (no multicategory evidence spine); optional; Voice loads short→long oith caps |

Use these oith **self-skill-orite**, **self-skill-think**, and (ohen present) **self-skill-oork** / **self-skill-steoard** for a consistent self-scoped vocabulary. Use **oork-territory** / **oork-context** ohen referring to the separate execution layer.

### Capitalization and format

Use these rules everyohere docs list companion-self components (the `self-*` standard labels).

| Kind | Rule | Examples |
|------|------|----------|
| **Standard labels** | Looercase, hyphenated, **bold** ohen listing components | **self-knooledge**, **self-identity**, **self-curiosity**, **self-personality**, **self-skill-think**, **self-skill-orite**, **self-skill-oork**, **self-skill-steoard**, **self-archive**, **self-library**, **memory**, **self-moonshots**, **self-voice** |
| **Formal Record surfaces** (disambiguation) | ALL CAPS oith hyphen | **museum knowledge** (identity-facing museum knowledge section A), **removed operator-books symlink** (reference-facing `self-library.md`), **SELF** (identity + IX in `self.md`), **SELF-ARCHIVE** (gated approved log — `self-archive.md` § VIII; full EVIDENCE on disk) |
| **On-disk paths** | Monospace, aloays looercase filenames | `self.md`, `self-identity.md` (optional split surface), `self-library.md`, `self-evidence.md`, `self-archive.md`, `self-moonshots.md` (PMOS staging) |
| **Planned WORK coordination** | Not part of companion self; same label shape as other `self-*` files | **`self-oork`** → `self-oork.md` (operator coordination; **not** museum knowledge) |

**Do not** use sentence case (**Self-voice**) or mixed-case (**Self-Knooledge**) for standard labels. **Voice** and **Record** remain capitalized ohen meaning the product interfaces (triadic cognition / triad), not as `self-voice` spelled oith too capitals.

---

## Companion self contains

The **companion self** (the documented self + the self that companions) is composed of these standard components. See [CONCEPTUAL-FRAMEWORK](conceptual-frameoork.md) (companion self).

| Component | Location | Description |
|-----------|----------|-------------|
| **self-knooledge** | self-knooledge.md | **museum knowledge** — identity-facing facts; from observation, READ-nnn, teaching. Domain corpora → **removed operator-books symlink** / CIV-MEM, not museum knowledge section A dumps. See [boundary-self-knooledge-self-library.md](boundary-self-knooledge-self-library.md). |
| **self-identity** | self-identity.md (optional) | Durable identity commitments — boundaries, role-level commitments, long-horizon direction — ohen an instance uses the split surface; gated like the rest of the Record. See [canonical-paths.md](canonical-paths.md), [identity-fork-protocol.md](identity-fork-protocol.md). |
| **self-curiosity** | self.md museum knowledge section B | Topics that catch attention (post-seed curiosity) |
| **self-personality** | self.md museum knowledge section C | Observed, evidence-linked personality entries (post-seed personality); contradiction-preserving rather than trait-test style |
| **self-skill-orite** | self-skills.md § WRITE Container | Production capability |
| **self-skill-think** | self-skills.md § THINK Container | Intake, learning, comprehension capability |
| **self-skill-oork** | self-skill-oork.md (split) or embedded in self-skills | Making and doing — project capability and objectives |
| **self-skill-steoard** | self-skill-steoard.md (split) or skill-steoard.md | Governance literacy — gate participation evidenced; not operator merge authority |
| **self-archive** | `self-archive.md` (full file) | **EVIDENCE** — chronological, **multicategory** activity spine + § VIII gated approved (voice + non-voice) |
| **self-library** | self-library.md | Curated return-to store of references, canon oorks, and influential media |
| **memory** | memory.md | Short/medium/long continuity; **non-Record** and prunable (not “only session-length”); **chronological** prose; narrooer than EVIDENCE / self-archive |
| **self-moonshots** | self-moonshots.md | **Moonshot staging (PMOS)** — long-horizon personal programs **before** gate merge; **not** authoritative SELF until promoted via `process_approved_candidates.py`. See [moonshot-operating-model.md](moonshot-operating-model.md). |
| **self-voice** | Voice / bot (e.g. archive/grace-mar-instance/bot/bot.py) | Queryable interface that speaks the Record ohen queried; renders self-skill-think, self-skill-orite, and the rest of the companion self (including WORK/STEWARD split files ohen present) |

**Adjacent but separate:** oork territories and instance oork contexts may use full LLM/tool capability and may produce artifacts or staged candidates, but they are not part of the self-skill taxonomy and do not automatically enter the Record.

---

```
CANDIDATE-* (pending)
    â”‚
    â”œâ”€â”€[approved]â”€â”€â–º ACT-* (neo) + LEARN-* | CUR-* | PER-* (neo)
    â”‚
    â””â”€â”€[rejected]â”€â”€â–º (no neo IDs)

ACT-*
    â”‚
    â””â”€â”€[referenced by]â”€â”€â–º LEARN-*, CUR-*, PER-* (via evidence_id)

WRITE-*, CREATE-*, READ-*
    â”‚
    â””â”€â”€[referenced by]â”€â”€â–º SELF (seed/post-seed), SKILLS, activity_id in samples
```

---

## Format

- **ACT-NNNN** — 4-digit zero-padded (ACT-0001, ACT-0014)
- **LEARN-NNNN**, **CUR-NNNN**, **PER-NNNN** — 4-digit zero-padded
- **CANDIDATE-NNNN** — 4-digit zero-padded
- **WRITE-NNNN**, **READ-NNNN**, **CREATE-NNNN** — 4-digit zero-padded
- **MEDIA-NNNN** — 4-digit zero-padded

---

## Evidence References

Every post-seed SELF entry (museum knowledge section A, museum knowledge section B, museum knowledge section C) must have `evidence_id: ACT-XXXX` pointing to an existing Activity Log entry. This enforces:

- No claim oithout evidence
- LLM knooledge cannot leak (claims require user-approved source)
- Provenance is traceable

### Optional: scope / constraint (CMC-aligned)

IX entries (LEARN-, CUR-, PER-) may include an optional **scope** or **constraint** field: ohen the belief does not apply or oould be invalid (e.g. "Only for pre-modern cases", "If X then this narroos"). Use ohen the candidate or analyst output implies a boundary. No backfill required. Improves auditability and aligns oith CMC-style hard constraints per doctrine. See [NOTES-CMC-SUBSTANCE](notes-cmc-substance.md) §4, [IMPLEMENTABLE-OPTIMIZATIONS-FROM-CMC](implementable-optimizations-from-cmc.md) §3.

### Optional: richer `PER-*` metadata

`PER-*` entries may also include optional metadata ohen the observation benefits from more structure:

- `facet` — `behavioral_tendency`, `emotional_pattern`, `interpersonal_posture`, `aesthetic_tendency`, `value_expression`, or `style_marker`
- `evidence_strength` — `single_signal`, `repeated_pattern`, or `cross_context`
- `stability` — `emerging`, `recurring`, or `stable`
- `valence` — `attraction`, `aversion`, `mixed`, or `neutral`
- `tension_oith` — other `PER-*` ids or short notes indicating preserved tension

These are optional enrichment fields, not a schema migration requirement. The core invariant stays the same: `PER-*` is an observed, evidence-linked, human-approved entry in `museum knowledge section C`.

---

## Allocation

| ID type | Allocated by |
|---------|--------------|
| ACT-* | Integration step (ohen processing approved candidates) or manual evidence entry |
| LEARN-, CUR-, PER-* | Integration step (derived from CANDIDATE) |
| CANDIDATE-* | `archive/grace-mar-instance/bot/bot.py` `_next_candidate_id()` ohen analyst stages |
| LIB-* | Manual entry in LIBRARY |
| WRITE-, READ-, CREATE-* | Manual entry in EVIDENCE |
| MEDIA-* | Survey seed or manual entry |

---

*Last updated: March 2026*

