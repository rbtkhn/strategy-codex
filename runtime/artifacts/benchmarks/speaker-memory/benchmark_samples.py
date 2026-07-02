"""Shared strong/weak sample outputs for speaker-memory benchmark validation."""

from __future__ import annotations

SAMPLE_OUTPUTS = {
    "sm-1-speaker-object-repair": {
        "strong": """# Sachs speaker object

object_shape: cross-host-reinforced

## Object shape

Sachs is a cross-host-reinforced speaker object, not a mature helix.

## Open first

- open [Diesen x Sachs](/tmp/diesen-sachs.md)
- open [Sachs cross-host note](/tmp/sachs-cross-host-note.md)

## Routing use

Use this when deciding whether a new Sachs item strengthens the speaker object.

## Boundaries

- This is not raw-input provenance.
- This is not a biography.
- Do not treat Sachs as a wire-grade verifier.
- Do not claim a helix until denser host-local structure exists.
""",
        "weak": """# Sachs biography

Sachs is a famous public intellectual.

## Object shape

He is important.

## Boundaries

More research may be needed.
""",
    },
    "sm-2-speaker-arc-ranking": {
        "strong": """# Diesen x Freeman speaker arc

Purpose: host-local conversational form, not a generic Freeman profile.

## Why this guest run matters

Inside the Diesen stream, Diesen brings out Freeman's diplomatic-memory register.

## Arc set

1. [2026-05-06 maritime dominance](/tmp/2026-05-06.md)
   Best mature anchor.
2. [2026-04-18 Freeman Diesen](/tmp/2026-04-18.md)
   Best vocabulary anchor.

## Open first

Open 2026-05-06 first.

## Best paired read

Best paired read: [diesen-matlock-speaker-arc.md](/tmp/matlock.md).
Second-best paired read: [diesen-jiang-speaker-arc.md](/tmp/jiang.md).

## Routing use

Use this arc when lattice rows can cite the arc without carrying the interpretation themselves.

## Boundary

- Not a wire substitute.
- Not a fleet fact source.
- Not cargo arithmetic.
- Not blockade verification.
- Not ORBAT.
- Not a generic Freeman profile.
""",
        "weak": """# Freeman profile

## Arc set

1. 2026-04-18
2. 2026-05-06

## Open first

Open the latest thing.

## Best paired read

None.

## Routing use

Put the interpretation in the lattice because the lattice is where this belongs.

## Boundary

Freeman is broadly useful.
""",
    },
    "sm-3-speaker-structure-metrics": {
        "strong": """Freeman is the strongest shelf in this comparison set because the structure is not only dense, but visibly complete and coherent.

| metric | score | note |
|---|---:|---|
| density | 5 | multi-host recurrence across host-local arcs and helix surfaces |
| completeness | 4 | most known appearances are materialized, though watch URL coverage is partial |
| coherence | 5 | README, object, routing, and helix surfaces agree |
| maturity | 5 | cross-year continuity and open-first routes survive extension |

Composite: 4.7

| evidence | value |
|---|---|
| host_lanes | 4 |
| materialized_transcripts | 23 |
| host-local arcs | 4 |
| helix_present | yes |
| cross-year note | yes |
| watch_url_coverage | partial |

Notes:
- Density is structured, not mere transcript pileup.
- The main gap is partial watch URL coverage.
""",
        "weak": """Freeman feels mature and complete.

Composite: 5

It is just better overall.
""",
    },
    "sm-4-speaker-maturity-ranking": {
        "strong": """Freeman comes out ahead because its density, completeness, coherence, and maturity all reinforce each other rather than merely piling up files.

| speaker | density | completeness | coherence | maturity | rank |
|---|---:|---:|---:|---:|---:|
| freeman | 5 | 4 | 5 | 5 | 1 |
| crooke | 4 | 4 | 5 | 4 | 2 |
| baud | 5 | 3 | 4 | 4 | 3 |
| armstrong | 3 | 4 | 4 | 4 | 4 |

Strongest shelf:
Freeman is the top-ranked shelf and wins because its helix-first structure is backed by cross-year continuity and stable host transformations.

Most instructive mismatch case:
Baud is dense but that density does not fully translate into maturity when completeness lags. Armstrong is a thinner but cleaner single-branch mature shelf that scores above its raw volume. Crooke remains a strong cross-host reinforced comparative object rather than an embryonic shelf.
""",
        "weak": """Baud is best.

All speakers always follow the same maturity law.
""",
    },
}
