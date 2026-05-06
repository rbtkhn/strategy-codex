# Bloom mastery and 2 Sigma â€” adaptation to companion-self / Grace-Mar

**Purpose:** Name **Benjamin Bloomâ€™s mastery-learning frame** and the **2 Sigma** finding (strong tutoring lifts most learners well above group instruction) and map them onto this repoâ€™s **gates, evidence, WORK compression, and containers** â€” without claiming school outcomes or adding automated mastery scores.

**Related lens:** [alpha-mastery-adaptation.md](alpha-mastery-adaptation.md) translates **Alpha Schoolâ€™s** operational mechanics (90% lesson gates, 2-hour block, Time Back) onto the same architecture. This doc stays **Bloom-first**; for Alpha-specific rows and benchmarks, use that file.

**Governed by:** Same boundary as the Alpha doc â€” design vocabulary and honest tooling descriptions, not verified performance data.

---

## What Bloom adds to the conversation

- **Mastery before advance** â€” Learners move on only after **demonstrated** understanding, so partial knowledge does not compound into â€œSwiss cheese.â€
- **Formative use of evidence** â€” Ongoing checks and corrections, not only a final exam.
- **2 Sigma** â€” Bloomâ€™s summary that **one-to-one mastery tutoring** (plus mastery pacing) produced effect sizes near two standard deviations vs conventional group instruction in his studies; later work debates replication and conditions. Here it is an **analogy**: the **Voice** and **operator tools** can play a tutoring-like role **grounded in the Record**, not unbounded model knowledge.

This codebase is **not** a learning management system. The analogy is **adult, self-directed, sovereign** practice on a **cognitive fork**.

---

## Map to companion-self / Grace-Mar

| Bloom idea | companion-self / Grace-Mar meaning | Where it lives |
|------------|-----------------------------------|----------------|
| Clear objectives | Founding intent + seed core facts (when present) | [`reflection-proposals/SEED-founding-intent.md`](../reflection-proposals/) (when present); `seed/minimal-core.json` per [seed-phase-wizard.md](seed-phase-wizard.md) â€” file may not exist until seed phase runs |
| Initial orientation | Hey rhythm + daily intention | [scripts/good-morning-brief.py](../scripts/good-morning-brief.py); `reflection-proposals/DAILY-INTENTION-*.md` |
| Formative evidence | Activity log, staging, approved trail | [`self-evidence.md`](../self-evidence.md), [`recursion-gate.md`](../recursion-gate.md) ([identity-fork-protocol.md](identity-fork-protocol.md)), [`self-archive.md`](../self-archive.md) after merge â€” not a `self-evidence/` directory or a separate `Record/` tree |
| Corrective loop | Contradictions + sovereign gate + merge script | [contradiction-resolution.md](contradiction-resolution.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md), RECURSION-GATE, [scripts/process_approved_candidates.py](../scripts/process_approved_candidates.py); staging conflict checks in `bot/conflict_check.py` â€” **no** `gate-guardian.js` in this repo |
| ~90% â€œmastery before advanceâ€ | Compression / clarity bar before treating work as closed | [scripts/jiang-compress.py](../scripts/jiang-compress.py), [COMPRESSION-ENGINE.md](skill-work/work-jiang/COMPRESSION-ENGINE.md) â€” **operator checklist + JSON schema**, not an automated 90% scorer (see below) |
| 80â€“85% flow zone | Sprint/session difficulty â€œin the zoneâ€ (self-rated) | Optional [sprint-template.md](../research/external/work-jiang/sprints/sprint-template.md); see also [alpha-school-reference.md](skill-work/work-alpha-school/alpha-school-reference.md), [educational-software-history-insights.md](educational-software-history-insights.md) |
| Practice / articulation | THINK vs WRITE containers | [`skill-think.md`](../skill-think.md), [`skill-write.md`](../skill-write.md) ([canonical-paths.md](canonical-paths.md)) |
| Time back | Intention + memory horizons + WORK lanes | good-morning-brief, [memory-template.md](memory-template.md), WORK files under `` |
| Variation reduction | Layer boundaries and identity/library rules | [AGENTS.md](../AGENTS.md), [conceptual-framework.md](conceptual-framework.md), [scripts/identity_library_boundary_rules.py](../scripts/identity_library_boundary_rules.py) â€” **no** `layer-enforcer.py` or `truth-density-score.py` unless added later |
| 1:1 tutoring analog | Recursive Record + Voice (queried, bounded) | [conceptual-framework.md](conceptual-framework.md) (triadic cognition, pipeline) |

---

## What the tooling actually does (no fairy tales)

**`jiang-compress.py` today**

- Runs an **interactive operator checklist** (y/N). Failure exits the script; it does **not** compute a percentage or block saves automatically like an LMS.
- Reads optional **`seed/minimal-core.json`** and **founding intent** paths when they exist.
- Emits **compression JSON** under `research/external/work-jiang/compressions/` and can **print a RECURSION-GATE stub** for manual paste â€” it does **not** merge into `self.md` or `self-evidence.md`.

So the parallel to â€œ90% before the next lessonâ€ is **discipline**: structured prompts toward **one-sentence clarity, linkable evidence, and next actions** before building on an artifact â€” not a hidden autograder.

**RECURSION-GATE**

- The **companion-controlled** integration moment for the Record. Analysts and operators **stage**; only approved paths merge (see AGENTS.md and the process script).

---

## Future / not shipped (v1 doc only)

Not implemented as first-class artifacts in this pass:

- A repo-wide **`progress-unit-tracker.json`** or automated mastery index
- Auto-tuning **good-morning-brief** from numeric â€œscoresâ€
- Mandatory **night reflection** hooks tied to Bloom bands

These can be revisited if the operator wants explicit schemas and scripts.

---

## Grace-Mar / operator notes

Living doc: tighten paths if instance layout changes; keep **template-only** names (`gate-guardian.js`, `layer-enforcer.py`, `truth-density-score.py`, fictional `Record/` trees) out of grace-mar prose unless explicitly labeled **future or external template**.

