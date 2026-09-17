# Chart review: Cascadia Build by Build, the Part 2 page

*Owner: Aaron Robbins. Opened 2026-09-16 by the build session. Companion to
`VIZ-PRINCIPLES.md` v2.8 and `CHART-REVIEW.md` v2.8 in `cascadia-standards`.
One chart: the test-surface matrix, an HTML table. Data as read on
2026-09-16, frozen at `d967ff5`.*

```
CASCADIA CHART REVIEW v2.8: docs/index.html (one chart, #matrix): 2026-09-16
Class: detailed                    Quadrant: explanatory
Relationship: change over time (test surfaces accumulate across nine builds
              ordered by first commit; the rows are the time axis)
States reached: default only; the page has no reader controls, so the default
              state is the only state (Rule 6.11 N/A)
Widths reached (K6): 320 · 741 · 742 · 1040: derived by src/render_charts.py
              from window.CASCADIA_BREAKPOINTS = [700]; the matrix host
              crosses 700 between viewports 741 and 742
              (docs/renders/k6-ladder.json). 320 is the narrowest supported
              width; 1040 the design width.
Once per publish (K7, K8): K7 PASS: every asset URL carries a content hash
              (cascadia.css?v=fc83ff023c, page.js?v=1af15cc9cc,
              favicon.svg?v=9f2fe5d980; no ECharts, no theme script ships).
              K8 PASS on presence: og:title, og:description, og:image,
              og:url, twitter:card, twitter:image, favicon linked; the
              og:image URL is absolute and names a thumbnail the site-side
              session has not yet produced (see Owed).
Reading panel (7.4): NOT RUN: renders handed to the Estate project; fatal
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

## 4 · Reading panel (Rule 7.4): RUN 2026-09-17, Cowork side

*The Estate project's record, committed as found on 2026-09-17 from the handoff copy; the estate's own copy is `cascadia-estate/panels/2026-09-17_Panel_build-by-build-matrix.md`. The record's headings are nested one level under this section. Em dashes inside the seats' quotations are theirs. The `Disposition` and `Novel?` columns are filled in §5 below, not in the record.*

## Reading panel — Cascadia Build by Build — matrix — 2026-09-17

Run from the Cascadia Estate Cowork project per `ESTATE-STATE.md` §3, against
the `cascadia-reading-panel` skill.

**`cascadia-standards` `HEAD` at run time: `build/retrospective-skill`
`5cd0ac54f8ac8965a9b8d36f2a58d10506bf0ec1`.** Read from `.git/HEAD` and the
branch ref directly, not by running git, per this project's Instructions.

> **This is not `main`, and the project's own Instructions name that as a trap.**
> *"An unmerged branch checked out at the wrong moment is the way this project
> quotes a rule that does not exist yet."* `ESTATE-STATE.md` §5 records this
> branch as committed, unmerged and not installed. **No rule text was quoted to
> any seat, and no rule text was consulted to produce the returns**, so the
> exposure here is confined to the `Rule` column of the disposition table below,
> which is this session's indication of where a finding is likely to land and not
> a citation. Treat that column as unverified against the Live standard until a
> session reading `main` confirms it.

### Source of the renders

`C:\Projects\cascadia-build-by-build\docs\renders`, mounted directly to this
session on 2026-09-17. Four PNGs panelled:

| Panelled as | File | Nominal width | Rendered px |
|---|---|---|---|
| Screen A | `matrix-320.png` | 320, narrowest | 560 × 4910 |
| Screen B | `matrix-741.png` | 741, below the host crossing | (K6 below) |
| Screen C | `matrix-742.png` | 742, above it | 1404 × 2764 |
| Screen D | `matrix-1040.png` | 1040, design width | 2000 × 2612 |

`k6-ladder.json` accompanied them and declares one breakpoint at 700, one chart,
and the crossing at host width 699/700 between the 741 and 742 viewports.

**Branch not verified.** The renders are stated to come from branch
`build/part2-page`. Only `docs\renders` was mounted, by Aaron's decision this
session, so this session cannot read that repository's `HEAD`. **The single check
that would settle it:** a session with the repository root reads `.git/HEAD`
there and confirms the branch and the commit the renders were produced at. The
claim is carried as asserted by the requester.

**Why only that folder was mounted.** Mounting the repository root would have put
the build's brief and its pre-panel notes inside the moderator's reach. Narrowing
the mount makes moderator-side blindness structural rather than a matter of
this session's restraint. It costs the branch verification above, and that trade
was Aaron's call, recorded here so the cost is visible rather than absorbed.

**`page-320.png`, `page-741.png`, `page-742.png` and `page-1040.png` were present
in that folder and were not panelled.** They are full-page renders and would have
carried the surrounding prose, which is the intended finding arriving from
outside the chart. They were excluded from the staging folder rather than
excluded by instruction, so no seat could have reached them.

### Pre-panel notes: not obtained. `N = not measured`

The build session's pre-panel notes exist and were deliberately withheld from
this session, by Aaron's decision this session, so that nothing about them could
steer the casting or the seats. Per the skill, a missing number is recorded
rather than reconstructed after the fact. **This run therefore contributes `D`
to Rule 7.4's retirement trigger and cannot contribute `N`.**

If the build author wants `N`, the `Novel?` column in the disposition table is
left blank for them to fill against notes they wrote before the panel ran.

### Staging: what the seats were given, and what was stripped

The four files were copied to a neutral folder and renamed `screen-a` through
`screen-d`. **The filenames were the leak being closed:** `matrix-741.png` and
`matrix-742.png` name the crossing in the filename, and a seat reading those
names learns where to look before it looks. Pixel widths were withheld for the
same reason. Seats were told only that A is a narrow phone, B and C are two
laptops, and D is a wide desktop, which is what a reader knows about their own
device.

**One adaptation to the skill's seat prompt, recorded because it is an
adaptation.** The prompt is written for *N* charts; this is one chart in four
states. Seats were told the four images are one graphic on four screens. Without
that they would have reported four unrelated charts and the returns would not
pool. The alternative, withholding it, was rejected because it manufactures a
confusion no reader has.

---

### Transport certification — measured, not asserted

**`blind: not certified`.** Contamination was measured directly this session,
before the returns were pooled, by a probe subagent given no task content and
asked only to report what its runtime had already placed in front of it.

The probe returned, before any prompt of mine:

- **Both connected `CLAUDE.md` files, in body text and not merely by name.**
  Among what it quoted: *"Where a companion document and VIZ-PRINCIPLES.md
  disagree, VIZ-PRINCIPLES wins and the companion is the defect"*, the Control
  Tower company allow-list in full, and *"A session commissioned to review writes
  one findings file and stops."*
- The `cascadia-reading-panel` skill description verbatim, including the phrase
  *"a blind, multi-seat adversarial read of charts before they ship"* and the
  words *"the roster, disposition and D/N/R metric blocks that CHART-REVIEW.md
  expects."*
- The full skills list, the deferred-tools list, `userEmail`, platform and OS.
- **`C:\Projects\cascadia-build-by-build\docs\renders`.**

#### Two corrections this measurement makes to parking lot §3a

**1. The extent claim is understated.** §3a records that *"Filenames and one-line
descriptions travel; rule content does not."* This probe shows `CLAUDE.md` **body
text** travels, including governance rules stated as rules. That is more than
filenames and more than one-line descriptions. What still appears not to travel
is `VIZ-PRINCIPLES.md` and `CHART-REVIEW.md` content, which is the distinction
§3a was reaching for, but the sentence as written is wrong and should be
narrowed to name the chart rules rather than rule content generally.

**2. A new vector, and this session created it.** The artifact's own repository
path reached the probe because this session mounted that folder. **Every seat
therefore knew the artifact was called `build-by-build` before it saw a
picture.** The two leaks §3a records, the skill description and the `CLAUDE.md`
files, are properties of the surface. This one is a property of *the moderator's
own setup action*, and it is the first of that class recorded. A mount made to
fetch images is not obviously a blindness decision, which is exactly why it got
made without one.

**How much it matters here: modestly.** "Build by build" telegraphs progression
across builds, which the chart's own title states anyway. It is recorded because
the class is new, not because this instance was costly.

**Both belong on the parking lot at §3a.** Filing them is a separate act and is
not done by this record.

---

### 1 · Roster

```
READING PANEL — Cascadia Build by Build, matrix — 2026-09-17
Decision served (Rule 0.1): read off the canvas, no brief available.
  Whether nine builds' accumulated verification practice is real and durable
  enough to be trusted, decided by someone assessing this body of work with
  the builder in the room.
