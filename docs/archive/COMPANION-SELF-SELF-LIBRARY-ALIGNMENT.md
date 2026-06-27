# companion-self alignment â€” removed operator-books symlink template (recommendation 4)

**Purpose:** Make **`platform/template/self-library.md`** in [companion-self](https://github.com/rbtkhn/companion-self) an **instance-agnostic governance package** (boundary + schema + **empty `entries:`**), aligned with:

- New instances bootstrapped from **companion-self** (removed operator-books symlink governance on **template** `main`),
- [archive/boundary-museum-knowledge-self-library.md](boundary-self-knowledge-self-library.md) (grace-mar canonical ontology),
- The companion-self template [`platform/template/self-library.md`](https://github.com/rbtkhn/companion-self/blob/main/platform/template/self-library.md) (governance + empty shelf).

This doc lives in **grace-mar** because the **PR is opened on companion-self**; grace-mar tracks the **intent** and **proposed file body** for operators.

---

## Current upstream state (as of 2026-03)

On **`main`**, companion-selfâ€™s [`platform/template/self-library.md`](https://github.com/rbtkhn/companion-self/blob/main/platform/template/self-library.md) is a **large** file (LIB rows cloned from grace-marâ€™s corpus). That is **useful as a reference corpus** but it is **not** a neutral template for **every** new instance: it bakes in grace-mar-specific rows and obscures the **museum knowledge vs removed operator-books symlink** boundary for first-time operators.

**Alignment goal:** Template = **governance + empty shelf**; optional **example / mirror** docs can hold dense LIB lists **outside** `platform/template/self-library.md`.

---

## Proposed direction (companion-self PR)

1. **Replace** `platform/template/self-library.md` with a **short** file: rule-of-one-line boundary, pointer to IFP / boundary doc in-repo, **schema** pointer (companion-self may mirror or link [library-schema.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/library-schema.md) from grace-mar or add `docs/library-schema.md` in template).
2. **Move** the existing long YAML / LIB list to something like **`docs/self-library-seed-example.md`** or **`platform/template/self-library.EXAMPLE-corpora.md`** (name TBD in PR) â€” clearly labeled **optional**, **not** copied into new instances by default.
3. Update **`how-instances-consume-upgrades.md`** (or template README) so new instances know: start **empty**, add LIB rows only via gate.

---

## Proposed `platform/template/self-library.md` body (paste into companion-self PR)

Paths below assume companion-self repo layout (`docs/identity-fork-protocol.md` exists upstream). Adjust links if companion-self uses different filenames.

```markdown
# removed operator-books symlink â€” template scaffold

**removed operator-books symlink** is the **governed reference** layer (lookup-first sources, canon, influence) â€” **not** museum knowledge (museum knowledge section A). Identity-facing facts stay in `self.md` + gate.

**Rule (one line):** museum knowledge is identity-facing; removed operator-books symlink is reference-facing. Do not store civilization-scale reference as museum knowledge section A merely because the companion may use it in lookup.

**Protocol:** [docs/identity-fork-protocol.md](../../docs/identity-fork-protocol.md)

**Entries schema:** follow the instanceâ€™s library schema (see grace-mar [`docs/library-schema.md`](https://github.com/rbtkhn/grace-mar/blob/main/docs/library-schema.md) if not yet mirrored in this repo).

**Template default:** no prefilled LIB rows â€” add rows through the normal gated pipeline when the companion approves.

---

## Entries

```yaml
entries: []
```

---

## Optional

If this template ships an **example corpus** for operators (e.g. public-domain story index), keep it in **`docs/â€¦`** or a clearly named **EXAMPLE** file â€” **not** as the default `entries:` block for new forks.
```

---

## PR status (2026-03-23) â€” **merged**

**Merged to companion-self `main`:** fast-forward to **`288b4386684e076df894536624308e69305ae229`** ([commit on `main`](https://github.com/rbtkhn/companion-self/commit/288b4386684e076df894536624308e69305ae229)).

**Upstream changes:** minimal `platform/template/self-library.md`; legacy LIB rows in `docs/self-library-example-corpus-grace-mar-derived.md`; `template-manifest.json` + `how-instances-consume-upgrades.md` updated.

---

## PR checklist (operator)

| Step | Action |
|------|--------|
| 1 | ~~Merge to companion-self `main`~~ â€” **Done** (`288b438`). |
| 2 | Optional: delete remote branch `template-self-library-governance` on GitHub if still present. |
| 3 | ~~TEMPLATE-BASELINE + MERGING-FROM~~ â€” **Updated** in grace-mar. |
| 4 | Periodic: re-diff grace-mar `self-library.md` vs [companion-self template](https://github.com/rbtkhn/companion-self/blob/main/platform/template/self-library.md) when auditing template drift. |

---

## Relation to other instances

Additional companions deploy from **companion-self** in **their own repositories**; they are not hosted inside the grace-mar repo. Each instanceâ€™s `self-library.md` should stay aligned with **template governance** on `main`; apply template wording improvements in that instanceâ€™s workspace when the template updates.

