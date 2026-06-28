**strategy-codex instance notes**

- Canonical theory shelf: [theory/README.md](../../../statecraft/states/theory/README.md) · [Form](../../../public/civ-state/theory/memory.md)
- Canonical retrieval matrix: [statecraft/states/indexes/source-retrieval-matrix.md](../../../statecraft/states/indexes/source-retrieval-matrix.md)
- Primary deep-grammar shelf: [statecraft/states/sacred-grammar/README.md](../../../README.md)
- Use this skill before lane descent when the governing pair is unclear or when a live object is being flattened into one layer too quickly.
- Secondary families such as `god`, `lit`, `art`, `geo`, `war`, and `peace` should be opened only after the governing pair is named.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-framework
python scripts/sync_portable_skills.py --verify --skill statecraft-framework
python scripts/validate_skills.py
```
