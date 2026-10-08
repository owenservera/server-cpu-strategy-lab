# ZCode kickoff prompt — fully wire CORE/SIGNAL research DB v1

**Usage:** Paste the content below into the **ZCode coordinator** running on the actual Windows checkout. This is one executable handoff, not a speculative future architecture proposal. It is written to remain useful even if the local agent has no context from this ChatGPT conversation.

---

You are the implementation coordinator for the public `owenservera/server-cpu-strategy-lab` repository on my Windows machine. Your objective is to wire the database from a checked-in SQLite prototype into an evidence-safe research pipeline, with **the smallest useful tested vertical slice first**.

## Mandatory discovery / no skipped reading

Before editing anything, read in full, in order:

1. `AGENTS.md`
2. `RESEARCH-ENTRY.md`
3. `research/README.md`, `research/routes.json`, `research/catalog.json`, `research/schema/packet.schema.json`, `research/INTAKE-AND-PROMOTION.md`
4. `docs/database/README.md`, `docs/database/ARCHITECTURE-V1.md`, `docs/database/SEGMENTATION-AND-MODELS.md`, `docs/database/IMPLEMENTATION-HANDOFF.md`, `docs/database/STATUS.json`
5. `db/README.md`, **all** `db/design/*.md`, both `db/migrations/*.sql`, `db/seed/foundation.json`, `db/scripts/research_db.py`, `db/tests/test_research_db.py`
6. **The binding work plan:** `docs/database/ZCODE-FULL-WIRING-ASSESSMENT.md`
7. Current `data/` and `tests/` inventory, open GitHub issues (especially #5), package scripts, existing CI and site deployment.

The full tested bundle was already pushed as exact, unchanged files in commit `971a24d3e94f03ec8a2280e07679d6e4a018ad30`. **Do not re-extract it, recreate it from prose, or assume a separate ZIP is required.**

## First action: local-state and environment audit

Confirm `git status --short`, local `HEAD`, `origin/main`, all worktrees and any in-progress agent work. Preserve local modifications; don't reset/delete/force-push and don't create permanent department branches. Register intended work at least at the task/deliverable level before making changes. Use a short-lived worktree if the active checkout is busy, reconcile with the latest main before final merge. Default to local available Python 3.11+ with SQLite 3.37+; don't assume WSL, Docker or Linux.

## Execute in strictly gated order

**Gate D1 — Environment and tests.** Detect `py -3.11` or `python`; run the seven `db/tests` fixture tests; collect versions and command logs; fix reproducible failures instead of suppressing assertions.

**Gate D2 — Real-corpus seed.** Run `seed`, `verify`, `stats`, and `export` with `db/scripts/research_db.py` on the **actual latest repository**. Run twice for idempotence. Record per-table/per-source counts, all data quality flags, forward IDC estimates versus actual measurements, nine separate TAM vintages, AMD and Microsoft/Docker attributed claims, model assumptions, 2025 unknown/NULL ISA shares, and the open IDC 2024 disagreement. On a collision, stop and investigate original value, vintage and change, never use `INSERT OR REPLACE` to hide it. Commit code/docs and a sanitized QA summary, not `db/runtime/` artifacts.

**Gate D3 — CI reproducibility.** Verify or implement isolated Python DB CI with `actions/setup-python`, fixture tests, clean real seed, verification and export checks. Keep the static website and GitHub Pages independent. Explicitly report the CI run URL and whether the run passed; don't claim green from local tests.

**Gate D4 — Packet adapter.** Build the smallest packet-to-database staging importer over the **existing** 19 research routes, with meaningful unsupported-route reporting, stable IDs, source versioning, review-state preservation, idempotence and provenance. Ensure all route data is retained without automatically promoting numbers to market facts. Add fixtures demonstrating duplicate packet, changed forecast revision, genuine source contradiction and source access/rights failures.

**Gate D5 — Review/promotion.** Implement an append-only reviewer protocol in `review_events`; users must approve publication explicitly or via documented allowed rules. Claims, measurements, forecasts and synthetic scenarios must stay separate. Avoid using an LLM's confidence as independent verification. Add a CLI before creating a multiuser web API.

**Gate D6 — Safe query/public data.** Build a typed segment query plan and an approved-read-only export for the static dashboard. Preserve buyer vs procurement-channel orthogonality, fiscal/calendar period distinctions, whole-system vs CPU silicon boundaries, and x86/Arm allocation frames. Implement one end-to-end user-visible panel that reads this **approved** export with attribution, date and warnings, while keeping the current dashboard working offline if DB isn't available.

**Gate D7 — Modeling and telemetry.** Design carefully before implementing: successful agent workflows → measured CPU core-seconds → cloud/local placement → utilization/isolation → net added provisioned cores/sockets → x86/Arm shares → net CPU ASP and revenue. Connect model input provenance, test uncertainty ranges and source-vintage sensitivities. Never treat future TAM as an observed market value.

**Gate D8 — Operations and portability.** Document restart, backups, restore, migrations, incremental updates and errors on actual Windows. Enforce a single DB writer and one Git reviewer/publisher authority. Do not switch to Postgres unless actual multiwriter needs arise and a reviewed cutover is authorized.

**Minimum useful release first:** prove the complete *read-only* loop: `real data → seed → review/validation → safe snapshot → one dashboard panel`. Then extend to new packets/reviewer automation. Use the gates above as the definition of complete, not LOC or elapsed time.

## Parallelization and autonomy

You may fan out independent audit, CI, evidence taxonomy, UI adapter and benchmark-design tasks if they avoid same-file conflicts and keep a coordinator. Do not duplicate work simply to parallelize; use duplicate work only for independent verification. Keep one consolidated `main`, short-lived worktrees only. Do not ask for approval at every routine safe engineering action, but **stop and request an explicit decision** before exposing unpublished data, changing source-of-truth authority, creating a hosted production service, force-pushing, deleting others' work, or switching to a multiwriter database.

## Hard evidence gates

- All sourced records have provenance, access status, denominator and verification state.
- `estimated/management_forecast/analyst_forecast/synthetic` cannot appear as independently verified observations.
- `CPU_silicon_revenue` and `server_system_spending` do not share an additive measure; OEM/ODM and hyperscaler demand are not double counted.
- An agent thread/core count is not benchmarked completed agent throughput.
- Git staging/approved source remains authoritative for v1; DB is derived until a future approved cutover.
- New research must reuse existing stable IDs and preserve old forecast vintages.
- Confidential consulting/client material and full third-party transcript copies are excluded.

## Required progress and final report

At each gate update the work record with `owner / scope / blocker / commit / tests / completion proof / next dependency`. Prefer working directly from the current research issue(s) without building a new PM system.

At the end, push completed, tested incremental commits to `main` (no force push). Report:
1. exact commit SHAs and any remaining local-only changes;
2. full live seed counts and `DB_VALIDATE_PASS` result;
3. test-suite and CI run URL/conclusion, including any failures;
4. which database tables and research routes are **actually wired** versus only designed;
5. current reviewer/publication authority and whether the dashboard is querying approved data;
6. blockers, unresolved market-definition conflicts, and the next minimum useful increment.

If a phase cannot be completed safely, preserve verified earlier phases and leave a machine-readable failure report and clear next action. **Do not claim the full pipeline is finished until the end-to-end release gates pass.**

---

See [full assessment](ZCODE-FULL-WIRING-ASSESSMENT.md) for rationale, precise dependencies and acceptance tests.
