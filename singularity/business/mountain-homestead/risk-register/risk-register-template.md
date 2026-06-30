# Mountain Homestead — Risk Register Template

Use for loop **`mountain-homestead-risk-register`**. One file per month under [`monthly/`](monthly/).

---

## Register header

```yaml
register_month: 2026-07
site: Pine, CO — 5 acres
review_date:
reviewer:
```

---

## Risk scoring

```text
priority_score = consequence × likelihood × urgency ÷ cost_to_reduce
```

Each field scored **1–5**:

| Field | 1 | 5 |
| --- | --- | --- |
| Consequence | Minor inconvenience | Asset loss / habitability threat |
| Likelihood | Unlikely this season | Very likely this season |
| Urgency | Can defer months | Action needed now |
| Cost-to-reduce | Cheap / easy | Expensive / hard |

---

## Risk table

| ID | Risk | Consequence | Likelihood | Urgency | Cost-to-reduce | Score | Owning loop | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R1 | | | | | | | | open |
| R2 | | | | | | | | |
| R3 | | | | | | | | |
| R4 | | | | | | | | |
| R5 | | | | | | | | |

**Owning loop values:** `mountain-homestead-ops`, `mountain-homestead-maintenance`, `mountain-homestead-wildfire-mitigation-review`, `mountain-homestead-utilities-continuity`, `mountain-homestead-water-systems-review`, `mountain-homestead-septic-review`, `mountain-homestead-seasonal-readiness`

---

## Top 5 risk-reduction actions (feeds weekly ops)

1.
2.
3.
4.
5.

---

## Escalations

List any risk threatening habitability, insurability, access, water, heat, or asset value:

```yaml
escalation_1:
escalation_2:
```

---

## Input sources this month

- [ ] Weekly ops cards
- [ ] Maintenance backlog
- [ ] Wildfire mitigation notes
- [ ] Utilities continuity card
- [ ] Water / septic status
- [ ] Access issues
- [ ] Weather outlook
- [ ] Insurance concerns

Strategy: [STRATEGIC-PLAN.md](../STRATEGIC-PLAN.md)
