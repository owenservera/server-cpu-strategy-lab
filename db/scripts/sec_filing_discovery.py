#!/usr/bin/env python3
"""Discover public SEC filing metadata for a watchlisted issuer (no filing body copies).
Requires SEC_USER_AGENT='Project Name contact@example.com'.
Example: python db/scripts/sec_filing_discovery.py --issuer-id fin:amd --from-year 2019
Then: python db/scripts/research_db.py ingest-financial --input db/runtime/sec-fin-amd.json
All rows remain INDEXED, not facts; no market data is automatically promoted.
"""
import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
WATCHLIST = ROOT/'data/financial-filings/issuer-watchlist.json'
SEC_BASE = 'https://data.sec.gov'
TICKERS = 'https://www.sec.gov/files/company_tickers.json'
DEFAULT_FORMS = '10-K,10-K/A,10-Q,10-Q/A,20-F,20-F/A,40-F,8-K,6-K,F-1,S-1'


def get_json(url, user_agent):
    req=Request(url,headers={'User-Agent':user_agent,'Accept':'application/json'})
    with urlopen(req,timeout=30) as res:
        return json.load(res)


def resolve_cik(symbol, user_agent):
    values = get_json(TICKERS,user_agent)
    matches = [row for row in values.values() if row.get('ticker','').upper()==symbol.upper()]
    if len(matches)!=1:
        raise ValueError(f'SEC ticker lookup ambiguous or absent for {symbol}; supply --cik')
    return str(matches[0]['cik_str']).zfill(10)


def filings_from_page(page, cik, issuer_id, name, forms, from_year):
    rows=page.get('filings',{}).get('recent',page)
    accession=rows.get('accessionNumber',[])
    entries=[]
    for i,number in enumerate(accession):
        def pick(key, default=''):
            values=rows.get(key,[])
            return values[i] if i<len(values) else default
        form=pick('form')
        filed=pick('filingDate')
        if form not in forms or not filed or int(filed[:4])<from_year:
            continue
        primary=pick('primaryDocument')
        if not primary or '/' in primary or '\\' in primary or primary.startswith('.'):
            continue
        accession_compact=number.replace('-','')
        url=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_compact}/{quote(primary)}'
        report_date=pick('reportDate')
        item={
          'id':f'finfil:sec:{cik}:{accession_compact}',
          'source_id':f'sec:{cik}:{accession_compact}',
          'issuer_id':issuer_id,
          'title':f'{name} {form} filed {filed}',
          'url':url,
          'regulator':'SEC',
          'filing_type':form,
          'accession_or_document_id':number,
          'filed_at':filed,
          'source_version':primary
        }
        if report_date:
            item['period_end']=report_date
        accepted=pick('acceptanceDateTime')
        if accepted:
            item['accepted_at']=accepted
        entries.append(item)
    return entries


def discover(issuer_id, cik, name, forms, from_year, user_agent):
    payload=get_json(f'{SEC_BASE}/submissions/CIK{cik}.json',user_agent)
    found=filings_from_page(payload,cik,issuer_id,name,forms,from_year)
    for older in payload.get('filings',{}).get('files',[]):
        # SEC gives a year range; only load files with plausible overlap.
        if int(str(older.get('filingTo','9999'))[:4]) < from_year:
            continue
        time.sleep(0.2)  # deliberately conservative (<=5 metadata requests/sec).
        page=get_json(f"{SEC_BASE}/submissions/{older['name']}",user_agent)
        found.extend(filings_from_page(page,cik,issuer_id,name,forms,from_year))
    unique={f['id']:f for f in found}
    return [unique[k] for k in sorted(unique, key=lambda k:(unique[k]['filed_at'],k))]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--issuer-id',required=True)
    p.add_argument('--cik',help='SEC CIK; otherwise resolve watchlist ticker using official SEC data')
    p.add_argument('--from-year',type=int,default=2019)
    p.add_argument('--forms',default=DEFAULT_FORMS)
    p.add_argument('--output',type=Path)
    p.add_argument('--user-agent',default=os.environ.get('SEC_USER_AGENT'))
    args=p.parse_args()
    if not args.user_agent or '@' not in args.user_agent:
        p.error('SEC requires an identifying user agent. Set SEC_USER_AGENT to project and contact email.')
    data=json.loads(WATCHLIST.read_text(encoding='utf-8'))
    issuer=next((x for x in data['issuers'] if x['id']==args.issuer_id),None)
    if not issuer:
        p.error('Unknown issuer ID in watchlist: '+args.issuer_id)
    if 'SEC' not in issuer['regulator'].split(';'):
        p.error('Issuer is not marked SEC; use its own national filing authority')
    cik=str(args.cik).zfill(10) if args.cik else resolve_cik(issuer['symbol'],args.user_agent)
    if not cik.isdigit() or len(cik)!=10:
        p.error('CIK must contain ten digits after zero padding')
    forms=set(x.strip() for x in args.forms.split(',') if x.strip())
    filings=discover(args.issuer_id,cik,issuer['name'],forms,args.from_year,args.user_agent)
    out=args.output or ROOT/'db/runtime'/f"sec-{args.issuer_id.replace(':','-')}.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        'schema_version':'1.0','public_only':True,
        'discovery':'SEC EDGAR submissions API metadata, not parsed facts',
        'retrieved_at':datetime.now(timezone.utc).isoformat(),
        'issuer_id':args.issuer_id,'cik':cik,
        'filings':filings
    },indent=2)+'\n',encoding='utf-8')
    print(f'Indexed {len(filings)} public SEC filing links to {out} (no numeric facts promoted)')


if __name__=='__main__':
    main()
