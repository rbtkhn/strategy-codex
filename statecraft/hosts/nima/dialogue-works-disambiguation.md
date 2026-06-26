WORK only; not Record.

# Dialogue Works disambiguation (alkorshid / nima / venue)

Purpose: route **Dialogue Works** (venue) vs **Nima Alkorshid** (person) vs legacy **`alkorshid`** / **`nima`** naming — Diesen parity for archive ingest, indices, and synthesis titles.

## Compat matrix

| Layer | Value | Role |
|-------|--------|------|
| Archive person thread | **`alkorshid`** | ingest, indices, dual `threads` on every appearance |
| Host shelf | **`hosts/nima/`** | Dialogue Works **host-law** only — not whole-speaker index |
| Voices shelf | **`voices/alkorshid/`** | **All appearances** source-index (Diesen parity) |
| MCQ / EOD `expert_id` | **`nima`** (compat) | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) |
| Script read aliases | `alkorshid`, `alkhorshid`, `nima alkhorshid` | one release cycle after rename ship |
| Deprecated archive thread | **`thread:nima`** | replace with **`thread:alkorshid`** on new/edited captures |

## Venue vs person channel (Diesen parity)

| | Glenn Diesen | Nima Alkorshid |
|---|--------------|----------------|
| YouTube channel / show | **Glenn Diesen** (person-named) | **Dialogue Works** (show-named) |
| Own-channel filename | `source-glenn-diesen-<guest>-*` | `source-dialogue-works-<guest>-*` |
| Wrong own-channel prefix | `source-diesen-*` | `source-dialogue-works-*` / `source-nima-*` |
| `channel_slug` | `glenn-diesen` | `dialogue-works` |
| `host` YAML on own show | Glenn Diesen | Nima Alkorshid |
| Person thread (host + guest) | `diesen` | `alkorshid` |

## Target routing

| Role | Filename | `threads` | Title |
|------|----------|-----------|-------|
| DW interview | `source-dialogue-works-<guest>-*` | `[alkorshid, guest]` | **Dialogue Works × Guest** |
| DW solo | `source-dialogue-works-<slug>-*` | `[alkorshid]` | **Dialogue Works** |
| Guest on Mario Nawfal | `source-mario-nawfal-alkorshid-*` | `[nawfal, alkorshid]` | **Mario Nawfal × Alkorshid** |
| Guest on Daniel Davis | `source-daniel-davis-alkorshid-*` | `[davis, alkorshid]` | **Daniel Davis × Alkorshid** |

## Venue-first titles (synthesis)

**Venue channel name first:** `Dialogue Works × Johnson`, `Daniel Davis × Alkorshid`, `Mario Nawfal × Alkorshid`.

Wrong: `Johnson × Alkorshid`, `Alkhorshid Johnson`, `Guest × Nima / Dialogue Works`.

Full channel display names: **Daniel Davis**, **Mario Nawfal**, **Judging Freedom** (not bare Napolitano/Nawfal/Deep Dive).

## Shelf division

| Surface | Owns |
|---------|------|
| [nima-host-law.md](nima-host-law.md) | DW host transformation, lane map pointers |
| [voices/alkorshid/alkorshid-source-index.md](../../voices/alkorshid/alkorshid-source-index.md) | All appearances index |

## Script touchpoints

| Script | Change |
|--------|--------|
| [audit_dialogue_works_alkorshid.py](../../../scripts/audit_dialogue_works_alkorshid.py) | Phase 0 role audit |
| [normalize_dialogue_works_opening_scaffold.py](../../../scripts/normalize_dialogue_works_opening_scaffold.py) | `is_dialogue_works_capture` — require `channel_slug: dialogue-works` |
| [post_land_dialogue_works_opening_normalize.py](../../../scripts/post_land_dialogue_works_opening_normalize.py) | same guard |
| [build_two_pillar_notebook_graph.py](../../../scripts/build_two_pillar_notebook_graph.py) | `host_thread`: `alkorshid` (+ `nima` read alias) |
| [build_speaker_routing_queue.py](../../../scripts/build_speaker_routing_queue.py) | route `alkorshid` thread |
| [cognition_streams_audit.py](../../../scripts/cognition_streams_audit.py) | verify `alkorshid` token |
| [backfill_nima_youtube_raw_input.py](../../../scripts/backfill_nima_youtube_raw_input.py) | doc note: targets `@dialogueworks01`, not thread rename |

## Intake guard (summary)

Apply Dialogue Works normalize / `source-dialogue-works-*` prefix **only** when `channel_slug: dialogue-works` (or filename already `source-dialogue-works-*` with matching slug). Cross-host captures on Daniel Davis / Mario Nawfal use venue prefix + `alkorshid` in `threads`.

## Related

- [nima-host-law.md](nima-host-law.md)
- [diesen-source-index.md](../../voices/diesen/diesen-source-index.md) — exemplar index
- Audit artifacts: `statecraft/audits/dialogue-works-alkorshid-audit-*.csv`
