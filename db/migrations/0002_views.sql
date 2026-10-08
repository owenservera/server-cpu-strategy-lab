-- Derived read-only views, avoiding incompatible accounting units.
CREATE VIEW IF NOT EXISTS v_measurement_evidence AS
SELECT m.measurement_id, m.metric_id, md.quantity_kind, md.expected_boundary,
       m.scope_id, sc.economic_boundary, m.period_label, m.period_kind,
       m.value_decimal, m.unit, m.qualifier, m.evidence_kind,
       m.verification_status, m.measurement_basis,
       s.publisher, s.publication_date, s.access_status, s.canonical_uri,
       m.legacy_ref
FROM measurements m
JOIN metric_definitions md ON md.metric_id=m.metric_id
JOIN market_scopes sc ON sc.scope_id=m.scope_id
JOIN source_documents s ON s.source_id=m.source_id;
CREATE VIEW IF NOT EXISTS v_forecast_history AS
SELECT f.forecast_id, f.metric_id, sc.economic_boundary, f.scope_id,
       v.publisher, v.issued_at, v.issued_date_precision, v.forecast_kind,
       f.target_period, f.value_decimal, f.unit, f.qualifier, f.estimate_kind,
       f.legacy_ref, s.access_status, s.canonical_uri
FROM forecasts f JOIN forecast_vintages v ON v.vintage_id=f.vintage_id
JOIN market_scopes sc ON sc.scope_id=f.scope_id
JOIN source_documents s ON s.source_id=v.source_id;
CREATE VIEW IF NOT EXISTS v_synthetic_outputs AS
SELECT mr.scenario_name, mr.as_of, cm.title, o.target_year,
       o.metric_key, o.segment_key, o.value_decimal, o.unit,
       o.is_missing, o.missing_reason, mr.status
FROM model_outputs o
JOIN model_runs mr ON mr.run_id=o.run_id
JOIN calculation_models cm ON cm.model_id=mr.model_id;
CREATE VIEW IF NOT EXISTS v_unresolved_conflicts AS
SELECT * FROM conflicts WHERE resolution_state='open';
