# Decision record: Cascadia Build by Build

*Owner: Aaron Robbins. Opened 2026-09-16, Part 0 (repository and guard layer).*

Each decision below is a fact about this module, with its reason and its
counterfactual. A decision that never becomes an instruction is not adopted, so
each names the file or mechanism that carries it.

---

## D0 · Layer 0, the four answers this build was approved on

**What this build proves that the portfolio does not already prove.** The
portfolio proves nine modules, each testable on its own. It does not show a
reader that the test surface widened build by build, and a qualified reader in
an active process reported not knowing what he was looking at. This build shows
the progression so nobody has to derive it from nine separate pages.

**Who reads it.** A hiring manager or interviewer with ninety seconds, arriving
cold from the homepage. Secondarily Aaron, in an interview, opening it as the
portfolio walk before pivoting to one module.

**The honest new skill.** Reading the estate's own repositories as data and
rendering a progression without inventing a score. The only new mechanism is a
data file one entry per build that a later retrospective skill appends to.

**Is a module the right instrument.** Yes, with one difference from every
predecessor: it has no data of its own. Its source is the other nine
repositories, read-only. That makes it the second class of build ESTATE-STATE
§3 does not yet name (parking lot §10b); recording the class is the Estate
project's job, not this build's.

*Counterfactual:* if the progression were legible from the nine module pages
already, there would be no module. The reader who did not know what he was
looking at is the evidence that it is not.

**Carried by:** `governance/spec.md`, which is the durable statement of this
build and of the standing decisions that follow from these four answers.

---

## D1 · Fourteen surfaces, each with a written detection rule

The matrix has fourteen columns in four bands: Data (one-command rebuild,
frozen source, source register), Numbers (row-count validation, validation
report, tests as code, independent re-derivation, golden fixture, negative
controls), Presentation (chart review, reading panel, metric register) and
Operation (scheduled run with health, reconciliation published). Each column
is defined by a paragraph saying what the surface is, what artifact counts as
evidence, and what does not. The paragraph is the rule; the script implements
the paragraph and never the other way round.

A cell is a repo-relative path or null. No score, no level, no weight, no
count. Where the evidence is a passage inside a file that serves another
purpose, the rule carries a quoted content marker. Where it is one named check
inside a validation script, the cell names the file and the script verifies
the check's own label is still there. An auto-detector by content pattern was
considered for the row-count column and rejected: a pattern that matched the
three real checks and not the hash and reproducibility checks beside them
would be a classifier fitted to nine repositories, presented as a rule.

*Counterfactual:* without a written rule per column, a filled cell is an
opinion, and the page's own test (every filled cell links to the file it
names) proves only that a file exists, not that it is the thing the column
claims.

**Carried by:** `governance/surfaces.md` and `src/inventory.py`.

## D2 · Rows and eras are constants fixed by the spec, not inferred

The nine rows, their names, site slugs, eras and stack phrases are constants
in `src/inventory.py`, copied from `governance/spec.md` and the site's own
table. The script infers nothing about membership or era; it reads dates from
each repository's log and cells from its files. A later build gets a row when
its constants are added, deliberately.

*Counterfactual:* an era inferred from what a repository carries would make the
era a score under another name, and the spec's standing decision 4 forbids the
score.

**Carried by:** `src/inventory.py`, the `ROWS` and `ERAS` constants;
`src/validate.py` fails if the rows on disk are not exactly those constants.

## D3 · Cells link to the artifact on GitHub, at the sibling's default branch

Every filled cell on the page is a link to
`https://github.com/RobbinsAnalytics/<remote>/blob/<default_branch>/<path>`,
or `tree/` where the path is a directory (its cell carries a trailing slash).
Both `remote` and `default_branch` are read from the sibling by
`src/inventory.py` and frozen in `data/builds.json`, because four of the nine
remotes differ from the local directory name (REMOTE-CONVENTION.md's split
pattern) and one default branch is `master`. Data belongs in the data file,
not in the page builder.

Nothing links to a local path, and nothing links to `cascadia-estate`, which
is private. Where a sibling relays its panel record from
`cascadia-estate/panels/` into its own `chart-review.md`, the cell links to
that chart review, as Part 1 recorded.

*Counterfactual:* a builder that derived the remote from the key would be right
for five rows and wrong for four, silently, until the link check ran.

**Carried by:** `src/inventory.py` (the two fields), `src/validate.py` (the
convention check), `src/build_page.py` (the URL form).