Charts panelled: 1     States: 4 (320 / 741 / 742 / 1040), default state each
Nature: simulated

  Seat 1  Hiring manager, ~20-person data and analytics group at a mid-sized
          insurer, 8 years in seat — simulated — why this seat: owns the
          advance-or-decline decision the artifact is built to inform. Will
          ask whether the staircase is a habit or a story told afterward.

  Seat 2  Staff data engineer, logistics, 12 years, inherits other people's
          pipelines — simulated — why this seat: the fourteen surfaces are his
          own craft, so he is the reader who can tell a real artifact from a
          checkbox, and the one who asks what happens when the source changes
          shape.

  Seat 3  Director of delivery, healthcare services, 15 years, came up through
          project management and does not read code — simulated — why this
          seat: the literacy floor, and the orthogonal concern. Cares only
          whether the practice survives its inventor leaving, and whether he
          can repeat what he was shown without being caught out.

  Seat 4  Visualization reader — simulated — canvas only; tables and the
          descriptive paragraph excluded.

Blindness asserted: design system ☑ · review and build notes ☑ · source data ☑ ·
                    intended finding from outside the artifact ☑ ·
                    other seats' output ☑
Blindness certified: ☐  — see transport section. Measured contaminated.
Run: parallel ☑  (all four spawned in one message)
Author's pre-panel notes recorded: ☐  → N = not measured
```

**The roster test, run honestly.** Could this be pasted unchanged onto a pricing
page or a plant dashboard? No. All three domain seats are cast to a claim about
engineering practice maturity and would read as nonsense against a margin plot.
Seat 3 is the non-analyst the casting guidance requires, and is the seat whose
concern, survivability after the inventor leaves, no other seat holds.

**Casting was done from the canvas, not from a brief**, which is the images-only
condition working as designed and is also its one cost: Rule 0.1's answer was
inferred from what the artifact declares about itself rather than read from the
document that should hold it. A different reading of whose decision this serves
would produce a different roster and possibly different findings.

---

### 2 · Returns

Verbatim. **Em dashes appear inside quotations because the seats wrote them**;
the house rule against them governs this record's own prose, not evidence.

#### Seat 1 · Hiring manager

**Screen A**
```
SENTENCE  "Somebody's tracking nine of their own projects against a fourteen-item
          quality checklist, and on my phone I could see the checklist existed but
          not most of it, because the table runs off the right edge of the screen."
          → carries the title's claim? no
