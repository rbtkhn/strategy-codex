# Speakers

Speakers are higher-order strategy-codex objects outside the current eight-stream scaffold. They may carry speaker-arcs, speaker-helixes, cross-year notes, profiles, and other speaker-local materials without becoming first-class cognition streams in this volume.

Promote a speaker into the scaffold only by explicit operator decision.

WORK only; not Record.

## Speaker object contract

A speaker folder becomes a first-class speaker-object folder when it contains a `*-speaker-object.md` note. That note is an orientation and routing object, not a provenance ledger.

Each speaker-object note should include:

- `WORK only; not Record.`
- `## Object shape`
- `## Open first`
- `## Boundaries`
- one declared object shape, either as an explicit `object_shape: <shape>` line or in the prose of the Object shape section

Allowed object shapes:

- `profile-only`
- `stream-native`
- `stream-anchored`
- `stream-anchored-with-cross-host-reinforcement`
- `single-helix`
- `double-helix`
- `triple-helix`
- `helix-first`

The object shape is a routing claim. It should tell future agents whether to enter through a native stream, a profile, a helix, or a cross-host reinforcement note. It should not flatten host-local speaker arcs into one generic speaker theory.

Validate with:

```bash
python scripts/validate_speaker_objects.py
```
