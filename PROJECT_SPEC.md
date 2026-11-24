# Errata — product and software requirements

**Status:** proposed plan, November 24, 2026. Owner: Rishi Bhansali.
Application implementation requires owner review. Nothing here is a measured result.

## Product requirements (PRD)

### Purpose and users
Errata helps a developer or electronics engineer answer technical questions whose
answers live in prose, table cells, plotted curves, diagrams or related revisions.
The product must show what supports an answer, under which conditions it applies,
and when the available documents do not establish an answer. Rishi is both builder
and learner; explainable implementation and reproducible experiments are product
constraints, not optional tutorials.

### Problem and differentiation
Text retrieval loses spatial context and often separates numbers from headers,
units, test conditions and version applicability. A useful answer requires an
evidence chain: document revision → page/region → extracted fact → calculation →
claim. Errata will store that chain explicitly, use deterministic calculations,
and expose disagreement instead of letting an LLM silently select a convenient value.

### Main journeys
1. Add an approved PDF; see ingestion state and any pages needing review.
2. Ask for a specification under explicit temperature, supply and part conditions;
   inspect a highlighted table cell and its headers beside the answer.
3. Request a value from a supported plot; see calibration, approximate result,
   units, uncertainty and the actual curve segment used.
4. Compare a datasheet with an applicable erratum; see both pieces of evidence,
   revision applicability and any unresolved contradiction.
5. Ask an unsupported question; receive an abstention with the missing evidence
   or condition, rather than a plausible but ungrounded number.

### Scope and delivery contract
Six weeks at 15–20 hours/week (90–120 hours total) delivers a modest local-first MVP
and a reviewable evaluation workflow. It does **not** promise production hardening
or every research feature. If less time is available, extend the calendar rather
than removing correctness gates. The final research release may take another
4–8 weeks or more, particularly for manual labeling and visual model evaluation.

| Capability | Six-week commitment | Later full-engine scope |
|---|---|---|
| PDF ingestion and versions | Immutable hashes, manual family/revision metadata, async jobs | Automatic revision discovery |
| Page/region indexing | Born-digital PDFs, text, tables, figures and diagram crops | Complex scans and robust OCR |
| Retrieval | Dense text + BM25 + cross-encoder, bounded corpus | Visual retrieval adopted after benchmark |
| Numerical evidence | Typed table facts, explicit conditions, unit conversions | Broad automatic fact extraction |
| Graphs | Reviewed calibration, single monotone curve, linear axes | Multiple curves, log axes, automatic calibration |
| Diagrams | Locate and cite diagram regions | Semantic connectivity/topology reasoning |
| Cross-document | Explicit family/revision relationships and curated errata rules | Automatic conflict discovery |
| Answers | Claim citations, deterministic arithmetic, abstention | Calibrated general multimodal confidence |
| UI | Question, answer, evidence, revision selector and job status | Team workflows and annotation tooling |
| Evaluation | 100 reviewed items if review time is available; never self-certify | Expanded families, visual baselines and calibrated judge |
| Operations | Local Compose, traces, budgets, setup CI → regression CI | Public multi-user service and managed AWS deployment |

A reduced MVP can ship after week 3: upload → table/text retrieval → cited answer →
evidence view. It must be labeled **text/table MVP**, not the complete engine.
A research release requires all required modalities and all three benchmark arms;
experimental visual work can delay that release without blocking the MVP.

### Non-goals
No autonomous engineering certification, arbitrary PDF understanding, unrestricted
web crawler, model pretraining, circuit simulator, multi-tenant SaaS or Kubernetes.
No graph-derived typical value may be presented as a guaranteed operating limit.

