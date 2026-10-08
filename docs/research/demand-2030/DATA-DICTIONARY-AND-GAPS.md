# Prioritized data dictionary and missing evidence register

**As-of:** 2026-10-08. These are **fields to collect**, not observed dataset values. A field's source hint never implies that the actual value has been verified or made public. Missing inputs must stay `null`; no backfilled forecasts masquerading as history.

## Ranking principle

Top 15 are prioritized for reducing uncertainty in **incremental agent CPU core-hours, CPU socket demand, net ASP and x86 vs Arm revenue capture**. This is an editorial ranking, *not* a statistically estimated value-of-information score. All source and access claims are provisional until the retrieval task independently validates them.

| Rank | Metric | Unit | Grain / denominator | Access / source | Dashboard |
| ---: | --- | --- | --- | --- | --- |
| 1 | CPU core-seconds per successful agent workflow | core_seconds | workload×ISA×sandbox×site×week / completed validated workflow | must_collect; instrumented benchmark | agent demand bridge |
| 2 | Cloud fraction of complete agent workflows | share | workload×model×buyer×month / all completed workflows | must_collect; endpoint+cloud telemetry | local/cloud elasticity |
| 3 | x86 CPU share by workload and end buyer | CPU revenue share | quarter×workload×buyer / all server CPU silicon revenue | partial_proxies; Mercury+cloud docs+buyer interviews public only | architecture opportunity |
| 4 | CPU sockets attached per AI GPU in production | sockets/GPU | rack×buyer×year / production accelerator quantity | partial_proxies; public OEM/OCP BOM | AI head-node matrix |
| 5 | Cloud CPU silicon spending per incremental AI MW | USD/MW | operator×rack class×year / commissioned IT MW | must_model; public BOM+power estimates | GW→CPU waterfall |
| 6 | Net CPU ASP per socket by tier | USD/socket | vendor×SKU tier×buyer×quarter / CPU silicon socket shipments | mostly_unavailable; Intel 10-Q+OEM price bands | ASP bridge |
| 7 | Total world server CPU shipments | sockets/quarter | region×quarter / all server CPU chip shipments | paywalled; Mercury/IDC/Omdia paywalled | units TAM |
| 8 | Incremental CPU sockets commissioned | sockets/quarter | buyer×workload×quarter / installed fleet delta | mostly_unavailable; OEM/customer rack disclosures | demand waterfall |
| 9 | CPU cores/socket of shipped mix | cores/socket | vendor×ISA×quarter / shipped physical sockets | partial_proxies; vendor mix and SKUs | socket density |
| 10 | Successful concurrent agent sessions per CPU node | sessions/node | task type×node×sandbox / successful distinct workflows | must_collect; controlled telemetry benchmark | agent density |
| 11 | Resident RAM per sandbox | GB/concurrent_session | task×sandbox×node / actual concurrent sessions | must_collect; benchmark telemetry | resource bottlenecks |
| 12 | Measured microVM versus container CPU overhead | percent | workload×runtime×ISA / native control CPU core seconds | must_collect; SBX/MXC native trials | isolation tax |
| 13 | AI rack host CPU model and core count | physical cores/rack | GPU platform×OEM / one verified rack build | partial_public; AMD OEM NVIDIA docs | rack BOM |
| 14 | Provisioned CPU utilization | share | buyer×workload×time / physical core-hours offered | nonpublic_proxy; operator telemetry | fleet capacity |
| 15 | Mercury AMD server CPU revenue and unit share | percent | quarter×market definition / matching x86 CPU unit/revenue market | public_secondary; Mercury public reporting | share vs mix |
| 16 | ARM/custom server CPU shipments | sockets/quarter | Arm vendor×buyer / all server CPU shipments | mostly_unavailable; Arm/vendor commentary+market trackers | ARM adoption |
| 17 | Hyperscaler CPU SKU deployments | counts and named SKU | buyer×cloud VM generation / orderable/installed instances | public_partial; AWS Azure GCP OCI catalogs | buyer mapping |
| 18 | Cloud on-demand price per vCPU-hour | USD/vCPU_hour | cloud×region×SKU×month / billable vCPU-hour | public; cloud public pricing APIs | cloud price index |
| 19 | Cloud spot/reserved effective prices | USD/vCPU_hour | cloud×commitment×region / vCPU-hour | public_partial; cloud public rate cards | buyer TCO |
| 20 | Agent tool calls per workflow | calls/workflow | task×agent×model / successful workflows | must_collect; agent trace instrumentation | workload complexity |
| 21 | P95 CPU core-seconds per tool call | core_seconds | tool class×ISA×runtime / completed tool call | must_collect; agent trace profiling | CPU intensity |
| 22 | Average endpoint agent share of tool work | percent | device class×task / all tool actions | must_collect; Windows ML+traces | endpoint substitution |
| 23 | Incremental task demand from cheap local models | percent elasticity | price bin×cohort×month / baseline completed workflows | must_collect; natural experiments | induced demand |
| 24 | CPU watts per completed agent workflow | joules/workflow | ISA×task×runtime / successful workflow | must_collect; power instrument+task traces | efficiency frontier |
| 25 | Cloud inference input-output token mix | tokens | model×deployment×month / completed requests | partial_public; public operator model metrics | token→CPU model |
| 26 | Agent code-compile and test workloads | core_hours/workflow | language×repository×ISA / successful coding task | must_collect; test harness logs | CI agent demand |
| 27 | Agent retrieval and SQL workload intensity | CPU_seconds/query | engine×data size×ISA / valid query result | must_collect; reproducible SQL/RAG suites | shadow CPU load |
| 28 | Agent isolation cold-start latency | milliseconds | runtime×OS×machine / successful sandbox starts | must_collect; SBX/MXC benchmark | sandbox overhead |
| 29 | Agent policy audit CPU cost | CPU_seconds/policy_event | runtime×policy_count / authorized action event | must_collect; MXC and SBX tests | governance tax |
| 30 | AMD EPYC vs Xeon volume growth | percent | vendor×quarter / same-vendor CPU units YoY | public_partial; Intel 10-Q+AMD commentary | share decomposition |
| 31 | Intel server CPU ASP YoY | percent | quarter / same-vendor server CPU ASP | public_primary; Intel 10-Q | pricing pressure |
| 32 | AMD EPYC unit and ASP proxy | index | quarter / AMD server CPU shipments | public_partial; AMD IR + independent market | ASP hypothesis |
| 33 | Enterprise server refresh replacement cycle | years | vertical×region×buyer / server installed base | partial_paid; OEM/IDC market research | baseline demand |
| 34 | Datacenter grid MW commissioned | MW | operator×region×quarter / commissioned IT power | public_partial; public energy/permit disclosures | power gating |
| 35 | Neocloud CPU rack complement by AI MW | sockets/MW | operator×platform×quarter / commissioned accelerator MW | partial_public; CoreWeave/Nebius/BOM | new entrants |
| 36 | Neocloud contracted vs deployed power | MW | operator×region×quarter / contracted and energized sites | public_partial; public IR | buyer maturity |
| 37 | OEM direct versus ODM channel shares | percent system revenue | quarter×region / global server system sales | public_partial; IDC market tracker | channel map |
| 38 | Branded OEM server orders versus sales | USD | OEM×fiscal quarter×product line / OEM reported bookings/sales | public_partial; Dell HPE Lenovo | enterprise leading index |
| 39 | OEM server operating margin | percent | OEM×fiscal quarter / OEM server segment revenue | public_partial; Dell HPE public IR | profit pool |
| 40 | ODM rack/server gross margin | percent | ODM×fiscal quarter / ODM computing revenue | public_partial; ODM reports | channel profit |
| 41 | Sovereign/private AI deployments | installed clusters | jurisdiction×vertical×year / production customer facility | public_partial; HPE OEM public contracts | vertical demand |
| 42 | CPU memory bandwidth per socket | GB/s | SKU×config / populated memory channels | public; AMD/Intel product guides | SKU spec matrix |
| 43 | PCIe/CXL I/O capacity | GB/s | SKU×platform / CPU lane and link configuration | public; CPU guides PCI-SIG CXL | host bottleneck |
| 44 | Datacenter DRAM/server prices | USD/GB | region×DIMM×quarter / installed memory capacity | public_partial; OEM catalog+market research | BOM sensitivity |
| 45 | CPU core count/available sockets supply | wafer or SKU orderable | vendor×node×quarter / production CPU units | mostly_private; vendor IR/OEM orderability | supply gating |
| 46 | Cloud VM ARM allocation | percent VM-hours | cloud×region×workload / CPU VM-hours consumed | mostly_private; cloud public configs | ARM share stress |
| 47 | Hyperscaler capex on short-life equipment | USD billion | company×fiscal quarter / disclosed total hardware capex | public_partial; Microsoft/Meta/Amazon IR | macro demand signal |
| 48 | Accelerator rack CPU/CPU-GPU cost mix | USD CPU/USD accelerator | platform×generation / fixed rack BOM | modeled; AMD Nvidia/OEM references | CPU attach value |
| 49 | Latency and workflow success performance | success/tasks/s | workload×runtime×CPU ISA / completed valid work | must_collect; benchmark harness | deployment choice |
| 50 | x86 binary compatibility cost for migration | USD or engineer hours | workload×legacy class / ported production application | must_collect; open portability studies | ARM switching cost |

