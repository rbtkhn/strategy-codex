# Portable Skills Drift Audit - 2026-05-22

## Scope

This audit reviews every file under [`skills`](.) against two portable-core principles:

1. [`self-llm.txt`](../archive/grace-mar-instance/self-llm.txt) currently resolves to a missing-profile fallback, which means portable skills must not assume repo-local Record files such as `self.md` or `archive/grace-mar-instance/museum-knowledge.md` exist in a new host.
2. [`recursion-gate.md`](../archive/grace-mar-instance/recursion-gate.md) keeps four rules load-bearing:
   - grounded before elegant
   - the agent may stage but may not merge
   - no duplicate lane / no duplicate fact
   - human review remains load-bearing

The objective here was not to rewrite everything. It was to identify duplication or drift from those principles, repair the highest-value seams, and leave a durable receipt with before/after examples.

## Inventory

### Framework and documentation

| File | Status | Notes |
|------|--------|-------|
| [README.md](README.md) | improved | Retitled to strategy-codex; now names portable core principles explicitly. |
| [_schema.md](_schema.md) | improved | Now requires host-equivalent placeholders and stage-only/approval-only language. |
| [manifest.yaml](manifest.yaml) | stable | Inventory source; no principle drift found in this pass. |
| [skill-candidates.md](skill-candidates.md) | stable | Candidate list only. |
| [skills-portable-drift-audit-2026-05-22.md](skills-portable-drift-audit-2026-05-22.md) | improved | This audit artifact; updated to cover the full tree and include before/after examples. |
| [_drafts/README.md](_drafts/README.md) | stable | Correctly frames drafts as non-canonical. |

### Listed portable skills

| Skill | Status | Notes |
|-------|--------|-------|
| [abundance-native-ventures](abundance-native-ventures/SKILL.md) | improved | Removed repo-local Record assumptions; added approval-packet and duplicate-lane discipline. |
| [academy-mirror-sync](academy-mirror-sync/SKILL.md) | stable | Already host-bounded and narrowly scoped. |
| [check-streams](check-streams/SKILL.md) | stable | Good portable glossary and no merge overreach. |
| [cognition-streams](cognition-streams/SKILL.md) | stable alias | Alias-like entry; no urgent drift. |
| [ideation-engine](ideation-engine/SKILL.md) | improved | Added grounding checks, duplicate-lane check, and `extend-existing` outcome. |
| [jurisdiction-campaign-history](jurisdiction-campaign-history/SKILL.md) | stable | Stayed inside research/briefing role. |
| [last30days](last30days/SKILL.md) | stable | Utility skill; no visible gate drift. |
| [packet-before-synthesis](packet-before-synthesis/SKILL.md) | improved | Restored packet-first as holding pattern rather than stealth closure; removed brittle repo-local coupling. |
| [politics-massie](politics-massie/SKILL.md) | stable | Narrow lane skill; no urgent principle conflict. |
| [portable-skills-sync](portable-skills-sync/SKILL.md) | stable | Sync utility already scoped to portable layer. |
| [primary-overhearing-analysis](primary-overhearing-analysis/SKILL.md) | stable | Strong source-hygiene orientation already present. |
| [repo-feedback-prompt](repo-feedback-prompt/SKILL.md) | stable | No Record/gate ambiguity found. |
| [repo-hygiene-pass](repo-hygiene-pass/SKILL.md) | stable | Good bounded scope. |
| [skill-narrative](skill-narrative/SKILL.md) | stable | Canonical copy looks fine; draft duplicate remains in `_drafts/`. |
| [strategy-notebook-expert-cross-weave](strategy-notebook-expert-cross-weave/SKILL.md) | improved | Converted heavy repo-local assumptions into host-equivalent notebook placeholders. |
| [strategy-notebook-guest-canon-note](strategy-notebook-guest-canon-note/SKILL.md) | improved | Converted host-stream note logic into portable placeholders and stronger boundary language. |
| [transcript-cleanup](transcript-cleanup/SKILL.md) | stable | Procedural cleanup skill; no gate conflict. |
| [transcript-proper-noun-normalization](transcript-proper-noun-normalization/SKILL.md) | stable | Focused normalization skill. |
| [work-jiang-ingest-fallback](work-jiang-ingest-fallback/SKILL.md) | stable | Bounded ingest fallback. |
| [youtube-raw-input-transcript](youtube-raw-input-transcript/SKILL.md) | stable | Good procedural scope. |

### Drafts

