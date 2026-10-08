# Segmentation and market model semantics

## Orthogonal axes

A physical CPU hardware purchaser belongs to an economic **end buyer** class (hyperscale public cloud, social internet hyperscaler, Tier-2 CSP, neocloud, enterprise, sovereign/government, research, telco). A separate **channel** axis records ODM/direct, Dell/HPE/Lenovo/Supermicro-style OEM, integrator, reseller or direct silicon. A third **workload** axis describes what cores do, and the **ISA** axis distinguishes EPYC/Xeon x86 from Arm/custom CPU architectures. Geography, purchase vs deployment date and service customer are additional axes.

**OEM revenue and hyperscaler hardware purchases are generally two views of the same economic transaction, not additive markets.** An agent triggering a database query on a shared cloud server also doesn't cause a separate socket sale unless additional demand crosses the available-fleet capacity boundary.

Hierarchies are useful for drilling down; they are **not automatically MECE partitions**. Example: 'AI inference' and 'agent runtime' may consume the *same* core-seconds. Use explicitly reviewed `partition_frames` when a sum to 100% must be guaranteed, and label unconstrained multiple tags as non-additive.

## Market boundary before numerical value

Every metric/market scope states whether it refers to:
- `cpu_silicon` (chips/sockets/revenue),
- `server_system` (full rack/server spending including memory/network/GPU),
- `corporate_financial` (vendor segment totals, gross income, capex),
- `cloud_service` (customer spending/VM-hours),
- `fleet_capacity` (cores/MW/racks),
- `workload` (tasks/core-seconds/tokens), or
- `unresolved`.

Never convert IDC x86 *full server systems dollars* into x86 *CPU silicon TAM* by equating their values. AMD Data Center GPU+CPU revenue cannot be used as EPYC-only revenue. Forecasts, speculative assumptions, declared product specs, and independently measured benchmarks need different evidence statuses.

## Bottom-up micro → macro bridge

Start from successfully completed workflows, not tokens or SMT threads:

```text
core_hours = workflows × CPU_core_seconds_per_successful_workflow / 3600
incremental_cloud_core_hours = core_hours × cloud_execution_fraction × (1+measured_isolation_tax)
cores_needed = peak_adjusted_core_hours / (hours_in_period × target_utilization)
net_new_cores = max(0, cores_needed - available_spare_cores - displaced_workload_cores)
new_sockets = net_new_cores / usable_physical_cores_per_socket
x86_sockets = new_sockets × x86_hardware_share
x86_cpu_silicon_revenue = x86_sockets × realized_net_x86_ASP
```

Each multiplication uses a **separate input record**, measured or assumed, with source, unit and low/base/high confidence. CPU/GPU host attach is a separate physical BOM branch (`host_CPU_sockets_per_rack × deployed_racks`) and must not be counted again as standalone agent execution. Local endpoint CPU hardware revenue is not server CPU TAM.

### Model dimensions to slice

Year (2024–2030), final hardware buyer, channel, ISA, CPU cores per socket, usage tier (general compute, accelerator host, agent sandbox), company/vendor, geography, cloud/local placement, workload, rack power, OEM/ODM margin layer and lifecycle/refresh type. Not all combinations have source evidence: the query planner must return **missing/unidentifiable**, not invent a complete multidimensional market cube.

### Reconciliation

```text
global_server_cpu_silicon_TAM
  = foundational_CPU_revenue
  + AI_host_CPU_revenue
  + net_new_dedicated_agent_CPU_revenue
x86_CPU_revenue + non_x86_CPU_revenue = total_CPU_revenue
```

These equalities only apply to models declaring the three buckets **mutually exclusive within one market definition**. Physical socket stock flow must reconcile installations, retirements, replacement and manufacturing/channel inventory changes separately. Do not count a stock snapshot as annual chip shipment flow.

V1 stores synthetic 2025–2030 scenario rows independently from real/future reported estimates and checks the subtotals. Its parameters are illustrative; it does not imply that AMD's >$220B 2030 estimate or Citi's later approximately $300B forecast is an observed or hard upper bound.

### Value of new evidence

Prioritize core-seconds per *successful* agent task, endpoint/cloud placement share, GPU host CPU attachment, source-verified CPU shipments and realized ASP, buyer-specific ISA mix, OCI/AWS/Azure/GCP actual available instance mapping, isolation overhead and fleet spare utilization. Those variables can change the x86 2030 output more than another repetition of a vendor keynote.

### Model uncertainty and evolution

Store a dated, immutable **model run** for each scenario; don't rewrite 'central' when inputs change. Add a new run and `revises` lineage. Future releases should support interval estimates, correlated assumptions and Monte Carlo/backtesting, with scenario and observed results never occupying the same UI series without explicit labels.

See [existing source taxonomy](../research/demand-2030/TAXONOMY-AND-ACCOUNTING.md), [existing model JSON](../../data/demand-2030/scenario-model.json) and [research gaps](../research/demand-2030/DATA-DICTIONARY-AND-GAPS.md).
