# Mountain Homestead — Strategic Plan

WORK only; not Record.

**Scope:** `operations/mountain-homestead/` operating system.

**One-line strategy:** The mountain homestead uses Singularity to become a risk-scored rural operating asset — every weekly task, monthly repair, and seasonal readiness action should reduce wildfire, continuity, access, water, septic, insurance, or infrastructure risk.

---

## Executive thesis

The homestead is managed as a **risk-first rural operating asset**, not a household chore list.

Operating model:

```text
asset protection
  → continuity
  → seasonal readiness
  → productive capacity
  → optional revenue
```

Core improvement: **risk register + seasonal readiness gate** that ranks threats by consequence, likelihood, urgency, and cost-to-reduce.

```text
weather / fire / access / utility signal
  → risk register
  → weekly ops card
  → maintenance backlog
  → seasonal readiness checklist
  → completed mitigation proof
  → insurance / asset-protection evidence
```

---

## Site

| Field | Value |
| --- | --- |
| Location | **Pine, Colorado** |
| Land | **5 acres** |
| Context | Rural mountain foothills — WUI wildfire-interface asset; seasonal access, snow, wildfire, drainage, and utility continuity are load-bearing |

Wildfire readiness is **core asset management**, not a seasonal side task. CSFS guidance: home ignition zone problem — structure ignitability and defensible space determine survival; ongoing maintenance required.

---

## Loop cluster

| Loop | Role |
| --- | --- |
| `mountain-homestead-ops` | Weekly ops card — starts with top 5 risk-reduction actions |
| `mountain-homestead-risk-register` | Monthly risk scoring and escalation |
| `mountain-homestead-maintenance` | Monthly infrastructure / capex / contractor backlog |
| `mountain-homestead-wildfire-mitigation-review` | Monthly ignition zone and defensible-space review |
| `mountain-homestead-utilities-continuity` | Monthly power, heat, water, comms 72-hour continuity |
| `mountain-homestead-water-systems-review` | Quarterly private well and water continuity |
| `mountain-homestead-septic-review` | Annual septic inspection/pump schedule |
| `mountain-homestead-seasonal-readiness` | Seasonal gate — fire, winter, mud, freeze, access |

See [`README.md`](README.md) for hard/soft dependency graph.

---

## Wildfire: home ignition zone

Defensible-space zones (per structure — house, garage, sheds, barns, decks):

```text
Zone 1: 0–5 feet from structures
Zone 2: 5–30 feet
Zone 3: 30–100 feet
```

Structural hardening checklist areas: Class A roof, gutter/deck/roof debris, 1/8-inch metal vent mesh, tempered/multi-pane windows, ground-to-siding clearance, combustible fencing within 5 feet.

Template: [`wildfire-mitigation/mitigation-proof-template.md`](wildfire-mitigation/mitigation-proof-template.md)

---

## Mitigation as insurance evidence

```text
mitigation action
  → before photo
  → contractor / owner work note
  → after photo
  → receipt / cost
  → zone affected
  → risk reduced
  → insurer / tax / resale evidence
```

Colorado wildfire-mitigation tax credit (2023–2027): mark expenses **possible / verify** only — check current Colorado Department of Revenue rules or a tax advisor before claiming eligibility.

---

## Risk scoring model

```text
priority_score = consequence × likelihood × urgency ÷ cost_to_reduce
```

Use 1–5 scores:

| Field | Meaning |
| --- | --- |
| Consequence | Damage if ignored |
| Likelihood | Probability in current season |
| Urgency | How soon action is needed |
| Cost-to-reduce | 1 = cheap/easy, 5 = expensive/hard |

Every weekly ops card starts with the **top 5 risk-reduction actions**, not the easiest chores.

Template: [`risk-register/risk-register-template.md`](risk-register/risk-register-template.md)

---

## Utilities: 72-hour continuity standard

Power, heat, water, communications, and access must survive a **72-hour** disruption window (winter storm → outage → heat loss → frozen pipes → cascading failure).

Template: [`utilities-continuity/72-hour-continuity-card.md`](utilities-continuity/72-hour-continuity-card.md)

Multi-hazard planning — do not optimize for wildfire only.

---

## Water (private well)

Private well owners are responsible for safe drinking water. Formal operating asset, not casual maintenance.

Checklist: [`water-systems/water-system-checklist.md`](water-systems/water-system-checklist.md)

---

## Septic

Preventive maintenance is cheaper than failure. Inspect every ~3 years; pump every 3–5 years; alternative systems may need annual inspection.

Rule: **do not wait for symptoms** — septic failure is a capex event.

Checklist: [`septic/septic-review-checklist.md`](septic/septic-review-checklist.md)

---

## Access

Driveway, turnaround, gate, address visibility, snow/mud access, and evacuation routes affect firefighter entry, EMS, contractors, and insurance perception.

Checklist: [`access/access-readiness-checklist.md`](access/access-readiness-checklist.md)

Review monthly in winter/fire season; quarterly otherwise (via weekly ops).

---

## 30-day operating plan

### Week 1 — Asset and risk inventory

Goal: make the property legible.

1. List all structures and critical systems
2. Create first risk register
3. Create first weekly ops card

Output: `risk-register/monthly/2026-07.md`

### Week 2 — Wildfire mitigation baseline

Goal: home ignition zone baseline.

1. Walk Zone 1 / 2 / 3 around every structure
2. Photograph ember traps (gutters, decks, vents, fences, wood piles)
3. Rank top 10 mitigation actions

Output: `wildfire-mitigation/2026-baseline.md`

### Week 3 — Utilities continuity baseline

Goal: prevent cascading failures.

1. Test backup power or record gap
2. Map power-outage failure chains
3. Create 72-hour continuity card

Output: `utilities-continuity/2026-baseline.md`

### Week 4 — Water / septic / access baseline

Goal: reduce hidden infrastructure risk.

1. Record water test and septic history
2. Review driveway, turnaround, evacuation routes
3. Produce first monthly maintenance report

Output: `maintenance/monthly-reports/2026-07.md`

---

## Weekly homestead scorecard

| Metric | Target | Why |
| --- | ---: | --- |
| Top 5 risks reviewed | weekly | Consequence-first attention |
| Zone 1 ignition hazards unresolved | 0 | Highest wildfire leverage |
| Gutter/deck/roof debris status | clear before fire season | Ember reduction |
| Backup power test | monthly / pre-storm | Continuity |
| Freeze-prone line review | monthly in cold season | Pipe protection |
| Water test status | current | Health and asset value |
| Septic inspection/pump status | current | Capex prevention |
| Access / driveway issues | reviewed monthly | Fire/EMS/contractor access |
| Insurance / mitigation proof notes | updated after work | Documentation |
| Contractor backlog reviewed | monthly | Prevents deferred-maintenance drift |

See also [`ops/README.md`](ops/README.md).
