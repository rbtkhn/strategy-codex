# Grace Gems — Strategic Plan

**Scope:** `operations/grace-gems/` operating system.

**One-line strategy:** Grace Gems uses Singularity to convert Etsy selling into a review-gated operating system — every listing is margin-tested, policy-safe, search-aware, and customer-promise clear before it touches the market.

---

## Executive thesis

Grace Gems is managed as a **margin-aware, policy-safe, dual-storefront Etsy operating system**.

Objective chain:

```text
more qualified listings
  → better search visibility
  → higher conversion
  → protected margin
  → lower customer-service risk
  → reusable operating workflows
```

**Review gate** between product creation and marketplace operations:

```text
product idea
  → listing draft
  → margin + policy review
  → photo / SEO / customer-promise review
  → publish / revise / hold
  → marketplace ops
  → customer-service feedback
  → product pipeline update
```

---

## Dual storefronts

| Storefront | Role | Best product fit |
| --- | --- | --- |
| **GraceGemsUS** | Main U.S. trust / conversion storefront | Custom gemstone jewelry, giftable pieces, personalized fine jewelry |
| **GioielloHandcrafted** | Artisan / design-forward storefront | Boutique, handcrafted, design-forward, one-of-one pieces |

**Rule:** Do not duplicate the same listing across both shops without a reason. Test same product family with different buyer promise, SEO angle, photo style, or price band.

Dual-shop routing fields (use in pipeline and review):

```text
target_shop:
why_this_shop:
buyer_intent:
price_band:
customization_level:
inventory_type:
brand_fit_score:
```

---

## Marketplace reality

Etsy is dense and pressured (100M+ listings, weak discretionary spending, platform competition). Grace Gems cannot win by being generic.

Compete on:

| Advantage | Meaning |
| --- | --- |
| **Trust** | Clear gemstone, metal, production, shipping, customization expectations |
| **Originality** | Real photos, visible handwork, human-touch evidence |
| **Conversion** | Strong first image, clear title, buyer-focused listing structure |
| **Margin discipline** | Fees, labor, materials, shipping, offsite ads modeled before publication |
| **Customer promise** | No over-promising customization, timing, quality, or permanence |
| **Repeatability** | Every listing reviewed by checklist and improved systematically |

---

## Positioning

Avoid positioning that depends only on "stone size for price." Lab-grown diamonds: use only where they support a clear customer promise, not as core brand identity.

**Brand center:** custom natural gemstone jewelry with visible human design and trustworthy execution.

Better positioning axes:

```text
custom natural gemstone design
personalized gift
handmade / hand-assembled quality
unique color story
birthstone / anniversary / occasion logic
two-storefront brand segmentation
trustworthy customization
```

---

## Etsy policy (Creativity Standards)

Safest categories for Grace Gems: **made by seller** or **designed by seller** (depending on in-house vs partner production).

Checklist per listing — see [`listings/review/listing-review-template.md`](listings/review/listing-review-template.md).

Key requirements:

- Human touch evidence
- Original photo or video of final product
- Production partner disclosure if applicable
- AI disclosure in description if AI used
- Gemstone and metal claims verified

---

## Fee economics and margin firewall

Etsy fees (reference): $0.20 listing fee; 6.5% transaction fee on price + shipping + gift wrap; Offsite Ads 12–15% on attributed orders (mandatory once shop qualifies).

Evaluate every listing in three margin scenarios:

| Scenario | Fee logic |
| --- | --- |
| **Base Etsy sale** | Listing + transaction + payment processing + shipping cost |
| **Etsy Ads sale** | Base + Etsy Ads spend allocation |
| **Offsite Ads sale** | Base + 12–15% attributed order fee |

**Net profit formula:**

```text
net_profit =
  sale_price
  + charged_shipping
  - materials_cost
  - packaging_cost
  - actual_shipping_cost
  - labor_cost
  - Etsy_listing_fee
  - Etsy_transaction_fee
  - Etsy_payment_processing_fee
  - ad_cost
  - offsite_ads_fee_if_any
```

**Margin thresholds:**

