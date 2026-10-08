# Advancing AI 2026 → Server CPU Demand: Research Path

**Date:** 2026-10-08 · **Status:** Research hypothesis and implementation plan, not investment guidance  
**Source event:** AMD Advancing AI 2026, July 23, 2026, full keynote with Dr. Lisa Su and invited partner executives  
**Video:** https://www.youtube.com/watch?v=crEztVjfAPM  
**Transcript identity:** Uploaded English auto-generated transcript, 3,189 lines, SHA-256 `1e5f2be84eff6c3ff81b71564d44f7c4ac0b355141782859e7686e72b866a058`. The transcript is not redistributed in this public repository; line anchors permit auditing against the retained user source and public video.  
**Corpus:** [97 curated claims](../../data/claims/amd-advancing-ai-2026-curated.json) · [all 196 lines containing digits, untriaged](../../data/sources/amd-advancing-ai-2026-numeric-anchors.json).  
**Companion:** [ROCm/x86 research dossier](../ROCM-X86-ROADMAP-2026-2031.md).

## The central question

**Will agentic AI generate a new server CPU demand curve—especially standalone x86 agent-sandbox racks—or will model efficiency, ARM displacement, workload consolidation and local execution offset most of the uplift?**

AMD CEO Lisa Su presented a server CPU TAM moving from a circa `$25B` starting market to **more than `$200B` by 2030** and called for >50% growth; later AMD earnings materials use **approximately `$220B`**. Treat these as **management forecasts with different vintages and rounding**, not observed sales. Neither a keynote nor an analyst projection proves unit volumes, ASPs, margins or x86-specific allocation. Do not sum AMD's ~$2T broad TAM, $1.4T accelerator TAM and CPU TAM: scopes differ and can overlap.

AMD identifies three separate CPU workloads:

1. **GPU/accelerator hosts:** high clock, memory bandwidth, I/O to keep accelerators fed; low unit ratio per accelerator rack but substantial system relevance.
2. **Agent execution sandboxes:** container/VM startup, tool invocation, code runs, browser automation, API gateway, query/retrieval, safety and orchestration; high concurrency and cores-per-watt. **This is the proposed incremental category** and the crux of the forecast.
3. **General-purpose compute:** ERP, database, virtual machines, storage/networking services and associated enterprise AI workloads; existing installed base, cycles, consolidation and cannibalization.

The first dashboard build should surface these three buckets and keep the unit economics separate. For x86, distinguish **AMD EPYC + Intel Xeon** from ARM (NVIDIA Vera, hyperscaler CPUs, Ampere/Arm AGI, Qualcomm). Never equate 'server CPU TAM' with 'x86 TAM'.

## Eight high-priority figures to disaggregate

| Rank | Keynote datum | What must be sliced | Critical methodological caveat |
| --- | --- | --- | --- |
| 1 | `$25B → >$200B by 2030` CPU TAM; later `~$220B` | Year × customer × workload × CPU architecture × shipment units × average realized selling price × contribution margin | Different forecast dates and units; AMD has not publicly supplied a clean audited agent/sandbox TAM breakdown. |
| 2 | New agent sandboxes called 'largest growth' | active concurrent agents × workflows/day × CPU core-seconds/step × memory/agent × duty cycle × machine utilization | Agent count is not CPU threads; agents can wait on network/GPU and run on existing fleets. |
| 3 | `>35 quadrillion tokens/month`, `~160x/2 years` | requests × user/agent × model × input/output/cache tokens × GPU inference × CPU overhead; geographic/provider coverage | Token demand is not a one-for-one CPU demand measure; tokenization definitions and extrapolation missing. |
| 4 | `~60%` of 2026 AI compute capacity allocated to inference | FLOPs vs GPU hours vs spend vs installed power; time evolution; CPU host/standalone split | Denominator undefined, training and inference hybrid serving may be miscoded. |
| 5 | Helios `72 GPUs / 18 CPUs` **official release**; keynote ASR says `75 GPUs` and `>4,600 cores` | SKU × CPU cores × GPU count × per-rack sockets × HBM × power × network × CPU/GPU price attach | Product variant and transcript conflict; do not use inconsistent BOM numbers for cost forecasts. |
| 6 | Venice `96-core HF` / `256-core sandbox` / `128-core enterprise`; `8–256` total range | socket/core count × sustained GHz × DDR/PCIe throughput × workload tier × rack density × SKU ASP | Hardware spec isn't deployed SKU mix or share. |
| 7 | `2.8x` agents/watt vs ARM, `3.3x` rack performance/watt | per-thread proxy vs actual completed agent tasks; measured E2E requests/s; idle and memory constraints; 100kW rack BOM | AMD methodology explicitly uses **CPU threads as proxy for agent capacity**; avoid plotting as real completed agents. |
| 8 | `46%` EPYC server CPU revenue share, `76%` cloud EPYC VM consumption CAGR | revenue vs unit share; product mix/ASP; installed sockets; consumption vs shipment; public/private clouds; price versus margin | Revenue share does not equal unit share; VM consumption is not shipments or vendor CPU sales. |

