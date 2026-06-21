from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import migrate_cognition_stream_receipt_keys as migrate  # noqa: E402


def test_migrate_renames_legacy_file_and_patches_channel_key(tmp_path: Path) -> None:
    window = tmp_path / "2026-05-21_to_2026-05-21"
    window.mkdir(parents=True)
    legacy = window / "alex-mercouris.discovery.json"
    legacy.write_text(
        json.dumps(
            {
                "channel_key": "alex-mercouris",
                "items": [{"id": "abc123", "title": "Example"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    aliases = {"alex-mercouris": "alexander-mercouris"}
    result = migrate.migrate_receipt_root(tmp_path, aliases, dry_run=False)

    target = window / "alexander-mercouris.discovery.json"
    assert not legacy.exists()
    assert target.is_file()
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["channel_key"] == "alexander-mercouris"
    assert result.to_dict()["counts"]["renamed"] == 1


def test_dry_run_does_not_write(tmp_path: Path) -> None:
    window = tmp_path / "2026-05-21_to_2026-05-21"
    window.mkdir(parents=True)
    legacy = window / "napolitano.discovery.json"
    legacy.write_text(json.dumps({"channel_key": "napolitano", "items": []}) + "\n", encoding="utf-8")

    aliases = {"napolitano": "judging-freedom"}
    result = migrate.migrate_receipt_root(tmp_path, aliases, dry_run=True)

    assert legacy.is_file()
    assert not (window / "judging-freedom.discovery.json").exists()
    assert result.to_dict()["counts"]["renamed"] == 1


def test_conflict_when_target_exists(tmp_path: Path) -> None:
    window = tmp_path / "2026-05-21_to_2026-05-21"
    window.mkdir(parents=True)
    (window / "daniel-davis-deep-dive.discovery.json").write_text(
        json.dumps({"channel_key": "daniel-davis-deep-dive", "items": []}) + "\n",
        encoding="utf-8",
    )
    (window / "daniel-davis.discovery.json").write_text(
        json.dumps({"channel_key": "daniel-davis", "items": []}) + "\n",
        encoding="utf-8",
    )

    aliases = {"daniel-davis-deep-dive": "daniel-davis"}
    result = migrate.migrate_receipt_root(tmp_path, aliases, dry_run=False)

    assert (window / "daniel-davis-deep-dive.discovery.json").is_file()
    assert result.to_dict()["counts"]["conflicts"] == 1
