# Research operating system (minimal, additive)

**Purpose:** Make the repository self-describing for any new researcher or AI session. **Entry point:** [../RESEARCH-ENTRY.md](../RESEARCH-ENTRY.md).

## Why this layer exists

Previously, source-specific extracts lived in `data/claims/`, the demand model lived in `data/demand-2030/`, and topical reports lived under `docs/research/`. Those are valuable but **not mutually discoverable by data type**. This module adds routing, cross-reference IDs and repeatable intake **without rewriting legacy files or making another competing repository of truth**.

## Architecture

```text
AGENTS.md → RESEARCH-ENTRY.md → catalog.json + routes.json
                                       │
Public source / conversation           │
  → discover prior records ────────────┘
  → research/packets/YYYY-MM-DD--slug.json
     ├─ sources + claim assertions + measurement candidates
     ├─ forecast revisions + hypotheses + strategic signals
     ├─ entities + relationships + contradictions
     ├─ downstream routes, open questions, evidence gaps
     └─ review decisions / promotion targets
  → validation + editorial checks
  → existing canonical topic datasets and analysis
  → UI and briefing outputs that cite promoted evidence
```

### Four layers, not four copies of the data

1. **Source context:** immutable identification, URLs, dates, speaker, version, copyright/access and locator. A source is not proof that every assertion it contains is true.
2. **Atomic observations and assertions:** typed facts, vendor claims, financial disclosures, projections, task measurements, entity links and contradictions, all linked to source IDs; no narrative-only records for discoverable quantitative claims.
3. **Curated analytical domains:** the existing [demand 2030 module](../docs/research/demand-2030/README.md), the [ROCm/x86 dossier](../docs/ROCM-X86-ROADMAP-2026-2031.md), technical guides, financial analysis and any future modules. Curated material references packet IDs rather than duplicating source text.
4. **Applications and insight:** downstream charts/briefings, tradeoff and sensitivity models, and next-question backlog. UI never bypasses attribution/quality status.

### First-class provenance / versioning

- **Source identity** = canonical public URL + publisher + version/publication date and, if appropriate, digest. A corrected PDF or updated investor deck is a new version with predecessor link.
- **Claim identity** = source assertion; retain precise source-location. Two sources saying the same thing are *two claims*, linked by `corroborates`, not one overwritten row.
- **Measurement identity** = metric + population/denominator + unit + period + region + observed/estimated + source. Changing scope is a different record.
- **Forecast identity** = publisher + issued date + model version + target year + market scope; never replace a former forecast with later guidance.
- **Conflict identity** = two comparable but discrepant records (or source-vintage mismatch) + status + resolution. If genuinely different denominators, mark `not_comparable` rather than resolving by choosing a favorite.
- **Insight identity** = hypothesis + evidence links + alternative explanations + falsification tests. A compelling executive quotation is *not* a verified observation.

### Work across several entry points

Examples: One AMD keynote can touch AI tokens, EPYC product specs, Intel/Arm competition, ROCm, OEM deployment timing, server CPU TAM projections, customer alliances and x86 standards. Route each piece to its appropriate record class while keeping a **single packet and source lineage**. One Docker paper may produce a measured sandbox overhead, a proposed technology concept and a security challenge; route all three rather than filing it simply as 'Docker news'.

### Legacy compatibility — important

Do **not** bulk-convert `data/claims/*` or `data/demand-2030/*` just to satisfy the new packet schema. Their existing records and validation tests stay valid. The catalog provides `legacy_paths` and the packet can point to `legacy_ref` so old evidence is reusable; gradually normalize only when actively revisiting an observation. Never delete a historic dataset before its successor passes denominator, lineage and conservation checks.

**Intake packet** is a staging and cross-link unit, **not a new verified market table**. Its unreviewed numbers must not automatically power dashboards. Promotion targets remain topic-specific and use existing names and financial semantics.

## Default lifecycle

`discovered → extracted → linked → needs_review → verified_or_attributed → promoted → consumed`

A route may end at `not_verified`, `superseded_as_new_vintage`, `rejected` or `conflicted`; keep the evidence of this decision. External web search and AI-generated statements must never silently skip review.

To validate, use `npm run check:research`, or `npm test` for regression coverage. No external packages, DB servers or cloud services required.

## Adding a domain

Update [catalog.json](catalog.json) and [routes.json](routes.json); include its canonical existing data paths, decision questions, required denominator and related topics. Add separate content only when the domain has distinct, reusable records. Resist duplicating files merely because a new session starts.

## Current risks explicitly acknowledged

- Existing claim corpora use differing naming/shape conventions; the packet is a **bridge**, not a claim of already-normalized historical data.
- The [2024 IDC system-spending source-vintage discrepancy](../docs/research/demand-2030/README.md) remains unresolved.
- Some numeric rows are attributed secondary sources and **not independently reverified**.
- Agent CPU core-seconds/workflow, local-vs-cloud share and real CPU silicon ASP by buyer are research gaps.
- The public corpus has line pointers for supplied third-party transcripts, **not republished transcripts or guaranteed public access to the original uploaded files**.
