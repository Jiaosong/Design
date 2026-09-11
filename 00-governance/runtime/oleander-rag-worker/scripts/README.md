# RAG bootstrap invariant

`metadata-indexes.txt` is declarative evidence for the required ten Vectorize metadata indexes.

Do not run any backfill until the deployed index confirms all ten fields exist. Cloudflare does not retroactively add previously inserted vectors to a newly created metadata index; a late metadata-index change therefore requires re-upsert/reindex.

Production bootstrap remains HOLD until Cloudflare account bindings are available and actual resource readback verifies:

- D1 database exists and schema is applied;
- Queue producer/consumer are bound;
- Vectorize index dimensions match the selected embedding model output;
- all ten metadata indexes exist;
- Worker secrets are configured outside Git;
- `/health` and a bounded shadow retrieval succeed.
