# Raw-Input Ownership vs Speaker Arc

WORK only; not Record.

This note distinguishes two nearby but different questions:

- **who owns the raw-input capture?**
- **what recurring host x guest form deserves a speaker arc later?**

They are related, but they are not the same object and should not be decided by the same rule.

## Short rule

- **raw-input ownership** decides where one capture belongs when it first enters the notebook
- **speaker arc** decides whether a repeated host x guest run has become a reusable host-local form

Do not use speaker-arc logic to name a raw-input file.
Do not use raw-input ownership logic to decide whether a speaker arc exists.

## Raw-input ownership

Raw-input ownership is an **ingest** decision.

Its job is to answer:

- what lane should own this file on disk?
- what should come first in the filename?
- what should `thread:` point to?

That decision is about **memory ownership**.

Examples:

- `Diesen x Freeman` on the Diesen channel -> **host-first**
- `Mario Nawfal x Pape` on an outside channel -> **expert-first**
- outside-channel `Ritter` interview -> usually **Ritter-first**

The point is to keep the file attached to the lane that actually owns the notebook memory.

## Speaker arc

A speaker arc is a **routing and interpretation** object built later.

Its job is to answer:

- why does this recurring host x guest run matter?
- which episodes anchor it?
- where should the operator open first?

That decision is about **host-conditioned conversational form**.

A speaker arc stays:

- host-local
- stream-local
- downstream of raw-input accumulation

## Why they can diverge

One capture can be owned by an expert lane at raw-input time and still never produce a speaker arc.

That happens when:

- the outside host is only a container
- the guest lane is the real notebook owner
- but there is no recurring host-local run worth compressing into an arc

Likewise, a designated host stream can own the raw-input and later produce a speaker arc because the same host x guest shape keeps returning.

So the two decisions are different:

- **raw-input ownership** asks: where does this file belong now?
- **speaker arc** asks: has this recurring host x guest contour become a reusable notebook object?

## Practical boundary

Ask these in order:

1. **Ingest question:** who owns this capture on disk?
2. **Later routing question:** has a repeated host-local run become strong enough for a speaker arc?

If you reverse those questions, the notebook starts to blur:

- filenames start teaching the wrong owner
- speaker arcs start getting inferred from single captures
- outside-channel guest appearances get mistaken for host-local forms

## Clean examples

- [youtube-pape-mario-nawfal-trump-s-next-iran-steps-revealed-2026-05-12.md](../../../codex/years/2026/raw-input/2026-05-12/youtube-pape-mario-nawfal-trump-s-next-iran-steps-revealed-2026-05-12.md)
  - raw-input ownership: **Pape-first**
  - no speaker arc implied by that fact alone

- [transcript-diesen-freeman-maritime-dominance-strait-of-hormuz-2026-05-06.md](../../../codex/years/2026/raw-input/2026-05-06/transcript-diesen-freeman-maritime-dominance-strait-of-hormuz-2026-05-06.md)
  - raw-input ownership: **Diesen-first**
  - later supports [diesen-freeman-speaker-arc.md](../../../codex/years/2026/diesen/diesen-freeman-speaker-arc.md) because the recurring host-local run is real

## Bottom line

**Raw-input ownership protects the right shelf.**

**Speaker arc protects the right recurring form.**

They should reinforce each other, but they should never be collapsed into one rule.
