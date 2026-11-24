# Evaluation and benchmarking strategy

Status: design only. **0 collected questions, 0 human-reviewed labels, 0 benchmark
runs.** Targets below are acceptance proposals, not performance claims.

## Dataset: 100 reviewed questions minimum
| Primary stratum | Count | Required evidence |
|---|---:|---|
| Text retrieval | 20 | Exact passage, conditions and region |
| Tables | 20 | Cell, row/column headers, units and footnotes |
| Graph numerical | 15 | Supported curve, anchors, trace and tolerance |
| Cross-document | 15 | At least two documents and reasoning links |
| Versions/conflicts | 15 | Revision applicability and resolution or ambiguity |
| Unanswerable | 15 | Missing evidence explanation, nearest distractors |
| **Total** | **100** | Each item manually approved |

Categories are primary/disjoint for counts; secondary tags allow overlap. Include
ambiguous conditions, incompatible units, no-answer distractors and “typical vs max”
cases. Do not fill the graph stratum with unsupported figures and count abstentions
as successful numerical answers. Unsupported plots belong in negative cases.

Use 60 development, 20 calibration/validation and 20 locked test items, stratified
as closely as possible. Group related questions by document family/revision lineage
and template; avoid near-duplicate leakage across splits. With two families this
may conflict with exact stratification: prioritize grouping, report actual counts,
and add families before claiming cross-family generalization. A 20-item test set
has high uncertainty; never present small differences as conclusive.

## Label record
Versioned JSONL fields: `id`, `question`, `primary_category`, `tags`, `split`,
`corpus_snapshot`, `source_hashes`, `applicable_versions`, `expected_status`,
`reference_answer`, `reference_claims`, `gold_regions` (page/bbox/role),
`required_evidence_sets`, `numeric_expectations` (value/unit/absolute+relative tolerance),
`conditions`, `allowed_calculation`, `unanswerable_reason`, `label_author`,
`reviewer`, `reviewed_at`, `review_status`, `notes`. No generated label is reviewed
until Rishi checks source evidence. Preserve raw proposal and review diff.

Rishi reviews every item against the original page. A second reviewer is preferable
for at least 20 items; if unavailable, use a delayed blind second pass by Rishi and
report that it is intra-rater consistency, not independent agreement. Resolve disputed
labels before freezing. Labeling is expected to take 8–15 hours initially plus
adjudication; this can extend the six-week calendar. Rights restrictions also apply
to benchmark excerpts and cropped evidence. Use owned synthetic fixtures in public
CI where vendor redistribution is not permitted.

## Three controlled pipelines
| Arm | Candidate/index content | Answer path |
|---|---|---|
| A: text-only RAG | PDF text chunks, dense+BM25 | Same generator, token limit and citation envelope |
| B: caption multimodal RAG | Same text plus versioned figure/table captions | Same generator; no structured numeric tool advantage |
| C: full Errata | Text, table facts, visual candidates, reviewed curves, revision expansion | Applicability checks, deterministic tools, validated claims |

A deliberately shares a strong text retriever rather than a weak straw-man baseline.
Compare end-to-end arms, then ablate C: remove visual, reranker, units/tools and revision
logic one at a time to identify the source of gains. A C run without visual retrieval
is labeled `errata-text-table`, never `full`. All arms use the same source snapshot,
query set, generation model/version, temperature, context budget, hardware policy
and retry limits. Record any differing preprocessing and its cost. Captions must not
be generated using test questions or answers. Test labels stay outside prompts.

## Metrics and exact conventions
- **Recall@K**, K=5,10,20: fraction of gold evidence units retrieved; deduplicate
  repeated region hits. Report page-level and region-level separately. Also report
  required-set coverage (all pieces needed for a cross-document answer).
- **MRR@10**: reciprocal rank of first relevant evidence unit, zero if missing.
- **nDCG@10**: gain grades 0 irrelevant, 1 useful context, 2 directly supporting;
  use `(2^grade-1)/log2(rank+1)` and ideal-ranking normalization.
- **Numerical accuracy**: canonicalize dimension-compatible units; pass when absolute
  error ≤ max(predeclared absolute tolerance, relative tolerance × |reference|).
  Use absolute tolerance near zero. Conditions and min/typ/max must match as well.
- **Unit accuracy**: correct dimension, unit conversion, scale and offset; report
  separately from value accuracy, plus joint value+unit+condition accuracy.