Other high-signal data from the transcript: Anthropic up to **2 GW** and OpenAI/Meta up to **6 GW each** partnership statements, `34x` MI455 throughput under high concurrency, `18x` token economics vs previous generation, `up to 30%` more Helios rack tokens/$ than comparison system, `3.3x` inference uplift and `2.4x` training uplift attributed to ROCm.ai, `43%` token-cost reduction in AMD's mixed local/cloud demo, and 2028 **Zen 7 Florence/Ferrara/Fidenza** plus 2030 **Zen 8 Ravenna**. Each has its own comparator, workload, event-time status and caveat in the corpus.

### Urgent source-quality issues

- **75 vs 72 Helios GPUs:** transcript [L397–402] seems to say `75`; AMD official launch states **72 MI455X GPUs and 18 Venice CPUs**. **Prefer official BOM** until video/slide crosscheck.
- **96-core CPU + >4,600 Zen6 cores per rack:** transcript [L375–382,L433–438] juxtaposes these numbers. 18 × 96 is not >4,600; may represent different configurations, transcript errors, or aggregate rack variants. **Unresolved**.
- **`$200B+` vs `$220B`**: Keynote [L189–197] and AMD's later earnings discussion differ in precision. Maintain vintage and source URL on both.
- **ROCm / x86:** keynote open software positioning and ROCm.ai improvements apply to GPU programming and heterogeneous deployment; they **do not announce HIP/ROCm device-kernel support on x86 CPU cores**.
- **`agents per watt` denominators:** official AMD footnotes define agent counts as estimates based on CPU threads; `100 kW` modeled rack analyses are not end-to-end agent throughput benchmarks.
- **`120 GB` Ryzen Halo vs `128 GB` later:** transcript [L2630–2634,L2684–2687] requires SKU/slide check.
- **`34x` vs `35x`** inference throughput: keynote [L629–638,L3104–3109], official product claims, precision/concurrency can differ.
- **Product names:** auto-caption `Epic` → EPYC, `Rockom` → ROCm, `Verono` → Verano, `Revena` → Ravenna; preserve transcript source, normalize separately.

## Data models: how to decompose the demand story

### Market value bridge (do not pretend AMD's TAM is x86 revenue)

`Server CPU TAM(t) = Σ_segments [shipped CPU sockets(t) × realized CPU ASP(t)]`

For each segment decompose:
- total server-equivalent compute required
- CPU cores and memory/IO per workload
- socket cores and actual utilization
- average sockets/system and replacement cycles
- share of workloads using x86 vs Arm vs specialized processors
- socket shipments (new workloads, upgrades, displaced sockets, replacement)
- vendor share and product tier/price mix
- revenue vs gross/operating margin (estimate only with labeled assumptions)

Publish low/base/high scenarios with assumptions; never manufacture an unobservable 'agent server ASP' series.

### Agentic CPU demand bridge

`Incremental core-hours = completed workflows × CPU-intensive steps/workflow × measured core-seconds/step ÷ 3600`

`Required provisioned cores = peak concurrent CPU demand ÷ target CPU utilization`

