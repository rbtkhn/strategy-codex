# State Lane Development Roadmap

WORK only; not Record.

Purpose: give every statecraft lane the same development sequence so each state can eventually stand as an independent repo without losing the shared Statecraft grammar.

## Source Flow

Statecraft lanes use a three-step source chain:

1. CIV-MEM informs `civilization/` and `empire/` equally.
2. `civilization/` names inherited code, durable fear, legitimacy memory, and successor-stable interests.
3. `empire/` names outward control drives, instruments, overreach patterns, and limiting principles.
4. `state/`, `transactions/`, and `helix.md` draw from `civilization/` and `empire/`, not directly from CIV-MEM.

This keeps CIV-MEM from becoming an all-purpose citation sink. It is upstream memory. The state lane must translate it into two governed folders before drafting policy.

## Standard Folder Spine

Each state lane should keep this minimum spine:

- `civilization/README.md`: the lane's inherited code and successor-stable legitimacy grammar.
- `civilization/seed-patterns.md`: three to five source-backed patterns ready for expansion.
- `empire/README.md`: the lane's outward control grammar and limiting principle.
- `empire/seed-instruments.md`: three to five instruments ready for expansion.
- `state/`: regulated doctrine and decision rules built from the two upstream folders.
- `helix.md`: the balancing mechanism between civilization and empire.
- `transactions/`: current-event and scenario drafts that test the lane against reality.

## Development Passes

### Pass 1: Seed

For each lane, add three civilization patterns and three empire instruments. Each seed should include a CIV-MEM source pointer, statecraft use, and failure mode.

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
- CIV-MEM references remain source pointers, not operational commands.

## Quality Tests

- **Equal upstream test:** Does CIV-MEM inform both civilization and empire, or only one side?
- **No direct-state shortcut:** Does `state/` draw from lane-local civilization and empire notes rather than raw CIV-MEM?
- **Successor-stability test:** Would the pattern still matter after a leadership or regime change?
- **Overreach test:** Does each empire instrument name the point where control starts damaging the civilization it claims to protect?
- **Extraction test:** Could this state lane become a repo tomorrow with coherent internal navigation?