| Draft | Status | Notes |
|------|--------|-------|
| [_drafts/academy-statecraft-drafting](_drafts/academy-statecraft-drafting/SKILL.md) | draft | Not part of listed portable set. |
| [_drafts/daily-brief-regen-merge](_drafts/daily-brief-regen-merge/SKILL.md) | draft | Review later for gate-language tightness before listing. |
| [_drafts/expert-forecast-ledger](_drafts/expert-forecast-ledger/SKILL.md) | draft | Research-only for now. |
| [_drafts/marandi-state-extraction](_drafts/marandi-state-extraction/SKILL.md) | draft | Lane-specific draft. |
| [_drafts/mercouris-daily-continuity-extraction](_drafts/mercouris-daily-continuity-extraction/SKILL.md) | draft | Lane-specific draft. |
| [_drafts/observability-to-cadence-capture](_drafts/observability-to-cadence-capture/SKILL.md) | draft | Good candidate for later portable review. |
| [_drafts/parsi-diplomacy-extraction](_drafts/parsi-diplomacy-extraction/SKILL.md) | draft | Lane-specific draft. |
| [_drafts/persian-regime-adaptive-strategy](_drafts/persian-regime-adaptive-strategy/SKILL.md) | draft | Strategy draft only. |
| [_drafts/printing-press-scrape-creators](_drafts/printing-press-scrape-creators/SKILL.md) | draft | No action in this pass. |
| [_drafts/ritter-warning-extraction](_drafts/ritter-warning-extraction/SKILL.md) | draft | No action in this pass. |
| [_drafts/russian-endurance-compression-strategy/notes.md](_drafts/russian-endurance-compression-strategy/notes.md) | draft note | Companion notes for the Russian/Persian dual-stack lens; useful context, not a listed portable skill. |
| [_drafts/russian-endurance-compression-strategy/SKILL.md](_drafts/russian-endurance-compression-strategy/SKILL.md) | draft | No action in this pass. |
| [_drafts/skill-narrative/SKILL.md](_drafts/skill-narrative/SKILL.md) | duplicate draft | Likely duplicate of canonical `skill-narrative`; keep draft-only until reconciled. |

## Main drift patterns

### 1. Repo-local Record assumptions inside portable cores

Several skills still read like they live inside one specific instance, referencing `self.md`, `self-library.md`, `self-skills.md`, `self-archive.md`, or concrete notebook files as if those were universal.

That drifts from [`self-llm.txt`](../archive/grace-mar-instance/self-llm.txt), which currently demonstrates the opposite: a portable consumer may not have those files at all.

### 2. Approval language that was close to merge language

Some skills said things like "gate-ready proposal" or "draft recursion-gate-ready text." That is not catastrophic, but it blurs the line between proposal packaging and authority.

[`recursion-gate.md`](../archive/grace-mar-instance/recursion-gate.md) is stricter: the agent may stage; it may not merge; human review remains load-bearing.

### 3. Duplicate-lane blindness

Several ideation or venture-oriented skills were good at generating possibilities, but not explicit enough about checking whether the idea already had an owning lane, note, or experiment.

That conflicts with the no-duplicate-lane principle in the gate.

### 4. Strategy-notebook portability gaps

Two strategy skills were conceptually strong but practically too tied to specific files like `daily-strategy-inbox.md`, `days.md`, `meta.md`, `STATUS.md`, `speaker-lattice.md`, and `strategy-commentator-threads.md`.

Portable skills can keep the pattern, but they need host-equivalent placeholders rather than fixed local paths as the main contract.

### 5. Elegant synthesis outrunning evidence routing

`packet-before-synthesis` had the right instinct, but it still leaned on repo-specific files and needed a harder statement that packet-first is a holding pattern, not a backdoor way to smuggle stronger claims through a lower-maturity surface.

## Improved skills

### 1. abundance-native-ventures

**Why it was chosen**

This skill touched both Record-adjacent language and new-surface creation pressure, which made it a high-value place to restore approval-first wording and duplicate-lane checks.

**Before**

```md
- `self.md` - identity and operating paradigm
- `self-library.md` - supporting references and source material
- `self-skills.md` - demonstrated capability and skill inventory
- `self-archive.md` / evidence surfaces - receipts, outcomes, and prior experiments
```

```md
3. **Proposal drafting**
   - Draft recursion-gate-ready text for adding an operating paradigm, skill, or library item.
```

**After**

```md
| Purpose | Portable placeholder |
|---------|----------------------|
| Identity and operating paradigm | `<operator-profile>` |
| Supporting references and source material | `<source-library>` |
| Demonstrated capability and skill inventory | `<skill-inventory>` |
| Receipts, outcomes, and prior experiments | `<evidence-surface>` |
```

