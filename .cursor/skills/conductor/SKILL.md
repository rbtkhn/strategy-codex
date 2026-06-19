---
name: conductor
preferred_activation: conductor
description: "DEPRECATED entry (Phase 2 compression): redirect to coffee hub + attention phrases. Triggers toscanini/karajan/conductor <name> → say coffee and pick hub A–D per CONDUCTOR-COMPRESSION-SPEC §10. Legacy Conductor Action Menu archived; use object rituals + extended coffee_close."
---

# Conductor — redirect stub (Phase 2 compression)

**Status:** **Redirect only** — standalone Conductor ritual is **compressed** into **`coffee`** + **default-from-hub attention** + **extended `coffee_close`**. Do **not** emit Conductor Action Menu (Allegro/Andante/Scherzo/Finale) on new sessions.

**Operator SSOT:** [CONDUCTOR-COMPRESSION-SPEC.md](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md) — cheat sheet **§10**, object rituals **§5**, close contract **§7**.

**Coffee SSOT:** [coffee SKILL](../coffee/SKILL.md) — Step 2 hub + default attention; legacy conductor triggers redirect here.

---

## When operator says a master slug or `conductor`

| Instead of (deprecated) | Do this |
|-------------------------|---------|
| `toscanini`, `furtwangler`, `karajan`, `kleiber`, `bernstein` | **`coffee`** → pick hub **A–D**; apply **default attention** from hub (§4 of compression spec) |
| `conductor` / `conductor kleiber` | **`coffee`** only — infer hub from Step 1; override with phrase (`C stakes pass`, `D long arc pass`) in same message |
| Conductor Action Menu A–D | **Object ritual** steps for the named object ([§5.1 intake closeout](../../../docs/skill-work/work-coffee/menu-reference.md#statecraft-intake-closeout) is reference) |
| `coffee_conductor_outcome` alone | **Extended `coffee_close`** only (Phase 3 — outcome lines deprecated) |

**Do not** ask "which attention?" — infer from hub letter unless operator overrides with a plain phrase.

**Do not** run `build_conductor_revisit_block` or a second A–D menu inside conductor. Open loops: coffee Step 1 **Recent rhythm**, bootstrap **Open loops**, live **72h watch** when statecraft is active.

---

## Close shape (substantive passes)

```bash
python scripts/log_coffee_close.py -u strategy-codex \
  --picked D --outcome partial --readiness execution_ready \
  --object-ref <path> --falsify "<one-line test>" --verdict shaped
```

**Dual-write ended (Phase 3):** extended `coffee_close` is **required**; do **not** append new `coffee_conductor_outcome` for strategy-codex.

**`verdict=promote|shaped`:** append **one RLJ entry** ([recursive-learn](../recursive-learn/SKILL.md)) before closing the arc.

**`bravo` / `weak`:** [§5.4 compression spec](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#54-bravo--weak-on-object-rituals) — `coffee_close outcome=done` or ack + fresh hub.

---

## Legacy archive (read-only)

Historical voice prototypes, HARD-PROTOCOL movement menu, and cadence `picked=conductor conductor=<slug>` rows remain **read-only** for rollups and archaeology.

- [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) — legacy pass shape (compatibility)
- [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../codex/CONDUCTOR-IMPROVEMENT-LOOP.md) — predecessor loop; successor = compression spec
- [conductor-proposal-lenses.md](../../../docs/skill-work/work-dev/conductor-proposal-lenses.md) — **keep** for coding-agent proposal posture (not conductor ritual)
- [HARD-PROTOCOL.md](HARD-PROTOCOL.md) — archived protocol; do not use for new operator entry

**Rollback:** If compression falsifiers fire, see [§9 rollback](../../../docs/skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md#9-compression-falsifiers-and-rollback) — restore this skill body from git; mark spec **paused**.
