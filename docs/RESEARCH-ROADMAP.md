# Research and product roadmap

The dashboard is the visual interface for a continuously improved, evidence-constrained public research library. Keep the initial product small. Every future surface must reduce learning time or improve decision accuracy.

## Database foundation

[Research database v1 architecture](database/README.md) and [implementation handoff](database/IMPLEMENTATION-HANDOFF.md) are ready. SQLite v1 uses separate evidence claims, measured facts, forecast vintages, synthetic scenario runs, hierarchical but non-additive market dimensions, additive allocation frames, source lineage and review history. The original 12-file source bundle has been committed unchanged under [`db/`](../db/) ([commit `971a24d`](https://github.com/owenservera/server-cpu-strategy-lab/commit/971a24d3e94f03ec8a2280e07679d6e4a018ad30)). Local fixture testing has passed seven tests. **Real-repository seed results, the currently failing database CI workflow, staged-packet ingest, reviewer promotion, segmentation query planning, executable models and the UI adapter remain explicit gates.** See the [ZCode full wiring plan](database/ZCODE-FULL-WIRING-ASSESSMENT.md) and [bootstrap prompt](database/ZCODE-BOOTSTRAP-PROMPT.md). PostgreSQL is reserved for actual remote multi-writer requirements.

## Reusable research intake and cross-session handoff

[RESEARCH-ENTRY.md](../RESEARCH-ENTRY.md) is the **universal intake document**. The agent starts with [AGENTS.md](../AGENTS.md) and uses [research/catalog.json](../research/catalog.json) plus [research/routes.json](../research/routes.json) to discover all affected topics and record types. A single keynote, benchmark, report or conversation can emit multiple linked outputs in **one staged research packet**. See [protocol](../research/INTAKE-AND-PROMOTION.md), [schema](../research/schema/packet.schema.json) and [example](../research/templates/packet.example.json).

Status: **routing, documentation, example and lightweight validation implemented**; future work includes empirical benchmark telemetry, source-vintage normalization across all legacy datasets, optional automated source dedupe, and materialized views for the dashboard. Do not bulk-migrate historic corpora or automatically promote third-party claims.

## Milestone 1 — Current starter (complete)

- [x] Cross-device responsive, static, zero-dependency interface.
- [x] Competitor positioning / workloads / AI demand drill-downs.
- [x] Transparent interactive electricity scenario.
- [x] Linked public source register and methodology caveats.
- [x] Source category awareness and compliance boundary.
- [x] Native Node local server, unit tests, Pages workflow.

## Demand intelligence 2024–2030

**Research corpus complete; UI execution pending.** See [demand-2030 research index](research/demand-2030/README.md). The module provides the buyer/channel/ISA taxonomy, 41 observed/reported or company-disclosed and forecast-labeled records, the TAM vintage ledger, fifty acquisition priorities, explicitly synthetic 2030 scenarios, source registry and [UI work plan](research/demand-2030/DASHBOARD-HANDOFF.md).

**Critical next data work:** benchmark successful agent task CPU core-seconds and sandbox overhead, obtain actual x86/Arm buyer workload mix, verify CPU:GPU rack BOM and deployed MW, reconcile the IDC 2024-vintage discrepancy, and collect socket ASP/units without using vendor Data Center segment revenue as CPU revenue. Keep real-world data and simulations in distinct ledgers, and validate via `npm test`.

## Milestone 2 — Evidence-rich market tracker

1. **Shipments and share** — find properly licensed Mercury Research / IDC / Omdia public series and validate metric definitions (units, revenue, sockets, quarter). Show gaps when series are unavailable. Never invent share percentages.
2. **Price architecture** — catalog public SKU prices separately from measured ASP reports and from total platform prices. Do not extrapolate confidential contracts.
3. **Supply map** — track publicly announced foundry/advanced packaging, product lead times, available OEM designs, platform availability and production claims, dated.
4. **Comparable CPU spec matrix** — real SKU data with each field traced to manufacturer product specifications and lifecycle date.
5. **AI workload evidence** — separate CPU-only serving, CPU as GPU host and retrieval/ETL, catalog reproducible latency/throughput metrics and workload definitions.
6. **Customer map** — hyperscaler/OEM/enterprise/HPC publicly announced deployments, with announcement vs shipping distinction.

## Milestone 3 — Interactive strategic reasoning

- Portfolio decision lab: user defines workload and priority; score only where measurements are comparable; provide sensitivity and uncertainty.
- Capability constellation: performance/core, performance/watt, memory, network, software portability, datacenter density.
- Market event timeline with observable facts, interpretation, and falsification conditions.
- Interview prep mode: question deck, 30-second answers, evidence links and explicit caveats.
- Distinguish buyer-demand leading indicators from financial-reporting lag.

## Milestone 4 — Data pipeline

- Public-source ingestion with immutable provenance records.
- Human editorial approval gates for claims and dates.
- JSON schema for source links, derived metrics, uncertainty and version history.
- Automated freshness alerts, staleness flags and regression checks.
- Consider public-only research API and static build, not required for MVP.

## Design acceptance criteria

- A reader identifies the three competing ecosystems in 30 seconds.
- A reader can articulate three distinct AI CPU roles in 60 seconds.
- No number is displayed without scope and source or “hypothetical” labeling.
- All interactive controls work by keyboard and touch.
- Mobile requires no horizontal page scrolling at 360px viewport.
- The project still works locally with no external package downloads.

## Optional investigation: why this topic may be urgent

Public-only explanations worth investigating, not client identity claims: (1) server replacement cycle, (2) EPYC versus Xeon competitive repositioning, (3) hyperscaler self-designed Arm adoption, (4) AI host CPU attach and CPU inference, (5) supply/price pressure. Track public indicators and rank hypotheses only after evidence collection. Never pretend to know a confidential requesting client's purpose.