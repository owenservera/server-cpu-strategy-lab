# Server CPU Pricing Observatory — strategic economics and reproducible estimation v1

**Research as-of:** 2026-10-08 · **Status:** methodology and staged public-source intake, **not verified net transaction-price model**.  
**Entry:** [RESEARCH-ENTRY](../../../RESEARCH-ENTRY.md) · **Packet:** [2026-10-08 pricing-economics](../../../research/packets/2026-10-08--server-cpu-pricing-economics.json) · **Database:** [v1 architecture](../../database/ARCHITECTURE-V1.md) · **Demand bridge:** [segmentation/models](../../database/SEGMENTATION-AND-MODELS.md).  
**Scope:** AMD EPYC versus Intel Xeon x86; Arm/custom silicon as the supplier/buyer outside option. Only publicly accessible evidence. Do **not** include the initiating consulting screenshot, client details, private former-employer experience, negotiated nonpublic discounts, or other restricted information.

## Decision thesis: price is not one number

The primary research question is **what semiconductor revenue each supplier realizes per physical CPU and why, what each purchasing layer pays, and how this translates into the buyer's cost per validated unit of useful compute**. This resolves the ambiguities in “ASP trends, discounting and hyperscaler vs enterprise pricing” without mistaking a reference price for an invoice, cloud rental rate or outcome.

