# Production Deployment HOLD

Repository implementation is not production deployment.

Release condition:

1. Cloudflare account execution surface is connected and authorized.
2. D1 / Queue / Vectorize / Worker resources are created and read back.
3. Vectorize dimensions are verified from an actual Workers AI embedding response before index creation/finalization.
4. All required metadata indexes exist before backfill.
5. Notion webhook signature validation succeeds with the real webhook secret.
6. CURRENT+DEFAULT shadow backfill completes without canonical collision or authority violation.
7. Golden Set authority violations = 0 and retrieval quality targets are evaluated.
8. Direct Notion retrieval vs RAG dual-read shows no material authority regression.
9. Existing OLEANDER anti-pollution/runtime gates pass on the same implementation head.

Until then:

`IMPLEMENTED_IN_REPO != DEPLOYED != SHADOW_PASS != DEFAULT_RETRIEVAL_CURRENT`.
