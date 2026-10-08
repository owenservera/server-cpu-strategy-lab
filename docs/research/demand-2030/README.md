# Server CPU demand to 2030 — integrated research index

**As of 2026-10-08 · Status: research integration, public evidence + labeled analytical scenarios.**  
**Scope:** 2024 through latest available 2026 quarter; scenario years 2027–2030.  
**Companion thesis:** [AMD keynote workbench](../AMD-ADVANCING-AI-2026-RESEARCH-PATH.md) · [key-figure decomposition](../KEY-FIGURE-DECOMPOSITION.md) · [Microsoft/Docker placement and isolation](../MICROSOFT-DOCKER-AGENTIC-DEMAND-SLICES.md) · [ROCm/x86 architecture](../../ROCM-X86-ROADMAP-2026-2031.md).

## What this module adds

| Layer | Committed file | Usage |
| --- | --- | --- |
| Public evidence registry | [source-registry.json](../../../data/demand-2030/source-registry.json) | Primary/secondary source URLs, date, access and licensing status |
| Historical observations | [historical-and-forecast-evidence.csv](../../../data/demand-2030/historical-and-forecast-evidence.csv) | 41 metric records with denominators, company fiscal period and provenance |
| Forecast revision history | [tam-forecast-vintages.csv](../../../data/demand-2030/tam-forecast-vintages.csv) | Separates AMD and bank estimates by publication vintage |
| CPU silicon TAM scenario workbook | [scenario-model.json](../../../data/demand-2030/scenario-model.json) | Internally additive 2025–2030 downside/central/upside, explicit x86 assumption |
| Full analysis | [MARKET-SYNTHESIS.md](MARKET-SYNTHESIS.md) | End buyers, channels, growth pockets, new player archetypes, disconfirming evidence |
| Buyer/channel/workload ontology | [TAXONOMY-AND-ACCOUNTING.md](TAXONOMY-AND-ACCOUNTING.md) | Dimension keys and non-double-counting identities |
| Recovery plan | [DATA-DICTIONARY-AND-GAPS.md](DATA-DICTIONARY-AND-GAPS.md) | Ranked high-marginal-value fields, methods, gaps and public URLs |
| Dashboard design | [DASHBOARD-HANDOFF.md](DASHBOARD-HANDOFF.md) | UI surfaces, figure definitions, derived data and acceptance criteria |

### The controlling question

Who creates additional **CPU silicon demand**, who physically procures CPUs, which workloads consume them, through what OEM/ODM channel, and how much is x86 (EPYC/Xeon) rather than custom Arm or another architecture? Value capture is measured in **chip units, ASP and CPU revenue**, not total GPU server dollars.

### Separation of evidence tiers

- **Company/market figures:** filing or tracker claims recorded with source, population, fiscal period, measurement basis. Not all historical rows have been independently re-audited against each original document.
- **Secondary analyst figures:** published descriptions of Mercury/Citi/BofA/Bernstein; original paywalled documents remain unverified unless marked otherwise.
- **Management forecasts:** AMD 2030 opportunity statements; not realized revenues or market consensus.
- **Synthetic scenarios:** our explicit 2025–2030 sensitivities, **not independent third-party forecasts** and **not actual data**. A high scenario may exceed AMD's latest >$220B projection: that number is not a physical ceiling.
- **Mechanistic hypotheses:** agent-core-seconds, sandbox isolation, on-device displacement and custom Arm share need reproducible benchmark evidence.

## Key reconciliations already required

1. **IDC systems vs CPU silicon:** [IDC July 2026](https://www.idc.com/promo/servers/) estimates 2025 worldwide server-system spending at $453.531B, 2026 at $646.998B and 2027 at $930.562B. These whole-system figures are *not* the $25B → >$220B server-CPU-silicon TAM discussed by AMD.
2. **2024 IDC vintage conflict:** completed research recap mentions ~$235.7B in 2024 while the current July 2026 IDC table states 2025 $453.531B and 2025 growth +78.2%. These imply about **$254.5B** in 2024, not $235.7B. Mark the 2024 amount **conflicted pending vintage reconciliation**; do not insert a definitive 2024 actual into the historical CSV.
3. **AMD unit vs dollar share:** broad server x86 **CPU shipment share** is not comparable to AMD share of **CPU revenue**, and Mercury's narrow EPYC-versus-Xeon SP metric uses yet another denominator. All must retain their named metric and population.
4. **Buyer ≠ route to market:** a hyperscaler can buy from an ODM, Dell, HPE or another partner. OEM/ODM revenue cannot be added again as separate demand on top of hyperscaler or enterprise purchases.
5. **Capex ≠ CPU spend:** Microsoft/Amazon/Meta capex, GPU rack revenue, OEM system revenue and cloud revenue are contextual leading indicators, not inputs directly additive to the CPU silicon market.
6. **Agent ≠ hardware core:** CPU threads per rack and simulated agents/watt are not end-to-end *successful tasks per second*. Agent CPU unit conversion requires observed core-seconds and concurrency.
7. **ARM ≠ IDC non-x86 system mix:** total cost of non-x86 systems can include accelerators, networking, HBM and CPUs; not a direct measure of Arm silicon units or revenue.
8. **New Citi forecast supersession:** Oct 7 public reporting describes a new ~$300B Citi 2030 TAM estimate. It is *secondary*, and should appear as a distinct vintage and trigger a primary-note retrieval task, not replace AMD's estimate.

## Proposed information architecture

`01-market-sizing` → `02-buyers` → `03-channels` → `04-workloads` → `05-architecture` → `06-unit-ASP-profit` → `07-supply` → `08-2030-scenarios` → `09-evidence-ledger`.

Keep every chart drill-down connected to a shared source pane: definition, unit, geography, observed vs modeled, fiscal period, denominator, contradictions and source URL. Preserve the project's existing zero-dependency static dashboard and `npm test` conventions.

## Compliance and refresh

Only public statements, public filings and public summaries of industry datasets are allowed. **Never copy expert-network client/screenshots, nonpublic employer data, licensed sell-side research or confidential discounting** into this public GitHub repository. Store full source claims with attribution and retrieval vintage, and publish derived summarized records only. Refresh quarterly from filings and whenever public TAM estimates change; require editorial review before "verified" UI badges.
