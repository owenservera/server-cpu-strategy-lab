# Target query & review API design (not implemented)

The v1 is a local SQLite mirror and read-only snapshot generator. This document specifies the **future** API contract so a UI and a multi-agent research worker can share vocabulary.

## Read surfaces

- `GET /v1/catalog/metrics`: metric ID, definition, unit, market boundary, denominator, aggregation rule, valid periods.
- `GET /v1/catalog/segments?axis=buyer|channel|isa|workload`: hierarchical nodes with valid dates and additive/nonadditive flags.
- `POST /v1/query/measurements`: `{metric_ids, periods, dimensions, publisher_filter, evidence_status_filter, aggregation_request}`. Server rejects period/boundary/denominator conflicts, non-additive summation, and mixed source vintages without explicit user choice; returns complete provenance, status, missing reasons and resolved scopes.
- `GET /v1/forecasts?vintage=all&target=2030&metric=...`: exact source vintages and qualifier; no implicit 'latest = true'.
- `GET /v1/models/{model_id}/runs`: synthetic scenario version/run manifest, parameters, calculated outputs, traceable dependencies, unresolved inputs.
- `GET /v1/evidence/{object_id}/lineage`: sources, supporting/contradicting claims, model dependencies and revisions.
- `GET /v1/research/gaps?priority=P0`: missing numerator/denominator/data series and proposed reproducible experiments.
- `GET /v1/conflicts?status=open`: contradictory source records; distinguished `not_comparable` vs `disputed`.

## Write/review surfaces (future)

- `POST /v1/ingestion/packets`: authenticated researcher stages a packet and gets proposed matches, duplicate candidates and validation diagnostics.
- `POST /v1/reviews/{object_id}`: independent reviewer records accepted/rejected/promoted with rationale, source access and visible side effects. No auto-promote.
- `POST /v1/models/run`: authenticated analyst starts an immutable calculation run with input hashes, user assumptions and requested uncertainty method.

## Example read request

```json
{
  "metric_ids": ["server_cpu_silicon_TAM"],
  "periods": ["2030"],
  "source_vintages": "all",
  "dimensions": {"isa": "isa:x86", "buyer": "buyer:hyperscaler_cloud"},
  "allow_synthetic": false,
  "aggregation_request": "none"
}
```

No v1 measurements can satisfy this query just by naming a 2030 total; the response must indicate that the requested x86/buyer breakdown is **not observed**, and optionally offer a separate synthetic scenario result.

## Source to UI provenance

Display canonical source link, publisher, publication/review date, historical period, exact unit, accounting boundary, population, qualifier, evidence status, original legacy ID and any open conflict. A missing reference cannot be silently replaced by the current largest TAM estimate. The frontend can cache a signed/versioned read-only JSON snapshot for static deployment; it must not access the DB file or write APIs directly.
