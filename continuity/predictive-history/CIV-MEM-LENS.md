# Predictive History - CIV-MEM reference spine
<!-- word_count: 603 -->

**Purpose:** Use civilization-memory framing - conditions, institutions, seams, continuity, horizons - as a structured overlay on Predictive History comparison work. CIV-MEM is a reference spine, not identity and not a second corpus.

**Boundary:** [`civilization_memory`](../../docs/archive/skill-work-legacy/work-civ-mem/README.md) and [`docs/civilization-memory/`](../../docs/civilization-memory/README.md) are external reference surfaces. They inform how you analyze the corpus; they do not become companion Record unless gated. See [README-operator.md](./README-operator.md).

---

## 1. Why civ-mem fits Predictive History

Predictive History mixes power, religion as institution, empire, alliance seams, and historical continuity - the same family of objects civ-mem is built to hold at civilization scale. The lattice below is a discipline for analysis, not a verdict on the corpus.

---

## 2. Lattice - what to look for in a lecture

| Lattice slot | Question for the text | Typical tags |
|--------------|----------------------|--------------|
| Conditions | What background is treated as fixed? | `conditions`, `constraints`, `starting-assumptions` |
| Institutions | What durable bodies carry action? | `institutions`, `governance`, `hierarchy` |
| Seams | Where does the speaker expect cracks? | `seams`, `friction`, `alliance` |
| Continuity / memory | What past is mobilized as authority? | `continuity`, `memory`, `founding-narrative` |
| Time structure | Eschatology, election cycles, or long decline | `time-horizon`, `eschatology`, `forecast-window` |
| Decline / stress vectors | Overextension, debt, civil unrest | `decline`, `overextension`, `internal-strain` |

Use these in analysis memos and optionally in registry rows.

---

## 3. Comparison bridge fields

For Predictive History comparison sidecars, keep the civ-mem object compact and explicit:

```json
"civ_mem": {
  "paths": ["docs/civilization-memory/..."],
  "case_families": ["Rome", "Persia"],
  "alignment_notes": "short note",
  "mismatch_notes": "short note",
  "bridge_paragraph": "short bridge paragraph",
  "confidence": "low"
}
```

Guidance:

- `paths` - exact CIV-MEM or CMC paths used as reference points.
- `case_families` - short labels for the historical family or analogue.
- `alignment_notes` - why the lecture and the civ-mem reference overlap.
- `mismatch_notes` - where the analogy breaks or overreaches.
- `bridge_paragraph` - one short paragraph explaining why the reference matters historically.
- `confidence` - `low`, `medium`, or `high`; use `low` when the bridge is only a relevance check.

Default rule for comparison passes:

- consult civ-mem on every comparison pass
- keep the bridge short
- do not force a match if relevance is weak
- prefer path references and operator-written synthesis over long paraphrase

---

## 4. Map registries - civ-mem use

| Registry | Primary civ-mem move |
|----------|----------------------|
| Influence | Attention over time, not truth. Ask whether a spike correlates with a condition change or seam visibility. |
| Predictions | Treat forecasts as time-structured claims against the world. Classify what kind of civilizational object is predicted. |
| Divergences | Ask which institution or seam a field foregrounds, not just whether the lecture is "right" or "wrong". |

---

## 5. Retrieval workflow

1. Human question - for example, "How does civ-mem talk about empire plus religion plus seam?"
2. Query - use the civ-mem corpus or the in-repo index.
3. Tag provenance - `{CMC: path}` on any pasted line in drafts.
4. Separate layers - what the lecture says, what CMC says, and your synthesis. Keep the civ-mem bridge short and explicit.

---

## 6. Worked example

| Slot | Example notes |
|------|---------------|
| Conditions | US empire role, Israel-Iran tension, and inequality under Pax Americana |
| Institutions | Church history, lobby, military-foreign-policy apparatus |
| Seams | US-Israel friction, coalition splits, intra-Christian division on eschatology |
| Continuity | Reformation, founding migrations, 1948 |
| Time structure | Second Coming frameworks; long decline rather than a quick fix |
| Decline stress | Inequality leading to appetite for total narratives |

This table belongs in an analysis memo, not the Voice profile, unless gated.

---

## Related

- [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md)
- [work-civ-mem README](../../docs/archive/skill-work-legacy/work-civ-mem/README.md)
- [Civilization memory lane](../../docs/lanes/civilization-memory.md)
