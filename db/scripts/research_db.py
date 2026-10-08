#!/usr/bin/env python3
"""CORE/SIGNAL v1 research store: zero-dependency SQLite, conservative legacy import.

Usage: python db/scripts/research_db.py [init|seed|verify|stats|export|query] [--db PATH] [--root REPO]
Safety: never overwrite a sourced value by ID, never convert a forecast into an observation,
never treat a scenario as actual; source dataset drift is a review error.
"""
from __future__ import annotations
import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ['0001_core.sql', '0002_views.sql', '0003_financial_filings.sql']


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def source_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numeric(value):
    if value is None:
        return None
    try:
        d = Decimal(str(value))
        if not d.is_finite():
            raise ValueError('NaN/Infinity are prohibited')
        return format(d, 'f')
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f'Non-decimal number: {value!r}') from exc


def stored(cnx, table, key, record):
    """Idempotent exact-match insert. Any same-ID changes demand explicit review/migration."""
    columns = list(record)
    vals = [record[x] for x in columns]
    quoted = ','.join('"'+c+'"' for c in columns)
    markers = ','.join('?' for _ in columns)
    cnx.execute(f'INSERT OR IGNORE INTO {table} ({quoted}) VALUES({markers})', vals)
    keys = list(key) if isinstance(key, tuple) else [key]
    where = ' AND '.join('\"'+c+'\"=?' for c in keys)
    existing = cnx.execute(f'SELECT {quoted} FROM {table} WHERE {where}', tuple(record[k] for k in keys)).fetchone()
    if existing is None:
        raise ValueError(f'Missing after insert {table}:{record[key]}')
    # The batch is the containing file version. Adding one new row changes the file
    # digest but must not rewrite other, unchanged evidence records.
    differences = [(col, existing[col], record[col]) for col in columns
                   if col not in ('batch_id', 'import_batch') and existing[col] != record[col]]
    if differences:
        raise ValueError(f'IMMUTABLE LEGACY ID COLLISION {table}:{record[key]}; changes {differences[:3]} — create a new vintage or review migration')


def object_id(cnx, oid, kind):
    stored(cnx, 'objects', 'object_id', dict(object_id=oid, object_type=kind))
    return oid


def batch(cnx, root, rel, source_kind='legacy_import'):
    path = root / rel
    if not path.exists():
        return None
    digest = source_digest(path)
    identifier = 'batch:' + hashlib.sha256((str(rel)+'|'+digest).encode()).hexdigest()[:20]
    stored(cnx, 'ingestion_batches', 'batch_id', dict(batch_id=identifier, input_path=str(rel), content_sha256=digest, source_kind=source_kind))
    return identifier


def source(cnx, sid, *, title, publisher, uri=None, published=None, version='', kind='other', access='public', rights='link_and_extract', sha=None, legacy='', note='', batch_id=None):
    oid = object_id(cnx, 'src:'+sid, 'source')
    stored(cnx, 'source_documents', 'source_id', dict(source_id=oid, title=title, publisher=publisher, canonical_uri=uri, publication_date=published,
           source_version=version, document_kind=kind, access_status=access, rights_status=rights, digest_sha256=sha, legacy_ref=legacy, note=note, batch_id=batch_id))
    return oid


def locator(cnx, source_id, value, kind='legacy_pointer'):
    sid='loc:'+hashlib.sha256((source_id+'|'+kind+'|'+value).encode()).hexdigest()[:24]
    stored(cnx,'source_locators','locator_id',dict(locator_id=sid,source_id=source_id,locator_kind=kind,locator_value=value))
    return sid


def claim(cnx, ident, *, src, statement, kind='vendor_claim', verification='attributed_unverified', locator_value=None, locator_kind='legacy_pointer', qualifier='', legacy=None, ingest_batch=None):
    oid=object_id(cnx, 'claim:'+ident, 'claim')
    loc=locator(cnx,src,locator_value,locator_kind) if locator_value else None
    stored(cnx,'evidence_claims','claim_id',dict(claim_id=oid,source_id=src,locator_id=loc,statement=statement,claim_kind=kind,
                                                verification=verification,claim_qualifier=qualifier,legacy_ref=legacy,batch_id=ingest_batch))
    if legacy:
        link(cnx,legacy,oid,ingest_batch)
    return oid


def link(cnx, legacy, oid, batch_id):
    if batch_id is None:
        raise ValueError('Legacy link must specify import batch')
    stored(cnx,'legacy_links','legacy_ref',dict(legacy_ref=legacy,object_id=oid,import_batch=batch_id))


