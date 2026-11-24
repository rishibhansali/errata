# Six-week roadmap and phase acceptance

**Plan only.** Estimated 15–20 hours/week including learning, review and contingency.
Each week budgets roughly 10–12 implementation hours, 3–4 learning/review hours and
2–4 evaluation/buffer hours. Labels count as real work. Rishi approves the plan
before phase 1 code begins. Do not compress skipped learning into an unexplained merge.

## Phase 0 — this setup
Deliver README, requirements, architecture/flows, schema, API, evaluation, deployment,
threat model, learning agreement, GitHub repository and documentation CI.
Acceptance: links/checks pass; repository is owned by `rishibhansali`; commits use
owner identity without AI co-author trailers; README says planning, not working app.
No paid services, app features, vendor PDF downloads or benchmark claims.

## Week 1 — reproducible foundation and first document (15–20 h)
- Session 1: review plan with Rishi; explain Python packages, virtual environments,
  HTTP, Docker and SQL. Choose pinned Python/model-compatible versions.
- Session 2: dependency/license matrix; create backend/frontend lockfiles, Compose
  PostgreSQL+pgvector/Redis, configuration models and minimal health endpoint.
- Session 3: schema migrations, artifact abstraction and validated PDF upload.
- Session 4: durable job record, worker lease/retries, parse/render a permitted fixture.
- Session 5: overlays for one page, smoke tests and walkthrough; identify corpus
  candidates and draft 10 questions without marking them reviewed.

Gate G1 (ING-01/02, VER-01, EXT-01): fresh setup commands work; real database/queue
smoke passes; two distinct revisions coexist; duplicate upload is idempotent; worker
crash/retry does not duplicate pages; invalid/oversize PDF rejected; rotated fixture
overlay is correct. Full tests and build pass from main after integration.

## Week 2 — text/table retrieval and evidence UI (15–20 h)
- Session 1: compare extraction on 20 representative pages; inspect 10 tables and
  manually label errors. Preserve headers, units and footnotes.
- Session 2: teach embeddings/cosine similarity; exact pgvector search, then BM25.
- Session 3: RRF fusion and small cross-encoder; measure candidate loss/latency.
- Session 4: React question/evidence layout, page viewer and citation selection.
- Session 5: 20 reviewed dev questions; trace source → database → ranked evidence.

Gate G2 (EXT-02, RET-01, UI-01): page/region IDs resolve; reviewer can verify every
numeric table answer input against headers; keyword-only and dense-only retrieval
run on identical filtered snapshot; clicking evidence shows correct revision/page.
Produce raw retrieval metrics, not superiority claims.

## Week 3 — end-to-end MVP (15–20 h)
- Session 1: provider protocol, one real provider adapter plus deterministic test fake;
  second provider can be added later without modifying domain code.
- Session 2: structured claims, citation validation, unit engine and allowlisted arithmetic.
- Session 3: evidence sufficiency rules, missing-condition abstention and conflict UI.
- Session 4: cache keys, trace spans, provider usage/cost recording and timeouts.
- Session 5: review 20 more questions (40 total); local demonstration and bug buffer.

Gate G3 (NUM-01/02, ANS-01/02, OPS-01): upload → question → supported answer or
abstention works in browser; every claim cites available evidence; unit edge cases,
provider outage and prompt-injection fixtures pass; real configured provider smoke
passes if provider mode is enabled. Publish **text/table MVP** only after review.

## Week 4 — bounded curves and document applicability (15–20 h)
- Session 1: coordinate transforms and linear interpolation lesson; supported-plot
  detector/checklist and synthetic ground-truth curves.
- Session 2: OpenCV trace proposals and reviewed calibration/trace import.
- Session 3: reject log/multi-curve/occluded plots; propagate pixel error and show
  source curve segment. Keep calibration UI minimal or use reviewed annotation file.
- Session 4: explicit document/fact relationships and curated applicable errata rules.
- Session 5: review 20 further questions (60 total), including condition mismatch.

Gate G4 (GRA-01, REV-01): supported synthetic curves meet predeclared tolerances;
real graph estimates checked by Rishi; no extrapolation; wrong package/temperature
cannot supersede a fact; unresolved conflict returns ambiguous with both citations.
Do not expand graph types to rescue benchmark coverage.

## Week 5 — benchmark corpus and visual feasibility (15–20 h)
- Sessions 1–2: review remaining 40 questions to reach 100. Reserve 6–8 hours here;
  extend schedule if review quality requires more time.
- Session 3: reproduce text-only baseline and caption-based baseline; separate offline
  caption cost from query cost. Freeze development/test manifests.
- Session 4: benchmark optional SigLIP adapter on selected pages; inspect ColPali
  memory/licensing/integration cost before deciding whether to implement it.
- Session 5: assess whether visual indexing earns its resource cost and survives
  reranking. Record failure examples and checkpoint hashes.

Gate G5 (RET-02, EVAL-01 partial): 100 items truly reviewed with evidence/tolerances
or milestone explicitly marked incomplete; identical snapshots and generation model
for comparisons; no test-set tuning. A complete visual pipeline is a release gate,
not a guaranteed week-5 result. If experiment slips, ship MVP and schedule extension.

## Week 6 — validation, reproducibility and handoff (15–20 h)
- Session 1: benchmark three arms if visual pipeline exists; otherwise mark complete
  arm pending and publish only completed comparisons with honest limitations.
- Session 2: deterministic regression CI; optional cost-capped scheduled model runs;
  bootstrap confidence intervals and numerical/unit/citation metrics.
- Session 3: human scoring rubric and exploratory LLM-judge agreement on reviewed
  examples; do not use uncalibrated judge as sole release gate.
- Session 4: security tests, dependency scan, restore drill, deployment runbook and
  cost estimates; private AWS staging only if separately authorized.
- Session 5: code walkthrough, reproducible demo, final limitation list and next tasks.

Gate G6 (SEC-01, EVAL-01): all completed features have full tests/build green on main;
config/services verified with real smoke; reproducible manifests/reports and review
history exist; release states unimplemented capabilities; no claimed complete engine
without visual arm, 100 reviewed questions and modality-specific evidence checks.

## After six weeks: stretch and completion backlog
1. Finish visual retrieval comparison and 100-item review if time gates slipped.
2. Expand a frozen held-out corpus and obtain a second independent reviewer.
3. Calibrate abstention and LLM judge on sufficient independent examples.
4. Automatic graph calibration; log axes/multiple series only after separate gold sets.
5. Diagram connection extraction, OCR-heavy documents and richer cross-document joins.
6. Automatic revision detection, robust conflict mining and second live LLM adapter.
7. Public read-only AWS demo, managed services, stronger authentication and load testing.

## How each coding session runs
Explain the current problem → sketch one example → make a small branch/commit →
walk through the changed code and tests → Rishi runs a small exercise → capture
questions and verified commands → integrate only after checks. No implementation
is complete just because the assistant wrote it. See [learning plan](docs/LEARNING.md).
