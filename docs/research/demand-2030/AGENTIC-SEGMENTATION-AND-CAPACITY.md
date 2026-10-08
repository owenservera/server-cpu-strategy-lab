# Agentic-era server CPU demand: segmentation and capacity model

**As of:** 2026-10-08 · **Planning horizon:** 2026–2035 · **Status:** research methodology and public evidence, NOT a measured CPU shipment forecast.

**Canonical context:** [research entry](../../../RESEARCH-ENTRY.md) · [intake packet](../../../research/packets/2026-10-08--agentic-server-cpu-segmentation.json) · [demand index](README.md) · [buyer/channel/ISA taxonomy](TAXONOMY-AND-ACCOUNTING.md) · [DB model semantics](../../database/SEGMENTATION-AND-MODELS.md) · [existing scenario model](../../../data/demand-2030/scenario-model.json).

## 1. Decision question and market boundary

**How much *incremental physical server CPU silicon demand* do agentic applications generate by 2030/2035, which physical buyer procures the CPU, and what share do x86 (AMD/Intel) versus Arm/custom architectures capture?**

Define and measure: activity → CPU/RAM/I/O reservation → usable fleet capacity → net installed sockets → new and replacement annual CPU silicon shipments → net realized CPU ASP → dollar revenue. Forecasts, surveys, cloud VM billings, all-server systems, hardware silicon and software revenues are separate series.

Existing [research](TAXONOMY-AND-ACCOUNTING.md) already maintains mutually exclusive economic physical hardware buyer, procurement channel, workload and ISA axes. **Do not introduce a competing buyer/ISA ledger** here. OEM and hyperscaler counts can reflect the *same* CPU purchase. A model lab is the service customer when a neocloud buys the actual CPU equipment. GPU-host CPU BOM must be counted once, not added again as agent sandbox CPUs. Local PC/mobile endpoint CPU purchases are excluded from server CPU TAM; a dedicated home/edge server is eligible only under explicitly stated server-CPU market definitions.

## 2. Segment by primary economic workflow purpose, not by agent vendor

One successfully completed *initiating workflow* is allocated to **one** primary-purpose category (or U0 unknown). This partition can sum to 100%; secondary tags are non-additive. Each workflow may contain multiple CPU execution events across services and sites; count each physical event once. A coding agent invoked via SaaS is D1, not a separate P1 market. A bank claims agent belongs to E3 and carries a regulated-industry *tag*; E4 is reserved for compliance/regulated-decisioning as the underlying outcome itself.

| Code | Primary purpose | Examples | Primary CPU questions |
| --- | --- | --- | --- |
| C1 | Consumer transactional | Shopping, travel, administration | Browser/tool sessions, APIs, backends |
| C2 | Personal persistent | Continuous assistant, monitoring, memory | Idle reservation, background CPU, local/cloud |
| C3 | Consumer creative | Documents, websites, media, personal data | Conversion, execution, rendering |
| E1 | Enterprise knowledge | Research, contracts, analytics | Search/RAG, document and governance work |
| E2 | Enterprise back-office | ERP, CRM, payroll, procurement, supply chain | Legacy transactions, databases, integration |
| E3 | Enterprise customer operations | Sales/service, contact centers, claims | Concurrent sessions and application tools |
| E4 | Compliance/sovereign purpose | Risk controls, regulated adjudication, public administration | Isolation, private placement, audit |
| D1 | Software engineering | Coding, compilation, CI/CD, testing, migration | Sustained core-seconds, peak RAM, retries |
| D2 | IT/security operations | SRE monitoring, remediation, threat response | Persistent agents, telemetry, verification |
| P1 | Residual embedded platform agents | Native SaaS agents without more-specific purpose | Multitenant sandbox infrastructure |
| P2 | Residual machine-to-machine agents | Agent markets, delegated autonomous transactions | Delegation graph and duplicated execution |
| X1 | Scientific/industrial/physical | Robotics operations, simulation, digital twins | Edge, simulation, back-end CPU |
| U0 | Unclassified | Unknown task purpose | Preserve unknown instead of guessing |

### Orthogonal non-additive dimensions

- **Industry:** banking, healthcare, technology, retail, manufacturing, government etc. Enterprise sector != workflow purpose.
- **Service customer / actor:** consumer, SMB, enterprise, model operator, public body, machine-to-machine counterpart; distinct from CPU hardware purchaser.
- **Placement per execution step:** hyperscale CSP, neocloud, enterprise private DC, sovereign DC, telco edge, home server, PC/mobile. Do not assign an entire hybrid workflow to a single place.
- **Execution topology:** shared host process/container, in-instance sandbox, pooled prewarmed session, dedicated microVM, dedicated long-lived VM, bare metal, GPU host.
- **CPU activity:** orchestration, browser/computer use, code/compile/test, ERP/DB transaction, retrieval, governance/security, CPU model inference, storage/network service and GPU host functions.
- **Ownership, ISA, procurement channel, period and lifecycle:** reuse canonical keys; distinguish installed stocks, net fleet growth, displacement, refresh, channel inventory and yearly shipments.
- **Resource metrics:** active agents, successful workflows, agent actions, runtime sessions, concurrent sessions, core-seconds, resident RAM GiB-hours, IOPS, vCPU billings, usable physical cores/socket and chip ASP all have DIFFERENT denominators.