def ensure_metric(cnx, metric_id, unit, boundary, basis=''):
    numeric_units=['USD_billion','USD_million','USD','percent','cores','sockets','unit','tokens']
    if unit.startswith('USD'):
        kind='currency'
    elif unit in ('percent','ratio','x') or 'percent' in unit:
        kind='ratio'
    elif 'core' in unit or 'unit' in unit or 'socket' in unit:
        kind='unit_count'
    elif 'power' in metric_id or unit in ('W','kW','MW'):
        kind='power'
    elif 'revenue' in metric_id and 'growth' in metric_id:
        kind='rate'
    else:
        kind='other'
    existing=cnx.execute('SELECT metric_id,canonical_unit FROM metric_definitions WHERE metric_id=?',(metric_id,)).fetchone()
    if existing:
        # Different units in a single metric ID are a data definition conflict, not a silent overwrite.
        if existing['canonical_unit']!=unit:
            raise ValueError(f'Metric unit conflict {metric_id}: {existing["canonical_unit"]} vs {unit}')
        return
    stored(cnx,'metric_definitions','metric_id',dict(metric_id=metric_id, display_name=metric_id.replace('_',' '),quantity_kind=kind,
        canonical_unit=unit, expected_boundary=boundary, aggregation_rule='non_additive',denominator_description=basis,
        interpretation='Legacy source metric. Requires semantic review before aggregation.', status='draft'))


def boundary(metric, scope, basis=''):
    if metric == 'server_system_spending' or metric.startswith('server_system_') or 'server_system' in scope:
        return 'server_system'
    if 'capex' in metric or scope in ('meta_company','supermicro_company','coreweave_company','dell_infrastructure_solutions'):
        return 'corporate_financial'
    if any(x in metric for x in ('intel_server_cpu','amd_server_x86','amd_epyc','amd_cloud_epyc','amd_enterprise_epyc')) or 'server_cpus' in scope or 'server_x86' in scope:
        return 'cpu_silicon'
    if scope.endswith('server_segment') or 'server_network' in scope or 'ai_server_systems' in scope:
        return 'server_system'
    if 'oracle_iaas' in metric or 'cloud_infrastructure' in scope:
        return 'cloud_service'
    if any(x in metric for x in ('hpe_','dell_','supermicro_','coreweave_')):
        return 'corporate_financial'
    return 'unresolved'


def ensure_scope(cnx, name, kind, basis=''):
    old=cnx.execute('SELECT economic_boundary FROM market_scopes WHERE scope_id=?',(name,)).fetchone()
    if old:
        if old['economic_boundary'] != kind and old['economic_boundary'] != 'unresolved' and kind != 'unresolved':
            raise ValueError(f'Conflicting accounting boundaries for scope {name}: {old["economic_boundary"]} vs {kind}')
        return
    stored(cnx,'market_scopes','scope_id',dict(scope_id=name,label=name.replace('_',' '),economic_boundary=kind,
        population=name,denominator_description=basis or ('Population named '+name+'; confirm with original source.'),accounting_notes='Legacy classification not automatically additive with other scopes'))


def date_precision(text):
    if re.match(r'^\d{4}-\d{2}-\d{2}$',text): return 'day'
    if re.match(r'^\d{4}-\d{2}$',text): return 'month'
    if re.match(r'^\d{4}$',text): return 'year'
    return 'unknown'


def period_kind(period, frequency):
    if 'FYQ' in period or frequency=='fiscal_quarter':return 'fiscal_quarter'
    if frequency=='fiscal_year' or period.endswith('-FY') or re.match(r'^\d{4}-FY$',period): return 'fiscal_year'
    if re.match(r'^\d{4}-Q[1-4]$',period): return 'calendar_quarter'
    if re.match(r'^\d{4}$',period): return 'calendar_year'
    return 'other'


def ensure_vintage(cnx, vintage_id, src, publisher, issued, kind='analyst', access='', note=''):
    stored(cnx,'forecast_vintages','vintage_id',dict(vintage_id=vintage_id,source_id=src,publisher=publisher,issued_at=issued,
        issued_date_precision=date_precision(issued),forecast_kind=kind,access_note=access,note=note))


def source_import(cnx, root):
    rel='data/demand-2030/source-registry.json'; bid=batch(cnx,root,rel)
    if not bid:return {}
    out={}
    for x in load_json(root/rel)['sources']:
        access=x.get('access','public')
        accepted={'public':'public','public_primary':'public','public_secondary':'public_secondary','public_transcript':'public_secondary',
            'public_secondary_only':'public_secondary','public_company_retrospective':'public_secondary','paywalled_not_accessed':'paywalled_unverified',
            'not_accessed':'paywalled_unverified','licensed_unavailable':'licensed_unavailable'}
        sta=accepted.get(access,'unverified')
        out[x['id']]=source(cnx,x['id'],title=x.get('scope',x['id']),publisher=x.get('origin',x['id']),uri=x.get('url'),published=x.get('published_at'),
            kind=x.get('kind','other'),access=sta, rights='unknown_do_not_copy' if sta in ('paywalled_unverified','licensed_unavailable') else 'link_and_extract',
            note='Registry quality: '+x.get('quality','unknown')+'; verification required. '+x.get('scope',''),legacy=rel+'#'+x['id'],batch_id=bid)
    return out