NUMBER    "Fourteen — but I got it from the headline ... and from the block of prose
          at the very bottom ... I could not get it off the grid."
          — located at: title and descriptive paragraph. NOT off the plot.
QUESTION  "What's off the right-hand side, and did you know it was gone?"
GAP       "A period. ... nothing tells me up front what stretch of time this covers
          or how fast that's supposed to be."
```

**Screen B**
```
SENTENCE  "Same thing, now I can see the whole grid: the marks get denser as you go
          down the rows, so whatever they're measuring, they were doing two of
          fourteen things at the start and nearly all of them by the end."
          → carries the title's claim? yes
NUMBER    "Build one, Cascadia Medical Devices, has exactly two marks in the row —
          both diamonds, in columns 1 and 4."
          — located at: marks in row 1. Off the plot.
QUESTION  "Why is the key not on the columns? I read this whole thing with my eyes
          bouncing up and down."
GAP       "Anything from outside this person's own head. ... nothing says who sat on
          them."
```

**Screen C**
```
SENTENCE  "This one confused me — the title says fourteen and the table stops at eight."
          → carries the title's claim? no
NUMBER    "Eight. The last column heading on the grid is '8 Golden fixture,' and the
          rule line above the headings ends there too."
          — located at: column header. Off the plot, and contradicts the title.
