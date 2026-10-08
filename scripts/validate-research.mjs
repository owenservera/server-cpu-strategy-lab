// Research validation: dependency-free structural + cross-reference checks.
// JSON Schema remains the normative contract; this script enforces critical repo invariants.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('..', import.meta.url));
export const repoRoot = resolve(here);
const readJSON = (path, root=repoRoot) => JSON.parse(readFileSync(resolve(root, path), 'utf8'));
const isString = x => typeof x === 'string' && x.trim().length > 0;
const collections = ['sources','claims','measurements','forecasts','scenarios','entities','relationships','events','signals','hypotheses','questions','conflicts','methods','requirements','promotions'];
const routeToCollection = {
  source:'sources', claim:'claims', measurement:'measurements',
  market_series:'measurements', technical_spec:'claims', benchmark:'measurements',
  forecast:'forecasts', scenario:'scenarios', entity:'entities',
  relationship:'relationships', company_event:'events', buyer_demand:'relationships',
  strategic_signal:'signals', milestone:'events', hypothesis:'hypotheses',
  question:'questions', conflict:'conflicts', method:'methods',
  product_requirement:'requirements'
};
const dateOk = x => /^\d{4}-\d{2}-\d{2}$/.test(x||'') && !Number.isNaN(Date.parse(x));
const hasDuplicate = arr => new Set(arr).size !== arr.length;

export function validateCatalog(catalog, routes, root=repoRoot) {
  const errors = [];
  if (!catalog || !Array.isArray(catalog.domains)) return ['catalog.domains must be an array'];
  if (!routes || !Array.isArray(routes.routes)) return ['routes.routes must be an array'];
  const domainIds = catalog.domains.map(d=>d.id);
  const routeIds = routes.routes.map(d=>d.id);
  if (hasDuplicate(domainIds)) errors.push('Duplicate catalog domain IDs');
  if (hasDuplicate(routeIds)) errors.push('Duplicate research route IDs');
  for (const route of routes.routes) {
    if (!routeToCollection[route.id]) errors.push('Unknown route-to-packet mapping: '+route.id);
    if (!isString(route.description) || !isString(route.canonical_destination)) errors.push('Unusable route: '+route.id);
    if (route.packet_collection !== routeToCollection[route.id]) errors.push('Route mapping mismatch: '+route.id);
  }
  for (const domain of catalog.domains) {
    if (!isString(domain.id) || !isString(domain.name)) errors.push('Domain missing ID/name');
    if (!Array.isArray(domain.questions) || !domain.questions.length) errors.push('Domain has no research questions: '+domain.id);
    for (const id of domain.related || []) if (!domainIds.includes(id)) errors.push('Unknown related domain '+id+' in '+domain.id);
    for (const id of domain.routes || []) if (!routeIds.includes(id)) errors.push('Unknown route '+id+' in '+domain.id);
    for (const path of [...(domain.canonical_docs||[]),...(domain.datasets||[])]) {
      if (!existsSync(resolve(root,path))) errors.push('Missing catalog path '+path+' in '+domain.id);
    }
  }
  for (const path of catalog.global_protections || []) if(!existsSync(resolve(root,path))) errors.push('Missing global protection '+path);
  return errors;
}

