# CORE/SIGNAL — Competitive Capture, Strategic Moves & Market Demand Signals

**Research vintage:** 2026-10-08  
**Scope:** Global server CPU silicon demand to 2030; company/architecture allocation **only**. The existing TAM and demand segmentation are immutable inputs to this study.  
**Status:** Research synthesis and analyst hypotheses; proposed staged intake, **not reviewed/promoted database facts**, neither an investment forecast nor a historical market-share dataset.  
**GitHub home:** https://github.com/owenservera/server-cpu-strategy-lab  
**Public-only:** Do not publish consultation/client information, NDA data, market-research subscription excerpts, contract prices, or confidential partner roadmaps.

## Executive findings

1. **The competition is no longer a two-firm x86 contest with incidental Arm substitution.** There are competing commercial control points: merchant x86 CPUs (AMD/Intel), captive hyperscaler Arm CPUs (AWS/Microsoft/Google), merchant or partner-supplied Arm CPUs (Arm AGI, Ampere, planned Qualcomm Dragonfly C1000), and AI-factory or GPU-system-selected CPUs (NVIDIA Vera, AMD host CPUs and others). A CPU win can result from procurement choice, platform specification or vertically integrated chip design.
2. **Arm is now both an ISA/IP supplier and a direct merchant silicon participant.** Arm launched the AGI CPU in March 2026 with Meta as lead partner; Arm IP revenue and Arm silicon revenue are different, non-additive commercial views. [ARM1]
3. **Qualcomm is a material entrant to monitor, but it is future-dated, not part of observed 2026 merchant share.** Qualcomm and Meta announced a multigenerational Dragonfly C1000 CPU relationship on June 24, with production scheduled to start in the second half of **2028**, not 2026. [QCOM1]
4. **Installed software environments are evolving alongside chips.** Google links GKE Agent Sandbox to Axion N4A; AWS now offers Graviton5 across M9g, C9g and R9g families. These are concrete substrate and workload-qualification signals—not measurements of global CPU silicon share. [GOOG1][AWS1][AWS2][AWS3]
5. **AI-factory CPU attachment is a different competitive decision.** NVIDIA Vera is marketed for standalone agentic racks and Vera Rubin GPU-connected racks. The CPU choice may be imposed by rack architecture, shifting demand away from standalone x86 bidding. Announced customers, system-builder support, samples, real shipments and recurring service capacity must be separately tracked. [NVDA1]
6. **Observed price changes can confound share reasoning.** Intel's Q2 2026 filing states server CPU volume +9% YoY and ASP +48% YoY, dominated by higher premium mix with some pricing actions and internal supply constraints. This is vendor-specific, not Intel overall share gain. AMD's $6.7B Q2 data center revenue includes GPUs and CPUs; it cannot stand in for EPYC-only sales. [INTC1][AMD1]
7. **Mercury unit-share scope is narrower than the problem.** Publicly reported Q2 2026 broad x86 server CPU unit mix: AMD 34.5%, Intel 65.5%, *inside x86*. Different narrower 1P/2P SP share and x86 revenue share are other denominators. None yields merchant-plus-captive Arm market share by itself. [MERC1]

## Existing repository review and boundaries

Reviewed `AGENTS.md`, `RESEARCH-ENTRY.md`, `research/README.md`, `research/catalog.json`, `research/routes.json`, `research/INTAKE-AND-PROMOTION.md`, `research/schema/packet.schema.json`, `docs/STRATEGIC-FRAMEWORK.md`, `docs/EVIDENCE-STANDARDS.md`, `docs/RESEARCH-ROADMAP.md`, `docs/research/demand-2030/README.md`, `docs/research/demand-2030/MARKET-SYNTHESIS.md`, `docs/research/demand-2030/TAXONOMY-AND-ACCOUNTING.md`, `docs/database/ARCHITECTURE-V1.md`, `docs/database/SEGMENTATION-AND-MODELS.md`, and `data/demand-2030/scenario-model.json` (accessed from current main via connected GitHub account).

