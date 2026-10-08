# UI / developer handoff: server CPU demand cube (2024–2030)

**Stage:** scoped build plan. **No deployment changes**, no replacement of the existing public-source dashboard. Preserve zero-dependency standalone mode, browser keyboard accessibility, touch interactions and the existing test harness.

## User outcomes

In 60 seconds the reader must distinguish: who buys CPU silicon, who sells the rack, who consumes the cloud service, which work runs on x86 vs Arm, and how much of growth is physical CPU shipments vs chip ASP/mix. The user should be able to inspect any claim's denominator/date/source, or tell that it is an assumption.

## Contract / data sources

Read fully: [module](README.md), [taxonomy](TAXONOMY-AND-ACCOUNTING.md), [market synthesis](MARKET-SYNTHESIS.md), [data dictionary](DATA-DICTIONARY-AND-GAPS.md), then the committed [source registry](../../../data/demand-2030/source-registry.json), [observations](../../../data/demand-2030/historical-and-forecast-evidence.csv), [forecast vintages](../../../data/demand-2030/tam-forecast-vintages.csv), and [scenario model](../../../data/demand-2030/scenario-model.json). These are not homogeneous market observations.

### Eight high-value figures to build (in dependency order)

| Rank | Panel | Axes / interaction | Data source and guard |
| --- | --- | --- | --- |
| 1 | **Demand by end buyer** | Hyperscale public, internet/internal, Tier-2 CSP, neocloud, enterprise, sovereign, HPC, telco. Year/region filters | Start as structural map and evidence cards; real socket percentages only after validated acquisition |
| 2 | **Buyer ↔ channel flow** | Buyer on left → ODM direct / Dell-HPE-Lenovo-Supermicro / integrator / custom silicon on right | **Two independent dimensions; never sum OEM channel and hyperscaler end-demand** |
| 3 | **System vs silicon divergence** | IDC 2025–27 x86/non-x86 **whole-server system dollars** vs distinct Intel/AMD CPU-chip ASP/volume signals | Different y axes, units, and warning. 2026/27 IDC FORECASTS; 2024 IDC vintage conflicted |
| 4 | **AMD vs Intel x86 share** | Quarter selector: broad x86 CPU unit share vs broad x86 CPU revenue share; no narrow EPYC/Xeon-SP mixing | Mercury public secondary reporting; locked scope and as-of badges |
| 5 | **Forecast-vintage timeline** | AMD November 2025, May/July/September 2026; Citi/BofA/Bernstein with publication dates | Forecast estimates, not observed TAM. Cite each; mark original bank notes unreviewed |
| 6 | **2030 workload waterfall** | Foundational → AI host → standalone agent execution → CPU-silicon total; switch downside/central/upside and year | `scenario-model.json`; labels '**synthetic scenario**' persistent, dollar categories add exactly |
| 7 | **x86/Arm opportunity matrix** | Workload × architecture × buyer, change assumed shares independently; show x86 and non-x86 CPU *silicon dollars* | Unknown 2025 actual ISA shares stay blank. Expose assumed architecture splits |
| 8 | **Agent CPU demand sensitivity** | Completed workflows, CPU core-sec/workflow, local share, isolation tax, utilization, usable cores/socket, CPU/GPU host ratio, net realized ASP | Until benchmark data exist: sliders are editable assumptions; output task core-hours/cores/sockets/$ with uncertainty |

### Chart semantics

- Distinct visual metadata chips (not colorful decorative badges) for `company_disclosed`, `secondary_market_estimate`, `management_forecast`, `analyst_forecast`, `synthetic_scenario` and `missing`.
- Every numeric mark opens evidence: source URL, date, period, originator, denominator, population, measure, access status, caveat, calculation and contradictions. If a citation is absent, suppress the numeric mark and show a gap state.
- Use **quantity-aware drilldowns**: systems, sockets, physical cores, CPU chip revenue, entire rack spending, cloud service revenue, capex, realized CPU ASP and gross margin pools may never be added together. Include a context tooltip showing why.
- Allow chronological filtering 2024–2030, but 2026 YTD **actual** and full-year 2026 **forecast** must not share an undifferentiated label.
- Fiscal quarter results (Dell FY27 Q2, HPE FY26 Q3) retain company fiscal period and must not masquerade as calendar quarter unless mapped explicitly.
- Put the source-vintage **2024 IDC discrepancy** into a visible review item (2024 $235.7B research recap vs ~ $254.5B implied by 2025 +78.2%). Don't graph one as fact without reconciliation.
- Keep the >$220B AMD forward estimate and Oct 2026 Citi ~$300B reported estimate independent of the synthetic $200B middle case.

## Interaction example

Select `Buyer: neocloud` → `Workload: GPU host` → `Architecture: x86` → `Vendor: AMD`; UI should show what is known (e.g., public announced racks and contracts), what is estimated (attachment and x86 distribution), and what remains missing (actual processor units and ASP). Another selector should switch to `agent execution` without double-counting the same physical CPU rack.

## Agentic workload calculator: correct units

`new_cloud_core_hours = successful_workflows × measured_CPU_core_seconds_per_workflow / 3600 × net_cloud_share × (1 + incremental_isolation_tax)`.

`provisioned_cores = peak_adjusted_core_hours / (hours_in_period × utilization)`.

`new_CPU_sockets = max(0, provisioned_cores / usable_cores_per_socket - unused_preexisting_equivalent_sockets)`.

`new_x86_CPU_silicon_value = new_CPU_sockets × x86_socket_fraction × net_CPU_ASP`.

CPU/GPU host silicon has a **separate** physical attach calculation; foundational SQL/ERP load adds a socket only if a new purchase is required. Do not multiply sandbox hardware by both `threads` and `agents` and then call result measured agent throughput.

## Implementation sequence for local agent

**D1:** Define parser and validation schemas for the existing data. Add one-page research index + evidence drawer and make chart data units typed. **D2:** Build first four historical/buyer/source panels. **D3:** Add the forecast-vintage and 2030 waterfall panels. **D4:** Add architecture and benchmark-parameter sensitivity. **D5:** Build unknown-data placeholders, contradiction rail, mobile testing, and automation-friendly static build. A new temporary worktree is fine, but merge back to `main` rather than establishing long-lived streams.

Do not build a large ETL service or ingest private consulting-screening information. Maintain public-only sources, and do not interfere with the separately managed Vercel/Verso deployment.

## Acceptance gates

1. For every number, user can see original source and date, metric unit, market and source status.
2. 2025 IDC system values sum to reported total; 2026/27 sums pass with published rounding tolerance.
3. Each modeled annual TAM equals its three distinct workload categories; modeled architecture parts add to total.
4. No chart conflates OEM with end-buyer, server systems with CPU silicon, FY with CY, AMD Data Center GPU+CPU revenue with EPYC revenue, or Arm CPU with IDC 'non-x86 systems'.
5. Forecasts and observed historical data cannot be displayed with identical status markings.
6. Existing dashboard tests and new demand-data tests pass via `npm test`.
7. Under 360px viewport horizontal scrolling is not needed for core controls; keyboard navigation reaches filters and evidence links.
