"""One-shot patch: civ-state-essay v0.2.6 literary/epic witnesses + carthage row."""
from pathlib import Path

SKILL = Path("skills/civ-state-essay/SKILL.md")
t = SKILL.read_text(encoding="utf-8")

GEO_ROW = (
    "| **Geo-branch (Rome)** | `essay-{vol}-{slug}.md` · tier geo-branch | "
    "Same template + meta + registry | **Same word + quote bands** as civic-chain when operator sets Rome pilot QA; "
    "standalone rival/place arc — not genesis→augustus chain order |"
)

if GEO_ROW not in t:
    anchor = (
        "| **Civic-chain** | `essay-{vol}-{slug}.md` | Generic essay template + `{vol}` meta sidecar + registry | "
        "~2,400–2,600 body words; ~450–550 quoted primary/pre-modern in `\"…\"` (Rome genesis–augustus) |"
    )
    if anchor not in t:
        raise SystemExit("geo-row anchor missing")
    t = t.replace(anchor, anchor + "\n" + GEO_ROW, 1)

OLD_STATE = """### Rome civic-chain essay state (QA class — check before edit)

Pin from target file + [`release-history.md`](../../public/civ-state/docs/release-history.md) when unsure.

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Genesis | `essay-rome-genesis.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · Gibbon Notes-only |
| Republic | `essay-rome-republic.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · L55 institutions |
| Caesar | `essay-rome-caesar.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |
| Augustus | `essay-rome-augustus.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |

After any **humanizing** pass on a node, default QA class for later edits on that file → **humanize** until operator folds bands."""

NEW_STATE = """### Rome essay-rome state (QA class — check before edit)

Pin from target file + [`release-history.md`](../../public/civ-state/docs/release-history.md) when unsure.

**Civic-chain four:**

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Genesis | `essay-rome-genesis.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · Gibbon Notes-only · *Aeneid* I.1–2 |
| Republic | `essay-rome-republic.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · L55 institutions · Punic compress (no Virgil body) |
| Caesar | `essay-rome-caesar.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes |
| Augustus | `essay-rome-augustus.md` | **`civic-chain-rome-humanize`** | v0.1.59 source-discipline · reception → Notes · *Aeneid* VI · *Georgics* I |

**Geo-branch (Rome pilot — civic-chain bands, no chain read order):**

| Essay | File | QA `--class` (current) | Pass notes |
|-------|------|------------------------|------------|
| Carthage | `essay-rome-carthage.md` | **`civic-chain-rome-humanize`** | rival-system · historiography + epic memory · *Aeneid* I + IV · anti-dup vs republic Livy XXII.54 |

After any **humanizing** pass on a node, default QA class for later edits on that file → **humanize** until operator folds bands."""

if OLD_STATE in t:
    t = t.replace(OLD_STATE, NEW_STATE, 1)
elif "### Rome essay-rome state" not in t:
    raise SystemExit("essay state block missing")

EPIC = """
### Literary / epic witnesses (Rome — poets in body)

Poets count as **primary ancient** body sources — same `"…"` weave as historians — but they witness **literary memory and legitimation**, not battle chronology. Do not substitute epic for Polybius/Livy on dates, orders of battle, or treaty text.

**Three witness types (classify before QA):**

| Type | Examples | Body job |
|------|----------|----------|
| **Chronicle / oratory** | Polybius, Livy, Appian, Cicero, Plutarch lives | What happened; institutions; turning points |
| **Law / inscription / document** | Twelve Tables refs, *Res Gestae*, official language | Public rule and formula |
| **Epic / literary memory** | Virgil, Horace, Ovid when load-bearing | How Romans **imagined** rivals, foundation, settlement — pairs with chronicle |

**Epic audit triggers** — before humanize QA on Rome `essay-rome-*`, grep body for: *Roman memory* · *memory Rome* · *annihilation* · *readers would* · rival-place mythology · *delenda* / curse / avenger tradition. If triggers fire and no epic/poet quote is woven, check volume map below — do not ship historiography-only when prose claims literary memory.

**Rome volume map (quote homes — dedupe by book, not by author):**

| Material | Primary essay | Notes |
|----------|---------------|-------|
| *Aeneid* **I.1–2** — arms and the man, Troy → Lavinium | `essay-rome-genesis` | Foundation epic frame |
| *Aeneid* **I** — Dido's Carthage / harbor city | `essay-rome-carthage` | Rival place (Book I harbor beat) |
| *Aeneid* **IV** — Dido's curse / avenger | `essay-rome-carthage` | Epic memory of Punic rival; pair with Cato/Appian |
| *Aeneid* **VI** — shield, *imperium sine fine* | `essay-rome-augustus` | Augustan legitimation |
| *Georgics* **I** — renewal / agriculture idiom | `essay-rome-augustus` | Peace idiom |
| Republic § Punic Wars (compress) | `essay-rome-republic` | **No Virgil body** — depth defers to carthage geo-branch |

**Theory pointer (placement law, not quote home):** [`rome-memory.md#faith-spine-mythology`](../../public/civ-state/volumes/rome/rome-memory.md#faith-spine-mythology) · [`faith-history-rome.md`](../../public/civ-state/volumes/rome/essays/faith-history-rome.md) euhemerism boundary — mythic substrate ≠ historiographical claim.

**Embed rules:** one **short** epic quote at a memory or legitimation turn; **swap-don't-pad** at quote band; pair epic with chronicle or oratory (e.g. Dido curse → Cato fig); active intro in authorial voice — avoid meta-only wrappers (*moralized rhetoric*, *One modern analyst*). Optional Notes label: `*(Epic memory — not chronicle SSOT)*`. Reuse PD edition from [`rome-bibliography.md`](../../public/civ-state/volumes/rome/rome-bibliography.md); book-level routing may also live in essay `.meta.yaml` — skill does not duplicate full lattice.
"""

if "### Literary / epic witnesses" not in t:
    ins_anchor = (
        "- **Band floor after reception removal:** expand **ancient** quotes and embodied beats "
        "in the same turn — do not backfill quoted band with modern reception.\n"
    )
    if ins_anchor not in t:
        raise SystemExit("epic insert anchor missing")
    t = t.replace(ins_anchor, ins_anchor + EPIC + "\n", 1)

t = t.replace(
    "**Current coverage (v0.2):** civic-chain four — genesis · republic · caesar · augustus.",
    "**Current coverage (v0.2.6):** civic-chain four — genesis · republic · caesar · augustus · geo-branch **carthage**.",
    1,
)

if "version: 0.2.6" not in t.split("---", 2)[0]:
    t = t.replace("version: 0.2.5", "version: 0.2.6", 1)

SKILL.write_text(t, encoding="utf-8")
print("patched", SKILL)