**Reuse exactly as-is:** Three **mutually exclusive** workload buckets (`foundational`, `ai_host`, `agent_execution`), economic buyer vs procurement channel distinction, forecast vintages, three 2030 TAM paths and quality taxonomy; don't rewrite historical/forecast evidence. 2030 synthetic amounts: downside **$100B** ($30B/$25B/$45B), central **$200B** ($40B/$55B/$105B), upside **$235B** ($44B/$70B/$121B). All synthetic analyst assumptions, not a observed market. Preserve existing x86/nonx86 assumptions as *baseline comparison*, not observations; new competitive scenarios are **parallel allocation overlays** with their own immutable run IDs, not edits to `scenario-model.json`.

**Gap assessment (priority):**

| Gap | Why this distorts decisions | Minimum reproducible evidence | Priority |
|---|---|---|---|
| G01 Direct silicon $ vs internal/captive-equivalent $ vs architecture/royalties | An Arm win can reduce merchant TAM while enriching several different entities | Buyer ownership, invoice/transaction channel, IP license model, benchmark vs merchant quote | P0 |
| G02 Vendor × buyer × workload penetration, not merely x86 share | Captive cloud chips can be invisible in standard merchant/x86 trackers | Cloud instance SKUs/region/GA, customer workloads, installed share with same denominator | P0 |
| G03 AI GPU host CPU selection rules | Bundled rack architectures can lock CPU shares independently of CPU specs | CPU/rack BOM, host sockets/GPU, interchangeability, deployed GPU rack volumes | P0 |
| G04 Verified volume, unit/share/ASP and price mix | 48% ASP growth does not mean 48% pricing power across all buyers | Fiscal filing price/volume bridge, source population, negotiated-price unknown flag | P0 |
| G05 Agent work efficiency and porting costs | High arm64 compatibility does not mean identical performance or zero migration costs | Successful task latency; core-sec, RAM GiB-hours, host occupancy, developer hours, operating images | P0 |
| G06 Non-x86 vendor product execution timing | A planned 2028 CPU must never appear as a 2026 share winner | Datasheets, GA dates, paid system deliveries, first production deployments | P0 |
| G07 Packaging, foundry, memory, supply constraints | Capacity/lead times can dominate architectural economics | Product availability, validated OEM systems, supply announcements, lead times, power/site constraints | P1 |
| G08 Platform software/qualification and compliance | x86 incumbency protects installed enterprise spending | Guest OS, kernel/container compatibility, hypervisor, regulated app certification and migration spend | P1 |
| G09 Regional/sovereign procurement restrictions | Vendors can win selectively even if global cost is inferior | Country eligibility, certifications, local support, supply-chain provenance | P1 |
| G10 Competitive operating behavior, not just quarterly launches | A single launch isn't a sustainable durable win | Price reset frequency, OEM program breadth, field qualification backlog, repeated SKU refresh | P1 |

## The competitive landscape as of 2026-10-08

