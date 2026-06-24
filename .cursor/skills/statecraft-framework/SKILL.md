---
name: statecraft-framework
description: Diagnose a live statecraft object through the Civilizational Statecraft Framework before drafting. Use when the operator needs the governing term named first (civilization, empire, entropy, faith, science, or memory), then memory rhythm/era sections when motion or shelf choice governs, dominant layer, likely outsider misread, likely failure layer, and the right downstream retrieval surface. Do not use for volume-front-door hardening, lane synthesis artifacts, or direct transaction drafting.
preferred_activation: statecraft-framework
activation: statecraft-framework
portable: true
version: 0.2.3
category: judgment-enhancement
status: active
scope_class: repo-governed
tags:
- operator
- statecraft
- civ-state
- doctrine
- routing
portable_source: skills/statecraft-framework/SKILL.md
synced_by: sync_portable_skills.py
---
# Statecraft Framework

**Preferred activation (operator):** say **`statecraft-framework`**.

Use this skill to diagnose a live object through the **Civilizational Statecraft Framework** before lane descent, clause drafting, or transaction design.

Compatibility note: older references to **`civ-state-frame`** mean this skill. **`desire`** as a governing term is retired — read appetite, spectacle, and compensatory overreach under **empire**.

This is not a drafting skill. It is a pre-draft diagnosis and routing skill.

## Core law

The framework reads live objects through **six governing terms** — rhythm and era law live on **memory** (not separate pages):

**Governing terms**

- **civilization** — inherited order, legitimacy substrate, continuity-bearing form
- **empire** — outward instrument, amplification, coercion stack
- **entropy** — historical causes and manifestations of civilizational degradation (war, revolution, disease, famine, ecological disaster, compound shocks)
- **faith** — sacred, moral, covenantal truth-order
- **science** — technical, procedural, evidentiary truth-order
- **memory** — continuity, wound, civilizational rhythm, era law, retrieval entry

**Temporal grammar** (sections on `public/civ-state/theory/memory.md`):

- **civilizational rhythm** — beautify → amplify → degrade (civilization → empire → entropy)
- **era law** — Ancient → Cybernetic shelf placement

The operator task is not to recite all six files. It is to identify the **governing term first**, then open memory **sections** when motion or era governs, then the likely misread and failure layers.

**Ship-bound theory SSOT:** `public/civ-state/theory/<term>.md`  
**Volume-local theory (when present):** `public/civ-state/volumes/<civ>/theory/<term>.md` — case history linking up to whole-work siblings.

Older families such as `god`, `lit`, `art`, `geo`, `war`, and `peace` are **secondary retrieval-and-expression families**, not primary ontology.

## Boundary

- WORK only; not Record.
- Do not use before the object is minimally verified and named — return to `state-deploy` first if needed.
- Do not draft transactions, lane books, or clause packages directly from this skill unless scope widens explicitly.
- Do not substitute Sacred Grammar, `state-memory`, helix, or transaction router surfaces — this skill chooses among them.
- If the object feels smooth too early, run a short false-elegance check.

## Workflow

1. **Identify the live object.** One line: crisis object, argument, lane problem, or draft target.

2. **Run the six governing questions.**
   - what civilizational inheritance is at stake?
   - what empire instrument is carrying it?
   - what faith-order authorizes it?
   - what science-order authorizes it?
   - what memory sustains it?
   - what historical shock (war, revolution, famine, plague, ecological rupture) governs degradation?

3. **Name the governing term first.**  
   Pick one: civilization · empire · entropy · faith · science · memory.

4. **Place motion and era when relevant** (open [memory.md](../../public/civ-state/theory/memory.md) sections — not a separate governing pick):
   - rhythm beat: beautify / amplify / degrade → `#civilizational-rhythm`
   - era shelf: which era carries the object → `#era-law`

5. **Name the likely outsider misread.**  
   What layer gets flattened or mistaken?

6. **Name the likely failure layer.**  
   What breaks settlement or drives overreach?

7. **Choose the return path.**
   - civilization or faith → Sacred Grammar · legitimacy surfaces
   - memory → `state-memory` · continuity notes · `#civilizational-rhythm` · `#era-law`
   - empire → empire / helix / transaction / routing surfaces (include overreach reads here)
   - science → procedural / verification / implementation
   - entropy → shock typology · memory degrades-beat section · era/sources shelves · [cross-case essay](../../public/civ-state/essays/cross-case-recurrence-and-sovereignty.md)

8. **Open the theory page for the governing term.**  
   Whole-work: `public/civ-state/theory/<term>.md`  
   Volume case read: `public/civ-state/volumes/<civ>/theory/<term>.md` when that shelf exists.

9. **Recommend a secondary family only if it helps.**  
   `god`, `lit`, `art`, `geo`, `war`, or `peace` after the route is clear.

10. **Kick back when the wrong tool is active.**  
    Missing verified facts, lane ownership, or settled crisis object → `state-deploy`.

## False-Elegance Check

- Wrong read 1: flattering but shallow term an outsider picks too quickly
- Wrong read 2: mechanically clever term a drafter picks too quickly
- Corrected read: which term still makes the next retrieval move concrete?

## Compact rules

**Faith / science:** coequal truth-orders — do not collapse one into the other.

**Entropy:** name one load-bearing historical manifestation or compound (war, revolution, disease, famine, ecological disaster). Do not conflate empire-overreach or civilization/empire divergence with entropy — those reads stay on empire, civilization, and memory `#civilizational-rhythm`.

**Memory:** without memory, phase and era are inert — open `#civilizational-rhythm` or `#era-law` when motion or shelf choice governs, even if another term won the governing read.

## Output

```markdown
**Civilizational Statecraft Framework**
- Live object:
- Governing term:
- Memory rhythm / era placement (if load-bearing):
- Likely outsider misread:
- Likely failure layer:
- Best return path:
- Theory page:
- If not ready, return to:
- Secondary family, if useful:
```

## Success condition

The next move becomes obvious: governing term, dominant failure, misread, and retrieval surface.

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- governing term and dominant failure layer must be named

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review

## Repo notes

- Bounded operator checklist: `statecraft/states/civilization-empire-faith-science-memory-entropy-retrieval-checklist.md`
- Cross-case comparative entry: `public/civ-state/essays/cross-case-recurrence-and-sovereignty.md`

## Preferred maintenance commands after skill edits

```powershell
python scripts/sync_portable_skills.py --skill statecraft-framework
python scripts/sync_portable_skills.py --verify --skill statecraft-framework
python scripts/validate_skills.py
```


## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical theory shelf: [theory/README.md](/C:/dev/strategy-codex/statecraft/states/theory/README.md) · [Form](/C:/dev/strategy-codex/statecraft/states/theory/form.md)
- Canonical retrieval matrix: [statecraft/states/indexes/source-retrieval-matrix.md](/C:/dev/strategy-codex/statecraft/states/indexes/source-retrieval-matrix.md)
- Primary deep-grammar shelf: [statecraft/states/sacred-grammar/README.md](/C:/dev/strategy-codex/statecraft/states/sacred-grammar/README.md)
- Use this skill before lane descent when the governing pair is unclear or when a live object is being flattened into one layer too quickly.
- Secondary families such as `god`, `lit`, `art`, `geo`, `war`, and `peace` should be opened only after the governing pair is named.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-framework
python scripts/sync_portable_skills.py --verify --skill statecraft-framework
python scripts/validate_skills.py
```
