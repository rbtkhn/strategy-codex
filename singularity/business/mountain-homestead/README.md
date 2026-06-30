# Mountain homestead — business operating shelf

WORK only; not Record.

Mountain homestead business operating shelf. Treat the 5-acre Pine, Colorado property as a **risk-first rural operating asset**: land + infrastructure + production capacity + risk management + optional revenue.

**Strategic plan (operating SSOT):** [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md)

## Site

| Field | Value |
| --- | --- |
| Location | **Pine, Colorado** |
| Land | **5 acres** |
| Context | Rural mountain foothills — WUI wildfire-interface asset; seasonal access, snow, wildfire, drainage, and utility continuity are load-bearing |

## Operating core

```text
asset protection → continuity → seasonal readiness → productive capacity → optional revenue
```

Every weekly task, monthly repair, and seasonal gate should reduce wildfire, continuity, access, water, septic, insurance, or infrastructure risk.

## Loops and shelves

| Loop | Shelf | Artifacts |
| --- | --- | --- |
| `mountain-homestead-ops` | [`ops/`](ops/README.md) | Weekly ops card, task/supply list, risk notes |
| `mountain-homestead-risk-register` | [`risk-register/`](risk-register/README.md) | Monthly risk register, top 5 actions, escalations |
| `mountain-homestead-maintenance` | [`maintenance/`](maintenance/README.md) | Monthly report, repair backlog, contractors |
| `mountain-homestead-wildfire-mitigation-review` | [`wildfire-mitigation/`](wildfire-mitigation/README.md) | Ignition zone review, defensible space, mitigation proof |
| `mountain-homestead-utilities-continuity` | [`utilities-continuity/`](utilities-continuity/README.md) | 72-hour continuity card, backup power/fuel log |
| `mountain-homestead-water-systems-review` | [`water-systems/`](water-systems/README.md) | Quarterly well review, test/filter log |
| `mountain-homestead-septic-review` | [`septic/`](septic/README.md) | Annual septic review, pump/inspection due dates |
| `mountain-homestead-seasonal-readiness` | [`seasonal-readiness/`](seasonal-readiness/README.md) | Seasonal gate checklists, post-season lessons |

**Access** (no separate loop): [`access/access-readiness-checklist.md`](access/access-readiness-checklist.md) — reviewed via weekly ops.

**Templates:** risk register · mitigation proof · 72-hour continuity · water · septic · access (paths under each shelf README).

**Action cards:** [`../../action-cards/mountain-homestead-risk-register/`](../../action-cards/mountain-homestead-risk-register/) · [standard](../../../docs/singularity/action-card-standard.md)

## Hard dependencies

```text
mountain-homestead-ops → mountain-homestead-maintenance → mountain-homestead-seasonal-readiness
mountain-homestead-ops → mountain-homestead-risk-register
mountain-homestead-ops → mountain-homestead-water-systems-review
mountain-homestead-maintenance → mountain-homestead-wildfire-mitigation-review
mountain-homestead-maintenance → mountain-homestead-utilities-continuity
mountain-homestead-maintenance → mountain-homestead-septic-review
```

## Soft feeds

| From | To | What flows |
| --- | --- | --- |
| `mountain-homestead-risk-register` | `mountain-homestead-ops` | Top 5 risk-reduction actions |
| `mountain-homestead-utilities-continuity` | `mountain-homestead-ops` | Continuity gaps |
| `mountain-homestead-wildfire-mitigation-review` | `mountain-homestead-risk-register`, maintenance | Mitigation proof, task list |
| `mountain-homestead-water-systems-review` | maintenance | Water risks and actions |
| `mountain-homestead-septic-review` | maintenance | Pump/inspection backlog |
| Risk register / wildfire / continuity | `mountain-homestead-seasonal-readiness` | Seasonal escalations and baselines |
