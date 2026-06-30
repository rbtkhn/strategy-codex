# Grace Gems — business operating shelf

WORK only; not Record.

Grace Gems business operating shelf. Contains output artifacts for marketplace operations, product pipeline planning, listing review gate, search/conversion optimization, customer service, promise audits, and business action cards.

**Strategic plan (operating SSOT):** [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md)

**Business doctrine (entity, policies):** [`docs/skill-work/work-business/grace-gems/`](../../docs/skill-work/work-business/grace-gems/README.md)

**Etsy storefronts (same business):**

| Shop | URL |
| --- | --- |
| GraceGemsUS | [etsy.com/shop/GraceGemsUS](https://www.etsy.com/shop/GraceGemsUS) |
| GioielloHandcrafted | [etsy.com/shop/GioielloHandcrafted](https://www.etsy.com/shop/GioielloHandcrafted) |

Market tag reference: [etsy.com/market/grace_gems](https://www.etsy.com/market/grace_gems)

## Operating core

Every listing is **margin-tested, policy-safe, search-aware, and customer-promise clear** before publish or promotion.

```text
product idea → listing draft → margin + policy review → publish / revise / hold → marketplace ops → CS feedback → pipeline update
```

## Loops and shelves

| Loop | Shelf | Artifacts |
| --- | --- | --- |
| `grace-gems-product-pipeline` | [`products/`](products/README.md), [`listings/drafts/`](listings/drafts/) | Weekly pipeline, listing drafts, photo checklists |
| `grace-gems-margin-policy-review` | [`listings/review/`](listings/review/README.md) | Margin note, policy compliance, quality score, publish decision |
| `grace-gems-marketplace-ops` | [`ops/`](ops/README.md) | Daily ops card, action list, issue log |
| `grace-gems-search-conversion-review` | [`listings/search-conversion/`](listings/search-conversion/README.md) | Weekly SEO/conversion review, experiment queue |
| `grace-gems-customer-service` | [`customer-service/`](customer-service/README.md) | Draft responses, issue log, reputation notes |
| `grace-gems-customer-promise-audit` | [`customer-service/promise-audits/`](customer-service/promise-audits/README.md) | Weekly promise audit, correction queue |

**Templates:** [`listings/review/listing-review-template.md`](listings/review/listing-review-template.md) · [`listings/search-conversion/listing-quality-score.md`](listings/search-conversion/listing-quality-score.md) · [`customer-service/promise-audits/customer-promise-checklist.md`](customer-service/promise-audits/customer-promise-checklist.md)

## Hard dependencies

```text
grace-gems-product-pipeline → grace-gems-margin-policy-review
grace-gems-marketplace-ops → grace-gems-search-conversion-review
grace-gems-customer-service → grace-gems-customer-promise-audit
```

## Soft feeds (not schema dependencies)

| From | To | What flows |
| --- | --- | --- |
| `grace-gems-margin-policy-review` | `grace-gems-marketplace-ops` | Approved listings, publish/revise/hold decisions |
| `grace-gems-search-conversion-review` | `grace-gems-product-pipeline` | SEO/conversion experiment queue |
| `grace-gems-customer-promise-audit` | `grace-gems-margin-policy-review`, product pipeline | Listing correction queue |
| `grace-gems-customer-service` | `grace-gems-marketplace-ops` | Unresolved issues for daily ops card |

## Dual-shop rule

Do not duplicate the same listing across GraceGemsUS and GioielloHandcrafted without a documented reason (different buyer promise, SEO angle, photo style, or price band). Use dual-shop routing fields in pipeline and review templates.
