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
