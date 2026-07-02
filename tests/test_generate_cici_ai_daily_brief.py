from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile
import unittest

from scripts.generate_cici_ai_daily_brief import (
    build_digest,
    load_recent_evidence,
    parse_dashboard_qualitative,
    parse_latest_dashboard_row,
    render_telegram_brief,
)

class GenerateCiciAIDailyBriefTests(unittest.TestCase):
    def test_parse_latest_dashboard_row_uses_latest_filled_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            dashboard = tmp_path / "dashboard.md"
            dashboard.write_text(
                """# Dashboard

## 4. Weekly snapshot table

| Week of | Evidence links reviewed | Invited | Joined | Introduced | Goal stated | First task completed | Returned within 7d | Issue / PR / artifact | Helper behavior | Notes |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2026-04-30 | [a](a.md) | 10 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | Confidence B from operator text. |
| 2026-05-21 | [b](b.md) | 0 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | Confidence A from artifact evidence. |
| YYYY-MM-DD |  |  |  |  |  |  |  |  |  |  |
""",
                encoding="utf-8",
            )
            row = parse_latest_dashboard_row(dashboard)
            self.assertEqual(row.week_of, "2026-05-21")
            self.assertEqual(row.first_task_completed, 1)
            self.assertEqual(row.confidence, "A")

    def test_build_digest_combines_dashboard_and_profiles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            docs = tmp_path / "docs" / "skill-work" / "work-cici"
            profiles_dir = docs / "member-profiles"
            progress_dir = docs / "cici-ai-progress"
            telegram_dir = docs / "cici-ai-telegram"
            evidence_dir = docs / "archive/placeholders/evidence"
            profiles_dir.mkdir(parents=True)
            progress_dir.mkdir()
            telegram_dir.mkdir()
            evidence_dir.mkdir()

            dashboard = docs / "cici-ai-community-dashboard.md"
            dashboard.write_text(
                """# Dashboard

## 4. Weekly snapshot table

| Week of | Evidence links reviewed | Invited | Joined | Introduced | Goal stated | First task completed | Returned within 7d | Issue / PR / artifact | Helper behavior | Notes |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2026-05-21 | [b](b.md) | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | Confidence B from operator text. Two messages include fork signals, but first task is still not evidenced. |

## 6. Qualitative observations

### What produced action

- Live GitHub review shows the cohort is past pure sign-up mode.

### What needs a simpler prompt

- Next prompt should ask for one concrete artifact only: "Reply with your OB1 fork URL or a screenshot showing the fork in your GitHub account."
""",
                encoding="utf-8",
            )
            (progress_dir / "README.md").write_text(
                """# cici-ai-progress

## Open loops

- Verify each applicant's OB1 fork or repo setup.

## Next action

Update the community dashboard with a lane-owned applicant table.
""",
                encoding="utf-8",
            )
            (telegram_dir / "README.md").write_text(
                """# cici-ai-telegram

## Open loops

- Create the next Telegram post after the first applicant wave.

## Next action

Post next-ob1-fork-proof-post-2026-04-30.md and route replies into progress.
""",
                encoding="utf-8",
            )
            (evidence_dir / "cici-ai-telegram-self-claims-2026-05-01.md").write_text(
                """# cici-ai Telegram self-claims

**Confidence:** B - operator-supplied Telegram text.

## Dashboard implications

- Introduced self: 4 additional introductions with GitHub accounts shared.
- Fork signal: 2 explicit self-reports mention a forked upstream workspace.

## Follow-up

- If needed, ask for a fork URL or screenshot next so the progress lane can turn the self-report into evidence-backed setup status.
""",
                encoding="utf-8",
            )

            (profiles_dir / "README.md").write_text("# Profiles\n", encoding="utf-8")
            (profiles_dir / "template.md").write_text("# Template\n", encoding="utf-8")
            (profiles_dir / "one.md").write_text(
                """# Profile

**Name:** Jayr / Dismantle
**GitHub handle:** [salajosefinojr-sys](https://github.com/salajosefinojr-sys)
**Current status:** Active but mapping needs cleanup
**Last verified GitHub activity:** 2026-05-20
**Evidence level:** A

## Open loops

- Confirm the handle mapping against the spreadsheet name
""",
                encoding="utf-8",
            )
            (profiles_dir / "two.md").write_text(
                """# Profile

**Name:** Jhon Ell / Ell
**GitHub handle:** [jhon-ell16](https://github.com/jhon-ell16)
**Current status:** Active builder
**Last verified GitHub activity:** 2026-05-22
**Evidence level:** A

## Open loops

- Keep updates short and durable
""",
                encoding="utf-8",
            )

            digest = build_digest(tmp_path, brief_date=date(2026, 5, 22))
            self.assertEqual(digest.mode, "setup")
            self.assertEqual(digest.confidence, "B")
            self.assertTrue(digest.what_moved)
            self.assertTrue(any("fork URL" in item for item in digest.what_matters_today))
            self.assertTrue(any("Jayr / Dismantle" in item for item in digest.who_needs_action))
            self.assertTrue(any("cici-ai-telegram/README.md" in path for path in digest.source_paths))
            self.assertTrue(any("Introduced self: 4 additional introductions" in item for item in digest.what_moved))

            telegram = render_telegram_brief(digest)
            self.assertIn("Daily cici-ai brief - 2026-05-22", telegram)
            self.assertIn("Reply with: fork URL or screenshot + one-line status", telegram)

    def test_parse_dashboard_qualitative_reads_named_subsections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            dashboard = tmp_path / "dashboard.md"
            dashboard.write_text(
                """# Dashboard

## 6. Qualitative observations

### What worked

- A launch sequence moved from copy to live setup.

### What produced action

- A smaller group now has visible fork activity.
""",
                encoding="utf-8",
            )
            qualitative = parse_dashboard_qualitative(dashboard)
            self.assertEqual(qualitative["what_worked"], ["A launch sequence moved from copy to live setup."])
            self.assertEqual(qualitative["what_produced_action"], ["A smaller group now has visible fork activity."])

    def test_load_recent_evidence_sorts_latest_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            (evidence_dir / "older.md").write_text(
                """# Older

**Confidence:** C

## Dashboard implications

- Older movement.
""",
                encoding="utf-8",
            )
            (evidence_dir / "newer-2026-05-10.md").write_text(
                """# Newer

**Confidence:** B

## Dashboard implications

- Newer movement.
""",
                encoding="utf-8",
            )
            notes = load_recent_evidence(evidence_dir, limit=2)
            self.assertEqual(notes[0].title, "Newer")
            self.assertEqual(notes[0].confidence, "B")
            self.assertEqual(notes[0].movement_bullets, ["Newer movement."])

if __name__ == "__main__":
    unittest.main()
