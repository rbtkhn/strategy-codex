
# Dialogue Works disambiguation (alkorshid / nima / venue)

Purpose: route **Dialogue Works** (venue) vs **Nima Alkhorshid** (person) vs legacy **`alkhorshid`** / **`nima`** naming — Diesen parity for archive ingest, indices, and synthesis titles.

## Display spelling (canonical)

| Layer | Spelling |
|-------|----------|
| **Display name** (`host:` YAML, speaker labels, operator prose, synthesis person leg) | **Nima Alkhorshid** (surname **Alkhorshid** — with **h**) |
| **Machine id** (`thread`, path slug `voices/alkorshid/`, filename token `*-alkorshid-*`) | **`alkhorshid`** (no **h**; script read aliases `alkhorshid`, `nima alkhorshid`) |
| **Wrong display** | `Nima Alkhorshid` / bare `Alkorshid` — fix on edit; do not use on new intake |
| **Verbatim ASR in archive body** | preserve guest mis-hearings (`Nema`, `Nemo these`, etc.) unless manual ASR spot-fix |

## Compat matrix

| Layer | Value | Role |
|-------|--------|------|
| Archive person thread | **`alkhorshid`** | ingest, indices, dual `threads` on every appearance |
| Host shelf | [`channels/dialogue-works/`](README.md) | Dialogue Works **host-law**, thread, arcs, channel index |
| Voices shelf | [`voices/alkorshid/`](../../voices/alkorshid/README.md) | **Alkhorshid** analyst profile + cross-host guest index |
| MCQ / EOD `expert_id` | **`nima`** (compat) | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) |
| Script read aliases | `alkhorshid`, `alkhorshid`, `nima alkhorshid` | one release cycle after rename ship |
| Deprecated archive thread | **`thread:nima`** | replace with **`thread:alkhorshid`** on new/edited captures |

## Venue vs person channel (Diesen parity)

| | Glenn Diesen | Nima Alkhorshid |
|---|---|--------------|----------------|
| YouTube channel / show | **Glenn Diesen** (person-named) | **Dialogue Works** (show-named) |
| Own-channel filename | `source-glenn-diesen-<guest>-*` | `source-dialogue-works-<guest>-*` |
| Wrong own-channel prefix | `source-diesen-*` | `source-dialogue-works-*` / `source-nima-*` |
| `channel_slug` | `glenn-diesen` | `dialogue-works` |
| `host` YAML on own show | Glenn Diesen | Nima Alkhorshid |
| Person thread (host + guest) | `diesen` | `alkhorshid` |

## Target routing

| Role | Filename | `threads` | Title |
|------|----------|-----------|-------|
| DW interview | `source-dialogue-works-<guest>-*` | `[alkorshid, guest]` | **Dialogue Works × Guest** |
| DW solo | `source-dialogue-works-<slug>-*` | `[alkorshid]` | **Dialogue Works** |
| Guest on Mario Nawfal | `source-mario-nawfal-alkorshid-*` | `[nawfal, alkorshid]` | **Mario Nawfal × Alkhorshid** |
| Guest on Daniel Davis | `source-daniel-davis-alkorshid-*` | `[davis, alkorshid]` | **Daniel Davis × Alkhorshid** |

## Venue-first titles (synthesis)

**Venue channel name first:** `Dialogue Works × Johnson`, `Daniel Davis × Alkhorshid`, `Mario Nawfal × Alkhorshid`.

Wrong: `Johnson × Alkorshid`, `Alkorshid Johnson`, `Guest × Nima / Dialogue Works` (missing **h**, person-first, or bare first name).

Full channel display names: **Daniel Davis**, **Mario Nawfal**, **Judging Freedom** (not bare Napolitano/Nawfal/Deep Dive).

## Shelf division

| Surface | Owns |
|---------|------|
| [nima-host-law.md](nima-host-law.md) | DW host transformation, lane map pointers |
| [dialogue-works-channel-index.md](dialogue-works-channel-index.md) | Dialogue Works channel route map (`source-dialogue-works-*`) |

## Script touchpoints

| Script | Change |
|--------|--------|
| [audit_dialogue_works_alkhorshid.py](../../../scripts/audit_dialogue_works_alkhorshid.py) | Phase 0 role audit |
| [normalize_dialogue_works_opening_scaffold.py](../../../scripts/normalize_dialogue_works_opening_scaffold.py) | `is_dialogue_works_capture` — require `channel_slug: dialogue-works` |
| [post_land_dialogue_works_opening_normalize.py](../../../scripts/post_land_dialogue_works_opening_normalize.py) | same guard |
| [build_two_pillar_notebook_graph.py](../../../scripts/build_two_pillar_notebook_graph.py) | `host_thread`: `alkhorshid` (+ `nima` read alias) |
| [build_voice_routing_queue.py](../../../scripts/build_voice_routing_queue.py) | route `alkhorshid` thread |
| [cognition_streams_audit.py](../../../scripts/cognition_streams_audit.py) | verify `alkhorshid` token |
| [backfill_nima_youtube_raw_input.py](../../../scripts/backfill_nima_youtube_raw_input.py) | doc note: targets `@dialogueworks01`, not thread rename |
| [fix_statecraft_common_asr_entities.py](../../../scripts/fix_statecraft_common_asr_entities.py) | labels `nima_alkhorshid_*` — meta/titles/speaker labels on sweep |
| [audit_dialogue_works_alkhorshid.py](../../../scripts/audit_dialogue_works_alkhorshid.py) | `spelling:` flags + `--fail-on-spelling` guardrail |

## Intake guard (summary)

Apply Dialogue Works normalize / `source-dialogue-works-*` prefix **only** when `channel_slug: dialogue-works` (or filename already `source-dialogue-works-*` with matching slug). Cross-host captures on Daniel Davis / Mario Nawfal use venue prefix + `alkhorshid` in `threads`.

## Related

- [nima-host-law.md](nima-host-law.md)
- [diesen-index.md](../../voices/diesen/diesen-index.md) — exemplar guest-only voice index (host → channel shelf)
- Audit artifacts: `statecraft/audits/dialogue-works-alkhorshid-audit-*.csv`
