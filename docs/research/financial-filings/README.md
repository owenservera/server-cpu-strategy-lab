# Corporate Financial Filings Intelligence — acquisition and model contract

**Program:** CORE/SIGNAL — Server CPU Strategy Lab  
**Design vintage:** 2026-10-08  
**Scope:** public evidence 2019–latest filed period; financial and competitive scenarios through 2030  
**Status:** implemented additive SQLite schema + prioritized issuer watchlist + offline staged filing intake + SEC discovery helper; **NOT** a completed 2019–2026 historical filing extraction or promoted numerical dataset.

**First read:** [RESEARCH-ENTRY](../../../RESEARCH-ENTRY.md) → [database](../../../docs/database/README.md) → [existing demand model semantics](../../../docs/database/SEGMENTATION-AND-MODELS.md). Do not build a parallel TAM, modify legacy demand totals, or conflate direct CPU purchases with systems, infrastructure or cloud service spending.

## Research questions / destinations

1. **CPU economics**: rebuild quarterly company-**reported** volume/ASP bridges and product mix where observable; keep EPYC-specific revenue **unknown** when AMD only reports a broader Data Center segment. Route to CPU pricing, competitive capture and `cpu_silicon` analysis.
2. **End buyer financing and acquisition**: hyperscaler/enterprise/neocloud capex, cash vs leases, RPO, contracted capacity, backlog and equipment funding; identify economic buyer, owner/operator and intermediary without duplicate CPU purchases.
3. **Supply**: foundry capacity, packaging, DDR/HBM, physical MW and power constraints. These constrain timing and cost; none directly establishes CPU shipments.
4. **Forward contractual evidence**: purchase obligations, leases, financing, guarantees and customer/supplier relationships. Distinguish contractual face amount from delivered units, recognized revenue and non-binding announcements.
5. **Strategic competition**: merchant x86 vs captive Arm vs licensed Arm royalty vs bundled AI-host CPUs; measure independent demand and financing dependencies.

The canonical **three demand buckets remain** `foundational`, `ai_host`, `agent_execution`; any proposed vendor allocation is a scenario overlay, not a historical TAM rewrite.

## Company and filing acquisition plan

Machine-readable index: [35-issuer priority watchlist](../../../data/financial-filings/issuer-watchlist.json). It contains **targets only**, not retrieved filings or data.

| Wave | Primary companies | Inputs | Initial output |
| --- | --- | --- | --- |
| P0 CPU and platform | AMD, Intel, NVIDIA, Arm, TSMC | 10-K/20-F, 10-Q/6-K, earnings releases, 8-K exhibits, financial analyst days | Revenue/ASP and segment changes, CPU/GPU split, manufacturing conditions, strategy |
| P0 buyer | Amazon, Microsoft, Alphabet, Meta, Oracle | Annual/quarterly statements, capex, lease and commitment notes, RPO | Physical procurement vs service obligations and financing |
| P0 channel | Dell, HPE | Annual/quarterly statements, server/AI segment and backlog | Server-channel bridge to silicon sales |
| P1 | Broadcom, Qualcomm, SoftBank, Micron, Samsung, SK hynix, CoreWeave, Supermicro, Wiwynn, Quanta, Nebius, ASML, Equinix, Digital Realty | US SEC plus company investor relations, DART/TWSE/TSE/local authority | Merchant-custom substitution, supplier bottlenecks, ODM mix, new buyer funding |
| P2 | Marvell, Foxconn, Lenovo, Amkor, Vertiv, Eaton, Alibaba, Tencent, Baidu | Exchange filings, annual/interim reports, channel/physical infrastructure results | Secondary demand and supply constraints |

Include amendments, accounting restatements, material contractual exhibits, prospectuses/credit agreements for neoclouds, and archived management presentation **vintages**. Obtain a regulator-native issuer identifier (CIK, other registration number), not ticker-only identity. Some companies have complex reporting/ownership paths, so no private-company audited figures are presumed to exist (e.g. Ampere).

Sources:
- US SEC data API: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- US SEC submissions: https://data.sec.gov/submissions/
- TSMC IR financial reports: https://investor.tsmc.com/english/financial-reports
- Korea DART: https://englishdart.fss.or.kr/
- Hong Kong HKEXnews: https://www1.hkexnews.hk/
- Relevant corporate investor relations and national securities authorities.

## Implemented database layer

Migration [`0003_financial_filings.sql`](../../../db/migrations/0003_financial_filings.sql) extends existing v1 source and model tables; no modifications to 0001 or 0002.