QUESTION  "Is columns nine through fourteen missing on purpose, or is my screen eating
          them? First read, I genuinely don't know which, and I'm not going to guess
          on your behalf."
GAP       "The rest of the table."
```

**Screen D**
```
SENTENCE  "This is the one that works: a nine-by-fourteen grid of engineering discipline
          over about four months, and the pattern is real."
          → carries the title's claim? yes
NUMBER    "Build four, Cascadia Finance, row four: one square and five diamonds in that
          row, and a little note directly under it saying 'Build four, the first Python
          build: five surfaces appear at once.'"
          — located at: marks in row 4 plus the row annotation. Off the plot.
QUESTION  "Who graded this? ... If that holds up under one click, I believe the rest of
          the grid. If it doesn't, the grid is a résumé with squares in it."
GAP       "Anything that went wrong. ... Real improvement has a row where it went
          backwards."
```

**Unprompted, across all four:** *"the same graphic told me eight, fourteen, and
'can't tell' depending on which screen I was sitting at ... their own artifact
fails its own instruction on a phone."*

#### Seat 2 · Staff data engineer

**Screen A**
```
SENTENCE  "Somebody's tracking nine of our builds against a checklist of testing/QA
          things ... but on my phone I could only see the first four or five columns,
          so I mostly read the paragraph at the bottom rather than the chart."
          → carries the title's claim? no
NUMBER    "Fourteen, and I got it out of the block of text underneath, not off the grid"
          — located at: descriptive paragraph. NOT off the plot.
QUESTION  "Is this cut off, or am I meant to scroll sideways?"
GAP       "Column names. ... Also, a total per row — the thing I actually want is
          'this build: 10 of 14,' and I ended up reconstructing it from prose."
```

**Screen B**
```
SENTENCE  "It's a coverage grid — nine builds down, fourteen test/QA practices across,
          oldest at top — and the short version is the marks pile up as you go down."
          → carries the title's claim? yes
NUMBER    "Build four, the Cascadia Finance row: six marks, five of them diamonds ...
          it's the only number here I could verify by eye in about four seconds."
          — located at: marks in row 4. Off the plot.
QUESTION  "What does 'fourteen by build nine' mean — does build nine have fourteen of
          these, or is fourteen the total across all nine builds ... ? I read the title
          the first way, then counted build nine's row and got ten"
GAP       "nothing tells me how a build gets credited with a surface ... in a meeting on
          a projected image I can't click anything, so it stays a claim."
```

**Screen C**
```
SENTENCE  "Same grid, and this one's easier to read because the columns actually have
          names on them — but I only see eight of the fourteen, so it's the left half
          of the story."
          → carries the title's claim? no
NUMBER    "Column 8, 'Golden fixture' — the bottom row ... has the green diamond sitting
          in it. And that stopped me, because the green note right underneath says
          'Build nine: the golden fixture is the fourteenth surface,' and on this screen
          the golden fixture is plainly column 8."
          — located at: mark in row 9 against the column header and the annotation.
QUESTION  "On this screen, is the diamond in the bottom row in the column it belongs in?"
GAP       "The other six columns. ... those are the ones I'd actually care most about,
          the operational ones. The half I can see is the half I'd have assumed."
```

**Screen D**
```
SENTENCE  "Nine builds, fourteen verification practices, and you can see the practice
          spread over time."
          → carries the title's claim? yes
NUMBER    "Build nine, the bottom row: ten marks out of fourteen columns. I counted them
          across the row ... I'd say it that way rather than 'fourteen,' because
          fourteen is the cumulative total across every build and I think people will
          hear it as build nine's score."
          — located at: marks in row 9. Off the plot.
QUESTION  "What regenerates this? ... A grid like this is right the day it's made and
          quietly wrong six weeks later."
