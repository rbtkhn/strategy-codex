# Analysis: Grace-Mar museum identity knowledge (archive) (museum knowledge section A)

**Purpose:** Analyze the **museum identity knowledge (archive)** dimension (museum knowledge section A) of the Grace-Mar Record â€” scope, sources, evidence linkage, and alignment with the companion-self model.

**Source:** `self.md` Â§ museum knowledge section A. KNOWLEDGE.  
**Canonical definition:** Facts that entered awareness through observation (AGENTS.md, ID-TAXONOMY, CONCEPTUAL-FRAMEWORK). **museum identity knowledge (archive)** = `self.md` museum knowledge section A. museum knowledge section A includes books and media consumed (from self-evidence.md Â§ I. READING LIST (READ-nnn) or self-library engagement/influence state).

**Date:** 2026-02-26

---

## 1. Scope and Counts

| Metric | Value |
|--------|--------|
| **museum knowledge section A entries** | 36 (LEARN-0001 through LEARN-0036) |
| **Evidence-linked** | 36/36 (every entry has `evidence_id: ACT-XXXX`) |
| **Provenance** | Mix: `curated_by: user` (early); `provenance: human_approved` (from LEARN-0026 onward, plus some earlier) |
| **Date range** | 2026-02-19 to 2026-02-24 |

All entries conform to the protocol: facts only, traceable to an activity (ACT-*). No claim without evidence.

---

## 2. Topic Clusters

**museum identity knowledge (archive)** in the Record clusters as follows:

| Cluster | LEARN IDs | Count | Representative topics |
|---------|-----------|--------|------------------------|
| **US history / presidents** | 0001, 0006, 0007, 0027 | 4 | George Washington, Lincoln (hat, 16th president, Emancipation), John Adams |
| **Space / solar system** | 0002, 0003, 0012, 0013â€“0023 | 13 | Jupiter Great Red Spot, Mars/Olympus Mons, no reptiles on Jupiter; Mercuryâ€“Pluto, Moon, Asteroid Belt (school workbook) |
| **Gemstones / minerals** | 0004, 0005, 0030 | 3 | Gemstones (shiny, rare); gemstones vs stones; diamond hardest |
| **Ballet / classical music** | 0008, 0009, 0026, 0035, 0036 | 5 | Nutcracker, Schubert D845, Swan Lake, Bach Goldberg Variations, Tchaikovsky Andante cantabile |
| **Books / media** | 0010, 0028, 0033 | 3 | The Wild Robot (Roz), Land Before Time 2 (Chomper), The Fox and the Hound (Tod, Copper) |
| **Biology / nature** | 0011, 0034 | 2 | Reptiles (scales, eggs, cold-blooded); extinct |
| **Culture / place** | 0024, 0029, 0031, 0032 | 4 | Egyptian pharaoh/King Tut; Tomb of Pakal (Palenque); Lunar New Year; Vietnamese food/pho |
| **Other** | 0025 | 1 | Black holes (gravity, light) |

**Observations:**
- **Space** dominates (13 entries), largely from one school workbook (ACT-0013) â€” one artifact, many facts; protocol allows multiple LEARN entries per ACT when distinct facts.
- **Presidents, ballet/music, and culture/place** show variety of sources: bot lookup, conversation, KBCP probes, companion report.
- **Reptiles** appear in both knowledge (LEARN-0011) and curiosity (museum knowledge section B); **gemstones** in knowledge and curiosity. No conflict â€” knowledge = â€œlearnedâ€; curiosity = â€œdrawn to.â€ Same topic can sit in both dimensions.

---

## 3. Sources of Knowledge (Evidence Types)

| Source type | ACT range / examples | LEARN count | Notes |
|-------------|----------------------|-------------|--------|
| **Bot lookup** (user asked, system looked up, approved) | ACT-0001â€“0012 | 12 | First pipeline batches; user-initiated lookups |
| **School worksheet** | ACT-0013 (solar system), ACT-0014 (pharaoh), ACT-0037 (extinction) | 13 | LEARN-0013â€“0023 (one ACT), 0024, 0034 |
| **Bot conversation** (expressed/shared, no lookup) | ACT-0016, 0029â€“0031 | 4 | Black holes, Lunar New Year, pho, Fox and the Hound |
| **KBCP (Knowledge Boundary Calibration Probe)** | ACT-0022â€“0026 | 5 | Swan Lake, John Adams, Land Before Time 2, Tomb of Pakal, diamond |
| **Companion report** (â€œwe listenedâ€, â€œwe didâ€) | ACT-0038, 0039 | 2 | Bach Goldberg, Tchaikovsky Andante cantabile |

