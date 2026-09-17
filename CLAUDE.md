# Cascadia Build by Build: what an agent needs to know

The Cascadia portfolio's test surface, build by build: one page showing which
tests each module could carry and when each surface first appeared. It
publishes to `https://www.robbinsanalytics.com/cascadia-build-by-build/`.
Remote is `RobbinsAnalytics/cascadia-build-by-build`.

**The estate's session rules, the surfaces, the guards, and the traps that have
each cost a session, are at
`C:\Projects\cascadia-standards\governance\SESSION-RULES.md`.** Read §1 to §7
and stop at the line. What gets published is governed by `PRINCIPLES.md` in the
same directory. This file carries only what is true of this repo.

## This module has no data of its own

**Its source is the other nine module repositories, read-only.** That is the
one way it differs from every predecessor, and it is the constraint that
governs everything under `src/`.

- **Never write in a sibling repository.** Not a file, not a config value.
- **Never commit in one.** A commit made from a session rooted here is
  unguarded by that repo's hooks, which load only from the primary working
  directory.
- **Never run `git status` in a sibling from a bash sandbox.** It takes
  `.git/index.lock` and can leave it behind, and a stale lock blocks every
  commit in that repo until someone deletes it. This build's predecessors left
  one in `cascadia-revenue-assurance` and found an older one in
  `cascadia-estate`. `git status` will not reveal a stale lock;
  `git update-index --refresh` will. Delete it and retry. Read a sibling with
  plumbing that does not take the lock, or with `git -C <path> log`, and prefer
  reads that do not touch the index at all.

## Parts, and which session runs which

**Part 0 is this repository and its guard layer, and it is done.** No code, no
data, no page. **Part 1 is a separate brief in a fresh session rooted here**,
where the guard is live rather than merely present; it writes
`src/inventory.py`, `data/builds.json` and `data/standard.json` and stops at
the numbers. Part 2 writes the page. Do not anticipate either here.
`governance/spec.md` is the durable statement of all three.

**This repo's own first commit was made from a session rooted at
`C:\Projects`, deliberately.** Creating the repo and installing the guard layer
is Part 0 of this build, and hooks load only from the primary working
directory, so that session was never governed by the hooks it was installing.

## Naming follows REMOTE-CONVENTION.md

Local directory and GitHub repository are both `cascadia-build-by-build`, the
one-name rule. No `-analytics` suffix.

## The freeze: `governance/freeze.toml` protects `data/*`

**`as_of_date` in `governance/freeze.toml` is a claim made out loud.** It is
the date the inventory was read from the nine sibling repositories, and the
page will say it. Advancing it is a deliberate act, never a side effect.

**`src/inventory.py` overwrites the freeze.** Run it only to deliberately
refresh the inventory, then commit the diff as a refreeze and move `baseline`
to the new commit. Against an unchanged estate it is byte-identical, which is
what `validate.py` checks; against a changed estate the diff is the change.

**Build order:** `python src/inventory.py`, then the gates:
`python src/validate.py`, `python src/validate_freeze.py`,
`python .claude/hooks/hook_test_matrix.py`. All exit zero or nothing is done.

**Generated, not authored.** `data/builds.json` and `data/standard.json` are
build outputs. Hand-editing either is the failure mode the rest of this estate
has already paid for; regenerate instead. The column definitions in
`governance/surfaces.md` and the constants at the top of `src/inventory.py`
are the authored layer.

**Know this about the template gate before trusting it: it cannot tell an
untracked file from an unchanged one.** `src/validate_freeze.py` is the estate
template verbatim (parking lot 8a). It compares with
`git diff --quiet <baseline> -- <path>`, and an untracked path produces no
diff, so a protected file that exists on disk but was never committed passes.
**A passing gate is therefore a claim about committed files only.** Check
`git status` in this repository too. The template carries this defect
estate-wide until a `cascadia-standards` session fixes it.

## Stage 2: the page, built from the two data files only

`docs/index.html` is built by `src/build_page.py` from `data/builds.json` and
`data/standard.json`, plus the as-of date and freeze commit in
`governance/freeze.toml`. Every figure on the page is computed there; the
prose is in `src/page_text.py` as plain strings with tokens the builder fills
and verifies, and it is the only authored text on the page. Two lines there
are marked `[AARON]` and ship in his words, not the session's.

**Rebuild order:** `python src/inventory.py` (only to deliberately refresh the
freeze), then `python src/build_page.py`, then `python src/render_charts.py`.
The renderer derives the K6 ladder from `window.CASCADIA_BREAKPOINTS` in
`docs/assets/page.js` and fails closed if none is declared.

**Generated, never edited:** `docs/index.html` and everything under
`docs/renders/`. The stylesheet is Revenue Assurance's, copied with a line
saying so; the favicon is the site's. No ECharts ships: the one chart is an
HTML table, and the chart review says why under 0.3.

**Not yet published.** The page ships only after the reading panel's record is
dispositioned in `governance/chart-review.md`. Enabling Pages and publishing
is Part 2b.

## Committing

**Stage by name, never the two blanket forms.** They are denied in
`.claude/settings.json`, and that block does **not** bind under
`bypassPermissions`. What binds is
`.claude/hooks/no_blanket_add_or_force_push.py`, a `PreToolUse` hook.

**Line-ending churn will not be cosmetic once data exists**, it would make "the
inventory is unchanged" unassertable. `.gitattributes` prevents it and landed
in the root commit; the git `pre-commit` gate in `.githooks/` catches what gets
through and fails closed. **It is inert until `git config core.hooksPath
.githooks` has been run in this clone**, and on POSIX it is also inert unless
`.githooks/pre-commit` is tracked `100755`. Both were done at initialisation;
confirm with `git ls-files -s .githooks/pre-commit`. Run
`python .claude/hooks/hook_test_matrix.py` to confirm the guards behave. Note
that the matrix cannot check the mode on Windows, where `core.fileMode` is
false: the index listing is the check, and it is a check of state, not
behaviour.

**This repo has no entry in
`cascadia-standards/governance/hook_manifest.json` yet.** That entry is
authored from a session rooted in `cascadia-standards`, never from here, and
`check_hook_drift.py` exits 3 estate-wide until it lands. Fee Examiner and
Revenue Assurance each went through the same gap; it is not a defect.
