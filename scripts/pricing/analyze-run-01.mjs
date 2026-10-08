// Pricing pilot analysis: all output is derived from public, typed, STAGED observations.
// Never infer negotiated chip ASP or discount from public OEM/reference quotes.
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const DEFAULT_DATA=fileURLToPath(new URL('../../data/pricing/run-01-2026-10-08/observations.json',import.meta.url));
const ensure=(ok,message)=>{if(!ok)throw new Error(message);};
export function analyzePricingRun(input) {
  ensure(input.schema_version==='1.0' && input.run_id==='pricing-observatory-run-01','Wrong pilot schema/run');
  const ids=new Set(),sources=new Set(input.source_registry.map(x=>x.id));
  for(const group of ['reported_asp','reference_prices','oem_quotes']){
    ensure(Array.isArray(input[group]),'Missing '+group);
    for(const record of input[group]){
      ensure(!ids.has(record.id),'Duplicate record '+record.id);ids.add(record.id);
      ensure(sources.has(record.source_id),'Orphan source '+record.id);
    }
  }
  for(const r of input.reference_prices){
    ensure(r.price_layer==='published_reference' && Number.isFinite(r.price_usd) && r.price_usd>0,'Bad reference anchor '+r.id);
    ensure(r.quantity_basis==='1000_unit_list_reference'||r.quantity_basis==='Intel_RCP_not_formal_offer','Unknown price basis');
  }
  const disagreements=[];
  const aspByPeriod=new Map();
  for(const r of input.reported_asp){
    ensure(r.price_layer==='reported_aggregate_ASP_change' && Number.isFinite(r.value_percent),'Bad ASP metric');
    const k=r.metric+'|'+r.period;
    const bucket=aspByPeriod.get(k)||[];bucket.push(r);aspByPeriod.set(k,bucket);
  }
  for(const [key,rows] of aspByPeriod)if(new Set(rows.map(r=>r.value_percent)).size>1)
    disagreements.push({metric_period:key,values:rows.map(r=>({source_id:r.source_id,vintage:r.report_vintage,value_percent:r.value_percent})),status:'unresolved_source_vintage_conflict'});
  const oemChecks=[];
  for(let i=0;i<input.oem_quotes.length;i++)for(let j=i+1;j<input.oem_quotes.length;j++){
    const a=input.oem_quotes[i],b=input.oem_quotes[j];
    if(a.brand!==b.brand||a.vendor!==b.vendor||a.server_model!==b.server_model)continue;
    ensure(a.currency===b.currency && a.region===b.region && a.tax_treatment===b.tax_treatment,'Incomparable OEM quotes');
    for(const q of [a,b]){
      ensure(q.price_layer==='oem_configurator_cpu_option_delta','Wrong OEM price layer');
      const selected=q.options.find(o=>o.sku===q.baseline_sku);
      ensure(selected && selected.delta_eur_cents===0,'Invalid OEM selected baseline: '+q.id);
      ensure(new Set(q.options.map(o=>o.sku)).size===q.options.length,'Repeated SKU in quote '+q.id);
    }
    const oa=new Map(a.options.filter(o=>o.delta_eur_cents!==null).map(o=>[o.sku,o.delta_eur_cents]));
    const ob=new Map(b.options.filter(o=>o.delta_eur_cents!==null).map(o=>[o.sku,o.delta_eur_cents]));
    const common=[...oa.keys()].filter(k=>ob.has(k)).sort();
    const ref=a.baseline_sku;
    ensure(ob.has(ref),'Reference SKU absent from second baseline');
    const residuals=common.map(sku=>({sku,residual_eur_cents:(oa.get(sku)-oa.get(ref))-(ob.get(sku)-ob.get(ref))}));
    const max=Math.max(...residuals.map(x=>Math.abs(x.residual_eur_cents)));
    ensure(max<=1,'OEM option baseline invariance failed: '+a.id+'/'+b.id+' residual cents '+max);
    oemChecks.push({server_model:a.server_model,first_quote:a.id,second_quote:b.id,matched_skus:common.length,
      reference_sku:ref,reference_option_gap_eur:Number(((oa.get(b.baseline_sku)-oa.get(ref))/100).toFixed(2)),
      max_abs_residual_eur_cents:max,status:'relative_option_spreads_consistent_NOT_semiconductor_invoice',
      co_requisites_verified:false});
  }
  ensure(oemChecks.length>=2,'Need AMD+Intel independent baseline checks');
  const amd=input.reference_prices.filter(r=>r.sku==='EPYC 9965');
  ensure(amd.length===2 && new Set(amd.map(r=>r.validity)).size===2,'Missing historical/current 9965 anchors');
  const prior=amd.find(r=>r.validity.includes('published launch'));
  const current=amd.find(r=>r.validity.includes('web_current'));
  ensure(prior&&current,'AMD anchor vintages unclear');
  const anchor={
    sku:'EPYC 9965',prior_usd:prior.price_usd,current_web_usd:current.price_usd,
    difference_usd:current.price_usd-prior.price_usd,
    reference_delta_percent:Number(((current.price_usd/prior.price_usd-1)*100).toFixed(2)),
    interpretation:'descriptive_price_reference_change_only_not_dated_market_index',
    historical_source_id:prior.source_id,current_source_id:current.source_id
  };
  const unknowns=input.unobservables.map(u=>{ensure(u.value===null && u.reason,'Do not impute unidentifiable field '+u.id);return {id:u.id,value:null,reason:u.reason};});
  return {run_id:input.run_id,as_of:input.as_of,status:'staged_nontransactional',
    counts:{sources:input.source_registry.length,reported_asp_vintages:input.reported_asp.length,
      reference_price_anchors:input.reference_prices.length,OEM_quote_configs:input.oem_quotes.length},
    reported_ASP_conflicts:disagreements,reference_price_comparison:anchor,
    oem_baseline_invariance:oemChecks,unidentifiable:unknowns,
    restrictions:['NEVER infer hyperscaler discounts from list or OEM upgrade prices',
      'DCAI revenue and AMD Data Center revenue are NOT CPU-only net revenue',
      'OEM option delta does NOT equal OEM CPU procurement price',
      'Published current-page prices are not an archived historical matched-SKU index',
      'No historical SKU index or buyer-class ASP is estimated by this pilot']};
}
if(process.argv[1] && fileURLToPath(import.meta.url)===process.argv[1]){
  const data=JSON.parse(readFileSync(process.argv[2]||DEFAULT_DATA,'utf8'));
  process.stdout.write(JSON.stringify(analyzePricingRun(data),null,2)+'\n');
}