def observations_import(cnx,root, sources):
    rel='data/demand-2030/historical-and-forecast-evidence.csv';bid=batch(cnx,root,rel)
    if not bid:return(0,0)
    n_meas=n_fc=0
    with (root/rel).open(newline='',encoding='utf-8') as f:
        for x in csv.DictReader(f):
            raw_kind=x['evidence_status']
            src=sources.get(x['source_id'])
            if not src: raise ValueError(f'Unregistered source in historical evidence: {x["source_id"]}')
            m=x['metric'];sc=x['segment'];e=boundary(m,sc,x['measurement_basis']); v=numeric(x['value']);unit=x['unit']
            ensure_metric(cnx,m,unit,e,x['measurement_basis']);ensure_scope(cnx,sc,e,x['caution'])
            legacy=rel+'#'+x['id']
            if raw_kind in ('forecast','company_forecast'):
                fid='forecast:legacy:'+x['id'];object_id(cnx,fid,'forecast')
                vid='vintage:'+x['source_id']+':'+str(x['source_year'])
                ensure_vintage(cnx,vid,src,x['source_id'],str(x['source_year']),kind='market_tracker' if 'tracker' in x['source_id'].lower() or 'IDC' in x['source_id'] else 'management',
                               note='Historical CSV forward estimate; exact release day captured in source registry')
                stored(cnx,'forecasts','forecast_id',dict(forecast_id=fid,vintage_id=vid,metric_id=m,scope_id=sc,target_period=x['period'],value_decimal=v,
                    unit=unit,qualifier='equal',estimate_kind='point',legacy_ref=legacy,note=x['caution']))
                link(cnx,legacy,fid,bid);n_fc+=1
            else:
                oid=object_id(cnx,'measure:legacy:'+x['id'],'measurement')
                evidence=raw_kind if raw_kind in ('company_reported','tracker_reported','secondary_estimate','independent_measurement','vendor_benchmark','anecdote','derived_from_observed') else 'secondary_estimate'
                qual='greater_than' if raw_kind=='company_claim_lower_bound' else 'equal'
                stored(cnx,'measurements','measurement_id',dict(measurement_id=oid,metric_id=m,scope_id=sc,source_id=src,claim_id=None,
                      period_label=x['period'],period_kind=period_kind(x['period'],x['frequency']),start_date=None,end_date=None,
                      value_decimal=v,unit=unit,qualifier=qual,evidence_kind=evidence,verification_status='attributed_unverified',
                      measurement_basis=x['measurement_basis'],note=x['caution']+'; raw evidence_status='+raw_kind,
                      legacy_ref=legacy,batch_id=bid))
                link(cnx,legacy,oid,bid);n_meas+=1
    return(n_meas,n_fc)


def tam_import(cnx,root,sources):
    rel='data/demand-2030/tam-forecast-vintages.csv';bid=batch(cnx,root,rel)
    if not bid:return 0
    count=0
    with (root/rel).open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            src=sources.get(row['source_id'])
            if not src:raise ValueError('Missing TAM source '+row['source_id'])
            scope=row['market']+':'+row['scope']
            ensure_scope(cnx,scope,'cpu_silicon','Global server CPU silicon TAM, not whole-server system spending')
            mid='server_cpu_silicon_TAM'
            ensure_metric(cnx,mid,'USD_billion','cpu_silicon','All-architecture global server CPU silicon revenue opportunity')
            vid='vintage:tam:'+row['id'];ensure_vintage(cnx,vid,src,row['publisher'],row['issued_at'],kind='management' if row['evidence_type']=='management_forecast' else 'analyst',access=row['access_status'],note=row['note'])
            oid=object_id(cnx,'forecast:tam:'+row['id'],'forecast')
            legacy=rel+'#'+row['id']
            stored(cnx,'forecasts','forecast_id',dict(forecast_id=oid,vintage_id=vid,metric_id=mid,scope_id=scope,target_period=row['year_horizon'],
                value_decimal=numeric(row['amount_usd_b']),unit='USD_billion',qualifier=row['qualifier'],estimate_kind='point',legacy_ref=legacy,note=row['note']))
            link(cnx,legacy,oid,bid);count+=1
    return count


def keynote_import(cnx,root):
    rel='data/claims/amd-advancing-ai-2026-curated.json';bid=batch(cnx,root,rel)
    if not bid:return(0,0)
    corpus=load_json(root/rel)
    src=source(cnx,corpus['source_id'],title='AMD Advancing AI 2026 keynote',publisher='AMD',uri=corpus.get('source_url'),published=corpus['event_date'],
               sha=corpus.get('original_sha256'),kind='keynote_transcript_index',access='public',rights='quote_with_limits',legacy=rel,batch_id=bid,
               note='Video public; original user-uploaded transcript not redistributed in this repository.')
    count=0
    for x in corpus['records']:
        ident='amd2026:'+x['id'];legacy=rel+'#'+x['id']
        span='L'+str(x['source_lines'][0])+'-L'+str(x['source_lines'][1])
        stmt=x['metric']+': '+str(x['value'])+' '+str(x['unit'])+'. '+x.get('caveat','')
        claim(cnx,ident,src=src,statement=stmt,kind=x['statement_class'],locator_value=span,locator_kind='line_range',
              verification='attributed_unverified',legacy=legacy,ingest_batch=bid)
        count+=1
    anchors_rel='data/sources/amd-advancing-ai-2026-numeric-anchors.json';ba=batch(cnx,root,anchors_rel)
    if ba:
        for entry in load_json(root/anchors_rel)['anchors']:
            locator(cnx,src,'L'+str(entry['line']),'line_range')
    signals_rel='data/claims/amd-advancing-ai-2026-strategic-signals.json';bs=batch(cnx,root,signals_rel);n=0
    if bs:
        for x in load_json(root/signals_rel)['records']:
            claim(cnx,'amd2026:signal:'+x['id'],src=src,statement=x['normalized_statement'],kind=x['class_name'],
                locator_value=x['source_line_range'],locator_kind='line_range',legacy=signals_rel+'#'+x['id'],ingest_batch=bs)
            n+=1
    return count,n