## 3. Bottom-up forecast and physical conservation

For each purpose segment `s`, time `t`, execution-step class `k`, location `p` and runtime `r`:

```
successful_workflows = eligible_population × adoption × active_share
                     × annual_completed_workflows_per_active_unit

CPU_core_seconds[s,t,k,p,r]
  = successful_workflows[s,t]
  × invocations_per_successful_workflow[k]
  × physical_host_core_seconds_per_invocation[k,p,r]
  × placement_probability[k,p,r]
  × retry_and_failed_attempt_multiplier[k]
```

*Avoid double-counting:* if the measurement is already end-to-end core-seconds **per successful workflow including retries**, do not multiply retries again. A parent agent and child agent often reference the same underlying hardware execution event. CPU cycles consumed by existing enterprise SaaS infrastructure are not a new hardware purchase until actual spare capacity is exceeded.

The proper capacity denominator is a **homogeneous physical host pool**. Compute constraints within the pool, then choose the binding capacity requirement:

```
K_cpu = peak_adjusted_core_hours / (period_hours × target_utilization)
K_ram = simultaneously_reserved_resident_GiB / usable_GiB_per_socket
K_io = peak_required_IOPS_or_bandwidth / sustainable_IO_per_socket
K_isolation = concurrent_isolated_sessions / safe_slots_per_socket
K_required_socket_equivalents = max(normalized K_cpu, K_ram, K_io, K_isolation)
K_incremental = max(0, K_required - available_reusable_spare - displaced_workload_capacity)
```

For mixed/NUMA/GPU fleets, solve host-placement constraints instead of one global `max`. If there are multiple locations, capacity isn't fungible across them. Count idle **reserved memory** and isolation independently of active core-seconds; cloud billing per vCPU-hour is not a physical CPU utilization measurement. Convert to `new sockets = net usable cores / weighted physical cores per socket` within SKU/ISA pools only.

```
annual_silicon_sales = sum(by buyer, SKU, ISA) annual_cpu_chip_shipments × realized_net_chip_ASP
installed_socket_stock[t] = stock[t-1] + net_installs + replacement_installs - retirement
```

Include replacement CPU sales in annual shipments without treating them as new installed capacity. Cloud-to-on-prem migration needs both released source capacity and receiving location capacity. Keep a dedicated GPU-host BOM CPU pool, which cannot be added again as separate agent execution hardware. Enterprise backend load must be allocated to foundational capacity or genuinely measured incremental pools, not reflexively labeled new dedicated agent racks.

**Independent drivers:** agent adoption, actions/workflow, CPU seconds/action, residency/concurrency, locality/elasticity, architecture-specific efficiency, weighted cores/socket, realized ASP, useful spare fleet, and procurement constraints. Different research vintages should result in immutable forecast runs, not overwritten 'central' values.

## 4. Public source findings and evidentiary status

