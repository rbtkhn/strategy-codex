---
name: "statecraft-framework"
preferred_activation: "statecraft-framework"
description: "Diagnose a live statecraft object through the Civilizational Statecraft Framework before drafting. Use when the operator needs the governing pair named first: civilization/empire, faith/science, or memory/desire; then the dominant layer, likely outsider misread, likely failure layer, and the right downstream retrieval surface. Do not use for volume-front-door hardening, lane synthesis artifacts, or direct transaction drafting."
portable: true
version: "0.1.0"
tags:
  - "operator"
  - "statecraft"
  - "civ-state"
  - "doctrine"
  - "routing"
portable_source: "skills-portable/statecraft-framework/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Statecraft Framework

**Preferred activation (operator):** say **`statecraft-framework`**.

Use this skill to diagnose a live object through the **Civilizational Statecraft Framework** before lane descent, clause drafting, or transaction design.

Compatibility note: older references to **`civ-state-frame`** mean this skill. In live doctrine, `civ-state` now means the **civilization-state** object under interpretation, not the name of this framework.

This is not a drafting skill. It is a pre-draft diagnosis and routing skill.

## Core law

The Civilizational Statecraft Framework reads live objects through three governing pairs:

- **civilization / empire**
- **faith / science**
- **memory / desire**

The operator task is not to recite all six terms. It is to identify the **governing pair first**, then the dominant layer inside that pair, then the most likely misread and failure layers.

Older families such as `god`, `lit`, `art`, `geo`, `war`, and `peace` are **secondary retrieval-and-expression families**, not primary ontology. Use them only after the governing pair is clear and only when they materially sharpen the read.

## Boundary

- WORK only; not Record.
- Do not use this skill before the object is minimally verified and named. If the object is still a live-event intake or ownership call, return to `state-deploy` first.
- Do not draft transactions, lane books, or clause packages directly from this skill unless the operator separately widens scope.
- Do not use this skill as a substitute for Sacred Grammar, `state-memory`, helix, or transaction router surfaces. It exists to choose among them.
- Use lane-local or CIV-STATE objects after diagnosis; do not remain at frame level longer than needed.
- If the object feels smooth too early, run a short false-elegance check before committing to the pair.

## Workflow

1. **Identify the live object.**
   Name the crisis object, argument, lane problem, routing uncertainty, or draft target in one line.
   If the object is still unstable as recent news, verify and classify it through `state-deploy` first.

2. **Run the six governing questions.**
   Ask:
   - what civilizational inheritance is at stake?
   - what empire instrument is carrying it?
   - what faith-order authorizes it?
   - what science-order authorizes it?
   - what memory sustains it?
   - what desire distorts or accelerates it?

3. **Name the governing pair first.**
   Choose the load-bearing pair:
   - `civilization / empire`
   - `faith / science`
   - `memory / desire`

4. **Name the dominant layer inside that pair.**
   Say which side of the pair is actually governing the object.

5. **Name the likely outsider misread.**
   What is the layer most likely to be flattened, ignored, or mistaken by outsiders?

6. **Name the likely failure layer.**
   Which layer is most likely to distort the object, break the settlement, or cause overreach?

7. **Choose the return path.**
   Route by dominant layer:
   - `civilization` or `faith` -> Sacred Grammar or adjacent legitimacy surfaces
   - `memory` -> `state-memory`
   - `empire` -> empire / helix / transaction / routing surfaces
   - `science` -> procedural / governance / verification / implementation surfaces
   - `desire` -> mutation / escalation / overreach surfaces

8. **Recommend a secondary family only if it helps.**
   Only after the route is clear, name `god`, `lit`, `art`, `geo`, `war`, or `peace` if one will materially sharpen retrieval or stress-testing.

9. **Kick back when the wrong tool is active.**
   If the diagnosis reveals the operator still lacks:
   - verified live facts,
   - honest lane ownership,
   - or a settled crisis object,
   send the object back to `state-deploy` rather than pretending the framework can finish the job alone.

## False-Elegance Check

Run a short stress test whenever the first governing-pair answer sounds elegant before retrieval consequences are obvious.

- Wrong read 1: what flattering but shallow pair would an outsider pick too quickly?
- Wrong read 2: what mechanically clever pair would a drafter pick too quickly?
- Corrected read: which pair still makes the next retrieval move concrete?

If the corrected read does not make the next surface more obvious than the wrong reads, the diagnosis is not ready yet.

## Compact rule for faith / science

`faith` and `science` are coequal truth-orders.

- Do not collapse sacred authorization into technical competence.
- Do not collapse technical competence into sacred legitimacy.
- In modern objects, many failures come from pretending one truth-order can silently substitute for the other.

## Output

Use this shape by default:

```markdown
**Civilizational Statecraft Framework**
- Live object:
- Governing pair:
- Dominant layer:
- Likely outsider misread:
- Likely failure layer:
- Best return path:
- If not ready, return to:
- Secondary family, if useful:
```

## Success condition

This skill succeeds when the next move becomes obvious:

- which pair governs
- which layer dominates
- what others are most likely to misread
- what is most likely to fail
- where the operator should retrieve next

## Repo notes

- Use this skill to keep `Pope Leo on AI` lane-split honest. The `statecraft` version owns papal office, legitimacy, Rome as civilizational carrier, authority under acceleration, and settlement-bearing implications.
- If a Pope Leo read is primarily about mediation, anthropology, authorship, synthetic judgment, or human formation, hand it back to `singularity` rather than flattening it into legitimacy talk too early.
- `Barnes on AI` is `statecraft`-only in this repo. Treat it as a speaker-owned side topic about bubble dynamics, incentive structure, energy dependence, and command pressure, not as a generic singularity AI essay.

## Preferred maintenance commands after skill edits

```powershell
python scripts/sync_portable_skills.py --skill statecraft-framework
python scripts/sync_portable_skills.py --verify --skill statecraft-framework
python scripts/validate_skills.py
```


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Canonical doctrine note: [Civilizational Statecraft Framework](/C:/dev/strategy-codex/statecraft/states/civilization-empire-faith-science-memory-desire.md)
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
