# Chart review: Cascadia Build by Build, the Part 2 page

*Owner: Aaron Robbins. Opened 2026-09-16 by the build session. Companion to
`VIZ-PRINCIPLES.md` v2.8 and `CHART-REVIEW.md` v2.8 in `cascadia-standards`.
One chart: the test-surface matrix, an HTML table. Data as read on
2026-09-16, frozen at `d967ff5`.*

```
CASCADIA CHART REVIEW v2.8 — docs/index.html (one chart, #matrix) — 2026-09-16
Class: detailed                    Quadrant: explanatory
Relationship: change over time (test surfaces accumulate across nine builds
              ordered by first commit; the rows are the time axis)
States reached: default only; the page has no reader controls, so the default
              state is the only state (Rule 6.11 N/A)
Widths reached (K6): 320 · 741 · 742 · 1040 — derived by src/render_charts.py
              from window.CASCADIA_BREAKPOINTS = [700]; the matrix host
              crosses 700 between viewports 741 and 742
              (docs/renders/k6-ladder.json). 320 is the narrowest supported
              width; 1040 the design width.
Once per publish (K7, K8): K7 PASS — every asset URL carries a content hash
              (cascadia.css?v=fc83ff023c, page.js?v=1af15cc9cc,
              favicon.svg?v=9f2fe5d980; no ECharts, no theme script ships).
              K8 PASS on presence — og:title, og:description, og:image,
              og:url, twitter:card, twitter:image, favicon linked; the
              og:image URL is absolute and names a thumbnail the site-side
              session has not yet produced (see Owed).
Reading panel (7.4): NOT RUN — renders handed to the Estate project; fatal
              under 7.1 until the record returns and is dispositioned here.
```

## 0 · Layer 0, the brief (Rules 0.1 to 0.3)

| | |
|---|---|
| **Whose decision** | A hiring manager or interviewer with ninety seconds, arriving cold from the homepage, deciding whether the portfolio's testing discipline is real and grew build by build before opening one module. Secondarily Aaron, in an interview, choosing which module's row to open. |
| **Horizon** | Tactical: one conversation. Not operational; nothing on the page is refreshed by a schedule. |
| **Literacy** | Reads a table and follows a link. May not know the vocabulary of the fourteen surfaces, which is why the key under the table carries every name and the row label carries the stack in plain words. |
| **Benchmark** | The row above: each build against the one before it, and build one against build nine. |
| **Cadence** | Refreshed when a build lands, by re-running `src/inventory.py` and committing the diff as a deliberate refreeze. Never a side effect. |
| **Available action** | Open a module's case study from its row label, or open the file a cell names. Every filled cell is a link. |
| **0.2 Quadrant** | Explanatory. The finding is the title's; the reader is not asked to find one. |
| **0.3 Class** | Detailed. Read for values (which cell is filled), not for shape alone. |

**Why a table and not a canvas (0.3, and decision D5).** The matrix is
categorical presence, not quantity: a cell is a path or it is empty. A table
is its own Rule 5.1 data layer, every cell can be a real link (a canvas cell
cannot), row and column headers are read by assistive technology without a
sibling DOM layer, and no axis exists to mis-scale. ECharts does not ship on
this page; the review notes it here under 0.3 as the brief asked.

## 1 · Checklist A, the matrix

Built by `src/build_page.py` (every figure and every string) and
`docs/assets/page.js` (geometry only), rendered by `src/render_charts.py` at
the four widths above. Renders are in `docs/renders/`: `matrix-<w>.png` and
`page-<w>.png`.

