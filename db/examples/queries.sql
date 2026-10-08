-- SQLite read-only examples. Uses text decimals for presentation, not SQL REAL for financial math.
-- 1. Source-backed historical measurements (company/secondary only, not verified truth)
SELECT period_label, metric_id, scope_id, value_decimal, unit, evidence_kind, access_status, canonical_uri
FROM v_measurement_evidence
ORDER BY metric_id, period_label, scope_id;

-- 2. One forecast target, ALL vintages: do not replace older AMD guidance.
SELECT publisher, issued_at, target_period, scope_id, value_decimal, unit, qualifier, access_status
FROM v_forecast_history
WHERE target_period='2030' AND metric_id='server_cpu_silicon_TAM'
ORDER BY issued_at, publisher;

-- 3. Separate scenario outputs, which must never be presented as historical data.
SELECT scenario_name, target_year, metric_key, segment_key, value_decimal, unit, is_missing
FROM v_synthetic_outputs
WHERE target_year=2030 ORDER BY scenario_name, metric_key;

-- 4. Source maturity and unverified transcript claims
SELECT s.publisher, s.access_status, c.verification, COUNT(*) AS claim_count
FROM evidence_claims c JOIN source_documents s ON s.source_id=c.source_id
GROUP BY s.publisher, s.access_status, c.verification;

-- 5. Partition frames are MECE by explicit assertion, not inferred from hierarchy names.
SELECT f.frame_id, f.axis_id, f.aggregation_basis, f.exclusivity, a.node_id, a.weight_decimal
FROM partition_frames f JOIN partition_allocations a ON a.frame_id=f.frame_id
ORDER BY f.frame_id,a.node_id;

-- 6. Unresolved research questions and source conflicts
SELECT question_id, priority, question, verification_method FROM research_questions WHERE status='open' ORDER BY priority,question_id;
SELECT conflict_id, issue, resolution_state, resolution_method FROM v_unresolved_conflicts;