GAP       "an empty cell means 'this build doesn't have that' ... I'd want to know how a
          build was confirmed *not* to have a surface ... Two, nothing dates the marks."
```

#### Seat 3 · Director of delivery

**Screen A**
```
SENTENCE  "someone showed me a grid of nine projects against a checklist of quality
          steps ... but on my phone I could only see the first four columns, so I'm
          taking their word for most of it."
          → carries the title's claim? no
NUMBER    "The only number I could actually repeat is from the block of text at the very
          bottom, not from the picture."
          — located at: descriptive paragraph. NOT off the plot.
QUESTION  "The headline says fourteen. I can see four columns. Where are the other ten,
          and did I just miss a scroll bar?"
GAP       "A way to tell that I was only seeing part of it. ... That's the thing that
          would worry me — not that it was clipped, but that it was clipped silently."
```

**Screen B**
```
SENTENCE  "It's a nine-by-fourteen scorecard ... and the marks fill in as you go down,
          so the newer work is more thoroughly checked than the older work."
          → carries the title's claim? yes
NUMBER    "Build four, Cascadia Finance. Reading along its row I counted five green
          diamonds, and there's a little note tucked directly underneath the row"
          — located at: marks in row 4 plus annotation. Off the plot.
QUESTION  "What is column nine? ... In a meeting I'd have run out of patience before I
          did that for more than one column."
GAP       "Column names where the columns are. And I'll admit the row labels down the
          left were hard going ... Not a styling complaint, it genuinely slowed my
          reading."
```

**Screen C**
```
SENTENCE  "Nine projects scored against eight quality checks, getting more complete over
          time. And that sentence would be wrong, which is the problem."
          → carries the title's claim? no
NUMBER    "Build nine ... I counted six marks across it, the last one a diamond under
          'Golden fixture.' But the paragraph underneath the chart says '10 at build 9.'
          So I have a picture telling me six and a text telling me ten, and I sat there
          for a moment trying to work out which one I'd broken."
          — located at: marks in row 9, against the descriptive paragraph.
QUESTION  "Your title says fourteen surfaces and tells me to count the diamonds. Your
          table has eight columns. Which number is the real one?"
GAP       "Any sign that the table had been trimmed. The right-hand edge looks like a
          finished edge. ... I'd have repeated the wrong count to my own boss with
          confidence, and if you've ever been corrected in that situation you'll know
          why this is the screen I'd remember."
```

**Screen D**
```
SENTENCE  "They've got fourteen named ways of proving a number is right, and they can
          show you which of nine projects carries which."
          → carries the title's claim? yes
NUMBER    "Fourteen, and I got it by counting the green diamonds myself, which is what
          the title asked me to do. ... That's the first time across all four screens
          the picture proved its own headline to me, and I liked it."
          — located at: diamonds counted across the grid. Off the plot.
QUESTION  "What is a golden fixture, and what is a negative control? Also 'Are these nine
          clients?' ... if the person who built this left tomorrow, does the next person
          get these fourteen boxes ticked because there's a process, or because they
          happened to read this chart?"
GAP       "nowhere does it say what good looks like ... Build eight has a visible hole and
          I don't know whether that's a problem or a deliberate choice."
```

**Unprompted, across all four:** *"D is the only one I could repeat to my boss
without being caught out. B I could use with effort. A told me it was
incomplete. C told me nothing was wrong and was the one that would have got me
in trouble."*

#### Seat 4 · Visualization reader

**Cross-screen, before any screen-specific answer**
```
"The natural move is to look at the row labelled 9 ... That row has ten marks, not
fourteen. The fourteen is a cumulative total ... Nothing on the plot draws that
running total: no tally column, no cumulative line, no 'so far' figure anywhere in
the grid. The subtitle rescues it with an instruction ... but that is prose asking
the reader to do arithmetic, not a drawn quantity."

"'two ways to check a number' at build one resolves to the two diamonds in row 1 ...
Only the second is literally a way to check a number. That the first counts as one
is taken on faith."
```

**Screen A**
```
ABOUT     "a compliance or adoption checklist ... I genuinely could not tell what the
          columns were ... the title is about a count reaching fourteen, and the chart
          shows about four and a half of the fourteen columns."
