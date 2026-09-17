"""page_text.py: the only authored text on the page.

Every string here is inlined by src/build_page.py. No figure is typed here:
a count, a running total or a first appearance is a token the builder fills
from data/builds.json, so K2 holds for the prose as well as for the summary.

Tokens the builder understands, and fails the build on if unknown:

    {link:<module name>}   the module's name, linked to its site case study
    {n:<key>}              how many surfaces that build carries
    {seen:<key>}           surfaces seen so far, that build included
    {firsts:<key>}         surfaces appearing for the first time at that build
    {first:<surface>}      the name of the first build to carry that surface,
                           linked

Two lines are Aaron's and ship in his words, not these: LEDE_AARON and
CLOSING_AARON. They are marked [AARON] and quoted in the Part 2 report for
his rewrite. House style: no em dashes; US spelling.
"""

# [AARON] The lede's first sentence. Draft for Aaron's rewrite.
LEDE_AARON = ("Nine Cascadia modules, built one after another over four months, and the "
              "tests each one could carry when it shipped.")

LEDE_SECOND = ("Every filled cell links to the file on GitHub that it names. An empty cell "
               "says the build did not carry that surface, and nothing is owed on it.")

# The matrix caption's subtitle, in secondary ink under the finding. The
# as-of date and the freeze are filled by the builder.
MATRIX_SUBTITLE = ("Nine portfolio modules (independent projects, not client work) by {n} "
                   "test surfaces, read from disk on {as_of}. Rows in first-commit order, "
                   "grouped by era. A square marks a surface the build carries and links to "
                   "the file; a diamond marks the first build to carry it, so there are {n} "
                   "diamonds in the table, one per surface. Count them to check the title.")

# Shown only where the table is wider than its screen and scrolls sideways.
SCROLL_HINT = ("The table is wider than this screen and scrolls sideways. All {n} columns "
               "are there.")

# Two annotations (Rule 3.4). The primary sits under the last row, at the
# mark the title's second number depends on; the secondary under the row where
# the most surfaces appear at once. Each is at most fourteen words. The builder
# fills the figures and asserts the facts they state.
ANNOTATION_PRIMARY = "Build nine: the golden fixture (column {col}) is the last of {n} to appear."
ANNOTATION_SECONDARY = "Build four, the first Python build: {firsts} surfaces appear at once."

# The standard's lane.
LANE_UNDATED = "v1.0, v2.0 and v2.1: undated, before the standard had a repository."
LANE_LABEL = "Design standard VIZ-PRINCIPLES"

# Five eras, three lines each: what could be tested, what had to be trusted,
# what the next era brought under test. Written from the matrix.
ERAS = {
    "Enterprise-shaped": {
        "tested": (
            "A one-command rebuild and a row-count check against stated expectations, in all "
            "three: {link:Cascadia Medical Devices}, {link:Cascadia Pharmacy} and "
            "{link:Cascadia Staffing}. Staffing added a second path: the KPIs the Power BI "
            "report shows, re-derived in SQL against the model."),
        "trusted": (
            "The source itself, since nothing was frozen or registered; every chart, since "
            "none was reviewed or read blind; and every published figure that was not one of "
            "Staffing's re-derived KPIs."),
        "next": (
            "A frozen source with a stated as-of date, a validation report committed beside "
            "the data, a chart review against a written standard, a reading panel, and a "
            "proof that the checks can fail."),
    },
    "Frozen and validated": {
        "tested": (
            "{link:Cascadia Finance} froze its SEC filings under a dated freeze, reconciled "
            "quarters to filed years and committed the report, fed every check corrupted data "
            "and published that all of them rejected it, and had its charts reviewed and read "
            "by a panel. The era's name understates it: the negative controls and the reading "
            "panel arrived here, not later."),
        "trusted": (
            "The row counts of the load, which no check compares against the source; the "
            "hashes of the raw files, which no register carries; the measure definitions, "
            "which no register states; and the published measures, which no second path "
            "re-derives."),
        "next": (
            "Tests as code, a metric register generated from the model that computes the "
            "numbers, a source register with a hash per file, and a row-count check against "
            "the source."),
    },
    "Reviewed and registered": {
        "tested": (
            "{link:Cascadia Deal Desk} kept everything Finance could test except the proof "
            "of failability, and added a count of conformed rows against raw. "
            "{link:Cascadia Control Tower} added dbt tests, a metric register generated from "
            "the model file and checked for drift on every build, a source register with a "
            "hash per file, and a published proof that its realism audits and structural "
            "checks trip on wrong numbers."),
        "trusted": (
            "That the numbers stay right after the build ends, since nothing runs on a "
            "schedule and no reconciliation is published; and the published measures "
            "themselves, since neither module re-derives them down a second path."),
        "next": (
            "A scheduled run that publishes its own health and run history, a "
            "reconciliation committed with its failures, and every published cell "
            "re-derived down a separately written path."),
    },
    "Operated": {
        "tested": (
            "{link:Cascadia Matter Ledger} and {link:Cascadia Fee Examiner} run a pipeline "
            "that re-asserts its invariants on a schedule and publish its health, its run "
            "history and a reconciliation that records the runs that stopped or failed. Both "
            "re-derive every published cell down a separately written path and carry a "
            "source register with hashes. Matter Ledger's one test file tests the page's "
            "touch readout in a browser."),
        "trusted": (
            "The build order, which neither states; the load's row counts, which neither "
            "compares to the source; the checks' own failability, which neither proves in a "
            "committed report; and the engine's first output, since no golden fixture "
            "existed before the code."),
        "next": (
            "A golden fixture specified by hand and committed failing before any engine "
            "existed, and a second derivation path written from the rules document rather "
            "than from the first path's code."),
    },
    "Re-derived": {
        "tested": (
            "{link:Cascadia Revenue Assurance} derives every published cell down two paths "
            "written from one rules document and compares them cell by cell; a "
            "hand-specified golden fixture, committed failing before either engine, passes "
            "on both. It keeps the freeze, the metric register, the chart review, the panel "
            "and the reconciliation, and adds tests as code."),
        "trusted": (
            "The source register, since a synthetic snapshot carries no hashes; the "
            "validation report and the proof of failability, since its gates print their "
            "result and do not commit it; and operation over time, since nothing runs on a "
            "schedule."),
        "next": (
            "Nothing is under test for a tenth build yet. No row exists for it, and no "
            "retrospective has been written for this one."),
    },
}

