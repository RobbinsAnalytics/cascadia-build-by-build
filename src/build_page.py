#!/usr/bin/env python3
"""build_page.py: write docs/index.html from data/builds.json and data/standard.json.

Every figure on the page (a count, a first appearance, a running total, a
date, a link target) is computed here from the two data files. The prose
lives in src/page_text.py as plain strings with tokens the builder fills;
no figure is typed there either (K2). docs/index.html is generated and never
edited by hand.

The one chart is an HTML table, not a canvas: the matrix is categorical, the
table is its own data layer (Rule 5.1), the caption carries the finding
(Rule 3.1) and a description paragraph carries the shape. No ECharts ships.

The page reads governance/freeze.toml for the as-of date and the freeze
commit only, so the provenance strip can name the freeze the numbers come
from. Rows and cells come from the data files and nowhere else.

    python src/build_page.py
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import tomllib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "src"))
import page_text as T  # noqa: E402
from inventory import BANDS, SURFACES, VERSIONS  # noqa: E402

SITE = "https://www.robbinsanalytics.com"
PAGE_URL = f"{SITE}/cascadia-build-by-build/"
THUMB_URL = f"{SITE}/assets/thumb-build-by-build.png"
REPO_URL = "https://github.com/RobbinsAnalytics/cascadia-build-by-build"
GITHUB = "https://github.com/RobbinsAnalytics"

# Surface display names. The soft hyphens (&shy;) are where a header may break
# at the design width; nothing rotates (Rule 2.8). Below the declared
# breakpoint the header shows the number alone and the key under the table
# carries the name (Rule 5.5: abbreviated by a declared mapping, never deleted).
SURFACE_NAMES = {
    "one_command_rebuild": "One-com&shy;mand re&shy;build",
    "frozen_source": "Frozen source",
    "source_register": "Source regis&shy;ter",
    "row_count_validation": "Row-count valid&shy;ation",
    "validation_report": "Valid&shy;ation report",
    "tests_as_code": "Tests as code",
    "independent_rederivation": "Inde&shy;pen&shy;dent re-deri&shy;va&shy;tion",
    "golden_fixture": "Golden fixture",
    "negative_controls": "Nega&shy;tive controls",
    "chart_review": "Chart review",
    "reading_panel": "Reading panel",
    "metric_register": "Metric regis&shy;ter",
    "scheduled_run_with_health": "Sched&shy;uled run with health",
    "reconciliation_published": "Recon&shy;cili&shy;ation pub&shy;lished",
}
BAND_ABBR = {"Data": "D", "Numbers": "N", "Presentation": "P", "Operation": "O"}
# Display-only soft hyphens for the era labels in their narrow sticky column.
ERA_SHY = {"Enterprise-shaped": "Enter&shy;prise-shaped", "Frozen and validated": "Frozen and vali&shy;dated",
           "Reviewed and registered": "Re&shy;viewed and regis&shy;tered", "Operated": "Oper&shy;ated",
           "Re-derived": "Re-derived"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen"]


def plain(name_html: str) -> str:
    return name_html.replace("&shy;", "")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def month(iso: str) -> str:
    y, m, _ = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def asset_v(name: str) -> str:
    """Content-hashed asset URL (K7)."""
    b = (DOCS / "assets" / name).read_bytes()
    return f"assets/{name}?v={hashlib.md5(b).hexdigest()[:10]}"


# ---------------------------------------------------------------------------
# facts, all from the two data files
# ---------------------------------------------------------------------------

def load() -> tuple[list[dict], list[dict], dict]:
    builds = json.loads((DATA / "builds.json").read_text(encoding="utf-8"))
    standard = json.loads((DATA / "standard.json").read_text(encoding="utf-8"))
    freeze = tomllib.loads((REPO / "governance" / "freeze.toml").read_text(encoding="utf-8"))["freeze"]
    if [r["first_commit"] for r in builds] != sorted(r["first_commit"] for r in builds):
        raise SystemExit("builds.json rows are not in first_commit order")
    if [e["version"] for e in standard] != VERSIONS:
        raise SystemExit("standard.json versions are not the expected list")
    return builds, standard, freeze


def facts(builds: list[dict]) -> dict:
    """First appearance per surface, counts per build, running count."""
    first: dict[str, str] = {}
    for r in builds:
        for s in SURFACES:
            if r["surfaces"][s] and s not in first:
                first[s] = r["key"]
    by_key = {r["key"]: r for r in builds}
    seen: set[str] = set()
    per: dict[str, dict] = {}
    for i, r in enumerate(builds, 1):
        filled = [s for s in SURFACES if r["surfaces"][s]]
        firsts = [s for s in filled if first[s] == r["key"]]
        seen |= set(filled)
        per[r["key"]] = {"index": i, "n": len(filled), "firsts": len(firsts),
                         "first_list": firsts, "seen": len(seen)}
    if len(first) != len(SURFACES):
        raise SystemExit("not every surface appears in some build")
    return {"first": first, "per": per, "by_key": by_key,
            "by_name": {r["name"]: r for r in builds}}


def cell_url(r: dict, path: str) -> str:
    kind = "tree" if path.endswith("/") else "blob"
    return f"{GITHUB}/{r['remote']}/{kind}/{r['default_branch']}/{path}"


def case_study_url(r: dict) -> str:
    return f"{SITE}/projects/{r['site_slug']}.html"


def link(r: dict) -> str:
    return f'<a href="{esc(case_study_url(r))}">{esc(r["name"])}</a>'


TOKEN = re.compile(r"\{(link|n|seen|firsts|first):([^}]+)\}")


def fill(text: str, F: dict) -> str:
    """Resolve prose tokens; fail on an unknown one (K2 for the prose)."""
    def sub(m: re.Match) -> str:
        kind, arg = m.group(1), m.group(2)
        if kind == "link":
            if arg not in F["by_name"]:
                raise SystemExit(f"prose links to an unknown module: {arg}")
            return link(F["by_name"][arg])
        if kind == "first":
            if arg not in F["first"]:
                raise SystemExit(f"prose names an unknown surface: {arg}")
            return link(F["by_key"][F["first"][arg]])
        if arg not in F["per"]:
            raise SystemExit(f"prose names an unknown build: {arg}")
        return WORDS[F["per"][arg][kind]].capitalize() if m.start() == 0 else WORDS[F["per"][arg][kind]]
    out = TOKEN.sub(sub, esc(text).replace("&#x27;", "'"))
    if "{" in out:
        raise SystemExit(f"unresolved token in prose: {out[:80]}")
    return out


# ---------------------------------------------------------------------------
# the matrix
# ---------------------------------------------------------------------------

def lane_positions(builds: list[dict], standard: list[dict]) -> dict[int, list[dict]]:
    """Boundary index -> dated versions whose date falls there. Boundary i is
    the gap before row i (0-based), so boundary len(builds) is after the last."""
    dates = [r["first_commit"] for r in builds]
    out: dict[int, list[dict]] = {}
    for e in standard:
        if e["date"] is None:
            continue
        i = 0
        while i < len(dates) and dates[i] <= e["date"]:
            i += 1
        out.setdefault(i, []).append(e)
    return out


def lane_row(entries: list[dict] | None, colspan: int, undated: bool = False) -> str:
    if undated:
        body = (f'<span class="lane-label">{esc(T.LANE_LABEL)}</span> '
                f'<span class="lane-undated">{esc(T.LANE_UNDATED)}</span>')
    else:
        marks = " ".join(
            f'<span class="lane-mark"><span class="lane-tick" aria-hidden="true"></span>'
            f'v{esc(e["version"])} <span class="lane-date">{esc(e["date"])}</span></span>'
            for e in entries)
        body = f'<span class="lane-label">{esc(T.LANE_LABEL)}</span> {marks}'
    return f'<tr class="lane"><td colspan="{colspan}"><div class="stick">{body}</div></td></tr>\n'


def annotation_row(text: str, colspan: int, primary: bool) -> str:
    cls = "annotation primary" if primary else "annotation secondary"
    return (f'<tr class="{cls}"><td colspan="{colspan}"><div class="stick">'
            f'<span class="ann-tick" aria-hidden="true"></span>{esc(text)}</div></td></tr>\n')


def matrix_table(builds: list[dict], standard: list[dict], F: dict, as_of: str) -> tuple[str, dict]:
    ncols = 2 + len(SURFACES)
    lanes = lane_positions(builds, standard)
    n = len(builds)

    # Which annotations go where, and their text (figures filled here).
    fin = F["by_name"]["Cascadia Finance"]["key"]
    last = builds[-1]["key"]
    if F["per"][last]["seen"] != len(SURFACES) or "golden_fixture" not in F["per"][last]["first_list"]:
        raise SystemExit("the primary annotation's fact is not true of the data")
    if F["per"][fin]["firsts"] != max(p["firsts"] for p in F["per"].values()):
        raise SystemExit("the secondary annotation's fact is not true of the data")
    ann_primary = T.ANNOTATION_PRIMARY
    ann_secondary = T.ANNOTATION_SECONDARY.format(firsts=WORDS[F["per"][fin]["firsts"]])
    for a in (ann_primary, ann_secondary):
        if len(a.split()) > 14:
            raise SystemExit(f"annotation exceeds fourteen words: {a}")

    # Rows in order, each tagged with the era group it belongs to (or None for
    # a lane between two eras), so the era header's rowspan can be computed.
    seq: list[tuple[str | None, str]] = []
    for i, r in enumerate(builds):
        for e in lanes.get(i, []) if i in lanes else []:
            pass
        if i in lanes:
            prev_era = builds[i - 1]["era"] if i > 0 else None
            group = r["era"] if prev_era == r["era"] else None
            seq.append((group, lane_row(lanes[i], ncols - 1 if group else ncols)))
        seq.append((r["era"], build_row(r, F)))
        if r["key"] == fin:
            seq.append((r["era"], annotation_row(ann_secondary, ncols - 1, primary=False)))
        if r["key"] == last:
            seq.append((r["era"], annotation_row(ann_primary, ncols - 1, primary=True)))
    if n in lanes:
        seq.append((None, lane_row(lanes[n], ncols)))

    # Emit, adding the era header with rowspan on each group's first row.
    body = lane_row(None, ncols, undated=True)
    i = 0
    while i < len(seq):
        group, row_html = seq[i]
        if group is None:
            body += row_html
            i += 1
            continue
        j = i
        while j < len(seq) and seq[j][0] == group:
            j += 1
        span = j - i
        era_th = f'<th scope="rowgroup" class="era" rowspan="{span}"><span>{ERA_SHY.get(group, esc(group))}</span></th>'
        body += seq[i][1].replace("<tr class=\"build\">", f"<tr class=\"build\">{era_th}", 1)
        for k in range(i + 1, j):
            body += seq[k][1]
        i = j

    head_bands = "".join(
        f'<th scope="colgroup" colspan="{len(cols)}" class="band">'
        f'<span class="name">{esc(band)}</span><span class="abbr" aria-hidden="true">{BAND_ABBR[band]}</span></th>'
        for band, cols in BANDS.items())
    head_surfaces = "".join(
        f'<th scope="col" class="surface" id="col-{s}"><span class="num">{i + 1}</span>'
        f'<span class="name">{SURFACE_NAMES[s]}</span></th>'
        for i, s in enumerate(SURFACES))
    subtitle = T.MATRIX_SUBTITLE.format(as_of=as_of)
    table = f'''<table class="matrix" aria-labelledby="matrix-title" aria-describedby="matrix-sub matrix-summary">
<thead>
<tr class="bands"><th scope="col" rowspan="2" class="era-h">Era</th><th scope="col" rowspan="2" class="build-h">Build</th>{head_bands}</tr>
<tr class="surfaces">{head_surfaces}</tr>
</thead>
<tbody>
{body}</tbody>
</table>'''
    return table, {"lanes": {str(k): [e["version"] for e in v] for k, v in lanes.items()},
                   "annotations": [ann_primary, ann_secondary], "subtitle": subtitle}


def build_row(r: dict, F: dict) -> str:
    p = F["per"][r["key"]]
    cells = ""
    for s in SURFACES:
        path = r["surfaces"][s]
        if not path:
            cells += '<td class="cell empty"></td>'
            continue
        is_first = F["first"][s] == r["key"]
        label = (f"{plain(SURFACE_NAMES[s])}: {path} in {r['remote']}"
                 + (", the first build to carry it" if is_first else ""))
        cls = "mark first" if is_first else "mark"
        cells += (f'<td class="cell"><a class="{cls}" href="{esc(cell_url(r, path))}" '
                  f'title="{esc(path)}" aria-label="{esc(label)}"><span aria-hidden="true"></span></a></td>')
    head = (f'<th scope="row" class="build-label"><span class="ord" aria-hidden="true">{p["index"]}</span>'
            f'{link(r)}<span class="meta">{esc(r["stack"])} <span class="dot">·</span> <span class="when">{esc(month(r["first_commit"]))}</span></span></th>')
    return f'<tr class="build">{head}{cells}</tr>\n'


def description(builds: list[dict], standard: list[dict], F: dict) -> str:
    """Rule 5.1 layer 1 and Rule 5.2 L1 to L3. Every figure computed above."""
    counts = ", ".join(f"{F['per'][r['key']]['n']} at build {F['per'][r['key']]['index']}" for r in builds)
    firsts = ", ".join(f"{F['per'][r['key']]['firsts']} at build {F['per'][r['key']]['index']}"
                       for r in builds if F["per"][r["key"]]["firsts"])
    seen = ", ".join(f"{F['per'][r['key']]['seen']} by build {F['per'][r['key']]['index']}" for r in builds)
    dated = [e for e in standard if e["date"]]
    undated = [e["version"] for e in standard if not e["date"]]
    l1 = (f"A table of {len(builds)} builds, one per row, oldest at the top, by {len(SURFACES)} test "
          f"surfaces, one per column, in four bands: {', '.join(BANDS)}. A square marks a surface the "
          f"build carries; a diamond marks the first build to carry it; an empty cell means the build "
          f"does not carry it.")
    l2 = (f"Surfaces carried per build: {counts}. First appearances: {firsts}. Surfaces seen so far, "
          f"build by build: {seen}. Rows between the builds mark the design standard's versions by "
          f"date: {len(dated)} dated versions from v{dated[0]['version']} on {dated[0]['date']} to "
          f"v{dated[-1]['version']} on {dated[-1]['date']}; {', '.join('v' + v for v in undated)} are undated.")
    l3 = ("The marks thicken down the table, and the diamonds step to the right as the rows descend: "
          "the first two columns fill from the top, the middle columns from the fourth row, and the "
          "last two columns from the seventh.")
    return f"{l1} {l2} {l3}"


# ---------------------------------------------------------------------------
# the page
# ---------------------------------------------------------------------------

T_TITLE = "Two ways to check a number at build one. Fourteen by build nine."


def check_title(builds: list[dict], F: dict) -> None:
    first_key, last_key = builds[0]["key"], builds[-1]["key"]
    if F["per"][first_key]["n"] != 2 or F["per"][first_key]["index"] != 1:
        raise SystemExit("the title's first number is not what the data says")
    if F["per"][last_key]["seen"] != 14 or F["per"][last_key]["index"] != 9:
        raise SystemExit("the title's second number is not what the data says")


def eras_html(builds: list[dict], F: dict) -> str:
    order = []
    for r in builds:
        if r["era"] not in order:
            order.append(r["era"])
    if set(order) != set(T.ERAS):
        raise SystemExit("page_text.ERAS does not match the eras in the data")
    out = ""
    for era in order:
        members = ", ".join(link(r) for r in builds if r["era"] == era)
        block = T.ERAS[era]
        out += (f'<section class="era-block"><h3>{esc(era)}</h3>'
                f'<p class="members">{members}</p>'
                f'<dl><dt>What could be tested</dt><dd>{fill(block["tested"], F)}</dd>'
                f'<dt>What had to be trusted</dt><dd>{fill(block["trusted"], F)}</dd>'
                f'<dt>What the next era brought under test</dt><dd>{fill(block["next"], F)}</dd></dl>'
                f'</section>\n')
    return out


def walk_html(builds: list[dict], F: dict) -> str:
    paras = "".join(f"<p>{fill(p, F)}</p>\n" for p in T.WALK)
    if set(T.MODULE_LINES) != {r["key"] for r in builds}:
        raise SystemExit("page_text.MODULE_LINES does not match the rows")
    items = "".join(f'<li>{link(r)}<span class="line">{fill(T.MODULE_LINES[r["key"]], F)}</span></li>\n'
                    for r in builds)
    return (f'{paras}<p class="list-intro">{esc(T.WALK_LIST_INTRO)}</p>\n<ol class="modules">\n{items}</ol>\n'
            f'<p class="closing">{esc(T.CLOSING_AARON)}</p>\n')


def key_html() -> str:
    parts = []
    for band, cols in BANDS.items():
        items = " ".join(f'<span class="k"><b>{SURFACES.index(s) + 1}</b> {SURFACE_NAMES[s]}</span>' for s in cols)
        parts.append(f'<span class="band-k"><b>{BAND_ABBR[band]}</b> {esc(band)}:</span> {items}')
    return "<br>\n".join(parts)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Build by Build</title>
<meta name="description" content="@@meta_desc@@">
<meta property="og:type" content="website">
<meta property="og:title" content="Build by Build">
<meta property="og:description" content="@@meta_desc@@">
<meta property="og:image" content="@@thumb_url@@">
<meta property="og:url" content="@@page_url@@">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="@@thumb_url@@">
<link rel="icon" href="@@v_favicon@@" type="image/svg+xml">
<link rel="stylesheet" href="@@v_css@@">
<style>
  .lede { font: 17px/1.65 var(--serif); max-width: 70ch; color: var(--ink); }
  h2 { font: 600 24px/1.3 var(--serif); margin: 34px 0 6px; }
  h3 { font: 600 17px/1.35 var(--serif); margin: 22px 0 4px; }

  /* ---- the matrix card: DOM order summary, table, key, strip; the summary
     renders after the table (Rule 5.1 keeps it first in the DOM). ---- */
  .chart-card { display: flex; flex-direction: column; padding: 14px 12px 10px; }
  .chart-card > .finding { order: 0; margin: 0 2px 2px; font: 600 20px/1.3 var(--serif);
                           color: var(--ink-serif); max-width: 60ch; }
  .chart-card > .sub { order: 0; margin: 0 2px 10px; font: 12.5px/1.5 var(--sans); color: var(--muted);
                       max-width: 78ch; }
  .chart-card > .chart-summary { order: 4; }
  .chart-card > .table-scroll { order: 1; }
  .chart-card > .key { order: 2; }
  .chart-card > .cascadia-provenance { order: 3; }
  .chart-summary { font: 13px/1.6 var(--sans); color: var(--ink-2); margin: 12px 2px 0; max-width: 80ch; }

  .table-scroll { position: relative; overflow-x: auto; overflow-y: hidden; }
  .table-scroll::before, .table-scroll::after {
    content: ""; position: sticky; top: 0; display: none; pointer-events: none; }
  .table-scroll.scrolls.can-right { box-shadow: inset -14px 0 12px -12px rgba(35,43,39,0.35); }
  .table-scroll.scrolls.can-left  { box-shadow: inset 14px 0 12px -12px rgba(35,43,39,0.35); }
  .table-scroll.scrolls.can-left.can-right {
    box-shadow: inset 14px 0 12px -12px rgba(35,43,39,0.35), inset -14px 0 12px -12px rgba(35,43,39,0.35); }

  table.matrix { border-collapse: separate; border-spacing: 0; font: 12px/1.35 var(--sans);
                 color: var(--ink); --era-w: 92px; --build-w: 200px; --cell-w: 48px; }
  table.matrix th, table.matrix td { border-bottom: 1px solid var(--grid); vertical-align: middle;
                                     padding: 4px 3px; text-align: left; background: var(--surface); }
  table.matrix thead th { vertical-align: bottom; color: var(--ink-2); font-weight: 600; }
  table.matrix thead th.band { text-align: center; border-bottom: 2px solid var(--ink-2);
                               padding-bottom: 3px; letter-spacing: 0.04em; }
  table.matrix thead th.surface { width: var(--cell-w); min-width: var(--cell-w); max-width: var(--cell-w);
                                  text-align: center; font-weight: 400; hyphens: manual; overflow-wrap: normal;
                                  padding: 6px 2px 4px; }
  table.matrix thead th.surface .num { display: block; font-weight: 600; color: var(--ink); }
  table.matrix thead th .abbr { display: none; }
  table.matrix th.era-h, table.matrix th.era { position: sticky; left: 0; z-index: 2;
                                               width: var(--era-w); min-width: var(--era-w); max-width: var(--era-w); }
  table.matrix th.build-h, table.matrix th.build-label { position: sticky; left: var(--era-w); z-index: 2;
                                               width: var(--build-w); min-width: var(--build-w); max-width: var(--build-w);
                                               border-right: 1px solid var(--grid); }
  table.matrix th.era { font: 600 12px/1.3 var(--serif); color: var(--ink-2); vertical-align: top;
                        hyphens: manual; overflow-wrap: anywhere;
                        padding-top: 8px; border-right: 1px solid var(--grid); }
  table.matrix th.build-label { font-weight: 400; }
  table.matrix th.build-label .ord { display: inline-block; width: 1.4em; color: var(--muted); font-size: 12px; }
  table.matrix th.build-label a { color: var(--ink); font: 600 13px/1.3 var(--serif); text-decoration: none; }
  table.matrix th.build-label a:hover { text-decoration: underline; }
  table.matrix th.build-label .meta { display: block; color: var(--muted); padding-left: 1.4em; }
  table.matrix th.build-label .meta .when { white-space: nowrap; }
  table.matrix td.cell { text-align: center; width: var(--cell-w); min-width: var(--cell-w); }
  table.matrix td.empty { background: var(--surface); }
  a.mark { display: flex; align-items: center; justify-content: center; width: 100%; min-width: 24px;
           min-height: 28px; margin: 0 auto; text-decoration: none; }
  a.mark > span { display: block; width: 12px; height: 12px; background: var(--ink-2); }
  a.mark.first > span { width: 15px; height: 15px; background: var(--s1);
                        clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%); }
  a.mark:hover > span { outline: 2px solid var(--ink); outline-offset: 1px; }
  a:focus-visible { outline: 2px solid var(--s1); outline-offset: 2px; }
  a.mark:focus-visible { outline: 2px solid var(--s1); outline-offset: -2px; }

  .stick { position: sticky; left: 0; box-sizing: border-box;
           max-width: calc(var(--wrap-w, 100%) - var(--era-w) - 16px); }
  tr.lane td { background: var(--page); color: var(--ink-2); font: 12px/1.5 var(--sans); padding: 2px 6px;
               border-bottom: 1px solid var(--grid); }
  tr.lane .lane-label { font-weight: 600; margin-right: 6px; color: var(--ink-2); }
  tr.lane .lane-mark { display: inline-block; margin-right: 10px; white-space: nowrap; }
  tr.lane .lane-tick { display: inline-block; width: 8px; height: 8px; background: var(--s2);
                       margin-right: 4px; vertical-align: -1px; }
  tr.lane .lane-date { color: var(--muted); }
  tr.annotation td { background: var(--surface); padding: 3px 6px 6px; border-bottom: 1px solid var(--grid); }
  tr.annotation.primary td { font: 600 13px/1.5 var(--serif); color: var(--ink-s1); }
  tr.annotation.secondary td { font: 12px/1.5 var(--serif); color: var(--ink-2); }
  .ann-tick { display: inline-block; width: 0; height: 0; margin: 0 6px 0 2px;
              border-left: 5px solid transparent; border-right: 5px solid transparent;
              border-bottom: 7px solid currentColor; vertical-align: 1px; }

  .key { font: 12px/1.7 var(--sans); color: var(--ink-2); margin: 10px 2px 0; }
  .key .band-k b, .key .k b { color: var(--ink); font-weight: 600; }
  .key .k { display: inline-block; margin-right: 10px; white-space: nowrap; }
  .key .legend { display: block; margin-top: 4px; }
  .key .legend .sq { display: inline-block; width: 10px; height: 10px; background: var(--ink-2); vertical-align: -1px; }
  .key .legend .di { display: inline-block; width: 13px; height: 13px; background: var(--s1); vertical-align: -2px;
                     clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%); }
  .key .legend .lt { display: inline-block; width: 8px; height: 8px; background: var(--s2); vertical-align: -1px; }

  /* Rule 4.2: bottom-left, Evergreen tick, three segments, 11 px Slate moss. */
  .cascadia-provenance { display: flex; align-items: baseline; gap: 7px; margin: 8px 0 0 2px;
                         font: 12px/1.5 var(--sans); color: var(--ink-2); }
  .cascadia-provenance .tick { display: inline-block; width: 3px; height: 11px; background: var(--s1);
                               align-self: center; flex: none; }

  /* Below the declared breakpoint (host < 700 px): numbers only in the header,
     band abbreviations, narrower sticky columns. Nothing rotates. */
  #matrix.narrow table.matrix { --era-w: 54px; --build-w: 104px; --cell-w: 24px; }
  #matrix.narrow table.matrix td.cell { padding: 2px 0; }
  #matrix.narrow table.matrix th.era, #matrix.narrow table.matrix th.build-label { padding: 4px 2px; }
  #matrix.narrow.chart-card { padding-left: 6px; padding-right: 6px; }
  #matrix.narrow table.matrix thead th.surface .name { display: none; }
  #matrix.narrow table.matrix thead th.band .name { display: none; }
  #matrix.narrow table.matrix thead th.band .abbr { display: inline; }
  #matrix.narrow table.matrix th.build-label a { font-size: 12px; }
  #matrix.narrow table.matrix th.build-label .meta { font-size: 12px; line-height: 1.3; }
  #matrix.narrow table.matrix th.era { font-size: 12px; }
  #matrix.narrow a.mark > span { width: 12px; height: 12px; }
  #matrix.narrow a.mark.first > span { width: 14px; height: 14px; }
  #matrix.narrow > .finding { font-size: 17px; }

  /* eras and walk */
  .era-block { margin: 18px 0 0; }
  .era-block .members { margin: 0 0 6px; font: 13px/1.5 var(--sans); color: var(--ink-2); }
  .era-block .members a { color: var(--ink-s1); text-decoration: none; }
  .era-block dl { margin: 0; max-width: 80ch; }
  .era-block dt { font: 600 12px/1.5 var(--sans); color: var(--ink-2); text-transform: uppercase;
                  letter-spacing: 0.06em; margin-top: 8px; }
  .era-block dd { margin: 2px 0 0; font: 14.5px/1.6 var(--sans); color: var(--ink); }
  .era-block dd a, .walk a { color: var(--ink-s1); text-decoration: none; }
  .era-block dd a:hover, .walk a:hover { text-decoration: underline; }
  .walk p { max-width: 78ch; font: 15px/1.65 var(--sans); }
  .walk .list-intro { color: var(--ink-2); margin-bottom: 4px; }
  ol.modules { padding-left: 1.4em; max-width: 80ch; }
  ol.modules li { margin: 8px 0; font: 14.5px/1.55 var(--sans); }
  ol.modules li a { font-weight: 600; }
  ol.modules .line { display: block; color: var(--ink-2); }
  .walk .closing { font: 600 16px/1.5 var(--serif); color: var(--ink-serif); margin-top: 18px; }
  .disclosure p { max-width: 88ch; }
  .disclosure a { color: var(--ink-s1); }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
</head>
<body>
<div class="wrap">

<header class="site-head">
  <p class="kicker"><a href="@@site@@">Cascadia Portfolio</a> · Build by Build</p>
  <h1>Build by Build</h1>
  <p class="lede">@@lede@@</p>
</header>

<h2>The test-surface matrix</h2>
<div class="chart-card" id="matrix">
  <h3 class="finding" id="matrix-title">@@title@@</h3>
  <p class="sub" id="matrix-sub">@@subtitle@@</p>
  <p class="chart-summary" id="matrix-summary">@@summary@@</p>
  <div class="table-scroll" tabindex="0" aria-label="Scrollable matrix">
@@table@@
  </div>
  <p class="key">@@key@@<span class="legend"><span class="sq"></span> the build carries the surface; the cell links to the file &nbsp; <span class="di"></span> the first build to carry it &nbsp; <span class="lt"></span> a design-standard version, placed by date</span></p>
  <div class="cascadia-provenance" role="note"><span class="tick"></span><span>@@prov1@@</span> · <span>@@prov2@@</span> · <span>@@prov3@@</span></div>
</div>

<h2>Five eras</h2>
@@eras@@

<h2>The walk</h2>
<div class="walk">
@@walk@@
</div>

<div class="disclosure">
<h3>About this page</h3>
<p>@@disclosure@@</p>
<p>Source, the inventory script, the surface definitions and the two data files:
<a href="@@repo_url@@">github.com/RobbinsAnalytics/cascadia-build-by-build</a>. Inventory read @@as_of@@; data frozen at commit <code>@@freeze_short@@</code>.</p>
</div>

</div>
<script src="@@v_page@@"></script>
</body>
</html>
"""


