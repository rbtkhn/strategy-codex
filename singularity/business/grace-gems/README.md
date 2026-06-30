# Grace Gems — business operating shelf

WORK only; not Record.

Grace Gems business operating shelf. Contains output artifacts for marketplace operations, product pipeline planning, listing optimization, customer service, reputation tracking, and business action cards.

**Business SSOT (doctrine, entity, policies):** [`docs/skill-work/work-business/grace-gems/`](../../docs/skill-work/work-business/grace-gems/README.md)

**Etsy storefronts (same business):**

| Shop | URL |
| --- | --- |
| GraceGemsUS | [etsy.com/shop/GraceGemsUS](https://www.etsy.com/shop/GraceGemsUS) |
| GioielloHandcrafted | [etsy.com/shop/GioielloHandcrafted](https://www.etsy.com/shop/GioielloHandcrafted) |

Market tag reference: [etsy.com/market/grace_gems](https://www.etsy.com/market/grace_gems)

## Loops and shelves

| Loop | Shelf | Artifacts |
| --- | --- | --- |
| `grace-gems-marketplace-ops` | [`ops/`](ops/README.md) | Daily ops card, prioritized action list, issue log |
| `grace-gems-product-pipeline` | [`products/`](products/README.md), [`listings/`](listings/README.md) | Weekly pipeline, listing drafts, photo checklists |
| `grace-gems-customer-service` | [`customer-service/`](customer-service/README.md) | Draft responses, issue log, reputation risk notes |

## Soft feed (not a schema dependency)

`grace-gems-customer-service` has no hard `loop_id` dependency on marketplace-ops. Unresolved customer issues and reputation risks **soft-feed** the daily `grace-gems-marketplace-ops` card during the ops review step.

## Dependency chain (hard)

```text
grace-gems-marketplace-ops → grace-gems-product-pipeline
```