def microsoft_docker_import(cnx,root):
    rel='data/claims/microsoft-docker-agentic-2026.json';bid=batch(cnx,root,rel)
    if not bid:return(0,0)
    data=load_json(root/rel)
    sr={}
    for x in data['sources']:
        # Uploaded transcript not a portable public source URL; do not hallucinate one.
        sr[x['id']]=source(cnx,x['id'],title=x['id']+' auto-generated transcript index',publisher='Microsoft' if 'microsoft' in x['id'] else 'Docker',
            uri=None,published=None,kind='user_supplied_transcript_index',access='local_pointer_unavailable',rights='unknown_do_not_copy',
            legacy=rel+'#'+x['id'],batch_id=bid,note='Original transcript conversation pointer '+x.get('reference','')+' unavailable across sessions; verify public video before promotion.')
    for x in data['claims']:
        loc='L'+str(x['source_lines'][0])+'-L'+str(x['source_lines'][1])
        claim(cnx,'microsoft-docker:'+x['id'],src=sr[x['source']],statement=x['metric']+': '+str(x['qualifier'])+' '+str(x['value'])+' '+x['unit'],kind=x['status'],
            locator_value=loc,locator_kind='line_range',legacy=rel+'#'+x['id'],ingest_batch=bid)
    for x in data['strategic']:
        loc='L'+str(x['source_lines'][0])+'-L'+str(x['source_lines'][1])
        claim(cnx,'microsoft-docker:'+x['id'],src=sr[x['source']],statement=x['title']+': '+x['detail'],kind='strategic_signal',
            locator_value=loc,locator_kind='line_range',legacy=rel+'#'+x['id'],ingest_batch=bid)
    return len(data['claims']),len(data['strategic'])


def taxonomy_import(cnx,root):
    foundation=load_json(root/'db/seed/foundation.json')
    for a in foundation['axes']:
        stored(cnx,'taxonomy_axes','axis_id',dict(axis_id=a['id'],label=a['label'],meaning=a['meaning'],additive_partition=1 if a['additive'] else 0))
    for n in foundation['nodes']:
        stored(cnx,'taxonomy_nodes','node_id',dict(node_id=n[0],axis_id=n[1],parent_id=n[2],label=n[3]))
    return len(foundation['nodes'])


def scenario_import(cnx,root):
    rel='data/demand-2030/scenario-model.json';bid=batch(cnx,root,rel,source_kind='model_export')
    if not bid:return 0
    doc=load_json(root/rel);sha=source_digest(root/rel)
    mod=object_id(cnx,'model:demand2030','model')
    stored(cnx,'calculation_models','model_id',dict(model_id=mod,title=doc['title'],metric_boundary='cpu_silicon',version='1.0',
        description='Legacy authored analytical sensitivity, never an observed market forecast.',definition_path=rel,code_sha256=None))
    n=0
    for scenario,rows in doc['year_rows'].items():
        run=object_id(cnx,'modelrun:demand2030:'+scenario+':'+sha[:16],'model_run')
        stored(cnx,'model_runs','run_id',dict(run_id=run,model_id=mod,scenario_name=scenario,as_of=doc['as_of'],source_sha256=sha,is_synthetic=1,status='reproduced'))
        assump=doc['architecture_share_by_workload_assumptions_for_2026_2030'][scenario]
        stored(cnx,'model_inputs','run_id',dict(run_id=run,input_key='isa_shares_2026_2030',value_json=json.dumps(assump,sort_keys=True,separators=(',',':')),
                                                meaning='Illustrative x86 fraction for each nonoverlapping workload pool'))
        for row in rows:
            for k,val in row.items():
                if not k.endswith('_usd_b'):continue
                if k.startswith('foundational'):seg='foundational'
                elif k.startswith('ai_host'):seg='ai_host'
                elif k.startswith('agent_execution'):seg='agent_execution'
                else:seg='total'
                stored(cnx,'model_outputs',('run_id','target_year','metric_key','segment_key'),dict(run_id=run,target_year=row['year'],metric_key=k,segment_key=seg,
                     value_decimal=numeric(val),unit='USD_billion',is_missing=1 if val is None else 0,
                     missing_reason='Unknown 2025 actual architecture allocation; scenario intentionally leaves blank' if val is None else None))
                n+=1
        # A checked mutually exclusive x86 vs non-x86 architecture split per workload pool.
        for segment, share in assump.items():
            frame='frame:'+scenario+':'+segment+':2026-2030:'+sha[:8]
            stored(cnx,'partition_frames','frame_id',dict(frame_id=frame,scenario_or_source_ref=run,axis_id='isa',period_label='2026-2030',
                aggregation_basis='fractions of illustrative CPU silicon TAM for '+segment,exclusivity='mutually_exclusive',status='checked'))
            for node,v in [('isa:x86',share),('isa:non_x86',Decimal(1)-Decimal(str(share)))]:
                cnx.execute('INSERT OR IGNORE INTO partition_allocations(frame_id,node_id,weight_decimal) VALUES(?,?,?)',(frame,node,numeric(v)))
                old=cnx.execute('SELECT weight_decimal FROM partition_allocations WHERE frame_id=? AND node_id=?',(frame,node)).fetchone()['weight_decimal']
                if Decimal(old)!=Decimal(str(v)):
                    raise ValueError('Conflicting model partition value in '+frame)
    return n


