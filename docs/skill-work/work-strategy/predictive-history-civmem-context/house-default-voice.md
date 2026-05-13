# `house-default` voice doctrine for PH CIV-MEM context

This file defines the initial voice for rendered `CIV-MEM Context` blocks in a
future Predictive History implementation.

## Voice profile label

Active v1 profile:

- `house-default`

This label should be treated as a **rendering-layer choice**, not as a change to
the underlying CIV-MEM payload structure.

## Voice composition

`house-default` is a blended voice:

- **historical cartographer** as the primary base
- **civilizational guide** as the secondary tone
- **prophetic-historical** as a rare intensifier

Compressed ratio:

- 70% cartographer
- 25% guide
- 5% prophetic-historical lift

## What each layer contributes

### Historical cartographer

This provides:

- placement
- structure
- terrain
- orientation

Typical feel:

- where this unit sits
- what larger arc surrounds it
- what civilizational terrain is being crossed

### Civilizational guide

This provides:

- legibility
- reader companionship
- sentence warmth without sentimentality

Typical feel:

- helping the reader notice the right thing
- explaining why the frame matters
- keeping the block inviting rather than merely schematic

### Prophetic-historical

This should be used sparingly.

Its job is:

- to add resonance when the stakes truly warrant it
- to leave one memorable line when earned

It should **not** dominate the block or turn every unit into a fate-drenched
performance.

## Preferred sentence behavior

- open with placement, not drama
- keep the first sentence structurally clear
- prefer "where this sits" over "what this proves"
- use 2-4 sentence units that remain easy to scan
- let elevated phrasing appear only after the basic orientation is already
  clear

## Good elevation

Good elevation:

- sharpens the stakes
- makes the historical frame memorable
- still preserves clarity

Example pattern:

- "This lecture belongs to the long arc of imperial legitimacy under stress."

## Overreach

Overreach happens when the prose:

- sounds grander than the payload warrants
- implies more certainty than the evidence supports
- uses civilizational drama to hide weak fit
- turns every unit into a fate statement

Bad signs:

- too many sweeping metaphors
- dramatic certainty in a low-fit case
- context block sounding like manifesto rather than orientation

## Low-fit rendering rule

If `Fit strength` is `light`:

- reduce rhetorical weight
- keep the block narrower
- avoid prophetic lift unless absolutely necessary
- foreground limits honestly

Low fit should still feel meaningful, but not inflated.

## Future modulation

Future voice tuning should happen as a **rendering-layer change**.

Possible later profiles:

- `cool-analytic`
- `teacherly-clear`
- `elevated-civilizational`
- `hard-diagnostic`

The future implementer should be able to change the voice profile without
changing:

- payload fields
- heading structure
- block placement
- pack ownership of the payload

