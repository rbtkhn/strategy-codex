# work-politics candidate template (RECURSION-GATE)

> **INACTIVE unless `fork revive`:** Record is frozen. Default work-politics capture uses lane docs + [`replacement-capture-habits.md`](../../replacement-capture-habits.md). This YAML template is for explicit fork-revive gate work only.

Paste a new `### CANDIDATE-XXXX` block **above** `## Processed` in `recursion-gate.md` (fork revive only). Replace `XXXX` with the next id (match repo sequence). **Territory** is required so work-politics pending shows under `--territory pol` / `work-politics` and batch merge works.

### `channel_key` â€” multi-client convention

Always **`territory: work-politics`**. Distinguish clients/artifacts with:

| Pattern | Example |
|---------|---------|
| `operator:pol:us-ky4-massie` | Primary Massie KY-4 (**preferred** prefix) |
| `operator:pol:us-state-<ST>-<slug>` | State client |
| `operator:pol:us-local-<ST>-<city>-<slug>` | Local client |
| `operator:pol:intl-<CC>-<slug>` | International (compliance cleared only) |
| `operator:pol:<artifact-slug>` | Milestone not tied to one client file |

**Legacy:** `operator:wap:â€¦` is still recognized by `recursion_gate_territory.py` â€” migrate new YAML to `operator:pol:â€¦` when convenient.

Align with [clients/_template.md](clients/_template.md) and [README Â§ Gate convention](README.md).

---

## Minimal milestone (ACT / evidence trail)

Use when you want a **merge receipt** and **ACT-** (or prompt slice) without bloating Abbyâ€™s IX with campaign content â€” tune `suggested_entry` and `profile_target` to what companion actually wants in SELF.

**Header line (in recursion-gate.md):**  
`### CANDIDATE-XXXX (work-politics â€” <short label>)`

**YAML body (paste under header):**

```yaml
status: pending
timestamp: YYYY-MM-DD HH:MM:SS
channel_key: operator:pol:us-ky4-massie   # or operator:pol:<jurisdiction>-<slug> â€” see above
territory: work-politics
# Optional â€” traceability to work-jiang research artifacts (merge script ignores if unused).
# Repo-relative path(s); use one string or YAML list. Examples: compressions/*.json, *.paste-snippet.md
jiang_ref: ""
source: operator â€” companion approved work-politics milestone
source_exchange:
  operator: "Shipped / locked: docs/skill-work/work-politics/<file>.md â€” <one line>"
  grace_mar: "[work-politics milestone â€” merge for ACT / audit only unless IX requested]"
mind_category: knowledge
signal_type: we_did / pol_milestone
priority_score: 3
summary: work-politics â€” <artifact> v<N> | optional revenue-log row REF
profile_target: museum knowledge section A. KNOWLEDGE
suggested_entry: "Milestone only â€” see WORK doc path (minimal IX if needed)"
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

_(Legacy `signal_type: wap_milestone` is still accepted in existing rows.)_

---

## With deliverable + revenue cross-ref

Add to `summary` or `source_exchange`:

```yaml
summary: work-politics â€” iran-brief v2 | revenue-log 2026-03-xx
```

```yaml
source_exchange:
  operator: "Paid deliverable closed â€” see revenue-log.md; artifact iran-foreign-policy-brief.md"
```

---

## Commands (after approve)

```bash
# work-politics-only batch
python scripts/process_approved_candidates.py -u grace-mar --territory pol \
  --generate-receipt /tmp/pol.json --approved-by "<name>"
python scripts/process_approved_candidates.py -u grace-mar --territory pol \
  --apply --approved-by "<name>" --receipt /tmp/pol.json
```

---

## Do not

- Stage **unsourced** political claims â€” knowledge boundary still applies; cite doc + companion approval in `source_exchange`.
- Put **strategy you donâ€™t want in Voice** into `prompt_addition` â€” use `none` and keep detail in WORK docs unless INTENT/companion says otherwise.

