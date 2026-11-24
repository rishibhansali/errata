# Deployment and operating-cost plan

No infrastructure is provisioned. All figures are budgeting assumptions in USD,
not quotes or measured costs. Reviewed November 24, 2026; re-price before deployment.

## Deployment stages
1. **Local development:** Docker Compose for API, worker, PostgreSQL+pgvector and
   Redis; frontend dev server; local artifact directory; optional external LLM.
   Heavy extraction/embedding runs offline. No GPU required for the initial MVP.
2. **Private demonstration:** build pinned images, deploy API/UI and worker to one
   small AWS Lightsail instance, private DB/Redis on its internal container network,
   TLS reverse proxy, private S3 artifacts and owner authentication. Ingest locally
   if model memory exceeds VM capacity. One VM is a demonstration, not high availability.
3. **Production candidate:** only after load/recovery tests, separate worker and API,
   managed PostgreSQL, managed cache, private S3, managed secrets and monitored backups.
   ECS/Fargate or EC2 choice follows profiling; no Kubernetes by default.

Use multi-stage images, non-root processes, read-only filesystems where possible,
explicit health checks and pinned dependency/image versions. CI builds/scans immutable
images; deployment identifies Git SHA and migration version. Deploy to staging,
run migration and real endpoint/queue smoke, then promote. Database migration must
have backup/restore plan. Roll back application image and corpus snapshot pointer;
never downgrade schema blindly if the previous binary is incompatible.

## Budget scenarios
[Official Lightsail pricing](https://aws.amazon.com/lightsail/pricing/) is the source
to recheck instance bundles, region, IPv4 inclusion and transfer. The ranges below
reserve budget rather than asserting a specific SKU price. GPU costs are excluded
unless explicitly enabled.

| Scenario | Infrastructure/month | Variable model allowance/month | Planning total/month |
|---|---:|---:|---:|
| Local laptop, existing hardware | $0 incremental cloud | $0–30 | $0–30 excluding electricity/hardware |
| Small private CPU demo | $30–90 compute + $5–15 storage/backups + $0–10 telemetry | $5–50 | $40–165 |
| Managed production candidate | $150–450 compute/DB/cache + $10–40 storage/telemetry | $10–100 | $170–590 |

Domain registration, taxes, internet egress above allowances, recovery capacity and
paid CI minutes can add cost. Managed services are optional, not a six-week requirement.
Do not use a free-tier assumption to make the budget work. Always-on GPU may dominate
all these numbers; use a capped offline experiment instead and stop instances afterward.

Example query estimate, **hypothetical rates, not a selected provider price**:
1,000 queries × (4,000 input tokens × $1/1M + 500 output tokens × $4/1M) = $6.
At 10,000 queries the same assumption is $60, before captions, embeddings, retries,
judging and storage. Actual cost is `Σ(tokens_by_rate × rate) + GPU_seconds × rate`.
Log rate-table date and distinguish estimates from invoice totals. Initial ingestion
cost is separate: pages × caption tokens/rate + embedding time + rendering/storage.
A $10 experiment cap and $50 monthly model cap are proposed defaults for owner review;
provider/project quotas and app-side hard limits should enforce them.

## Complete setup checklist for future implementation
These are future requirements, not instructions that work against the current repo.
- Approve scope; install the chosen Python/Node runtimes and Docker through documented
  project tooling; create `.venv` and project-local frontend dependencies from locks.
- Copy `.env.example` to `.env`; replace local DB credentials for any networked service.
- Start PostgreSQL with pgvector and Redis, apply migrations, create artifact paths
  with correct permissions and load an approved corpus manifest.
- Select/pin text, reranker and optional visual model checkpoints; review licenses,
  download weights to ignored local cache and verify hardware capacity.
- Choose LLM provider/model and supply its key if generation is enabled; agree to
  any source-content egress. Disabled provider mode is not a full answer demo.
- Configure parser backend, BM25 snapshot location, worker concurrency, upload limits,
  revision metadata, unit policy and reviewed graph annotations.
- For cloud: AWS account, region, billing alarms/quotas, least-privilege IAM, private
  artifact bucket, TLS/domain, authentication secrets, network rules and backup policy.
- Configure OTLP destination if tracing is enabled; redact content and verify export.
- Run complete tests/build and real DB, Redis, provider, artifact and HTTP smoke tests.
- Execute backup restoration and deletion/cache invalidation tests before opening access.

## Operations and recovery
Proposed demo targets: daily DB/artifact manifest backups, RPO ≤24 h and RTO ≤4 h,
verified by restoration rather than claimed from configuration. Artifacts referenced
by snapshots must be backed up consistently. Keep previous app image and published
snapshot; retain backup keys securely. Monitor queue age, job failures, provider
error rate, query p95, disk free space and spend. Alert at 50/80/100% budget, with
hard model request stop at the cap. A read-only precomputed demo is the fallback
when a provider or budget is unavailable; clearly label cached demonstration answers.