def project_gaps(cnx,root):
    rel='data/demand-2030/priority-data-fields.json';bid=batch(cnx,root,rel)
    if not bid:return 0
    d=load_json(root/rel)
    for x in d['fields'][:15]:
        oid=object_id(cnx,'question:priority:'+x['id'],'question')
        stored(cnx,'research_questions','question_id',dict(question_id=oid,question='How can we obtain and validate '+x['metric']+'?',
            priority='P0',verification_method=x['validation'],legacy_ref=rel+'#'+x['id']))
        link(cnx,rel+'#'+x['id'],oid,bid)
    return min(15,len(d['fields']))


def financial_issuer_import(cnx, root):
    """Seed acquisition targets only; a target is not a filing or an observation."""
    rel = 'data/financial-filings/issuer-watchlist.json'
    path = root / rel
    if not path.exists():
        return 0
    manifest = load_json(path)
    if manifest.get('schema_version') != '1.0':
        raise ValueError('Unsupported financial issuer watchlist schema')
    seen = set()
    for issuer in manifest['issuers']:
        iid = issuer['id']
        if iid in seen:
            raise ValueError('Duplicate financial issuer '+iid)
        seen.add(iid)
        if issuer['priority'] not in ('P0','P1','P2','P3'):
            raise ValueError('Invalid financial issuer priority '+iid)
        stored(cnx, 'financial_issuers', 'issuer_id', dict(
            issuer_id=iid, entity_id=None, legal_name=issuer['name'],
            primary_symbol=issuer.get('symbol'), jurisdiction=issuer['jurisdiction'],
            primary_regulator=issuer['regulator'],
            investor_relations_url=issuer.get('investor_relations_url'),
            role_tags_json=json.dumps(issuer.get('roles', []), sort_keys=True,
                                      separators=(',', ':')),
            acquisition_priority=issuer['priority'],
            coverage_start_year=issuer.get('coverage_start_year', 2019),
            note='Acquisition target only, NOT retrieved filing evidence.'))
    return len(seen)