```md
3. **Approval packet drafting**
   - Draft host-ready approval text for adding an operating paradigm, skill, or library item.
   - Keep the proposal balanced: benefits, risks, counterarguments, duplicate-lane check, and evidence required.
```

**Net effect**

The skill now preserves the venture pattern while no longer assuming Grace-Mar-style surfaces or blurring packet-drafting with merge authority.

### 2. ideation-engine

**Why it was chosen**

This skill was already strong, but it lacked an explicit check for duplicate-lane sprawl and needed a more honest way to say "the right answer may be to extend an existing lane."

**Before**

```md
5. **Prepare approval memo**
   - Recommend approve, refine, or archive.
```

**After**

```md
5. **Prepare approval memo**
   - Recommend approve, refine, extend-existing, or archive.
```

```md
## Grounding checks
1. Is the demand signal sourced, observed, or merely analogical?
2. Is there already an owning lane, memo, or experiment that should be extended instead of cloned?
```

**Net effect**

The skill is still generative, but it now better reflects the gate's anti-duplication principle and makes evidence basis explicit in the output template.

### 3. packet-before-synthesis

**Why it was chosen**

This skill is directly about source hygiene and maturity ladders, so any drift here matters more than drift in a purely procedural utility.

**Before**

```md
- Use [packet-crosswalk.md](../docs/skill-work/work-strategy/packet-crosswalk.md) if the choice is not obvious.
```

```md
- If yes, do not collapse them into one ... sentence yet.
```

The method was good, but it leaned on repo-specific artifacts and did not explicitly say that packet-first must not become stealth closure.

**After**

```md
## Portable rule
Packet-first is a source-bound holding pattern, not stealth closure.

- Preserve the seam before strengthening the claim.
- Keep official-primary, attributed gloss, and later corroboration visibly separate.
- Do not use packet work to smuggle a canon claim, Record claim, or approval-ready synthesis through a lower-maturity route.
```

**Net effect**

The skill now states its portable doctrine plainly and does not depend on local strategy-codex files to make sense.

### 4. strategy-notebook-expert-cross-weave

**Why it was chosen**

This was one of the clearest cases where a good local workflow had been copied into the portable layer without enough host abstraction.

**Before**

```md
1. Both experts appear in the **commentator roster** (`strategy-commentator-threads.md` pattern) ...
2. Source lines exist ... in **`daily-strategy-inbox.md`**
```

```md
Under **`chapters/YYYY-MM/days.md`**, in the correct **`## YYYY-MM-DD`** block:
```

**After**

```md
| Purpose | Portable placeholder |
|---------|----------------------|
| Commentator roster with stable expert ids | `<expert-roster>` |
| Daily inbox or ingest queue | `<daily-inbox>` |
| Calendar notebook or daily page surface | `<calendar-notebook>` |
```

```md
Use this skill when two indexed **`thread:<expert_id>`** lines in a host daily inbox should become **one explicit judgment seam** on a dated notebook page without collapsing distinct evidence chains.
```

**Net effect**

The portable skill now preserves the cross-weave pattern while no longer pretending every host has the same strategy-codex notebook layout.

### 5. strategy-notebook-guest-canon-note

**Why it was chosen**

This skill had the same portability issue as expert-cross-weave, but with an additional ontology risk: a host-local speaker arc can too easily sound like a permanent taxonomy or canon claim.

**Before**

```md
6. **Wire the notebook surfaces**
   - Add a citation from the guest row in `speaker-lattice.md`
   - Add or refine the `thread:<expert_id>` row in `strategy-commentator-threads.md`
