# Implementation handoff: database v1

**Bundle already imported:** All 12 tested source files are now committed under [`db/`](../../db/) on `main`, byte-identical to the archive, in [commit `971a24d`](https://github.com/owenservera/server-cpu-strategy-lab/commit/971a24d3e94f03ec8a2280e07679d6e4a018ad30). **Do not import/extract again.** This file preserves the historical original handoff; the current implementation plan is [ZCode full wiring assessment](ZCODE-FULL-WIRING-ASSESSMENT.md) plus [bootstrap prompt](ZCODE-BOOTSTRAP-PROMPT.md).

## Exact delivery steps

1. Confirm current `main` contains source commit `971a24d` and preserve active local work; short-lived worktrees may be used.
2. **Already completed:** The 12 original source files are present in `db/` and were blob-hash verified; do not extract a separate ZIP.
3. **Already completed:** `.gitignore` excludes `db/runtime/`, `*.sqlite`, `*.sqlite-shm` and `*.sqlite-wal`.
4. Run `python -m unittest discover -s db/tests -v` with Python 3.11+ (SQLite 3.37+). The earlier isolated fixture suite passed 7 tests.
5. Run `python db/scripts/research_db.py seed`, `verify`, `stats`, `export` **on actual repository sources**. If import fails on an evidence-ID collision, **investigate and preserve the source/vintage**, do not replace immutable values or skip constraints.
6. Check seed record counts against the live corpus, model sum-to-total identity, partition ISA shares = 1, open IDC 2024 conflict, forecast vintage count and source access flags. Current known legacy corpus includes 41 mixed observed/forward rows, 9 TAM forecast vintages, 97 AMD numeric claims, 38 AMD strategic signals and 19+11 Microsoft/Docker claim/signal entries.
7. **CI workflow added:** `.github/workflows/database-ci.yml` runs Python 3.11 fixture tests, full Git corpus seed, verify, export and data-class checks. Check its actual run conclusion, diagnose any failure and add Windows replication; do not infer a green CI from the workflow file alone. Add npm aliases only if they do not require Python for `npm start`.
8. Source code is already committed to `main`. ZCode must now push **verified wiring fixes**, report actual source counts and test/CI evidence; keep the static dashboard working independently.

## Seed behavior and constraints

`source_documents` includes public, public-secondary, paywalled-unverified and local-pointer-unavailable statuses. Vendor benchmarks and transcript numbers remain `evidence_claims`, not independently observed measurements. Forward-looking IDC/analyst data populate `forecasts` (not historical observations). 2030 trajectories are stored only in synthetic model runs; null missing 2025 ISA shares are preserved. The importer won't rewrite an old sourced value under the same key unless a reviewed migration makes a new record/vintage.

## V1 source and review boundaries

Git CSV/JSON and `research/packets/` remain review/publishing authority. SQLite is a reproducible local read model, not the multiuser source of truth yet. Do **not** claim ingestion API, automatic packet promotion, RLS, production PostgreSQL, CI success, or live dashboard DB integration without evidence and tests.

## Next after import

Implement a packet-to-database adapter with a **staging transaction** and independent human review; then build read-only parametrized segmentation queries with market-boundary validation, task-level benchmark telemetry, versioned model runs and provenance graph exploration. PostgreSQL transition follows only after operational concurrency is needed.
