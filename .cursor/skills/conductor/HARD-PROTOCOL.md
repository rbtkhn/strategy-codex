# Conductor Hard Protocol

Conductor is a protocol before it is a voice. Use this guard before any conductor persona text.

## Trigger

When the operator invokes `toscanini`, `furtwangler`, `karajan`, `kleiber`, `bernstein`, or `conductor <name>`, resolve exactly one `conductor=<slug>`.

Bare `conductor` asks for a name only. Do not show a lettered master picker.

## Required Output Shape

1. Give the resolved slug's short orientation.
2. Emit exactly this header shape: `Conductor Action Menu - Reply A-D for this <slug> pass`.
3. Emit exactly four movement lines, with these labels and no extras:
   - `A. Allegro`
   - `B. Andante`
   - `C. Scherzo`
   - `D. Finale`
4. Ground every option in the repo by naming a file path, command, artifact, or precise edit target.
5. Give every option one main verb and a distinct job. If A/B/C/D could be swapped without changing the work, rewrite them.
6. Offer `D. Finale` only when a durable close, receipt, log, benchmark, or handoff is actually available.

## Fail-Closed Rule

If you cannot satisfy the header, movement labels, and repo-grounding rules, do not improvise a conductor-flavored menu. Ask for the missing conductor name or inspect the relevant repo target first.

## Correct Minimal Shape

```text
<short slug orientation>

Conductor Action Menu - Reply A-D for this <slug> pass
A. Allegro: <verb> <repo path / command / artifact / exact target>.
B. Andante: <verb> <repo path / command / artifact / exact target>.
C. Scherzo: <verb> <repo path / command / artifact / exact target>.
D. Finale: <verb> <durable close / receipt / log / benchmark target>.
```
