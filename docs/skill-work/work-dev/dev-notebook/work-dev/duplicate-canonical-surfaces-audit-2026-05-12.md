# Duplicate canonical surfaces audit - 2026-05-12

## Purpose

Isolate the "duplicate canonical surfaces" hazard from the rest of the dirty tree and distinguish:

- true membrane danger
- documented optional surfaces that only look dangerous
- naming-contract ambiguity that can create false duplicates even when the files themselves are legitimate

This is a `work-dev` membrane audit note, not a Record change and not a gate artifact.

## Short verdict

The repo does **not** primarily suffer from a simple "too many root files" problem.

The sharper hazard is a **three-part authority ambiguity**:

1. some root-level files are **optional compatibility or derived surfaces** but can be mistaken for canonical authority
2. some genuinely canonical root surfaces exist **untracked**, which weakens membrane clarity
3. the repo still carries an inconsistent naming contract between **`skill-*`** and **`self-skill-*`** language

So the right diagnosis is:

- **not** "delete all apparent duplicates"
- **yes** "clarify which surfaces are canonical, optional, derived, or compatibility-only"

## What is not actually the duplicate problem

### 1. `self-evidence.md` is not a rival to `self-archive.md`

Per [canonical-paths.md](../../../../canonical-paths.md):

- `self-archive.md` is the canonical evidence file
- `self-evidence.md` is an optional compatibility pointer for old bookmarks

The hazard is not that both files exist.
The hazard is that older docs and scripts still sometimes talk as if `self-evidence.md` were the main evidence body.

### 2. `self-history.md` is not a stealth Record file

Per [canonical-paths.md](../../../../canonical-paths.md), `self-history.md` is an optional **derived dual log**.

Its existence is legitimate.
The membrane risk is only if someone mistakes it for a merge-authority surface.

### 3. `SELF-LIBRARY/` is not a duplicate of `self-library.md`

The architecture docs distinguish:

- `self-library.md` = governed library file
- `SELF-LIBRARY/` = navigator / discoverability tree

So the directory and the file are not duplicates in purpose.
They only become a membrane problem if one is treated as authoritative over the other without that distinction being stated.

### 4. `self-work.md` is adjacent, not identity-canonical

`self-work.md` is explicitly a coordination surface, not SELF-KNOWLEDGE.

Its root presence is not itself the duplicate-canonical hazard.

## What is the real hazard

### 1. Untracked canonical root surfaces

The most serious membrane issue is when a file that is supposed to be canonical exists at repo root but is still untracked or migration-ambiguous.

Current examples:

- `self-library.md`
- `self-history.md` (optional, but still a named standard surface)
- `self-evidence.md` (compatibility pointer, but currently floating)

Why this matters:

- an operator can see a valid-looking canonical path
- but Git history and review discipline do not yet treat it as settled terrain
- that weakens confidence about what is live doctrine versus migration residue

### 2. `skill-*` versus `self-skill-*` naming drift

This is the sharpest conceptual hazard.

The repo currently supports language like:

- `skill-think.md`
- `skill-write.md`
- `skill-steward.md`

but also documents split-template language like:

- `self-skill-think.md`
- `self-skill-write.md`
- `self-skill-steward.md`

The result is not one broken file.
The result is a naming contract that can generate **false duplicates in the operator's mind**:

- are `skill-think.md` and `self-skill-think.md` the same thing?
- is one canonical and one legacy?
- should docs link one while scripts read the other?

Right now, the answer is not stated cleanly enough in one place.

### 3. Mixed-age documentation around evidence and skills

There is clear drift across docs and scripts:

- newer doctrine strongly centers `self-archive.md`
- older or mixed-era docs still mention `self-evidence.md` as if it were the active evidence body
- some docs treat `skill-think.md` / `skill-write.md` as normal instance files
- some newer docs frame the split as `self-skill-*`

This means the membrane problem is partly semantic:

- the repo can contain legitimate files
- yet still feel duplicate because the naming contract is under-specified

## Working classification

### Legitimate canonical or standard surfaces

- `self.md`
- `self-knowledge.md`
- `self-archive.md`
- `self-memory.md`
- `self-skills.md`
- `recursion-gate.md`
- `self-moonshots.md`

### Legitimate optional / compatibility / derived surfaces

- `self-evidence.md` - compatibility pointer
- `self-history.md` - derived dual log
- `self-work.md` - coordination surface
- `SELF-LIBRARY/` - navigator tree beside `self-library.md`

### Membrane hazard surfaces

- untracked `self-library.md`
- untracked `self-evidence.md`
- untracked `self-history.md`
- untracked `skill-think.md`
- untracked `skill-write.md`
- untracked `skill-steward.md`

The main risk is **authority ambiguity**, not file count.

## Recommended next hardening slice

### A. Declare the active skill-file naming contract

One doc should plainly answer:

- for this repo, are the active root files `skill-think.md` / `skill-write.md` / `skill-steward.md`?
- or are those transitional names and `self-skill-*` is the intended end state?

Until that is explicit, the repo will keep generating false duplicate anxiety.

### B. Normalize the evidence-language contract

Audit and update mixed-age docs so they consistently say:

- `self-archive.md` = canonical evidence body
- `self-evidence.md` = optional compatibility pointer only

### C. Decide which untracked root surfaces are meant to live

For each of:

- `self-library.md`
- `self-history.md`
- `self-evidence.md`
- `skill-think.md`
- `skill-write.md`
- `skill-steward.md`

decide whether it is:

1. canonical and should be tracked
2. optional but should still be tracked
3. migration residue and should be removed
4. generated / compatibility-only and should perhaps be gitignored or rebuilt intentionally

## Best concise interpretation

The duplicate-canonical-surfaces problem is real, but it is **narrower and more semantic** than it first appears.

The main danger is:

- **half-migrated authority language**

not:

- mere root-level abundance

That means the safest next membrane move is to harden the naming and authority contract before doing any broad cleanup.
