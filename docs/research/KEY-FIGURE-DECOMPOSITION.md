# Key figures — x86 / agentic server CPU demand decomposition

**Source provenance:** AMD Advancing AI 2026 full keynote, July 23, 2026, [video](https://www.youtube.com/watch?v=crEztVjfAPM). Consult [97 claim records](../../data/claims/amd-advancing-ai-2026-curated.json). Company market projections, marketing benchmarks and partner plans remain attributed, not independent actuals.  
**Research date:** 2026-10-08.  
**North-star question:** Is AI infrastructure adding `new x86 CPU spending`, or redistributing workloads, architectures and server values?

## Figure 1 — CPU market TAM + compound growth (P0)

**Source:** keynote L169–197. AMD's earlier forecast was roughly $60B by 2028 (verify year from historic slides), with ~18–20% CAGR. At this keynote AMD describes an approximately $25B starting market and a >$200B 2030 server CPU market growing >50%. Later AMD Q2 commentary cites **~$220B in 2030**.

**Mathematical reconciliation (strictly illustrative, not another market forecast):**

| Hypothetical base year | Base revenue | End revenue | Years | Required CAGR |
| --- | ---: | ---: | ---: | ---: |
| 2025 | $25B | $200B | 5 | 51.6% |
| 2025 | $25B | $220B | 5 | 54.5% |
| 2026 | $25B | $200B | 4 | 68.2% |
| 2026 | $25B | $220B | 4 | 72.2% |

**Why this matters:** The phrase '>50%' is arithmetically compatible with a 2025 baseline but says relatively little about near-term shipments. Verify the starting **year**, whether $25B means actual sales or addressable theoretical demand, and whether TAM prices reflect mix inflation.

**Required slices:** `year × (general-purpose, sandbox, GPU host) × (x86, ARM, other) × socket units × ASP × geography × buyer type`, keeping GPU hardware revenue entirely separate.

**Questions:** How much of >$200B is incremental CPU units, how much premium ASP inflation, how much a newly classified type of agent infrastructure? What is the implicit implied 2030 socket base and foundry capacity? Forecast confidence bands should emerge only from validated model inputs.

## Figure 2 — Agent sandboxes as a new compute class (P0)

**Source:** keynote L938–975 and Meta testimony L1299–1324. The CPU execution path includes tools, code, search/vector database, security, distributed state, data movement, APIs, and agent orchestration. AMD's later commentary describes sandboxes as the prospective largest segment but the smallest today.

**Canonical measurable output:** *successfully completed useful agent workflows*, not threads, containers, active sessions, or tokens.  
For each workload record `task_count, duration_s, CPU_core_seconds, CPU_energy_joules, memory_peak_gb, IOPS, network_bytes, GPU_time, waits, completed_successfully`. Group by language/build, browser automation, knowledge retrieval, SQL, document parsing, tool/API orchestration and security checks.

**Open variables:** concurrency distribution; fraction of active vs idle tools; batching/reuse; virtualization container density; prewarm caching; average duration; P95 CPU time; model placement; enterprise and hyperscaler economics; existing VM fleet capacity. Demand can increase dramatically even if cost/agent falls, or plateau if utilization improves faster than completed-workflow volume.

**UI:** Sankey of one agent task from GPU LLM to separate CPU stages and back, plus sliders for `workflow count × CPU-seconds × duty × utilization`. Never assume every parallel agent needs a physical core.

## Figure 3 — Global token volume and inference share (P0)

**Source:** L47–83. >35 quadrillion tokens/month and ~160x in two years, ~60% of global AI 'compute capacity' used for inference in 2026.

**Slicing grid:** input vs output vs cached vs reasoning tokens; generated vs processed tokens; humans vs agents; training vs inference, small vs frontier models; API/public vs internal private workloads; GPU accelerator compute vs CPU orchestration. **Denominator warning:** '60% compute capacity' is not equivalent to server CPU share, GPU revenue share or CPU time share.

**Critical ratios:** completed tasks / million generated tokens; CPU core-seconds / 1M tokens; inference host CPU load / GPU card; CPU energy cost / request. First measure ratios by workload and concurrency; then scale demand.

## Figure 4 — Helios CPU/GPU attachment (P0)

**Source:** keynote L375–438 plus [AMD official July launch release](https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era). Official base architecture specifies **72 MI455X GPUs and 18 Venice CPUs** (4 GPUs/CPU); the auto-caption says 75 GPUs, describes a 96-core HF board, and claims >4,600 Zen6 cores per rack. **Do not silently harmonize these**: BOM/variant or transcript correction is required.

**Slices:** CPU/accelerator sockets, cores/GPU, HBM/GPU, network throughput, CPU memory/I/O, CPU and GPU list prices separately, rack TDP, cooling and real utilization; compare to NVIDIA Vera Rubin ARM and other racks. `72/18` is a hardware ratio in one AMD configuration, not the share of x86 in worldwide AI racks. Agent sandbox CPUs exist outside this ratio.

**Strategic read:** changing host CPU architecture could erode x86 attachment even while separate agent sandbox racks expand x86 demand.

## Figure 5 — EPYC SKU mix and margin capture (P0)

**Source:** L924–1068 and enterprise L2150–2200. AMD framed three Venice examples: high-frequency 96-core host, 256-core density sandbox, 128-core general-purpose. Entire EPYC family described as 8–256 cores.

**Slices:** list price and realized ASP by SKU/configuration (different evidence quality), cores and default CPU power, memory channel population and costs, clock under load, cache, OEM availability, license-per-core, x86 compatibility, TCO and effective useful-work/$.

**Do not infer CPU-only gross margins from AMD Data Center segment operating margin**: that segment includes GPU and additional products; Intel's DCAI also aggregates lines with differing economics. Reconstruct a range using disclosed segment results plus defensible third-party price/mix evidence, and label all inferred margin estimates as assumptions.

## Figure 6 — 'Agents per watt' and other benchmark headlines (P0)

**Source:** L1073–1129 and [AMD methodology](https://www.amd.com/content/dam/amd/en/documents/solutions/ai/methodology-description.pdf).

The keynote says up to **2.8x agents/watt** vs ARM and **3.3x rack performance/watt**. In AMD's published footnotes, some 'agents' are **estimated from CPU threads used as proxy resources**, not empirically completed concurrent production agents. Rack-level comparisons mix data, modeled assumptions and vendor-selected workloads. The 100kW rack baseline must specify node density, CPU power, server overhead, networking, cooling and rack form factor.

**Research deliverable:** separate theoretical thread/core capacity, standard synthetic throughput, and end-to-end successful agent workflows. Replicate across several actual machines and stop treating marketing proxy as production throughput.

## Figure 7 — Customer momentum, not just headline GW (P0/P1)

**Source:** AMD partners in transcript, plus official releases. Anthropic **up to 2GW**, OpenAI **up to 6GW**, Meta **up to 6GW**; AMD claimed `46%` server CPU **revenue** share last quarter and `76%` 3-year public-cloud EPYC VM consumption CAGR.

**Slices:** commitment signed → hardware order → rack shipped → datacenter powered → deployed → utilization achieved → revenue recognized. For GW announcements capture unit (IT load? contracted capacity? power budget?), campus region, schedule, CPU-GPU attachment and supplier distribution. No GPU-to-CPU conversion without system BOM and power. VM consumption must have instance-hours denominator, independent customer evidence and architecture mix. Do not equate revenue share with unit share.

## Figure 8 — Demand offsets and alternate architectures (P0/P1)

**Sources:** x86 ecosystem and AMD future roadmap; keynote L2550–2700 local model efficiency, L3065–3090 Zen7/Zen8, [ROCm/x86 dossier](../ROCM-X86-ROADMAP-2026-2031.md).

Collect competing effects in a **counterfactual** chart:
- + Agent autonomy and persistent workloads increase CPU tool-compute hours.
- + Workload data preparation, indexing, governance, security and retrieval create CPU-dependent stages.
- + Existing x86 enterprise binaries and developer toolchains can lower EPYC/Xeon adoption barriers.
- – Agent optimization, sandbox reuse and model compression reduce CPU per completed task.
- – Low-cost local execution reduces a portion of central server requests.
- – ARM/vertical integration captures part of GPU host and standalone server growth.
- ± ROCm.ai accelerates GPU programming and throughput; it does **not** announce a full HIP x86 CPU execution device.
- ± Zen7's promised AI compute extensions and x86 EAG ACE could change direct CPU AI execution economics only if hardware, compilers, runtimes and customers deploy them.

**Dashboard task:** show both a 'vendor bullish thesis' and an explicit counter-thesis, each with evidence, uncertainty, assumptions, observable disconfirming signals and as-of date.

## Minimum datasets to collect first

1. `cpu_market_tam_vintages.csv`: issuer/research firm, publication and base year, market scope, revenue vs units, CAGR, forecast, revisions.
2. `workload_cpu_profile.csv`: completed tasks, CPU core-seconds, session latency, RAM, GPU wait, I/O, concurrent task count and source machine.
3. `rack_bom.csv`: GPU, x86 and ARM CPU sockets/SKUs, core counts, power, NIC/DPU, memory, storage and public price bands.
4. `vendor_segment_financials.csv`: AMD/Intel disclosed quarterly revenue, GAAP/segment income and disclosures; not falsely labeled CPU profit.
5. `vendor_cpu_sku_prices.csv`: vendor listed 1k-unit price / OEM list versus independently observed sale price, with dates.
6. `coalition_isa_shipping.csv`: ACE/AVX10/FRED/other standards → actual silicon → compiler → framework → shipment milestones.
7. `amd_cpu_gpu_customer_milestones.csv`: agreements by customer, capacity, deployed MW, racks, realized revenue, independent sources.
8. `software_execution_backends.csv`: ROCm/HIP GPU-host versus CPU-device support, compiler targets, PyTorch/vLLM/ZenDNN, dates.

**Do not fill unknown cells with guesses.** Use `null` with `missing_reason`, and store estimations in scenario tables, not observed fact tables.