The companion [machine-readable dictionary](../../../data/demand-2030/priority-data-fields.json) adds source, update cadence, specific validation plan and field rank. Publicly inaccessible metrics should use reproducible proxies, not fabricated point estimates.

## Acquisition priority

**First 30 days:** source-verify market and supplier time series; define representative agent workflow suite and run identical native/container/SBX/MXC tasks on comparable EPYC/Xeon/Arm or cloud instances; record P50/P95 core seconds, success, RAM, watts, network and latency; capture public CPU/GPU rack BOMs and cloud VM architectures.

**Days 31–60:** expand four buyer cohorts (Tier-1 cloud, private enterprise, neocloud, sovereign/HPC) and OEM/ODM procurement channel mapping; work from disclosed cloud instance catalogs and genuine commissioned equipment, not capex headline alone; validate CPU/GPU attachment and Arm substitutes.

**Days 61–90:** update bottom-up stock-flow demand model, net-new socket inference and realized-ASP uncertainty; perform sensitivity/tornado analyses; pressure-test cases where local computation, Arm adoption and better sandbox pooling reduce x86 capture.

## Non-identifiability / contradictions

1. The $25B market baseline and AMD/analyst $100B–$300B+ TAM narratives have incompatible forecast vintage/conditions unless explicitly stated.
2. Intel's reported ASP increase does **not** determine industrywide ASP, nor AMD CPU-only gross margin.
3. IDC server-system spending includes GPUs and networking, cannot be inverted into CPU silicon without verified BOM and mix.
4. Hyperscaler cloud purchase and OEM/ODM vendor sale are two sides of one transaction; do not sum them.
5. CPU utilization of agent tools, RAM pressure and endpoint displacement remain the model's biggest empirical unknowns.
6. A benchmark measuring runnable sandboxes or SMT threads is *not* successful workflow throughput.
7. Source access: public-secondary press ≠ licensed Mercury/Omdia dataset; no redistribution of inaccessible commercial research.

**Verification gate:** no observed numerical series is accepted into the UI without a direct or clearly attributed public source, fixed denominator, vintage and conflict check; synthetic model controls must be visually distinguished.