def ingest_financial(root, db_path, input_path):
    """Transactional, offline, public-only manual filing intake; never auto-promotes."""
    path = input_path.resolve()
    doc = load_json(path)
    if doc.get('schema_version') != '1.0' or not isinstance(doc.get('filings'), list):
        raise ValueError('Expected financial filing input schema_version 1.0 and filings array')
    cnx = open_db(db_path)
    try:
        init(root, cnx)
        with cnx:
            financial_issuer_import(cnx, root)
            digest = source_digest(path)
            bid = 'batch:financial:' + hashlib.sha256((str(path)+'|'+digest).encode()).hexdigest()[:20]
            stored(cnx, 'ingestion_batches', 'batch_id', dict(
                batch_id=bid, input_path=str(path), content_sha256=digest,
                source_kind='research_packet', state='staged',
                note='Public financial filing intake. Requires independent evidence review.'))
            fcount = mcount = ccount = mapping_count = 0
            fact_ids, commitment_ids = {}, {}
            for f in doc['filings']:
                if not f['url'].startswith('https://'):
                    raise ValueError('Public HTTPS filing URL required')
                issuer = cnx.execute('SELECT legal_name FROM financial_issuers WHERE issuer_id=?',
                                     (f['issuer_id'],)).fetchone()
                if issuer is None:
                    raise ValueError('Unknown issuer: '+f['issuer_id'])
                src = source(cnx, f['source_id'], title=f['title'],
                             publisher=issuer['legal_name'], uri=f['url'],
                             published=f['filed_at'], version=f.get('source_version',''),
                             kind='financial_filing', access='public',
                             rights='link_and_extract',
                             sha=f.get('digest_sha256'),
                             note='Public source metadata; extracted facts require review.',
                             batch_id=bid)
                fid = f['id']
                stored(cnx, 'financial_filings', 'filing_id', dict(
                    filing_id=fid, issuer_id=f['issuer_id'], source_id=src,
                    regulator=f['regulator'], filing_type=f['filing_type'],
                    accession_or_document_id=f.get('accession_or_document_id'),
                    period_start=f.get('period_start'), period_end=f.get('period_end'),
                    fiscal_year=f.get('fiscal_year'), fiscal_quarter=f.get('fiscal_quarter'),
                    filed_at=f['filed_at'], accepted_at=f.get('accepted_at'),
                    amendment_of=f.get('amendment_of'),
                    extraction_status='needs_review' if f.get('facts') or f.get('commitments') else 'indexed',
                    note='Intake stage only; not independently verified.'))
                fcount += 1
                for x in f.get('facts',[]):
                    external_id=x['id']
                    if external_id in fact_ids:
                        raise ValueError('Duplicate fact id: '+external_id)
                    mid=object_id(cnx, 'measure:filing:'+external_id, 'measurement')
                    metric=x['metric_id']; unit=x['unit']; bound=x['economic_boundary']
                    ensure_metric(cnx,metric,unit,bound,x['denominator'])
                    ensure_scope(cnx,x['scope_id'],bound,x['denominator'])
                    loc=locator(cnx,src,x['source_locator'],'filing_section')
                    stored(cnx,'measurements','measurement_id',dict(
                        measurement_id=mid,metric_id=metric,scope_id=x['scope_id'],
                        source_id=src,claim_id=None,period_label=x['period_label'],
                        period_kind=x['period_kind'],start_date=x.get('period_start'),
                        end_date=x.get('period_end'),value_decimal=numeric(x['value']),
                        unit=unit,qualifier=x.get('qualifier','equal'),
                        evidence_kind='company_reported',
                        verification_status='attributed_unverified',
                        measurement_basis=x['denominator'],
                        note='Public filing extract; unreviewed. '+x.get('note',''),
                        legacy_ref=None,batch_id=bid))
                    stored(cnx,'financial_fact_contexts','measurement_id',dict(
                        measurement_id=mid,filing_id=fid,source_locator_id=loc,
                        xbrl_taxonomy=x.get('xbrl_taxonomy'),xbrl_concept=x.get('xbrl_concept'),
                        normalized_concept=x['normalized_concept'],
                        statement_type=x['statement_type'],reporting_basis=x['reporting_basis'],
                        accounting_standard=x.get('accounting_standard','not_disclosed'),
                        reported_currency=x.get('reported_currency'),
                        consolidation_scope=x.get('consolidation_scope','not_disclosed'),
                        segment_label=x.get('segment_label'),
                        original_context_ref=x.get('original_context_ref'),
                        is_restated=int(bool(x.get('is_restated',False)))))
                    fact_ids[external_id]=mid;mcount+=1
                for x in f.get('commitments',[]):
                    cid=x['id']
                    if cid in commitment_ids:
                        raise ValueError('Duplicate commitment id: '+cid)
                    loc=locator(cnx,src,x['source_locator'],'filing_section')
                    amount=x.get('amount')
                    stored(cnx,'financial_commitments','commitment_id',dict(
                        commitment_id=cid,filing_id=fid,locator_id=loc,
                        obligor_issuer_id=f['issuer_id'],
                        counterparty_issuer_id=x.get('counterparty_issuer_id'),
                        counterparty_name_public=x.get('counterparty_name_public'),
                        commitment_kind=x['commitment_kind'],
                        amount_decimal=numeric(amount) if amount is not None else None,
                        currency=x.get('currency') if amount is not None else None,
                        qualifier=x.get('qualifier','equal') if amount is not None else 'unquantified',
                        start_date=x.get('start_date'),end_date=x.get('end_date'),
                        cancellation_terms=x.get('cancellation_terms','undisclosed'),
                        amount_basis=x['amount_basis'],economic_layer=x['economic_layer'],
                        status='disclosed',verification_status='attributed_unverified',
                        note='Unreviewed, non-additive disclosure. '+x.get('note','')))
                    commitment_ids[cid]=cid;ccount+=1
            for x in doc.get('model_mappings',[]):
                if x['source_kind'] not in ('fact','commitment'):
                    raise ValueError('Mapping source_kind must be fact or commitment')
                sid=x['source_ref']
                fact = fact_ids.get(sid) if x['source_kind']=='fact' else None
                commitment = commitment_ids.get(sid) if x['source_kind']=='commitment' else None
                if fact is None and commitment is None:
                    raise ValueError('Mapping must reference a fact/commitment in the same intake: '+sid)
                stored(cnx,'financial_model_mappings','mapping_id',dict(
                    mapping_id=x['id'],measurement_id=fact,commitment_id=commitment,
                    target_model_id=x.get('target_model_id'),
                    target_input_key=x['target_input_key'],
                    source_boundary=x['source_boundary'],target_boundary=x['target_boundary'],
                    transformation_method=x['transformation_method'],
                    transformation_version=x['transformation_version'],
                    denominator_notes=x['denominator_notes'],
                    uncertainty_notes=x.get('uncertainty_notes',''),
                    review_status='proposed',reviewer=None,reviewed_at=None))
                mapping_count+=1
        problems=verify(cnx)
        if problems:
            raise ValueError('Financial intake validation errors: '+str(problems))
        return dict(filings=fcount,facts=mcount,commitments=ccount,
                    proposed_model_mappings=mapping_count,review_state='staged')
    finally:
        cnx.close()