Then translate into rack/sockets after memory, I/O, resilience, isolation and physical power limits. Measure CPU usage while GPU inference is waiting separately to prevent double-counting. Reconcile workload completions, **not runnable containers/threads**, as the economic service output.

Drivers to capture in experiments: workflow length; tool-call count and mix; average vs P95/p99 CPU duration; CPU utilization; concurrency scheduling; sandbox warm/cold start; network waiting; per-agent memory and IOPS; LLM size; context/cache; x86-only binaries; batchability; overhead of authorization/logging/security; container reuse.

### GPU host CPU attach bridge

For each accelerator rack/platform capture:
- system bill of materials (GPU count and model; CPU count/model, memory, NICs, DPUs, storage, power envelope, coolant);
- standalone vs embedded host cores; data ingest/tensor prep/serving orchestration/communications paths;
- host demand expressed as `CPU socket-equivalents per GPU/rack` and `host CPU revenue per $1 of GPU hardware`, with explicit numerator/denominator;
- GPU utilization sensitivity to CPU, memory, I/O and networking; test whether 96 high-frequency cores vs 256 high-density cores changes performance;
- ARM/NVIDIA-host platform substitutions; don't assume all AI accelerators attach to x86.

### Economics and margins

Track separately:
1. **Vendor** x86 server CPU shipments and realized ASP, disclosed AMD/Intel server/DC segment revenue, company non-GAAP adjustments and reported operating income; **CPU-only margins are not generally disclosed**.
2. **Customer** platform price, software license per core, electricity PUE, amortization, memory and storage, rack cooling, paid cloud instances vs self-hosted.
3. **Workload** completed agents/hour, billable token input/output/cache, task success and SLO, completed tool actions / watt / dollar.

Treat public MSRP/1k-unit pricing, realized ASP and confidential hyperscaler pricing as distinct evidence classes; do not infer any private pricing.

## Research work packets — implement in dependency order

### P0-A: Definition and TAM reconstruction

**Questions:** Exactly which sockets are counted by AMD? Which CPU revenue buckets are included? Does $25B refer to 2025, an annualized 2026 baseline, or a selectively defined market? Why did AMD update the forecast from 18–20% toward >50% and $220B by 2030? Is the ~$220B end market addressable spending, shipped product revenue, or a projection including new workloads? 

**Sources:** keynote [L160–197], AMD investor roundtable July 23, AMD Q2 2026 earnings transcript, Q2 earnings release, independent Mercury/IDC/Omdia definitions.

**Deliverables:** `data/markets/cpu-tam-vintages.csv`; vendor-neutral taxonomy; decomposition with full denominators; forecast bridge showing every variable and unknown. **Gate:** can explain forecast without silently treating agents as threads.

### P0-B: Agent task CPU telemetry benchmark

**Questions:** How many CPU core-seconds does a typical agent workflow generate, at what concurrency and core/memory mix? Is the agent sandbox rack truly *net new* spend? Can ARM perform the same tool-execution workloads cost-effectively?

**Tests:** reproducible representative workloads: repository manipulation, build/tests, browser actions, SQL/vector retrieval, file parsing, terminal scripts, API calls, long-running orchestration. Record wall time, CPU time, peak memory, network/gpu idle, IOPS, warm/cold-start overhead and completion accuracy. Compare EPYC, Xeon, Graviton/Vera/other Arm only on comparable real systems and software environments.

**Deliverables:** `research/agent-cpu-telemetry/`, portable benchmark harness spec, workload mix table and share of AI cost attributable to non-GPU CPU tasks. **Gate:** report completed useful tasks/watt and verified billing cost, never synthetic 'agents per thread' as measured throughput.

