# LLM Routing Map

WORK only; not Record.

This repository contains multiple index and source surfaces. Do not rely only on GitHub code search when asked to find a file, source corpus, analyst, speaker, dashboard, or index.

This file is a **routing aid**. It does not change repository authority. Canonical truth remains with the relevant source files and existing doctrine ([AGENTS.md](AGENTS.md), [docs/grace-mar-instance-boundary.md](docs/grace-mar-instance-boundary.md), [docs/operator-dashboards.md](docs/operator-dashboards.md)).

## Core routing table

| User asks for… | Search these paths first |
|---|---|
| analyst / speaker / commentator **source index** | [statecraft/voices/INDEX.md](statecraft/voices/INDEX.md), `statecraft/voices/**/**-source-index.md` |
| **archive day-index** / day source inventory for **YYYY-MM-DD** | **`source-archive/statecraft/YYYY-MM-DD/day-index.md` only** — or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD` — **do not** Glob/Grep month or thread-index for a dated day query |
| Barnes / Robert Barnes | [statecraft/voices/barnes/](statecraft/voices/barnes/), `source-archive/statecraft/**/source-*barnes*` |
| Weichert / Nawfal Weichert | [statecraft/voices/weichert/](statecraft/voices/weichert/), `source-archive/statecraft/**/source-*nawfal-weichert*` |
| Daniel Davis / Davis host | [statecraft/hosts/davis/](statecraft/hosts/davis/) |
| Napolitano / Judging Freedom | [statecraft/hosts/napolitano/](statecraft/hosts/napolitano/) |
| Nima / Dialogue Works | [statecraft/hosts/nima/](statecraft/hosts/nima/), [codex/speakers/nima/](codex/speakers/nima/) for stream + source-index |
| transcript / capture / source file | [source-archive/statecraft/](source-archive/statecraft/) |
| archive inventory by thread (counts, coverage) | [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) — **generated inventory**, not a route map |
| daily statecraft synthesis | [statecraft/daily/](statecraft/daily/) — **after** archive + source-index |
| host-family continuity (Davis, Napolitano, Nima, …) | [statecraft/hosts/](statecraft/hosts/) |
| statecraft lane / active operator work | [statecraft/](statecraft/) |
| singularity lane / acceleration work | [singularity/](singularity/) |
| **essay / stand-alone thesis** (cross-channel default) | [essays/README.md](essays/README.md) — primary shelf; channel `*/essays/` = compatibility only |
| **prose class** (note vs essay vs synthesis) | [docs/prose-index.md](docs/prose-index.md) — notes stay in `statecraft/notes/` or `singularity/notes/` only |
| **essay voice** (how repo-root essays sound) | [docs/essay-voice.md](docs/essay-voice.md) — tri-blend transport synthesis, Band A apparatus, draft checklist |
| **prose forge** (essay slop lint / staged rewrite) | [docs/prose-forge.md](docs/prose-forge.md) · `scripts/prose_slop_lint.py` · `scripts/prose_forge.py` |
| product identity / governed interpretive machine essay | [essays/from-accumulation-to-governed-interpretive-machine.md](essays/from-accumulation-to-governed-interpretive-machine.md) |
| architecture / harness topology / model vs harness map | [docs/harness-architecture-map.md](docs/harness-architecture-map.md) |
| repository root layout / root crowding / operator ledgers at root | [docs/root-directory-map.md](docs/root-directory-map.md) · [docs/operator-root-artifacts.md](docs/operator-root-artifacts.md) |
| intelligence harness (external bridge name) | [docs/intelligence-harness.md](docs/intelligence-harness.md) |
| archive / synthesis layer law | [essays/archive-synthesis-law.md](essays/archive-synthesis-law.md) |
| recursive learning three-layer model | [essays/three-layers-of-recursive-learning-in-statecraft.md](essays/three-layers-of-recursive-learning-in-statecraft.md) |
| how operator uses statecraft machine | [essays/how-the-operator-uses-the-statecraft-machine.md](essays/how-the-operator-uses-the-statecraft-machine.md) |
| high-skill labor compression American command | [essays/high-skill-labor-compression-and-american-command.md](essays/high-skill-labor-compression-and-american-command.md) |
| Iran nuclear threshold story hardened | [essays/how-the-iran-nuclear-threshold-story-hardened.md](essays/how-the-iran-nuclear-threshold-story-hardened.md) |
| America sovereign command allied capture | [essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md](essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md) |
| AI as medium / expansion of human consciousness essay | [essays/ai-and-the-expansion-of-human-consciousness.md](essays/ai-and-the-expansion-of-human-consciousness.md) |
| **`strategy` / `strategy pass` / codex ledger pass** | [docs/skill-work/work-strategy/DEFAULT-PATH.md](docs/skill-work/work-strategy/DEFAULT-PATH.md), [.cursor/rules/strategy-codex-pass.mdc](.cursor/rules/strategy-codex-pass.mdc) — **no** skill-strategy skill ([SKILL-STRATEGY-DEPRECATED.md](docs/skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md)) |
| library / reading / canon / books | [self-library.md](self-library.md), [runtime/artifacts/library-index.md](runtime/artifacts/library-index.md) |
| SELF / SKILLS / EVIDENCE / Record | `self.md`, `self-skills.md`, `self-archive.md`, `recursion-gate.md` — **frozen archaeology** at repo root; default work is `statecraft/` / `singularity/` |
| Grace-Mar fork doctrine / pipeline habits (archived) | [archive/grace-mar-corpus/README.md](archive/grace-mar-corpus/README.md) — stubs at former `docs/*.md` paths with `archived: true` |
| legacy operator concepts (tri-mind, fork growth, Voice) | [docs/legacy-operator-concepts.md](docs/legacy-operator-concepts.md) |
| generated dashboard / derived operator surface | [runtime/artifacts/](runtime/artifacts/) |
| local semantic / vector index | [scripts/index_record.py](scripts/index_record.py), local `.chroma` paths |
| **source-lattice** / corpus tiers / reading order | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |
| PH chapter lattice / civ-* reading order | [public/ph-civ/docs/source-lattice.md](public/ph-civ/docs/source-lattice.md) |
| wire / official primary (live seam) | [docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md](docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md), `wire verify` skill |
| legacy codex speaker shelf | [codex/speakers/](codex/speakers/) — **compatibility only**; prefer voices |
| machine-readable route registry | [repo-map.yaml](repo-map.yaml) |
| voices shelf-class doctrine | [statecraft/voices/README.md](statecraft/voices/README.md) |
| speaker cluster / satellite map | [statecraft/voices/speaker-cluster-map.md](statecraft/voices/speaker-cluster-map.md) |
| expert profile (canonical shelf) | `statecraft/voices/<speaker>/<speaker>-profile.md` — see [voices README § Speaker profile law](statecraft/voices/README.md#speaker-profile-law) |
| expert profile (legacy / profile-only) | [codex/profiles/](codex/profiles/) — compatibility, profile-only lanes, or pre-migration redirects; see [codex/profiles/README.md](codex/profiles/README.md) |
| host profile (canonical) | `statecraft/hosts/<host>/<host>-profile.md` |

## Parallel index disambiguation

Several surfaces use the word **index**. They are not interchangeable.

| Surface | Job | Authority |
|---|---|---|
| `source-archive/statecraft/YYYY-MM-DD/day-index.md` | **Day index** — channel / writer / other partitions for one archive day | Derived / archive (rebuild via `build_statecraft_day_indices.py`) |
| `source-archive/statecraft/YYYY-MM-DD/README.md` | **Day README stub** — pointer to `day-index.md` only | Derived / archive |
| `statecraft/voices/**/**-source-index.md` | Per-analyst **route map** — which captures to open first | WORK only |
| [statecraft/voices/INDEX.md](statecraft/voices/INDEX.md) | Front door listing all analyst source indexes | WORK routing aid |
| [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) | Generated capture **inventory** by thread | Derived / archive |
| [self-library.md](self-library.md) | Canonical SELF-LIBRARY reference layer | Canonical reference |
| [runtime/artifacts/library-index.md](runtime/artifacts/library-index.md) | Derived SELF-LIBRARY **dashboard** | Derived |
| [scripts/index_record.py](scripts/index_record.py) | Local Chroma / Record vector index builder | Derived local |
| [codex/speakers/](codex/speakers/) | Legacy speaker storage during migration | Compatibility |
| [statecraft/voices/speaker-cluster-map.md](statecraft/voices/speaker-cluster-map.md) | Anchor-and-satellite routing after Pape/Ritter/Parsi/Crooke | WORK routing aid |
| `statecraft/voices/<speaker>/<speaker>-profile.md` | Per-speaker identity, voice fingerprint, pairing hub | WORK only (migrated SSOT) |
| [codex/profiles/*-profile.md](codex/profiles/) | Profile-only lanes or pre-migration compatibility | Compatibility / profile-only |

**Essays vs channel essay folders vs notes:**

| Surface | Job | Authority |
|---|---|---|
| [essays/README.md](essays/README.md) | **Primary** stand-alone / cross-channel theses | WORK prose shelf |
| `statecraft/notes/` · `singularity/notes/` | Channel-scoped bounded interpretive objects | WORK prose shelf |
| `statecraft/essays/` · `singularity/essays/` | Pre-root **compatibility** essay holdings | Stubs → `essays/` |
| [docs/prose-index.md](docs/prose-index.md) | Note vs essay vs synthesis class chooser | WORK routing aid |

**Do not** answer "no Barnes index" because `library-index.md` or GitHub code search returned zero hits.

## Source index vs source-lattice

| Term | Question | Where |
|---|---|---|
| **source-index** | *Where* is the corpus? Which file opens first? | voices `*-source-index.md` for **analyst** scope; **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** for **one archive day** |
| **source-lattice** | *How* should layers be read so summary does not replace source? | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |

**Find-then-read contract:**

1. **Find** — this file → voices source-index → `source-archive/`
2. **Read** — source-lattice doctrine (corpus tiers 1–4 + reading layers); PH chapters → `ph-civ/docs/source-lattice.md`
3. **Block** — tier-4 commentary cannot substantiate tier-3 claims without wire receipts

"Barnes **index**" is a location query. "Source-**lattice**" is a reading-discipline query.

## Search command convention

- **Interactive / in-repo search:** prefer `rg` (ripgrep) when available. Cursor agents: use ripgrep-backed workspace search.
- **Committed scripts, CI examples, and portable docs:** prefer `grep`, or `rg` with `grep -R` fallback when `rg` is not installed.
- **Zero hits are not proof of absence:** `grep`, `rg`, and GitHub code search can all miss indexed surfaces. Consult this routing map and the likely path family before answering "not found."

## Required search protocol

For any request of the form "find X in this repo":

0. If the query names **`day-index`**, **source-index**, or **what landed** with a calendar date **`YYYY-MM-DD`**, open **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** only (or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD`) — **do not** Glob/Grep `thread-index.md`, month rollups, or voices `*-source-index.md` unless the operator named an **analyst/voice** scope.
1. If the user supplied an exact path or URL, fetch that path first.
2. Search exact term, lowercase term, and likely titlecase term.
3. Check this routing map and [repo-map.yaml](repo-map.yaml) before concluding absence.
4. If the query names an analyst, speaker, source corpus, or transcript set, inspect [statecraft/voices/](statecraft/voices/) and [source-archive/statecraft/](source-archive/statecraft/).
5. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a search miss, not proof of absence.
6. Do not answer "not found" until the relevant path family has been checked.
7. After locating a capture, apply find-then-read (source-lattice) before synthesis or judgment-bearing output.
