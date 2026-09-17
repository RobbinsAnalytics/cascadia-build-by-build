# The fourteen surfaces

*Part 1, 2026-09-16. The column definitions for the test-surface matrix: what
each surface is, what artifact counts as evidence, and what does not. These
paragraphs are the detection rules. `src/inventory.py` implements them and
never the other way round: where the script and a paragraph disagree, the
paragraph is wrong or the script is, and one of them gets fixed.*

A cell holds one repo-relative path or nothing. A directory cell carries a
trailing slash, so a page can link to it as a tree rather than a blob without
reading the sibling itself. The path is the artifact a
reader can open and that the page will link to. Where several artifacts
qualify, the cell carries the most specific one, and the rest are not lost:
they are on disk in the same repository, one click away. An empty cell is a
fact about what a build carried, never a debt.

## How the script reads a paragraph

Each paragraph names candidate artifacts in order of specificity. The script
tries them in that order against the sibling repository and takes the first
that exists on disk and is tracked by that repository's git index. Where the
evidence is a passage inside a file that also serves another purpose (a build
order inside a README, a panel record inside a chart review, a proof section
inside a validation report), the candidate carries a content marker, quoted in
the paragraph, that the file must match. Where the evidence is one named check
inside a validation script, the cell names the file and the script verifies
that the check's own label is still in it, so the cell empties if the check is
removed. Those named checks are listed at the end of this document and in
`src/inventory.py` beside the row they belong to.

The script never writes in a sibling and never runs a command that takes a
sibling's index lock. It reads with `git log`, `git ls-files`, `git show` and
the filesystem.

---

## Data

### `one_command_rebuild`

A single entry point rebuilds the module from its source. **Counts:** a
`run_*.ps1` at the repository root or under `scripts/`; or a documented,
ordered rebuild in `README.md` or `CLAUDE.md` that names the scripts in
sequence, detected by a heading containing "rebuild", or the phrases "run in
this order" or "build order is". **Does not count:** a folder of scripts with
no stated order, or a mention that something "rebuilds from the snapshot"
without saying how. Two of the nine carry no stated order and read empty here
even though each has a working build.

### `frozen_source`

The source data is pinned so the build reads the same bytes every time and the
as-of date is a claim rather than a side effect. **Counts:** `governance/freeze.toml`;
or a committed `data/raw/` snapshot whose manifest states an as-of date (a
JSON key `as_of` or `as_of_date`). **Does not count:** data pulled at build
time, or a generator that reproduces the data on demand without a committed
snapshot. A seeded synthetic snapshot that is committed and dated counts: it is
frozen in the same sense, and the page's reader is asking whether the numbers
can move under the build, not where they came from.

### `source_register`

A record of what was pulled, from where, when, and what it hashes to, so a
reader can prove the build ran against what is committed. **Counts:**
`governance/source-register.md`; or a `manifest.json` under `data/raw/`
carrying a per-file `sha256`. **Does not count:** a README citation, or a
manifest that records URLs and byte counts but no hash. One module's raw
manifest records bytes and an as-of date and no hash; it reads empty here and
that is the right reading.

## Numbers

### `row_count_validation`

The build asserts that what it loaded is what it expected to load, by row
count. **Counts:** a `*validate_rowcounts.sql`; or a validation script with a
named check that compares a row count it computed against a count it did not
compute, from the source table, a manifest, or a stated expectation. **Does
not count:** a count printed in a notebook or a log, or a referential-integrity
check. The three enterprise builds carry the SQL form. Of the later builds,
three carry a named check and are listed at the end; the others validate their
load by hash or by reproducibility, which is a different and stronger claim,
and this column does not pretend to hold it.

### `validation_report`

The validation suite's result is committed, not only printed. **Counts:**
`governance/validation_report*.md` committed in the repository. **Does not
count:** a validation script with no published output, a run log, or a
reconciliation document (that is its own surface).

### `tests_as_code`

Tests live in a test framework's own shape and can be run as tests. **Counts:**
`dbt/tests/` and the model tests beside it; `src/test_*.py` or `test_*.py`;
a `tests/` directory. **Does not count:** assertions inside a build script, or
a validation gate, which is what the two Numbers columns above hold. One
module's only test file tests the page's touch readout in a browser; it is a
test as code and the cell says so by pointing at it.

### `independent_rederivation`

A second, separately written path re-derives the published measures and
compares them cell by cell with what the first path published. **Counts:**
`src/validate_measures.py` whose own docstring says it re-derives (the marker
is the word "re-derive" in its first sixty lines), whether written from a
rules document or written to differ structurally from the builder; or a
KPI-validation SQL run against the BI model, `powerbi/validate_*_kpis.sql`.
**Does not count:** a script that re-reads the first path's output, or a check
inside the validation suite that recomputes a stored column from base facts
without producing the published cells. One module recomputes its three fill
rates from base facts inside its validation suite and compares them with the
stored column; that is a reconciliation, not a second derivation of what the
page shows, and it reads empty here.

### `golden_fixture`

Expected values specified by hand, before the code that must reproduce them.
**Counts:** `tests/golden/` or `test_golden.py`. **Does not count:** expected
values generated by the code under test, including a captured numeric baseline
used to prove a reskin changed no number.

