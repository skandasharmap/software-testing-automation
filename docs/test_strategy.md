# Test Strategy

- **Design techniques**: Equivalence Partitioning, Boundary Value Analysis, Decision Tables.
- **API testing**: Positive/negative paths, HTTP codes, idempotency, concurrency (reserve/release).
- **Contract checks**: Validate response bodies against Pydantic schemas.
- **Performance**: RPS baseline, latency p95.
- **Security**: Static scan (Bandit), ZAP baseline (manual or pipeline step).