- **Citation correctness**: claim-level support precision and evidence coverage;
  right page but wrong cell is incorrect. Automated ID checks are necessary but do
  not prove support. Region overlap uses predeclared IoU≥0.5 plus human cell/header
  review; report annotation geometry failures separately.
- **Faithfulness**: supported factual claims / factual claims, human rubric first;
  omissions are measured by coverage, not hidden by short answers.
- **Abstention**: precision/recall/F1 on unanswerable cases and balanced accuracy;
  also report answerable coverage, false abstention, false answer and selective risk
  so always-abstain cannot win. Treat ambiguity and partial outcomes explicitly.
- **Latency**: p50/p95 end-to-end and stage time, warm/cold, concurrency and cache
  policy; run at least three repetitions for timed queries, preserve failures.
- **Cost**: input/output/cached tokens × versioned provider price plus actual GPU
  time; separately show ingestion, captioning, indexing, storage and query costs.
  Unknown prices are `unknown`, never zero. Normalize cost per answered and per
  correct answer in addition to per query.

Numerical tolerances are chosen during labeling before predictions: table values
honor printed precision; graph tolerances reflect resolution, calibration and line
thickness. Report conditional accuracy and accuracy on all answerable items so
abstentions cannot hide hard cases. Use paired bootstrap intervals grouped by family
where feasible and report sample sizes; two families limit meaningful cluster inference.

## Proposed release targets
For supported, reviewed MVP tasks: Recall@10 ≥0.85, numerical+unit accuracy ≥0.90,
citation support precision ≥0.95 and unanswerable recall ≥0.90 while answerable
coverage ≥0.80. These are aspirational quality gates to review after the first dev
baseline; freeze any adjusted thresholds before test evaluation. They do not certify
engineering safety. Report per-stratum counts/intervals even when aggregate passes.
Latency target is warm p95 ≤15 s on declared hardware; per-query spend target ≤$0.05
is a planning budget, dependent on selected provider/context. No current measurements.

## Calibrated LLM judge
Use the judge only for qualitative support/faithfulness assessments, not arithmetic.
Freeze rubric, prompt and judge version; blind pipeline names and randomize order.
On ≥30 development/calibration human-scored outputs, compare confusion matrices,
weighted agreement, false-support rate and disagreements by modality. Reviewer
adjudicates disagreements. Proposed adoption gate: ≥0.8 agreement and ≤5% false
support, with uncertainty explicitly reported; the sample is too small to establish
strong reliability. If it fails or sample is insufficient, judge remains exploratory.
Never tune judge on locked test labels. Estimate judge cost separately. Use a different
model family from generation when practical and disclose shared-model bias.

## Reproducible tooling to implement
Planned commands (not runnable in this planning repository):
```text
python -m benchmarks.validate --dataset benchmarks/questions.jsonl
python -m benchmarks.run --pipeline text --manifest benchmarks/frozen.json
python -m benchmarks.run --pipeline captions --manifest benchmarks/frozen.json
python -m benchmarks.run --pipeline errata --manifest benchmarks/frozen.json
python -m benchmarks.compare --runs artifacts/runs --output artifacts/report
```
Each run saves Git SHA, dependency lock hash, corpus/dataset hashes, split, model
revisions, prompt/config hashes, hardware, seed, pricing date, raw ranked evidence,
claims, predictions, failures, timings and usage. Outputs are immutable and rerunnable;
publish only rights-cleared reports. Never replace failed runs with an unlabeled rerun.

## Regression CI/CD
Current CI checks documentation only. Future pull requests run offline deterministic
unit/contract tests, synthetic PDF extraction and numerics, real Postgres integration,
frontend build and small retrieval fixtures. Reject any numerical/unit/citation-ID
regression on fixed fixtures. A frozen model retrieval subset can gate >2 percentage
point recall drop after accounting for deterministic settings. Small-set step sizes
must be stated, not treated as continuous statistics.

Scheduled/manual full model evaluation uses protected secrets, explicit cost cap and
pinned corpus; never expose keys to fork PRs. Reports are artifacts with a baseline
comparison. Human signoff is required to replace gold data or approved baseline.
Release workflow requires full tests/build on main, real service smoke, the frozen
benchmark run and review of metric drops; CI must distinguish unavailable external
services from a successful benchmark.