| Player and strategy | Current strengths / public evidence | Constraints and failure modes | Most exposed demand bucket | Status |
|---|---|---|---|---|
| **Intel Xeon 6 P-cores/E-cores, Xeon 6+ Clearwater Forest** | Broad x86 software/OEM enterprise ecosystem; P-core workloads, differentiated dense E-core scaling; Intel 18A Xeon 6+ up to 288 E-cores, Q2 2026 SKU launch. Q2 2026 filing shows strong premium product mix. [INTC1][INTC2] | Intel 18A and packaging/yield/supply continuity, hyperscaler custom substitution, premium ASP demand elasticity; +48% ASP not unit market-share gain. | Foundational, agent_execution, some AI host | Launched; independent work benchmarks required |
| **AMD EPYC Turin/Venice, Helios** | EPYC density/performance/qualification, TSMC ecosystem, OEM/hyperscaler footprint, first Venice 2nm production ramp announced May 2026. [AMD1][AMD2] | Premium x86 contested by Intel E-core and Arm density; NVIDIA system CPU bundling; AMD corporate Data Center includes Instinct, obscuring CPU-only profitability and ASP. | All three | Venice ramp announced; separate production and field qualification from shipments |
| **AWS Graviton5** | Vertical hardware+software+cloud pricing control, GA M9g general (Jun10), C9g compute (Jun30) and R9g memory (Aug31). [AWS1][AWS2][AWS3] | Mostly AWS cloud captive economics, customer regional/SKU coverage, migration and native deps, no direct merchant CPU invoice. | Foundational and agent_execution | Cloud GA observed; shipment share unavailable |
| **Microsoft Azure Cobalt 200** | Cloud-native Arm virtualization, business app/agent workloads; broad memory/compute shapes. [MSFT1] | Azure-specific, preview vs regional GA, platform compatibility vs x86, customer migration economics | Foundational, agent_execution | Preview, not global GA |
| **Google Axion N4A + GKE Agent Sandbox** | N4A generally available Jan 2026 and Google links agent sandbox deployments to custom Arm capacity. [GOOG1][GOOG2] | Google infrastructure only, unknown internal chip transfer price and share, heterogeneous CPU/GPU co-location | Foundational, agent_execution | N4A GA; product integration signal |
| **Arm AGI CPU** | First Arm-owned production silicon, 136-core max, Meta lead partnership; open ODM/on-prem cloud buyers possible; OCI joins ecosystem. [ARM1][ARM2] | Need physical paid shipment counts, support/ODM qualification, partner-channel incentives; direct Arm silicon business may create channel friction with Arm licensees. | Agent_execution, AI host, foundational scale-out | Vendor announced production-ready; partner pipeline ≠ worldwide shipped units |
| **NVIDIA Vera CPU / Rubin platform** | Standalone agentic CPU rack and integrated Vera Rubin CPU+GPU architecture; data movement/attachment from NVLink; extensive OEM partnerships. [NVDA1] | Vendor performance claims not neutral benchmarks; standalone vs bundled revenue/volume unknown; customers collaborating or planning do not equal recurring deployments | AI_host first, agent_execution emerging | Launched; split integration/shipments by form factor |
| **Qualcomm Dragonfly C1000, Meta partnership** | Oryon-based chiplet agentic/AI-host CPU plans, Meta supplier partnership, Qualcomm full-stack inference portfolio. [QCOM1][QCOM2] | First-gen CPU execution and partner rollout remain future; announced **H2 2028** production; projected perf/watt claims unverified independently | Agent_execution, foundational, AI_host (2028+) | Roadmap/partnership ONLY in 2026 |
| **Ampere / SoftBank** | Arm merchant alternative independent of captive hyperscalers; SoftBank acquired in Nov 2025, regional cloud/enterprise partner opportunities. [AMPR1] | Product competitiveness, OEM routes, software qualification, SoftBank strategic portfolio conflicts, limited independent market-share disclosure | Foundational/agent_execution | Existing commercial Arm CPUs; quantify deployed adoption |
| **Oracle and other clouds** | Important buyers and choice-set providers for AMD/Intel/Arm/NVIDIA; OCI joined Arm AGI ecosystem. [ARM2] | Buying multiple architectures and partnering does not imply any one hardware technology won the full estate | All | Demand allocator, not an ISA |

## Competitive scenario taxonomy: condition → winner → losing opportunity → evidence

All scenarios **conditional stress tests, not forecasts**. Multiple may coexist by buyer and workload; do not assume mutually exclusive market futures unless the simulation explicitly chooses one scenario driver set.

**S01 — Intel recovery within x86:** A renewed enterprise refresh plus Xeon 6+ cloud-density efficiency, x86 application requirements, and credible 18A supply/price execution reduces AMD's x86 share gains and Arm qualification velocity. *Triggers:* independent per-task throughput/watt vs AMD/Graviton under common envelopes; OEM model breadth, long-term inventory availability, renewed cloud instance GA across at least two buyer classes; shipment share in precisely matched Mercury x86 universe. *Alternative:* ASP increase is a premium mix/supply outcome without durable unit win. *Disconfirmation:* consistent x86 shipment-share erosion and inferior normalized workload economics despite price actions.

**S02 — AMD extends its x86 lead:** Venice production ramp translates to qualified large-scale systems and AMD wins both traditional compute refresh and nonbundled AI host sockets, while Intel competes mainly on pricing and some E-core density. *Triggers:* socket-level independent power/throughput, AMD wins in vendor-neutral cloud instances, competitive OEM SKU GA, source-verifiable x86 unit and revenue shares. *Alternative:* integrated GPUs—not EPYC—explain AMD Data Center segment growth. *Disconfirmation:* AMD x86 unit-share flattening with deteriorating CPU-specific realized pricing.

