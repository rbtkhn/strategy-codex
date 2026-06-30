# Grace Gems — Listing Review Template

Use for loop **`grace-gems-margin-policy-review`**. One file per listing review under [`listings/review/`](.).

Copy this block into a dated review note (e.g. `2026-07-baseline.md` or `listing-<slug>-review.md`).

---

## Listing identity

```yaml
listing_id:
shop: GraceGemsUS | GioielloHandcrafted
listing_title:
review_date:
reviewer:
status: draft | active | relist
```

## Dual-shop routing

```yaml
target_shop:
why_this_shop:
buyer_intent:
price_band:
customization_level:
inventory_type:
brand_fit_score:
```

---

## Margin fields

```yaml
sale_price:
materials_cost:
labor_minutes:
labor_rate:
packaging_cost:
shipping_charged:
shipping_actual:
etsy_listing_fee: 0.20
etsy_transaction_fee:        # 6.5% of price + shipping + gift wrap
payment_processing_fee:
etsy_ads_allocated:
offsite_ads_risk:            # 12% or 15% if attributed
gross_margin_dollars:
gross_margin_percent:
```

### Margin scenarios

| Scenario | Survives threshold? | Notes |
| --- | --- | --- |
| Base Etsy sale | yes / no | |
| Etsy Ads sale | yes / no | |
| Offsite Ads sale | yes / no | |

### Margin thresholds (reference)

| Listing type | Minimum gross margin |
| --- | ---: |
| Simple accessory / lower-price | 50–60% |
| Custom gemstone jewelry | 60–70% |
| High-touch custom order | 70%+ |

```yaml
margin_decision: publish | revise price | bundle | hold | retire
```

---

## Etsy Creativity Standards

```yaml
category: made_by_seller | designed_by_seller | sourced_by_seller
human_touch_evidence:
original_photo_or_video: yes | no
customization_shown_in_first_image: yes | no | n/a
production_partner_disclosure_needed: yes | no
production_partner_disclosed: yes | no | n/a
AI_disclosure_needed: yes | no
AI_disclosed: yes | no | n/a
gemstone_or_metal_claims_verified: yes | no
policy_status: pass | revise | hold | reject
```

---

## Listing Quality Score (summary)

Full rubric: [`../search-conversion/listing-quality-score.md`](../search-conversion/listing-quality-score.md)

| Component | Weight | Score (0–max) |
| --- | ---: | ---: |
| Search matching | 20 | |
| First-image strength | 15 | |
| Trust clarity | 15 | |
| Conversion copy | 15 | |
| Margin | 15 | |
| Policy safety | 10 | |
| Customer-service risk | 10 | |
| **Total** | **100** | |

```yaml
quality_score_total:
quality_decision: publish_promote | publish_no_ads | revise | hold | retire
```

Thresholds: 90+ publish/promote · 75–89 publish no ads · 60–74 revise · <60 hold/retire

---

## Customer promise (pre-publish)

See [`../../customer-service/promise-audits/customer-promise-checklist.md`](../../customer-service/promise-audits/customer-promise-checklist.md).

```yaml
customer_promise_clear: yes | no
top_buyer_question_likely:
promise_gaps:
```

---

## Final decision

```yaml
publish_decision: publish | revise | hold | reject
blockers:
next_actions:
feeds_to: grace-gems-marketplace-ops | grace-gems-product-pipeline
```

---

Strategy: [STRATEGIC-PLAN.md](../../STRATEGIC-PLAN.md)