# The walk: era by era, short, then the nine modules one line each.
WALK = [
    ("The first three builds were shaped like enterprise work: a SQL Server star schema, "
     "a Power BI report, and one script that rebuilt the whole thing and printed a "
     "row-count table at the end. What could be checked was the load. What was published "
     "was trusted. {link:Cascadia Staffing} put one crack in that: the KPIs the report "
     "showed were re-derived in SQL and compared."),
    ("{link:Cascadia Finance} moved the work to Python and a static page, and with it came "
     "what a static page makes possible: a frozen source with a date on it, a validation "
     "report committed beside the data, a proof that the checks reject corrupted input, a "
     "chart review against a written standard, and a panel of readers who did not know the "
     "finding. {firsts:cascadia-finance-analytics} surfaces appeared in one build."),
    ("{link:Cascadia Deal Desk} and {link:Cascadia Control Tower} kept those and registered "
     "what they published: a metric register generated from the model, tests in the "
     "warehouse layer, and a source register with a hash per file."),
    ("{link:Cascadia Matter Ledger} and {link:Cascadia Fee Examiner} ran on a schedule and "
     "published what running looks like: health, history, a reconciliation that records "
     "its own failures, and every published cell re-derived a second way."),
    ("{link:Cascadia Revenue Assurance} wrote the rules first, the golden fixture second and "
     "two engines third, and published nothing until all of them agreed."),
]

WALK_LIST_INTRO = "Nine modules, oldest first."

MODULE_LINES = {
    "manufacturing-analytics": (
        "A simulated MES and NASA engine-degradation data in SQL Server, Fabric and Power "
        "BI: OEE and predictive maintenance, rebuilt by one script with a row-count table at "
        "the end."),
    "cascadia-pharmacy-analytics": (
        "CMS Part D and CDC VaxView in SQL Server and Power BI: messy public data cleaned "
        "into a star schema, with row counts validated on load."),
    "cascadia-staffing-analytics": (
        "CMS nurse-staffing data in SQL Server and Power BI: marketplace labor KPIs, each "
        "re-derived in SQL against the model."),
    "cascadia-finance-analytics": (
        "FormFactor's SEC filings, frozen and reconciled quarter to year, with a proof that "
        "every check rejects corrupted data and charts a panel read blind."),
    "cascadia-dealdesk-analytics": (
        "A seeded quote book matched against an agreement register: pricing exceptions "
        "priced in dollars, validated, reviewed and panelled."),
    "cascadia-controltower-analytics": (
        "A seeded fulfillment network anchored to public data: dbt tests, a generated "
        "metric register, and realism audits proven to fail."),
    "cascadia-matter-ledger-analytics": (
        "Federal civil dockets, frozen and then extended by a scheduled pull that publishes "
        "its health, its history and its reconciliation."),
    "cascadia-fee-examiner": (
        "Bankruptcy fee applications resolved across sources with no shared key: a source "
        "register with hashes and every cell re-derived a second way."),
    "cascadia-revenue-assurance": (
        "A synthetic subscription book: two derivation paths from one rules document, a "
        "golden fixture written first, and invoices reconciled to the month."),
}

# [AARON] The walk's closing line. Draft for Aaron's rewrite. The page stops here.
CLOSING_AARON = "From here the walk is a conversation. Pick a module; its row is where it starts."

DISCLOSURE = (
    "An independent portfolio project by Aaron Robbins. This page is generated from two "
    "data files, data/builds.json and data/standard.json, in the repository linked below; "
    "the inventory script that writes them reads the nine module repositories and never "
    "writes in one. No score, level, weight or percentage exists in the data. A cell is a "
    "path or it is empty. Older modules are not retrofitted; an empty cell is a fact about "
    "what a build carried, never a debt.")
