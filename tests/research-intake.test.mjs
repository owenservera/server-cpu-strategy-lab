import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { validateResearch, validateCatalog, validatePacket, repoRoot } from '../scripts/validate-research.mjs';

const json=p=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const catalog=json('../research/catalog.json');
const routes=json('../research/routes.json');
const template=json('../research/templates/packet.example.json');
const clone=x=>structuredClone(x);

test('research entry and catalog refer to existing, uniquely routed domains',()=>{
  const result=validateResearch();
  assert.deepEqual(result.errors,[],result.errors.join('\n'));
  assert.ok(result.domain_count>=6);
  assert.ok(result.route_count>=19);
  assert.deepEqual(validateCatalog(catalog,routes),[]);
});

test('sample multi-route packet is staged, linked to legacy facts and never promoted',()=>{
  assert.equal(template.sample_only,true);
  assert.ok(template.domains.length>=2);
  assert.ok(template.routes.length>=5);
  assert.equal(template.public_only,true);
  assert.ok(template.search_before_write.prior_ids.length>=2);
  assert.ok(template.promotions.every(x=>x.review_status==='not_applicable'));
  assert.deepEqual(validatePacket(template,catalog,routes),[]);
});

test('packet validator detects denominator loss, unsourced claim, invented routes and policy breach',()=>{
  const wrong=clone(template);
  wrong.routes.push('not_a_real_route');
  wrong.sources[0].access='restricted_unpublishable';
  wrong.forecasts[0].source_id='invented';
  wrong.measurements=[{id:'metric:broken',source_id:'invented',metric_id:'server_cpu_tam',value:null,unit:'USD',period:'2030',population:'global',denominator:'',measurement_kind:'observed',verification:'verified'}];
  wrong.routes.push('measurement');
  const errors=validatePacket(wrong,catalog,routes);
  assert.ok(errors.some(x=>x.includes('Unknown research route')));
  assert.ok(errors.some(x=>x.includes('Restricted source')));
  assert.ok(errors.some(x=>x.includes('nonexistent packet source')));
  assert.ok(errors.some(x=>x.includes('denominator')));
  assert.ok(errors.some(x=>x.includes('Null measurement missing reason')));
});

test('routing helper finds existing ROCm and server demand modules without network access',()=>{
  const out=execFileSync(process.execPath,['scripts/research-route.mjs','AMD ROCm x86','--json'],{cwd:repoRoot,encoding:'utf8'});
  const d=JSON.parse(out);
  assert.ok(d.matching_domains.some(x=>x.id==='architecture-and-software'));
  assert.equal(d.schema,'research/schema/packet.schema.json');
});
