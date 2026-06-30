# LLM Routing Map

> **Machine routing SSOT.**
> Not a human onboarding surface.


This repository contains multiple index and source surfaces. Do not rely only on GitHub code search when asked to find a file, source corpus, analyst, speaker, dashboard, or index.

This file is a **routing aid**. It does not change repository authority. Canonical truth remains with the relevant source files and existing doctrine ([AGENTS.md](../../AGENTS.md), [docs/archive/grace-mar.md](../../docs/archive/grace-mar.md), [docs/operator-dashboards.md](../operator-dashboards.md)).

**Routing hierarchy:** [README.md](README.md) → [docs/start-here.md](../start-here.md) → [repo-map.yaml](../../repo-map.yaml) → domain README. Detail: [docs/routing-reference.md](../routing-reference.md).

## Core routing shortcuts

| User asks for… | Search these paths first |
|---|---|
| analyst / speaker / commentator **source index** | [statecraft/voices/voice-index.md](../../statecraft/voices/voice-index.md), `statecraft/voices/**/**-source-index.md` |
| **archive day-index** / day source inventory for **YYYY-MM-DD** | **`source-archive/statecraft/YYYY-MM-DD/day-index.md` only** — or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD` — **do not** Glob/Grep month or thread-index for a dated day query |
| transcript / capture / source file | [source-archive/statecraft/](../../statecraft) |
| archive inventory by thread (counts, coverage) | [source-archive/statecraft/thread-index.md](../../source-archive/statecraft/thread-index.md) — **generated inventory**, not a route map |
| daily statecraft synthesis | [statecraft/synthesis/day/](../../statecraft/synthesis/day) — **after** archive + source-index |
| **statecraft note registry** / which notes exist / essay candidate / route integrity | [statecraft/notes/INDEX.md](../../statecraft/notes/INDEX.md) → [runtime/artifacts/statecraft-notes-registry.md](../../runtime/artifacts/statecraft-notes-registry.md) — **before** grepping `statecraft/notes/` |
| host-family continuity (Davis, Napolitano, Nima, …) | [statecraft/channels/](../../statecraft/channels) |
| **YouTube channel roster** / check-sources / `channel_slug` | [statecraft/channels/channel-index.json](../../statecraft/channels/channel-index.json) · [channel-index.md](../../statecraft/channels/channel-index.md) |
| statecraft lane / active operator work | [statecraft/](../../statecraft) |
| singularity lane / acceleration work | [singularity/](../../singularity) |
| **essay / stand-alone thesis** (cross-channel default) | [essays/README.md](../../essays/README.md) — primary shelf; channel `*/essays/` = compatibility only |
| **prose class** (note vs essay vs synthesis) | [docs/prose-index.md](../prose-index.md) |
| architecture / harness topology / model vs harness map | [docs/harness-architecture-map.md](../../docs/harness-architecture-map.md) |
| repository root layout / root crowding | [docs/root-directory-map.md](../../docs/root-directory-map.md) |
| **source-lattice** / corpus tiers / reading order | [docs/source-lattice-beyond-the-repo.md](../source-lattice-beyond-the-repo.md) |
| machine-readable route registry | [repo-map.yaml](../../repo-map.yaml) |
| Grace-Mar fork doctrine (archived) | [docs/archive/grace-mar.md](../../docs/archive/grace-mar.md) |
| frozen Record surfaces (fork revive only) | `archive/grace-mar-instance/` — not default operator work |

<!-- GENERATED:sections -->

## Parallel index disambiguation

Several surfaces use the word **index**. They are not interchangeable.

| Surface | Job | Authority |
|---|---|---|
| `source-archive/statecraft/YYYY-MM-DD/day-index.md` | **Day index** — channel / writer / other partitions for one archive day | Derived / archive (rebuild via `build_statecraft_day_indices.py`) |
| `source-archive/statecraft/YYYY-MM-DD/README.md` | **Day README stub** — pointer to `day-index.md` only | Derived / archive |
| `statecraft/voices/**/**-source-index.md` | Per-analyst **route map** — which captures to open first | WORK only |
| [statecraft/voices/voice-index.md](../../statecraft/voices/voice-index.md) | Front door listing all analyst source indexes | WORK routing aid |
| [source-archive/statecraft/thread-index.md](../../source-archive/statecraft/thread-index.md) | Generated capture **inventory** by thread | Derived / archive |
| [archive/grace-mar-instance/self-library.md](../../archive/grace-mar-instance/self-library.md) | Canonical removed operator-books symlink reference layer | Canonical reference |
| [runtime/artifacts/library-index.md](../../runtime/artifacts/library-index.md) | Derived removed operator-books symlink **dashboard** | Derived |
| [scripts/index_record.py](../../scripts/index_record.py) | Local Chroma / Record vector index builder | Derived local |
| [docs/archive/codex-speakers-deprecated.md](../archive/codex-speakers-deprecated.md) | Tombstone for terminated `codex/speakers/` | Archive |
| [statecraft/channels/](../../statecraft/channels) | Host-family continuity (Davis, Napolitano, Nima / Dialogue Works) | WORK only |
| [statecraft/channels/channel-index.json](../../statecraft/channels/channel-index.json) | **YouTube channel roster** (main) — check-sources SSOT; human: [channel-index.md](../../statecraft/channels/channel-index.md) | Derived from archive; rebuild via `refresh_statecraft_archive_indices.py` |
| [statecraft/voices/speaker-cluster-map.md](../../statecraft/voices/speaker-cluster-map.md) | Anchor-and-satellite routing after Pape/Ritter/Parsi/Crooke | WORK routing aid |
| `statecraft/voices/<speaker>/<speaker>-profile.md` | Per-speaker identity, voice fingerprint, pairing hub | WORK only (migrated SSOT) |
| [codex/profiles/*-profile.md](../../codex/profiles) | Profile-only lanes or pre-migration compatibility | Compatibility / profile-only |

**Essays vs channel essay folders vs notes:**

| Surface | Job | Authority |
|---|---|---|
| [essays/README.md](../../essays/README.md) | **Primary** stand-alone / cross-channel theses | WORK prose shelf |
| `statecraft/notes/` · `singularity/notes/` | Channel-scoped bounded interpretive objects | WORK prose shelf |
| `statecraft/essays/` · `singularity/essays/` | Pre-root **compatibility** essay holdings | Stubs → `essays/` |
| [docs/prose-index.md](../prose-index.md) | Note vs essay vs synthesis class chooser | WORK routing aid |

**Do not** answer "no Barnes index" because `library-index.md` or GitHub code search returned zero hits.

## Source index vs source-lattice

| Term | Question | Where |
|---|---|---|
| **source-index** | *Where* is the corpus? Which file opens first? | voices `*-source-index.md` for **analyst** scope; **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** for **one archive day** |
| **source-lattice** | *How* should layers be read so summary does not replace source? | [docs/source-lattice-beyond-the-repo.md](../source-lattice-beyond-the-repo.md) |

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
3. Check this routing map and [repo-map.yaml](../../repo-map.yaml) before concluding absence.
4. If the query names an analyst, speaker, source corpus, or transcript set, inspect [statecraft/voices/](../../statecraft/voices) and [source-archive/statecraft/](../../statecraft).
5. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a search miss, not proof of absence.
6. Do not answer "not found" until the relevant path family has been checked.
7. After locating a capture, apply find-then-read (source-lattice) before synthesis or judgment-bearing output.