**S03 — Captive hyperscaler Arm expansion:** AWS Graviton5, Google Axion and Microsoft Cobalt broaden SKU/region support and migrate agent/cloud-native capacity from merchant x86. *Triggers:* repeatable task economics (successful tasks/$, watts, RAM bottleneck), 3rd-party public customer migrations, GA in major regions, published cloud platform provisioned share if disclosed. *Winner:* Arm ISA adoption and each hyperscaler's cost position; not necessarily Arm merchant CPU sales. *Disconfirmation:* incomplete software compatibility, migration reversal, x86 discounted total cost dominance.

**S04 — NVIDIA system CPU capture:** New Rubin/Vera accelerated racks ship with an integrated host CPU, locking some AI-host demand to Vera; standalone CPU racks capture agent tool execution where independent CPU bidding was previously assumed. *Triggers:* published OEM rack BOM, shipments, CPU-host ratio, independent successful task density, net customer-operated installations. *Alternative:* customers retain AMD/Intel hosts for independent inference backends and Vera remains limited to tightly bundled systems. *Disconfirmation:* continued freedom of host CPU selection at hyperscale AI deployment.

**S05 — Merchant Arm attacks agent infrastructure:** Arm AGI and Ampere systems qualify beyond native cloud first parties; Qualcomm follows only when C1000 reaches 2028 production and subsequently ships. *Triggers:* accessible OEM commercial catalogs, physical installed instances, agent-runtime benchmarks, public contracts converting to deliveries. *Alternative:* dominant Arm gains remain captive cloud designs; merchant Arm never gains material share. *Disconfirmation:* weak OEM volume or software-porting TCO defeats promised rack density.

**S06 — Heterogeneous, sovereign, regulated market:** Traditional enterprise/regulated workloads maintain x86 qualifications while new inference and agent sandbox workloads prefer Arm or vendor-specific AI host platforms. *Triggers:* actual production certifications, procurement tenders with platform requirements, cloud vs on-prem share by vertical. *Alternative:* even regulated buyers move to approved Arm guest OS/platforms. *Disconfirmation:* Arm obtains broad compliance parity and cost-adjusted enterprise migrations.

**S07 — Supply/price shocks drive temporary shares:** Intel constrained supply, TSMC advanced-node availability, memory subsystem/packaging lead times or software licensing change buying choices independent of benchmark superiority. *Triggers:* reported lead times, supply warnings, OEM substitution policy, vendor volume vs ASP changes, signed order to installed capacity lag. *Alternative:* buyers absorb price hikes without switching due certification lock-in. *Disconfirmation:* after normalization of availability, prior architecture choice returns. [INTC1]

### Demand bucket → likely competitive battleground

- **Foundational** ($40B central 2030 synthetic): Enterprise x86 incumbency (Intel/AMD) vs cloud-native scale-out captive Arm (AWS/Google/Microsoft) vs merchant Arm options. Critical factors licensing, migration labor, memory, idle utilization and OEM support.
- **AI_host** ($55B): AI rack/platform BOM, headnode CPU and memory attachment; NVIDIA Vera vs AMD EPYC / Intel Xeon and any sanctioned independent Arm host. Critical whether platform vendor dictates socket and how many CPUs per actually installed GPU rack.
- **Agent_execution** ($105B): Isolation density, sandbox RAM, CPU-core-seconds per *successful* task, byte movement and guest OS, cloud/local placement; captive Arm, Arm AGI, Intel Xeon 6+ / AMD EPYC, NVIDIA Vera standalone, Qualcomm after 2028. This bucket has **largest hypothetical allocation sensitivity**, not a verified total demand figure.

## Correct allocation model, parallel to existing TAM

**Identity for an approved TAM run**: `TAM_y = sum_w D[y,w]` with `w ∈ {foundational, ai_host, agent_execution}`.

For a compatible market boundary, separate *physical CPU platform allocation* from *financial entity value capture*:

```
D[y,w]                            # USD billion, immutable existing scenario input
R[y,w,buyer]                      # mutually exclusive end-owner revenue allocation, sums to 1
A[y,w,buyer,architecture]         # CPU silicon economic-equivalent allocation, sums to 1
V[y,w,buyer,architecture,vendor]  # mutually exclusive CPU platform attribution, sums to 1
allocated_equivalent_usd_b = D * R * A * V
```

