WORK only; not Record.

# Statecraft Channels

Purpose: hold the canonical live **channel-family** continuity surfaces that belong to repo-root `statecraft/`.

**Folder rule:** one subdirectory per **`channel_slug`** on the [main channel-index roster](channel-index.md) ([`channel-index.json`](channel-index.json)). Archive `channel_slug` and shelf folder name must match.

This layer exists so live channel-law, channel-native routing pressure, and guest-lane classification no longer depend on retired `codex/speakers/<host>/...` paths for active statecraft work.

## Vertical stack (archive → voices → channels → states)

Read live work in this order when layers blur:

1. [`source-archive/statecraft/`](../../source-archive/statecraft/) — **Statecraft Archive** (verbatim sources)
2. [`statecraft/voices/`](../voices/) — **Statecraft Synthesis** (whole-analyst continuity)
3. [`statecraft/channels/`](../channels/) — host-conditioned **guest** transformation (not whole-analyst shelves)
4. [`statecraft/states/`](../states/) — **CIV-STATE** source-memory substrate

Do not flatten guest-on-host reads into `voices/` when host law changes retrieval posture.

## Canonical rule

- `statecraft/channels/<channel_slug>/` — one folder per main roster channel
- `statecraft/sheets/` — cross-host comparison notes and compact routing law
- `statecraft/voices/` — speaker-state identity, support spines, speaker-native routing
- Legacy **`codex/speakers/`** terminated — [codex-speakers-deprecated.md](../../docs/archive/codex-speakers-deprecated.md)

## Main roster (15 channels)

| `channel_slug` | Shelf | Watchlist | Notes |
| --- | --- | --- | --- |
| `alexander-mercouris` | [alexander-mercouris/](alexander-mercouris/README.md) | yes | Solo Mercouris channel; analyst SSOT → [voices/mercouris](../voices/mercouris/) |
| `dialogue-works` | [dialogue-works/](dialogue-works/README.md) | yes | Nima / Dialogue Works; [dialogue-works-channel-index.md](dialogue-works/dialogue-works-channel-index.md) |
| `daniel-davis` | [daniel-davis/](daniel-davis/README.md) | yes | Feasibility / settlement-room host law |
| `glenn-diesen` | [glenn-diesen/](glenn-diesen/README.md) | yes | Diesen channel; analyst SSOT → [voices/diesen](../voices/diesen/) |
| `judging-freedom` | [judging-freedom/](judging-freedom/README.md) | yes | Legal / constitutional / process pressure |
| `mario-nawfal` | [mario-nawfal/](mario-nawfal/README.md) | | Breaking-headline register (≠ Moral Resistance) · [mario-nawfal-channel-index.md](mario-nawfal/mario-nawfal-channel-index.md) |
| `the-duran` | [the-duran/](the-duran/README.md) | yes | Duran channel (Mercouris + Christoforou) |
| `india-global-left` | [india-global-left/](india-global-left/README.md) | | [india-global-left-channel-index.md](india-global-left/india-global-left-channel-index.md) |
| `neutrality-studies` | [neutrality-studies/](neutrality-studies/README.md) | | Pascal Lottaz neutralist host frame · [neutrality-studies-channel-index.md](neutrality-studies/neutrality-studies-channel-index.md) |
| `predictive-history` | [predictive-history/](predictive-history/README.md) | | Operator PH YouTube (≠ `codex/predictive-history/` book) · [predictive-history-channel-index.md](predictive-history/predictive-history-channel-index.md) |
| `breaking-points` | [breaking-points/](breaking-points/README.md) | | [breaking-points-channel-index.md](breaking-points/breaking-points-channel-index.md) |
| `tucker-carlson` | [tucker-carlson/](tucker-carlson/README.md) | | [tucker-carlson-channel-index.md](tucker-carlson/tucker-carlson-channel-index.md) |
| `reason-resist` | [reason-resist/](reason-resist/README.md) | | **Host-only:** Dimitri Lascaris = channel law, not a voice shelf — [reason-resist-channel-index.md](reason-resist/reason-resist-channel-index.md); no `lascaris-index`; guests → [voices/](../voices/) |
| `redacted-news` | [redacted-news/](redacted-news/README.md) | yes | [redacted-news-channel-index.md](redacted-news/redacted-news-channel-index.md) |
| `moral-resistance` | [moral-resistance/](moral-resistance/README.md) | | Sulaiman Ahmed; MOU / legislative-action lane · [moral-resistance-channel-index.md](moral-resistance/moral-resistance-channel-index.md) |

Low-volume channels: [channel-index-misc.md](channel-index-misc.md) (misc roster — add shelves when promoted).

## Channel index (SSOT)

- [channel-index.md](channel-index.md) — human roster + stats (regenerated from archive captures)
- [channel-index.json](channel-index.json) — machine roster for **check-sources**
- [channel-index-misc.md](channel-index-misc.md) — low-volume channels excluded from main roster

## High-leverage host orthogonality

[Davis](daniel-davis/README.md) and [Napolitano](judging-freedom/README.md):

- **Daniel Davis** — feasibility, bargaining geometry, settlement-room pressure
- **Judging Freedom** — legal, constitutional, process pressure

Shared comparison: [host-backbone-napolitano-davis-orthogonality-2026-05.md](../sheets/host-backbone-napolitano-davis-orthogonality-2026-05.md).

## What belongs here

- channel front doors (`README.md`, `index.md`)
- host-law notes
- host identity profiles when the live channel shelf is canonical here
- host-native guest-lane maps — **canonical arc bodies** in [`statecraft/notes/`](../notes/README.md) (`arc-<guest>-<host>-host.md`); channel root keeps **compat redirects** only (e.g. `davis-<guest>-arc.md`)
- live routing distinctions that apply across multiple speaker shelves

## Flat shelf law

**Effective 2026-06:** every channel shelf root is **flat**.

- `statecraft/channels/<channel_slug>/` contains **files only** — no subdirectories under a channel folder.
- Guest-lane arc **redirects**, host monthly shelves, and host wiring surfaces live as sibling files at the channel root; arc **bodies** → `statecraft/notes/`.
- Legacy `channels/<slug>/stream/` is **terminated**.

See also [`statecraft/voices/README.md` § Flat shelf law](../voices/README.md#flat-shelf-law).

## What does not belong here

- raw transcript authority
- lane judgment
- speaker-native month ladders
- new live doctrine in `codex/`

## Boundary

Use this layer when the real question is how a **channel** changes a guest, not when the real question is whole-speaker identity or raw-source chronology.

## Intake law

`Statecraft Archive → Statecraft Synthesis → channel / host law → bridge if needed → lane drafting`

Open the **`channel_slug`** shelf matching capture frontmatter before jumping to helix, state, or bridge splits when the bottleneck is still transcript-conditioned reading.

## Maintenance

Align shelves to index: `python scripts/align_channel_shelves_to_index.py` (after `channel-index.json` changes).
