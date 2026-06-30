# Grace Gems — Listing Quality Score

Rubric for loops **`grace-gems-margin-policy-review`** and **`grace-gems-search-conversion-review`**.

Score each listing **0–100**. Use with [`../review/listing-review-template.md`](../review/listing-review-template.md).

---

## Components

| Component | Weight | What to check |
| --- | ---: | --- |
| Search matching | 20 | Title, tags, attributes, category, buyer query fit |
| First-image strength | 15 | Clear, attractive, final product visible, customization shown |
| Trust clarity | 15 | Materials, gemstone, metal, size, shipping, returns, customization |
| Conversion copy | 15 | Benefit-led description, gift use case, occasion, reassurance |
| Margin | 15 | Meets margin threshold under base and ad-risk scenario |
| Policy safety | 10 | Human touch, original photo, partner / AI disclosure if needed |
| Customer-service risk | 10 | No ambiguous promises, timing, quality, or customization gaps |

---

## Scoring guide (per component)

Assign 0 to full weight for each row. Partial credit allowed.

**Search matching (20):** Title contains primary keyword; 13 tags used meaningfully; category and attributes match buyer intent; no keyword stuffing.

**First-image (15):** Product fills frame; accurate color; lifestyle or scale if helpful; customization example visible when listing is custom.

**Trust clarity (15):** Metal type precise (solid vs filled vs plated); gemstone natural/treated stated; size/dimensions; production + shipping time separated; return policy for custom items clear.

**Conversion copy (15):** Opens with buyer benefit; occasion/gift angle; answers top objection; readable on mobile.

**Margin (15):** Meets type threshold on base sale; survives offsite-ads scenario at 35%+ gross or explicit exception documented.

**Policy safety (10):** Creativity Standards pass; original media; disclosures complete.

**CS risk (10):** No "example only" photo without label; color variation noted; customization limits explicit.

---

## Decision rule

```text
90–100 = publish / promote
75–89  = publish but do not advertise yet
60–74  = revise before publish
<60    = hold / rewrite / retire
```

---

## Weekly search-conversion use

For **`grace-gems-search-conversion-review`**, also record:

```yaml
listing_id:
shop:
views_7d:
favorites_7d:
conversion_rate:
search_terms:
experiment: title | tags | first_image | price | shipping | description
hypothesis:
before_score:
target_score:
```

Strategy: [STRATEGIC-PLAN.md](../../STRATEGIC-PLAN.md)