Architecture vocabulary: `x86`, `arm`, `other_nonx86`, `unidentified`. Vendor attribution examples: `amd_epyc`, `intel_xeon`, `aws_graviton_captive`, `msft_cobalt_captive`, `google_axion_captive`, `arm_agi`, `ampere`, `qualcomm_dragonfly`, `nvidia_vera`, `other`, `unidentified`. `x86` may not imply Intel or AMD when niche vendors are observed. Vendor attribution must use buyer-compatible candidates and dated product eligibility (e.g., Qualcomm C1000 production before 2028 is **ineligible**).

**CRUCIAL ACCOUNTING:** The `allocated_equivalent` is **not** directly invoice revenue for captive CPU designs. Compare physical CPU value-equivalent *exposure* using a clearly stated synthetic transfer-value convention; show separate ledger of (a) observed external merchant CPU manufacturer net silicon revenue where independently supportable, (b) synthetic captive CPU equivalent, (c) IP royalties/licenses, (d) cloud service or GPU system revenues. Do not sum (b), (c), (d) on top of the same total CPU silicon TAM. When a market definition excludes captive chips, an internal CPU *value-equivalent* must not be called confirmed merchant market revenue. Report `unknown_scope` where a denominator is unavailable.

Vendor revenue allocation scenario must be in **revenue dollars**, not unit market share; shipment-share series can constrain a model *only* after reconciling vendor ASP by workload/owner/architecture. If `R`,`A`,`V` are unavailable, produce null/unidentified outputs rather than invented full-share distributions. Partner logos, cloud VM SKUs and chip spec rankings are directional evidence only, not precise shares.

### Anchored sensitivity without inventing vendor market shares

Under existing **central 2030** demand row ($40B foundational / $55B AI host / $105B agent execution), shifting **10 percentage points of a single workload bucket's captured silicon-value allocation**, while keeping its total fixed, moves the equivalent of **$4.0B / $5.5B / $10.5B**, respectively. This is purely the algebra of an assumed 10-point shift; it is not evidence of plausibility. For each shift subtract exactly the same amount from an identified competing destination; `unidentified` is permitted only explicitly, never silently assigned to favored vendor. Never automatically translate revenue-dollar shares to sockets, shipments or gross profit.

**Model scenarios should be differentiated by drivers, not arbitrary winners.** Rather than pre-populating AMD 30%, Intel 30%, Arm 40% with no evidence, encode conditional preference priors as **unknown** and let eligible workload economics + actual customer implementation data determine possible range. Scenario names are narrative *conditions* and independent allocation deltas, not a fabricated market-share forecasting table.

## Reproducible competitive inference method

1. **Define market grain and observation universe**: date, quarter, country/region, buyer/economic equipment owner, application workload, SKU/ISA, merchant vs captive, unit vs silicon USD, procurement channel, shipment/installation/cloud-instance state.
2. **Map qualified choice sets**: for each buyer×workload×deployment context, list legally and technically available CPU designs, selected OS/container/hypervisor stacks, accelerator attachment and reference racks. Mark qualification phase `announced → sampled → validated → GA/qualified → contracted → delivered → deployed → measured-utilized`.
3. **Collect normalized task-cost evidence**: `successes/hour`, `p50/p99 latency`, `core-seconds/success`, `memory GiB-hour/success`, `energy joules/success`, `rack throughput per fixed kW`, failure/retry, migration labor, software licenses. Test across at least two replicates and document kernel, compiler, runtime and image architecture. SPEC CPU 2026 is a baseline, not a substitute for agent-task or production transaction benchmarks. [SPEC1]
4. **Translate to buyer economics**: `effective_TCO = hardware purchase amortization + memory/network/energy/cooling + software/license + operations + migration + downtime / qualified successful workload throughput`; normalize wall-clock, SLA, utilization and geographic energy prices. Cloud VM hourly advertised price is **not** CPU silicon ASP.
5. **Infer choice probabilities, not premature point share**: compare matched alternatives by net benefit and switching hurdle. Fit discrete choice only once observed dated customer deployment/purchase wins exist. Until then, report best/worst viable outcomes with transparent eligibility and price constraints.
6. **Connect to physical shipments**: stock→new build+replacement−retirement, chip/socket per system and purchased vs leased ownership; keep gross system spending, CPUs, accelerators, and merchant foundry services distinct.
7. **Backtest as-of vintages**: freeze 2026 assumptions; see whether actual subsequent GA, shipments, cloud expansion and Mercury data confirm leading signal directions. Prevent hindsight leak; measure prediction accuracy, false positives, and time from announcement to commercial deployment.
8. **Uncertainty**: show evidence class P1–P6, publication date, exact scope/denominator, access type, quantified low/base/high only from justified priors or ranges. Correlated drivers (hyperscaler share and migration intensity; GPU rack designs and CPU attach ratios; cost and chip ASP) must not be independent by default.

