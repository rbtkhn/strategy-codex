# LLM Routing Map

WORK only; not Record.

This repository contains multiple index and source surfaces. Do not rely only on GitHub code search when asked to find a file, source corpus, analyst, speaker, dashboard, or index.

This file is a **routing aid**. It does not change repository authority. Canonical truth remains with the relevant source files and existing doctrine ([AGENTS.md](AGENTS.md), [docs/grace-mar-instance-boundary.md](docs/grace-mar-instance-boundary.md), [docs/operator-dashboards.md](docs/operator-dashboards.md)).

## Core routing table

| User asks for… | Search these paths first |
|---|---|
| analyst / speaker / commentator **source index** | [statecraft/civ-lens/INDEX.md](statecraft/civ-lens/INDEX.md), `statecraft/civ-lens/**/**-source-index.md` |
| Barnes / Robert Barnes | [statecraft/civ-lens/barnes/](statecraft/civ-lens/barnes/), `source-archive/statecraft/**/source-*barnes*` |
| Daniel Davis / Davis host | [statecraft/hosts/davis/](statecraft/hosts/davis/) |
| Napolitano / Judging Freedom | [statecraft/hosts/napolitano/](statecraft/hosts/napolitano/) |
| Nima / Dialogue Works | [statecraft/hosts/nima/](statecraft/hosts/nima/), [codex/speakers/nima/](codex/speakers/nima/) for stream + source-index |
| transcript / capture / source file | [source-archive/statecraft/](source-archive/statecraft/) |
| archive inventory by thread (counts, coverage) | [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) — **generated inventory**, not a route map |
| daily statecraft synthesis | [statecraft/daily/](statecraft/daily/) — **after** archive + source-index |
| host-family continuity (Davis, Napolitano, Nima, …) | [statecraft/hosts/](statecraft/hosts/) |
| statecraft lane / active operator work | [statecraft/](statecraft/) |
| library / reading / canon / books | [self-library.md](self-library.md), [artifacts/library-index.md](artifacts/library-index.md) |
| SELF / SKILLS / EVIDENCE / Record | `self.md`, `self-skills.md`, `self-archive.md`, `recursion-gate.md` |
| generated dashboard / derived operator surface | [artifacts/](artifacts/) |
| local semantic / vector index | [scripts/index_record.py](scripts/index_record.py), local `.chroma` paths |
| **source-lattice** / corpus tiers / reading order | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |
| PH chapter lattice / civ-* reading order | [statecraft/civ-lens/jiang/ph-civ/docs/source-lattice.md](statecraft/civ-lens/jiang/ph-civ/docs/source-lattice.md) |
| wire / official primary (live seam) | [docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md](docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md), `wire verify` skill |
| legacy codex speaker shelf | [codex/speakers/](codex/speakers/) — **compatibility only**; prefer civ-lens |
| machine-readable route registry | [repo-map.yaml](repo-map.yaml) |
| civ-lens shelf-class doctrine | [statecraft/civ-lens/README.md](statecraft/civ-lens/README.md) |
| speaker cluster / satellite map | [statecraft/civ-lens/speaker-cluster-map.md](statecraft/civ-lens/speaker-cluster-map.md) |
| expert profile (canonical shelf) | `statecraft/civ-lens/<speaker>/<speaker>-profile.md` — see [civ-lens README § Speaker profile law](statecraft/civ-lens/README.md#speaker-profile-law) |
| expert profile (legacy / profile-only) | [codex/profiles/](codex/profiles/) — compatibility, profile-only lanes, or pre-migration redirects; see [codex/profiles/README.md](codex/profiles/README.md) |
| host profile (canonical) | `statecraft/hosts/<host>/<host>-profile.md` |

## Parallel index disambiguation

Several surfaces use the word **index**. They are not interchangeable.

| Surface | Job | Authority |
|---|---|---|
| `statecraft/civ-lens/**/**-source-index.md` | Per-analyst **route map** — which captures to open first | WORK only |
| [statecraft/civ-lens/INDEX.md](statecraft/civ-lens/INDEX.md) | Front door listing all analyst source indexes | WORK routing aid |
| [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) | Generated capture **inventory** by thread | Derived / archive |
| [self-library.md](self-library.md) | Canonical SELF-LIBRARY reference layer | Canonical reference |
| [artifacts/library-index.md](artifacts/library-index.md) | Derived SELF-LIBRARY **dashboard** | Derived |
| [scripts/index_record.py](scripts/index_record.py) | Local Chroma / Record vector index builder | Derived local |
| [codex/speakers/](codex/speakers/) | Legacy speaker storage during migration | Compatibility |
| [statecraft/civ-lens/speaker-cluster-map.md](statecraft/civ-lens/speaker-cluster-map.md) | Anchor-and-satellite routing after Pape/Ritter/Parsi/Crooke | WORK routing aid |
| `statecraft/civ-lens/<speaker>/<speaker>-profile.md` | Per-speaker identity, voice fingerprint, pairing hub | WORK only (migrated SSOT) |
| [codex/profiles/*-profile.md](codex/profiles/) | Profile-only lanes or pre-migration compatibility | Compatibility / profile-only |

**Do not** answer "no Barnes index" because `library-index.md` or GitHub code search returned zero hits.

## Source index vs source-lattice

| Term | Question | Where |
|---|---|---|
| **source-index** | *Where* is the corpus? Which file opens first? | civ-lens `*-source-index.md` |
| **source-lattice** | *How* should layers be read so summary does not replace source? | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |

**Find-then-read contract:**

1. **Find** — this file → civ-lens source-index → `source-archive/`
2. **Read** — source-lattice doctrine (corpus tiers 1–4 + reading layers); PH chapters → `ph-civ/docs/source-lattice.md`
3. **Block** — tier-4 commentary cannot substantiate tier-3 claims without wire receipts

"Barnes **index**" is a location query. "Source-**lattice**" is a reading-discipline query.

## Search command convention

- **Interactive / in-repo search:** prefer `rg` (ripgrep) when available. Cursor agents: use ripgrep-backed workspace search.
- **Committed scripts, CI examples, and portable docs:** prefer `grep`, or `rg` with `grep -R` fallback when `rg` is not installed.
- **Zero hits are not proof of absence:** `grep`, `rg`, and GitHub code search can all miss indexed surfaces. Consult this routing map and the likely path family before answering "not found."

## Required search protocol

For any request of the form "find X in this repo":

1. If the user supplied an exact path or URL, fetch that path first.
2. Search exact term, lowercase term, and likely titlecase term.
3. Check this routing map and [repo-map.yaml](repo-map.yaml) before concluding absence.
4. If the query names an analyst, speaker, source corpus, or transcript set, inspect [statecraft/civ-lens/](statecraft/civ-lens/) and [source-archive/statecraft/](source-archive/statecraft/).
5. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a search miss, not proof of absence.
6. Do not answer "not found" until the relevant path family has been checked.
7. After locating a capture, apply find-then-read (source-lattice) before synthesis or judgment-bearing output.