| Price layer / observable | Economic meaning and denominator | Evidence / trap |
|---|---|---|
| **A. Reference / 1KU / RCP** | USD per identified Xeon/EPYC **CPU package**, as-of vendor publication and quantity rule | [Intel specifications](https://www.intel.com/content/www/us/en/products/sku/246074/intel-xeon-6990e-processor-576m-cache-2-20-ghz/specifications.html), [AMD EPYC specifications](https://www.amd.com/en/products/specifications/server-processor.html); public guidance **not** realized sale |
| **B. Semiconductor invoice / contract** | Gross price invoiced to OEM/ODM or CSP per qualified chip and contractual quantity | Usually private; contract language and programs differ |
| **C. Net realized semiconductor ASP** | Net recognized CPU-only revenue / **physically sold CPU units**, accounting for rebates/credits/revenue reductions | If both numerator and denominator are unavailable, **not identified**; Intel DCAI and AMD Data Center totals are not a pure CPU numerator |
| **D. OEM option / channel shadow price** | Incremental configured-server charge for replacing a CPU, per server option | [Dell R770](https://www.dell.com/es-es/shop/servidores-almacenamiento-y-redes/poweredge-r770/spd/poweredge-r770/promo_r770_2?view=configurations) / [R7725](https://www.dell.com/es-es/shop/servidores-almacenamiento-y-redes/poweredge-r7725/spd/poweredge-r7725/gl_promo_per7725_1); adjust forced heatsink/PSU/RAM changes and base SKU |
| **E. Awarded enterprise system price** | Paid full BOM/support/package value / **number of equivalent servers** | Public tender with line-level configuration, buyer, location, taxes, services, quantities. **Not CPU-only** |
| **F. Cloud instance rental** | Public VM rate / provisioned vCPU-hour or instance-hour | Indirect buyer substitute/rent signal; shared fleet depreciation, margin, network, RAM, reserved pricing and utilization confound chip acquisition |
| **G. Workload economic cost** | 3–5-year total cost / SLA-qualified completed tasks or measured throughput-time | Procurement target; license costs, full-server power, fleet efficiency and switching may dominate nominal CPU price |

**Unit guardrails:** physical packages != sockets populated != cores != SMT threads != virtual CPUs != servers != racks != GPU hosts. One two-socket system can contain two chips; AMD chiplets are not independent merchant CPUs. For market accounting, uniquely assign each CPU shipment to the physical purchasing event; OEM/ODM resales and cloud end consumption are **not** additional silicon units.

A conceptual semiconductor **revenue-recognition** waterfall is:
```text
vendor_reference_price (observed anchor, NOT booked revenue)
   [not a direct accounting reconciliation]
invoice/contract consideration (usually unobserved)
 - applicable revenue-reducing rebates, incentives, credits and price protection
 = net semiconductor consideration recognized, subject to accounting policy
 / shipped CPU units for the SAME product scope and period
 = CPU net realized ASP (only if both terms are identifiable)
```
[AMD FY2025 10-K](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm) explicitly discusses customer incentives and variable consideration; not every marketing program necessarily reduces revenue, so classify each agreement/accounting treatment rather than subtracting all spending. This waterfall is a taxonomy, **not** proof that the components or net price are public.

## Findings worth preserving as separate observations

| Source-reported Intel server ASP YoY | Value | Source-reported driver and caveat |
|---|---:|---|
| FY2022 vs FY2021 | **−5%** | Higher hyperscale customer-revenue mix. [2022 10-K](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-23-000006/intc-20221231.htm), DCAI Revenue Summary |
| FY2023 vs FY2022 | **+20%** | Lower hyperscale customer mix + higher high-core-count product mix. [2024 10-K](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-25-000009/intc-20241228.htm); confirm historical comparative passage |
| FY2024 vs FY2023 (FY2025 comparative disclosure) | **+11%** | High-core-count mix, per [Intel 2025 10-K](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000011/intc-20251227.htm); pending separate locator audit |
| FY2024 vs FY2023 (original FY2024 10-K) | **+12%** | Different original vintage; see [Run 01 conflict](RUN-01-2026-10-08.md); do not chain without reconciliation |
| FY2025 vs FY2024 | **−4%** | Pricing actions and lower-core-count mix, same 2025 10-K; pending separate locator audit |
| H1 FY2026 vs H1 FY2025 | **+38%** | Premium mix dominates, demand pricing smaller. [Q2 2026 10-Q](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000157/intc-20260627.htm) |
| Q2 FY2026 vs Q2 FY2025 | **+48%** | Q2-only comparison in the same filing, **not a further +48% sequential increase** |

**Reading:** These are reported aggregate ASP changes, not a matched-SKU price index. Intel said Q2 2026 server volume rose 9%, chiefly from hyperscaler demand, even as premium mix and available-supply constraints contributed to higher aggregate ASP. Consequently, neither “hyperscalers pay 30% less” nor “CPU prices rose 38%” follows from these data. Annual percentages can form a labeled **reported-ASP-change chain** only after fiscal series checks; do not chain an H1 YoY or Q2 YoY number onto the annual index. No absolute Intel net ASP dollar value has been established.

**Immutable reference anchor:** AMD's [Oct 10 2024 EPYC 9005 launch SKU table](https://www.amd.com/en/newsroom/press-releases/2024-10-10-amd-launches-5th-gen-amd-epyc-cpus-maintaining-le.html) reports **EPYC 9965, 192 cores, 500W, USD 14,813 at 1KU**. A later [live SKU page](https://www.amd.com/es/products/processors/server/epyc/9005-series/amd-epyc-9965.html) was reported to display **USD 11,988**; treat this as *unconfirmed live-page evidence* until its 2026 as-of, currency/region and archived content are captured. Even a genuine reference-price drop says nothing definite about AMD's average booked contract revenue. Save both snapshots; never replace one with the other.

## Supplier-side framework: how Intel and AMD set/defend price

Treat pricing as constrained portfolio optimization, **not** maximizing sticker price per SKU:

```text
Expected contribution = Σ_(SKU,buyer,quarter) shipped_units ×
    (net_realized_price_per_cpu − variable_silicon/packaging/test/logistics_cost)
```

Maximize subject to wafer/die yield, CCD/compute-tile bins, package and substrate supply, test capacity, lead time, qualified OEM platforms, long-term purchasing commitments and customer opportunity cost. For a constrained input, rank opportunities by **contribution per scarce input-unit** (e.g. test hour/package capacity), not simply $/CPU. Gross margin includes allocations and is **not** identical to contribution.

Pricing levers and segmentation controls:
- **Technical:** core count and P-core/E-core/Zen5c/Zen5 distinction; cache, frequency, memory capacity/bandwidth, PCIe, coherency, socket count, NUMA, security, TDP, workload throughput and density, qualification.
- **Commercial:** annual volume commitment, forecast accuracy, supply reservation, sourcing alternative, architecture porting cost, rebates/price protection/marketing consideration, channel layers and lifecycle timing.
- **Strategic:** premium generation anchoring, defender share versus gross profit, utilization/yield, product launch ramps, volume-risk sharing, custom SKU/ASIC and Arm alternatives, software/platform ecosystem.
- **Supply:** when capacity is unconstrained, incremental low-price share may be attractive; when constrained, discounted deals consume scarce resources and increase opportunity cost.

**Unobservable supplier cost:** corporate or DCAI/Data Center gross margin must not be assigned directly as Xeon/EPYC SKU margin. Build a separately flagged *engineering cost interval* from chiplet/tile area, dies per wafer, yield, external foundry agreements, packaging, test, scrap, logistics and cost-accounting sensitivity. Never label scenario COGS as a company-reported SKU cost.

Pricing floor (modeled) ≈ **incremental variable cost + capacity opportunity cost + required contribution**. Pricing ceiling (buyer-specific) ≈ **value of capacity/performance/TCO versus the next best qualified alternative**. Neither is a disclosed invoice price.

## Buyer decision models and channel crosswalk

| Economic buyer | Procurement path | What can be estimated from public data | Primary leverage / economic constraint |
|---|---|---|---|
| Hyperscaler / CSP / large platform | Direct CPU agreement or ODM/OEM contract; multi-year platform qualification | Disclosed product mix, some unit and supply signals; net CPU invoices **usually unavailable** | Enormous volume/forecast certainty, dual sourcing, custom Arm/CPU design, power-density limits, schedule risk |
| OEM/ODM | Buys merchant silicon, attaches a platform, sells through integrator or direct | Reference vs configured-option spread, advertised support and bundle | Inventory, discount programs, qualification, pass-through margin and services |
| Enterprise / sovereign / government | OEM reseller, multiyear RFQ, public tender, owned fleet or leased cloud | Full delivered-system awards with BOM, configured-server deltas, TCO | Per-core/VM license exposure, power, SLA, integration, migration and vendor support |
| HPC/research/AI factories | Procurement programs for validated platform/rack; sometimes accelerator host CPU | Public tender BOM and benchmark; accelerator host CPU must be counted exactly once | Application scaling, HPC performance per watt, node/rack networking and accelerator-to-host ratio |

For **enterprise bids**, require exact OEM/SKU/server configuration, selected processor count, memories/storage/NIC/GPU/cooling, included support, tax, currency, award date and units. Public procurement entry points: [Spain PLACSP](https://contrataciondelestado.es/wps/portal/DatosAbiertos), [EU TED Search API](https://docs.ted.europa.eu/api/latest/search.html), and [US federal opportunities](https://sam.gov/). Contracts lacking CPU-specific BOM stay in *system-only* evidence.

For **cloud economics**, on-demand vCPU instance tariffs must never be divided by CPUs to imply the cloud operator's Xeon/EPYC purchase price. Cloud rates include load factor, memory, network, storage, capex amortization, reserved/spot discounts, operating expense and margin. Compare cloud as an **alternative to purchasing servers**, not as another chip ASP observation.

### Reproducible pricing questions, methods and formulas

**1 — Reference matched-SKU index.** Capture the same SKU at dates t and t−1 (same geography, currency, tax and quantity basis). Compute:
```text
log_index_t = Σ_s fixed_weight_s × ln(reference_price_s,t / reference_price_s,t−1)
index_t = exp(log_index_t)
```
Record matched sample size and SKU coverage. New/retired SKUs are not simply swapped in. Add a hedonic quality-adjusted reference index `ln(price) ~ time + cores + clocks + cache + TDP + memory_channels + generation + target_segment` with transparent out-of-sample validation. Both are **reference**, not net-price indices.

**2 — ASP decomposition.** In a scope with actual matched volume weights and net prices:
```text
ASP_t = Σ_(sku,buyer) unit_share_(sku,buyer,t) × net_price_(sku,buyer,t)
ΔASP = price_within_cell + sku/generation_mix + buyer_mix + interactions
```
Use symmetric Shapley decomposition where the joint distribution is observed; otherwise mark individual price and mix effects **not identified**. Report gross mix shifts and uncertainty separately; do not infer discounts from qualitative attribution alone.

**3 — Hyperscaler–enterprise price gap.** A valid like-for-like model requires *net semiconductor* prices with same CPU SKU, period and comparable volume/terms:
```text
ln(P_net_i / P_reference_s,t) = α + β_H hyperscaler_i +
     f(ln(volume_i)) + sku_FE + quarter_FE + region_FE + terms + ε_i
conditional_net_gap = exp(β_H) − 1
```
No contract observations => **no point estimate**. Report synthetic discounts only as tunable scenarios. Moreover, the relevant counterfactual for enterprise purchasing may be the OEM's semiconductor transfer cost, not the price on the enterprise server invoice. Do not regress list price against buyer class and call that negotiated discount.

**4 — OEM pass-through.** Fix OEM/model/region/date/baseline CPU and measure raw option delta. Replay selected CPU, record forced cooling/PSU/RAM/bundle upgrades, deduct observable co-requisite deltas to estimate adjusted shadow CPU option premium. Estimate how a reference repricing changes adjusted OEM spread across time/SKUs controlling platform age and configuration; this is not a supplier contract price even if the estimated slope is close to one.

**5 — Supplier contribution interval.** For each compatible cost scenario:
```text
estimated_CPU_contribution = estimated_net_semiconductor_price −
    (dies_and_yield + packaging + test + logistics + incremental_warranty)
```
Public cost engineering has wide uncertainty. Do not equate total operating margin, depreciation allocation or fabs' sunk fixed expense with per-chip marginal contribution. Supply-shadow-cost stress tests must be explicit.

**6 — Buyer TCO and break-even.** For each *equivalent delivered workload*:
```text
3_to_5_year_TCO = acquired_servers + software_licenses + rack/network +
    (measured_avg_wall_power_kW × 8760 × years × PUE × energy_price_per_kWh)
    + support + staffing + migration − residual_value
TCO_per_work = TCO / successful_SLA_qualified_work_units
```
Use observed workload-specific throughput and utilization/availability, not max clock/core count. Account for software licensing per core/socket and constrained power/cooling floors. SPEC CPU 2026 is a [standard benchmark](https://www.spec.org/cpu2026/) but is not a substitute for workload-specific VM/SQL/Java/agent testing.

**Illustration only, not market evidence:** Fleet A requires 2 servers at $20,000 each to meet validated load. Fleet B meets it on 1 server at $28,000. Assume equal service, zero software/energy differences and no residual: B can bear an **$12,000 higher** *total* system acquisition price than A before losing the hardware CAPEX advantage. Including per-core license and measured power can move that break-even substantially; it is **not** a hyperscaler discount estimate.

## Source precedence, identifiability and validation

Evidence grades follow [project P1–P6 policy](../../EVIDENCE-STANDARDS.md), combined with **price-specific identification**; a P1 filing can prove a reported *ASP change* without proving any individual buyer's *ASP dollars*.

| Source / cost to obtain | Confident measurement possible | Not identified without more |
|---|---|---|
| Vendor dated official SKU tables (free) | Reference 1KU/RCP at publication vintage | Net sale, quantity-weighted ASP |
| Intel 10-K/10-Q (free) | Reported aggregate server ASP percent movement, qualitative mix | SKU-specific price change or total merchant CPU revenue via all DCAI |
| OEM configurator (free, volatile) | Relative option premium, if baseline/BOM fixed | Semiconductor OEM invoice and enterprise awarded discount |
| Public BOM-rich tenders (free, extraction effort) | Contracted **full-system** price/units | CPU cost allocation unless multiple matched configurations support it |
| Independent benchmarks and power tests (varied license) | Tested performance/workload, if config and rules valid | Purchase price or different workload productivity |
| Industry shipment/revenue estimates (often paid) | CPU unit-share and market-size estimates at stated denominator | Direct confidential per-customer negotiated invoice |
| Import/export/customs (patchy) | Certain shipment proxy signals with HS-code bounds | Reliable server CPU SKU ASP without part-level classification |

**Capture schema (future DB extension, no production migration in this commit):** `source_id, source_locator, published_at, capture_timestamp_utc, digest_sha256, rights, parser_version, measurement_id, vendor, sku, generation, physical_package, cores, core_type, sockets_per_server, quantity_basis, buyer_class, procurement_channel, end_buyer, OEM, server_model, baseline_sku, co_requisite_BOM, price_layer, original_value, currency, country, tax_status, FX_date/rate/source, period_start/end, fiscal_calendar, market_boundary, numerator, denominator, measurement_kind, verification, estimation_model_hash, assumptions, uncertainty_interval, missing_reason`. Preserve raw local values; only then derive FX-normalized comparable observations (using dated [ECB data](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.ff.html)). Store publication date and capture date separately (some current pages do not display publication dates).

**Anti-false-precision rules:** every estimate names target, numerator, denominator, coverage, direct/indirect observables, priors, sensitivity and date. Missing core inputs yield NULL+reason rather than a filled spreadsheet cell. Confidence depends on *identifiability* and independent source classes, not repeated reseller listings. Control selection bias from promoted SKUs, limited configurator inventory, unavailable tenders, survivorship and public buyers unlike hyperscalers.

**Validation order:** (i) field/currency/SKU unit checks; (ii) exact public locator and stored snapshot or permitted digest; (iii) supplier mix-versus-ASP aggregate reconciliation; (iv) source independence; (v) out-of-time and leave-one-OEM/buyer-out holdouts; (vi) prediction interval coverage + model calibration; (vii) resample/Monte Carlo sensitivities with correlated variables; (viii) reviewed promotion. A model reproducing an aggregate FY Intel reported ASP change does not validate its hidden customer-level prices.

## Research work plan and integration

**P0, immediate:** Recheck Intel historical ASP source passages; snapshot vendor SKU/RCP/1KU lists by launch-vintage/quarter; capture Dell R770/R7725 fixed-baseline options with all co-requisites; acquire a minimum *pilot sample* of 10–20 public BOM-rich tender awards. Build a source ledger and match each observation to a stable SKU and market boundary.

**P0, inference gate:** Secure legally usable CPU-only shipment/unit and revenue denominators, stratified by customer when available. If none, leave **D006** net ASP unobserved; do not manufacture an endpoint from Intel segment revenue or AMD CPU+GPU segment. Ask whether mix effects alone explain measured changes and whether industry coverage represents enterprise or public-sector procurement only.

**P1, estimation:** Publish separately (1) quality-adjusted reference index, (2) reported vendor ASP index, (3) configured-OEM option premium, (4) awarded enterprise system-price distribution, (5) any *identified* buyer-class net discount, (6) workload $/qualified task frontier. Backtest before visualization.

**P1, strategic hypothesis tests:** premium mix vs realized repricing; capacity scarcity's effect on price/contract allocation; Arm outside-option effect on RFQ; OEM pass-through lag; software license break-even; supplier contribution per package bottleneck.

**P2, quarterly operating cadence:** monthly current SKU snapshots, quarterly filings/awards, generation-launch source refresh, immutable quarterly model runs and source-version conflicts. No automatic research-packet-to-DB promotion until [database wiring gates](../../database/ZCODE-FULL-WIRING-ASSESSMENT.md) and [intake review](../../../research/INTAKE-AND-PROMOTION.md) are complete.

**Output ownership:** The live packet contains source-specific observations, claims, hypotheses, routes and open gaps. This chapter owns reusable analytical design; `data/demand-2030/` continues owning the macro chip shipment/revenue model; `db/` defines eventual typed storage. New claims should link to existing packet IDs, never duplicate raw full-text source dumps.

### Public-safe interview answer

“Published Xeon RCP and EPYC 1KU are useful pricing anchors, but not actual customer net prices. Intel's reported server ASP shifts reflect SKU mix, hyperscaler mix and repricing; for example, 2022's decline coincided with more hyperscale revenue, while 2026's increases were largely premium-mix driven. Public disclosures do not identify a stable hyperscaler-versus-enterprise net discount percentage. We can estimate public reference index movements, OEM CPU-option spreads and full-system procurement prices; to infer contracted semiconductor ASP rigorously requires same-SKU, period, buyer and quantity denominators. For buyers, the economically meaningful comparison is validated workload TCO, not sticker discount.”

**Boundary:** Discussion strictly of public filings, public market evidence, and independently modeled assumptions; never imply private contract or client-specific knowledge.

### FY2024 original-filing vintage discrepancy — 2026-10-08 addendum

[Pricing Observatory Run 01](RUN-01-2026-10-08.md) confirms a source-version mismatch: Intel's original FY2024 10-K reports server ASP +12%, volume −10%, while its FY2025 comparative reports +11%, volume −8%, for 2024 versus 2023. Those are different **disclosure vintages**; preserve both, label conflict `conflict:run01:intel-fy2024` and do not settle the cause without accounting/scope review. The earlier pricing packet's +11% is correctly attributed to the later comparative; neither replaces the other. This is a reproducibility gate for all future reported-ASP series.