| Table / view | Role |
| --- | --- |
| `financial_issuers` | Watchlist entities and issuer/regulator identity; optional link to existing `entities` |
| `financial_filings` | One source-backed filing version; issuer, authority, accession, reporting period, amendment, review status |
| `financial_fact_contexts` | Exactly one canonical `measurements` row per numeric observation plus exact filing locator, XBRL tag, fiscal context, basis and reported currency |
| `financial_commitments` | Source-located, **non-additive** contract/lease/financing/RPO/backlog disclosure; counterparty optional, cancellation and timing tracked |
| `financial_flow_links` | Same-contract/overlap/upstream/financing/supersession graph; no automatic aggregation |
| `financial_model_mappings` | Proposed or reviewed mapping of one evidence row into an explicitly specified model input; includes scope, transformation and uncertainty |
| `v_financial_fact_context`, `v_financial_commitment_evidence` | Read-only evidence-labeled query/export surfaces; not market totals |

Fiscal YTD and standalone quarter are distinct (`reporting_basis`). A later filed comparative/recast amount is a distinct filing/source vintage, not an overwrite of the original. Amendments are connected via `amendment_of`; currency normalization requires a separate derived record and rate/vintage. Reported number precision is stored as decimal **text**. Rights/access, company assertions and independently checked statements have separate statuses. Foreign-key and source-locator triggers prevent fact/filing provenance mismatch.

In `financial_commitments`, `amount_decimal` is an **absolute nominal amount in the provided currency units** (e.g. US dollars, not "millions of dollars"). Preserve source display scale in `amount_basis`; no automatic currency conversion, discounting, annualization or aggregation. A commitment with no public number uses `null` with qualifier `unquantified`; do not invent numbers.

### Mapping economic layers correctly

| Filing concept | What it can support | What it does **not** establish |
| --- | --- | --- |
| Vendor Data Center segment revenue | Public vendor financial/strategic signals | EPYC-only or CPU-silicon revenue without separately evidenced product attribution |
| Intel disclosed server ASP/volume bridge | Reported company-specific price/quantity movements | Global CPU average selling price, any single SKU's net contract price |
| Hyperscaler capex | Funded/constructed infrastructure and cash investment | CPU silicon revenue or new server CPU sockets on its own |
| RPO/backlog | Forward demand contract/revenue recognition signal | Hardware shipments, CPU value, cash capex or irrevocable orders |
| Supplier capacity commitments | Potential future supply envelope | Realized shipment, standalone CPU allocation or confirmed demand |
| OEM/ODM server revenue | Channel and system spend signals | Independent demand additive to the end buyer's spend |
| Arm licensing/royalties | ISA/IP supplier economic capture | Merchant Arm CPU shipments or server CPU sales in the same denominator |
| NVIDIA AI system sales | Platform and bundled host attach hypothesis | Standalone CPU ASP or vendor-interchangeable CPU sockets |

**Overlaps example:** a cloud customer promises spend to a cloud provider; that provider signs data center or equipment obligations; a CPU vendor sells chips into the equipment chain. Those are linked financial flows. A sum of all disclosed contract amounts is not end-market CPU TAM. Keep funding source and obligor separate from economic end user and CPU owner.

## Operational instructions (local Windows PowerShell)

Python 3.11+ and SQLite 3.37+ are sufficient for schema, manifests and manual intake. The static dashboard remains independent.

```powershell
python db/scripts/research_db.py seed
python db/scripts/research_db.py stats
python db/scripts/research_db.py verify
python -m unittest discover -s db/tests -v
```

For **SEC issuers**, identify your retrieval client with SEC's required user-agent and discover official filing *metadata*. This step needs internet access, handles historical submission pages, and saves only public links and metadata to a gitignored runtime JSON file:

```powershell
$env:SEC_USER_AGENT = 'CORE SIGNAL research contact@example.com' # replace with actual contact
python db/scripts/sec_filing_discovery.py --issuer-id fin:amd --from-year 2019
python db/scripts/research_db.py ingest-financial --input db/runtime/sec-fin-amd.json
python db/scripts/research_db.py query --sql "SELECT issuer_id,filing_type,filed_at,extraction_status FROM financial_filings ORDER BY filed_at DESC LIMIT 20"
```

The script does **not** harvest full text, scrape private data, bypass paywalls, infer values or promote filing facts. Company filings indexed this way start `indexed` and carry no measurements. The SEC helper requires real issuer CIK resolution and an explicit contact user agent; respect SEC access policies and backoffs. International filings require provider-specific adapters and human validation, not SEC URL fabrication.

### Next: stage extracted numeric facts, commitments and mapping proposals

