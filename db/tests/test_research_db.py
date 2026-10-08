import csv
from decimal import Decimal
import json
import pathlib
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPT_ROOT/'scripts'))
import research_db as db


def write(root,relative,content):
    target=root/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(content,(dict,list)):
        target.write_text(json.dumps(content,indent=2)+'\n',encoding='utf-8')
    else:
        target.write_text(content,encoding='utf-8')


def fixture(root):
    for src in sorted((SCRIPT_ROOT/'migrations').glob('*.sql')):
        write(root,'db/migrations/'+src.name,src.read_text())
    write(root,'db/seed/foundation.json',json.loads((SCRIPT_ROOT/'seed/foundation.json').read_text()))
    write(root,'data/demand-2030/source-registry.json',{'sources':[
        {'id':'IDC_SERVER_2026','origin':'IDC','scope':'Worldwide server systems','url':'https://example.org/idc','published_at':'2026-07-28','kind':'tracker','access':'public','quality':'report'},
        {'id':'AMD_CITI_SEP2026','origin':'AMD','scope':'Global silicon TAM','url':'https://example.org/amd','published_at':'2026-09-08','kind':'conference','access':'public_secondary','quality':'claim'}]})
    header='id,period,frequency,metric,segment,value,unit,measurement_basis,evidence_status,source_id,source_year,caution\n'
    historical=header + '\n'.join([
       'H001,2025,annual,server_system_spending,world_all_server_systems,453.531,USD_billion,system_revenue,tracker_reported,IDC_SERVER_2026,2026,Complete servers',
       'H004,2026,annual,server_system_spending,world_all_server_systems,646.998,USD_billion,system_revenue,forecast,IDC_SERVER_2026,2026,Forecast only'])+'\n'
    write(root,'data/demand-2030/historical-and-forecast-evidence.csv',historical)
    vintage='id,issued_at,publisher,market,year_horizon,amount_usd_b,qualifier,scope,source_id,access_status,evidence_type,note\nT006,2026-07-23,AMD,world_server_cpu_silicon_TAM,2030,200,greater_than,all_architectures,AMD_CITI_SEP2026,keynote_derived,management_forecast,Attributed vendor estimate\n'
    write(root,'data/demand-2030/tam-forecast-vintages.csv',vintage)
    write(root,'data/claims/amd-advancing-ai-2026-curated.json',{
        'source_id':'amd-advancing-ai-2026-keynote-transcript','source_url':'https://youtube.com/watch?v=abc','event_date':'2026-07-23',
        'original_sha256':'0'*64,'records':[{'id':'A011','source_lines':[189,197],'metric':'2030 CPU TAM','value':200,'unit':'USD billion',
        'caveat':'Qualifiers matter','statement_class':'management_forecast'}]})
    write(root,'data/sources/amd-advancing-ai-2026-numeric-anchors.json',{'anchors':[{'line':191,'numeric_tokens':['200']} ]})
    write(root,'data/claims/amd-advancing-ai-2026-strategic-signals.json',{'records':[
        {'id':'Q001','source_line_range':'L74-L117','normalized_statement':'Agent execution is a possible new source of CPU demand','class_name':'vendor_strategy'}]})
    write(root,'data/claims/microsoft-docker-agentic-2026.json',{
      'sources':[{'id':'microsoft-windows-agentic-keynote','reference':'turnXXfile','transcript_lines':100},
                 {'id':'docker-sbx-microvm-talk','reference':'turnYYfile','transcript_lines':200}],
      'claims':[{'id':'MS08','source':'microsoft-windows-agentic-keynote','metric':'local_tokens','qualifier':'claimed','value':1600000,'unit':'tokens','status':'product_demo','source_lines':[1,2]}],
      'strategic':[{'id':'DK-S1','source':'docker-sbx-microvm-talk','title':'MicroVM overhead','detail':'Measure empirically','source_lines':[2,5]}]})
    rows=[]
    for scenario,split,shares in [('downside',[30,25,45],[.75,.35,.45]),('central',[40,55,105],[.82,.45,.55]),('upside',[44,70,121],[.9,.55,.65])]:
      r=[]
      for year in range(2025,2031):
        base=split if year==2030 else ([17.7,7,0.3] if year==2025 else [18,8,4])
        total=sum(Decimal(str(x)) for x in base)
        x86=sum((Decimal(str(x))*Decimal(str(s)) for x,s in zip(base,shares))) if year>2025 else None
        r.append(dict(year=year,foundational_usd_b=base[0],ai_host_usd_b=base[1],agent_execution_usd_b=base[2],total_cpu_silicon_tam_usd_b=float(total),
                      x86_silicon_tam_usd_b=float(x86) if x86 is not None else None,nonx86_silicon_tam_usd_b=float(total-x86) if x86 is not None else None))
      rows.append((scenario,r,{'foundational':shares[0],'ai_host':shares[1],'agent_execution':shares[2]}))
    write(root,'data/demand-2030/scenario-model.json',{'title':'Example synthetic scenario model','as_of':'2026-10-08',
      'year_rows':dict((k,v) for k,v,s in rows), 'architecture_share_by_workload_assumptions_for_2026_2030':dict((k,s) for k,v,s in rows)})
    write(root,'data/demand-2030/priority-data-fields.json',{'fields':[
      {'id':'D001','metric':'CPU core seconds per workflow','validation':'Instrument identical tasks'}]})


class ResearchDbTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.t.name)
        fixture(self.root)
        self.path=self.root/'db/runtime/test.sqlite'
    def tearDown(self):
        self.t.cleanup()
    def connect(self):
        return db.open_db(self.path)
    def test_seed_is_idempotent_and_preserves_evidence_kinds(self):
        report=db.seed(self.root,self.path)
        self.assertEqual(report['measurements'],1)
        self.assertEqual(report['market_forward_forecasts'],1)
        self.assertEqual(report['tam_forecasts'],1)
        c=self.connect()
        self.assertEqual(db.verify(c),[])
        self.assertEqual(c.execute('SELECT COUNT(*) FROM measurements').fetchone()[0],1)
        self.assertEqual(c.execute('SELECT COUNT(*) FROM forecasts').fetchone()[0],2)
        self.assertEqual(c.execute('SELECT COUNT(*) FROM evidence_claims').fetchone()[0],4)
        self.assertEqual(c.execute('SELECT COUNT(*) FROM source_locators WHERE source_id=?',('src:amd-advancing-ai-2026-keynote-transcript',)).fetchone()[0],3)
        self.assertEqual(c.execute('SELECT COUNT(*) FROM model_outputs').fetchone()[0],108)
        self.assertIsNone(c.execute("SELECT value_decimal FROM model_outputs WHERE target_year=2025 AND metric_key='x86_silicon_tam_usd_b' LIMIT 1").fetchone()[0])
        self.assertEqual(c.execute("SELECT resolution_state FROM conflicts WHERE conflict_id='conflict:idc-2024-server-systems-vintage'").fetchone()[0],'open')
        c.close()
        db.seed(self.root,self.path)
        c=self.connect()
        self.assertEqual(db.verify(c),[])
        self.assertEqual(c.execute('SELECT COUNT(*) FROM forecasts').fetchone()[0],2)
        self.assertEqual(c.execute('SELECT COUNT(*) FROM measurements').fetchone()[0],1)
        c.close()
    def test_sql_rejects_mismatched_taxonomy_axis_and_partition(self):
        db.seed(self.root,self.path)
        c=self.connect()
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO taxonomy_nodes(node_id,axis_id,parent_id,label) VALUES('badnode','buyer','isa:x86','Bad')")
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO partition_allocations(frame_id,node_id,weight_decimal) SELECT frame_id,'buyer:all','1' FROM partition_frames LIMIT 1")
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO source_documents(source_id,title,publisher) VALUES('orphan','x','y')")
        c.close()
    def test_source_drift_is_not_silently_overwritten(self):
        db.seed(self.root,self.path)
        path=self.root/'data/demand-2030/source-registry.json'
        x=db.load_json(path)
        x['sources'][0]['scope']='Completely changed market universe'
        path.write_text(json.dumps(x))
        with self.assertRaisesRegex(ValueError,'IMMUTABLE LEGACY ID COLLISION'):
            db.seed(self.root,self.path)
        c=self.connect()
        s=c.execute("SELECT title FROM source_documents WHERE source_id='src:IDC_SERVER_2026'").fetchone()[0]
        self.assertEqual(s,'Worldwide server systems')
        c.close()
    def test_forecast_qualifier_and_numeric_precision_are_kept(self):
        db.seed(self.root,self.path)
        c=self.connect()
        r=c.execute("SELECT qualifier,value_decimal FROM v_forecast_history WHERE forecast_id='forecast:tam:T006'").fetchone()
        self.assertEqual((r[0],r[1]),('greater_than','200'))
        self.assertEqual(db.numeric('0.00000001234000'),'0.00000001234000')
        self.assertEqual(c.execute("SELECT COUNT(*) FROM v_measurement_evidence WHERE economic_boundary='server_system'").fetchone()[0],1)
        c.close()
    def test_partition_mass_balance_and_synthetic_actual_separation(self):
        db.seed(self.root,self.path)
        c=self.connect()
        frame=c.execute('SELECT frame_id FROM partition_frames LIMIT 1').fetchone()[0]
        c.execute('UPDATE partition_allocations SET weight_decimal=? WHERE frame_id=? AND node_id=?',('0.01',frame,'isa:x86'))
        self.assertTrue(any('does not sum to 1' in x for x in db.verify(c)))
        self.assertEqual(c.execute("SELECT COUNT(*) FROM measurements WHERE metric_id='server_cpu_silicon_TAM'").fetchone()[0],0)
        c.close()
    def test_snapshot_discloses_forecast_and_synthetic_status(self):
        db.seed(self.root,self.path)
        c=self.connect()
        out=self.root/'snapshot.json'
        summary=db.exports(c,out)
        d=json.loads(out.read_text())
        self.assertEqual(summary['measurements'],1)
        self.assertEqual(summary['forecasts'],2)
        self.assertEqual(summary['synthetic_scenarios'],108)
        self.assertTrue(all('evidence_kind' in x for x in d['measurements']))
        self.assertTrue(all('forecast_kind' in x for x in d['forecasts']))
        c.close()

    def test_new_source_registry_entry_preserves_prior_unmodified_rows(self):
        db.seed(self.root,self.path)
        path=self.root/'data/demand-2030/source-registry.json'
        source_info=db.load_json(path)
        source_info['sources'].append({'id':'NEW2026','origin':'Example','scope':'Independent report','url':'https://example.org/new','published_at':'2026-10-08','kind':'article','access':'public','quality':'primary'})
        path.write_text(json.dumps(source_info))
        db.seed(self.root,self.path)
        c=self.connect()
        self.assertEqual(db.verify(c),[])
        self.assertEqual(c.execute("SELECT COUNT(*) FROM source_documents WHERE source_id IN ('src:IDC_SERVER_2026','src:NEW2026')").fetchone()[0],2)
        c.close()


if __name__=='__main__':unittest.main()
