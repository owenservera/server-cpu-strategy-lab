# RESEARCH ENTRY — one prompt, multiple evidence routes

> You are entering **CORE/SIGNAL — Server CPU Strategy Lab**, a public, source-traceable research and strategy dashboard. The job is to **increase verifiable decision-useful intelligence**, not merely accumulate pages or duplicate notes.

## Research backend target

All research routes are intended to converge on a typed, provenance-preserving backend database. Read [database v1 specification](docs/database/README.md) and [the evidence/model architecture](docs/database/ARCHITECTURE-V1.md). A claim is not a measurement; a forecast is not a historical fact; a scenario is not a source. The current Git corpus and packet review protocol remain authoritative until the DB cutover is explicitly tested and approved.

## Start in 60 seconds

1. Read **[AGENTS.md](AGENTS.md)** and **[research/README.md](research/README.md)**.
2. Inspect **[research/catalog.json](research/catalog.json)** to find current domain ownership, questions, datasets and unresolved gaps.
3. Use **[research/routes.json](research/routes.json)** to identify **every applicable output route** for the material; a single user conversation may match ten routes.
4. Retrieve sources, identify prior equivalent claims/metric definitions and deduplicate by source, scope, period, denominator, qualifier and vintage.
5. Produce **one intake packet**: `research/packets/YYYY-MM-DD--short-slug.json`. Conform to **[research/schema/packet.schema.json](research/schema/packet.schema.json)** and read **[research/INTAKE-AND-PROMOTION.md](research/INTAKE-AND-PROMOTION.md)** before promotion.
6. Validate `npm run check:research` and `npm test`; only promote data to a domain dataset when quality/status rules allow.
7. Report the new knowledge, corroborations, contradictions, high-value missing data and changed conclusions, with the precise files and commit.

### The first question is NOT “where should I write my report?”
It's: **what reusable facts, assumptions, disagreements, relationships and questions does this input create, which existing records does it support or challenge, and what decisions could it change?**

### Choose all fitting routes

| Input / discovered content | Routes (composable) | Typical destination |
| --- | --- | --- |
| Full keynote / video transcript / report / presentation | `source`, `claim`, `strategic_signal`, `question`, `conflict` | One packet + domain indexes; no raw copyrighted transcript published |
| SEC filing, vendor earnings, official public statistics | `source`, `measurement`, `market_series`, `company_event` | Packet; approved facts to relevant domain data files |
| CPU, GPU, OS, standard, API release or product roadmap | `source`, `technical_spec`, `company_event`, `relationship`, `milestone` | Packet; specs and standards/roadmap module |
| New buyer, channel, hyperscaler or competitive strategy | `entity`, `relationship`, `buyer_demand`, `strategic_signal`, `question` | Packet; buyer/channel and market study |
| Benchmark or repeatable agent workload | `benchmark`, `measurement`, `method`, `claim` | Packet + benchmark results when verified |
| 2030 TAM projection, analyst revision | `source`, `forecast`, `conflict`, `question` | Packet; time-stamped forecast-vintages if accepted |
| New x86/Arm software concept, future scenario | `hypothesis`, `scenario`, `question`, `relationship` | Packet; optional model work, never marked observed |
| Corrections, conflicting numerical reports | `conflict`, `source`, `claim` | Packet; keep both vintages with review resolution |
| UX idea, dashboard visualization, research automation | `product_requirement`, `question` | Packet and implementation issue/spec; not a market-data fact |
| Mixed research conversation | **All matching routes** | One coherent packet, many referenced domain views |

## Canonical separation

- **Inputs:** URLs, transcript pointers, documents, events and license status.
- **Statements:** what a specific speaker, filing or organization asserts, with time and exact locator.
- **Measurements:** normalized numerical data WITH denominator, period, unit, coverage and observed/estimated status.
- **Knowledge links:** entities, relationships, supportive or contradictory evidence and revision lineage.
- **Reasoning:** analyst hypotheses, tested methods, falsification conditions and models.
- **Outputs:** published domain tables, charts, briefings and implementation work.

**DO NOT:** assume vendor guidance is an observation; replace a historical forecast with the latest forecast; equate system dollars with CPU silicon; sum OEM and hyperscaler as independent buying segments; use transcript captions as verified primary technical facts; fabricate missing rows; publish full third-party texts without rights; mix any confidential consultation/client material into public GitHub.

## Paths you should know

- [Research architecture and lifecycle](research/README.md) · [machine routing](research/routes.json) · [topic catalog](research/catalog.json)
- [Research packet schema](research/schema/packet.schema.json) · [packet example](research/templates/packet.example.json) · [promotion protocol](research/INTAKE-AND-PROMOTION.md)
- [Existing AMD keynote numeric corpus](data/claims/amd-advancing-ai-2026-curated.json) · [Microsoft/Docker signals](data/claims/microsoft-docker-agentic-2026.json)
- [Demand-2030 dataset](data/demand-2030/) · [demand research index](docs/research/demand-2030/README.md)
- [ROCm/x86 dossier](docs/ROCM-X86-ROADMAP-2026-2031.md) · [project research roadmap](docs/RESEARCH-ROADMAP.md)
- [Evidence classes](docs/EVIDENCE-STANDARDS.md) · [public compliance boundaries](docs/COMPLIANCE.md)

## For a new ChatGPT research session

Read `AGENTS.md` and `RESEARCH-ENTRY.md` from https://github.com/owenservera/server-cpu-strategy-lab, load the catalog, inspect relevant existing research, and follow the intake protocol. **Discover all routes that apply to my request; extract reusable evidence, route multiple outputs, and report contradictions and high-value next questions.** Do not create a new disconnected research document by default.

If the user has asked only for an analysis or a proposal, **do not assume permission to publish or commit changes**. The packet protocol applies when a repo update is requested or authorized.
