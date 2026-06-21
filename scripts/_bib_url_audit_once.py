#!/usr/bin/env python3
"""One-shot bibliography URL verifier — stdin or file paths as args."""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

TIMEOUT = 12
UA = "strategy-codex-bibliography-audit/1.1"


def check(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return True, str(r.status)
    except Exception:
        try:
            req2 = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req2, timeout=TIMEOUT) as r:
                return True, str(r.status)
        except Exception as e:
            return False, str(e)[:100]


def main() -> int:
    text = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    urls = re.findall(r"^\s+-\s+(https://\S+)", text, re.M)
    fail = []
    for u in urls:
        ok, info = check(u)
        if not ok:
            fail.append((u, info))
    print(f"TOTAL {len(urls)} FAIL {len(fail)}")
    for u, info in fail:
        print(f"FAIL {u}\n  {info}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
