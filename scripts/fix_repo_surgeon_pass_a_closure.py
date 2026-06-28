#!/usr/bin/env python3
"""One-shot manual closure for repo-surgeon pass-a remaining ~70 broken_link warnings."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: str, old: str, new: str) -> bool:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        return False
    p.write_text(text.replace(old, new), encoding="utf-8")
    return True


def patch_all(path: str, old: str, new: str) -> int:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count:
        p.write_text(text.replace(old, new), encoding="utf-8")
    return count


def main() -> None:
    changes: list[str] = []

    def record(path: str, old: str, new: str, *, all_occurrences: bool = False) -> None:
        if all_occurrences:
            n = patch_all(path, old, new)
            if n:
                changes.append(f"{path}: {n}x {old!r} -> {new!r}")
        elif patch(path, old, new):
            changes.append(f"{path}: {old!r} -> {new!r}")

    # skills
    record(
        "skills/_drafts/fast-tools-finish/SKILL.md",
        "../../../../.cursor/skills/coffee/",
        "../../../.cursor/skills/coffee/",
    )

    # notes
    record(
        "statecraft/notes/recursive-learning-three-lane-audit.md",
        "../../america/transactions/",
        "../america/transactions/",
        all_occurrences=True,
    )
    record(
        "statecraft/notes/recursive-learning-three-lane-audit.md",
        "../../china/transactions/",
        "../china/transactions/",
        all_occurrences=True,
    )
    record(
        "statecraft/notes/reentry/2026-06-week2-start-here.md",
        "../../../compact/",
        "../../compact/",
        all_occurrences=True,
    )
    record(
        "statecraft/notes/watch/2026-06-16-72h-watch-run.md",
        ".../kent-restraint-lever-walk-away-vs-weichert-collapse-2026-06.md",
        "../kent-restraint-lever-walk-away-vs-weichert-collapse-2026-06.md",
        all_occurrences=True,
    )
    record(
        "statecraft/notes/wire/2026-06-08-09-news-verify-matrix.md",
        "source-dialogue-works-colonel-douglas-macgregor-wilkerson-ramat-david-2026-06-09.md",
        "source-dialogue-works-wilkerson-israels-grand-strategy-coming-apart-2026-06-09.md",
    )

    # sheets
    record(
        "statecraft/sheets/source-archive-residue/2026-04-27/2026-04-27-diesen.md",
        "../../../../../../../voices/crooke/",
        "../../../../voices/crooke/",
    )
    record(
        "statecraft/sheets/transaction-router.md",
        "../../../transactions/",
        "../transactions/",
        all_occurrences=True,
    )
    record(
        "statecraft/sheets/trilateral-state-memory-audit.md",
        "../../../transactions/",
        "../transactions/",
        all_occurrences=True,
    )

    # states / volumes / essays / export-templates
    record(
        "statecraft/states/essays/high-skill-labor-compression-and-civilizational-statecraft.md",
        "../../../../ph-civ-to-civ-state-bridge.md",
        "../ph-civ-to-civ-state-bridge.md",
    )
    record(
        "statecraft/states/export-templates/public-README.md",
        "../../../../essays/cross-case-recurrence-and-sovereignty.md",
        "../../../public/civ-state/essays/cross-case-recurrence-and-sovereignty.md",
    )
    record(
        "statecraft/states/export-templates/public-README.md",
        "../../../../essays/high-skill-labor-compression-and-civilizational-statecraft.md",
        "../essays/high-skill-labor-compression-and-civilizational-statecraft.md",
    )
    record(
        "statecraft/states/export-templates/source-lattice.md",
        "../../../essays/cross-case-recurrence-and-sovereignty.md",
        "../../../public/civ-state/essays/cross-case-recurrence-and-sovereignty.md",
    )
    record(
        "statecraft/states/volumes/README.md",
        "../../../../../../../config/civilizational_statecraft_public_export.yaml",
        "../../../../platform/config/civilizational_statecraft_public_export.yaml",
    )
    record(
        "statecraft/states/volumes/README.md",
        "../../../../theory/README.md",
        "../../theory/README.md",
    )
    record(
        "statecraft/states/volumes/civ-state-america/game-theory-america.md",
        "../../../../../america/america-doctrine.md",
        "../../../america/README.md",
    )
    record(
        "statecraft/states/volumes/civ-state-persia/secret-history-persia.md",
        "../../../../../../research/repos/civilization_memory/",
        "../../../../research/repos/civilization_memory/",
        all_occurrences=True,
    )
    record(
        "statecraft/states/volumes/civ-state-rome/civilization-rome.md",
        "rome-volume-writing-brief.md",
        "ROME-PASS.md",
    )

    # synthesis
    record(
        "statecraft/synthesis/METHOD.md",
        "../notes/intake/../notes/intake/../notes/intake/../notes/intake/intake-digest-TEMPLATE.md",
        "../notes/intake/intake-digest-TEMPLATE.md",
    )
    record(
        "statecraft/synthesis/day/2026-06-18.md",
        "../../../../../recursive-learning-journal.md",
        "../../recursive-learning-journal.md",
        all_occurrences=True,
    )
    record(
        "statecraft/synthesis/day/2026-06-24.md",
        "[conflict-ukraine-donbas-hinge](../../notes/conflict-ukraine-donbas-hinge.md)",
        "`conflict-ukraine-donbas-hinge` (pending promotion)",
    )

    # transactions
    record(
        "statecraft/transactions/hormuz-transit-sanctions-relief-compact/comparison.md",
        "[Iran](../iran.md)",
        "[Persia](persia.md)",
    )
    record(
        "statecraft/transactions/persia-nuclear-latency-recognition-framework/comparison.md",
        "[Iran](../iran.md)",
        "[Persia](persia.md)",
    )

    # voices — depth
    for rel in (
        "statecraft/voices/armstrong/armstrong-thread.md",
        "statecraft/voices/barnes/barnes-mind.md",
        "statecraft/voices/barnes/barnes-thread.md",
        "statecraft/voices/freeman/freeman-thread.md",
        "statecraft/voices/jermy/jermy-thread.md",
        "statecraft/voices/marandi/marandi-thread.md",
    ):
        record(rel, "../../../../docs/", "../../../docs/", all_occurrences=True)

    record(
        "statecraft/voices/krapivnik/krapivnik-profile.md",
        "../../../channels/",
        "../../channels/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/map/open-first-routes.md",
        "../../../../notes/",
        "../../notes/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/map/open-first-routes.md",
        "../../../notes/",
        "../../notes/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/marandi/marandi-page-2026-04-21-blockade-islamabad-hormuz.md",
        "../../strategy-state-iran/voices/iri-institutional/thread.md",
        "../../../codex/strategy-state-iran/voices/iri-institutional/thread.md",
    )
    record(
        "statecraft/voices/mercouris/mercouris-transcript.md",
        "../../../../source-archive/",
        "../../../source-archive/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/pape/pape-cross-host-note.md",
        "../../../../source-archive/",
        "../../../source-archive/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/diesen/diesen-thread.md",
        "../../crooke/",
        "../crooke/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/diesen/diesen-transcript.md",
        "../../crooke/",
        "../crooke/",
        all_occurrences=True,
    )
    record(
        "statecraft/voices/diesen/diesen-thread.md",
        "../../../codex/strategy-expert-diesen-transcript.md",
        "../../../codex/profiles/diesen-profile.md",
    )
    record(
        "statecraft/voices/diesen/diesen-host-wiring-2026.md",
        "diesen-routing.md",
        "index.md",
    )

    # crooke doubled notes paths
    for rel in (
        "statecraft/voices/crooke/crooke-march-may-2026-interview-arc-threads.md",
        "statecraft/voices/crooke/crooke-shelf-2026-03.md",
        "statecraft/voices/crooke/crooke-shelf-2026-04.md",
        "statecraft/voices/crooke/crooke-shelf-2026-05.md",
    ):
        record(rel, "../../notes/../../notes/", "../../notes/", all_occurrences=True)

    # malformed markdown — parsi
    record(
        "statecraft/voices/parsi/parsi-thread.md",
        "In the current Parsi shelf, the canonical structure lives in [parsi-arc.md](parsi-arc.md, [parsi-routing.md](parsi-routing.md, [parsi-helix.md](parsi-helix.md, [parsi-2025-present-arc-threads.md](parsi-2025-present-arc-threads.md), [parsi-forecast-ledger-2025-2026.md](parsi-forecast-ledger-2025-2026.md), and [parsi-interview-appearances-2025-2026.md](parsi-interview-appearances-2025-2026.md, not this file.",
        "In the current Parsi shelf, the canonical structure lives in [parsi-arc.md](parsi-arc.md), [parsi-routing.md](parsi-routing.md), [parsi-helix.md](parsi-helix.md), [parsi-2025-present-arc-threads.md](parsi-2025-present-arc-threads.md), [parsi-forecast-ledger-2025-2026.md](parsi-forecast-ledger-2025-2026.md), and [parsi-interview-appearances-2025-2026.md](parsi-interview-appearances-2025-2026.md), not this file.",
    )

    # crooke-thread malformed
    record(
        "statecraft/voices/crooke/crooke-thread.md",
        "crossed by [crooke-helix.md](crooke-helix.md, with [crooke-thread-international-law.md](crooke-thread-international-law.md)",
        "crossed by [crooke-helix.md](crooke-helix.md), with [crooke-thread-international-law.md](crooke-thread-international-law.md)",
    )

    # davis malformed
    record(
        "statecraft/voices/davis/davis-thread.md",
        "**Companion files:** [davis-profile.md](davis-profile.md (profile) and [davis-transcript.md](davis-transcript.md)",
        "**Companion files:** [davis-profile.md](davis-profile.md) (profile) and [davis-transcript.md](davis-transcript.md)",
    )
    record(
        "statecraft/voices/davis/davis-transcript.md",
        "**Companion files:** [davis-profile.md](davis-profile.md (profile) and [davis-thread.md](davis-thread.md)",
        "**Companion files:** [davis-profile.md](davis-profile.md) (profile) and [davis-thread.md](davis-thread.md)",
    )

    # pape malformed commentator-threads link
    record(
        "statecraft/voices/pape/pape-thread.md",
        "[strategy-commentator-threads.md](../../../codex/strategy-commentator-threads.md (`mercouris`",
        "[strategy-commentator-threads.md](../../../codex/strategy-commentator-threads.md) (`mercouris`",
    )

    # ritter malformed inbox link
    record(
        "statecraft/voices/ritter/ritter-thread.md",
        "[daily-strategy-inbox.md `## 2026-04-19`](../daily-strategy-inbox.md (paste line + `batch-analysis | Ritter Substack",
        "[daily-strategy-inbox.md `## 2026-04-19`](../../../codex/daily-strategy-inbox.md) (paste line + `batch-analysis | Ritter Substack",
    )

    # armstrong colon in URL
    record(
        "statecraft/voices/armstrong/armstrong-cross-host-note.md",
        "[armstrong-cash-hormuz-digital-dollar-arc](../davis/davis-thread.md:495)",
        "[armstrong-cash-hormuz-digital-dollar-arc](../davis/davis-thread.md) (line 495)",
    )

    # export template stub
    stub = ROOT / "statecraft/states/export-templates/sibling.md"
    if not stub.exists():
        stub.write_text(
            "# Sibling term page (template stub)\n\nWORK only; not Record.\n",
            encoding="utf-8",
        )
        changes.append("created statecraft/states/export-templates/sibling.md")

    print(f"Applied {len(changes)} change groups:")
    for line in changes:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
