# Server CPU strategy: first-principles framework

## Central proposition

Server CPU competition should be analyzed as a **workload → platform → procurement → economics** decision, not a simple ranking of processors.

### 1. Market structure

**Direct x86 CPU competitors:** Intel Xeon and AMD EPYC. **Adjacent substitutability:** Arm Neoverse and custom Arm hyperscaler platforms. Distinguish merchant CPU sales, cloud instances, OEM/ODM platforms and internally designed silicon.

### 2. Demand and segmentation

| Segment | Demand driver | Decision power | Core question |
| --- | --- | --- | --- |
| Hyperscaler | Fleet utilization and compute service margin | Infra design + procurement | Useful work per dollar, watt and rack? |
| OEM/ODM | Platform portfolio and customer qualifications | OEM product/category teams | Which qualified configurations can sell at margin? |
| Enterprise | Legacy workloads, virtualization and refresh | IT, purchasing, application owners | Migration-adjusted TCO and risk? |
| HPC | Science/engineering throughput and grants | Architects / domain teams | Real application run time and memory/IO scalability? |
| AI infrastructure | Model serving, GPU fleet, retrieval/ETL | Systems architects and AI platform teams | Which layer of AI compute is constrained? |

### 3. Supply and price boundaries

Supply = silicon output + packaging + substrates + qualified platform integration + channel and geographic restrictions. Pricing has layers: manufacturer published SKU list, OEM/ODM integration, negotiated hyperscaler purchase agreements and end-user system acquisition. ASP/discounting cannot be reliably inferred from single list-price pages.

### 4. Margin and share interpretation

- Unit share, revenue share and installed-base share are different measurements.
- A high-core-count SKU doesn't imply equal core utilization in customer workloads.
- OEM cloud instance availability is a proxy for ecosystem breadth, not shipment volume.
- Combined AMD data-center segment includes GPUs and CPUs; no pure EPYC share can be deduced.

### 5. Competitive pressure hypotheses to test

- **H1: Hyperscaler portfolio shift** — large cloud customers can adopt architectures workload-by-workload; validate instance offers, launches and public vendor cases.
- **H2: Enterprise qualification inertia** — procurement and software certification slow switches; validate with open customer evidence and licensing schedules.
- **H3: AI increases CPU heterogeneity** — AI-serving host, CPU-only inference and retrieval pipelines generate distinct requirements; validate with open benchmarks and reference systems.
- **H4: Energy changes fleet procurement** — power and facility limits can alter optimal CPU purchase independent of list price; validate with fleet configurations and energy contracts when publicly documented.

All hypotheses above are analytic questions, **not measured conclusions**.

## Suggested 15-minute learning sequence

1. Scan key facts and scope caveats.
2. Compare three ecosystem strategies.
3. Choose the buyer/workload likely to matter to your question.
4. Test power/economic sensitivity, then explicitly list missing TCO variables.
5. Map which AI layer is driving CPU consumption.
6. Read the five questions and open corresponding public sources.