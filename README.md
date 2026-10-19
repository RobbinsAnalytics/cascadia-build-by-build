## Current portfolio extension (2026-10-19)

The eleven-build publication uses the pinned additive inventory. The original ten-build freeze remains unchanged. Build the current page with:

```text
python src/extend_inventory.py
python src/extend_inventory.py --check
python src/build_expanded_page.py
python src/validate_extension.py
```

See governance/portfolio-extension-decision.md for scope, provenance and the distinction between artifacts and completed requirements. Commands below describe the historical baseline; do not run the original page renderer over the current approved page.

---

# Cascadia Build by Build

The Cascadia portfolio proves nine modules, each testable on its own. What it
does not show is that the test surface widened build by build, and a reader
arriving cold has had to derive that from nine separate pages. This module
renders the progression directly: which tests each build could carry, when each
surface first appeared, and what every filled cell links to on disk. It has no
data of its own. Its source is the other nine module repositories, all of
them read-only, and nothing here invents a score.

**Status: Part 2b. Page built, panelled, dispositioned and published from `main:/docs`. Part 3, surfacing on the site, is next.**

## Repository and folder names match

Local `cascadia-build-by-build`, remote `cascadia-build-by-build`, under the
estate's one-name convention. The older modules keep their `-analytics` local
suffix and are not renamed.