### `negative_controls`

A check suite is fed deliberately wrong values that must trip, and the result
is published beside the real run. **Counts:** `governance/validation_report.md`
carrying a section whose heading contains "can fail" and whose body records
each scenario's outcome as "tripped" or "rejected". **Does not count:** a test
suite alone, a realism check that has only ever seen good data, or a
guard-layer test matrix (every governed repository carries one; it tests the
hooks, not the numbers). Two modules carry this and neither uses the phrase
"negative control": both have a `--prove-failable` flag on the validation
suite. Finance publishes "Proof the checks can fail" (eight checks, all
rejected corrupted data) and Control Tower "Proof the realism audits can fail"
(six audit scenarios and fifteen structural ones, all tripped). Finance's is a
surprise for its era, and the surprise is a file.

## Presentation

### `chart_review`

The author's checklist review of every chart against the design standard,
committed. **Counts:** `governance/chart-review.md`. **Does not count:** a
mention in a README, or a review that lives only in a Cowork project.

### `reading_panel`

A blind, multi-seat read of the rendered charts, returned and dispositioned.
**Counts:** a panel record in its own file, `governance/READING-PANEL*.md`,
`governance/reading-panel-returns*.md` or `governance/panel/findings.json`; or a
panel record carried inside `governance/chart-review.md`, detected by a heading
containing "Reading panel (Rule 7.4)" and a later heading containing
"disposition". **Does not count:** pre-panel notes without a returned record,
or a chart review whose panel row reads "NOT RUN". Three of the six governed
modules carry the record inside the chart review, two of them because the
estate now files the panel's own record outside the module repository and
relays it in. Where that is the case the two Presentation cells share a path.

### `metric_register`

Every published measure has a written definition, an owner and lineage.
**Counts:** `governance/metric_register.md`. **Does not count:** a metrics
table in the page. Whether the register is generated from the models or typed
is not in the cell; it is here: Control Tower's is generated from `meta` blocks
in its dbt model file and checked for drift on every build; Matter Ledger's,
Fee Examiner's and Revenue Assurance's are typed, and their build scripts cite
the register rather than write it.

## Operation

### `scheduled_run_with_health`

A scheduled process runs the pipeline and publishes its own health and run
history. **Counts:** `governance/health.json`, with `governance/run_history.jsonl`
beside it; or `governance/last_live_run.json`. **Does not count:** a one-off
pull, or a scheduled task whose record lives only in the task store.

### `reconciliation_published`

A reconciliation is committed as a document that would show a failure if there
were one: the comparison, the variance, and every row that did not tie.
**Counts:** `governance/reconciliation.md`. **Does not count:** a reconciliation
step that only logs, or one that is asserted in prose without the rows. The
three modules that carry it reconcile three different things: a live increment
against a frozen baseline including runs that stopped or failed; two exhibits
of one fee application against each other with the non-comparable ones
labelled; and invoice lines against their constituent months, published even
where every difference is zero.

---

## Named checks

Cells that point at one check inside a validation script. The script verifies
the check's label is still present in the file.

| Row | Surface | File | Check, by its own label |
|---|---|---|---|
| `cascadia-dealdesk-analytics` | `row_count_validation` | `src/validate.py` | "conformed rows {total} != raw quote lines {raw}", inside check 1 |
| `cascadia-controltower-analytics` | `row_count_validation` | `validate.py` | "Database content hash matches the recorded run", check 11, which hashes `COUNT(*)` per fact table against `governance/generator_run.json` |
| `cascadia-revenue-assurance` | `row_count_validation` | `src/validate.py` | "the engine refused exactly the transactions the generator intended, by reason", check 6, counts against the raw manifest |

## Refinements made against disk in Part 1

Recorded so the next session knows which clauses were written after reading
the nine repositories rather than before.

1. `one_command_rebuild`: the documented-order form is detected by three
   phrases, listed above, because the six Python modules state their order in
   three different ways and none ships a run script.
2. `frozen_source`: a committed synthetic snapshot with a dated manifest
   counts. Deal Desk has no `freeze.toml` and a committed, dated `data/raw/`.
3. `source_register`: the hash requirement is what separates Control Tower's
   raw manifest (hashes) from Finance's (bytes and URLs).
4. `row_count_validation`: the Python form is a named check, not a pattern,
   because a content pattern that matched the three real checks and not the
   hash and reproducibility checks beside them would be a classifier fitted to
   nine repositories and presented as a rule.
5. `independent_rederivation`: the rules-document clause became one of two
   acceptable ways of being separately written, because Fee Examiner's second
   path is separate by construction rather than by a rules document and is a
   second path in every other respect.
6. `negative_controls`: the evidence is the published proof section, not the
   suite, so the cell points at the validation report and shares a path with
   `validation_report`. The outcome word is "tripped" or "rejected" because
   the two modules that carry it chose one each.
7. `reading_panel`: a record carried inside `chart-review.md` counts, with the
   heading and disposition markers above. Finance, Fee Examiner and Revenue
   Assurance carry theirs that way.
8. `reconciliation_published`: "including failures" rather than "including
   failed runs", because the spec's wording is the durable one and only Matter
   Ledger's reconciliation is about runs.
