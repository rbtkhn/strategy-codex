# Media Quality Gate — [lesson-id]

WORK only; not Record.

**Media pack:** `media-packs/[lesson-id]/`
**Reviewer:**
**Date:**

---

## Gate decision

**Status:** approve | revise | hold | reject

---

## 1. Factual accuracy

| Check | Pass | Notes |
| --- | --- | --- |
| Claims match source packet and lesson brief | | |
| Dates, names, places verified | | |
| AI visuals labeled as illustration/reconstruction where needed | | |
| No fabricated maps, documents, or quotes | | |

## 2. Pedagogy

| Check | Pass | Notes |
| --- | --- | --- |
| Method spine preserved in media order | | |
| Evidence before outcome in learner-facing sequence | | |
| Visuals clarify prediction/evidence/causality/outcome | | |
| No decorative AI slop without instructional purpose | | |

## 3. Rights and disclosure

| Check | Pass | Notes |
| --- | --- | --- |
| Commercial-safe asset classes per tool-notes | | |
| No unclear likeness or trademark risk | | |
| AI assistance disclosed where platform requires | | |
| Music/stock assets licensed or royalty-free documented | | |

## 4. Bias and representation

| Check | Pass | Notes |
| --- | --- | --- |
| Representation reviewed for stereotype or omission | | |
| Prefer diagrams/timelines over personification where uncertain | | |

## 5. Production quality

| Check | Pass | Notes |
| --- | --- | --- |
| Audio intelligible; pacing appropriate | | |
| Captions planned or attached | | |
| Segment lengths within target band | | |

---

## Rejection log (if any assets rejected)

| Asset | Reason | Action |
| --- | --- | --- |
| | | |

---

## Provenance Pattern Note

External reference: [apresmoi/jianglens](https://github.com/apresmoi/jianglens) demonstrates a useful discipline for keeping source and interpretation visibly separate: individual sources remain inspectable, while compressed lens pages preserve provenance links back to source material.

For Predictive History, media assets should preserve the same separation:

```text
source claim ≠ lesson interpretation ≠ visual reconstruction
```

Every public asset should make clear what is source-grounded, what is interpretive compression, and what is illustrative media.

---

## Outcome routing

- **Approve** → `predictive-history-distribution-pack`; assets to `distribution/`
- **Revise** → return to `predictive-history-media-pack` with notes
- **Hold** → block publish until source or rights issue resolved
- **Reject** → document in feedback loop if learner-facing failure pattern