```

```md
## Placement rule
- Preferred home: `codex/<year>/<host-stream>/<host>-<guest>-speaker-arc.md`
```

**After**

```md
| Purpose | Portable placeholder |
|---------|----------------------|
| Canonical host x guest raw inputs | `<stream-raw-input>` |
| Host-stream routing surface | `<speaker-routing>` |
| Lattice or speaker index surface | `<lattice-surface>` |
| Thread roster or expert continuity surface | `<thread-surface>` |
```

```md
- Do not promote a host-local arc into Record-bearing truth, permanent taxonomy, or a cross-host canon claim without an explicit human decision.
```

**Net effect**

The skill keeps the speaker-arc ontology but now names the host-local boundary much more clearly.

## Documentation updates made in this pass

### README.md

Added an explicit portable-core principles section so the layer itself now states:

- use host-equivalent placeholders
- propose or stage only; never merge
- grounded before elegant
- no duplicate-lane sprawl
- human pass remains load-bearing

### _schema.md

Added explicit schema guidance that:

- portable skills should prefer host-equivalent placeholders
- portable cores may describe proposal or stage-only outputs
- portable cores should not imply direct merge authority

## Quantified impact

### Coverage

- `39` files under [`skills`](.) were explicitly accounted for in this audit.
- `5` high-risk portable skills were materially improved.
- `5` generated `.cursor/skills/*/SKILL.md` derivative runtime copies were regenerated to stay aligned with the portable source layer.
- `3` documentation surfaces were strengthened:
  - [README.md](README.md)
  - [_schema.md](_schema.md)
  - [skills-portable-drift-audit-2026-05-22.md](skills-portable-drift-audit-2026-05-22.md)

### Portability gain

Across the five improved skills, audited repo-local path assumptions on the high-risk surfaces dropped to `0` matches for:

- `self.md`
- `self-library.md`
- `self-skills.md`
- `self-archive.md`
- `daily-strategy-inbox.md`
- `strategy-commentator-threads.md`
- `speaker-lattice.md`
- `chapters/YYYY-MM/days.md`

Those same five skills now contain `26` explicit host-equivalent placeholders:

- `abundance-native-ventures`: `5`
- `ideation-engine`: `6`
- `packet-before-synthesis`: `0`
- `strategy-notebook-expert-cross-weave`: `9`
- `strategy-notebook-guest-canon-note`: `6`

### Governance hardening

The five revised portable skills now contain `38` explicit governance or authority terms (`approval`, `stage`, `merge`, `Record`) across their bodies.

The meaningful effect is qualitative as well as quantitative:

- `abundance-native-ventures` now frames proposal work as `approval packet` drafting rather than quasi-merge language.
- `ideation-engine` now includes `extend-existing` as a first-class outcome, directly reducing duplicate-lane proliferation.
- `packet-before-synthesis` now explicitly states that packet-first is a source-bound holding pattern, not stealth closure.

### Change volume

In the tracked workset for this pass:

- `294` insertions
- `164` deletions

Within the five portable source skills alone:

- `135` insertions
- `77` deletions

Within the five regenerated `.cursor/skills` derivative runtime copies:

- `139` insertions
- `80` deletions

This was therefore a real contract rewrite on the riskiest portable seams, not a cosmetic copy edit.

### Verification

- [`validate_skills.py`](../scripts/validate_skills.py) passed with the bundled runtime.
- Forbidden-string spot checks passed on the revised skills.
- [`sync_portable_skills.py --verify`](../scripts/sync_portable_skills.py) now passes in the bundled runtime without `PyYAML`, via a stdlib fallback for the manifest/frontmatter subset used by the portable-skill sync path.
- After adding that fallback, the five affected `.cursor/skills/*/SKILL.md` derivative runtime copies were regenerated through the live sync script.

## What remains stable but worth watching

- `skill-narrative` has a likely duplicate draft in `_drafts/skill-narrative`.
- Several drafts may deserve future review before listing, especially if they start to inherit lane-specific merge assumptions or fixed path contracts.
- A later pass could normalize wording across all stable skills so terms like "approval process," "host equivalent," and "Record-bearing" are more uniform.

## Verification target for the next step

The next verification step should confirm:

1. the five revised skills still sync cleanly through the portable-skills tooling,
2. no manifest or sync assumptions broke,
3. the updated portable docs and skill bodies remain internally consistent.

## Follow-on fix completed

After the main audit pass, the previously blocked verifier path was repaired directly in [sync_portable_skills.py](../scripts/sync_portable_skills.py).

Benefit:

- the portable layer is self-checking again in the bundled runtime,
- the five touched derivative runtime copies can now be reproduced by script,
- the environment no longer depends on `PyYAML` for this narrow portable-skill sync workflow.

## Toscanini verifier receipt

Verified now:

- the portable source layer syncs and verifies in the bundled runtime without `PyYAML`,
- the five touched derivative runtime copies can be regenerated by the live sync script,
- the fallback parser accepts the current manifest and frontmatter subset used by this portable-skill workflow.

Would be falsified by:

- introducing YAML features outside the documented subset, such as block scalars, inline collections, anchors, aliases, or merge keys,
- a future `sync_portable_skills.py --verify` failure in the bundled runtime,
- divergence between a regenerated derivative runtime copy and its portable source.

Standard regression check:

- run `sync_portable_skills.py --verify`,
- run a one-skill `--dry-run`,
- run `validate_skills.py`,
- keep the portable manifest and frontmatter inside the parser's explicitly accepted subset.
