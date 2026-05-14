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

- `profile-only` - a light orientation shelf, not yet a mature thread, stream, or helix
- `stream-native` - the main body of the object is one native cognition stream
- `stream-anchored` - one native stream is primary, but the object is less stream-native than depth-native
- `stream-anchored-with-cross-host-reinforcement` - one native stream remains primary, while guest appearances materially reinforce the object
- `cross-host-reinforced` - no thick native stream dominates; the object coheres through recurring cross-host usefulness
- `single-helix` - one host-local branch carries helix-like depth
- `double-helix` - two host-local branches are mature enough to read together
- `triple-helix` - three host-local branches are mature enough to read together
- `helix-first` - host transformation is the primary way to enter the object, even if the exact branch count is still being refined

The object shape is a routing claim. It should tell future agents whether to enter through a native stream, a profile, a helix, or a cross-host reinforcement note. It should not flatten host-local speaker arcs into one generic speaker theory.

Validate with:

```bash
python scripts/validate_speaker_objects.py
```