| Listing type | Minimum target gross margin |
| --- | ---: |
| Simple accessory / lower-price item | 50–60% |
| Custom gemstone jewelry | 60–70% |
| High-touch custom order | 70%+ |
| Loss-leader / test listing | Explicit exception only |

---

## Listing Quality Score

Score each listing 0–100 — full rubric: [`listings/search-conversion/listing-quality-score.md`](listings/search-conversion/listing-quality-score.md).

| Component | Weight |
| --- | ---: |
| Search matching | 20 |
| First-image strength | 15 |
| Trust clarity | 15 |
| Conversion copy | 15 |
| Margin | 15 |
| Policy safety | 10 |
| Customer-service risk | 10 |

**Decision rule:**

```text
90–100 = publish / promote
75–89  = publish but do not advertise yet
60–74  = revise before publish
<60    = hold / rewrite / retire
```

---

## Customer promise and CS root causes

Checklist: [`customer-service/promise-audits/customer-promise-checklist.md`](customer-service/promise-audits/customer-promise-checklist.md).

**Root-cause taxonomy** (classify messages by cause, not issue type only):

| Root cause | Action |
| --- | --- |
| Listing unclear | Fix listing copy |
| Photo misleading | Add image or caption |
| Customization ambiguous | Add customization menu |
| Shipping timing issue | Add timeline block |
| Quality concern | Add pre-ship QA photo |
| Buyer expectation mismatch | Add FAQ or variant guide |

**Feedback loop:**

```text
customer message → root cause → listing correction → fewer future messages → better reviews → better search / trust
```

---

## Loop cluster

| Loop | Role |
| --- | --- |
| `grace-gems-product-pipeline` | Weekly drafts, dual-shop routing, pipeline priorities |
| `grace-gems-margin-policy-review` | **Gate** — margin, policy, quality score before publish |
| `grace-gems-marketplace-ops` | Daily shop ops on both storefronts |
| `grace-gems-search-conversion-review` | Weekly SEO/conversion experiments |
| `grace-gems-customer-service` | Event-driven buyer message handling |
| `grace-gems-customer-promise-audit` | Weekly listing clarity audit from CS patterns |

See [`README.md`](README.md) for hard/soft dependency graph.

---

## 30-day operating plan

### Week 1 — Establish controls

Goal: prevent bad listings and bad economics.

1. Run `grace-gems-margin-policy-review` on 10 current or draft listings
2. Use listing review template and margin fields
3. Output: `listings/review/2026-07-baseline.md`

### Week 2 — Improve conversion

Goal: identify where views fail to become sales.

1. Record views, favorites, conversion, search terms
2. Score listings with Listing Quality Score
3. Rewrite bottom 5 with good product potential
4. Do not advertise listings scoring below 75
5. Output: `listings/search-conversion/2026-week-2.md`

### Week 3 — Customer-service feedback loop

Goal: reduce avoidable buyer questions.

1. Review last 30–90 days of messages
2. Categorize by root cause
3. Update listings that caused confusion
4. Draft response templates for top 5 recurring questions
5. Output: `customer-service/promise-audits/2026-week-3.md`

### Week 4 — Operating review

Goal: determine which improvements are compounding.

1. Review listings updated in Weeks 1–3
2. Compare before/after metrics where available
3. Retire or hold low-quality or low-margin listings
4. Output: `ops/monthly-review/2026-07.md`

---

## Weekly scorecard

| Metric | Target | Why |
| --- | ---: | --- |
| New reviewed listings | 3–5/week | Throughput |
| Listings scoring 75+ | 80%+ | Publish quality |
| Listings scoring 90+ | 20%+ | Promotion candidates |
| Gross margin after base fees | 50%+ | Profit protection |
| Gross margin after offsite ad risk | 35%+ | Downside survival |
| Buyer-message root causes fixed | 3/week | Reputation protection |
| High-view low-conversion listings improved | 2/week | Conversion leverage |
| Customer issues unresolved >48h | 0 | Reputation / search risk |

See also [`ops/README.md`](ops/README.md).

---

## Business doctrine (external)

Entity, policies, and long-form business context: [`docs/skill-work/work-business/grace-gems/`](../../docs/skill-work/work-business/grace-gems/README.md).