### Signals (track cross-company comparables, not press release counts)

| Signal ID | Indicator, numerator/denominator | Frequency | Leading / lagging | What changes the conclusion? |
|---|---|---|---|---|
| SI01 | # qualified paid merchant CPU systems by vendor and OEM (exclude announced SKUs) | monthly/quarterly | leading | More buyer breadth strengthens durable commercialization |
| SI02 | # cloud regions+families GA and public arm64 customer production cases | monthly | leading | Expanded options make captive Arm migration feasible |
| SI03 | Realized x86 server CPU unit and revenue share with *same* denominator and fiscal basis | quarterly when public | lagging | Validates AMD vs Intel competition only within x86 |
| SI04 | Client vendor CPU server volume and ASP bridge, by company filing | quarterly | mixed | Distinguishes scarcity/mix/repricing from physical unit adoption |
| SI05 | Independently measured successful agents per rack kW/GiB-hour on eligible CPUs | monthly experiment | leading | Reorders which CPU architecture has lowest qualified TCO |
| SI06 | CPU host attachment in certified accelerator rack BOM × deployed rack counts | per rack launch + quarterly shipments | leading/lagging | Quantifies NVIDIA/AMD/Intel CPU exposure to GPU ecosystem |
| SI07 | Major app/OS/compliance certifications by architecture and date | event-driven | leading | Removes enterprise Arm barriers or deepens Intel/AMD lock-in |
| SI08 | Design collaboration → samples → production → paid shipments for newcomers | event-driven | leading/lagging | Decides whether Arm AGI/Qualcomm CPU plans convert to true share |
| SI09 | Chip availability, supply warnings, lead time and actual delivered SKUs | monthly/quarterly | leading | Isolates supply-led from workload-led switches |
| SI10 | Cloud VM total customer price per successful task + system energy | monthly | leading | Does Arm cloud price advantage survive real-world constraints? |
| SI11 | Merchant-vs-captive CPU ratio for same *measured buyer portfolio* (often unavailable) | annual | lagging | Corrects denominator for addressable merchant CPU market |
| SI12 | Closed inference host operators, weight-IP owner, system/rack procurement owner | quarterly | leading | Prevents double-counted model lab, neocloud and hyperscaler purchases |

## Priority research queue and proposed falsification activities

**P0-A: Build vendor/buyer SKU qualification map** (one week of bounded public-source work). Collect current EC2 Graviton/EPYC/Xeon catalogs, Azure Cobalt/EPYC/Xeon, GCP Axion/x86, OCI and OEM certified server platforms with exact GA/region/status, SKU, guest OS and instance price sheet date. Report eligible choice sets, *not purchased market share*. Assign confidence and dated eligibility.

**P0-B: Build vendor evidence scorecards**. One page each Intel, AMD, AWS Graviton, Microsoft Cobalt, Google Axion, Arm AGI, Ampere, NVIDIA Vera, Qualcomm Dragonfly; each must include value-proposition, moat, constraint, quantitative independent tests, named customer deployment stage, direct/indirect revenue boundary, next thesis-breaking event.

**P0-C: Establish mixed platform benchmark harness.** Select two candidate workload bundles: (i) scale-out API+PostgreSQL+cache and (ii) agent code/test sandbox running real successful tasks. Fix concurrency, p99 latency, memory limit, image/kernel/compiler/runtime, failure criteria and power accounting. Test x86 Intel, x86 AMD and Arm where resources available. Publish configuration hashes; report missing options transparently.

