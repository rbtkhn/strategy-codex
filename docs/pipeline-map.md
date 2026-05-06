# Pipeline Map

**Purpose:** Diagram the feedback loops that feed the cognitive fork â€” which modules feed which, where data is transformed, and where loops exist or are missing.

**See also:** [architecture.md](architecture.md), [grace-mar.mdc](../.cursor/rules/grace-mar.mdc), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md) (identity-diff at the gate)

---

## Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                           INPUT CHANNELS                                         â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Channel 1: Bot (Automated)     â”‚  Channel 2: Operator (Manual)                  â”‚
â”‚  Telegram â†’ Analyst â†’ PENDING   â”‚  "We [did X]" â†’ Cursor â†’ PENDING               â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚                                        â”‚
                 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                      â–¼
                         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                         â”‚     RECURSION-GATE      â”‚
                         â”‚  (integration moment:   â”‚
                         â”‚   user approve/reject)  â”‚
                         â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                      â”‚ approved
                                      â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                           INTEGRATION                                            â”‚
â”‚  self.md  â”‚  self-evidence.md (ACT-*)  â”‚  session-log.md  â”‚  bot/prompt.py              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                      â”‚
                                      â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                           FORK STATE                                             â”‚
â”‚  SELF (IX-A/B/C)  â”‚  SKILLS (THINK/WRITE/WORK)  â”‚  EVIDENCE (module logs)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Recursive Learning Process

**Recursive learning** means the Record improves itself over time: each cycle refines the model of the person, and the refined Record shapes the next cycle's inputs and interpretations.

### Definition

The **recursive learning process** is:

1. **Input** â€” Activity (conversation, artifact, "we did X") enters the system.
2. **Signal detection** â€” Analyst compares input to current Record; identifies new knowledge, curiosity, personality.
3. **Staging** â€” Candidates written to RECURSION-GATE.
4. **Integration moment** â€” User approves or rejects.
5. **Merge** â€” Approved content integrated into SELF, EVIDENCE, prompt.
6. **Updated Record** â€” Fork state now reflects the new content.
7. **Cycle repeats** â€” Next input is analyzed *against the updated Record* (dedup, richer context). Voice responses use the updated profile. Proposed activities (future) could use SKILLS container edge.

**Recursion** = The output of step 6 becomes input to step 1 (indirectly): the Record influences what gets detected (analyst dedup), what the Voice says (SYSTEM_PROMPT), andâ€”when implementedâ€”what activities get proposed (container edge).

### Current vs. Full Recursion

| Loop | Status | Description |
|------|--------|-------------|
| **Forward** (input â†’ Record) | âœ… Implemented | Activity â†’ detect â†’ stage â†’ approve â†’ merge |
| **Record â†’ Voice** | âœ… Implemented | Prompt embeds Record; Voice speaks from it |
| **Record â†’ Analyst** | âœ… Implemented | Dedup list prevents re-staging known content |
| **Record â†’ Proposed activities** | âŒ Not implemented | SKILLS container edge could drive "propose activity at edge" |

The edgeâ†’quest loop (Record proposes activities at the container boundary) would close the recursion: the Record would influence *what the companion is invited to do next*, creating new input. See Gaps below.

### Cybernetic Framing

The pipeline is a **cybernetic loop** (Wiener): feedback corrects drift. Entropy (forgotten details, LLM leak, stale profile) is countered by sustained input and approval. Session continuity (read SESSION-LOG, RECURSION-GATE before starting) closes the loop across sessions.

---

## Channel 1: Bot Pipeline

```
User message (Telegram)
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Grace-Mar reply  â”‚  â† SYSTEM_PROMPT (SELF, SKILLS, EVIDENCE inline)
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â”œâ”€â”€[if lookup triggered]â”€â”€â–º LIBRARY reference lane first â†’ if hit: REPHRASE; if miss: LOOKUP_PROMPT â†’ REPHRASE_PROMPT â†’ reply
          â”‚
          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Analyst (async)  â”‚  â† ANALYST_PROMPT, compares to profile for dedup
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â”œâ”€â”€[signal found]â”€â”€â–º stage_candidate() â†’ recursion-gate.md **before** `## Processed`
          â””â”€â”€[NONE]â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º (no staging)
