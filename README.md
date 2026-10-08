# CORE/SIGNAL — Server CPU Strategy Lab

**A 10-minute, visual, interactive field guide to the server CPU market.**

Intended for fast strategic orientation: x86 competition, Arm's adjacent pressure, differentiated workloads, server economics and the AI-driven infrastructure shift. The interface uses cited public facts and clearly labeled teaching models rather than invented market shares or pricing.

![Status](https://img.shields.io/badge/status-working%20starter-c3f68d) ![Data](https://img.shields.io/badge/data-public%20only-blue)

## ⚡ Start in 30 seconds

Requirements: Node.js 20+; no package installation or API keys required.

```bash
npm start
```

Open http://127.0.0.1:4173 in a browser. On Windows you may also double-click `OPEN-WINDOWS.cmd` inside the extracted folder, or run these commands in PowerShell. `npm test` validates the economic simulator. To generate an entirely self-contained HTML file for double-click opening (including on mobile), run `npm run build:single`; it creates `standalone.html`. The same static site can be hosted on GitHub Pages. The 2026 comparison also covers AMD EPYC 9006 (up to 256 cores/socket) and Intel Xeon 6+ (up to 288 E-cores/socket), based on their published product documents.

## New: AMD Advancing AI 2026 — x86 demand research corpus

A July 2026 public AMD keynote has been indexed as a **research source**, not accepted as an independent forecast. The uploaded auto-caption transcript is *not* republished publicly.

- [Eight key figures — decompositions and source gaps](docs/research/KEY-FIGURE-DECOMPOSITION.md) — $25B to $200B+/220B assumptions, agent CPU core-hour demands, rack BOM, CPU unit/ASP/margin mix and x86/ARM substitution.
- [Full research and dashboard implementation path](docs/research/AMD-ADVANCING-AI-2026-RESEARCH-PATH.md) — eight critical numbers to decompose, three CPU demand segments, workload-to-socket TAM models, pricing/margin gaps, verification priorities, and UI design.
- [97 sourced quantitative claims](data/claims/amd-advancing-ai-2026-curated.json) — normalized claims, source line ranges, status and caveats.
- [196 numeric-bearing source lines](data/sources/amd-advancing-ai-2026-numeric-anchors.json) — exhaustive decimal-digit line index over the 3,189-line uploaded transcript, explicitly untriaged.
- [38 strategic/qualitative signals](data/claims/amd-advancing-ai-2026-strategic-signals.json) — attributed strategic arguments, customer testimony and vendor roadmaps.
- [Related ROCm/x86 future](docs/ROCM-X86-ROADMAP-2026-2031.md).
- [Corpus integrity test](tests/keynote-corpus.test.mjs); included by `npm test`.

**Core caution:** AMD's $200B+ 2030 CPU TAM estimate (later ~ $220B) is vendor guidance; the `agents per watt` figures can use CPU thread counts as estimates rather than observed agent task throughput. Helios auto-caption GPU/core figures conflict with official product literature; see the research path's contradiction queue.

## Dashboard sections

| Surface | Interaction | What it teaches |
| --- | --- | --- |
| Executive overview | Fast-scan evidence cards | What is known, with caveats |
| Competitive map | Select AMD / Intel / Arm ecosystem | Differentiated strategies and verification questions |
| Demand engine | Choose a workload | Why buying criteria differ by buyer |
| Pricing & TCO | Five adjustable assumptions and reset | Energy sensitivity, not vendor benchmarks |
| AI compute shift | Select a CPU role | CPU inference vs GPU host vs data infrastructure |
| Strategic briefing | Expand five strategic questions | Preparation for a high-level expert conversation |
| Source ledger | Open primary sources | Provenance, dates, publisher and claim caution |
| Field guide | Scannable glossary | Industry terminology in plain language |

## Information integrity

**Public repository boundary:** No expert-network screening material, screening answers, project emails, hidden client identities, MNPI, confidential pricing, historical employer internals or private consultation-related materials belong here. All example numbers are either public primary-source disclosures or explicitly hypothetical calculations. Read [docs/COMPLIANCE.md](docs/COMPLIANCE.md) before contributing.

The AMD 2025 **$16.6B data-center revenue** cited in the UI includes **EPYC CPUs plus Instinct GPUs**. It cannot be interpreted as AMD server CPU revenue or share. Any vendor claim should be clearly labeled and independently verified before strategic use.

## Project organization

- `index.html`, `styles.css`, `app.js` — responsive, accessible interactive dashboard.
- `data.js` — inspectable editorial content, source references and strategy lenses.
- `economics.js` — pure deterministic power-cost model; `tests/` contains unit tests.
- `server.mjs` — built-in Node local server; no third-party production dependencies.
- `scripts/build-standalone.mjs` — packages styles and modules into a single offline HTML artifact.
- `docs/RESEARCH-ROADMAP.md` — evidence backlog and investigation tracks.
- `docs/STRATEGIC-FRAMEWORK.md` — competitive and market logic.
- `docs/EVIDENCE-STANDARDS.md` — claim-quality rules.
- `docs/COMPLIANCE.md` — public-only information boundaries.
- `.github/workflows/pages.yml` — GitHub Pages deployment.

## Public GitHub repository

Repository: https://github.com/owenservera/server-cpu-strategy-lab

The application is hosted from this repository. The static dashboard entry point (`index.html`) can be opened locally or deployed using GitHub Pages. GitHub Pages requires repository **Settings → Pages → Build and deployment → Source → GitHub Actions**. The included workflow publishes on pushes to `main`; do not assume the site is live before confirming a successful deployment.

## Development principles

1. **Visual-first**: users should understand the market structure before reading prose.
2. **Evidence-bound**: every number points to a public primary document and its date.
3. **No false precision**: do not infer share, ASP, margins, or adoption from vendor marketing.
4. **Workload before vendor**: compare like-for-like workloads, not disconnected peak specs.
5. **Static-first**: keep the interface install-free and easy to deploy, then modularize as complexity grows.
6. **Mobile-capable**: touch-friendly interactions and readable charts on phone as well as desktop.

## Next milestone

Connect a versioned, public-data ingestion layer, add carefully sourced shipment and revenue-share series from properly licensed data, workload comparison matrices with benchmark provenance, the public OEM availability index and an AI inference economics lab. See [docs/RESEARCH-ROADMAP.md](docs/RESEARCH-ROADMAP.md).

Licensed under [MIT](LICENSE). Public informational research, not financial or investment advice.