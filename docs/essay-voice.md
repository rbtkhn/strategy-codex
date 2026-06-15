# Essay Voice

WORK only; not Record.

**One-sentence definition:** topic-first, third-person, tri-blend transport synthesis with Kissinger spine, solemn gravitas, and light apparatus.

**Scope:** repo-root [`essays/`](../essays/README.md) transport voice only — not [`skill-write`](skill-write/README.md) public copy, not channel notes, not named-mind passes.

**Placement vs voice:** [prose-index.md](prose-index.md) chooses *where* prose lives; this file defines *how* repo-root essays sound.

---

## Draft checklist

Run before treating an essay draft as shelf-ready.

| Step | Check |
|------|--------|
| **1. Genre** | Named: argument/transport · system/product · comparative voice · (elsewhere) intelligence essay per [statecraft-intelligence-essay skill](../.cursor/skills/statecraft-intelligence-essay/SKILL.md) |
| **2. Apparatus band** | **Band A default:** prose-first, **max one comparison table**; pin-cites and verbatim depth live in notes/archive links |
| **3. Weight budget** | One Churchill set-piece per major strand **or** one table — not both at full density unless the table *is* the insight |
| **4. Topic-first lede** | First screen names **who / what / spine** in **prose** — not a mechanical `X names Y` triad; see [Template slop](#template-slop-comparative-voice-ledes) |
| **5. Author** | Third person; no diary **I** |
| **6. Tri-blend** | Kissinger structure + parallel; Churchill set-piece where primary must speak; Durant clarity in transitions |
| **7. Moral register** | Kissinger-realist: consequence, limits, who bears cost — not sermon, not neutral technocracy |
| **8. Forensic sources** | Barnes/Jiang (or other analyst) findings reported in **solemn third person** — no sardonic import from notes |
| **9. Falsifiers** | Optional prose bullets — not a second table |
| **10. Close** | **Kissinger warning** is the **final paragraph** — declarative consequence if constraints ignored; no rhetorical question ([drafting-no-rhetorical-question-closer.mdc](../.cursor/rules/drafting-no-rhetorical-question-closer.mdc)) |
| **11. Return paths** | Links-only tail — required shape, not apparatus |
| **12. Promotion** | If promoted from a note: **compress apparatus**; do not copy note pin-cite density |

Optional frontmatter on new essays: `voice_profile: tri-blend-band-a` (future lint/tooling hook).

---

## Purpose and boundary

| Layer | Role | SSOT |
|-------|------|------|
| **Notes** | Bounded interpretive objects; verbatim depth, pin-cites, analyst register OK | `statecraft/notes/`, `singularity/notes/` |
| **Archive** | Full primary capture | `source-archive/` |
| **Essays (this doc)** | Transport synthesis — thesis that travels | `essays/` |
| **Public copy** | Shorter derivative for Locals/X/PH | [write-operator-preferences.md](skill-write/write-operator-preferences.md) |

Essays **carry** the argument. Notes **hold** the receipts. Do not mirror note density in essay body.

---

## Genre decision tree

```
Is the finished piece a stand-alone thesis at repo-root essays/?
├─ No → notes/ or synthesis/ per prose-index
└─ Yes → Which essay genre?
    ├─ Single thesis, one arc, no named register comparison
    │   → Argument / transport (default)
    ├─ Product identity, definitional, short-version blocks
    │   → System / product
    ├─ Multi-register compare (e.g. Leo + Barnes + Jiang)
    │   → Comparative voice
    └─ Archive-grounded, speaker-hidden intelligence prose
        → statecraft-intelligence-essay skill (different shelf/genre;
           not tri-register compare; quotes usually omitted)
```

**Comparative voice** may name registers (office, liability, formation) but is **not** a tri-mind roundtable. Sources are **lanes**, not speakers in dialogue.

---

## Apparatus router

| Band | When | Allowed in essay body |
|------|------|------------------------|
| **Band A (default)** | Most repo-root essays | Prose; max **one** comparison table; archive/note links; one set-piece per major strand |
| **Band B (legacy)** | Pre-doctrine essays; notes | Pin-cite grids, verbatim lists, multiple tables — **do not copy on promotion** |
| **Literature matrix** | Thesis *is* lineage / non-uniqueness / design-family comparison | Evidence matrix + support cluster per [citation-evidence-pattern.md](citation-evidence-pattern.md) |

**Promotion voice shift:** When a note promotes to an essay, **compress apparatus**. Keep thesis and convergent claim; move pin-cites and verbatim stacks to notes/archive links.

**Weight budget (Band A):** If Leo (or any primary strand) gets a Churchill set-piece block quote, do **not** also add a pin-cite table for the same strand unless the table alone carries the disproportion insight.

---

## Tri-blend profile

Operator elicitation (2026-06): **Kissinger–Churchill–Durant** blend — not pastiche of any one author.

### Kissinger (spine)

- Structural realism: power, limits, who bears cost
- Historical **parallel as proof move** — one disciplined parallel per major section; inspectable; abstain if weak
- Nested qualification before strong claims
- **Warning close:** declarative consequence if constraints are ignored

**Do not pastiche:** opacity without translation; faux-diplomatic throat-clearing; invented historical rhyme.

### Churchill (texture)

- Periodic rhythm in load-bearing sentences
- **One extended quotation set-piece** per major strand when a primary or office source must speak
- Moral weight without cheap triumphalism or faux oratory

**Do not pastiche:** bombast; anthologies of one-liners where a set-piece would do; mock Churchillian cadence.

### Durant (transitions)

- Civilizational readability in section flow and lede clarity
- Human continuity across sections — not full narrative biography mode
- Topic + thesis on the **first screen**

**Do not pastiche:** encyclopedic survey; charming anecdote opener before the reader knows the thesis.

---

## Eight laws

1. **Topic-first opening** — thesis triad allowed (who / what / spine).
2. **Third person** — no **I**; operator judgment without diary voice.
3. **Mixed rhythm** — long build → short punch; avoid flat academic evenness.
4. **Kissinger parallels** — recurring, disciplined; one per major section; proportionate; abstain when weak.
5. **Kissinger-realist morality** — consequence, limits, cost-bearing; morality through mechanism.
6. **Churchill set-pieces** for primary/office sources; **paraphrase** analyst lanes in solemn third person.
7. **Light apparatus** — max one table; falsifiers as prose list unless the object demands a table.
8. **Solemn close** — Kissinger warning last; not a rhetorical question.

### Resolved tensions

| Tension | Rule |
|---------|------|
| Set-piece vs table | Weight budget: one or the other at full density per strand |
| Warning vs falsifiers | Falsifiers (optional) → then **warning close is final paragraph** |
| Solemn vs forensic | Report forensic findings solemnly; sardonic register stays in notes |
| Exemplar vs template | [`leo-barnes-jiang-on-ai.md`](../essays/leo-barnes-jiang-on-ai.md) = structural exemplar, **Band B legacy** for apparatus |

---

## Default shapes per genre

### Argument / transport

1. Lede — topic + spine (Durant clarity)
2. Shared seam (why this thesis now)
3. Three to four body sections (parallel + set-piece where warranted)
4. Convergent claim
5. Falsifiers (optional, prose bullets)
6. **Kissinger warning close**
7. Return paths (links only)

Prefer **prose comparison** over a table unless disproportion *is* the insight.

### Comparative voice

1. Tri-register lede — who / what / shared spine
2. Shared seam
3. Per-voice sections (paraphrase analyst lanes; set-piece for primaries)
4. Comparative seam (overlap / divergence / productive tension)
5. Convergent claim
6. Falsifiers (optional)
7. **Kissinger warning close**
8. Return paths

Not a tri-mind roundtable. Not speaker-by-speaker transcript spine unless comparison **is** the thesis.

### System / product

For essays such as [from-accumulation-to-governed-interpretive-machine.md](../essays/from-accumulation-to-governed-interpretive-machine.md) and [interpretive-machine.md](../essays/interpretive-machine.md):

- Short-version blocks and fenced thesis allowed
- Same solemn third-person
- Apparatus **slightly looser** when definitional or product-identity work requires it
- Literature matrix when lineage is load-bearing — see apparatus router

---

## Derivation boundary (essay → public copy)

Essays are **upstream** of [skill-write](skill-write/README.md). Public copy is a **derivative**, not a paste of the essay.

| Essay keeps | Locals / X / PH typically strips |
|-------------|----------------------------------|
| Full tri-blend arc | Compress to one public-facing claim |
| Kissinger parallels | One beat or drop |
| Churchill set-pieces | Short quote or paraphrase only |
| Comparison table | Prose or drop |
| Falsifiers block | Usually drop |
| Return paths | Drop or single link |

Full trim ladder doc is optional Phase 2. Until then, use [write-shipping-checklist.md](skill-write/write-shipping-checklist.md) on the **derivative**, not the essay file.

---

## Anti-patterns

From [write-operator-preferences.md](skill-write/write-operator-preferences.md) analyst-residue (adapted for essays):

| Pattern | Why it fails |
|---------|----------------|
| Tri-mind / roundtable voice | Essays compare registers; they do not host M/M/B dialogue |
| Speaker-by-speaker transcript spine | Unless comparison **is** the thesis |
| Heavy pin-cite grids in body | Band B; belongs in notes/archive |
| Verbatim one-liner anthologies | Use one set-piece or paraphrase |
| Faux Churchill bombast | Texture without substance |
| Kissinger opacity | Qualification without translation |
| Rhetorical question closer | Violates law 8 |
| Sardonic Barnes/Jiang register in essay body | Forensic content, solemn transport |
| Note dump in return paths | Links only |

### Before / after (Band B → Band A)

**Before (apparatus-heavy — do not default to this):**

```markdown
| § | Claim (archive) |
|---|-----------------|
| **99** | AI systems merely imitate human intelligence; no moral conscience |
| **110** | To disarm means discrediting the assumption that technical power confers the right to govern |
```

**After (Band A — prose + set-piece + link):**

```markdown
Leo’s encyclical refuses the succession fiction directly. In §99 of
[*Magnifica Humanitas*](../source-archive/statecraft/2026-05-15/source-vatican-magnifica-humanitas-leo-xiv-2026-05-15.md),
systems “merely imitate” human intelligence: they “do not have a moral conscience,”
do not “judge good and evil,” and do not “bear responsibility for consequences.”
The office claim is not that machines are useless; it is that competence cannot
inherit judgment. Full pin-cite grid lives in the archive capture, not here.
```

---

## Exemplars

| Essay | Model for |
|-------|-----------|
| [leo-barnes-jiang-on-ai.md](../essays/leo-barnes-jiang-on-ai.md) | Comparative voice structure, tri-register compare, evidence tier — **not** apparatus density; closer is falsifier-shaped, not warning-shaped (legacy gap) |
| [ai-and-the-expansion-of-human-consciousness.md](../essays/ai-and-the-expansion-of-human-consciousness.md) | Prose-first medium argument, decisive close |
| [from-accumulation-to-governed-interpretive-machine.md](../essays/from-accumulation-to-governed-interpretive-machine.md) | System essay, short-version |
| [interpretive-machine.md](../essays/interpretive-machine.md) | Definitional + ancestor convergence |

AI cluster reading order: see [essays/README.md](../essays/README.md) — voice doc does not merge cluster essays.

---

## Sample voice paragraph

> Machine competence is scaling faster than answerability. Pope Leo XIV names what no algorithm may inherit: moral judgment and pastoral witness. Robert Barnes names who pays when capex, energy, and campaign finance reorganize around an overstated product. Jiang Xueqin names the end-state hidden inside the branding. The parallel is not new. Whenever a civilization confuses persuasive speech with office — or price with truth — institutions discover too late that someone must still bear responsibility. The warning is equally plain: if office, liability, and formation are treated as optional layers on top of scale, the remaining politics will be performed by machines and billed to populations who were told the future had already arrived.

---

## Band A Leo retrofit sample

Primary treatise: [*Magnifica Humanitas*](../source-archive/statecraft/2026-05-15/source-vatican-magnifica-humanitas-leo-xiv-2026-05-15.md) (15 May 2026). Doctrinal foundation: [*Antiqua et Nova*](../source-archive/statecraft/2025-01-28/source-vatican-antiqua-et-nova-ai-2025-01-28.md). Institutional anchor: [Vatican City State AI guidelines (DCCII)](../source-archive/statecraft/2024-12-16/source-vatican-city-state-ai-guidelines-dccii-2024-12-16.md).

Leo’s encyclical is a social encyclical in the lineage of *Rerum Novarum*, not a technical white paper. From a statecraft angle, Rome speaks as a legitimacy-bearing office with civilizational residue. The text treats AI as part of a **change of era** — tools that can serve the good or distort it when profit and homogenizing power outrun conscience. *Antiqua et Nova* already drew the office line: treatment decisions and the weight of responsibility “must always remain with the human person and **should never be delegated to AI**.” The Vatican City guidelines operationalize that instinct for institutional life — judicial interpretation, fact analysis, and sentencing reserved to the magistrate.

The programmatic refusal is concentrated in §99–111. Rather than a pin-cite grid, the load-bearing claim can be carried in prose and one set-piece:

> Nor do they have a moral conscience, since they do not judge good and evil, grasp the ultimate meaning of situations, or bear responsibility for consequences.

That sentence is the statecraft seam: one of the world’s oldest legitimacy-bearing offices insists that machine competence is not enough to inherit moral judgment, witness, or rule. §110 presses the political consequence — to “disarm” AI is to discredit the assumption that “technical power automatically confers the right to govern.” Pastoral and formation risks appear in the same register: §100 warns that fluent systems can “weaken personal creativity and judgment”; §118 insists humanity “flourishes not despite limitations, but often through them.”

For singularity-facing work, the question is what synthetic mediation does to formed presence when advice, rhetoric, and witness become scalable. Leo’s answer is assistance without succession — developers bear design vision; deployers bear accountability; pastors and magistrates retain what algorithms can simulate but not carry. Verbatim depth and section-by-section pins remain in the archive capture and in channel notes; the essay carries the transport claim only.

If office, liability, and formation are treated as optional layers on top of scale, the remaining politics will be performed by machines and billed to populations who were told the future had already arrived.

---

## Relation to other layers

| Layer | Holds |
|-------|--------|
| `source-archive/` | Full primaries |
| `statecraft/notes/`, `singularity/notes/` | Verbatim depth, pin-cites, reconsideration reads |
| `essays/` | Transport synthesis (this voice) |
| `skill-write/` | Shorter public derivatives |

**Cross-links:**

- [prose-index.md](prose-index.md) — placement
- [citation-evidence-pattern.md](citation-evidence-pattern.md) — literature matrix exception
- [drafting-topic-lede.mdc](../.cursor/rules/drafting-topic-lede.mdc) — topic-first (essays extend)
- [statecraft-intelligence-essay skill](../.cursor/skills/statecraft-intelligence-essay/SKILL.md) — speaker-hidden genre

**Phase 2 (optional):** full essay → Locals trim ladder doc.

**Phase 3 — Prose Forge lint:** [`docs/prose-forge.md`](prose-forge.md) · `python3 scripts/prose_slop_lint.py` — enforces [Template slop](#template-slop-comparative-voice-ledes) rules SLOP-01–08 (SLOP-03 manual). Wrapper: `python3 scripts/prose_forge.py lint`.

---

## Return paths

- [essays/README.md](../essays/README.md)
- [prose-index.md](prose-index.md)
- [write-operator-preferences.md](skill-write/write-operator-preferences.md)
