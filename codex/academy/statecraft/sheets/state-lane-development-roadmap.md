# State Lane Development Roadmap


Purpose: give every statecraft lane the same development sequence so each state can eventually stand as an independent repo without losing the shared Statecraft grammar.

End state: each lane becomes a book and a machine. The book side is a complete, compelling, evidence-backed civilizational volume. The machine side is a governed recursive update loop that lets statecraft work improve the lane without automatic rewriting.

## Source Flow

Statecraft lanes use this source chain:

1. CIV-EMP informs `civilization/` and `empire/` equally.
2. `civilization/` names inherited code, durable fear, legitimacy memory, and successor-stable interests.
3. `empire/` names outward control drives, instruments, overreach patterns, and limiting principles.
4. `state/`, `transactions/`, and `helix.md` draw from `civilization/` and `empire/`, not directly from the upstream source base.

CIV-EMP is the academy-statecraft local source base derived from the two-volume Civilization and Empire frame. This keeps CIV-EMP from becoming an all-purpose citation sink: the state lane must translate it into two governed folders before drafting policy.

## Standard Folder Spine

Each state lane should keep this minimum spine:

- `civilization/README.md`: the lane's inherited code and successor-stable legitimacy grammar.
- `civilization/seed-patterns.md`: three to five source-backed patterns ready for expansion.
- `empire/README.md`: the lane's outward control grammar and limiting principle.
- `empire/seed-instruments.md`: three to five instruments ready for expansion.
- `state/`: regulated doctrine and decision rules built from the two upstream folders.
- `helix.md`: the balancing mechanism between civilization and empire.
- `transactions/`: current-event and scenario drafts that test the lane against reality.
- `updates/pending.md`: the membrane where live outputs stage recursive update candidates before book surfaces change.

## Development Passes

### Pass 1: Seed

For each lane, add three civilization patterns and three empire instruments. Each seed should include a CIV-EMP source pointer, statecraft use, and failure mode.

### Pass 2: Deepen

Promote each seed into its own note only when it becomes active in a transaction, current-event brief, or comparative statecraft test. Avoid expanding notes merely because more history is available.

### Pass 3: Regulate

Update `helix.md` with a crosswalk showing how each civilization pattern authorizes an empire instrument, how that instrument protects the civilization, and where statecraft must restrain it.

### Pass 4: Extract

Before a lane becomes an independent repo, verify that it can stand without reaching back to shared files except through explicit source pointers:

- The lane has a readable README.
- Civilization and empire folders each have their own pattern/instrument index.
- State rules cite lane-local civilization and empire files.
- Transactions cite lane-local state rules.
- CIV-EMP references remain source pointers, not operational commands.

### Pass 5: Recurse

After a current-event brief, transaction, objection matrix, or scenario test, stage candidate improvements in `<lane>/updates/pending.md`:

- new civilization pattern
- new empire instrument
- new state regulator
- new helix crosswalk
- new transaction precedent
- new falsifier or revisit trigger

Recursive updates must be reviewable before integration. The lane learns through governed acceptance, not silent self-rewrite.

Use [Recursive Update Candidate Template](../templates/recursive-update-candidate.md). Keep v1 Markdown-only: no IDs, scripts, or validation are required until real use proves the queue shape.

## Quality Tests

- **Equal upstream test:** Does CIV-EMP inform both civilization and empire, or only one side?
- **No direct-state shortcut:** Does `state/` draw from lane-local civilization and empire notes rather than raw CIV-EMP?
- **Successor-stability test:** Would the pattern still matter after a leadership or regime change?
- **Overreach test:** Does each empire instrument name the point where control starts damaging the civilization it claims to protect?
- **Extraction test:** Could this state lane become a repo tomorrow with coherent internal navigation?
- **Book test:** Could a serious reader follow the civilizational story without needing the whole academy workspace?
- **Machine test:** Can a new statecraft output produce structured update candidates for the lane?
- **Membrane test:** Does the candidate sit in `updates/pending.md` before any book-surface edit?
