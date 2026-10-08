# MECE buyer × channel × workload × architecture accounting

Use a **multi-axis cube**, not a sum of loosely defined market categories. This document is the canonical classification contract for all demand data.

## Independent axes and allowed keys

**End economic buyer** (`buyer_id`): 
`hyperscaler_cloud` (AWS, Azure, Google Cloud, Oracle Cloud, Alibaba); `hyperscaler_internal` (Meta and other internet giants for own use); `tier2_regional_csp`; `neocloud_ai_infrastructure`; `model_lab_owner_operator`; `enterprise_large`; `enterprise_mid_smb`; `gov_sovereign`; `research_hpc`; `telco_edge`; `other_unclassified`.

**Procurement channel** (`channel_id`): `odm_direct`, `oem_branded`, `systems_integrator`, `direct_chip_custom`, `managed_service_host`, `reseller_other`, `unknown`. A colocation landlord is not an end buyer unless it owns the computing equipment. A model lab leasing capacity from a neocloud is the *customer* of infrastructure service, while the **owner/operator that purchases CPU hardware** is the direct CPU buyer. Store `service_customer_id` separately so purchased CPU units are never assigned twice.

**Workload** (`workload_id`): `foundational_cloud_vm`, `transaction_database_erp`, `storage_data_network`, `enterprise_virtualization`, `hpc_eda_science`, `ai_accelerator_host`, `cpu_inference`, `agent_sandbox_tools`, `retrieval_vector_etl`, `governance_security_observability`, `sovereign_regulated_compute`, `edge_telco`, `unattributed_other`. At hardware allocation time, all workloads must be allocated fractions of a physical socket totaling at most 100%; workloads do not automatically imply separate socket purchases. For TAM scenarios use **three non-overlapping value pools**: foundational (includes shared infrastructure), AI host (physical CPU attachment to accelerator racks), agent sandbox (net new dedicated capacity only).

**Architecture** (`isa_id`): `x86_amd_epyc`, `x86_intel_xeon`, `x86_other`, `arm_aws_graviton`, `arm_google_axion`, `arm_ms_cobalt`, `arm_nvidia_grace_vera`, `arm_ampere`, `arm_qualcomm`, `arm_other_custom`, `other_unknown`. Hardware architecture is NOT identical to execution OS, runtime backend or host's GPU architecture. AMD EPYC GPU-host + AMD Instinct GPU remains **x86 CPU**; Graviton + GPU remains **Arm CPU**.

**Geography** `country_region`; **ownership** `hardware_owner_id`; **market time** `year`, `quarter`, `fiscal_year_end`; **hardware unit** `sockets`, `cores`, `servers`, `racks`; **measurement** `unit_shipments`, `installed_sockets`, `asp_realized_usd`, `cpu_silicon_revenue_usd`, `whole_server_system_spending_usd`, `capex_usd`. Never compare across incompatible denominators without an explicit mapping.

## Demand ledger accounting rules

### Uniqueness key
`(period, hardware_purchase_event_id, CPU_socket_or_chip_serial, physical_buyer)` when traceable, or aggregate `(period, buyer_id, channel_id, workload_allocation_id, isa_id, country_region, vendor_sku, event_type)` when not.

Each purchased CPU socket records one and only one **economic hardware buyer** and one procurement channel. Service customers are separate commercial relationships; revenue of OEM sellers and hyperscaler buyers describes two sides of **one transaction**, not two markets.

### Revenue reconciliation
`server_cpu_silicon_revenue = Σ(CPU_sockets_shipped × net_realized_CPU_ASP)`.

`all_CPU_revenue = x86_CPU_revenue + nonx86_CPU_revenue + unknown_ISA_CPU_revenue` within the *same market definition*. If the source gives only x86 vs nonx86 complete **server systems**, keep those in a different ledger and never use it to derive chip revenue shares.

Stock flow:
`installed_sockets[t] = installed_sockets[t-1] + new_sockets[t] + replacement_new_sockets[t] - retired_sockets[t]`. Shipments may include channel inventory accumulation; installed stock flow and manufacturer shipments may diverge.

Incremental agent sockets are constrained by actual CPU time and utilization:
`incremental_core_hours = successful_workflows × measured_CPU_core_seconds_per_workflow / 3600 × net_cloud_fraction × (1 + measured_isolation_overhead)`.
`required_installed_cores = peak_corrected_CPU_core_hours / (hours_per_period × target_utilization)`.
`sockets = required_installed_cores / usable_cores_per_socket`.

**Important:** Separately subtract existing spare capacity and displaced workloads; tool workloads can run on existing enterprise or hyperscale CPUs. Do not automatically count incremental tasks as incremental hardware. Memory, storage, compliance and GPU attachment can be binding constraints before cores.

### Workload revenue attribution
Assign each socket a **primary purchased purpose**, with secondary utilization fractions for other tasks; when distributed compute runs on shared infrastructure, primary-purpose allocations sum exactly to one per socket. An agent triggering a database query contributes **additional utilization** to a foundational workload and only adds a new physical socket if constrained capacity expansion is observed or defensibly modeled.

### Channel buyer crosswalk (examples, not exhaustive)

| Buyer | ODM direct | Branded OEM | Custom/direct | Key warning |
| --- | --- | --- | --- | --- |
| Tier-1 hyperscale public cloud | Yes | Yes | Yes | Azure may procure vendor/ODM/OEM products; classify by actual purchase |
| Social/internet hyperscaler | Yes | Yes | Yes | Own-use rack is not AWS/Azure revenue |
| Regional CSP | Some | Common | Rare | Cloud VM revenue ≠ hardware sales |
| Neocloud / AI infrastructure | Yes | Yes | Some | GPU-heavy rack spend ≠ CPU revenue |
| Enterprise / private AI | Less common | Common | Some | OEM ISG income and enterprise CPU demand overlap |
| Government / sovereign | Possible | Common | Possible | Integrator is sales channel, public body end buyer |
| HPC and research | Yes | Common | Possible | Grant/facility procurement vs service compute distinction |
| Model labs | Varies | Varies | Varies | Service customer may not own infrastructure |

## Revenue/margin pools

Keep at least five gross-margin layers separate: `cpu_silicon_supplier`, `memory_network_assembly`, `oem_odm_system`, `cloud_or_neocloud_service`, `application_or_agent_runtime`. A $1 CPU purchase can appear in multiple downstream gross-revenue ledgers; *do not add their gross revenues to estimate chip TAM*. AMD Data Center and Intel DCAI margins include products other than CPUs. Proprietary hyperscaler CPU costs and transfer pricing may not be disclosed.

## Missing values and refusal rules

For any unavailable field, store `null` and `missing_reason`. Do not transform FY into calendar year without explicitly labeling it. Do not fill unknown vendor market share with a residual unless same-source universe sums to 100% and definitions match. Do not use public CPU list prices to infer undisclosed hyperscaler net CPU ASP. Do not infer architecture of an entire AI rack from one host board specification.