TITLE     "'Fourteen' — not checkable. I count five diamonds on this screen ... The
          other nine are off the right edge." / "To A's credit, the truncation is
          honest: marks are visibly bisected at the right frame edge and the '5' in the
          header is cut mid-glyph, so a reader knows something is missing."
FORM      "at phone width the matrix can't be delivered at all."
HARD      "The era labels hyphenate brutally: 'Enter-prise-shaped', 'Frozen and
          vali-dated' ... so each row is a tall block and the row rhythm of the matrix
          is lost."
GRAY      "Survives, because the distinction is carried by shape (square vs diamond) as
          well as colour. That's a real design strength and I'd say so." ... "The blue
          design-standard chips and the grey carry-squares are the same shape, differing
          only by colour and by sitting in a band row."
NUMBER    "build one carries two surfaces, both first appearances — read off row 1 ...
          I cannot get the headline fourteen off this plot."
```

**Screen B**
```
ABOUT     "clearly an adoption/coverage matrix ... This is the only screen where I'd say
          the picture and the title tell the same story unaided."
TITLE     "I counted the diamonds: 2 + 1 + 5 + 3 + 2 + 1 = 14. It checks out."
FORM      "the title asserts a growth from 2 to 14 and the matrix makes you tally it.
          But B is the screen where the tally is actually performable."
HARD      "Every mark needs a two-step lookup ... Fourteen lookups to learn what the
          chart is about. That's fine for counting, useless for reading." / "There are
          no vertical rules — to decide whether a mark in row 8 sits in column 10 or 11
          you track your eye up about 1,100 pixels with nothing to follow."
GRAY      "Survives on shape."
NUMBER    "Fourteen — the total count of green diamonds across the nine build rows."
          — located at: diamonds counted in the grid. Off the plot.
```

**Screen C**
```
ABOUT     "It looked complete — the plot area runs to the right edge with clean white
          space ... nothing is clipped, nothing is bisected. After reading the title:
          flat contradiction."
TITLE     "I counted the diamonds as the subtitle instructed ... Eight. The instruction
          'Count the diamonds to check the title' returns a number that contradicts the
          title, and the chart gives the reader no reason to doubt their own count." /
          "Cascadia Matter Ledger (row 7) loses both of its diamonds and appears here as
          a build that contributed nothing new."
FORM      "a chart that silently drops 43% of its columns while looking complete isn't
          the wrong chart, it's a broken one. Whatever the responsive rule is that
          produced C, it needs to either signal the crop the way A does or refuse to
          render."
HARD      "The header numerals sit above their names in a slightly larger weight, which
          reads at first glance as a data value rather than an index."
GRAY      "the chart's problem is that a third of its marks aren't printed in any colour."
NUMBER    "I would read eight ... I'm naming it plainly as the answer this plot gives,
          and it is the wrong one."
```

**Screen D**
```
ABOUT     "nine builds in first-commit order ... No divergence."
TITLE     "Yes, every piece." / "One wording trap worth naming even on the sound screen.
          The footer says 'the golden fixture is the fourteenth surface.' Golden fixture
          is column 8 ... the eye goes to the rightmost column looking for it, and the
          diamond isn't there. I had to trace it twice."
FORM      "It is not the right form for what the title claims, which is a two-point
          trend. ... A small cumulative-count column at the right edge ... would be the
          one element that survives a responsive crop. I'd call this the chart's central
          design gap rather than a defect."
HARD      "No vertical rules across fourteen columns spanning roughly 1,000 pixels" /
          "The interleaved design-standard rows ... put a second, unrelated timeline
          into the row axis of the matrix ... a reader counting rows must know to skip
          them." / "nothing visually separates 'does not carry' from 'not applicable.'"
GRAY      "Survives, and this is the screen where I'd say so without caveat on size."
NUMBER    "Fourteen — counted as green diamonds across all nine build rows, columns 1-14."
          — located at: diamonds counted in the grid. Off the plot.