def seed(root,db):
    cnx=open_db(db)
    init(root,cnx)
    try:
        with cnx:
            tax=taxonomy_import(cnx,root)
            financial_issuers=financial_issuer_import(cnx,root)
            src=source_import(cnx,root)
            measures,forward=observations_import(cnx,root,src)
            tam=tam_import(cnx,root,src)
            claims,signals=keynote_import(cnx,root)
            ms,ms_signals=microsoft_docker_import(cnx,root)
            outputs=scenario_import(cnx,root)
            questions=project_gaps(cnx,root)
            # A source-vintage discrepancy from existing research remains unresolved.
            review=source(cnx,'idc-2024-vintage-unverified',title='Unreconciled IDC 2024 server spending estimate mentioned in existing market synthesis',
                publisher='Research recap (unverified original vintage)',uri=None,kind='analysis_note',access='unverified',rights='unknown_do_not_copy',
                note='Do not plot as actual: 2024 $235.7B vs ~ $254.5B inferred from newer IDC 2025 base and growth. Source vintage unverified.')
            left=src.get('IDC_SERVER_2026')
            if left:
                oid=object_id(cnx,'conflict:idc-2024-server-systems-vintage','conflict')
                stored(cnx,'conflicts','conflict_id',dict(conflict_id=oid,left_object_id=left,right_object_id=review,
                      issue='2024 worldwide server-system value differs across IDC source vintages; market scope and series revision unresolved.',
                      resolution_state='open',resolution_method='Locate and independently compare original dated IDC 2024 and 2025 series, geography, accelerator inclusion and reported growth.'))
    finally:
        cnx.close()
    return dict(financial_issuers=financial_issuers,taxonomy_nodes=tax,sources=len(src)+4,measurements=measures,market_forward_forecasts=forward,tam_forecasts=tam,
                amd_keynote_claims=claims,amd_strategic_signals=signals,microsoft_docker_claims=ms,microsoft_docker_signals=ms_signals,
                scenario_cells=outputs,priority_questions=questions)