**P0-D: Resolve market-share crosswalk.** In a licensed/public compliant manner, isolate `Mercury Q2 broad x86 server unit`, `Mercury narrow SP 1P/2P`, `x86 server CPU revenue`, `all-ISA chip unit` and `hyperscaler internally designed CPU share` as distinct universes. Never interpolate Arm into x86 without same denominator and real units.

**P0-E: CPU GPU-rack host BOM audit.** Sample vendor Helios, Vera Rubin, and other OEM accelerator reference architectures. Mark mandatory bundled CPU, optional interchangeable host CPU, host core count, number of physical CPU packages per rack, announcement vs installed. Obtain public deployment evidence before extrapolation.

**P1-F: Competitive strategy event ledger**. Capture launches (date/scope), OEM validations, cloud GA, co-design announcement, hyperscaler instance catalogs, partner contracts, first paid deliveries, price/volume bridge, and counterevidence. Add review states, `last_seen`, `next_expected`, predicted directional competitive allocation and specific falsification.

**P1-G: Price/economics crosswalk**. Public list SKU price, OEM complete system net-of-support (if public), cloud VM per-hour, per-successful-task, power/RAM/TCO. Contracts and CPU ASP remain unknown absent sourced disclosures. Use sensitivity ranges, not pretend list prices are realized ASPs.

## Dashboard and database overlay design (additive, not a market-model change)

**Recommended separate module:** `docs/research/competitive-capture/` plus *one* multipath packet. Add catalog pointer and linked strategy questions in `cpu-platforms-and-competitors`, `market-demand-2030` and `architecture-and-software`. Do not create an incompatible second demand taxonomy.

**Proposed data entities** (staged research collections first; evolve SQLite v1 only after code/DB review): `competitive_platform` (vendor, ISA, merchant/captive, lifecycle), `choice_set` (buyer×workload×deployment×date), `qualification_event`, `competitive_signal` (source/status/alternative), `benchmark_case`, `scenario_driver` (conditional trigger + direction), `capture_allocation` (run×bucket×buyer×platform revenue weights), `commercial_boundary` (actual silicon $/hypothetical captive equivalent/IP/cloud service), `allocation_lineage` (source+revision+model run).

**Dashboard panels:** (1) Architecture share vs direct economic capture; (2) vendor/CPU choice-set matrix by buyer and workload; (3) launch-to-GA-to-delivery progress timeline; (4) scenario shock explorer with locked TAM totals, waterfall redistribution and explicit unidentified; (5) strategic early-warning signals ranked by evidentiary maturity; (6) loss pathways—what could undo incumbent advantage; (7) assumption/provenance/contradiction pane. Tooltip must always show denominator/metric, source and status, and why result is conditional.

**Acceptance criteria:** all modeled vendor allocation weights sum to 1.000000 per exclusive partition; all 2030 workload dollars reconcile to $100B/$200B/$235B input case, without mutating any existing model; x86 and Arm unit share never mistaken for server CPU revenue share; merchant invoices not added to captive equivalent or royalty/cloud rev; future 2028 CPUs prohibited from historical 2026 realized shipments; source as-of dates never silently updated; unresolved allocations explicitly unknown. Snapshot tests must include zero/NULL share, no-eligible-vendor, sum>1 rejection, stress transfer conservation, platform-phase downgrade, shared actor (Meta both partner/customer), and duplicate channel view.

## Known uncertainties and qualifiers

- This report relies primarily on vendor filings, cloud feature blogs and public secondhand Mercury market-share reporting; **vendor comparisons are not independent normalized workload benchmarks**.
- As of 2026-10-08, public auditable all-ISA all-world server CPU chip unit/revenue share with captive equivalent value is not established here. Do **not** fill missing values with press-release claim counts.
- CEO comments, partnership amounts, 2028 production plans and SKU launches indicate commercial intent—not 2026 revenue, margin or physical deployment.
- Intel's +48% YoY ASP is a vendor-quarter mix effect, not market ASP; AMD's $6.7B Data Center figure includes accelerator revenue.
- The existing 2030 three-bucket TAM and x86 split are synthetic; retention preserves the analysis contract but does **not** imply forecasts are independently validated.
- A technically good Arm processor may capture no merchant CPU revenue if the end customer buys proprietary cloud CPU capacity; an Arm licensing or royalty win is not a second full CPU sale.
- Microsoft Cobalt 200 was in **preview** in the retrieved official announcement; no globally GA Cobalt 200 claim is made here.
- Qualcomm Dragonfly C1000 was announced with **production planned H2 2028**, making it a roadmap leading indicator until stronger deployment evidence exists.

