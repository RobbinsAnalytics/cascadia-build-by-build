# Build by Build: spec

*v0.2 · 2026-09-16 · v0.2 removes the retired title from the Names table, which v0.1 spelled out in the sentence retiring it; Part 0's own final check caught it. Written from the Build by Build Cowork project. Durable: says what must be true when each part is done, carries nothing perishable. Prompts are generated from this, one part at a time, after the previous part reports (SESSION-RULES rule 9). Aaron approved the ideation this spec encodes on 2026-09-16.*

---

## Layer 0

**What this build proves that the portfolio does not already prove.** The portfolio proves nine modules, each testable on its own. It does not show a reader that the test surface widened build by build, and a qualified reader in an active process reported not knowing what he was looking at. This build shows the progression so nobody has to derive it from nine separate pages.

**Who reads it.** A hiring manager or interviewer with ninety seconds, arriving cold from the homepage. Secondarily Aaron, in an interview, opening it as the portfolio walk before pivoting to one module.

**The honest new skill.** Reading the estate's own repositories as data and rendering a progression without inventing a score. The only new mechanism is a data file one entry per build that a later retrospective skill appends to.

**Is a module the right instrument.** Yes, with one difference from every predecessor: it has no data of its own. Its source is the other nine repositories, read-only. That makes it the second class of build ESTATE-STATE §3 does not yet name (parking lot §10b); recording the class is the Estate project's job, not this build's.

## Names and places

| Thing | Value |
|---|---|
| Module name | Build by Build |
| Local directory and GitHub repository | `cascadia-build-by-build` (one-name rule, REMOTE-CONVENTION.md) |
| Remote | `https://github.com/RobbinsAnalytics/cascadia-build-by-build.git` |
| Published page | `https://www.robbinsanalytics.com/cascadia-build-by-build/` |
| Site case study | `projects/cascadia-build-by-build.qmd` in `RobbinsAnalytics.github.io` |
| Former working title | Retired 2026-09-16 and not spelled here, so that no copy of this spec carries it. It must not appear in the repo, the page or the site. The Build by Build Cowork project holds the record of what it was and why it went. |

## Standing decisions (Aaron's, 2026-09-16)

1. Rows are the nine module repositories. Build by Build is not a row.
2. The standard's version chain (VIZ-PRINCIPLES v1.0 to v2.8) is a thin second lane under the module rows.
3. Five eras: Enterprise-shaped; Frozen and validated; Reviewed and registered; Operated; Re-derived.
4. One chart: the test-surface matrix. No complexity index. No tool-convergence chart; the stack is a word in the row label.
5. No page-level "still trusted, not tested" section. Question three of the retro appears only inside the current build's retro block and as each era's "what the next era brought under test."
6. The interview pivot is verbal. The page ends at a list of modules; Aaron continues.
7. `interview-portfolio-walk.md` (Job Search project) informs the walk section. It is not reproduced.
8. Older modules are deliberately not retrofitted (parking lot §5). An empty cell is a fact, never a debt. Nothing on the page implies one is owed.
9. No retrospectives are reconstructed. Rows are synthesized from what is on disk.
10. Every filled cell links to the artifact it names. That is the page's own test.

## Parts

### Part 0: repository and guard layer

Rooted at `C:\Projects`, deliberately, per the Revenue Assurance and Fee Examiner precedent: hooks load only from the primary working directory, so the session that installs them is never governed by them. Root commit on `main`.

**Done when:** the directory exists with the starter kit installed and activated (`core.hooksPath` set, `.githooks/pre-commit` tracked `100755`, test matrix passing); `CLAUDE.md`, `README.md`, `governance/spec.md` (this document) and `governance/decision-record.md` (Layer 0 above, as D0) are committed in the root commit; the remote is set and the root commit pushed; nothing under `src/`, `data/` or `docs/` exists.

### Part 1: the data layer, stop at the numbers

Rooted in `cascadia-build-by-build`. Branch `build/part1-inventory`.

**Produces**

