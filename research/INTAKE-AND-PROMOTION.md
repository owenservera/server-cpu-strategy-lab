# Research intake, routing and promotion protocol

**Canonical entry:** [../RESEARCH-ENTRY.md](../RESEARCH-ENTRY.md). This is the operating manual for processing new sources or mixed research conversations while preserving the evidence and meaning of existing corpus records.

## Stage 0 — Decide whether publishing is authorized

A user may request brainstorming, advice or comparison without asking for repository modification. In that case, answer without writing. For an authorized public-repo update, continue. Reject confidential consultation materials, client-identifying screenshots, unpublished employer research and anything with uncertain publication rights; never "sanitize" secrets by guessing they are harmless. Consult [public compliance](../docs/COMPLIANCE.md).

## Stage 1 — Find the right existing home

Read [catalog.json](catalog.json), identify all affected domains, inspect their data definitions and current source/claim registries; use GitHub search if topic or literal numbers are unclear. **Do not create a new file for each conversational subject by default.** Existing analytical modules own their topics; the intake packet owns the new research session's cross-domain provenance.

## Stage 2 — Register the source once

Capture public URL, canonical publisher, author/speaker, publication date, retrieved/as-of date, version, format, legal access and the exact source locator (URL to table/section, report page, video timestamp, transcript line or filing exhibit). Record stable source ID. A URL found in a source registry is an **index entry**, not independent verification that every linked number is true.

Third-party keynotes: analyze the full public video or user-supplied transcript where authorized; publish **summaries, normalized claims and minimal supporting quotations within license limits**, not a copy of the transcript. Annotate automatic caption errors and unknown speaker attribution.

## Stage 3 — High-recall discovery / low-noise promotion

Sweep the input for all distinct information classes:

1. Numeric metrics and denominator (units, percent, dollars, time, entity cohort).
2. Technical specs, measured performance and support/availability state.
3. Forecasts, revised guidance and explicit future capacity commitments.
4. Companies, alliances, customer/supplier relationships and direct purchase channels.
5. Strategic intentions and qualitative market mechanisms.
6. Contradictions, changed definitions, incomparable populations, revisions.
7. Methods/assumptions, hypotheses, falsification experiments and follow-up questions.
8. Product UI implications and missing datasets.

Stage all useful **nonduplicative** items, but do not automatically promote every extracted numeral. Model names, timestamps, rhetorical examples and unattributed figures often do not belong in accepted market tables.

## Stage 4 — Classify and route MULTIPLE outputs

Use [routes.json](routes.json) for all matching routes, then make a packet in `research/packets/YYYY-MM-DD--slug.json` as defined by [schema](schema/packet.schema.json).

Example: a 100-minute AMD keynote can produce `source`, `claim`, `forecast`, `technical_spec`, `entity`, `relationship`, `strategic_signal`, `question` and `conflict`. Put the source only once; claims reference it; forecasts reference both. One conversation can legitimately produce multiple packets **only if it contains independent source events requiring separate versioning**.

**Never use the data's paragraph heading as the type.** A number in the 'AI' part of an investor keynote may be a management estimate, a physical GPU spec, an experimental benchmark or a new procurement commitment—all different records.

## Stage 5 — Reconcile evidence rather than overwrite

- **Same numerical claim, different independent sources:** preserve separate source assertions linked by `corroborates`. Confidence improves if denominators and methods align; raw number of citations is not independent corroboration.
- **New version of a forecast:** register new `issuer + publication date + target period + market scope + qualifier`; keep the earlier vintage. Forecast history is evidence about uncertainty, not observed revenue.
- **Different denominators:** keep separate, label `not_comparable`; e.g. x86 server CPU unit share vs revenue share, whole server dollars vs CPU silicon, OEM channel vs end-buyer demand, 2026 fiscal quarter vs 2026 calendar quarter.
- **True disputed claim:** retain both side IDs in a `conflict` record with `open` status, required verification and explicit resolution note.
- **New fact invalidates prior figure:** mark supersession/lineage and UI deprecation without deleting historical source context.
- **Source assertions vs observations:** use `reported_company`, `secondary_estimate`, `vendor_benchmark`, `modeled` and independent reproducible evidence explicitly.
- **Missing input:** null + reason, not a made-up placeholder, until a user-editable synthetic scenario is requested.

