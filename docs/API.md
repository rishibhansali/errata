# API specification

Proposed `/v1` REST API. No endpoints exist yet. Pydantic models will generate
OpenAPI during implementation. UUID IDs, UTC timestamps, versioned JSON contracts.
Local mode binds loopback; network mode requires authenticated access. Public demo
is read-only against a curated corpus; ingestion requires owner credentials.

| Method and path | Input | Output / behavior |
|---|---|---|
| POST /v1/documents | multipart PDF + metadata JSON; Idempotency-Key header | 202 `{document_id,version_id,job_id,status}`; existing hash may return 200 |
| GET /v1/documents | cursor, limit≤100, family_id | paginated metadata and revision summaries |
| GET /v1/documents/{id}/versions | document ID | immutable revisions, applicability and ingestion state |
| GET /v1/jobs/{id} | job ID | status, stage, progress, safe_error, retryable |
| POST /v1/jobs/{id}/retry | authenticated owner | 202; only retryable failed jobs, bounded attempts |
| POST /v1/queries | question, snapshot_id, filters, optional requested_unit | validated answer envelope below |
| GET /v1/queries/{id} | query ID | retained answer envelope, respecting retention/access scope |
| GET /v1/versions/{id}/pages/{page_number} | one-based PDF page | page metadata and access-scoped image URL |
| GET /v1/regions/{id} | immutable region ID | bbox, page, revision, text/crop URL and review status |
| GET /v1/snapshots | cursor, limit | published snapshot manifests, enabled modalities |
| GET /health/live | none | process health, no secret/service detail |
| GET /health/ready | none | ready only when required DB/cache/index snapshot available |

Default upload limits to validate in phase 1: 25 MB, 200 pages/document, 2 ingestion
jobs and 3 query requests concurrently; longer manuals need explicit offline import
with resource budget. Corpus may contain selected documents up to 1,000 pages total.
Initial HTTP query deadline 30 seconds. Question length ≤4,000 characters; allowlisted
filter keys only. No arbitrary remote URL ingestion in MVP. A later URL importer
must block private/link-local destinations and validate every redirect and resolved IP.

### Example request (illustrative, not real evidence)
```json
{
  "question": "What is the specified maximum current at the documented supply and temperature?",
  "snapshot_id": "00000000-0000-0000-0000-000000000001",
  "filters": {"family_ids": [], "version_ids": []},
  "requested_unit": "mA"
}
```
Empty filters mean the selected snapshot, not unrestricted access. Explicit revision
selection means answer for that revision; label historical scope and show applicable
errata without silently replacing the requested evidence.

### Answer envelope
```json
{
  "query_id": "00000000-0000-0000-0000-000000000002",
  "snapshot_id": "00000000-0000-0000-0000-000000000001",
  "status": "abstained",
  "answer": "Specify the part, supply voltage and temperature range.",
  "claims": [],
  "citations": [],
  "calculations": [],
  "conflicts": [],
  "missing_evidence": ["part", "supply voltage", "temperature range"],
  "confidence": {"kind": "evidence_status", "value": "insufficient"},
  "usage": {"input_tokens": 0, "output_tokens": 0, "estimated_usd": 0},
  "timing_ms": {"total": 0},
  "trace_id": "illustrative-only",
  "cache_hit": false
}
```
Statuses: `answered`, `partial`, `ambiguous`, `abstained`. Claims contain `id`, `text`,
`citation_ids`, optional typed `numeric_value`, `unit`, `conditions` and `uncertainty`.
Citations contain `id`, `version_id`, `sha256`, `page_number`, `printed_page_label`,
`region_id`, `bbox`, `source_url`, `evidence_role`, `review_status` and scoped image URL.
Calculations expose operation, input evidence IDs, canonical inputs, result, unit
and engine version. Uncertainty must not imply calibrated probability when absent.

### Errors and security
Uniform error: `{error:{code,message,retryable,request_id,details}}`. Return 400 for
malformed scope, 401/403 authentication/access failures, 404 unavailable IDs, 409
idempotency conflict/unpublished snapshot, 413 oversize upload, 415 invalid format,
422 schema validation, 429 quota, 503 temporary dependency failure, 504 timeout.
An evidence abstention is a successful 200 response, not a server error. No stack
traces or provider secrets in responses. A reused idempotency key with different
content is 409. Keys are scoped to authenticated user and retained at least 24 hours.

Tests must cover contract examples, pagination, invalid UUIDs, coordinate invariants,
job polling, access isolation, evidence availability, provider timeouts and retry
semantics. Streaming/SSE and cancel endpoints are stretch features, not implied by
this initial contract. Exact endpoint names may change through documented ADRs.
