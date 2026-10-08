# Non-negotiable database invariants and failure handling

| Invariant | Mechanism in v1 | Still requiring later work |
|---|---|---|
| Every sourced measurement has attribution | NOT NULL source FK and source access metadata | Programmatic verification of original documents |
| Company assertion differs from measured observation | Separate `evidence_claims`, `measurements` and verification fields | Human editorial review before promotion |
| Forecasts never silently become history | `forecast_vintages`/`forecasts` separate from `measurements` | UI labeling and as-of controls |
| Scenario numbers are synthetic | `model_runs.is_synthetic=1`, distinct `model_outputs` | Executable model provenance/uncertainty propagation |
| Fiscal quarters differ from calendar quarters | `period_kind` and `period_label` | Fiscal-period mapping after confirmed company calendar |
| Complete-system dollars ≠ CPU silicon dollars | `economic_boundary` on scopes and metrics | Query planner must block incompatible aggregates |
| OEM channel ≠ end buyer | Orthogonal taxonomy axes | Hardware-purchase event ledger and ownership dedupe |
| Workload tags can overlap | `workload` axis is non-additive; `workload_pool` models nonoverlapping revenue | Physical deployment allocation with spare-capacity deductions |
| Model share allocation sums to one | `partition_frames` + Decimal validator | Multi-year versioned allocation periods |
| More recent estimate doesn't overwrite old forecast | Keyed `forecast_vintages` and immutable ID importer | Reviewed version transitions and diff API |
| Numeric precision/qualifiers retained | Canonical decimal strings and `greater_than` qualifier | Rigorous uncertainty/bound arithmetic |
| Conflicted data isn't resolved by preference | Separate `conflicts`, open IDC 2024 discrepancy | Conflict review dashboard and independent source verification |
| User-submitted third-party transcript isn't republished | Source locator pointers, attribution only | License-by-source enforcement and ingest redaction scans |
| No unsourced material published as market fact | Read-only export preserves evidence status | Approval-gated public snapshot materialization |
| Seed is reproducible and non-destructive | File SHA batches, `INSERT OR IGNORE` + same-ID content comparison | Incremental importer for reviewed revisions |

**Transaction discipline:** Source imports are wrapped in a SQLite transaction, foreign keys are enabled, and duplicate IDs with changed factual fields abort instead of rewriting prior content. Only batch linkage may vary when another row is added to the same source file. Data correction should use a new ID or an explicit reviewer-approved migration; do not edit prior evidence records in place without lineage.

**Important v1 boundary:** `measurements` values are not automatically globally verified, because much of the prior corpus is explicitly company-reported or secondary-derived. The loader sets verification to `attributed_unverified`. Historical dataset names such as `historical-and-forecast-evidence.csv` do not confer factual certainty.

**Database engine limitations:** SQLite is single-writer and local. It does not solve remote concurrent agents, row-level access control, live streaming data ingestion, multiuser approvals, or petabyte analytics. The future design addresses these without requiring an initial heavy server deployment.
