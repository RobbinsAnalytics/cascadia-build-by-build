#!/usr/bin/env python3
"""validate.py: the domain gate for Cascadia Build by Build. Exit 1 stops a publish.

Checks the things governance/spec.md says must be true of the data layer:

  1. every row's repository exists beside this one, and the rows are exactly
     the nine the spec fixes, in first_commit order
  2. every row's era is one of the five, first_commit <= last_commit, retro is
     null, and every surface cell is a repo-relative path or null
  3. every filled cell's path exists on disk in the named sibling and is
     tracked in that sibling's index: the page's own test, applied before
     there is a page
  4. data/standard.json carries each version once, in order, with dates that
     never go backwards where they are present; every row's remote and
     default_branch are set, and the remote follows REMOTE-CONVENTION.md
  5. re-running src/inventory.py reproduces both files byte for byte, so the
     inventory is a function of disk and not of the session that ran it

It does not check the freeze; that is src/validate_freeze.py, run after it.
Every sibling read here is `git ls-files` or the filesystem. Nothing here
writes anywhere, in this repository or any other.

    python src/validate.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
import inventory  # noqa: E402  (the constants: rows, eras, surfaces, versions)

failures: list[str] = []

# cascadia-standards/governance/REMOTE-CONVENTION.md: the split pattern drops
# "-analytics" on the remote; every other row's remote equals its key.
SPLIT_ROWS = {"cascadia-controltower-analytics", "cascadia-dealdesk-analytics",
              "cascadia-finance-analytics", "cascadia-matter-ledger-analytics"}


def ok(msg: str) -> None:
    print(f"  [PASS] {msg}")


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  [FAIL] {msg}")


def tracked(repo: Path, rel: str) -> bool:
    r = subprocess.run(["git", "-C", str(repo), "ls-files", "--", rel],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode == 0 and bool(r.stdout.strip())


def main() -> int:
    print("Cascadia Build by Build: domain gate\n")

    builds = json.loads(inventory.BUILDS_JSON.read_text(encoding="utf-8"))
    standard = json.loads(inventory.STANDARD_JSON.read_text(encoding="utf-8"))

    # 1. rows and their repositories -------------------------------------------
    expected_keys = [r["key"] for r in inventory.ROWS]
    got_keys = [r["key"] for r in builds]
    if sorted(got_keys) == sorted(expected_keys) and len(got_keys) == len(set(got_keys)):
        ok(f"rows are exactly the {len(expected_keys)} the spec fixes")
    else:
        fail(f"rows differ from the spec: {sorted(set(got_keys) ^ set(expected_keys))}")
    firsts = [r["first_commit"] for r in builds]
    if firsts == sorted(firsts):
        ok("rows are ordered by first_commit")
    else:
        fail("rows are not ordered by first_commit")
    for r in builds:
        repo = inventory.ESTATE / r["key"]
        if (repo / ".git").exists():
            ok(f"{r['key']}: repository exists")
        else:
            fail(f"{r['key']}: repository missing at {repo}")

    # 2. row shape ---------------------------------------------------------------
    for r in builds:
        k = r["key"]
        if r["era"] not in inventory.ERAS:
            fail(f"{k}: era {r['era']!r} is not one of the five")
        if not (r["first_commit"] <= r["last_commit"]):
            fail(f"{k}: first_commit {r['first_commit']} after last_commit {r['last_commit']}")
        if r["retro"] is not None:
            fail(f"{k}: retro is filled; Part 1 sets it null")
        if list(r["surfaces"].keys()) != sorted(inventory.SURFACES):
            fail(f"{k}: surface keys are not the fourteen")
        for s, v in r["surfaces"].items():
            if v is not None and (not isinstance(v, str) or not v or v.startswith(("/", "\\"))
                                  or ".." in v.split("/")):
                fail(f"{k}: {s} is not a repo-relative path or null: {v!r}")
    if not failures:
        ok("every row has a valid era, ordered dates, null retro, and path-or-null cells")

    # 2b. the link fields: REMOTE-CONVENTION.md's two patterns ---------------
    for r in builds:
        k = r["key"]
        if not r.get("remote") or not r.get("default_branch"):
            fail(f"{k}: remote or default_branch is empty")
            continue
        expected = k[:-len("-analytics")] if k in SPLIT_ROWS else k
        if r["remote"] != expected:
            fail(f"{k}: remote {r['remote']!r} does not follow REMOTE-CONVENTION "
                 f"(expected {expected!r})")
    if not any("remote" in f or "default_branch" in f for f in failures):
        ok("remote and default_branch are set on every row and follow REMOTE-CONVENTION.md")

    # 3. every filled cell resolves -----------------------------------------------
    filled = checked = 0
    for r in builds:
        repo = inventory.ESTATE / r["key"]
        for s, v in r["surfaces"].items():
            if v is None:
                continue
            filled += 1
            p = repo / v
            if not p.exists():
                fail(f"{r['key']}: {s} -> {v} does not exist on disk")
            elif not tracked(repo, v):
                fail(f"{r['key']}: {s} -> {v} exists but is not tracked in that repository")
            else:
                checked += 1
    if checked == filled:
        ok(f"all {filled} filled cells exist on disk and are tracked in their repository")

    # 4. the thin lane -------------------------------------------------------------
    versions = [e["version"] for e in standard]
    if versions == inventory.VERSIONS:
        ok(f"standard.json carries the {len(versions)} versions once each, in order")
    else:
        fail(f"standard.json versions are {versions}, expected {inventory.VERSIONS}")
    dated = [e["date"] for e in standard if e["date"] is not None]
    if dated == sorted(dated):
        ok(f"standard.json dates never go backwards ({len(dated)} dated, "
           f"{len(standard) - len(dated)} null)")
    else:
        fail("standard.json dates go backwards")
    for e in standard:
        if (e["date"] is None) != (e["commit"] is None):
            fail(f"v{e['version']}: date and commit must be null together")

    # 5. the inventory is a function of disk ----------------------------------------
    r = subprocess.run([sys.executable, str(REPO / "src" / "inventory.py"), "--check"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        ok("re-running inventory.py reproduces both files byte for byte")
    else:
        fail("re-running inventory.py does not reproduce the committed files")
        print(r.stdout[-2000:])

    print()
    if failures:
        print(f"DOMAIN GATE: FAILED ({len(failures)} failure(s)). Publish nothing, commit nothing.")
        return 1
    print("DOMAIN GATE: PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