```

**Bot feeds:** SELF (IX-A Knowledge, IX-B Curiosity, IX-C Personality) via lookup and conversation signals. Does **not** directly feed SKILLS modules or EVIDENCE module logs (THINK/WRITE/WORK).

**Bot produces:** ACT-* entries (activity log) when candidates are approved. Each approved candidate becomes an ACT-* + SELF entry + prompt.py update.

---

## Channel 2: Operator Pipeline

```
User says "we [did X]" (Cursor)
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Signal detection â”‚  Manual analysis â€” identify knowledge, curiosity, personality
â”‚  (human + AI)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Stage candidate  â”‚  Write to recursion-gate.md with analysis
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â–¼
    [same integration as Channel 1]
```

**Operator feeds:** Any observed activity â€” school work, art, overheard moments, real-world events. Same destination: RECURSION-GATE â†’ SELF, EVIDENCE (ACT-*), etc.

---

## Pillar Evidence Flows

### WRITE (EVIDENCE Â§ II. WRITING LOG)

```
Physical artifact (handwritten)
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  User captures    â”‚  Photograph â†’ save to artifacts/
â”‚  (manual)         â”‚  Add entry to self-evidence.md Writing Log
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â”œâ”€â”€â–º skills.md WRITE (vocabulary, complexity, style)
          â””â”€â”€â–º SELF.linguistic_style, SELF.interests, SELF.emotional_patterns
```

**Automation:** None. Fully manual. No bot feed.

---

### READ (EVIDENCE Â§ I. READING LIST)

```
Books / articles consumed
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  User logs        â”‚  Add entry to self-evidence.md Reading List (READ-*)
â”‚  (manual)         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â”œâ”€â”€â–º skills.md THINK (comprehension, vocabulary, interests)  â† direct
          â”‚
          â””â”€â”€â–º SELF IX-A/B/C  â† NOT automatic; only via RECURSION-GATE + approve
```

**Do not assume** logging READ-* or updating THINK also updates SELF.IX. For identity lines (what she *knows* about the book, sustained curiosity, stance), stage separate candidates and approve. Full ritual: [we-read-think-self-pipeline.md](we-read-think-self-pipeline.md).

**Operator convention:** When the operator says **"we finished [book]"** or **"we read [title]"**, treat it as a pipeline invocation. Run signal detection and stage a candidate that can create a READ-* entry (or a LEARN-* / curiosity candidate that references the book so THINK and SELF.IX can be updated on approval). Do not ignore book-completion signals.

**Minimal READ entry shape** (for staged candidates): `id: READ-XXXX`, `title`, `date`, `evidence_tier` (e.g. 4 OBSERVED), and 1â€“2 comprehension or interest notes. See [evidence-template.md](evidence-template.md) Â§ III for full structure.

**Automation:** None for bot. Operator-triggered: "we finished [X]" / "we read [X]" â†’ stage READ or LEARN candidate. **Gap:** Bot conversations about books could feed interest signals, but those go to SELF IX-B (curiosity), not to THINK module. No structured READ evidence from bot.

---

### WORK creation (EVIDENCE Â§ III. CREATION LOG â€” BUILD container)

```
Physical artifact (artwork, collage, etc.)
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  User captures    â”‚  Photograph â†’ save to artifacts/
â”‚  (manual)         â”‚  Add entry to self-evidence.md Creation Log
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â”œâ”€â”€â–º skills.md BUILD (originality, elaboration, flexibility)
          â””â”€â”€â–º SELF.reasoning_patterns, SELF.interests
