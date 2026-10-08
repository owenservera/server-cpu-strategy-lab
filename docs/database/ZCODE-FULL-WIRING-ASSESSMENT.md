# ZCode integration assessment — database v1 through an operational evidence pipeline

**Date:** 2026-10-08 · **Status:** technical assessment and ordered execution gates · **Target:** Windows-first ZCode agent team, single consolidated `main`.  
**Starting commit:** [971a24d](https://github.com/owenservera/server-cpu-strategy-lab/commit/971a24d3e94f03ec8a2280e07679d6e4a018ad30) contains all twelve `db/` source files **byte-for-byte identical** to the v1 ZIP (checked against Git object hashes). Do not re-extract or rewrite the bundle.  
**Governing entry:** [AGENTS.md](../../AGENTS.md), [RESEARCH-ENTRY.md](../../RESEARCH-ENTRY.md), [intake and promotion](../../research/INTAKE-AND-PROMOTION.md), [DB invariants](../../db/design/INVARIANTS.md).  
**Do not confuse:** `docs/database/` captures the architecture/design; `db/` now contains the actual runnable implementation. This document is a work-order/assessment, not proof of completed integration.

## 1. Verified starting point versus uncompleted wiring

| Component | Evidence / implementation now | Status and next gate |
| --- | --- | --- |
| Source code and migrations | `db/migrations/0001_core.sql`, `0002_views.sql`, `db/scripts/research_db.py`, `db/seed/foundation.json`, tests/docs | **Committed unchanged**, hashes checked |
| Relational evidence model | 31 tables, 4 read-only views; sources/claims/measurements/forecast vintages/taxonomy/model runs/graph/review scaffolding | **Schema exists**, not all tables populated or operational |
| Local Python SQLite prototype | Python stdlib only; SQLite >=3.37; `seed, verify, stats, export, query` commands | **Construction fixture passed seven tests**, not proof against latest full checkout |
| Default repository source imports | Registry, 41 mixed historical/forecast rows, 9 TAM vintage rows, 97+38 AMD items, 19+11 Microsoft/Docker items, priority questions, synthetic 2030 runs | **Importer code exists**, latest `main` full-seed results unverified |
| Existing Git research intake | `AGENTS.md`, `RESEARCH-ENTRY.md`, `research/routes.json`, packet schema, catalog | **Documented and partly validated**; **no general packet-to-DB writer** |
| Approval/review | `review_events`, `knowledge_edges`, `conflicts` schema and quality flags | **Storage scaffolding**; **no implemented reviewer/promotion service** |
| Market segmentation | Buyer/channel/workload/ISA taxonomy and scope tables; checked x86/non-x86 scenario splits | **Seeded vocabulary exists**; **not yet a general additive query planner** |
| Agent workload telemetry | Core-seconds, successful workflow, sandbox isolation test designs | **Experimental specification only**, no verified benchmark ingestion |
| Executable market modeling | Existing authored synthetic `scenario-model.json` seeded into model runs/outputs | **Stores scenarios but does not execute or recalibrate forecast DAGs** |
| Dashboard/publication | `db export` writes `db/runtime/research_snapshot.json`; old static frontend still uses `data.js` | **Not wired**; do not publish raw SQLite or unreviewed data |
| CI/Windows replication | Node tests and Pages workflows exist, plus Python DB fixture tests | **DB-specific CI / latest full real-corpus import not confirmed** |
| Multiuser remote operations | No hosted DB/API, no auth/RLS, no cross-machine editor workflow | **Future capability**; do not deploy PostgreSQL prematurely |

### Immediate findings that must shape the work

- **Git is still the review/publication source of truth.** SQLite is a reproducible read model and evidence warehouse; no automatic DB write-back to `data/` or web app. Establish a deliberate authority transition later, never accidental dual masters.
- **One source can create many heterogeneous records.** The 19 routes in `research/routes.json` must fan out to typed tables. Only the legacy corpus sources currently have specialized import paths.
- **Schema breadth ≠ implementation coverage.** `entities`, `entity_relationships`, `scope_dimensions`, `model_dependencies`, `review_events` and other advanced tables exist but are not made operational by current legacy seed. Do not label those features complete.
- **A source registry is not source verification.** Legacy market rows are largely `attributed_unverified`; imported estimates must retain publisher/access status, qualifiers and period.
- **Model-vintage drift is intentional.** AMD >$200B keynote, later >$220B, reported bank ~$300B scenarios must remain independent forecast vintages; `greater_than` is a mathematical bound, not a point estimate.
- **Do not blend economic boundaries.** IDC whole-server system spend, EPYC CPU revenue, AMD Data Center CPU+GPU segment, CPU silicon TAM, hyperscaler capex, GPU rack value and cloud services are different populations.
- **Transaction and safety review needed.** `seed` calls `init` before its own data transaction; bulk imports are transactional but schema migration commits are separate. Do not silently re-run/overwrite a curated production SQLite file.
- **Value precision is protected, dimensional aggregation isn't automatic.** Decimal strings preserve numerical values; arbitrary SQL `SUM` across unrelated scoped records would still be analytically invalid without query-planner checks.
- **Generated export is not a safe published dataset by itself.** `exports()` includes attributed measurements, vendor forecasts and unresolved conflicts; any public dashboard adapter must explicitly filter and label each class, or use reviewer-approved materialized views.
- **The local Windows environment must be probed, not assumed.** Test whichever Python executable/SQLite build ZCode actually uses; don't assume Linux, Docker, WSL, a running database service or remote secrets.

## 2. Ordered deliverables with dependencies and completion gates

Each deliverable must create an inspectable artifact/log and merge a small, tested change to `main`. Keep short-lived implementation worktrees only.

### D0 — Reconcile main and preserve local work (blocking)

Owner: ZCode coordinator.

1. `git fetch origin`; inspect `git status --short`, `git rev-parse HEAD`, `git rev-parse origin/main`; inventory active ZCode/OpenCode/Codex worktrees. **Do not discard uncommitted changes or reset local agent work.**
2. Verify the twelve `db/` files are present at or after `971a24d`. Confirm `.gitignore` already excludes `db/runtime/`, `*.sqlite`, `*.sqlite-shm`, `*.sqlite-wal`.
3. Read `db/README.md`, all four `db/design` guides, `docs/database/README.md`, `research/INTAKE-AND-PROMOTION.md` and this document. Register owner, scope, start time, intended files and blockers in the team's work log/issue.
4. Preserve the original `db/` files as a verified immutable baseline; implement changes only with explicit follow-on commits after baseline testing.

**Gate:** local HEAD sync disposition recorded; no dirty files lost; identical database source tree acknowledged.

### D1 — Windows environmental and fixture baseline (blocking)

Owner: DB engineer + QA.

On PowerShell at repository root:

```powershell
git status --short
py -3.11 -c "import sys, sqlite3; print(sys.version); print(sqlite3.sqlite_version)"
py -3.11 -m unittest discover -s db/tests -v
```

If the launcher `py -3.11` is unavailable, use an installed `python` with version >=3.11 and SQLite >=3.37. Do not install WSL, Docker, a hosted DB or unrelated packages. Record executable path, versions, 7-test result and elapsed time.

**Gate:** fixture suite passes on target machine; any failure gets a minimal reproducer and a distinct fix commit. Do not silently weaken assertions.

### D2 — Full live-corpus seed, semantic QA and reproducible ledger (blocking)

Owner: DB engineer + research/evidence reviewer.

```powershell
py -3.11 db/scripts/research_db.py seed
py -3.11 db/scripts/research_db.py verify
py -3.11 db/scripts/research_db.py stats
py -3.11 db/scripts/research_db.py export
py -3.11 db/scripts/research_db.py query --sql "SELECT COUNT(*) AS count FROM v_forecast_history"
```

Use `--root` and `--db` when necessary. Review `db/runtime/research.sqlite` locally (gitignored). Capture a machine-readable `db/runtime/seed-audit.json` or equivalent containing: git SHA, Python/SQLite versions, input digest inventory, DB schema version, counts by table and verification status, and explicit unsupported/missing records. Keep the audited *summary* in a review report and the raw generated DB private/local. Test idempotent re-seeding against unchanged files. Test that changing a sourced value under an existing ID **fails** instead of silently replacing it; do this in a disposable fixture, not production data.

Expected input inventory, **not pre-asserted live DB counts**: 41 historical/forward evidence rows, 9 TAM vintages, 97 quantitative + 38 strategic AMD items, 19 numeric + 11 strategic Microsoft/Docker records, and 50 research priority fields (first 15 imported as P0 questions). Classify all forward-looking entries as `forecasts`, NOT historical observations; ensure 2025 actual architecture split is missing/NULL; keep IDC 2024 vintage conflict open.

**Gate:** `DB_VALIDATE_PASS` on the current real corpus; recorded and reviewed count reconciliation, stable second seed, no unregistered source IDs or incoherent scope boundaries. Any source conflicts go to a review queue, not `INSERT OR REPLACE`.

### D3 — Isolated database CI / portability (can parallelize with D2)

Owner: QA/CI.

Set up/check a separate `database-ci.yml` with `actions/setup-python` and no npm or GitHub Pages permissions beyond `contents: read`. Run fixture tests + clean DB seed + verify + stats + export, assert source/vintage counts and that no generated DB files were committed. Trigger on `db/**`, relevant `data/**`, and DB workflow changes. Add Windows smoke test only if runners are available; do not infer that successful Linux Python tests prove Windows ZCode installation.

**Gate:** explicitly confirmed green DB CI run on a commit that contains full source data. The existing Pages and Node workflow failures are tracked independently; do not claim all project CI is green if DB only passes.

### D4 — Public-research packet → staging database ingestion (core missing plumbing)

Owner: ingestion engineer + evidence reviewer. Requires D2.

Implement adapter to parse the **existing** `research/schema/packet.schema.json`; call `npm run check:research` first. Support every of the 19 route types by mapping to typed destination, or return a structured `unsupported_route` without dropping records. Source identity = publisher + canonical URI + document version/publication date (plus hash if available). Stage new sources, locators, speaker claims, measurements, forecasts, entities, relationships, research questions, conflicts and methods under one `ingestion_batches` record. Deduplicate by semantic identity and existing `legacy_links`, not just title or matching numeric value.

Preserve original source and claim IDs and exact line/page/video locators. An updated report is a **new vintage**; independent corroboration is a **new source claim** linked to prior, not an overwrite. Staged numeric claims must not be auto-populated into observed `measurements`.

**Gate:** ingest same test packet twice without duplicates; ingest a changed forecast to create a new vintage; ingest a contradictory claim preserving both sides; unknown route produces explicit actionable error; malicious/restricted material blocked before persistence or public output. Add deterministic fixture tests.

### D5 — Human review, promotion and provenance APIs (core missing plumbing)

Owner: research/evidence reviewer + backend engineer. Requires D4.

Define explicit state machine: `discovered → extracted → checked_against_original → reviewed → approved/promoted`, plus `rejected`, `superseded`, `conflicted`, `not_comparable`. Implement append-only `review_events` (who, when, reason, evidence, old/new references) and reviewer-only writes to accepted analytical tables. Don't let model agents silently self-approve independent verification. Every published measurement must have metric, unit, numerator/denominator, market boundary, calendar/fiscal period, source URL, confidence/review status and exact reference locator.

Provide CLI commands first; defer network API and credentials until the local workflow is stable. Keep feedback to original Git packet review status explicit; avoid divergent dual-write authority. Publication should be a deterministic, reproducible operation.

**Gate:** unreviewed items excluded from `approved` view; promotions are auditable; rejected/corrected claims retain lineage; last publisher/source timestamp visible; rollback via new review event rather than deleting historical facts.

### D6 — Safe query layer, segmentation cube and browser data boundary

Owner: data/analytics engineer + frontend engineer. Requires D2; publication quality requires D5.

Introduce allowlisted **typed** measures and aggregation rules: buyer (economic hardware owner) × procurement channel (OEM/ODM) × workload × CPU ISA × region × year × fiscal/calendar period. Add `scope_dimensions` and complete *disjoint* `partition_frames`; a hierarchy membership is not proof of additivity. Verify one physical CPU purchase has one economic buyer and one procurement channel; a model lab renting a neocloud GPU is a service user, not an additional chip buyer.

Generate read-only, **approved-data-only** static JSON during a build step, independent of `npm start`; do not publicly serve `db/runtime/research.sqlite` or raw `research_snapshot.json` without approval filters. Wire a data adapter to existing dashboard `app.js` and `data.js`, preserving offline/static fallback. Provide evidence/source drawer, explicit nulls, temporal vintage dropdown and `vendor_claim/actual/forecast/synthetic` distinctions.

**Gate:** x86 CPU shipments and revenue cannot be added together; IDC system spending cannot mix with CPU silicon TAM; OEM and hyperscaler purchase flows do not double count; frontend remains operable if DB unavailable, supports keyboard/mobile, and does not display rejected/unreviewed claims as verified.

### D7 — Executable micro-to-macro scenario engine (after D5+D6; substantial design cycle)

Owner: modeling/quant engineer.

Do **not** hard-code Lisa Su's >$220B into an observed history table. Convert independent workload observations to modeled socket demand:

```text
completed_workflows × measured_core_seconds_per_workflow
  × cloud_execution_share × (1 + measured_isolation_overhead)
  → CPU_core_hours
  → adjusted_provisioned_cores (utilization, burst/P95, memory and I/O)
  → gross_new_sockets (usable cores/socket)
  − spare existing / displaced sockets
  → net new silicon sockets × x86/Arm share × dated net ASP
  → CPU silicon dollars (and explicit uncertainty)
```

Separate GPU host attachment, net-new standalone agent execution and foundational compute with declared non-overlapping workload pools. Support multiple model definitions, input distributions, bottom-up/toplevel reconciliation residuals, downside/central/upside, backtest versions and sensitivity/tornado analysis. Every model run must be immutable at model-version + source-data-snapshot ID; model inputs have provenance or explicitly synthetic status. Use Python `Decimal` or explicit numeric policy; unknown realized CPU ASP/Arm mix is not zero.

**Gate:** deterministic rerun produces identical outputs and hashes from same inputs; measurable factors have source links; synthetic-only results are labeled and excluded from observed series; scenario and ISA partitions sum to total within declared precision; no double-counted demand across buyer/channel dimensions.

### D8 — Operations, access, backups, and explicit cutover criteria

Owner: local coordinator.

Keep SQLite WAL/backups, migration checksums, `PRAGMA foreign_key_check`, startup diagnostics, safe single-writer ownership and per-release sanitized exports. Avoid storing private client data or proprietary transcript bodies. If multiple ZCode agents mutate concurrently, serialize DB writes through one coordinator/transaction queue. Backup before reviewed schema migrations, test restore, and record source Git commit/DB release ID.

A future Postgres migration is justified only by actual multi-writer remote agent/reviewer needs or hosted query API demand. Specify cutover as a **separate decision**: compare row counts, record hashes, export digests and model outputs across SQLite/Postgres; freeze writes, migrate, reconcile, switch authority, and keep reversible snapshot. Do not introduce unaudited dual-write state.

**Gate:** repeatable Windows installation, runbook and restore proof, deterministic release tag/export, one clearly declared writer of record. No claim of production service until health monitoring, auth, review and recovery tests pass.

## 3. Recommended agent fan-out (short-lived worktrees only)

| Lane | Parallelizable scope | Required handoff |
| --- | --- | --- |
| A / Coordinator | D0 + overall registration, dependency gates, main merges | Task ledger with owner/start/branch/status/next handoff |
| B / DB + ingestion | D1, D2 then D4 | Seed evidence counts, importer and route coverage tests |
| C / Evidence & ontology | Audit D2 meanings, D5 approval and D6 buyer/channel semantics | Exact source/boundary conflicts; approval examples |
| D / Frontend | Prepare D6 adapter against documented static JSON shape; do not publish until D5 | UI tests, fields/units/quality badges |
| E / QA/CI | D3 in parallel; independent adversarial tests D4–D7 | Machine-readable QA run, reproducible failures |
| F / Modeling | D7 hypotheses/fixtures in parallel, production model only after D5/D6 | Assumption provenance, forecast vintage sensitivity |

No permanent departmental branches and no simultaneous conflicting writes to one file. Use a single consolidated `main` after evidence gates.

## 4. Delivery artifacts your ZCode agent must report

Each completed gate writes: (i) commit SHA; (ii) files touched; (iii) tests + logs; (iv) counted inputs/outputs; (v) risks and unresolved conflicts; (vi) status of Git vs SQLite data authority; (vii) the next cheapest uncertainty-reducing action. Prefer `.project`/issue log if already available; do not introduce an unrelated PM system. For D2 specifically include a seed-count report and source quality breakdown with no leaked file contents or secrets.

**No permission to claim:** "all data are in the database," "dashboard queries SQLite live," "ROCm has an official CPU backend," "verified market history," "CI green," "backend production-ready," "multiuser service" or "forecast proven" until those propositions pass their respective gates.

## 5. First-release target (smallest actually useful installable slice)

**R1 definition:** On a Windows developer machine, a clean checkout can run Python seed and validation, inspect a source-attributed x86/Arm/TAM forecast history via one CLI query, and produce a read-only JSON artifact consumed by one newly added dashboard panel **without** serving unapproved claims as facts. An agent can submit one multi-route research packet, see its staged records, and see why they are or are not publishable.

This validates the *closed loop* of research → schema → reviewed evidence → safe query/export → UI, before pursuing live APIs, automated market forecasts or PostgreSQL.

## 6. Explicit checkpoints for the human reviewer

1. **D2** seed audit: are the real corpus imports correct and existing values preserved?
2. **D5** approval semantics: which verification classes may be auto-checked but never auto-approved?
3. **R1** dashboard evidence rendering: does every view keep units, market boundary, data vintage and verification status?
4. **D7** modeling: approve definitions and falsification tests before presenting 2030 modeled sockets/dollars.

This assessment is actionable without new credentials; any cloud service, push credential, private data or irreversible cutover requires separate explicit approval.