- `src/inventory.py`: reads the nine sibling repositories read-only, writes `data/builds.json`. Never writes outside this repo. Never runs `git status` in a sibling.
- `data/builds.json`: one entry per row, schema below.
- `data/standard.json`: the thin lane. One entry per VIZ-PRINCIPLES version, with the date each version landed, read from `cascadia-standards` (change-log headings at `design-system/VIZ-PRINCIPLES.md` and the archive, dated from that repo's log).
- `governance/surfaces.md`: the column definitions, one paragraph each: what the surface is, what artifact counts as evidence, what does not.
- `governance/freeze.toml` protecting `data/*`; `src/validate_freeze.py` copied verbatim from `cascadia-standards/templates/validate_freeze.py`. The template gate passes untracked protected paths (parking lot §8a); `CLAUDE.md` says so.
- `src/validate.py`: every filled cell's path exists on disk; every row's repo exists; dates are ordered; no surface is filled for a build whose era precedes the era that introduced it unless the artifact is actually there (the matrix is allowed to surprise, but the surprise must be a file).
- A report that prints the matrix as text, rows by columns, filled or empty, with the artifact path per filled cell.

**Row schema** (`data/builds.json`, array, ordered by `first_commit`)

```
{
  "key":          "cascadia-finance-analytics",     // local directory name
  "name":         "Cascadia Finance",
  "site_slug":    "cascadia-finance",               // projects/<slug>.qmd on the site
  "era":          "Frozen and validated",
  "stack":        "Python, SQLite, ECharts",         // one short phrase, from the site's own table
  "first_commit": "2026-07-21",                     // git log, oldest commit, that repo
  "last_commit":  "2026-08-26",
  "surfaces": {
    "one_command_rebuild":      "run_build.ps1" | null,
    "frozen_source":            "governance/freeze.toml" | null,
    "source_register":          null,
    "row_count_validation":     "src/validate.py" | null,
    "validation_report":        "governance/validation_report.md" | null,
    "tests_as_code":            null,
    "independent_rederivation": null,
    "golden_fixture":           null,
    "negative_controls":        null,
    "chart_review":             "governance/chart-review.md" | null,
    "reading_panel":            null,
    "metric_register":          null,
    "scheduled_run_with_health":null,
    "reconciliation_published": null
  },
  "retro": null                                     // filled by the future retro skill; shape below
}
```

Fourteen surfaces in four bands: **Data** (one-command rebuild; frozen source; source register with hashes), **Numbers** (row-count validation; validation report; tests as code; independent re-derivation; golden fixture; negative controls), **Presentation** (chart review; blind reading panel; metric register), **Operation** (scheduled run with health and run history; reconciliation published including failures). A cell holds a repo-relative path or null. Nothing else. No score, no level, no weight.

`retro`, when present: `{ "could_test_at_start": [..], "can_test_now": [..], "had_to_trust": [..], "next_under_test": [..], "written": "YYYY-MM-DD" }`. Part 1 sets it to null for every row. The retrospective skill, when Aaron creates it, writes it. Revenue Assurance has a formal retrospective in its Cowork project; if Aaron supplies it, Part 1 may fill that one row from it, verbatim, and no other.

**Era membership** is fixed by this spec and carried in the file: Enterprise-shaped (Medical Devices, Pharmacy, Staffing); Frozen and validated (Finance); Reviewed and registered (Deal Desk, Control Tower); Operated (Matter Ledger, Fee Examiner); Re-derived (Revenue Assurance). A later build gets an era when its row is written.

**Done when:** the four gates exit zero (`validate.py`, `validate_freeze.py` after the freeze commit, the test matrix, and the inventory re-run producing a byte-identical file); the text matrix is in the report; Aaron has read the numbers. **No page, no chart, no site change in Part 1.** Part 2 is briefed only after Aaron reads the matrix.

### Part 2: the page

Rooted in `cascadia-build-by-build`. Branch `build/part2-page`. Briefed from this spec plus Part 1's report.

**Produces** `docs/index.html` built by `src/build_page.py` from `data/builds.json` and `data/standard.json` only, in this order:

1. **Lede.** Title "Build by Build". One sentence saying what the page is and that every filled cell links to the file it names. The motto is the site's, not repeated as a slogan here.
2. **The matrix.** Rows oldest at top; the fourteen columns in their four bands; a filled cell is a link, an empty cell is empty; the stack as a word in the row label; the era as a group label down the left; the standard's versions as a thin lane beneath, positioned by date. Title carries what the plot shows (Rule 7.1). Working title, to be tested by the panel: "Each build kept every test the last one had." No colour scale. No score.
3. **Eras.** Five blocks. Each: what could be tested, what had to be trusted, what the next era brought under test. Three lines. Each names its modules with links. The current build's block carries its four retro questions in full when a retro exists in the data; until then, the same three lines.
4. **The walk.** Era by era in short prose, ending in a list of the nine modules with one line each. The page stops there.
5. **Provenance strip.** Generated date, `builds.json` freeze, standard HEAD, per Rule 4.2.

Everything on the page is generated from the two data files except the era prose and the walk, which live in `src/` as text the builder inlines. Era prose is Aaron's voice; Part 2 drafts it and reports it for his edit before publish.

Rendering: `src/render_charts.py` renders the matrix at the K6 ladder widths as `CHART-REVIEW.md` names them, to `docs/renders/`, for the Estate project's reading panel. Images only cross to the panel. `governance/chart-review.md` and `governance/pre-panel-notes.md` per precedent. Stylesheet copied from the Revenue Assurance precedent (there is no design-system stylesheet; parking lot §8d) and **every `@font-face url()` verified to resolve on the published path** before publish, because the precedent's fonts 404 (§8d).

**Done when:** page builds offline from the data files; renders exist at every K6 width; chart review filed; renders handed to the Estate project; panel record returned and dispositioned; `main` merged; page live at its path.

### Part 3: surfacing on the site

Rooted in `RobbinsAnalytics.github.io`. One branch. Briefed after Part 2 is live. The `surface-module` skill in that repo walks the module additions; the items below are what this build adds on top.

1. `projects/cascadia-build-by-build.qmd` and its navbar entry, per the skill.
2. `index.qmd` "The Cascadia Portfolio" section: the paragraph shrinks to its first sentence and a link to the page. The teaser is text and a link only. No timeline in the section.
3. `index.qmd` hero: remove the `.hero-motto` line "Proof is the Point"; "Trust What You Can Test" becomes the subhead alone (parking lot §7b, Aaron's decision).
4. `tools/build_thumbs.py`: the portfolio card's "eight modules" and "Eight governed BI modules" become the true count (parking lot §8h); a `MODULES` entry for Build by Build so its OG card is generated.
5. Conditional, Aaron's call before issue: the `Live` badge resolution (parking lot §7a: remove from one card, remove from every synthetic module, or rename site-wide to `Published`).
6. Conditional, own commit: guard or remove `workflow_dispatch` in `.github/workflows/publish.yml` (parking lot §8h). Unrelated to content; separable if Aaron strikes it.

Visual-regression baselines for `index` move at every width; repeat the surfacing session's pattern (regenerate on the runner, commit the index images, nothing else).

**Done when:** the case study and teaser are live, the hero carries one line, the portfolio card count is true, and the homepage is handed to the Estate project for the panel it has never had (parking lot §10a).

## Auto-update contract

`data/builds.json` is the page's only input for rows. A new build's row is appended by the retrospective skill, or by re-running `src/inventory.py` and committing the diff as a deliberate refreeze. `src/inventory.py` re-run against an unchanged estate must produce a byte-identical file; that is the test that the inventory is a function of disk and not of the session that ran it.

## Owed elsewhere, not in any part

- `hook_manifest.json` entry for `cascadia-build-by-build`: a `cascadia-standards` session, after Part 0.
- ESTATE-STATE §3 second class of build (§10b) and the retrospective row in §3a (§10c): the Estate project.
- Reading panel on the homepage (§10a): the Estate project, after Part 3.
- The retrospective skill: Aaron creates it. Part 1's `retro` field is its contract.
- `templates/validate_freeze.py` untracked-path fix and the `cfg_path` NameError (§8a): a `cascadia-standards` session. This module's copy carries the defect until then and its `CLAUDE.md` says so.

## Parking lot disposition

| Item | Folded in | Where | Why or why not |
|---|---|---|---|
| §7b hero motto | Yes | Part 3 | Decided; same file the teaser edits |
| §7a Live badge | Conditional | Part 3 | Aaron's call among three options before the brief issues |
| §8h thumb count | Yes | Part 3 | Same `MODULES` list Part 3 must edit anyway |
| §8h `workflow_dispatch` | Conditional, own commit | Part 3 | Same repo, unrelated to content; strike if unwanted |
| §8h surface-module grid cap | No | | Skill edit; hits the §1 wall |
| §8d font 404 | Yes, as a must | Part 2 | The page copies the precedent's stylesheet and would inherit the 404 |
| §8d stylesheet decision | No | | Aaron's structural call; the page copies precedent either way |
| §8b index.lock | Yes | Part 0 | The kit `CLAUDE.md` placeholder gets the rule for this repo |
| §8a validate_freeze | No | | Template fix belongs in `cascadia-standards`; `CLAUDE.md` carries the caveat |
| §2 freeze.toml not instantiated | Yes | Part 1 | Instantiate it for real, protecting `data/*` |
| §2 no remote configured | Yes | Part 0 | Remote set before the first surviving commit |
| §2 `Bash(python src/*)` allow | Yes | Part 0 | One line in `settings.json`, matching Revenue Assurance |
| §5 not retrofitted | Yes, as a rule | Part 2 | An empty cell is a fact, never a debt |
| §10a, §10b, §10c | No | Estate project | Not a Code session's to write |
| §3, §3a, §8c, §8e, §8f, §8g | No | | Standard or skill changes, the author's |
| §9 Revenue Assurance candidates | No | | Belong to that module |
