# Grace Gems — Customer Promise Checklist

Use in **`grace-gems-margin-policy-review`** (pre-publish) and **`grace-gems-customer-promise-audit`** (weekly).

---

## Pre-publish questions

Answer each for the listing under review.

| # | Question | clear? | fix if no |
| ---: | --- | --- | --- |
| 1 | What exactly will the buyer receive? | | |
| 2 | Is the photographed item the exact item or an example? | | |
| 3 | Are gemstone color variations explained? | | |
| 4 | Are metal, plating, gold-filled, or solid-gold claims precise? | | |
| 5 | Is customization scope clear (what is / is not included)? | | |
| 6 | Is production time clear? | | |
| 7 | Is shipping time separated from production time? | | |
| 8 | Is return / exchange policy clear for custom items? | | |
| 9 | What question is the buyer most likely to ask? | | |
| 10 | Is that question answered in the listing? | | |

---

## Root-cause taxonomy (customer messages)

Classify each buyer message or review by **root cause**, not surface issue type alone.

| Root cause | Typical signal | Listing fix |
| --- | --- | --- |
| Listing unclear | "I thought it included…" | Rewrite description block |
| Photo misleading | "Looks different in person" | New photo or example caption |
| Customization ambiguous | "Can you also…?" | Variation menu or limits section |
| Shipping timing issue | "When will it ship?" | Production + ship timeline block |
| Quality concern | Stone, metal, or finish dispute | QA photo step; materials clarity |
| Buyer expectation mismatch | Gift size, color, or style surprise | FAQ, size guide, color note |

```yaml
message_date:
shop: GraceGemsUS | GioielloHandcrafted
order_id:
root_cause:
listing_id:
listing_fix_required: yes | no
fix_description:
template_update: yes | no
resolved: yes | no
```

---

## Weekly audit output (promise-audit loop)

```yaml
audit_week:
listings_reviewed:
issues_from_messages:
corrections_queued:
top_recurring_question:
templates_updated:
priority_fixes:   # ranked by revenue impact and reputation risk
```

Strategy: [STRATEGIC-PLAN.md](../../STRATEGIC-PLAN.md)
