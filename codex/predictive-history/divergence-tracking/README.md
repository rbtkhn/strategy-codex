# Jiang lectures â€” divergences from mainstream views

**Purpose:** When building the book/site, mark where Jiangâ€™s **stated claims** **depart** from **named** mainstream or consensus positions â€” without treating â€œmainstreamâ€ as morally true or false. This is **operator research** (clarity + fair comparison), **not** Voice knowledge until merged through the gate.

**Volume II (Civilization):** The second book pass for that strand is **Part II â€” Divergence**, not prediction adjudication. See [`book/PART-II-CIVILIZATION-DIVERGENCE.md`](../book/PART-II-CIVILIZATION-DIVERGENCE.md) and [`CHAPTER-DIVERGENCE-BOX.md`](../CHAPTER-DIVERGENCE-BOX.md).

**Hard rule:** Always tag **whose** mainstream you mean (jurisdiction, discipline, or institution). â€œMainstreamâ€ without a scope is vague.

---

## Dimensions of divergence

| `divergence_type` | Meaning | Compare carefully |
|-------------------|---------|-------------------|
| `empirical` | Fact claims (dates, who could read scripture, vote counts) | Primary sources + specialists |
| `interpretive` | Causation, motivation, â€œwhat drivesâ€ policy | Competing IR / history models |
| `pedagogical_compression` | Simplification for class (not offered as journal-grade) | Label explicitly; not â€œwrong,â€ **compressed** |
| `normative` | What *should* happen (justice, â€œevil,â€ strategy) | Separate from predictive claims |

---

## Strength (operator judgment)

| `strength` | Use when |
|------------|----------|
| `strong` | Clear opposition to a well-defined consensus in named field |
| `moderate` | One contested school among several |
| `nuance` | Mostly aligns; emphasis or framing differ |
| `unclear` | Need more sourcing on both sides |

---

## How to write a good row

1. **`jiang_claim`** â€” Short, fair paraphrase (can quote transcript in `lecture_ref`).  
2. **`mainstream_anchor`** â€” Name the consensus: e.g. â€œtypical US diplomatic history undergraduate narrative,â€ â€œCatholic teaching today on scripture access,â€ â€œmainstream IR (structural realism) on Middle East alliances.â€  
3. **`mainstream_summary`** â€” One or two sentences; avoid straw men.  
4. **`evidence_notes`** â€” What would falsify your labeling of â€œmainstreamâ€ or refine the divergence.  
5. **`sources_mainstream`** â€” URLs or citations (optional but encouraged for non-obvious claims).  

---

## Registry

Append-only JSONL: [registry/divergences.jsonl](registry/divergences.jsonl)

Fields (typical):

- `divergence_id`, `video_id`, `lecture_ref`
- `topic_tags` (array)
- `jiang_claim`, `mainstream_anchor`, `mainstream_summary`
- `divergence_type`, `strength`
- `evidence_notes`, `sources_mainstream` (array), `sources_jiang` (optional; usually lecture URL)

**SQLite:** the same rebuild script indexes divergences into [../registry/work_jiang_metrics.sqlite](../registry/README.md) for ad hoc SQL; JSONL stays canonical.

---

## Relation to other lanes

- **[Prediction tracking](../prediction-tracking/README.md)** â€” Did a **forecast** land? Divergence tracking asks: **does the thesis match how a field usually explains the same topic?**  
- **[Influence tracking](../influence-tracking/README.md)** â€” Attention, not truth.  
- **CIV-MEM / analysis memos** â€” Divergence rows can point to `analysis/*-analysis.md` for full argument maps.

## CIV-MEM lens

â€œMainstreamâ€ often differs by **which institution or seam** a discipline foregrounds (e.g. realist IR vs religious-network causality). Use [CIV-MEM-LENS.md](../CIV-MEM-LENS.md) to state **both** the lecture's **seam/institution emphasis** and the comparator fieldâ€™s, then add the short civ-mem bridge if relevant - this reduces straw-man comparisons.

---

## Related

- [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md)  
- [codex/predictive-history/README-operator.md](../README-operator.md)  

