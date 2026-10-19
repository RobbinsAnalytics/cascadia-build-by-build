# Build forward: detection evaluation

Owner disposition, 2026-10-19: a future candidate, outside the current matrix for all eleven builds. Earlier exploratory records are historical context, not completed current assurance.

Candidate definition (formerly proposed as Surface 16):

 `detection_evaluation` | Numbers

A locked evaluation measures whether controls detect independently labeled failures, remain quiet on clean opportunities, and detect within the stated time window. It publishes the complete evaluation population, including misses and unobservable cases.

This surface owns population-level scoring and evaluator validity, including the disabled-detector, always-alert and missing-row mutants. Surface 9 retains diagnostic injections, reachability and paired clean controls for individual checks. Cross-reference shared executions rather than removing diagnostic specificity or copying inconsistent outcomes. The linked module evaluation protocol supplies the detailed procedure; its existence does not establish that every requirement was met.

**Counts:** committed `governance/detection-evaluation.md` with headings `Detection evaluation` and `Evaluator can fail`, linked to `governance/evaluation-protocol.md`, the precommitted truth-key identity, and `governance/detection-results.json`. Evidence includes actual detector/evaluator input separation, frozen detector output before key disclosure, per-class eligible targets and clean opportunities, matched detections, misses, false alarms, duplicate/unmatched alerts, not-yet-observable cases, and latency with unresolved cases retained. Record outcomes for a disabled detector, an always-alert detector, and a missing-scoring-row mutant. The truth and scoring rules cannot be supplied solely by the implementation under evaluation.

**Does not count:** a selected list of successful corruptions, aggregate accuracy alone, output-derived expectations, a committed hash described as proof of secrecy, caught-only latency described as overall latency, omitted held-out attempts, or a harness that succeeds after detector output disappears. Honest misses remain in the report; a surface is present even when the measured result blocks certification.

**Inventory detection:** require the report headings, protocol, access and output-lock records, commitment references, complete per-instance result schema, cohort bindings, and evaluator-mutant receipts. Recompute simple report totals from the committed event-level results, including all eligible and censored cases. Inspect declared commit ancestry and version references without executing sibling code. Static inspection cannot certify that no person saw an answer key.
