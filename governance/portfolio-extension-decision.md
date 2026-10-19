# Additive portfolio inventory and UI, 2026-10-19

Aaron requested an eleventh build, the two new Claim Integrity test surfaces,
and a Felix UI update to Build by Build. Codex prepared an isolated candidate;
Claude integrates it and returns a rendered preview before any merge.

The original `data/builds.json`, `data/standard.json`, inventory script,
validator and freeze declaration remain unchanged. Their fourteen-column
baseline is not a determination about the two additional definitions.

The authored extension is `governance/claim-integrity-extension.json`, pinned
to repository commit `e936d1ada2b5cfc54919157e4d9b8b9cd833506c`. Its status basis
is the build's frozen public verification snapshot. Repository byte identities
and served-snapshot identities remain separate where they differ. No new
execution is implied by recording either identity.

`governance/surface-catalog.json` defines sixteen stable IDs. The additional
counting clauses are appended to `governance/surfaces.md`. This is adoption into
this portfolio inventory, not an edit to the shared standards repository.
Older builds are explicitly not assessed in columns 15 and 16. No new positive
or negative conclusion about those builds is inferred from the old matrix.

`src/extend_inventory.py` deterministically writes `data/builds-expanded.json`
and `data/cell-evidence.json`. The latter separates presence, outcome and scope.
Limited records are not completed requirements. Honest failure, blocked,
deferred, open and historical states remain intact.

The current publication renderer is `src/build_expanded_page.py`, followed by
`src/validate_extension.py`. The original renderer remains available for its
historical inventory and must not overwrite the approved extension page during
integration. The original freeze gate continues to protect its original files.
No gate is disabled and no old file is regenerated to force a pass.

The new snapshot, evidence register, catalog, clauses and generated page must
be committed together. Later changes to any of them need deliberate review and
updated provenance. A prepared local candidate is not a published receipt.

No chart-invariant certification, independent evaluator custody, blind reading
panel or final-control effectiveness is claimed for this update. Focused
responsive, navigation, inventory-preservation and source checks are sufficient
for this UI integration. Any already-required website candidate checks still
apply. No new Claim Integrity assurance or detector-remediation cycle is requested.
