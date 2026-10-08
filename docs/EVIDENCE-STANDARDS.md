# Evidence protocol

## Claim classes

| Class | Standard | UI treatment |
| --- | --- | --- |
| P1: audited/public financial | SEC filings, regulatory or company IR with dates | Source + reporting-period caveats |
| P2: primary technical | Product specifications, cloud service docs | Source + product/SKU/date |
| P3: vendor marketing | Performance comparisons supplied by manufacturer | Clearly label **Vendor claim** |
| P4: independent reproducible | Published benchmark methods and configs | Context, workload, hardware, software, date |
| P5: interpretation | Derived hypothesis based on cited facts | Label as analysis/hypothesis |
| P6: scenario | User-editable hypothetical assumptions | Label illustrative; show formula |

## Prohibited shortcuts

- Do not use combined AMD data-center revenue as CPU-only revenue.
- Do not use server *CPU unit share* as a substitute for server *CPU revenue share*.
- Do not mix single-socket with dual-socket platforms when interpreting density or cost.
- Do not equate product list prices with ASPs or hyperscaler transfer prices.
- Do not translate peak benchmarks into real-world application performance without workload and config validation.
- Do not forecast CPU shipment growth directly from GPU demand.
- Do not show fabricated time series or unsupported precise market sizes.

## Source register (starter)

- **AMD25** — AMD investor relations, 2025 earnings reported Feb 3, 2026: https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results
- **AMD24** — AMD EPYC 9005, Oct 10, 2024: https://www.amd.com/en/newsroom/press-releases/2024-10-10-amd-launches-5th-gen-amd-epyc-cpus-maintaining-le.html
- **INTEL25** — Xeon 6 portfolio launch, Feb 24, 2025: https://newsroom.intel.com/data-center/intel-unveils-leadership-ai-networking-solutions-xeon-6-processors
- **INTELAI** — GPU host Xeon, May 22, 2025: https://www.intel.com/content/www/us/en/newsroom/news/artificial-intelligence/new-intel-xeon-6-cpus-maximize-gpu-ai-performance.html
- **INTEL26** — Xeon 6 architecture reference reviewed Feb 24, 2026: https://www.intel.com/content/www/us/en/support/articles/000098612/processors/intel-xeon-processors.html
- **ARM** — Arm Neoverse inference development path: https://learn.arm.com/learning-paths/servers-and-cloud-computing/ai-portal-cloud-text-to-text/1-setup/

- **AMD6** — AMD 6th Gen EPYC Venice architecture, Jul 23 2026: https://www.amd.com/en/blogs/2026/agentic-ai-amd-epyc-9005-cpus-wins-today-epyc-9006.html
- **AMD6RAMP** — AMD Venice 2nm production ramp, May 21 2026: https://newsroom.amd.com/news/amd-announces-production-ramp-of-next-generation-a/
- **INTEL6PLUS** — Intel Xeon 6+ portfolio Q2 2026: https://www.intel.com/content/www/us/en/products/details/processors/xeon/6-plus-series.html
- **AZUREAMD** — AMD/Microsoft Azure collaboration, Jul 20 2026: https://newsroom.amd.com/news/microsoft-azure-ai-infrastructure/

## Freshness model

Every published fact needs: publisher, canonical URL, publication/review date, metric definition, related claim, confidence, and last checked date. Automated fetches must stage suggested changes for editorial verification, not silently rewrite evidence. Refresh financial data quarterly, products at major launches, market-share datasets when authorized and licensed.