## Source registry (public links; claim-level verification must precede promotion)

- **[INTC1]** Intel Q2 2026 SEC 10-Q (published July 2026): https://www.sec.gov/Archives/edgar/data/50863/000005086326000157/intc-20260627.htm
- **[INTC2]** Intel Xeon 6+ product catalog / Q2 2026 launch: https://www.intel.com/content/www/us/en/products/details/processors/xeon/6-plus-series.html
- **[AMD1]** AMD Q2 2026 results, Aug 4 2026: https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results
- **[AMD2]** AMD 2nm Venice production ramp, May 21 2026: https://newsroom.amd.com/news/amd-announces-production-ramp-of-next-generation-a/
- **[MERC1]** Tom's Hardware, Aug 22 2026, public secondary reporting on Mercury Q2 2026: https://www.tomshardware.com/pc-components/cpus/desktop-cpu-shipments-crater-20-percent-amid-high-component-costs-but-amd-gains-record-share-despite-ugly-desktop-processor-market-intel-floods-laptop-market-with-millions-of-cpus-but-amd-still-sets-all-time-share-records
- **[AWS1]** Graviton5 M9g GA, June 10 2026: https://aws.amazon.com/blogs/aws/now-available-amazon-ec2-m9g-and-m9gd-instances-powered-by-new-aws-graviton5-processors/
- **[AWS2]** Graviton5 C9g GA, June 30 2026: https://aws.amazon.com/blogs/aws/amazon-ec2-c9g-and-c9gd-instances-powered-by-aws-graviton5-processors-are-now-available/
- **[AWS3]** Graviton5 R9g GA, Aug 31 2026: https://aws.amazon.com/blogs/aws/amazon-ec2-r9g-and-r9gd-instances-powered-by-aws-graviton5-processors-are-now-generally-available/
- **[GOOG1]** Google Axion N4A VM GA, Jan 27 2026: https://cloud.google.com/blog/products/compute/axion-based-n4a-vms-now-in-preview
- **[GOOG2]** Google agent sandbox + Axion reference, Google Next 2026: https://cloud.google.com/blog/products/compute/whats-new-in-compute-at-next26
- **[MSFT1]** Azure Cobalt 200 VMs preview, June 2026: https://azure.microsoft.com/en-us/blog/new-azure-cobalt-200-vms-deliver-50-performance-improvement-fully-optimized-for-modern-agentic-ai-workloads/
- **[ARM1]** Arm AGI first direct CPU, Meta lead, Mar 24 2026: https://newsroom.arm.com/news/arm-agi-cpu-launch
- **[ARM2]** Arm AGI Oracle ecosystem statement, June 2 2026: https://newsroom.arm.com/news/arm-agi-cpu-oracle-cloud-infrastructure-agentic-ai
- **[NVDA1]** NVIDIA Vera CPU launch March 16 2026: https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai
- **[QCOM1]** Qualcomm–Meta June 24 2026, Dragonfly C1000 H2 2028 production, public syndication: https://www.nasdaq.com/press-release/qualcomm-and-meta-announce-strategic-multi-generation-agreement-data-center-cpus-2026
- **[QCOM2]** Qualcomm investor release June 24 2026: https://investor.qualcomm.com/news-events/press-releases/news-details/2026/Qualcomm-Accelerates-Diversification-with-Comprehensive-Strategy-for-Data-Center-and-Sees-Multiple-Inflection-Points-Over-the-Next-3-to-5-Years/default.aspx
- **[AMPR1]** SoftBank Ampere acquisition announcement/closure and regional OEM deployment need primary source confirmation before market-series promotion; see previously existing competitor roadmap and perform subsequent source intake; no numeric Ampere share claimed here.
- **[SPEC1]** SPEC CPU 2026, May 5 2026: https://www.spec.org/pressreleases/2026/20260505-spec-releases-cpu-2026-benchmark-suite/

**Publication state:** Research study in the public repository; related typed research packet remains staged for review. No existing TAM, historical shipment dataset, or dashboard actuals were changed. Consult `RESEARCH-ENTRY.md` for the promotion gate.