```

**Automation:** None. Fully manual. No bot feed.

---

## Canonical Artifact Taxonomy

When saving retained visual evidence under `artifacts/`, default to these high-frequency classes:

| Class | Typical examples | Usual evidence surface |
|------|-------------------|------------------------|
| **Writing sample** | journal page, story, copied text, reflection, school writing | `WRITE-*` entry in EVIDENCE Â§ II |
| **Drawing / illustration** | free drawing, character art, imaginative scene | `CREATE-*` entry in EVIDENCE Â§ III |
| **Worksheet / school page** | science worksheet, reading response, vocabulary page | Usually `WRITE-*`; sometimes `ACT-*` if the artifact supports multiple signals |
| **Craft / collage / physical project** | collage, cutout, 3D craft, poster | `CREATE-*` entry in EVIDENCE Â§ III |
| **Multi-page packet** | booklet, worksheet sequence, multi-page assignment | One parent `ACT-*` plus linked `WRITE-*` / `CREATE-*` entries as needed |
| **Scratch / whiteboard thinking** | planning page, labeling exercise, rough problem-solving | `WRITE-*` or `ACT-*` depending on whether text or process is primary |
| **Reading-adjacent artifact** | book response page, read-aloud follow-up, favorite-book drawing | `WRITE-*`, `CREATE-*`, or `ACT-*` depending on dominant modality |
| **Skill-work project artifact** | plan, checklist, mockup, poster, territory-specific deliverable | Usually `CREATE-*` or `ACT-*` |
| **Meaningful digital output** | typed page, app-made creative work, designed graphic | Match content type: `WRITE-*`, `CREATE-*`, or `ACT-*` |
| **Progress comparison snapshot** | before/after work, growth comparison over time | Usually linked from `ACT-*`; may reference multiple artifact files |

### Naming convention

- Save files in lowercase under `artifacts/`.
- Prefer existing evidence IDs in filenames when known:
  - `write-0007-title-slug.png`
  - `create-0011-title-slug.jpg`
  - `act-0045-title-slug-page-1.png`
- If an activity has multiple pages, append `-page-1`, `-page-2`, etc.
- Avoid generic root-level names like `Image_*.jpg`; rename on save so the file already carries its evidence context.
- If uncertain whether something is `WRITE-*` or `CREATE-*`, decide by dominant signal:
  - text / authored words -> `WRITE-*`
  - visual making / design / artwork -> `CREATE-*`
  - mixed packet or multi-signal event -> `ACT-*` can be the parent evidence anchor

---

## SELF â† Pillar Feedback (from ARCHITECTURE)

| Pillar activity | Feeds SELF |
|-----------------|------------|
| WRITE | linguistic_style (primary), interests, emotional_patterns |
| THINK | interests, preferences, values |
| WORK (creation) | reasoning_patterns, interests |

---

## Integration Step (File Update Protocol)

The approval step is the **integration moment** â€” the conscious gate where the companion (Mind) chooses what enters the Record. When candidates are **approved**, merge into **all** of:

| File | Update |
|------|--------|
| `self.md` | IX-A, IX-B, IX-C entries (merged) |
| `self-evidence.md` | New ACT-* in Activity Log |
| `recursion-gate.md` | Move candidate to Processed |
| `session-log.md` | Session record |
| `bot/prompt.py` | YOUR KNOWLEDGE, YOUR CURIOSITY, YOUR PERSONALITY + analyst dedup list |

---

## Gaps and Missing Loops

| Gap | Description | Potential fix |
|-----|-------------|---------------|
| **THINK has no bot feed** | Bot conversations mention books, but THINK module (comprehension, vocabulary) has no automated input. Reading List is empty. | Add analyst signal for "book discussed" â†’ stage candidate that could create READ-* or link to interest. Or: operator workflow for "we finished [book]." |
| **WRITE / WORK (creation) fully manual** | No automation for artifact capture. User must photograph, save, and write EVIDENCE entry. | Optional: upload flow (e.g. Telegram photo â†’ staging for EVIDENCE), or template script for new WRITE/WORK entries. |
| **Edge â†’ quest feedback** | Container edge (SKILLS) could drive "propose activity" but there is no automated quest generator. | Future: script that reads SKILLS, infers edge, outputs suggested activities. |
| ~~No pipeline event log~~ | ~~Staging and approval implicit in file edits~~ | âœ… Implemented: `pipeline-events.jsonl` â€” bot emits `staged`; operator runs `emit_pipeline_event.py applied CANDIDATE-XX` when processing. |

---

## Counterfactual Pack (Emulation Harness)

`scripts/run_counterfactual_harness.py` runs adversarial probes against the emulation. Probes stress the knowledge boundary, LLM-leak resistance, and in-scope behavior. Run before prompt changes to detect regressions.

```bash
python scripts/run_counterfactual_harness.py
```

---

## Loop Summary

| Loop | Exists? | Frequency |
|------|---------|-----------|
| Bot â†’ Analyst â†’ PENDING â†’ Integration â†’ SELF, prompt | âœ… Yes | Per exchange (when signal found) |
| Operator â†’ PENDING â†’ Integration â†’ SELF, EVIDENCE | âœ… Yes | Per "we [did X]" |
| WRITE artifact â†’ EVIDENCE â†’ SKILLS, SELF | âœ… Yes | Manual, per artifact |
| READ artifact â†’ EVIDENCE â†’ SKILLS, SELF | âš ï¸ Sparse | Manual, 0 entries so far |
| WORK (creation) artifact â†’ EVIDENCE â†’ SKILLS, SELF | âœ… Yes | Manual, per artifact |
| SKILLS/edge â†’ propose activity â†’ artifact â†’ EVIDENCE | âŒ No | Not implemented. Would close recursive loop. |

---

*Last updated: February 2026*

