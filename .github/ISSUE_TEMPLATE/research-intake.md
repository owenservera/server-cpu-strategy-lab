---
name: Research intake / new source
about: Suggest a public keynote, report, dataset, finding or concept for the research corpus
title: "Research intake: "
labels: []
assignees: []
---

Read [RESEARCH-ENTRY.md](../../RESEARCH-ENTRY.md) before opening a source-intake task. This issue is a request for research, **not accepted verified evidence**.

## Public source / primary link

Original public URL(s), publisher, publication date, version and license/access status. Do not upload third-party full transcripts, confidential consultation/client material or private data.

## Research question

What decision or contradiction could this change?

## Relevant entry routes (check all that apply)

- [ ] Source and attributed claim
- [ ] Measured numeric data or time series
- [ ] Product / software / standards specifications
- [ ] Forecast / 2030 TAM revision
- [ ] Company, buyer, OEM/ODM and relationship
- [ ] Benchmarks and methodology
- [ ] Hypothesis, future scenario or new concept
- [ ] Contradiction / correction
- [ ] UX/dashboard change or research method
- [ ] Unknown; route using `research/routes.json`

## Existing research to reuse

Paths / IDs from `research/catalog.json`, `data/claims/`, `data/demand-2030/`, or other source ledgers.

## Definition and verification requirements

What are the key numbers, their denominators and vintage, what proof is available, and what claims remain uncertain?

## Outcome requested

Expected data record(s), analytical insight, contradiction resolution, user-facing dashboard impact, and follow-up questions.

## Acceptance criteria

- [ ] References existing records rather than blindly duplicating them
- [ ] Any new evidence is attributable and sufficiently scoped
- [ ] Reviewer explicitly approves or rejects promotion
- [ ] `npm run check:research` and `npm test` have been run