| Check | The matrix |
|---|---|
| 0.1 / 0.2 / 0.3 | named above; explanatory; detailed |
| 1.1 relationship matches title | change over time: "at build one" and "by build nine" are two positions on the row axis, and the title claims what accumulated between them |
| 1.2 encoding | presence by position in a grid; nothing quantitative is carried on a lower-ranked channel |
| 1.3 aspect banked | N/A: no line |
| 1.4 causal disclaimer | N/A |
| 2.1 baseline matches claim | N/A: no value axis; the title's two numbers are counts of marks |
| K1 axis extent, bounds derived | N/A: no axis. The two numbers in the title are asserted against the data by `check_title()` in `build_page.py`, and the build fails if either is false |
| 2.2 single value axis | PASS (none) |
| 2.3.1 slots fixed | two mark kinds, fixed for the page: a Slate moss square for "carries", an Evergreen diamond for "first to carry"; a Glacier tick for a standard version in the lane. The key repeats all three under the table |
| 2.3.2 sentiment not by colour alone | N/A (no sentiment). The first-appearance distinction is carried by shape (diamond against square) and by each link's accessible name, not by hue alone |
| 2.3.3 / 2.3.4 mark size | 12 px squares, 15 px diamonds (14 px below the breakpoint), 8 px lane ticks: solid fills validated at block size; the 8 px tick sits between the point and block classes and carries a text label beside it, so nothing rests on its hue |
| 2.3.5 at most four categories | three (square, diamond, lane tick) |
| 2.3.6 data geometry at or above 3:1 | PASS: Slate moss 5.82:1, Evergreen 5.18:1, Glacier 3.55:1 on Paper; no Rain |
| 2.4 gridlines | the table's 1 px Mist row rules are structure, not gridlines; no vertical rules except the two that separate the sticky label columns from the cells. Recorded as PASS with that reading |
| 2.5 no decoration | PASS: flat fills, no shadow, no gradient, no icon in the plot |
| 2.6 part-to-whole | N/A |
| 2.7 sort | rows in first-commit order and columns in the spec's band order, both inherently ordered: PASS (exception) |
| 2.8 horizontal text | PASS: header names break at declared soft hyphens; nothing rotates at any width |
| 2.9 rounded to the decision | counts only; dates ISO in the lane per house style |
| 3.1 finding title at top | PASS: an `<h3>` above the table, the table `aria-labelledby` it. Not a `<caption>`: made `display: block` and sticky inside the scroll wrapper, a caption collapsed to the first column's width and rendered below the header (§2, #1); left as `table-caption` it scrolls away with the table, which Rule 5.1's own narrow-table clause warns of |
| 3.2 title readable from the plot | "two ways at build one": two diamonds in row one. "fourteen by build nine": fourteen diamonds in the table, the last in row nine. Both are counted from marks, and the subtitle says to count the diamonds. No computed-aggregate exception is needed; the description carries the counts as well |
| 3.3 focus treatment | the diamonds are the saturated series (Evergreen) and are the series the title talks about; the squares are context in Slate moss, above 3:1 and named by the key, not Rain; the primary annotation is in Evergreen ink, matched to the diamonds |
| 3.4 annotation at the mark, one dominant | primary under row nine, the mark the second number depends on, 12 words; secondary under row four where the most surfaces appear at once, 11 words, smaller and in secondary ink. Linkage is adjacency (each in its own row directly beneath its mark) plus colour. Both figures in the annotations are computed and asserted in `build_page.py` |
| K3 no annotation over a mark | PASS at all four widths: each annotation is its own row; nothing is drawn over a cell |
| 3.5 arrangement | rows adjacent in build order and grouped by era; columns grouped by band; the comparison the title affords (row one against the whole column of diamonds) is a vertical scan down one table |
| 3.6 direct labels | every column carries its name in the header at and above the breakpoint and its number below it, with the number-to-name mapping declared in the key at every width (Rule 5.5's declared abbreviation, not a legend that replaces a label); every row carries its name, stack and month; every mark carries an accessible name naming surface, path, repository and first-ness. The key's mark meanings (square, diamond, tick) cannot be written in each cell and are the one legend on the page |
| 4.1 holes | an empty cell is an empty cell, declared in the subtitle, the key and the description; nothing is zero-filled; the three undated standard versions are listed as undated in the lane's first row, not placed |
| 4.2 strip | bottom-left of the card, Evergreen tick, three segments, 12 px Slate moss: source, read date with the freeze and the standard's commit, flags |
| K5 rendered segment count | 3 at all four widths (`render_charts.py` counts the render) |
| 4.3 travels alone | the subtitle carries how to check the title; the key carries every meaning; the strip carries the as-of, the freeze and the undated note. A screenshot of the card is complete |
| 4.5 uncertainty | N/A: every cell is a file that exists or does not |
| 5.1 access layers | summary first in the DOM (rendered under the table); the chart is the table, so layer 2 is the chart itself; layer 3: native table semantics with row and column headers, and every mark a focusable link whose name states surface, path, repository and first-ness. The finding is the accumulation of diamonds down the rows, which the description states as an L3 shape clause. Narrow treatment: the table scrolls inside a focusable wrapper with sticky row-label columns and scroll shadows; the title is outside the wrapper; no stacking, so no ARIA roles are needed |
| 5.2 description L1 to L3, never L4 | type, encodings and bands (L1); surfaces per build, first appearances per build, running count, the lane's extremes and the undated versions (L2); where the marks thicken and the diamonds step (L3). No cause or implication |
| K2 every figure traces to a build step | every figure in the title, subtitle, annotations, description, lane and row labels is computed in `build_page.py` from `data/builds.json` and `data/standard.json` (`facts()`, `description()`, `lane_positions()`, `check_title()`); prose in `page_text.py` carries no typed figure, only tokens the builder fills and verifies |
| 5.3 WCAG AA | 12 px minimum text everywhere on the card (the strip at 12 px, above Rule 4.2's 10 to 11 px, because 5.3's floor is stated as anywhere); reflow at 320 asserted by `render_charts.py` (the document never scrolls sideways; the table scrolls inside its wrapper, which is 1.4.10's data-table allowance and 5.1's named treatment); focus ring 2 px Evergreen on every link; every cell link at least 24 by 28 px; `color-scheme: light` |
| 5.4 monochrome | square against diamond survives grayscale; the lane tick carries its label |
| 5.5 responsive | form constant: a table at every width. Below the host breakpoint the surface names collapse to their numbers and the band names to their letters, both by the mapping printed in the key; nothing is deleted; nothing rotates; the marks do not shrink below 12 px |
| K4 tick interval derived | N/A: no axis ticks |
| 5.6 reduced motion | no animation or transition exists; a reduced-motion rule zeroes any the browser might add |
| 5.7 dark mode | `color-scheme: light` declared in the stylesheet; no dark palette exists (D6) |
| 6.7 one strip | one chart, one strip, under the card; the page carries no second strip. The "About this page" block at the page end names the freeze in prose and is not a strip |
| 7.1 / 7.4 panel | **NOT RUN**: fatal under 7.1 until it is; recorded, not claimed |
| 7.2 AI output cleared | the page was model-built; this checklist was run in full by the build session, which is the author and cannot be the panel |
| K6 widths | 320 · 741 · 742 · 1040, recorded above |

**Preference score, as the author reads it: 0.** No PREFERENCE check is
failed on the author's own reading.

**Invariant status: one open**, 7.1/7.4, because no panel has run. **The page
does not ship until it has.** Everything else is PASS, PASS-BY-EXCEPTION or
N/A as recorded.

## 2 · Findings from this build session's own review, before any panel

Found on the renders and fixed before this file was written. None of these
is a pre-panel note; the notes are what the author still suspects.

1. The finding title, placed in a `<caption>` made `display: block` and
   sticky so it would not scroll away, collapsed to the first column's width
   and rendered between the header and the body. Fixed by moving the title
   and subtitle to an `<h3>` and a paragraph above the scroll wrapper, with
   `aria-labelledby` and `aria-describedby` on the table.
2. At the design width the table was 978 px in a 974 px wrapper and scrolled
   by four pixels. Fixed by narrowing the build column and the era column.
3. At 320 the era column clipped "Enterprise". Fixed with display-only soft
   hyphens in the era labels and a wider narrow era column.
4. At 320 the annotation and lane rows scrolled off with the table. Fixed by
   a sticky inner block sized to the wrapper, so a spanning row's text stays
   in view while the cells scroll.
5. Two header names broke mid-word ("One-comma nd", "penden t"). Fixed with
   soft hyphens and `overflow-wrap: normal`.
6. The row label's month wrapped between "Jun" and "2026". Fixed with a
   no-wrap span.
7. The strip, the lane rows and the row ordinals were set at 11 to 11.5 px.
   Raised to 12 px, Rule 5.3's floor.

## 3 · Decisions the review records

- **The standard's lane is a set of thin rows between the builds**, each at
  the row boundary its date falls in, with the three undated versions listed
  in one row at the top. The brief described a strip under the last row with
  markers at row boundaries, which a horizontal strip cannot have; rows are
  the table's only time axis, so the markers sit between them. The brief also
  placed v2.3, v2.4 and v2.5 (2026-08-10) between Deal Desk and Control
  Tower; Control Tower's first commit is 2026-08-08, so they sit between
  Control Tower and Matter Ledger, with v2.6 and v2.7.
- **One provenance strip.** The matrix carries it; the page does not get a
  second (Rule 6.7 as the brief reads it). The closing block names the
  freeze in prose.
- **The as-of date is the read date**, 2026-09-16, not the build date. The
  page carries no build timestamp so a rebuild against unchanged data is
  byte-identical, which is what the freeze wants to be able to say.

## Owed

- The reading panel, run from the Estate project on `docs/renders/`, at 320
  and 1040 at least; its record and disposition enter §4 of this file.
- The two `[AARON]` lines in `src/page_text.py`, rewritten by Aaron before
  publish.
- The thumbnail `og:image` names, produced by the site-side session.
- Publishing and Pages: Part 2b.

## Verdict

**DO NOT SHIP** until the panel returns. No other invariant is open.
