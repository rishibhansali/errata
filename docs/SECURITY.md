# Threat model and risk register

Status: proposed controls; none are claimed implemented. Assets: provider keys,
source documents, evidence integrity, revision provenance, user questions, evaluation
labels, artifact storage, compute budget and repository credentials.

Trust boundaries: browser → API; API → DB/queue; untrusted PDF → parser worker;
retrieved content → LLM; application → external providers; CI → secrets/cloud.
Local single-user scope reduces exposure but does not make PDFs trustworthy.

| Threat / risk | Likelihood / impact | Planned control | Verification / owner |
|---|---|---|---|
| PDF parser exploit or decompression bomb | Medium / high | Isolated non-root worker, no network, page/size/time/memory limits, patched pinned parser | Malformed/oversize fixtures and process limit smoke; Rishi |
| Prompt injection inside text/figure | High / high | Documents are data; no arbitrary tools/shell; schema-bound outputs and evidence validation | Hostile embedded instructions cannot access secrets or invent citation IDs; Rishi |
| SSRF through document URL | Medium / high | No remote importer in MVP; future HTTPS allowlist, DNS/IP/redirect validation, block metadata/private ranges | Redirect and rebinding tests before enabling; Rishi |
| Secrets exposed in Git/logs/frontend | Medium / high | Ignored env files, server-only keys, log redaction, secret scan | Inspect bundle/log fixtures and CI scan; Rishi |
| Unauthorized access or cross-scope cache | Medium / high | Loopback by default, owner-only ingestion, scoped auth/artifact URLs and cache keys | Access isolation tests with two principals before multi-user mode; Rishi |
| Wrong numerical answer | High / high | Preserve units/conditions, typed calculations, reviewed curves, abstention | Gold numerical tests, unsupported-graph negatives; Rishi |
| Wrong revision precedence | High / high | Explicit applicability and reviewed supersession; never date-only override | Same parameter/different conditions and silicon revisions tests; Rishi |
| Malicious or accidental artifact replacement | Medium / high | Immutable hashes, scoped storage, manifest verification | Mutated artifact fails checksum and invalidates evidence; Rishi |
| Copyright/license mismatch | Medium / high | Source/model/dependency ledger, no vendor PDFs in Git by default | Rights review before ingestion/redistribution; Rishi |
| Runaway API/GPU spend | Medium / medium | Quotas, bounded context/retries, hard cap, offline GPU jobs | Budget-exhaustion test and resource shutdown check; Rishi |
| Evaluation leakage or overclaim | High / high | Frozen grouped split, separate labels from prompts, raw outputs, honest status | Review data lineage and report manifests; Rishi |
| Worker crash/Redis loss | Medium / medium | Durable DB jobs, leases, reconciliation, idempotent writes | Kill/restart integration and duplicate delivery test; Rishi |
| Supply-chain compromised dependency/model | Medium / high | Lockfiles/hashes, reviewed licenses, no remote model code by default, scans | Clean build and model load without trust_remote_code; Rishi |
| Scope exceeds six-week capacity | High / high | Text/table MVP first, gated graph/visual experiments, weekly scope review | Phase gate review; extend dates instead of claiming finished work; Rishi |
| Small evaluation set misleads | High / medium | Per-stratum counts, intervals, external review later | Disclose limited family diversity and test size; Rishi |
| Data loss or unavailable citations | Medium / high | Backups, immutable snapshots, tombstones, restore drills | Restore matching DB/artifact snapshot; Rishi |

## Safety and privacy boundaries
Errata is an evidence inspection tool, not an engineering signoff authority. Display
whether a value is typical, guaranteed or approximate. Raw documents may contain
instructions, URLs and code; none receive authority to run commands. Calculation
operations are allowlisted domain functions, not Python eval or model-generated SQL.
Parameterize database queries. Sanitize Markdown/HTML in UI and document metadata,
apply CSP, restrict CORS and never render untrusted script in PDF wrappers.

Keep raw queries/documents out of default traces; retain minimal IDs/timings and
config hashes. Proposed retention: debug traces 7 days, operational summaries 30 days;
owner-configurable and documented before external hosting. Deletion removes source
artifacts/derived crops/vectors, invalidates caches, and marks affected historical
citations unavailable. Third-party provider retention policies must be reviewed before
enabling egress. Public demo supports a fixed approved corpus and no anonymous upload.

## Release security gate
Before any public service: real auth/access and upload limits tested, dependencies
scanned, no exposed DB/Redis, TLS configured, budgets enforced, backups restored and
provider data handling reviewed. Document residual risks and unsupported modes.
This is a concrete future release gate, not a request to provision services now.
