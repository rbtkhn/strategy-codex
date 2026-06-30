# Predictive History Tolstoy Lens Upstream Notes
<!-- word_count: 351 -->

<!-- Academy note
academy_origin: true
created_at: 2026-05-16
source_context: rbtkhn/predictive-history@1dbab13d1288e1d54c2904ea75d8f7a5e4ed529f
intended_use: upstream_deepening_notes
boundary: WORK only; not Record; not a Predictive History edit
-->

**Purpose:** Hold candidate notes that could later help Predictive History evolve the Tolstoy Lens from actor-pressure causation into actor-pressure-conscience causation where appropriate.

## Current Upstream Baseline

Predictive History already has:

- `docs/tolstoy-lens.md`: the bounded commentary standard.
- `docs/predictive-history-after-tolstoy.md`: front-door essay on pressure reading after Tolstoy.
- `corpus/cross-volume/tolstoy-question.md`: routed actor-pressure corridor.
- `registries/causation-lenses.yaml`: source-of-truth registry for where the lens may appear.

The existing standard is good because it blocks three bad moves:

- great-man simplification
- impersonal determinism
- using system pressure to erase moral responsibility

The academy-theology opportunity is to add a fourth protection:

- theological overreach, where sacred pressure is mistaken for divine authorization or fate

## Suggested Upstream Addition

Add a compact section to `docs/tolstoy-lens.md` after "Voice Rules" or before "Acceptance Standard":

```md
## Theological Pressure

Some pressure fields are sacred, moral, or eschatological rather than merely institutional or material. In those cases, the lens may name theological pressure, but it must not convert pressure into providence.

Ask what sacred story, doctrine, ritual memory, conscience, or eschatological horizon made action historically legible. Then state the boundary: this does not make the action divinely authorized, morally innocent, or inevitable.
```

Then add one acceptance bullet:

```md
- when sacred pressure is active, distinguishes theological pressure from providential claim
```

And one voice rule:

```md
- Do not treat sacred pressure as divine endorsement.
```

## Registry-Level Option

If the registry grows, add optional fields only where needed:

```yaml
theological_pressure:
  - messianic expectation
  - sacred history
  - eschatological mobilization
theology_boundary: "Name the pressure without making a providential claim."
```

Do not require these fields for every lens. Most Tolstoy Lens entries should remain ordinary actor-pressure entries.

## First Candidate Nodes

| Source | Why it fits | Theological-pressure addition |
|---|---|---|
| `civ-25` | Paul is already framed through messianic expectation and doctrinal portability. | Distinguish movement portability from theological truth-claim. |
| `civ-53` | Dostoevsky is already framed through Orthodoxy, conscience, guilt, and inner necessity. | Clarify conscience as pressure without reducing Russia to literature or theology. |
| `gt-22` | The nation-state entry already names eschatological mobilization and sacred history. | Separate eschatological pressure from deterministic collapse prophecy. |

## What Not To Do

- Do not make the Tolstoy Lens a theology doctrine.
- Do not imply Predictive History is now "Tolstoy plus providence."
- Do not add theological-pressure fields to every actor.
- Do not weaken existing representation-not-endorsement language.
- Do not use this to decide live political questions without source review.

## Short Form

The upstream contribution can be as simple as:

> The Tolstoy Lens can name sacred pressure, but it should not make providential claims. Sacred pressure can make action historically legible without making it divinely authorized, morally innocent, or inevitable.
