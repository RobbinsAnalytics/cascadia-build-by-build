#!/usr/bin/env python3
"""inventory.py: read the nine sibling module repositories and write the data.

Cascadia Build by Build, Part 1. This module has no data of its own. Its source
is the other nine module repositories, read-only, and the estate's standards
repository for the thin lane of VIZ-PRINCIPLES versions.

    python src/inventory.py            write data/builds.json and data/standard.json
    python src/inventory.py --check    build both in memory and compare with disk;
                                       exit 1 if either differs, writing nothing

THE THREE RULES THIS SCRIPT LIVES UNDER

  1. It never writes outside this repository and never runs a command that
     writes in a sibling. Every sibling read is `git log`, `git ls-files`,
     `git show`, `git symbolic-ref` or the filesystem. None of those takes
     `.git/index.lock`. It never runs `git status` anywhere.
  2. Rows, eras, names, slugs and stack phrases are constants fixed by
     governance/spec.md. Nothing about a row's membership is inferred.
  3. The detection rules are the paragraphs in governance/surfaces.md. The
     RULES table below implements them; where the two disagree, one is wrong.
     A cell is a repo-relative path or None, nothing else. Every path written
     is verified to exist on disk and to be tracked in that sibling's index.

Re-running against an unchanged estate produces byte-identical files: keys are
sorted, indentation is fixed, and no timestamp is written. The run timestamp
belongs in the session report, not here.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
ESTATE = REPO.parent
DATA = REPO / "data"
BUILDS_JSON = DATA / "builds.json"
STANDARD_JSON = DATA / "standard.json"

STANDARDS_REPO = ESTATE / "cascadia-standards"
VIZ_PRINCIPLES = "design-system/VIZ-PRINCIPLES.md"
VIZ_HEADER = re.compile(r"^\*\*Aaron Robbins · Robbins Analytics · v(\d+\.\d+)")

# ---------------------------------------------------------------------------
# Constants fixed by governance/spec.md. Not inferred, not detected.
# ---------------------------------------------------------------------------

ERAS = (
    "Enterprise-shaped",
    "Frozen and validated",
    "Reviewed and registered",
    "Operated",
    "Re-derived",
)

# key: local directory name under C:\Projects. site_slug: projects/<slug>.qmd
# on the site. stack: the one-phrase form of the site's own table in
# cascadia.qmd, shortened; copied, not re-derived.
ROWS = [
    {"key": "manufacturing-analytics", "name": "Cascadia Medical Devices",
     "site_slug": "cascadia-medical-devices", "era": "Enterprise-shaped",
     "stack": "SQL Server, Fabric, Power BI"},
    {"key": "cascadia-pharmacy-analytics", "name": "Cascadia Pharmacy",
     "site_slug": "cascadia-pharmacy", "era": "Enterprise-shaped",
     "stack": "SQL Server, Power BI"},
    {"key": "cascadia-staffing-analytics", "name": "Cascadia Staffing",
     "site_slug": "cascadia-staffing", "era": "Enterprise-shaped",
     "stack": "SQL Server, Power BI"},
    {"key": "cascadia-finance-analytics", "name": "Cascadia Finance",
     "site_slug": "cascadia-finance", "era": "Frozen and validated",
     "stack": "Python, SQLite, ECharts, SEC XBRL"},
    {"key": "cascadia-dealdesk-analytics", "name": "Cascadia Deal Desk",
     "site_slug": "cascadia-dealdesk", "era": "Reviewed and registered",
     "stack": "Python, SQLite, ECharts"},
    {"key": "cascadia-controltower-analytics", "name": "Cascadia Control Tower",
     "site_slug": "cascadia-controltower", "era": "Reviewed and registered",
     "stack": "Python, DuckDB, dbt, ECharts"},
    {"key": "cascadia-matter-ledger-analytics", "name": "Cascadia Matter Ledger",
     "site_slug": "cascadia-matter-ledger", "era": "Operated",
     "stack": "Python, DuckDB, ECharts, scheduled pull"},
    {"key": "cascadia-fee-examiner", "name": "Cascadia Fee Examiner",
     "site_slug": "cascadia-fee-examiner", "era": "Operated",
     "stack": "Python, CSV/JSON, ECharts"},
    {"key": "cascadia-revenue-assurance", "name": "Cascadia Revenue Assurance",
     "site_slug": "cascadia-revenue-assurance", "era": "Re-derived",
     "stack": "Python, CSV, ECharts, DuckDB gate"},
]

BANDS = {
    "Data": ["one_command_rebuild", "frozen_source", "source_register"],
    "Numbers": ["row_count_validation", "validation_report", "tests_as_code",
                "independent_rederivation", "golden_fixture", "negative_controls"],
    "Presentation": ["chart_review", "reading_panel", "metric_register"],
    "Operation": ["scheduled_run_with_health", "reconciliation_published"],
}
SURFACES = [s for band in BANDS.values() for s in band]

# The VIZ-PRINCIPLES versions the thin lane carries, v1.0 to v2.8, in order.
VERSIONS = ["1.0", "2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"]

# ---------------------------------------------------------------------------
# Detection rules: governance/surfaces.md, implemented.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Candidate:
    """One candidate artifact for a surface.

    pattern: a repo-relative glob. Tried in the order listed; within one glob,
             matches are sorted so the result is stable.
    markers: regexes that must ALL match the file's text. Used where the
             evidence is a passage inside a file that also serves another
             purpose. A directory candidate cannot carry markers.
    """
    pattern: str
    markers: tuple[str, ...] = ()


C = Candidate

# Content markers, quoted in governance/surfaces.md.
BUILD_ORDER = r"(?im)^(#+ .*\brebuild\b|run in this order\b|.*\bbuild order is\b)"
AS_OF_KEY = r'"as_of(?:_date)?"\s*:'
PER_FILE_HASH = r'"sha256"\s*:'
REDERIVES_IN_DOCSTRING = r"(?is)\A(?:[^\n]*\n){0,60}?[^\n]*re-?deriv"
PROOF_HEADING = r"(?im)^#+ .*\bcan fail\b"
PROOF_OUTCOME = r"(?i)\b(?:tripped|rejected)\b"
PANEL_HEADING = r"(?m)^#{2,3} .*Reading panel \(Rule 7\.4\)"
DISPOSITION_HEADING = r"(?im)^#+ .*\bdisposition\b"

RULES: dict[str, list[Candidate]] = {
    "one_command_rebuild": [
        C("run_*.ps1"),
        C("scripts/run_*.ps1"),
        C("README.md", (BUILD_ORDER,)),
        C("CLAUDE.md", (BUILD_ORDER,)),
    ],
    "frozen_source": [
        C("governance/freeze.toml"),
        C("data/raw/*manifest*.json", (AS_OF_KEY,)),
    ],
    "source_register": [
        C("governance/source-register.md"),
        C("data/raw/**/manifest*.json", (PER_FILE_HASH,)),
    ],
    "row_count_validation": [
        C("**/*validate_rowcounts.sql"),
        # The Python form is a named check per row; see NAMED_CHECKS.
    ],
    "validation_report": [
        C("governance/validation_report.md"),
        C("governance/validation_report*.md"),
    ],
    "tests_as_code": [
        C("dbt/tests"),
        C("src/test_*.py"),
        C("test_*.py"),
        C("tests"),
    ],
    "independent_rederivation": [
        C("src/validate_measures.py", (REDERIVES_IN_DOCSTRING,)),
        C("powerbi/validate_*_kpis.sql"),
    ],
    "golden_fixture": [
        C("tests/golden"),
        C("src/test_golden.py"),
        C("test_golden.py"),
    ],
    "negative_controls": [
        C("governance/validation_report.md", (PROOF_HEADING, PROOF_OUTCOME)),
    ],
    "chart_review": [
        C("governance/chart-review.md"),
    ],
    "reading_panel": [
        C("governance/READING-PANEL*.md"),
        C("governance/reading-panel-returns*.md"),
        C("governance/panel/findings.json"),
        C("governance/chart-review.md", (PANEL_HEADING, DISPOSITION_HEADING)),
    ],
    "metric_register": [
        C("governance/metric_register.md"),
    ],
    "scheduled_run_with_health": [
        C("governance/health.json"),
        C("governance/last_live_run.json"),
    ],
    "reconciliation_published": [
        C("governance/reconciliation.md"),
    ],
}

# Cells that point at one named check inside a validation script. Applied only
# where the rule above found nothing. The marker is the check's own label; if
# the check is removed from the file, the cell empties on the next run.
NAMED_CHECKS: dict[tuple[str, str], Candidate] = {
    ("cascadia-dealdesk-analytics", "row_count_validation"):
        C("src/validate.py", (r"conformed rows \{total\} != raw quote lines \{raw\}",)),
    ("cascadia-controltower-analytics", "row_count_validation"):
        C("validate.py", (r"Database content hash matches the recorded run",)),
    ("cascadia-revenue-assurance", "row_count_validation"):
        C("src/validate.py", (r"the engine refused exactly the transactions the generator intended, by reason",)),
}

# ---------------------------------------------------------------------------
# Read-only git helpers. None of these takes the index lock.
# ---------------------------------------------------------------------------


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {repo.name}: {r.stderr.strip()}")
    return r.stdout


def branch_of(repo: Path) -> str:
    try:
        return git(repo, "symbolic-ref", "--short", "HEAD").strip()
    except RuntimeError:
        return "(detached) " + git(repo, "rev-parse", "--short", "HEAD").strip()


def commit_dates(repo: Path) -> tuple[str, str]:
    """Author dates, ISO, of the oldest and newest commits reachable from HEAD."""
    dates = git(repo, "log", "--format=%as").split()
    if not dates:
        raise RuntimeError(f"{repo.name}: no commits")
    return dates[-1], dates[0]


def tracked(repo: Path, rel: str) -> bool:
    """True if `rel` (file or directory) has at least one tracked file."""
    out = git(repo, "ls-files", "--", rel)
    return bool(out.strip())


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def text_of(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def resolve(repo: Path, cand: Candidate) -> str | None:
    """The first tracked match of `cand` in `repo`, repo-relative, or None."""
    matches = sorted(p for p in repo.glob(cand.pattern) if ".git" not in p.parts)
    for p in matches:
        rel = p.relative_to(repo).as_posix()
        if not p.exists() or not tracked(repo, rel):
            continue
        if cand.markers:
            if not p.is_file():
                continue
            text = text_of(p)
            if not all(re.search(m, text) for m in cand.markers):
                continue
        return rel
    return None


def surfaces_for(row_key: str) -> dict[str, str | None]:
    repo = ESTATE / row_key
    cells: dict[str, str | None] = {}
    for surface in SURFACES:
        found = None
        for cand in RULES[surface]:
            found = resolve(repo, cand)
            if found:
                break
        if found is None and (row_key, surface) in NAMED_CHECKS:
            found = resolve(repo, NAMED_CHECKS[(row_key, surface)])
        cells[surface] = found
    return cells


def build_rows() -> tuple[list[dict], list[str]]:
    """The nine rows, ordered by first_commit, plus provenance lines."""
    rows, provenance = [], []
    for spec in ROWS:
        repo = ESTATE / spec["key"]
        if not (repo / ".git").exists():
            raise RuntimeError(f"sibling repository missing: {repo}")
        if spec["era"] not in ERAS:
            raise RuntimeError(f"{spec['key']}: era {spec['era']!r} is not one of the five")
        first, last = commit_dates(repo)
        head = git(repo, "rev-parse", "--short", "HEAD").strip()
        provenance.append(f"{spec['key']:34} branch={branch_of(repo):8} HEAD={head} "
                          f"first={first} last={last}")
        cells = surfaces_for(spec["key"])
        for surface, rel in cells.items():
            if rel is not None and not (repo / rel).exists():
                raise RuntimeError(f"{spec['key']}: {surface} resolved to a path "
                                   f"that does not exist: {rel}")
        rows.append({
            "key": spec["key"],
            "name": spec["name"],
            "site_slug": spec["site_slug"],
            "era": spec["era"],
            "stack": spec["stack"],
            "first_commit": first,
            "last_commit": last,
            "surfaces": cells,
            "retro": None,
        })
    rows.sort(key=lambda r: (r["first_commit"], r["key"]))
    return rows, provenance


# ---------------------------------------------------------------------------
# The thin lane: VIZ-PRINCIPLES versions dated from cascadia-standards' log
# ---------------------------------------------------------------------------


def build_standard() -> list[dict]:
    """One entry per version. Date = the first commit, in date order across
    both of the repository's roots, whose VIZ-PRINCIPLES.md carries that
    version in its header. A version never seen as the live header is null."""
    if not (STANDARDS_REPO / ".git").exists():
        raise RuntimeError(f"standards repository missing: {STANDARDS_REPO}")
    shas = git(STANDARDS_REPO, "rev-list", "--reverse", "--date-order", "HEAD").split()
    roots = set(git(STANDARDS_REPO, "rev-list", "--max-parents=0", "HEAD").split())
    first_seen: dict[str, str] = {}
    for sha in shas:
        r = subprocess.run(["git", "-C", str(STANDARDS_REPO), "show", f"{sha}:{VIZ_PRINCIPLES}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            continue
        for line in r.stdout.splitlines()[:10]:
            m = VIZ_HEADER.match(line)
            if m:
                first_seen.setdefault(m.group(1), sha)
                break
    entries = []
    for v in VERSIONS:
        sha = first_seen.get(v)
        if sha is None:
            entries.append({"version": v, "date": None, "commit": None,
                            "basis": "no commit in cascadia-standards introduces this "
                                     "version's header; the log cannot settle a date"})
            continue
        date = git(STANDARDS_REPO, "log", "-1", "--format=%as", sha).strip()
        subject = git(STANDARDS_REPO, "log", "-1", "--format=%s", sha).strip()
        basis = f"header first appears at {sha[:7]}: {subject}"
        if sha in roots:
            basis += ("; a root commit, so the document entered the log already at "
                      "this version and the date is an upper bound on when it landed")
        entries.append({"version": v, "date": date, "commit": sha, "basis": basis})
    return entries


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def matrix_text(rows: list[dict]) -> str:
    """The matrix as text: nine rows by fourteen columns, then the paths."""
    cols = SURFACES
    head = f"{'row':34} " + " ".join(f"{i + 1:>2}" for i in range(len(cols)))
    lines = [head]
    for r in rows:
        marks = " ".join(" X" if r["surfaces"][s] else " ." for s in cols)
        lines.append(f"{r['key']:34} {marks}")
    lines.append("")
    lines.append("columns: " + ", ".join(f"{i + 1}={s}" for i, s in enumerate(cols)))
    lines.append("")
    for r in rows:
        lines.append(f"{r['key']}  ({r['era']}; {r['first_commit']} to {r['last_commit']})")
        for s in cols:
            if r["surfaces"][s]:
                lines.append(f"    {s:26} {r['surfaces'][s]}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="compare in-memory output with disk; write nothing")
    args = ap.parse_args()

    rows, provenance = build_rows()
    standard = build_standard()
    builds_text, standard_text = dumps(rows), dumps(standard)

    print("Sibling repositories as read (branch, HEAD, oldest and newest author dates):")
    for line in provenance:
        print("  " + line)
    print()
    print(matrix_text(rows))
    print()
    print("standard.json:")
    for e in standard:
        print(f"  v{e['version']:4} {e['date'] or 'null':10} {e['basis']}")
    print()

    if args.check:
        ok = True
        for path, text in ((BUILDS_JSON, builds_text), (STANDARD_JSON, standard_text)):
            on_disk = path.read_bytes() if path.exists() else None
            same = on_disk == text.encode("utf-8")
            print(f"  {'SAME' if same else 'DIFFERS':8} {path.relative_to(REPO).as_posix()}")
            ok = ok and same
        print("\nINVENTORY CHECK:", "byte-identical" if ok else "DIFFERS from disk")
        return 0 if ok else 1

    DATA.mkdir(exist_ok=True)
    for path, text in ((BUILDS_JSON, builds_text), (STANDARD_JSON, standard_text)):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"  wrote {path.relative_to(REPO).as_posix()} ({len(text.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
