# CIV-STATE Era Hardening Checklist

Use this checklist when hardening or reviewing CIV-STATE bibliography structure, volume chronology, or era-facing retrieval doctrine.

## Chronology Law

- `Ancient` -> `476`
- `Medieval` -> `1453`
- `Colonial` -> `1815`
- `Industrial` -> `1991`
- `Cybernetic` -> `post-1991`

These are form-historical boundaries, not just date labels.

## Structure Checks

- Does every civilization volume expose a bibliography front door?
- Do Rome, China, and Persia expose `Ancient / Medieval / Colonial / Industrial / Cybernetic` primary-source files?
- Do Russia and America expose `Medieval / Colonial / Industrial / Cybernetic` primary-source files and avoid Ancient bibliography files?
- Do all five expose Cybernetic?

## Shelf Checks

- Does every Industrial shelf terminate at `1991`?
- Does every Cybernetic shelf begin after `1991`?
- Are post-1991 source doors kept out of Industrial?
- Do bibliography indexes keep primary sources central and bounded secondary supports subordinate?

## README Checks

- Do volume READMEs match the bibliography chronology?
- Do top-level CIV-STATE and statecraft doctrine files use the same `1991` Industrial/Cybernetic boundary?
- Do late-opening cases read as documentary exceptions rather than malformed volumes?

## Validation

Run:

```bash
python scripts/validate_civ_state_eras.py
```

Use the script for structural and doctrinal drift detection. Use this checklist for operator judgment and review.
