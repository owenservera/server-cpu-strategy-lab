# Research Database: Architecture & v1 bootstrap (2026-10-08)

**Decision:** Start with a local **SQLite 3.37+** evidence warehouse and move to PostgreSQL when simultaneous remote writers, reviewer transactions, or hosted APIs actually require it. The existing [public research intake protocol](../../RESEARCH-ENTRY.md) and Git files remain the publication/review authority until a deliberate database cutover.

## Where to start

1. [Architecture and ERD](ARCHITECTURE-V1.md) — source provenance, typed evidence, multi-axis market taxonomy and synthetic models.
2. [Segmentation and modeling contract](SEGMENTATION-AND-MODELS.md) — how micro task telemetry, macro CPU data and 2030 hypotheses can be reconciled without double counting.
3. [Implementation and seed handoff](IMPLEMENTATION-HANDOFF.md) — tested local ZIP, CLI, migration gates and downstream frontend contract.
4. [Existing buyer/channel taxonomy](../research/demand-2030/TAXONOMY-AND-ACCOUNTING.md) and [data dictionaries](../research/demand-2030/DATA-DICTIONARY-AND-GAPS.md).

The complete original implementation is **now committed unchanged under [`db/`](../../db/)** as of [commit `971a24d`](https://github.com/owenservera/server-cpu-strategy-lab/commit/971a24d3e94f03ec8a2280e07679d6e4a018ad30). All 12 file Git blobs were hash-checked against the archive. **No ZIP extraction is needed.** The local ZCode team must now execute the [full wiring assessment](ZCODE-FULL-WIRING-ASSESSMENT.md) using the [single bootstrap prompt](ZCODE-BOOTSTRAP-PROMPT.md); the real-corpus seed, CI run, packet promotion and dashboard integration are separate gates.

## Financial filings extension

The additive [financial-disclosure program](../research/financial-filings/README.md) now introduces `db/migrations/0003_financial_filings.sql`, a [35-issuer collection watchlist](../../data/financial-filings/issuer-watchlist.json), an SEC submissions metadata discovery helper and a staged financial JSON intake command. It maps reported facts to the **existing** canonical `measurements` rows and stores contracts, liabilities, RPO/backlog and proposed model mappings separately to avoid double counting. The watchlist is not an already-acquired financial corpus; no historical issuer fact should be presumed loaded. See [database implementation](../../db/README.md) for commands. Full ETL automation, reviewed actual numbers and frontend wiring remain separate gates.

## Seed origin and scope

- `data/demand-2030/source-registry.json` → source metadata, legal/access flags and lineage.
- `historical-and-forecast-evidence.csv` → measured/reported records **or** forecast records according to source status.
- `tam-forecast-vintages.csv` → distinct issuer/date/target-period forecasts; `greater_than` remains a lower bound.
- `scenario-model.json` → explicitly **synthetic** model runs; not history. 2025 architecture shares remain NULL.
- AMD keynote, Microsoft/Docker claim corpora and numeric anchors → attributed, unverified claims and source locators, **not automatically verified numbers**.
- The P0 data gaps and IDC 2024 source-vintage disagreement → open questions/conflict records.

Do not import confidential consulting material, assume paywalled-source access, or commit generated SQLite files. Browser consumers only receive read-only, status-labeled snapshots; no raw DB connection or unreviewed claims.

## Minimal commands

From a checkout containing `db/` (Python 3.11+ with SQLite 3.37+, no pip dependencies):

```powershell
python db/scripts/research_db.py seed
python db/scripts/research_db.py verify
python db/scripts/research_db.py stats
python db/scripts/research_db.py export
python -m unittest discover -s db/tests -v
```

The database and JSON export are generated under `db/runtime/`, which must be gitignored. Keep the current static dashboard deploy independent of this experimental backend.

**v1 acceptance:** source identity and immutable legacy refs; no observation/forecast/scenario conflation; fiscal vs calendar periods; scope/metric accounting boundaries; partition shares sum to 1; observed values are not invented; user-controlled scenario outputs always labeled synthetic.