Evidence linkage is consistent: every LEARN entry has exactly one `evidence_id` pointing to self-evidence.md Â§ V. ACTIVITY LOG. Some ACTs support multiple LEARN entries (e.g. ACT-0013 â†’ LEARN-0013 through LEARN-0023); that is by design (one artifact, many facts).

---

## 4. Schema and Provenance

- **Required fields per entry:** `id`, `date`, `topic`, `source`, `her_understanding`, `evidence_id`.
- **Optional:** `curated_by: user`, `provenance: human_approved`. Newer entries tend to include `provenance: human_approved` (File Update Protocol).
- **No scope/constraint** on any museum knowledge section A entry in the current set; optional per IDENTITY-FORK-PROTOCOL / KNOWLEDGE-BOUNDARY-FRAMEWORK when a belief has a boundary.

---

## 5. Downstream Consumption

| Consumer | How museum knowledge section A is used |
|----------|-------------------|
| **SYSTEM_PROMPT (archive/grace-mar-instance/bot/prompt.py)** | Section â€œYOUR KNOWLEDGE (from observations)â€ â€” compressed bullet list. Not a 1:1 dump of all 36 LEARN entries; summarized by topic (e.g. â€œGeorge Washington as first president, John Adams as 2nd, Abraham Lincoln as 16thâ€). |
| **ANALYST_PROMPT** | Dedup list and â€œKnown topicsâ€ plus â€œIX-A. Knowledge (post-seed)â€ bullets so analyst does not re-stage existing knowledge. |
| **PRP (export_prp.py)** | PRP embeds a compressed knowledge section; source is self.md (museum knowledge section A/B/C). |
| **scripts/metrics.py** | `RecordCompleteness.ix_a` = count of `id: LEARN-NNNN` in self.md (36). Reported in pipeline health. |

**Prompt sync:** The ANALYST â€œIX-A. Knowledge (post-seed)â€ block in prompt.py is a maintained summary. If new LEARN entries are merged into self.md but the prompt section is not updated, the Voice and analyst dedup can drift. Per File Update Protocol, prompt and SELF must be updated together on merge.

---

## 6. Alignment with Companion-Self and Protocol

| Criterion | Status |
|----------|--------|
| **museum identity knowledge (archive)** (= museum knowledge section A) | âœ… ID-TAXONOMY and CONCEPTUAL-FRAMEWORK: **museum identity knowledge (archive)** is `self.md` museum knowledge section A. |
| **Evidence linkage** | âœ… Every LEARN entry has `evidence_id`. |
| **Knowledge boundary** | âœ… Only documented facts; no LLM leak. Sources are bot lookup, conversation, school, KBCP, companion report. |
| **Gated pipeline** | âœ… All entries merged after staging and approval (SESSION-LOG and SELF-ARCHIVE reflect this). |
| **Provenance** | âœ… `curated_by: user` or `provenance: human_approved` present. |

---

## 7. Summary

- **Grace-Mar museum identity knowledge (archive) (museum knowledge section A)** consists of **36 evidence-linked facts** (LEARN-0001â€“LEARN-0036) across space, US history, gemstones, ballet/music, books/media, biology, and culture/place.
- **Sources** are diverse: bot lookups, school worksheets, conversation, KBCP probes, and companion reports. Each entry traces to an ACT-* in EVIDENCE.
- **Protocol and companion-self alignment:** Evidence linkage, knowledge boundary, and gated merge are satisfied. Downstream (prompt, PRP, metrics) consume museum knowledge section A in compressed form; keeping prompt and SELF in sync on merge remains important.

---

*Analysis based on self.md Â§ museum knowledge section A, self-evidence.md, archive/grace-mar-instance/bot/prompt.py, scripts/metrics.py, and AGENTS.md / ID-TAXONOMY.*

