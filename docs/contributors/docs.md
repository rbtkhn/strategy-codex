# Contributor checklist — docs

1. Read [`docs/start-here.md`](../start-here.md) and slim [`AGENTS.md`](../../AGENTS.md).
2. Class: **work** authority — not Record, not generated unless documenting a generator.
3. Grace-Mar / fork blocks → pointer to [`docs/archive/grace-mar.md`](../archive/grace-mar.md) (≤3 lines).
4. Routing tables → prefer [`docs/routing-reference.md`](../routing-reference.md) or regenerate [`LLM-ROUTING.md`](../../LLM-ROUTING.md).
5. Preflight: `python3 scripts/check_archive_boundary.py` · `python3 scripts/check_doc_duplication.py`
6. Architecture claims → [`docs/architecture.md`](../architecture.md) (active), not archived grace-mar corpus stub.
7. README / start-here length → [complexity-readme-start-here-trim-plan.md](../complexity-readme-start-here-trim-plan.md)