1. [IDC, June 3 2026](https://www.idc.com/resource-center/blog/leading-through-the-agentic-deployment-era/) **forecasts** 1.15 billion active agents and 217 billion actions/day in 2029. This is neither observed usage nor a CPU-core-seconds metric. Original IDC actions and agent identities need a definition/crosswalk before translation to CPU.
2. [McKinsey 2026 AI survey, Aug 25](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) reports 40% of **large-company respondents** (>$1B annual revenue) and 22% of smaller-company respondents say their organizations scale agents. These are **respondent shares**, not globally measured population adoption rates.
3. [Gartner, June 25 2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) **forecasts** >40% agentic AI project cancellation by end 2027. Production conversion and retention must be modeled, not assumed from pilots.
4. [AMD, May 7 2026](https://www.amd.com/en/blogs/2026/agentic-ai-changes-the-cpu-gpu-equation.html) proposes CPU-centric agent execution racks in addition to GPU hosts and gives **>$120B 2030 server CPU TAM**. Vendor management forecast, already indexed as **T002** in the existing [TAM vintages](../../../data/demand-2030/tam-forecast-vintages.csv). Other AMD and Citi vintages already exist; **no duplicated TAM entries**.
5. [AWS AgentCore, Aug 13 2025](https://aws.amazon.com/blogs/machine-learning/securely-launch-and-scale-your-agents-and-tools-on-amazon-bedrock-agentcore-runtime/) describes dedicated per-session microVMs with up to 8-hour sessions. [AWS docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html) distinguish idle and active session states. One logical microVM does NOT imply one physical CPU socket.
6. [Microsoft Azure Container Apps, Nov 19 2024](https://techcommunity.microsoft.com/blog/appsonazureblog/azure-container-apps-dynamic-sessions-general-availability-and-more/4303561) describes Hyper-V-isolated sessions and **historically** reported Copilot using >400,000 sessions/day then. This is a dated vendor service claim, not 2026 measured demand; [Azure documentation](https://learn.microsoft.com/en-us/azure/container-apps/sessions) describes prewarmed session pools.
7. [Google Cloud, July 9 2026](https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-run-sandboxes-are-in-public-preview/) reports Cloud Run sandbox preview that shares its containing instance's allocated CPU/RAM. Additional logical sandboxes need not create new sockets.
8. [IDC server tracker, updated July 28 2026](https://www.idc.com/promo/servers/) reports $453.531B worldwide 2025 **whole-server-system** spending and Q1 2026 server unit growth of +3.3% YoY. Existing demand module already has this evidence. Neither figure is CPU-only silicon TAM; retain the unresolved 2024 IDC vintage discrepancy.

These public architectures establish **distinct capacity-accounting hypotheses**. Their source announcements do not establish comparable host CPU efficiency, utilization or memory footprints. Measure before ranking or forecasting.

## 5. Transparent, intentionally synthetic sensitivity illustration

Take **only as a premise** IDC's forecast of **217 billion actions/day in 2029**. Suppose all actions execute in server CPU capacity, each action takes the indicated *physical CPU core-seconds*, the physical fleet has 128 usable cores/socket at 65% target utilization, and there is no spare capacity or local execution correction:

```
gross_socket_equivalents = 217e9 × assumed_core_seconds_per_action
                            / (86400 × 128 × 0.65)
```

| Assumed physical core-seconds/action | Gross provisioned physical socket equivalents |
| ---: | ---: |
| 0.1 | ~3,019 |
| 1 | ~30,187 |
| 10 | ~301,872 |
| 60 | ~1,811,231 |

**Synthetic gross capacity only**; *not* annual shipments, incremental sockets, ARM/x86 share, CPU revenue, or a new 2030 TAM forecast. Forecast actions need not be distinct compute invocations. Peak concurrency, memory reservation, I/O, existing capacity, local execution and task elasticity could produce drastically different physical results.

## 6. P0 research and benchmark design

Benchmark successful **consumer browser transaction; persistent assistant; enterprise RAG/document processing; ERP/CRM transaction; customer-support task; regulated workflow; autonomous software change + compile/test; incident response; SaaS-embedded agent; and multiagent delegation**. Repeat each task across a dedicated microVM, shared-instance sandbox, prewarmed pool and private/endpoint hosts when feasible.

Capture task success predicate, retries/failures, workflow ID, execution-event IDs, CPU host SKU and ISA, actual physical **core-seconds** (not only guest billed vCPU-hours), peak and resident GiB-hours, session duration and idle duty, I/O and network, model call locations, GPU host attachment, allocated/provisioned virtual and physical cores, launch latency, concurrency, cost per successful output, energy, utilization and lifecycle. The proposed starting target of 20 repeated runs/config is a *sampling protocol*, not proof of statistical power; estimate uncertainty and increase sample size when needed.

**Research priorities:** P0 [D001](../../../data/demand-2030/priority-data-fields.json) core-seconds/successful workflow incl. failed attempts; P0 **new** RAM reservation and active/idle concurrency; P0 [D002](../../../data/demand-2030/priority-data-fields.json) per-step cloud/local placement and induced demand; P0 [D007/D008](../../../data/demand-2030/priority-data-fields.json) spare/displaced host capacity versus new sockets; P0 [D003/D009](../../../data/demand-2030/priority-data-fields.json) buyer × ISA × cores/socket × realized CPU ASP; P1 [D004](../../../data/demand-2030/priority-data-fields.json) GPU rack host CPU attachment, not additive to standalone sandboxes.

**Proposed—not implemented—data objects:** `agent_demand_segment` (MECE initiating purpose); `agent_workflow_profile` (versioned benchmark execution graph); `runtime_placement_profile` (per-step location, topology, idle RAM and peak concurrency); `segment_demand_projection` (immutable model run, physical stock-flow and silicon value). Extend existing SQLite-first DB design; do not claim schema/ETL/dashboard implementation.

### Falsification / alternative outcomes

Agents can remain mostly lightweight API requests on existing CPU fleets; runtime pooling can reduce required RAM per agent; local tools may remove server execution while creating secondary backend load; Arm/custom CPUs and higher core-density sockets can reduce x86 unit capture; private cloud may simply shift hardware owner; supply, power and project ROI can bottleneck activity. Falsify with host-level task traces, buyer-level procurement, actual ISA/ASP and constrained capacity data—not by tuning assumed core-seconds to a vendor TAM forecast.

**No independently measured per-action server CPU use, per-session RAM footprint, annual agent-attributable physical socket shipment series or verified 2035 CPU revenue forecasts are claimed here.**