```

---

### Moderator's note: what the images and the ladder together establish

Three of four seats read Screen C as columns **deleted**. `k6-ladder.json`, which
no seat saw, says otherwise: at viewport 742 the table is 964 px inside a 676 px
wrapper and `scrolls: true`. **The columns are present and scrolled out of view.**

**That correction does not weaken the finding; it sharpens it, and it moves the
remedy.** A crop at a column boundary with no cue is what a reader meets in the
default state, and the default state is the most-seen view. This session verified
the cue question directly rather than inferring it, by cropping the right edge of
both narrow renders:

- **Screen A (320):** the `5` is severed mid-glyph at the card edge. Visibly truncated.
- **Screen C (742):** the band rule, the row separators and the card border all
  terminate cleanly after column 8, with white margin beyond. **No clipped glyph,
  no fade, no scrollbar, no partial column.** It is indistinguishable from a
  finished eight-column table.

**The crossing runs the wrong way.** From the ladder: at 741 the narrow layout is
engaged, the table is 494 px in a 687 px wrapper, and it **fits**. At 742 the
narrow layout disengages, the table becomes 964 px, the wrapper **shrinks** to
676 px, and it overflows by 288 px. So the chart is complete below the breakpoint
and loses six columns above it, across a one-pixel change in viewport width.

**This is the finding a K6 ladder exists to produce**, and it is not visible from
either render alone. It is stated here as a moderator observation derived from the
ladder file, not as a seat return, and it is the build author's to accept or
reject like any other.

---

### 3 · Disposition

**Sorted by `n` descending. `Disposition` is left empty throughout: it belongs to
the build author under Rule 7.4 and is not this project's to make.** `Novel?` is
blank because `N` was not measured. The `Rule` column is this session's
indication only; see the `HEAD` warning at the top.

| # | Finding, in the reviewer's words | Seats | n | Defect? | Novel? | Disposition | Rule |
|---|---|---|---|---|---|---|---|
| 1 | *"the title says fourteen and the table stops at eight"* — and *"The right-hand edge looks like a finished edge"* | 1,2,3,4 | **4** | yes | | *author* | K6 / 6.11 |
| 2 | *"The title tells me to count the diamonds and I physically cannot."* (320 and 742) | 1,2,3,4 | **4** | yes | | *author* | K6 / 7.1 |
| 3 | *"Fourteen lookups to learn what the chart is about. That's fine for counting, useless for reading."* (741, numeric-only headers) | 1,2,3,4 | **4** | yes | | *author* | labelling |
| 4 | *"The instruction 'Count the diamonds to check the title' returns a number that contradicts the title, and the chart gives the reader no reason to doubt their own count."* | 1,3,4 | **3** | yes | | *author* | 7.1 |
| 5 | *"I read the title the first way, then counted build nine's row and got ten"* — "Fourteen by build nine" reads as build nine's score; the cumulative total is never drawn | 2,3,4 | **3** | yes | | *author* | 7.1 |
| 6 | *"the green note ... says 'the golden fixture is the fourteenth surface,' and on this screen the golden fixture is plainly column 8"* (also a trace-twice trap at 1040) | 2,4 | 2 | yes | | *author* | 7.1 |
| 7 | *"Not a styling complaint, it genuinely slowed my reading"* — era and build labels hyphenate and wrap to four or five lines at narrow widths | 3,4 | 2 | yes | | *author* | type pairing |
| 8 | *"they interrupt the build sequence and a reader counting rows must know to skip them"* — the design-standard version rows put a second timeline in the row axis at equal visual weight | 3,4 | 2 | yes | | *author* | 5.x |
| 9 | *"to decide whether a mark in row 8 sits in column 10 or 11 you track your eye up about 1,100 pixels with nothing to follow"* | 4 | 1 | yes | | *author* | 3.x |
| 10 | *"the blue version chips and the grey carry-squares become identical, distinguishable only by living in a grey band row"* — the one encoding not redundant to shape | 4 | 1 | yes | | *author* | 3.4 |
| 11 | *"Are these nine clients? The names read like real engagements to me and I couldn't tell whether I was looking at internal projects or customer work."* | 3 | 1 | yes | | *author* | 0.1 |
| 12 | *"absence is much harder to establish than presence and it's usually where these things rot"* — no support for "empty cells are facts, not debts" | 1,2,3 | **3** | no | | *author* | — |
| 13 | *"Every one of these fourteen boxes is ticked by the same people who wrote the list"* | 1,3 | 2 | no | | *author* | — |
| 14 | *"would let the reader read '14' directly off row 9 instead of counting 14 diamonds spread over 2,000 pixels"* — no per-row or cumulative total column | 2,4 | 2 | no | | *author* | — |
| 15 | *"a surface could have been added to build one last week and it'd look identical to one that shipped with it"* — marks are undated | 2 | 1 | no | | *author* | — |

**Why 12, 13, 14 and 15 are marked "no".** They are questions about the subject
matter and about scope, not misreadings a competent reader would make from the
picture. 13 in particular is the question the room will ask and the artifact may
be right to leave to the conversation. **14 is the interesting one**: seat 4 named
it a design gap rather than a defect unprompted, and it is also the single change
that would blunt findings 1, 2 and 5 at once, since a total pinned to the right
edge is the element most likely to survive a crop. Recorded as a non-defect with
the highest leverage on the table.

**Findings 1, 2 and 3 are four-seat convergence.** Four readers who could not see
each other fell into the same three holes. Those are the fix order.

---

### 4 · Summary

```
PANEL: 4 seats, simulated · 1 chart (4 states) · findings 15 · defects 11 · novel not measured
       fixed 0 · accepted 0 · rejected 0 · multi-seat defects 8
       D = 11.00 defects/chart · N = not measured · R = not yet dispositioned
