-- Financial evidence extension v1.1; additive to CORE/SIGNAL v1.
-- Source docs and atomic measurements remain canonical. Financial rows add context,
-- commitment topology and explicit, gated model-input lineage.
CREATE TABLE IF NOT EXISTS financial_issuers (
  issuer_id TEXT PRIMARY KEY,
  entity_id TEXT REFERENCES entities(entity_id),
  legal_name TEXT NOT NULL,
  primary_symbol TEXT,
  jurisdiction TEXT NOT NULL,
  primary_regulator TEXT NOT NULL,
  regulator_entity_id TEXT,
  investor_relations_url TEXT,
  role_tags_json TEXT NOT NULL DEFAULT '[]',
  acquisition_priority TEXT NOT NULL CHECK(acquisition_priority IN ('P0','P1','P2','P3')),
  coverage_start_year INTEGER NOT NULL DEFAULT 2019 CHECK(coverage_start_year BETWEEN 1900 AND 2200),
  note TEXT NOT NULL DEFAULT ''
) STRICT;
CREATE INDEX IF NOT EXISTS idx_financial_issuer_priority ON financial_issuers(acquisition_priority,issuer_id);

CREATE TABLE IF NOT EXISTS financial_filings (
  filing_id TEXT PRIMARY KEY,
  issuer_id TEXT NOT NULL REFERENCES financial_issuers(issuer_id),
  source_id TEXT NOT NULL UNIQUE REFERENCES source_documents(source_id),
  regulator TEXT NOT NULL,
  filing_type TEXT NOT NULL,
  accession_or_document_id TEXT,
  period_start TEXT, period_end TEXT,
  fiscal_year INTEGER CHECK(fiscal_year BETWEEN 1900 AND 2200),
  fiscal_quarter INTEGER CHECK(fiscal_quarter BETWEEN 1 AND 4),
  filed_at TEXT NOT NULL,
  accepted_at TEXT,
  amendment_of TEXT REFERENCES financial_filings(filing_id),
  extraction_status TEXT NOT NULL DEFAULT 'indexed' CHECK(extraction_status IN('indexed','retrieved','extracted','needs_review','reviewed','rejected')),
  note TEXT NOT NULL DEFAULT '',
  CHECK(amendment_of IS NULL OR amendment_of <> filing_id),
  CHECK(period_start IS NULL OR period_end IS NULL OR period_start<=period_end),
  UNIQUE(regulator,accession_or_document_id)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_financial_filings_issuer_period ON financial_filings(issuer_id,period_end,filing_type);

-- Facts are measurements, not re-created numbers. This one-to-one annotation
-- captures exact source context (GAAP/IFRS, YTD vs standalone, taxonomy, units).
CREATE TABLE IF NOT EXISTS financial_fact_contexts (
  measurement_id TEXT PRIMARY KEY REFERENCES measurements(measurement_id),
  filing_id TEXT NOT NULL REFERENCES financial_filings(filing_id),
  source_locator_id TEXT NOT NULL REFERENCES source_locators(locator_id),
  xbrl_taxonomy TEXT,
  xbrl_concept TEXT,
  normalized_concept TEXT NOT NULL,
  statement_type TEXT NOT NULL CHECK(statement_type IN('income','balance_sheet','cash_flow','segment','footnote','non_gaap','operating_kpi','other')),
  reporting_basis TEXT NOT NULL CHECK(reporting_basis IN('instant','duration_ytd','duration_quarter','duration_year','cumulative','other')),
  accounting_standard TEXT NOT NULL DEFAULT 'not_disclosed',
  reported_currency TEXT,
  consolidation_scope TEXT NOT NULL DEFAULT 'not_disclosed',
  segment_label TEXT,
  original_context_ref TEXT,
  is_restated INTEGER NOT NULL DEFAULT 0 CHECK(is_restated IN(0,1)),
  CHECK(reported_currency IS NULL OR length(reported_currency)=3)
) STRICT;
CREATE TRIGGER IF NOT EXISTS trg_financial_fact_source_insert
BEFORE INSERT ON financial_fact_contexts
WHEN (SELECT source_id FROM measurements WHERE measurement_id=NEW.measurement_id)
    <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
 OR (SELECT source_id FROM source_locators WHERE locator_id=NEW.source_locator_id)
    <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
BEGIN SELECT RAISE(ABORT,'financial fact measurement/locator must match filing source'); END;
CREATE TRIGGER IF NOT EXISTS trg_financial_fact_source_update
BEFORE UPDATE OF measurement_id,filing_id,source_locator_id ON financial_fact_contexts
WHEN (SELECT source_id FROM measurements WHERE measurement_id=NEW.measurement_id)
    <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
 OR (SELECT source_id FROM source_locators WHERE locator_id=NEW.source_locator_id)
    <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
BEGIN SELECT RAISE(ABORT,'financial fact measurement/locator must match filing source'); END;

-- Commitments are NOT revenue, capex, orders or silicon TAM. Capture exposure
-- without fabricating values, and preserve uncertain counterparties.
CREATE TABLE IF NOT EXISTS financial_commitments (
  commitment_id TEXT PRIMARY KEY,
  filing_id TEXT NOT NULL REFERENCES financial_filings(filing_id),
  locator_id TEXT NOT NULL REFERENCES source_locators(locator_id),
  obligor_issuer_id TEXT REFERENCES financial_issuers(issuer_id),
  counterparty_issuer_id TEXT REFERENCES financial_issuers(issuer_id),
  counterparty_name_public TEXT,
  commitment_kind TEXT NOT NULL CHECK(commitment_kind IN
   ('purchase_obligation','cloud_capacity','foundry_capacity','supply_capacity','equipment','lease','financing','guarantee','rpo','backlog','other')),
  amount_decimal TEXT,
  currency TEXT,
  qualifier TEXT NOT NULL DEFAULT 'equal' CHECK(qualifier IN('equal','approximately','greater_than','less_than','range_low','range_high','unquantified')),
  start_date TEXT, end_date TEXT,
  cancellation_terms TEXT NOT NULL DEFAULT 'undisclosed',
  amount_basis TEXT NOT NULL,
  economic_layer TEXT NOT NULL CHECK(economic_layer IN
   ('corporate_financial','server_system','cpu_silicon','cloud_service','fleet_capacity','unresolved')),
  status TEXT NOT NULL DEFAULT 'disclosed' CHECK(status IN('disclosed','amended','fulfilled','cancelled','superseded')),
  verification_status TEXT NOT NULL DEFAULT 'attributed_unverified',
  note TEXT NOT NULL DEFAULT '',
  CHECK((amount_decimal IS NULL AND currency IS NULL AND qualifier='unquantified') OR
        (amount_decimal IS NOT NULL AND currency IS NOT NULL AND qualifier<>'unquantified')),
  CHECK(start_date IS NULL OR end_date IS NULL OR start_date<=end_date)
) STRICT;
CREATE INDEX IF NOT EXISTS idx_financial_commitment_filing ON financial_commitments(filing_id,commitment_kind);
CREATE TRIGGER IF NOT EXISTS trg_financial_commitment_source_insert
BEFORE INSERT ON financial_commitments
WHEN (SELECT source_id FROM source_locators WHERE locator_id=NEW.locator_id)
  <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
BEGIN SELECT RAISE(ABORT,'commitment locator must match filing source'); END;
CREATE TRIGGER IF NOT EXISTS trg_financial_commitment_source_update
BEFORE UPDATE OF locator_id,filing_id ON financial_commitments
WHEN (SELECT source_id FROM source_locators WHERE locator_id=NEW.locator_id)
  <> (SELECT source_id FROM financial_filings WHERE filing_id=NEW.filing_id)
BEGIN SELECT RAISE(ABORT,'commitment locator must match filing source'); END;

-- Same contract, upstream/downstream financing or economic overlap is a
-- relationship, not something that can be summed automatically.
CREATE TABLE IF NOT EXISTS financial_flow_links (
  left_commitment_id TEXT NOT NULL REFERENCES financial_commitments(commitment_id),
  right_commitment_id TEXT NOT NULL REFERENCES financial_commitments(commitment_id),
  relationship TEXT NOT NULL CHECK(relationship IN('same_contract','upstream_downstream','finances','overlaps','supersedes','independent_verified')),
  evidence_source_id TEXT NOT NULL REFERENCES source_documents(source_id),
  note TEXT NOT NULL DEFAULT '',
  PRIMARY KEY(left_commitment_id,right_commitment_id,relationship),
  CHECK(left_commitment_id<>right_commitment_id)
) STRICT;

-- Model input proposals are explicit bridges, not implicit acceptance of a
-- disclosed commitment as CPU orders. No model run changes by insertion.
CREATE TABLE IF NOT EXISTS financial_model_mappings (
  mapping_id TEXT PRIMARY KEY,
  measurement_id TEXT REFERENCES measurements(measurement_id),
  commitment_id TEXT REFERENCES financial_commitments(commitment_id),
  target_model_id TEXT REFERENCES calculation_models(model_id),
  target_input_key TEXT NOT NULL,
  source_boundary TEXT NOT NULL,
  target_boundary TEXT NOT NULL,
  transformation_method TEXT NOT NULL,
  transformation_version TEXT NOT NULL,
  denominator_notes TEXT NOT NULL,
  uncertainty_notes TEXT NOT NULL DEFAULT '',
  review_status TEXT NOT NULL DEFAULT 'proposed' CHECK(review_status IN('proposed','needs_review','approved','rejected','superseded')),
  reviewer TEXT,
  reviewed_at TEXT,
  CHECK((measurement_id IS NOT NULL AND commitment_id IS NULL) OR
        (measurement_id IS NULL AND commitment_id IS NOT NULL)),
  CHECK(review_status<>'approved' OR (reviewer IS NOT NULL AND reviewed_at IS NOT NULL))
) STRICT;

CREATE VIEW IF NOT EXISTS v_financial_fact_context AS
SELECT f.filing_id,f.issuer_id,f.filing_type,f.filed_at,f.period_end,
       m.measurement_id,m.metric_id,m.value_decimal,m.unit,m.evidence_kind,
       m.verification_status,m.period_label,m.measurement_basis,
       fc.normalized_concept,fc.statement_type,fc.reporting_basis,
       fc.reported_currency,fc.segment_label,fc.is_restated,
       sd.canonical_uri,l.locator_kind,l.locator_value
FROM financial_fact_contexts fc
JOIN financial_filings f ON f.filing_id=fc.filing_id
JOIN measurements m ON m.measurement_id=fc.measurement_id
JOIN source_documents sd ON sd.source_id=f.source_id
JOIN source_locators l ON l.locator_id=fc.source_locator_id;

CREATE VIEW IF NOT EXISTS v_financial_commitment_evidence AS
SELECT c.commitment_id,f.issuer_id,f.filing_type,f.filed_at,
       c.commitment_kind,c.amount_decimal,c.currency,c.qualifier,
       c.start_date,c.end_date,c.amount_basis,c.economic_layer,
       c.status,c.verification_status,c.cancellation_terms,
       c.counterparty_issuer_id,c.counterparty_name_public,
       sd.canonical_uri,l.locator_value
FROM financial_commitments c
JOIN financial_filings f ON f.filing_id=c.filing_id
JOIN source_documents sd ON sd.source_id=f.source_id
JOIN source_locators l ON l.locator_id=c.locator_id;