def open_db(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(str(path))
    c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    c.execute('PRAGMA busy_timeout=3000')
    c.execute('PRAGMA journal_mode=WAL')
    return c


def init(root,cnx):
    for fname in SCHEMA:
        sql=(root/'db/migrations'/fname).read_text(encoding='utf-8')
        digest=hashlib.sha256(sql.encode('utf-8')).hexdigest()
        cnx.executescript(sql)
        row=cnx.execute('SELECT checksum_sha256 FROM schema_migrations WHERE migration_id=?',(fname,)).fetchone()
        if row and row['checksum_sha256']!=digest:
            raise ValueError('Applied schema migration has been changed: '+fname+'; add a new migration')
        if not row:
            cnx.execute('INSERT INTO schema_migrations(migration_id,checksum_sha256) VALUES(?,?)',(fname,digest))
            cnx.commit()


def verify(cnx):
    problems=[]
    # SQLite foreign keys enforce most lineage constraints.
    problems += ['FOREIGN KEY '+str(dict(x)) for x in cnx.execute('PRAGMA foreign_key_check')]
    for p in cnx.execute("SELECT frame_id FROM partition_frames WHERE exclusivity='mutually_exclusive'"):
        values=[Decimal(row[0]) for row in cnx.execute('SELECT weight_decimal FROM partition_allocations WHERE frame_id=?',(p['frame_id'],))]
        if not values or sum(values)!=Decimal(1):
            problems.append(f'Partition {p["frame_id"]} does not sum to 1: {values}')
        if any(v<0 or v>1 for v in values): problems.append('Partition share out of [0,1]: '+p['frame_id'])
    for run in cnx.execute('SELECT run_id, scenario_name FROM model_runs'):
        byyear={}
        for x in cnx.execute('SELECT target_year,metric_key,value_decimal FROM model_outputs WHERE run_id=?',(run['run_id'],)):
            byyear.setdefault(x['target_year'],{})[x['metric_key']]=Decimal(x['value_decimal']) if x['value_decimal'] is not None else None
        for year,vals in byyear.items():
            three=['foundational_usd_b','ai_host_usd_b','agent_execution_usd_b']
            if not all(k in vals for k in three+['total_cpu_silicon_tam_usd_b']):
                problems.append('Missing workload cells for '+run['run_id']+' year '+str(year));continue
            if sum(vals[k] for k in three)!=vals['total_cpu_silicon_tam_usd_b']:
                problems.append('Workload subtotal mismatch '+run['run_id']+' year '+str(year))
            if year==2025:
                if vals.get('x86_silicon_tam_usd_b') is not None or vals.get('nonx86_silicon_tam_usd_b') is not None:
                    problems.append('2025 actual architecture value must be null '+run['run_id'])
            else:
                if vals.get('x86_silicon_tam_usd_b') is None or vals.get('nonx86_silicon_tam_usd_b') is None:
                    problems.append('Missing modeled ISA allocation '+run['run_id']+' year '+str(year))
                elif vals['x86_silicon_tam_usd_b']+vals['nonx86_silicon_tam_usd_b'] != vals['total_cpu_silicon_tam_usd_b']:
                    problems.append('ISA subtotal mismatch '+run['run_id']+' year '+str(year))
    # Numeric year totals tracked by vintage, not collapsed to a single favorite forecast.
    # No orphan objects beyond intentional sources/claims/models/insights.
    for x in cnx.execute('SELECT measurement_id,value_decimal FROM measurements'):
        try: numeric(x['value_decimal'])
        except ValueError: problems.append('Invalid decimal measurement '+x['measurement_id'])
    for x in cnx.execute('SELECT forecast_id,value_decimal FROM forecasts'):
        try: numeric(x['value_decimal'])
        except ValueError: problems.append('Invalid decimal forecast '+x['forecast_id'])
    for c in cnx.execute('SELECT commitment_id,amount_decimal FROM financial_commitments WHERE amount_decimal IS NOT NULL'):
        try:
            if Decimal(numeric(c['amount_decimal'])) < 0:
                problems.append('Negative disclosed commitment '+c['commitment_id'])
        except ValueError:
            problems.append('Invalid financial commitment decimal '+c['commitment_id'])
    for x in cnx.execute("SELECT mapping_id,measurement_id,commitment_id FROM financial_model_mappings WHERE review_status='approved'"):
        if x['measurement_id'] is not None:
            st=cnx.execute('SELECT verification_status FROM measurements WHERE measurement_id=?',(x['measurement_id'],)).fetchone()
        else:
            st=cnx.execute('SELECT verification_status FROM financial_commitments WHERE commitment_id=?',(x['commitment_id'],)).fetchone()
        if st is None or st[0] in ('attributed_unverified','rejected','conflicted'):
            problems.append('Approved model mapping depends on unreviewed evidence '+x['mapping_id'])
    return problems


def counts(cnx):
    tables=['source_documents','source_locators','evidence_claims','measurements','forecasts','forecast_vintages','market_scopes','metric_definitions',
            'taxonomy_nodes','model_runs','model_outputs','partition_frames','research_questions','conflicts','ingestion_batches',
            'financial_issuers','financial_filings','financial_fact_contexts','financial_commitments','financial_model_mappings','financial_flow_links']
    return {t:cnx.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in tables}


def exports(cnx,target):
    # Safe static snapshot: every figure must display evidence type or synthetic scenario.
    def out(view):return [dict(row) for row in cnx.execute('SELECT * FROM '+view)]
    content={"version":"researchdb-v1","warning":"Read-only evidence snapshot. Source-backed and synthetic records are separate; no automatic verification or market summation.",
             "measurements":out('v_measurement_evidence'),"forecasts":out('v_forecast_history'),"synthetic_scenarios":out('v_synthetic_outputs'),
             "unresolved_conflicts":out('v_unresolved_conflicts'),
             "financial_facts":out('v_financial_fact_context'),"financial_commitments":out('v_financial_commitment_evidence')}
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return {k:len(v) for k,v in content.items() if isinstance(v,list)}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['init','seed','verify','stats','export','query','ingest-financial'])
    p.add_argument('--root',type=Path,default=DEFAULT_ROOT)
    p.add_argument('--db',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--input',type=Path,help='Public-only JSON filing intake; starts staged, never promoted')
    p.add_argument('--sql',type=str,help='Read-only SELECT or WITH statement for query command')
    args=p.parse_args(argv)
    root=args.root.resolve()
    db=(args.db or root/'db/runtime/research.sqlite').resolve()
    try:
        if args.command=='ingest-financial':
            if not args.input: raise ValueError('ingest-financial requires --input JSON path')
            print(json.dumps(ingest_financial(root,db,args.input),indent=2))
            print('FINANCIAL_STAGED_ONLY')
            return 0
        if args.command=='seed':
            summary=seed(root,db)
            print(json.dumps({'seed':summary,'database':str(db)},indent=2))
            c=open_db(db)
            problems=verify(c)
            c.close()
            if problems: raise ValueError('Seed consistency errors: '+str(problems))
            print('DB_VALIDATE_PASS')
            return 0
        cnx=open_db(db)
        if args.command=='init':init(root,cnx);print('DB_SCHEMA_INITIALIZED')
        elif args.command=='verify':
            problems=verify(cnx)
            print('DB_VALIDATE_FAIL: '+str(problems) if problems else 'DB_VALIDATE_PASS')
            if problems:return 2
        elif args.command=='stats':print(json.dumps(counts(cnx),indent=2))
        elif args.command=='export':print(json.dumps(exports(cnx,(args.output or root/'db/runtime/research_snapshot.json').resolve()),indent=2))
        elif args.command=='query':
            sql=(args.sql or '').strip()
            if not re.match(r'^(SELECT|WITH)\s',sql,re.IGNORECASE) or ';' in sql:
                raise ValueError('Only a single read-only SELECT or WITH query allowed')
            cnx.execute('PRAGMA query_only=ON')
            rows=[dict(row) for row in cnx.execute(sql)]
            print(json.dumps(rows,indent=2))
        cnx.close()
        return 0
    except (ValueError,sqlite3.Error,KeyError,FileNotFoundError) as exc:
        print('DB_ERROR: '+str(exc),file=sys.stderr)
        return 2


if __name__=='__main__':raise SystemExit(main())