export function validatePacket(packet, catalog, routes, {root=repoRoot, actualPath, allowSample=true}={}) {
  const errors = [];
  const add = message=>errors.push((packet?.packet_id||'packet')+': '+message);
  if (!packet || typeof packet !== 'object') return ['Packet must be an object'];
  if (packet.schema_version !== '1.0') add('Unexpected schema_version');
  if (!/^\d{4}-\d{2}-\d{2}--[a-z0-9][a-z0-9-]*$/.test(packet.packet_id||'')) add('packet_id format YYYY-MM-DD--slug required');
  if (!dateOk(packet.created_at)) add('Invalid created_at');
  if (!isString(packet.title)) add('Missing title');
  if (packet.public_only !== true) add('public_only must be true');
  if (!['staged','needs_review','partially_promoted','promoted','archived'].includes(packet.status)) add('Invalid status');
  if (packet.sample_only && !allowSample) add('Samples cannot be ingested as live packets');
  if (packet.sample_only && packet.status !== 'staged') add('Sample must remain staged');
  if (actualPath && !packet.sample_only) {
    const expected=packet.packet_id+'.json';
    if (actualPath.split(/[\\/]/).at(-1)!==expected) add('Live packet filename must match packet_id');
  }
  const domainIds = new Set(catalog.domains.map(x=>x.id)), routeIds = new Set(routes.routes.map(x=>x.id));
  if (!Array.isArray(packet.domains) || !packet.domains.length) add('No domains classified');
  for (const id of packet.domains||[]) if (!domainIds.has(id)) add('Unknown research domain '+id);
  if (!Array.isArray(packet.routes) || !packet.routes.length) add('No routes classified');
  for (const id of packet.routes||[]) if (!routeIds.has(id)) add('Unknown research route '+id);
  if (hasDuplicate(packet.domains||[])) add('Duplicate domains');
  if (hasDuplicate(packet.routes||[])) add('Duplicate routes');
  const lookup = new Map();
  for (const group of collections) {
    if (!Array.isArray(packet[group]||[])) {add(group+' must be an array');continue;}
    for (const record of packet[group]||[]) {
      if (!isString(record?.id||record?.record_id)) {add(group+' entry lacks id or record_id');continue;}
      if (group==='promotions') continue;
      if (lookup.has(record.id)) add('Duplicate record ID '+record.id);
      lookup.set(record.id,{group,record});
    }
  }
  // Presence checks: a route describes a real output, not just a keyword.
  for (const id of packet.routes||[]) {
    const group=routeToCollection[id];
    if (group && !(packet[group]||[]).length) add('Declared route '+id+' has no '+group+' records');
  }
  const sourceIds=new Set((packet.sources||[]).map(s=>s.id));
  const seenSourceKeys=new Set();
  for (const s of packet.sources||[]) {
    if (!isString(s.title)||!isString(s.publisher)||!isString(s.kind)||!isString(s.url)||!dateOk(s.published_at)) add('Incomplete source '+s.id);
    if (!/^https:\/\//i.test(s.url)) add('Source URL must be public HTTPS: '+s.id);
    if (s.access==='restricted_unpublishable') add('Restricted source cannot be committed in public packet: '+s.id);
    if (!['public','public_secondary','public_paywalled','licensed_unavailable'].includes(s.access)) add('Missing/invalid public access status: '+s.id);
    if (!['link_and_extract','quote_with_limits','publish_licensed','unknown_do_not_copy'].includes(s.rights)) add('Missing source rights status: '+s.id);
    const key=(s.url||'').replace(/\/$/,'').toLowerCase()+'|'+s.published_at+'|'+(s.version||'');
    if (seenSourceKeys.has(key)) add('Repeated identical source version in packet: '+s.id);
    seenSourceKeys.add(key);
  }
  for (const group of ['claims','measurements','forecasts']) for (const r of packet[group]||[]) {
    if (!sourceIds.has(r.source_id)) add(group+' '+r.id+' references nonexistent packet source '+r.source_id);
  }
  for (const c of packet.claims||[]) {
    if (!isString(c.statement)||!isString(c.claim_class)||!isString(c.verification)||!isString(c.source_locator)) add('Claim missing evidence fields: '+c.id);
    if (!['attributed_unverified','checked_against_original','independently_corroborated','conflicted','rejected'].includes(c.verification)) add('Invalid claim verification: '+c.id);
  }
  for (const m of packet.measurements||[]) {
    for (const key of ['metric_id','unit','period','population','denominator','measurement_kind','verification']) if (!isString(m[key])) add('Measurement '+m.id+' lacks '+key);
    if (m.value!==null && (typeof m.value!=='number'||!Number.isFinite(m.value))) add('Measurement '+m.id+' value not finite number or null');
    if (m.value===null && !isString(m.missing_reason)) add('Null measurement missing reason: '+m.id);
    if (m.measurement_kind==='modeled' && !Array.isArray(packet.scenarios)) add('Modeled measurement lacks scenario context: '+m.id);
  }
  for (const f of packet.forecasts||[]) {
    for(const key of ['issuer','issued_at','target_period','metric_id','market_scope','unit','qualifier']) if(!isString(f[key])) add('Forecast '+f.id+' lacks '+key);
    if (!dateOk(f.issued_at)) add('Forecast '+f.id+' has invalid issued_at');
    if(f.value!==null && (typeof f.value!=='number'||!Number.isFinite(f.value))) add('Forecast '+f.id+' invalid value');
    if(!['equal','approximately','greater_than','less_than','range_low','range_high'].includes(f.qualifier)) add('Forecast '+f.id+' missing standardized qualifier');
    if(f.claim_id && !lookup.has(f.claim_id) && !isString(f.legacy_ref)) add('Forecast '+f.id+' has missing claim_id '+f.claim_id);
  }
  for(const h of packet.hypotheses||[]) {
    if(!isString(h.thesis)||!isString(h.alternative)||!isString(h.falsification_test)||!Array.isArray(h.evidence_ids)) add('Hypothesis incomplete '+h.id);
  }
  for(const c of packet.conflicts||[]) {
    if(!isString(c.left_ref)||!isString(c.right_ref)||!isString(c.issue)||!isString(c.resolution_plan)) add('Conflict incomplete '+c.id);
    if(!['open','resolved','not_comparable','superseded_vintage'].includes(c.status)) add('Invalid conflict status '+c.id);
  }
  for(const q of packet.questions||[]) {
    if(!isString(q.question)||!isString(q.method)||!['P0','P1','P2'].includes(q.priority)) add('Question incomplete '+q.id);
    for(const id of q.domains||[]) if(!domainIds.has(id)) add('Unknown question domain '+id);
  }
  for(const p of packet.promotions||[]) {
    if(!isString(p.record_id)||!isString(p.target_path)||!isString(p.decision_note)||!['pending','approved','rejected','not_applicable','promoted'].includes(p.review_status)) add('Incomplete promotion decision: '+p.record_id);
    if(!lookup.has(p.record_id)) add('Promotion points to missing record '+p.record_id);
    if((p.review_status==='promoted'||p.review_status==='approved')&&!existsSync(resolve(root,p.target_path))) add('Approved promotion target missing '+p.target_path);
    if(packet.sample_only && ['approved','promoted'].includes(p.review_status)) add('Sample packet cannot promote records');
  }
  const s=packet.search_before_write;
  if(!s || !Array.isArray(s.checked_paths)||!s.checked_paths.length||!isString(s.dedupe_notes)) add('Search-before-write evidence required');
  for(const path of s?.checked_paths||[]) if(!existsSync(resolve(root,path))) add('Checked path does not exist: '+path);
  if((packet.sources||[]).length===0 && (packet.claims||[]).length>0) add('Claims without any public sources');
  return errors;
}

function walkPackets(folder) {
  if(!existsSync(folder)) return [];
  const found=[];
  for(const e of readdirSync(folder)) {
    const p=join(folder,e);
    if(statSync(p).isDirectory()) found.push(...walkPackets(p));
    else if(e.endsWith('.json')) found.push(p);
  }
  return found;
}
export function validateResearch(root=repoRoot) {
  const catalog=readJSON('research/catalog.json',root);
  const routes=readJSON('research/routes.json',root);
  const schema=readJSON('research/schema/packet.schema.json',root);
  const errs=validateCatalog(catalog,routes,root);
  if(schema.properties?.schema_version?.const!=='1.0') errs.push('Packet schema_version changed without migration');
  const template='research/templates/packet.example.json';
  const sample=readJSON(template,root);
  errs.push(...validatePacket(sample,catalog,routes,{root,actualPath:template}));
  const packets=walkPackets(resolve(root,'research/packets'));
  const seenIds=new Set();
  for(const path of packets) {
    const relativePath=relative(root,path);
    const pkt=JSON.parse(readFileSync(path,'utf8'));
    if(seenIds.has(pkt.packet_id)) errs.push('Duplicate packet_id '+pkt.packet_id);
    seenIds.add(pkt.packet_id);
    errs.push(...validatePacket(pkt,catalog,routes,{root,actualPath:relativePath,allowSample:false}));
  }
  return {errors:errs,domain_count:catalog.domains.length,route_count:routes.routes.length,live_packet_count:packets.length,validated_template:template};
}

if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {
    const status=validateResearch();
    if(status.errors.length) {
      process.stderr.write('Research validation FAIL:\n'+status.errors.map(x=>' - '+x).join('\n')+'\n');
      process.exitCode=1;
    } else {
      process.stdout.write('Research validation PASS: '+status.domain_count+' domains, '+status.route_count+' routes, '+status.live_packet_count+' live packets + template.\n');
    }
  } catch(e) {
    process.stderr.write('Research validation FAIL: '+e.stack+'\n');
    process.exitCode=1;
  }
}