def main() -> int:
    builds, standard, freeze = load()
    F = facts(builds)
    check_title(builds, F)
    as_of = freeze["as_of_date"]
    baseline = freeze["baseline"]
    if not re.fullmatch(r"[0-9a-f]{40}", baseline):
        raise SystemExit("freeze.toml baseline is not a commit SHA; freeze the data before building the page")
    table, meta = matrix_table(builds, standard, F, as_of)
    summary = description(builds, standard, F)
    v28 = next(e for e in standard if e["version"] == VERSIONS[-1])
    prov = [
        "Source: nine Cascadia module repositories on GitHub, and cascadia-standards",
        f"read {as_of}, frozen at {baseline[:7]}, standard v{v28['version']} at {v28['commit'][:7]}",
        "cells link to files; empty cells are facts, not debts; three standard versions undated",
    ]
    for seg in prov:
        if " · " in seg:
            raise SystemExit("a provenance segment contains the strip separator (K5)")
    lede = esc(T.LEDE_AARON) + " " + esc(T.LEDE_SECOND)
    meta_desc = ("Which tests each Cascadia module could carry, build by build, and where each kind "
                 "of test first appeared. Every filled cell links to the file it names.")
    out = TEMPLATE
    for k, v in {
        "meta_desc": esc(meta_desc), "thumb_url": THUMB_URL, "page_url": PAGE_URL, "site": SITE,
        "v_favicon": asset_v("favicon.svg"), "v_css": asset_v("cascadia.css"), "v_page": asset_v("page.js"),
        "lede": lede, "summary": esc(summary), "table": table, "key": key_html(),
        "title": esc(T_TITLE), "subtitle": esc(meta["subtitle"]),
        "prov1": esc(prov[0]), "prov2": esc(prov[1]), "prov3": esc(prov[2]),
        "eras": eras_html(builds, F), "walk": walk_html(builds, F),
        "disclosure": esc(T.DISCLOSURE), "repo_url": REPO_URL, "as_of": esc(as_of),
        "freeze_short": baseline[:7],
    }.items():
        out = out.replace(f"@@{k}@@", v)
    if "@@" in out:
        raise SystemExit("unsubstituted token in the template")
    if "—" in out:
        raise SystemExit("an em dash reached the page")
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(out, encoding="utf-8", newline="\n")
    n_links = out.count('class="mark')
    print(f"wrote docs/index.html: {len(out.encode('utf-8'))} bytes, {n_links} cell links, "
          f"lanes at boundaries {meta['lanes']}")
    print("title:", T_TITLE)
    print("[AARON] lede:", T.LEDE_AARON)
    print("[AARON] closing:", T.CLOSING_AARON)
    print("annotations:", meta["annotations"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
