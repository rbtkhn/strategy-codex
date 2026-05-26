# Bookshelf — formal bibliography (generated)

**WORK only;** not Record.

Markdown files in this directory are **generated** from [../bookshelf-catalog.yaml](../bookshelf-catalog.yaml). Do not edit them by hand.

| File | Use |
|------|-----|
| [REFERENCES-shelf-by-era.md](REFERENCES-shelf-by-era.md) | All shelf rows grouped by `era` (ancient → cybernetic) |
| [REFERENCES-shelf-by-shelf-id.md](REFERENCES-shelf-by-shelf-id.md) | Same entries, sorted by `Shelf-NNNN` |

**Regenerate:** `python3 scripts/build_hn_bookshelf_bibliography.py`  
**Check (CI):** `python3 scripts/build_hn_bookshelf_bibliography.py --check`  
**Cited subset (paste into a chapter or appendix):** `python3 scripts/build_hn_bookshelf_bibliography.py --cited-ids Shelf-0001,Shelf-0002` (or `--cited-ids-file` with one id per line)

**Style:** Simplified Chicago *author–date*; optional imprint fields in YAML (`cite_as`, `place`, `publisher`, `edition`, `series`, `editor`, `translator`). For publication, treat this as a **working** list and strip the trailing `` `Shelf-…` `` tags if the venue requires a clean *References* section.

Overview: [../BOOKSHELF.md](../BOOKSHELF.md).
