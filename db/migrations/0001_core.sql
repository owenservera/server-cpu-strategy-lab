-- CORE/SIGNAL research warehouse v1. SQLite 3.40+, foreign_keys=ON required.
-- Immutable-ish public evidence, normalized scopes, typed facts, vintage forecasts,
-- calculation lineage, non-overlapping market accounting and human promotion gates.
CREATE TABLE IF NOT EXISTS schema_migrations (
  migration_id TEXT PRIMARY KEY, checksum_sha256 TEXT NOT NULL,
  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;
CREATE TABLE IF NOT EXISTS ingestion_batches (
  batch_id TEXT PRIMARY KEY, input_path TEXT NOT NULL, content_sha256 TEXT NOT NULL,
  source_kind TEXT NOT NULL CHECK(source_kind IN('legacy_import','research_packet','manual_review','model_export')),
  state TEXT NOT NULL DEFAULT 'staged' CHECK(state IN('staged','reviewed','promoted','rejected')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, note TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE TABLE IF NOT EXISTS objects (
  object_id TEXT PRIMARY KEY, object_type TEXT NOT NULL CHECK(object_type IN
    ('source','claim','measurement','forecast','entity','relationship','model','model_run','hypothesis','question','conflict','event','benchmark')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;
CREATE TABLE IF NOT EXISTS source_documents (
  source_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  title TEXT NOT NULL, publisher TEXT NOT NULL,
  canonical_uri TEXT, publication_date TEXT, source_version TEXT NOT NULL DEFAULT '',
  document_kind TEXT NOT NULL DEFAULT 'other',
  access_status TEXT NOT NULL DEFAULT 'public' CHECK(access_status IN
    ('public','public_secondary','paywalled_unverified','licensed_unavailable','local_pointer_unavailable','unverified')),
  rights_status TEXT NOT NULL DEFAULT 'link_and_extract' CHECK(rights_status IN
    ('link_and_extract','quote_with_limits','unknown_do_not_copy','public_domain')),
  digest_sha256 TEXT, retrieved_at TEXT,
  legacy_ref TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '',
  batch_id TEXT REFERENCES ingestion_batches(batch_id)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_sources_uri ON source_documents(canonical_uri, publication_date);
CREATE TABLE IF NOT EXISTS source_locators (
  locator_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source_documents(source_id),
  locator_kind TEXT NOT NULL CHECK(locator_kind IN('url_fragment','timestamp','line_range','page','filing_section','legacy_pointer','unspecified')),
  locator_value TEXT NOT NULL, excerpt_summary TEXT NOT NULL DEFAULT '',
  UNIQUE(source_id,locator_kind,locator_value)
) STRICT;
CREATE TABLE IF NOT EXISTS evidence_claims (
  claim_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  source_id TEXT NOT NULL REFERENCES source_documents(source_id),
  locator_id TEXT REFERENCES source_locators(locator_id),
  statement TEXT NOT NULL,
  claim_kind TEXT NOT NULL,
  verification TEXT NOT NULL DEFAULT 'attributed_unverified' CHECK(verification IN
   ('attributed_unverified','checked_original','independently_verified','conflicted','rejected')),
  claim_qualifier TEXT NOT NULL DEFAULT '',
  legacy_ref TEXT UNIQUE, batch_id TEXT REFERENCES ingestion_batches(batch_id),
  added_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;
CREATE INDEX IF NOT EXISTS idx_claims_source ON evidence_claims(source_id);
CREATE TABLE IF NOT EXISTS entities (
  entity_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  name TEXT NOT NULL, kind TEXT NOT NULL,
  external_uri TEXT, note TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE TABLE IF NOT EXISTS entity_aliases (
  entity_id TEXT NOT NULL REFERENCES entities(entity_id), alias TEXT NOT NULL,
  PRIMARY KEY(entity_id,alias)
) STRICT;
CREATE TABLE IF NOT EXISTS entity_relationships (
  relation_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  subject_id TEXT NOT NULL REFERENCES entities(entity_id),
  predicate TEXT NOT NULL,
  object_id TEXT NOT NULL REFERENCES entities(entity_id),
  source_id TEXT REFERENCES source_documents(source_id),
  assertion_status TEXT NOT NULL DEFAULT 'announced',
  valid_from TEXT, valid_to TEXT, note TEXT NOT NULL DEFAULT '',
  CHECK(subject_id<>object_id)
) STRICT;
CREATE TABLE IF NOT EXISTS taxonomy_axes (
  axis_id TEXT PRIMARY KEY, label TEXT NOT NULL,
  meaning TEXT NOT NULL, additive_partition INTEGER NOT NULL DEFAULT 0 CHECK(additive_partition IN(0,1))
) STRICT;
CREATE TABLE IF NOT EXISTS taxonomy_nodes (
  node_id TEXT PRIMARY KEY, axis_id TEXT NOT NULL REFERENCES taxonomy_axes(axis_id),
  parent_id TEXT REFERENCES taxonomy_nodes(node_id),
  label TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active' CHECK(status IN('active','deprecated','proposed')),
  is_residual INTEGER NOT NULL DEFAULT 0 CHECK(is_residual IN(0,1)),
  valid_from TEXT, valid_to TEXT, notes TEXT NOT NULL DEFAULT '',
  UNIQUE(axis_id,label,parent_id), CHECK(parent_id IS NULL OR parent_id<>node_id)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_taxonomy_parent ON taxonomy_nodes(axis_id,parent_id);
CREATE TRIGGER IF NOT EXISTS trg_taxonomy_axis_insert BEFORE INSERT ON taxonomy_nodes
WHEN NEW.parent_id IS NOT NULL AND (SELECT axis_id FROM taxonomy_nodes WHERE node_id=NEW.parent_id)<>NEW.axis_id
BEGIN SELECT RAISE(ABORT,'taxonomy parent must share axis'); END;
CREATE TRIGGER IF NOT EXISTS trg_taxonomy_axis_update BEFORE UPDATE OF parent_id,axis_id ON taxonomy_nodes
WHEN NEW.parent_id IS NOT NULL AND (SELECT axis_id FROM taxonomy_nodes WHERE node_id=NEW.parent_id)<>NEW.axis_id
BEGIN SELECT RAISE(ABORT,'taxonomy parent must share axis'); END;
CREATE TABLE IF NOT EXISTS entity_segments (
  entity_id TEXT NOT NULL REFERENCES entities(entity_id), node_id TEXT NOT NULL REFERENCES taxonomy_nodes(node_id),
  role TEXT NOT NULL DEFAULT 'classified', source_id TEXT REFERENCES source_documents(source_id),
  valid_from TEXT, valid_to TEXT,
  PRIMARY KEY(entity_id,node_id,role)
) STRICT;
CREATE TABLE IF NOT EXISTS market_scopes (
  scope_id TEXT PRIMARY KEY,
  label TEXT NOT NULL, economic_boundary TEXT NOT NULL CHECK(economic_boundary IN
    ('cpu_silicon','server_system','cloud_service','corporate_financial','fleet_capacity','workload','unresolved')),
  population TEXT NOT NULL, denominator_description TEXT NOT NULL,
  accounting_notes TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE TABLE IF NOT EXISTS scope_dimensions (
  scope_id TEXT NOT NULL REFERENCES market_scopes(scope_id),
  axis_id TEXT NOT NULL REFERENCES taxonomy_axes(axis_id),
  node_id TEXT NOT NULL REFERENCES taxonomy_nodes(node_id),
  allocation_role TEXT NOT NULL DEFAULT 'filter' CHECK(allocation_role IN('filter','total','partial','annotation')),
  PRIMARY KEY(scope_id,axis_id)
) STRICT;
CREATE TRIGGER IF NOT EXISTS trg_scope_axis BEFORE INSERT ON scope_dimensions
WHEN (SELECT axis_id FROM taxonomy_nodes WHERE node_id=NEW.node_id)<>NEW.axis_id
BEGIN SELECT RAISE(ABORT,'scope axis mismatch'); END;
CREATE TABLE IF NOT EXISTS metric_definitions (
  metric_id TEXT PRIMARY KEY, display_name TEXT NOT NULL,
  quantity_kind TEXT NOT NULL CHECK(quantity_kind IN
    ('currency','unit_count','ratio','rate','capacity','performance','time','power','energy','other')),
  canonical_unit TEXT NOT NULL,
  expected_boundary TEXT NOT NULL DEFAULT 'unresolved' CHECK(expected_boundary IN
    ('cpu_silicon','server_system','cloud_service','corporate_financial','fleet_capacity','workload','unresolved')),
  aggregation_rule TEXT NOT NULL DEFAULT 'non_additive' CHECK(aggregation_rule IN
    ('sum','stock_snapshot','weighted_mean','ratio','non_additive')),
  denominator_description TEXT NOT NULL DEFAULT '',
  interpretation TEXT NOT NULL DEFAULT '',status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN('draft','reviewed'))
) STRICT;
CREATE TABLE IF NOT EXISTS measurements (
  measurement_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  metric_id TEXT NOT NULL REFERENCES metric_definitions(metric_id),
  scope_id TEXT NOT NULL REFERENCES market_scopes(scope_id),
  source_id TEXT NOT NULL REFERENCES source_documents(source_id),
  claim_id TEXT REFERENCES evidence_claims(claim_id),
  period_label TEXT NOT NULL,
  period_kind TEXT NOT NULL CHECK(period_kind IN('calendar_year','calendar_quarter','fiscal_year','fiscal_quarter','other')),
  start_date TEXT, end_date TEXT,
  value_decimal TEXT NOT NULL, unit TEXT NOT NULL,
  qualifier TEXT NOT NULL DEFAULT 'equal' CHECK(qualifier IN('equal','approximately','greater_than','less_than','range_low','range_high')),
  evidence_kind TEXT NOT NULL CHECK(evidence_kind IN('company_reported','tracker_reported','secondary_estimate','independent_measurement','vendor_benchmark','anecdote','derived_from_observed')),
  verification_status TEXT NOT NULL DEFAULT 'attributed_unverified',
  measurement_basis TEXT NOT NULL, note TEXT NOT NULL DEFAULT '',
  legacy_ref TEXT UNIQUE,
  batch_id TEXT REFERENCES ingestion_batches(batch_id)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_measurement_slice ON measurements(metric_id,scope_id,period_label);
CREATE INDEX IF NOT EXISTS idx_measurement_source ON measurements(source_id);
CREATE TABLE IF NOT EXISTS forecast_vintages (
  vintage_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES source_documents(source_id),
  publisher TEXT NOT NULL, issued_at TEXT NOT NULL, issued_date_precision TEXT NOT NULL DEFAULT 'day' CHECK(issued_date_precision IN('day','month','year','unknown')),
  forecast_kind TEXT NOT NULL CHECK(forecast_kind IN('management','analyst','market_tracker','other')),
  access_note TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE TABLE IF NOT EXISTS forecasts (
  forecast_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  vintage_id TEXT NOT NULL REFERENCES forecast_vintages(vintage_id),
  metric_id TEXT NOT NULL REFERENCES metric_definitions(metric_id),
  scope_id TEXT NOT NULL REFERENCES market_scopes(scope_id),
  target_period TEXT NOT NULL,
  value_decimal TEXT NOT NULL, unit TEXT NOT NULL,
  qualifier TEXT NOT NULL DEFAULT 'equal' CHECK(qualifier IN('equal','approximately','greater_than','less_than','range_low','range_high')),
  estimate_kind TEXT NOT NULL DEFAULT 'point' CHECK(estimate_kind IN('point','low','high')),
  legacy_ref TEXT UNIQUE,
  note TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE INDEX IF NOT EXISTS idx_forecast_vintage ON forecasts(vintage_id,target_period,metric_id,scope_id);
CREATE TABLE IF NOT EXISTS calculation_models (
  model_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  title TEXT NOT NULL, metric_boundary TEXT NOT NULL,
  version TEXT NOT NULL, description TEXT NOT NULL,
  definition_path TEXT NOT NULL, code_sha256 TEXT
) STRICT;
CREATE TABLE IF NOT EXISTS model_runs (
  run_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  model_id TEXT NOT NULL REFERENCES calculation_models(model_id),
  scenario_name TEXT NOT NULL, as_of TEXT NOT NULL,
  source_sha256 TEXT NOT NULL, is_synthetic INTEGER NOT NULL DEFAULT 1 CHECK(is_synthetic=1),
  status TEXT NOT NULL DEFAULT 'reproduced' CHECK(status IN('reproduced','requires_review','invalidated')),
  UNIQUE(model_id,scenario_name,as_of,source_sha256)
) STRICT;
CREATE TABLE IF NOT EXISTS model_inputs (
  run_id TEXT NOT NULL REFERENCES model_runs(run_id),
  input_key TEXT NOT NULL, value_json TEXT NOT NULL,
  meaning TEXT NOT NULL DEFAULT '',
  PRIMARY KEY(run_id,input_key)
) STRICT;
CREATE TABLE IF NOT EXISTS model_outputs (
  run_id TEXT NOT NULL REFERENCES model_runs(run_id),
  target_year INTEGER NOT NULL CHECK(target_year BETWEEN 1900 AND 2200),
  metric_key TEXT NOT NULL, segment_key TEXT NOT NULL DEFAULT 'total',
  value_decimal TEXT, unit TEXT NOT NULL, is_missing INTEGER NOT NULL DEFAULT 0 CHECK(is_missing IN(0,1)),
  missing_reason TEXT,
  PRIMARY KEY(run_id,target_year,metric_key,segment_key),
  CHECK((value_decimal IS NULL AND is_missing=1 AND missing_reason IS NOT NULL) OR (value_decimal IS NOT NULL AND is_missing=0))
) STRICT;
CREATE TABLE IF NOT EXISTS model_dependencies (
  run_id TEXT NOT NULL REFERENCES model_runs(run_id),
  object_id TEXT NOT NULL REFERENCES objects(object_id),
  role TEXT NOT NULL, note TEXT NOT NULL DEFAULT '',
  PRIMARY KEY(run_id,object_id,role)
) STRICT;
CREATE TABLE IF NOT EXISTS partition_frames (
  frame_id TEXT PRIMARY KEY, scenario_or_source_ref TEXT NOT NULL,
  axis_id TEXT NOT NULL REFERENCES taxonomy_axes(axis_id),
  period_label TEXT NOT NULL,
  aggregation_basis TEXT NOT NULL,
  exclusivity TEXT NOT NULL CHECK(exclusivity IN('mutually_exclusive','multi_label')),
  status TEXT NOT NULL DEFAULT 'staged' CHECK(status IN('staged','checked','rejected'))
) STRICT;
CREATE TABLE IF NOT EXISTS partition_allocations (
  frame_id TEXT NOT NULL REFERENCES partition_frames(frame_id),
  node_id TEXT NOT NULL REFERENCES taxonomy_nodes(node_id),
  weight_decimal TEXT NOT NULL,
  PRIMARY KEY(frame_id,node_id)
) STRICT;
CREATE TRIGGER IF NOT EXISTS trg_allocation_axis BEFORE INSERT ON partition_allocations
WHEN (SELECT axis_id FROM taxonomy_nodes WHERE node_id=NEW.node_id)<>(SELECT axis_id FROM partition_frames WHERE frame_id=NEW.frame_id)
BEGIN SELECT RAISE(ABORT,'allocation node has wrong axis'); END;
CREATE TABLE IF NOT EXISTS hypotheses (
  hypothesis_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  thesis TEXT NOT NULL, alternative TEXT NOT NULL,
  falsification_test TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open', legacy_ref TEXT
) STRICT;
CREATE TABLE IF NOT EXISTS research_questions (
  question_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  question TEXT NOT NULL, priority TEXT NOT NULL CHECK(priority IN('P0','P1','P2')),
  verification_method TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open', legacy_ref TEXT
) STRICT;
CREATE TABLE IF NOT EXISTS conflicts (
  conflict_id TEXT PRIMARY KEY REFERENCES objects(object_id),
  left_object_id TEXT NOT NULL REFERENCES objects(object_id),
  right_object_id TEXT NOT NULL REFERENCES objects(object_id),
  issue TEXT NOT NULL,
  resolution_state TEXT NOT NULL DEFAULT 'open' CHECK(resolution_state IN('open','resolved','not_comparable','superseded_vintage')),
  resolution_method TEXT NOT NULL,
  CHECK(left_object_id<>right_object_id)
) STRICT;
CREATE TABLE IF NOT EXISTS knowledge_edges (
  left_object_id TEXT NOT NULL REFERENCES objects(object_id),
  relation TEXT NOT NULL CHECK(relation IN
     ('supports','contradicts','corroborates','derived_from','revises','mentions','motivates','tested_by','cites','impacts','replaces')),
  right_object_id TEXT NOT NULL REFERENCES objects(object_id),
  note TEXT NOT NULL DEFAULT '',
  PRIMARY KEY(left_object_id,relation,right_object_id),
  CHECK(left_object_id<>right_object_id)
) STRICT;
CREATE TABLE IF NOT EXISTS review_events (
  review_id INTEGER PRIMARY KEY,
  object_id TEXT NOT NULL REFERENCES objects(object_id),
  action TEXT NOT NULL CHECK(action IN('staged','reviewed','approved','rejected','promoted','deprecated','conflict_opened','conflict_resolved')),
  reviewer TEXT NOT NULL, outcome_note TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(object_id,action,reviewer,outcome_note)
) STRICT;
CREATE TABLE IF NOT EXISTS legacy_links (
  legacy_ref TEXT PRIMARY KEY,
  object_id TEXT NOT NULL REFERENCES objects(object_id),
  import_batch TEXT NOT NULL REFERENCES ingestion_batches(batch_id),
  UNIQUE(object_id,legacy_ref)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_legacy_object ON legacy_links(object_id);
