# Evolution plan: from Git-derived SQLite mirror to collaborative market-model service

## Stage 0 — current v1 (now)

- Commit the SQL migrations, canonical taxonomy seed, import CLI and tests.
- Keep published Git CSV/JSON **authoritative**, SQLite as reproducible analytical mirror.
- Verify the real corpus seed on a developer machine/CI; the fixture tests independently validate behavior, not each legacy market figure.
- Make read-only static export available with source/vintage/status. Do not switch frontend dashboards to unreviewed database tables.

## Stage 1 — transactional ingestion + reviewer promotion

- Build packet-to-DB normalizer from [research/schema/packet.schema.json](../../research/schema/packet.schema.json); stage everything in `ingestion_batches` and `evidence_claims`.
- Add `promotion_decisions` with reviewer, timestamp, rationale, source licenses and scope/denominator review. Only approved facts appear in `approved_market_observations` materialization.
- Deduplicate via canonical source URL/publisher/issue date/content hash and exact metric population + period + qualifier; preserve independent claims as separate source assertions.
- Add unit ontology and conversions (USD millions vs billions, currency time series, nominal vs real), materialized market facts and confidence scores with calibrated standards.
- Add true physical procurement events and allocation evidence (buyer, OEM/ODM channel, seller, location, socket count, actual architecture). Explicitly represent beneficiary vs asset owner.
- Preserve all source and model version history; never mutate a forecast vintage because a company raised its guidance.

## Stage 2 — quantitative market research engine

- Define comparable segment-population `segment_universe` rules, temporal hierarchy versions and hierarchy-safe query planner.
- Add reusable statistical series indexed by source, metric, period, cohort, provenance and revision; cross-validation against independent sources.
- Instrument benchmark tasks (successful agent workflows, core-seconds, RAM, watts, isolation mode, environment, task success, sample count). Sample/trial records remain separate from interpreted conclusions.
- Implement model expressions and unit-typed DAGs with immutable calculation-run manifests, inputs with uncertainty ranges, uncertainty propagation and scenario forks.
- Partition monthly CPU demand by *final hardware owner* and add observed/inferred capacity reuse, local/cloud displacement and x86/Arm switching.
- Materialize scenario confidence intervals and sensitivity/tornado input multipliers. Run `model total = compatible, disjoint segments` checks every build.

## Stage 3 — PostgreSQL service trigger

Move when one or more are actually true: multiple researchers/agents concurrently write and review; authenticated remote queries are needed; packet volume makes SQLite write locks operationally expensive; or background real-time jobs must update shared tables. **Do not migrate solely because PostgreSQL sounds more professional.**

Suggested stack: PostgreSQL 16/17 with `NUMERIC` for Decimal, normalized provenance tables, `JSONB` for high-variance append-only payloads, indexed foreign keys and full-text search. Use one write API with transactions and row-level security; optional object store for licensed and permissioned source blobs, **never a public raw-transcript repository**. Heavy analytical scans can use DuckDB/Parquet exports independently. Add pgvector only if actual semantic cross-source retrieval proves useful; a knowledge graph does not automatically need a graph DB.

### Migration contract

1. Freeze a corpus release hash and source snapshots; export v1 tables and full legacy ref/lineage map.
2. Define PostgreSQL migrations for all typed entities, preserving stable IDs and the exact source/forecast/segment date+scope keys.
3. Translate SQLite `STRICT`/`CHECK` to PostgreSQL enums/check constraints, `TEXT` decimal to `NUMERIC(p,s)` with documented bounds; special handling for ultra-large token counts and rare fractional ratios.
4. Backfill **including all prior forecast vintages and staged records**, not just approved/recent entries.
5. Dual-run validation on both DBs: entity counts, source hashes, ISO dates, partition sums, model outputs, counterexample test queries and query results.
6. Promote PostgreSQL as writer only after a cutover gate; disable SQLite writer, keep it as a disposable local snapshot; remove dual-write after reconciliation.
7. Version the public dashboard snapshot contract independently so the frontend deployment doesn't break during the cutover.

## Explicit non-goals for v1

No crawler, real-time external data feed, hosted DB, vector embeddings, auto-generated 2030 market forecast, human identities, paywalled source replication, background monitoring or schema-free EAV dumping ground. We need accurate source and accounting semantics before sophisticated infrastructure.