```

Emitted by `scripts/panel_metrics.py`, with two corrections made by hand and
stated rather than silently applied:

**1. `R = 0.00` as printed is wrong and is recorded as "not yet dispositioned".**
The script computes `R` as rejected over findings, so an undispositioned panel
reports a perfect zero rejection rate, which is the most flattering possible
reading of a panel nobody has judged yet. `R` here is not zero; it does not exist
yet.

**2. The script exits non-zero on this input.** Its schema admits only `fixed`,
`accepted` and `rejected`. **It has no state for "disposition pending, and it
belongs to someone else"** — which is the normal condition of every panel this
estate runs, because `ESTATE-STATE.md` §3 puts the panel in this project and
Rule 7.4 puts disposition with the build author. The tool cannot represent the
estate's own division of labour. **Build-forward candidate.**

**`D = 11.00` is not comparable to prior panels and should not be read as a
27-fold regression against Deal Desk's 1.91.** `D` is defects over charts, and
this panel has one chart where that one had eleven. Per state, this is 2.75.
**A second build-forward candidate:** `D`'s denominator makes single-chart panels
and K6-ladder panels incommensurable with multi-chart panels, and Rule 7.4's
retirement trigger reads `D` across consecutive modules as though they were.

### What this record can and cannot be held to

Held to, and checkable by anyone opening this file: a roster with a stated reason
per seat, four items returned per seat per state, a located source for every
quoted number including the four that could only be sourced to the descriptive
paragraph, and a row for every finding.

Not established by this record: that the renders come from `build/part2-page`;
that the `Rule` column matches the Live standard, given `HEAD` was an unmerged
branch; and blindness, which was measured contaminated rather than asserted
clean.

**A clean panel is never a pass, and this one was not clean.** Eleven candidate
defects from four readers measure nothing about how often a real reader would
misread this. Three readers are not a sample.

## Owed

- The reading panel, run from the Estate project on `docs/renders/`, at 320
  and 1040 at least; its record and disposition enter §4 of this file.
- The two `[AARON]` lines in `src/page_text.py`, rewritten by Aaron before
  publish.
- The thumbnail `og:image` names, produced by the site-side session.
- Publishing and Pages: Part 2b.

## Verdict

**DO NOT SHIP** until the panel returns. No other invariant is open.