## D4 · The title is a claim about first appearances, in a fixed shape

The matrix's title is "Two ways to check a number at build one. Fourteen by
build nine." Its shape is a count of test surfaces at the first build and the
running count of surfaces seen by the last, both readable by counting the
diamond marks. The first working title, "Each build kept every test the last
one had", was retired on 2026-09-17 because it is false on the plot: Matter
Ledger and Fee Examiner lack the one-command rebuild and row-count columns
that every earlier build carried, Finance lacks row-count validation, and
Revenue Assurance lacks the source register and the scheduled run. The
per-row count is not monotone; the running count is, by construction, and
that is what the title claims. The build fails if either number stops being
true of the data.

*Counterfactual:* a title that claimed more than the marks show would be
repeated by readers who never check it (Rule 3.2), and the page's own test,
every cell a link, would not catch it.

**Carried by:** `src/build_page.py` (`T_TITLE`, `check_title()`),
`governance/chart-review.md` 3.2.

*Amended 2026-09-17, after the reading panel.* Three of four seats read
"Fourteen by build nine" as build nine's own score and counted its row (ten).
The second clause now reads "Fourteen had appeared by build nine", the same
shape with the cumulative sense carried by the verb, and the subtitle says
there are fourteen diamonds in the table, one per surface. The numbers and
the build's assertion of them are unchanged.

## D5 · The matrix is an HTML table, not a canvas

The matrix is categorical presence, not quantity: a cell holds a path or
nothing. It is rendered as a real `<table>` with row and column headers, and
every filled cell is a link. A table is its own Rule 5.1 data layer, its
headers are read by assistive technology without a sibling DOM layer, a
canvas cell cannot be a link, and there is no axis to scale. ECharts does not
ship on this page. The class is detailed and the quadrant explanatory (Rules
0.2 and 0.3, declared in the chart review).

*Counterfactual:* a grid drawn on a canvas would need a parallel table for
Rule 5.1 anyway, and its cells could only point at files through a tooltip,
which a static render cannot show.

**Carried by:** `src/build_page.py`, `governance/chart-review.md` §0.

## D6 · No dark mode

The page declares `color-scheme: light` and carries no dark palette. Rule
5.7: dark mode is a second, separately validated palette or it is nothing,
and no second palette exists in the estate.

**Carried by:** `docs/assets/cascadia.css` (`color-scheme: light`),
`governance/chart-review.md` 5.7.

## D7 · The tenth row: Cascadia Early Warning, in the Re-derived era, pending Aaron's call on a sixth

Added 2026-10-07 from a session rooted in `cascadia-early-warning`, on a
branch, with nothing merged. The row is read from disk like the other nine:
`src/inventory.py` resolves its fourteen cells from the repository's own
files, and `data/builds.json` is regenerated, not edited.

**The era.** The spec fixes five eras and says a later build gets an era when
its row is written. Early Warning re-derives every published cell down a
separately written SQL path (the Re-derived move), runs a scheduled live edge
with health and a published reconciliation (the Operated move), and adds a
move no earlier build made: the forecast harness, its periods and its
promotion rule are committed before the first forecast row, the locked test
runs once, and the validator reads the git log to prove both. It takes the
latest era the spec defines, Re-derived, because an era is a label for a
period of the portfolio and not a score, and because inventing a sixth era
("Pre-registered") is a change to the spec that only Aaron makes.

**What this row does not change.** The title's claim ("Fourteen had appeared
by build nine") stays true: the tenth build introduces no fifteenth surface,
so the diamond count is unchanged and so is the sentence. `LEDE_AARON` still
reads "Nine Cascadia modules"; it is Aaron's accepted line and is not
rewritten by a session. The three generated count sentences (the matrix
subtitle, the walk's intro, the disclosure) now say ten.

*Counterfactual:* leaving the row until a retrospective skill exists, which
the spec allows, and which would have left the page saying nine while a
tenth build was live.

**Carried by:** `src/inventory.py` (ROWS); `src/page_text.py`
(`MODULE_LINES`, three count sentences); `governance/spec.md` (rule 1);
`data/builds.json`; `governance/freeze.toml` (as-of and baseline, moved with
the refreeze commit).


*Amended 2026-10-07, same session.* Two build-time checks assumed the last
row is the build where the fourteenth surface appeared: `check_title`
tested the last row's running count and index, and the primary annotation
was anchored on the last row. Both now find the build that introduced the
golden fixture and test that it is build nine with a running count of
fourteen. The title and the annotation text are unchanged.
