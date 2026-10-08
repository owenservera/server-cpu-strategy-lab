# Research Database v1 — reproducible local seed

**Status (2026-10-08): implemented SQLite prototype and deterministic repository import, not a deployed multi-user production service.** The Git research corpus remains the authoritative publication/review workflow until a migration is explicitly approved. A future PostgreSQL service can become the transactional source of truth when collaboration and ingestion volume require it.

Start with [DB design](design/ARCHITECTURE.md) and [accounting invariants](design/INVARIANTS.md). For new sources, still start from [RESEARCH-ENTRY.md](../RESEARCH-ENTRY.md): research packets are staged, not accepted as fact by mere ingestion.

## What the database actually does

- Maintains source provenance, immutable-at-ID attributed claims, source locators and file digests.
- Splits *measurements* from dated *forecasts* and *synthetic scenario calculations*.
- Tracks metrics/units, market boundary, population/denominator and fiscal/calendar period.
- Holds a multi-axis, hierarchical buyer/channel/workload/ISA/location taxonomy; buyers and sales channels are **not** two independent markets.
- Provides typed entities, relationships, review events, conflicts, questions, cross-evidence links and allocation frames.
- Seeds from the **existing** repository datasets (no manually recopied figures); flags legacy source quality and retains original record IDs.
- Supports repeatable local exports for a future dashboard backend adapter, with evidence statuses retained.
- Validates allocation sums, provenance FKs, scenario identities and revenue-workload reconciliation.

## Quick start (Windows PowerShell / macOS / Linux)

Requires **Python 3.11+** with a bundled **SQLite 3.37+**; no pip dependencies, Docker or credentials. The original dashboard still runs without Python.

```powershell
python db/scripts/research_db.py seed
python db/scripts/research_db.py verify
python db/scripts/research_db.py stats
python db/scripts/research_db.py export
python -m unittest discover -s db/tests -v
```

The default local DB file is `db/runtime/research.sqlite`; the export is `db/runtime/research_snapshot.json`. Both are **generated**, gitignored, and never carry private material. Use `--db C:\path\to\research.sqlite` and `--root C:\path\to\repo` as appropriate. The app is **not yet wired** to this export; the existing static UI is unaffected.

A safe read-only query:

```powershell
python db/scripts/research_db.py query --sql "SELECT * FROM v_forecast_history ORDER BY issued_at"
```

To rebuild from scratch, archive your local file if it contains any independently reviewed changes, then delete *only the generated SQLite file* and rerun `seed`. Do not overwrite an actively curated production DB this way.

## Database directory

```text
db/
  migrations/       0001_core.sql and 0002_views.sql; additive, checksummed
  seed/             foundation.json taxonomy; import reads existing data/*
  scripts/          research_db.py loader, validation and static export
  tests/            SQLite fixture-based regression tests
  design/           schema semantics, accounting, evolution/operating plan
  examples/         read-only queries demonstrating evidence-safe slicing
  runtime/          generated only; ignored by Git
```

## Current seed lineage

| Existing repo data | v1 destination | Treatment |
|---|---|---|
| `data/demand-2030/source-registry.json` | `source_documents` | Indexed, **not blindly verified** |
| `historical-and-forecast-evidence.csv` | `measurements` **or** `forecast_vintages` + `forecasts` | Prevent forward-looking IDC estimates becoming observed history |
| `tam-forecast-vintages.csv` | `forecast_vintages` + `forecasts` | Keeps each 2030 estimate and original qualifier (`>` vs `≈`) |
| `scenario-model.json` | `calculation_models`, `model_runs`, `model_inputs`, `model_outputs` | Explicit synthetic runs, separate from reported observations; blank unknown 2025 ISA shares |
| AMD keynote curated claims, strategic signals, numeric anchors | `source_documents`, `source_locators`, `evidence_claims` | Original line pointers; **vendor/transcript assertions only** |
| Microsoft/Docker claim/signal index | `source_documents`, `source_locators`, `evidence_claims` | No invented portable transcript URL; local-pointer-unavailable provenance |
| `priority-data-fields.json` top 15 | `research_questions` | P0 open acquisition targets, not market values |
| `docs/research/demand-2030/...` IDC source conflict | `conflicts` | Open, **not** reconciled |

No original dataset is overwritten, deprecated or converted into a verified fact during seeding. The immutable-at-ID loader refuses to rewrite a sourced row when its numerical value or definition changes; a future importer needs a reviewed new vintage/revision. New unchanged rows in an updated file can be added without treating the changed file checksum as a change to every previous row.

## Modeling micro and macro together

Micro task measurements belong in `measurements` with `expected_boundary='workload'` and **successfully completed task denominator**. Macro Intel/AMD socket, system, revenue and ASP data are separate metrics. A model run bridges **completed tasks → core-seconds → required provisioned cores → incremental sockets → CPU silicon revenue**, carrying every empirical coefficient/assumption via `model_inputs` and `model_dependencies`. Never compute a new physical socket from a task event without deducting available fleet capacity and accounting for utilization, placement, CPU density and Arm substitution.

The v1 schema provides the tables and integrity rails for that workflow; the independent workload benchmark ETL and the live model execution API are **not implemented** yet. Future measurements must be staged and reviewed before inclusion in a model.

## Next gates

1. Verify the full repository seed in your environment/CI; the unit suite uses representative fixtures, not the paid-source originals.
2. Build research-packet ingestion and an editor/reviewer API with append-only approvals.
3. Add dimensional query compiler with hierarchy-safe aggregation and release/vintage snapshots.
4. Add executable model engines with Decimal values, uncertainty intervals and evidence lineage.
5. Promote PostgreSQL only when there is an actual concurrent-writing/multi-user requirement. See [evolution plan](design/EVOLUTION.md).
