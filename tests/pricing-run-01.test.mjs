import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {analyzePricingRun} from '../scripts/pricing/analyze-run-01.mjs';
const path=new URL('../data/pricing/run-01-2026-10-08/observations.json',import.meta.url);
const load=()=>JSON.parse(readFileSync(path,'utf8'));
test('Run 01: two OEM baseline invariance checks, one each AMD and Intel',()=>{
 const r=analyzePricingRun(load());
 assert.equal(r.oem_baseline_invariance.length,2);
 assert.deepEqual(r.oem_baseline_invariance.map(x=>x.server_model).sort(),['PowerEdge R770','PowerEdge R7725']);
 assert.ok(r.oem_baseline_invariance.every(x=>x.max_abs_residual_eur_cents===0));
 assert.ok(r.oem_baseline_invariance.every(x=>x.co_requisites_verified===false));
});
test('Run 01: reporting vintage disagreement survives; never silently rebase',()=>{
 const r=analyzePricingRun(load());
 assert.equal(r.reported_ASP_conflicts.length,1);
 assert.deepEqual(r.reported_ASP_conflicts[0].values.map(x=>x.value_percent).sort((a,b)=>a-b),[11,12]);
 assert.equal(r.reported_ASP_conflicts[0].status,'unresolved_source_vintage_conflict');
});
test('Run 01: only reference repricing; no buyer discount inferred',()=>{
 const r=analyzePricingRun(load());
 assert.deepEqual([r.reference_price_comparison.prior_usd,r.reference_price_comparison.current_web_usd],[14813,11988]);
 assert.equal(r.reference_price_comparison.difference_usd,-2825);
 assert.equal(r.unidentifiable.find(x=>x.id==='missing:actual-hyperscaler-net-asp').value,null);
 assert.equal('hyperscaler_discount' in r,false);
});
test('Run 01: reject invalid baseline and incompatible currency',()=>{
 const bad=load();
 bad.oem_quotes[1].options.find(x=>x.sku==='EPYC 9355').delta_eur_cents=123;
 assert.throws(()=>analyzePricingRun(bad),/Invalid OEM selected baseline/);
 const bad2=load();
 bad2.oem_quotes[1].currency='USD';
 assert.throws(()=>analyzePricingRun(bad2),/Incomparable OEM quotes/);
});
test('Run 01: reject large incorrectly derived option spreads',()=>{
 const bad=load();
 bad.oem_quotes[1].options.find(x=>x.sku==='EPYC 9555').delta_eur_cents+=500;
 assert.throws(()=>analyzePricingRun(bad),/baseline invariance failed/);
});
