#!/usr/bin/env python3
"""Fail-closed checks for the public beads-expert package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "beads-expert" / "SKILL.md"
REFERENCE = ROOT / "skills" / "beads-expert" / "references" / "storage-model.md"


def frontmatter_scalar(document: str, key: str) -> str | None:
    frontmatter = document.split("---", 2)[1]
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def main() -> int:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    skill = SKILL.read_text(encoding="utf-8")
    reference = REFERENCE.read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    require(frontmatter_scalar(skill, "name") == "beads-expert", "skill name drifted")
    require(frontmatter_scalar(skill, "version") == "2.0.0", "skill version drifted")
    require(frontmatter_scalar(skill, "compatibility") is not None, "compatibility missing")
    require(REFERENCE.is_file(), "storage-model reference missing")
    require("https://github.com/gastownhall/beads" in skill, "current upstream missing")
    require("bd dolt push" in skill and "bd dolt pull" in skill, "Dolt sync workflow missing")
    require("refs/dolt/data" in reference, "Dolt Git ref contract missing")
    require("DoltHub is one optional" in reference, "DoltHub terminology missing")
    require("Freshie is separate" in reference, "Freshie separation missing")
    require("bd sync               # Sync with git" not in agents, "AGENTS still teaches bd sync")
    require("flush/import/export + git sync" not in claude, "CLAUDE still teaches legacy sync")
    require("npx skills add jeremylongshore/resume-firebase" in readme, "install command missing")
    require(
        not (ROOT / "services" / "worker" / "service-account-key.json").exists(),
        "tracked service-account key placeholder returned",
    )

    for stale in (
        "https://github.com/steveyegge/beads",
        ".beads/beads.db",
        "bd --no-daemon",
        "bd stats",
        "{baseDir}",
    ):
        require(stale not in skill, f"stale Beads contract returned: {stale}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("beads-expert repository contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