**Priority note:** the official [AMD EPYC 9006 agentic workload article](https://www.amd.com/en/blogs/2026/agentic-ai-amd-epyc-9005-cpus-wins-today-epyc-9006.html) publishes a detailed stage taxonomy: gateway/stream, context assembly, planning, retrieval, reasoning, ephemeral and enterprise tools, verification. Use this as benchmark **starting material**, not a vendor-neutral measurement.

### P0-C: GPU rack attach and architecture conversion

**Questions:** What share of future GPU systems use x86 vs ARM hosts? What is actual CPU capacity required per GPU for each major inference pattern? How do host CPU spend and agent sandbox CPU spend interact?

**Sources:** official Helios [AMD launch](https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era) (72 GPU /18 CPU), NVIDIA Vera Rubin BOM, public OCP designs, hyperscaler instance/platform specs, OEM sales/technical collateral.

**Deliverables:** `data/systems/rack-bom.csv`, schematic and CPU/GPU/IO attachment matrices, independent CPU/GPU-ratio scenarios; explicitly resolve 96-core/4600-core conflict.

### P0-D: CPU market share × pricing × margins

**Questions:** How much of AMD's server share gain is CPU units vs rising premium ASP? Does future segment mix favor GPU hosts (frequency), sandboxes (core density), or enterprise (lower-power SKU)? Which pieces grow revenue and what costs absorb margins?

**Sources:** Mercury Research broad vs pure-server series, AMD/Intel SEC and quarterly reports, hyperscaler instance disclosures, EPYC and Xeon SKU public 1k prices, TSMC/foundry supply data.

**Deliverables:** separated unit-share and revenue-share timelines; estimated realized ASP bands with uncertainty; pricing and profitability bridge; proof that company segment margins ≠ CPU SKU margins.

### P0-E: Validate key benchmark footnotes

Reproduce AMD's vendor methodology assumptions for `agents/watt`, `100 kW rack`, Helios token/$, MI455 vs MI355, and Venice vs Intel/ARM. Use the [published methods PDF](https://www.amd.com/content/dam/amd/en/documents/solutions/ai/methodology-description.pdf) and launch footnotes; capture benchmark workload, model version, concurrency, token lengths, compiler/runtime, GPU host CPU, prices, power, comparator and date.

**Deliverable:** each benchmark gets a machine-readable measurement card with `vendor_claim`, `reproduction_status`, `independent_confirmation`, `comparability` and warnings. No unlabeled vendor benchmarks on comparative UI charts.

### P1-F: Deployment commitments converted into demand evidence

Record Anthropic (up to 2 GW), OpenAI (up to 6 GW), Meta (up to 6 GW) and other public partnerships as **announced capacities**, separate from shipped, powered, utilized and purchased CPU hardware. Track planned date, region, rack/sockets/BOM, software readiness, agreement terms (if public), risk and cancellations. Cross-reference AMD's 2027 supply expansion statements and foundry/memory lead times.

### P1-G: CPU ISA, ROCm, AI software and competitive displacement

Track:
- x86 EAG ACE → Zen 7 'AI compute extensions' → Intel counterparts → LLVM/GCC/oneDNN/ZenDNN dispatch → measured CPU inference/agent performance;
- ROCm/ROCm.ai/Hyperloom GPU improvements versus **separate** CPU execution backend hypothesis ([existing dossier](../ROCM-X86-ROADMAP-2026-2031.md));
- Arm alternatives: NVIDIA Vera, hyperscaler-designed Arm CPUs, Qualcomm/Arm server entry;
- software portability: existing x86 enterprise dependencies, native ARM builds, emulation/virtualization, binary translation;
- *substitution effects*: low-cost local models and edge inference reduce some cloud demand even while multiplying agent count.

### P1-H: Independent leading indicators and forecast challenge

Collect quarterly new public series: cloud-instance architecture mix, VM hours, agent platform run rates, demand for ephemeral sandbox infrastructure, cloud capex by type, OEM server shipments, CPU SKU availability/list ASP, fab/packaging supply, memory prices, power contracts. Run explicit skeptical scenarios:
1. **Agent abundance**: long autonomous runs multiply CPU workload.
2. **Optimization / reuse**: agents become more efficient; idle waiting and lightweight sandbox reuse reduce CPU per task.
3. **ARM capture**: CPU demand grows, but a smaller portion is x86.
4. **Local migration**: desktop/enterprise/edge agents displace centralized CPU demand.
5. **AI capex constrained**: power, financing and cooling keep dollars below theoretical workloads.

## Dashboard UX requirements

Introduce a dedicated **'AI → CPU Demand'** workbench:

- **KPI strip:** $25B observed/management baseline vs $200B+ keynote vs $220B later guidance; 60% inference compute (ambiguous denominator); >35 quadrillion monthly tokens (AMD estimate), 46% EPYC revenue share (market definition required). Always place exact `as_of`, source, market definition, and `forecast/vendor estimate` label.
- **Three-segment demand flow:** GPU hosts ↔ agent sandboxes ↔ general purpose, expandable to ARM and edge/local, with stack layers (CPU/GPU/ROCm/network/memory).
- **TAM waterfall, not one pie:** workload sessions → CPU hours → cores → sockets → shipments → ASP → CPU TAM; unknown values rendered as striped/unavailable, not 0.
- **Task economics experiment:** sliders for tasks/agent, CPU seconds/task, CPU utilization, rack watts, agent duty cycle, x86 architecture share, purchase/lease pricing; show outcomes as scenarios only.
- **Rack BOM viewer:** Helios, NVIDIA Vera Rubin, Xeon/EPYC generic CPU rack, ARM CPU rack; visually reconcile GPU/CPU ratios and show confidence and BOM assumptions.
- **Claim audit drawer:** click any chart and inspect original source/video timestamp or transcript line range, competitor benchmark methodology, counter-evidence, reconciliation status.
- **Strategic leading indicator ticker:** vendor price/supply, hyperscaler commitments, software shipping status, standards implementations, OEM production vs announced.
- **Contradiction rail:** '75 vs 72 GPUs', '96×18 vs >4600 cores', 'agents as CPU threads', 200B vs 220B, ROCm open vs x86 runtime; none silently auto-resolved.
- **Executive briefing mode:** 30-second market interpretation, 10-minute walkthrough, deep technical view; mobile first and responsive with source footnotes.

### Minimal deliverable order for a local coding agent

1. Validate quantitative and qualitative claim schema, load both corpus files in UI; run integrity tests and label all values as claims. Do not wire live news feeds first.
2. Build **three-lane demand flow** with three vendor-projection source cards and proof-of-definition warnings.
3. Build first TAM waterfall with only sourced anchors, plus user-controlled simulated parameters (no fabricated historical series).
4. Build claim detail modal and source/version ledger.
5. Integrate CPU per agent task benchmark schema and rack BOM, keeping missing data explicit.

## Research standards / gates

Every claim requires immutable source link, source owner/speaker, event date, **as-of**, source line range, metric scope, unit, denominator, segment, status (`measured | vendor_estimate | product_spec | demo | agreement | plan | scenario`), first-party vs independent evidence, and contradictory claims. Treat public source notes and verified financial statements separately from automated-caption transcription.

No unpublished client/company private information; do not upload raw expert-network materials. This corpus is derived from a **public AMD keynote**, not any private consultation.

## Official research starting points

- Keynote video: https://www.youtube.com/watch?v=crEztVjfAPM
- AMD launch and benchmark methodology: https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era
- AMD rack-scale agentic CPU demand: https://www.amd.com/en/blogs/2026/agentic-ai-needs-rack-scale-cpu-performance-amd-epyc.html
- AMD detailed agent CPU benchmark: https://www.amd.com/en/blogs/2026/agentic-ai-amd-epyc-9005-cpus-wins-today-epyc-9006.html
- AMD ROCm 10 & ROCm.ai: https://newsroom.amd.com/news/rocm-10-software-ai-native-developer-experiences/
- AMD EPYC 9006 hardware and caveats: https://www.amd.com/en/products/processors/server/epyc/9006-series.html
- Separate later-forecast source: https://stockanalysis.com/stocks/amd/transcripts/660937-q2-2026/ (seek primary IR webcast/slides)
- x86 ACE: https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/

**Exit criteria for this research pass:** every transcript line with digits indexed; 97 curated numeric claims triaged; first quantitative x86 demand model decomposed into distinct workload segments; conflicting definitions flagged; eight priority figures assigned verification tasks; no unsupported 2030 margin or shipment estimates displayed as actual.
