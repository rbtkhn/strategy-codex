# CIV-MEM pack payload template

Use this as the **canonical structured payload** inside a future Predictive
History archive/placeholders/evidence/media pack.

The payload should be stable, compact, and independent from the exact voice used
for the visible context block.

## Payload fields

### Primary object

What kind of civilizational object is this unit fundamentally about?

Typical answers:

- empire under stress
- alliance system
- legitimacy regime
- church-state settlement
- founding narrative
- frontier/center tension
- elite formation system

Length: 1 short phrase or 1 sentence.

### Historical arc

What larger historical or civilizational arc does this lecture/chapter belong
to?

The arc should be specific enough to orient, but not so long that it becomes a
mini-essay.

Examples:

- late-imperial overstretch and loss of strategic flexibility
- religious legitimation inside declining hegemonic orders
- civilizational transition from founding vitality to bureaucratic sclerosis

Length: 1-2 sentences.

### Dominant slots

Which CIV-MEM lattice slots matter most here?

Choose 2-3 from:

- conditions
- institutions
- seams
- continuity / memory
- time structure
- decline / stress vectors

Each chosen slot should be paired with a short note, not just a label.

### Reader orientation

How should the reader enter this unit?

This field should tell the later rendered block what kind of attention to
solicit. It should answer questions like:

- read this as a structure-first lecture, not only a current-events commentary
- watch for how legitimacy and alliance strain are being linked
- notice how memory and institution are doing more work than immediate events

Length: 1-2 sentences.

### Fit strength

Required values:

- `strong`
- `medium`
- `light`

This field controls the eventual rhetorical weight of the rendered block.

### Mismatch / limit note

Optional but recommended whenever fit is not strong.

Use this to say where the CIV-MEM reading is partial, stretched, or
non-exhaustive.

Examples:

- the unit is more literary than civilizational, so the context should stay
  lighter
- the historical arc clarifies the background but does not explain the whole
  argument

Length: 1 sentence.

## Suggested pack section shape

```markdown
## CIV-MEM orientation

- **Primary object:** ...
- **Historical arc:** ...
- **Dominant slots:** ...
- **Reader orientation:** ...
- **Fit strength:** strong | medium | light
- **Mismatch / limit note:** ...   # optional
```

## Authoring rule

The pack owns the **payload**, not necessarily the final polished reader prose.
It may also store a draft rendered block if useful, but the stable conceptual
content should remain easy to reuse across multiple future surfaces.