## Stage 6 — Maximize marginal intelligence

For each candidate find answers to:
- What new decision does this enable or materially change?
- Does it corroborate, update, contradict or merely repeat something already recorded?
- What *numeric denominator, buyer segment, ISA, calendar vintage or workload* is missing?
- Can we derive a meaningful **non-double-counted** metric from confirmed source inputs? If so, store the formula and output separately.
- What **strong opposing interpretation** could overturn the headline conclusion?
- What is the shortest next research action with the greatest uncertainty reduction?

Prioritize `P0` data gaps by decision impact and public availability. A 30-second hint about GPU socket attachment with a verified BOM may be more valuable than another 60-page market commentary. Stop adding content when it yields no new reusable claim, uncertainty reduction or next-step decision.

## Stage 7 — Review before promoting

Use [evidence class policy](../docs/EVIDENCE-STANDARDS.md), licensing checks and the domain accounting definitions. Review should establish:
- source and origin are public, accurate and stable;
- company filing vs vendor assertion vs independently measured status;
- exact time, market universe, geography, numerator, denominator, unit, reported currency;
- source methodology and any corrected version;
- whether the information is already recorded (legacy reference);
- any schema/data-calculation constraints and downstream effect.

**Promoting** means updating the appropriate preexisting domain dataset or a tightly justified new topic dataset. Staging `research/packets/` does **not** mean numbers are dashboard-ready. Every promoted record needs a `promotions[]` decision with the path and review status; never label verified just because an agent says so.

## Stage 8 — Validate, hand off and close the loop

Run `npm run check:research` and `npm test` and preserve their results. For genuinely new measurements, extend tests to cover units, denominators, duplicates, source IDs, non-double-counted totals and forecast-vintage retention. Update affected domain module documentation and [catalog](catalog.json) only if relevant boundaries or evidence gaps changed.

Your response should say:
- New source(s), claims, measurements, future signals and relationships added.
- Existing IDs reused instead of duplicated.
- Key insights and altered conclusions, plus credible counterarguments.
- Unresolved conflicts and high-value unanswered questions (with `P0/P1/P2`).
- Promoted datasets vs staged records, and test outcome and commit link.

## Common high-risk examples

| Scenario | Correct treatment | Wrong treatment |
| --- | --- | --- |
| AMD says >$220B server CPU TAM by 2030 | Dated attributed `forecast`, same market definition and issuer vintage | Treat as actual 2030 silicon revenue |
| Two press reports quote Mercury share | Preserve primary estimate lineage and secondary access flags | Count as two independent market research firms |
| Microsoft shows 1.6M local coding input tokens | Vendor demo + workload question, check cumulative vs single pass | Treat as average user demand |
| Docker says SBX isolates an agent | Technical claim + reproduce safety and CPU/RAM overhead | Assume confirmed zero-overhead, invulnerable microVM |
| 2024 IDC amount differs between vintages | Conflict with both dated scopes; do not splice | Recalculate secretly and overwrite past data |
| Analyst TAM jumps from $130B to $300B | Separate vintage records + causal forecast revision research | Silent replace or add $170B to addressable revenue |
| OEM revenue and AWS infrastructure build | Two perspectives on one flow | Sum both as separate CPU purchases |
| ROCm can compile x86 host code | CPU host support, separate device execution hypothesis | Announce AMD ROCm first-class x86 CPU backend |

## Improvements to consider later, not prerequisites

Canonical global entity IDs, automated URL normalization and content hashing, a SQLite event ledger and programmatic dashboard materialized views could improve scale once dozens of packets accumulate. **Do not deploy a database or heavy crawler before this low-overhead protocol proves useful.** Metrics can be manually cross-linked safely in Git today.