### Corpus and rights
Start with 8–12 publicly accessible manufacturer documents from two part families,
including at least two related errata/manual sets and genuine revision pairs when
available. A candidate is the [STM32F405/415 documentation catalog](https://www.st.com/en/microcontrollers-microprocessors/stm32f405-415/documentation.html).
This is a discovery lead, not a verified licensed dataset. Select the second family
after checking graph quality, terms and genuine revision availability. Do not claim
historical PDFs exist before locating them. If revision pairs cannot be acquired,
reduce claimed coverage; synthetic fixtures must remain separate from real benchmarks.

Record source URL, publisher, retrieval date, SHA-256, title, part family, revision,
published date, license/terms URL, permitted uses and reviewer decision. Public
access is not a redistribution license. Default Git contents are metadata, original
annotations and permitted fixtures; vendor PDFs, crops and large extracted text stay
local. Audit whether even derived annotations/excerpts may be shared. Unknown rights
block redistribution. No corpus downloads or human review have occurred yet.

## Software requirements (SRS)

The IDs below are traceable to roadmap gates and planned test cases.

| ID | Requirement | Verification / acceptance |
|---|---|---|
| ING-01 | Validate PDF type, limits and rights metadata; preserve original hash | Duplicate content returns existing revision; bad/oversize files rejected |
| ING-02 | Durable asynchronous states and retry-safe processing | Kill worker mid-job; restart completes once without duplicate regions |
| VER-01 | Separate immutable revision identity from publication date | Two revisions coexist; changing latest does not rewrite citations |
| EXT-01 | Store pages and text/table/figure/diagram bounding boxes | Reviewed fixture overlays align with visible content and page rotation |
| EXT-02 | Preserve table headers, footnotes, merged cells and units | At least 10 reviewed tables retain relevant header/condition context |
| RET-01 | Fuse text dense and BM25 retrieval, then rerank | Same corpus/filter contract across both indexes; report Recall@K and MRR |
| RET-02 | Swappable visual candidate adapter with explicit model revision | Visual experiment reproduces candidates; no fabricated enabled status |
| NUM-01 | Store raw tokens, canonical units, ranges and qualifiers | Zero dimensionally invalid conversions pass tests; originals retained |
| NUM-02 | Execute allowlisted arithmetic only | No eval/generated code; division by zero and incompatible units rejected |
| GRA-01 | Digitize supported plots with reviewed anchors and uncertainty | Held-out anchor checks and known synthetic curves pass tolerance; unsupported plots abstain |
| REV-01 | Apply explicit supersession only within matching applicability | Temperature/package/silicon revision mismatches cannot override facts |
| ANS-01 | Return claim-level page and region citations | Every factual answer claim resolves to an immutable evidence record |
| ANS-02 | Distinguish answered, partial, ambiguous and abstained | Missing units/conditions/critical evidence triggers reasoned abstention |
| UI-01 | Answer and evidence side by side | Selecting a citation opens matching page overlay and revision label |
| OPS-01 | Cache by corpus/config/model versions, track usage and traces | Revision/provider change invalidates cache; repeat request exposes cache hit |
| EVAL-01 | Version 100+ human-reviewed questions and compare three pipelines | Frozen manifest, review status and reproducible raw reports; no result without run |
| SEC-01 | Bound uploads, retrieval, model use and untrusted content | Adversarial prompt/file/URL tests; network restrictions and limits verified |

### Graph algorithm contract
Input: a single identified curve on a Cartesian graph, monotonic x, linear x/y axes,
readable labels, no broken axes, no occlusion, no dual axes and no ambiguous legend.
The user confirms at least two x and two y calibration anchors and curve identity.
OpenCV supplies candidate curve pixels; a reviewer approves the trace. Store pixel
samples, transforms, anchors and estimated pixel error. Convert x and y by affine
calibration; interpolate piecewise linearly inside the supported domain only. Propagate
pixel/calibration uncertainty and report significant digits accordingly. Reject
extrapolation, unapproved traces and unsupported graph classes. This is assisted
digitization, explicitly not general automatic graph comprehension.

### Conflict and answer policy
Facts are comparable only when parameter, component, package, silicon revision,
conditions, unit dimension and min/typ/max roles agree. An explicit erratum can
supersede an affected fact; a later date alone does not prove precedence. Store
`supersedes`, `qualifies`, `contradicts` and `references` edges with provenance and
review state. Conflicting applicable evidence without an authoritative resolution
must be shown as ambiguous. Never treat different test conditions as a contradiction.

Confidence initially means evidence status, not an LLM's self-reported probability.
Hard checks precede generation; a valid answer needs evidence coverage, verified
numerical inputs and applicable revision context. Probabilities appear only after
calibration against labeled validation data. Report extraction uncertainty separately
from retrieval confidence and real-world measurement uncertainty.

### Nonfunctional requirements
- Reproducibility: source hashes, parser/model revisions, prompts, seeds and config
  accompany each ingestion and benchmark; migration rollback is documented.
- Performance targets, unmeasured: warm query p95 ≤15 s, first response ≤3 s where
  streaming is enabled, for 1–3 concurrent users and up to 1,000 indexed pages.
  Report exact hardware, cold starts and provider time separately.
- Reliability: immutable artifacts, idempotent jobs, bounded retries and atomic
  index publication; no partial revision visible as fully indexed.
- Accessibility: keyboard navigation, labeled controls, readable contrast and a
  text alternative to colored evidence highlights.
- Privacy: model egress opt-in, no document bodies in default telemetry; local
  artifact deletion invalidates caches and evidence availability explicitly.
- Budget: no cloud/GPU resource creation during planning; quotas and spend limits
  precede public demo. See [deployment estimates](docs/DEPLOYMENT.md).

## Acceptance and release status
Every requirement above remains **planned**. Phase gates are in [ROADMAP.md](ROADMAP.md).
The complete engine is accepted only after human-reviewed evaluation, supported
visual retrieval, bounded graph numerics, all citations/conditions checked and
reproducible reports exist. Failing a numerical or evidence gate narrows supported
scope or delays release; it never justifies unsupported accuracy claims.