Use an explicit local JSON file with `schema_version: "1.0"`, `public_only: true`, `filings: [...] ` and optional `model_mappings: [...] `, `flow_links: [...] `. Each filing needs stable ID, issuer ID, source ID, public HTTPS URL, form, regulator, filed date and title. Numeric fact fields include `id`, `metric_id`, `scope_id`, `economic_boundary`, `denominator`, `period_label`, `period_kind`, `value`, `unit`, `source_locator`, `normalized_concept`, `statement_type` and `reporting_basis`. Commitment fields include `id`, `source_locator`, `commitment_kind`, `amount` or null, `currency` if quantified, `amount_basis`, `economic_layer`, optional publicly identified counterparty and cancellation terms. Never store a nominal magnitude before restoring the full unit scale.

```powershell
python db/scripts/research_db.py ingest-financial --input db/runtime/curated-financial-intake.json
python db/scripts/research_db.py verify
python db/scripts/research_db.py export
```

This command is an **offline transactional staging importer**: it stores new public-document metadata, observation rows and non-additive commitments without making them verified or affecting synthetic model runs. Reimport of unchanged input is idempotent; conflicting IDs/values require review/new vintages. A reviewed filing cannot silently acquire newly appended facts. Both `financial_model_mappings` and future promotion remain independent review gates. Files in `db/runtime/` are gitignored; verified/reviewed source pointers and research packets are later published under existing Git conventions, not an opaque SQLite file.

## Extraction and review protocol

1. **Resolve** company identity and current filing accession. Record primary page URL, filing receipt date, fiscal/report period, amendment and digest/version. Do not treat newer management projections as earlier financial actuals.
2. **Extract** financial line items/footnotes with exact section/XBRL tag, numeric scale and currency, YTD-versus-standalone, the stated consolidation/segment and the accounting standard. Retain correction vintages.
3. **Join/normalize** to canonical `metric_definitions`, `market_scopes`, issuer, workload and buyer/channel axes only with preserved denominators. Do not transform annual quarter data via subtraction until comparable contexts are confirmed.
4. **Identify obligation links** by reported counterparty, shared contract and upstream/downstream financial relationships. Preserve uncertainty in indirect or undisclosed counterparties; do not manufacture missing relationships.
5. **Stage and route** `source` + `financial_filing` + `financial_commitment` (as applicable), and claim + measurement + forecast + entity + relationship + buyer_demand + strategic_signal + conflict + question in `research/packets/`. Filing/commitment arrays are optional for old packets, with explicit non-additive obligations. This SQLite importer does *not* replace packet editorial approval.
6. **Review, then map** to pricing, historical time series, capacity constraints or competitive allocation. Approval requires actual evidence review, a fully specified denominator and explicit transformation with sensitivity bounds.
7. **Validate** `npm run check:research`, `npm test`, `python -m unittest discover -s db/tests -v`, `seed`, `verify`, `export`. Compare CI evidence and do not claim success solely because a workflow file exists.

For fiscal-quarter normalization, keep revenue, capex, debt/leases and cash-flow basis separate. Apply period comparisons only when issuer, accounting basis, consolidation, measurement scope, unit, and restatement vintage match. Never infer a fiscal year's last quarter from annual minus 9-month figures unless all these conditions and the exact cumulative basis are satisfied.

## Read-model outputs and decision boundaries

The local export adds `financial_facts` and `financial_commitments`, with explicit verification statuses. No financial facts are promoted to historical server-CPU series merely by appearance in this export. The static UI is not currently wired to the DB.

Long-run company × period × segment × supplier/customer × ISA coverage should drive:
- CPU ASP/volume/mix charts with product-revenue identification caveats.
- Capital-commitment versus delivered-capacity timelines with cash/noncash and cancellability annotations.
- A counterparty network to detect duplicate flows and vendor-supported purchasing.
- Competitive share stress tests using the **existing** TAM as fixed input.
- Evidence-gap lists that explicitly distinguish missing public disclosure from zero.

## Acceptance checklist

- [x] Additive schema, immutable source-vintage path, scope-aware fact context and overlap structure.
- [x] 35-company machine-readable filing acquisition watchlist.
- [x] Offline public SEC metadata discovery script and manual staged importer.
- [x] New regression tests for staging and source-locator integrity (execution must be checked via CI).
- [ ] Automated scheduled collection with rate limits, retry/backoff, and issuer-level identity validation.
- [ ] Extract and review the actual 2019–2026 historical filing corpus (no asserted completeness).
- [ ] First reviewed CPU ASP/volume quarterly series and supply/demand commitments graph.
- [ ] Reviewed packet-to-DB promotion adapter, read-only UI integration and model sensitivity/backtests.

**Security/compliance:** public sources only, no expert network/client confidential information, no copyright-infringing transcript or full document mirror in Git, no fee-wall bypass. Separate acquisition intent, published evidence, and analyst inference throughout.
