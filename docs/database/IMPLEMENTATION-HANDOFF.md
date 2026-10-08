# Implementation handoff: database v1

**Package:** `server-cpu-research-db-v1.zip`, generated and regression-tested in the ChatGPT session on 2026-10-08. The ZIP is a **user-downloadable artifact from that conversation**; it is not yet a publicly hosted GitHub release. The repository contains this canonical design/spec. The local agent must add the ZIP's `db/` directory as source files to `main` (after comparing with current main), not treat the ZIP as an authoritative database containing private data.

## Exact delivery steps

1. Confirm current clean `main` and save local agent work; use a short-lived worktree if required.
2. Extract `server-cpu-research-db-v1.zip` at repository root. The archive paths begin with `db/` and contain **12 source files**: core/view SQL migrations, seed ontology JSON, Python CLI importer, unittest suite, architecture/evolution/invariant/API docs and example queries.
3. Merge `.gitignore.part` rules manually: `db/runtime/`, `*.sqlite`, `*.sqlite-shm`, `*.sqlite-wal`. No generated SQLite/JSON snapshot committed.
4. Run `python -m unittest discover -s db/tests -v` with Python 3.11+ (SQLite 3.37+). The earlier isolated fixture suite passed 7 tests.
5. Run `python db/scripts/research_db.py seed`, `verify`, `stats`, `export` **on actual repository sources**. If import fails on an evidence-ID collision, **investigate and preserve the source/vintage**, do not replace immutable values or skip constraints.
6. Check seed record counts against the live corpus, model sum-to-total identity, partition ISA shares = 1, open IDC 2024 conflict, forecast vintage count and source access flags. Current known legacy corpus includes 41 mixed observed/forward rows, 9 TAM forecast vintages, 97 AMD numeric claims, 38 AMD strategic signals and 19+11 Microsoft/Docker claim/signal entries.
7. Add `db/tests` to CI with Python setup and the `seed → verify → export` smoke test, separate from GitHub Pages permissions. Add scripts to `package.json` only if doing so doesn't introduce a hidden Python runtime requirement for `npm start`.
8. Commit to `main`, report SHA and show seeded counts + test output. The existing static dashboard must remain operational and not depend on database availability.

## Seed behavior and constraints

`source_documents` includes public, public-secondary, paywalled-unverified and local-pointer-unavailable statuses. Vendor benchmarks and transcript numbers remain `evidence_claims`, not independently observed measurements. Forward-looking IDC/analyst data populate `forecasts` (not historical observations). 2030 trajectories are stored only in synthetic model runs; null missing 2025 ISA shares are preserved. The importer won't rewrite an old sourced value under the same key unless a reviewed migration makes a new record/vintage.

## V1 source and review boundaries

Git CSV/JSON and `research/packets/` remain review/publishing authority. SQLite is a reproducible local read model, not the multiuser source of truth yet. Do **not** claim ingestion API, automatic packet promotion, RLS, production PostgreSQL, CI success, or live dashboard DB integration without evidence and tests.

## Next after import

Implement a packet-to-database adapter with a **staging transaction** and independent human review; then build read-only parametrized segmentation queries with market-boundary validation, task-level benchmark telemetry, versioned model runs and provenance graph exploration. PostgreSQL transition follows only after operational concurrency is needed.
