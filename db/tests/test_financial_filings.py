"""Financial-filing extension regressions; synthetic fixtures, no asserted company facts."""
import copy
import json
import pathlib
import sqlite3
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import research_db as db


class FinancialFilingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        migrations = self.root/'db/migrations'
        migrations.mkdir(parents=True)
        for src in (ROOT/'migrations').glob('*.sql'):
            (migrations/src.name).write_bytes(src.read_bytes())
        issuer = {
            'id':'fin:sample','name':'Synthetic Filing Test Corporation',
            'symbol':'TST','regulator':'SEC','jurisdiction':'US','priority':'P0',
            'roles':['buyer'],'coverage_start_year':2019,
            'investor_relations_url':'https://example.org/investors'
        }
        manifest = self.root/'data/financial-filings/issuer-watchlist.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({'schema_version':'1.0','issuers':[issuer]}))
        self.dbpath = self.root/'db/runtime/filing-test.sqlite'
        self.input = self.root/'test_input.json'
        self.packet = {
          'schema_version':'1.0','public_only':True,
          'filings':[{
            'id':'finfil:test:2025','source_id':'test-filing-2025','issuer_id':'fin:sample',
            'title':'Synthetic 2025 10-K','url':'https://example.org/filing/2025',
            'regulator':'SEC','filing_type':'10-K','accession_or_document_id':'TEST-001',
            'filed_at':'2026-02-01','period_start':'2025-01-01','period_end':'2025-12-31',
            'fiscal_year':2025,
            'facts':[{
              'id':'test-capex','metric_id':'test_capex','scope_id':'test_consolidated',
              'economic_boundary':'corporate_financial','denominator':'Cash additions to PP&E at consolidated company, excluding leases',
              'period_label':'2025-FY','period_kind':'fiscal_year','period_start':'2025-01-01',
              'period_end':'2025-12-31','value':'250.125','unit':'USD_million',
              'source_locator':'Cash Flow / capital expenditures',
              'normalized_concept':'capital_expenditure','statement_type':'cash_flow',
              'reporting_basis':'duration_year','reported_currency':'USD'
            }],
            'commitments':[{
              'id':'test-cloud','source_locator':'Commitments / Cloud capacity',
              'commitment_kind':'cloud_capacity','amount':'3000000000','currency':'USD',
              'amount_basis':'Absolute reported USD, no annualization',
              'economic_layer':'corporate_financial',
              'cancellation_terms':'undisclosed'
            }]
          }],
          'model_mappings':[{
            'id':'test-map','source_kind':'fact','source_ref':'test-capex',
            'target_input_key':'buyer_capex_not_cpu_sales',
            'source_boundary':'corporate_financial','target_boundary':'cpu_silicon',
            'transformation_method':'Proposal only: must identify server share and CPU BOM',
            'transformation_version':'v1','denominator_notes':'Not additive with server or CPU revenue'
          }]
        }
    def tearDown(self):
        self.tmp.cleanup()
    def write_packet(self):
        self.input.write_text(json.dumps(self.packet),encoding='utf-8')
    def connect(self):
        return db.open_db(self.dbpath)

    def test_watchlist_seeds_without_inventing_filings(self):
        cnx=self.connect()
        db.init(self.root,cnx)
        with cnx:
            self.assertEqual(db.financial_issuer_import(cnx,self.root),1)
            self.assertEqual(db.financial_issuer_import(cnx,self.root),1)
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM financial_issuers').fetchone()[0],1)
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM financial_filings').fetchone()[0],0)
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM measurements').fetchone()[0],0)
        cnx.close()

    def test_staged_intake_is_idempotent_and_non_additive(self):
        self.write_packet()
        r=db.ingest_financial(self.root,self.dbpath,self.input)
        self.assertEqual((r['filings'],r['facts'],r['commitments'],r['proposed_model_mappings']), (1,1,1,1))
        self.assertEqual(db.ingest_financial(self.root,self.dbpath,self.input),r)
        cnx=self.connect()
        self.assertEqual(db.verify(cnx),[])
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM financial_filings').fetchone()[0],1)
        fact=cnx.execute('SELECT * FROM v_financial_fact_context').fetchone()
        self.assertEqual(fact['value_decimal'],'250.125')
        self.assertEqual(fact['reporting_basis'],'duration_year')
        self.assertEqual(fact['verification_status'],'attributed_unverified')
        obligation=cnx.execute('SELECT * FROM v_financial_commitment_evidence').fetchone()
        self.assertEqual(obligation['amount_decimal'],'3000000000')
        self.assertEqual(obligation['economic_layer'],'corporate_financial')
        self.assertEqual(cnx.execute('SELECT review_status FROM financial_model_mappings').fetchone()[0],'proposed')
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM model_inputs').fetchone()[0],0)
        snapshot=self.root/'out.json'
        db.exports(cnx,snapshot)
        payload=json.loads(snapshot.read_text())
        self.assertEqual(len(payload['financial_facts']),1)
        self.assertEqual(len(payload['financial_commitments']),1)
        cnx.close()

    def test_cross_filing_locator_rejected_by_trigger(self):
        self.write_packet()
        db.ingest_financial(self.root,self.dbpath,self.input)
        cnx=self.connect()
        # A known source belonging to some other filing may not be substituted.
        other=db.source(cnx,'other-filing',title='Other filing',publisher='Other',uri='https://example.org/other')
        foreign=db.locator(cnx,other,'Item 10','filing_section')
        with self.assertRaises(sqlite3.IntegrityError):
            cnx.execute('UPDATE financial_fact_contexts SET source_locator_id=?',(foreign,))
        with self.assertRaises(sqlite3.IntegrityError):
            cnx.execute('UPDATE financial_commitments SET locator_id=?',(foreign,))
        cnx.close()

    def test_unreviewed_evidence_cannot_support_approved_model_mapping(self):
        self.write_packet()
        db.ingest_financial(self.root,self.dbpath,self.input)
        cnx=self.connect()
        cnx.execute("UPDATE financial_model_mappings SET review_status='approved',reviewer='synthetic-test',reviewed_at='2026-10-08' WHERE mapping_id='test-map'")
        self.assertTrue(any('unreviewed evidence' in x for x in db.verify(cnx)))
        cnx.close()

    def test_negative_commitments_flagged_and_invalid_input_rolls_back(self):
        self.packet['filings'][0]['commitments'][0]['amount']='not-a-number'
        self.write_packet()
        with self.assertRaisesRegex(ValueError,'Non-decimal'):
            db.ingest_financial(self.root,self.dbpath,self.input)
        cnx=self.connect()
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM financial_filings').fetchone()[0],0)
        self.assertEqual(cnx.execute('SELECT COUNT(*) FROM measurements').fetchone()[0],0)
        cnx.close()


if __name__=='__main__':
    unittest.main()
