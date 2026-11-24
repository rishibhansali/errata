# Build Errata while learning it

Rishi owns the project and should be able to explain, run and modify its core paths.
The assistant writes code, but every phase includes an explanation, a reproducible
exercise and a reviewable change. Do not hide decisions behind a framework.

## Session agreement
1. Start with the feature's purpose and a tiny example using actual project concepts.
2. Explain prerequisites and two relevant tradeoffs before introducing a dependency.
3. Implement one small slice on a descriptive branch; keep commits readable.
4. Walk through entrypoint → domain logic → storage/provider → output. Explain types,
   failure paths, tests and why the code is arranged this way.
5. Rishi runs a command or changes a small parameter and predicts the result first.
6. Save a concise walkthrough under `docs/learning/` when implementation starts:
   concepts, file/line links, commands, expected observations and unresolved questions.
7. End with what works, what is still uncertain and what the next slice teaches.

No quizzes are mandatory. If a concept is unfamiliar, explain it without assuming
prior SQL, ML or deployment experience. Prefer short working examples to long theory.
Owner approval is required before implementation begins; each lesson can be paced
slower without sacrificing correctness. Do not claim Rishi reviewed code or completed
an exercise unless he actually did.

| Phase | Learn | Hands-on exercise | Understanding checkpoint |
|---|---|---|---|
| Setup | Git commits/branches, environments, secrets and documentation | Clone, create venv, run docs check; inspect commit diff | Explain tracked vs ignored files |
| Week 1 | HTTP, FastAPI/Pydantic, SQL PK/FK, migrations, queues | Upload fixture, inspect job and page rows, kill/restart worker | Explain why a queue message is not the durable job |
| Week 2 | Chunking, embeddings, cosine similarity, BM25, rank fusion | Run keyword/dense searches separately and inspect top results | Explain why exact part numbers and semantic queries differ |
| Week 3 | Provider interfaces, schema validation, units, claims and caching | Change requested unit; inspect numeric trace and evidence IDs | Distinguish generation from deterministic calculation |
| Week 4 | Pixel/data transforms, interpolation, uncertainty and applicability | Calibrate a graph and compare a point; change temperature filter | Explain why plot precision and conditions limit an answer |
| Week 5 | Ground truth, splits, leakage, retrieval metrics and ablations | Hand-compute Recall@5/MRR for one query; review one label | Explain why a good answer can still have a bad citation |
| Week 6 | Traces, p95, budgets, CI, containers and restore | Trace slow query, reproduce report, restore test snapshot | Explain what must pass before a release |

## Vector database lesson sequence
1. Store three text snippets and their source IDs in PostgreSQL before adding vectors.
2. Illustrate a vector as a list of numbers; manually compare two tiny vectors using
   dot product and cosine similarity. Explain that similarity is not truth.
3. Generate embeddings with a pinned model and store dimension/model metadata.
4. Query exact nearest neighbors in pgvector and inspect distances and evidence IDs.
5. Add document-family/revision filters and demonstrate why the same filters must
   apply to keyword and vector search.
6. Compare BM25 rankings; combine rank positions with RRF instead of adding unrelated
   raw scores. Inspect a failure where the exact part number matters.
7. Add a cross-encoder and inspect which candidates it promotes or drops.
8. Only then compare exact search with HNSW: latency, memory, build time and Recall@K.
   Use EXPLAIN ANALYZE and repeat with restrictive filters.
9. Demonstrate an embedding-model upgrade with a separate index and atomic snapshot
   switch; old dimensions are not interchangeable with the new model.

Primary reading, introduced at the relevant lesson:
[PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html),
[pgvector](https://github.com/pgvector/pgvector),
[FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/),
[Pydantic](https://docs.pydantic.dev/latest/),
[PyTorch basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html),
[OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/).
These are reading references, not installed dependencies or completed lessons.

## Review prompts
Can I locate the source of this number? Which code rejects incompatible units?
What changes if the source revision changes? What happens when the provider is down?
Which benchmark demonstrates improvement? Can I reproduce that run? If any answer
is unclear, the next walkthrough should follow that path before expanding the feature.
