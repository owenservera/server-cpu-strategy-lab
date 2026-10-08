// Discover relevant existing research without asking a model to guess repo paths.
// Heuristic suggestions only: agents must read the routing contract and inspect prior evidence.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const catalog=JSON.parse(readFileSync(resolve(root,'research/catalog.json'),'utf8'));
const routeData=JSON.parse(readFileSync(resolve(root,'research/routes.json'),'utf8'));
const args=process.argv.slice(2);
const json=args.includes('--json');
const query=args.filter(x=>x!=='--json').join(' ').trim();
if(!query) {
  process.stderr.write('Usage: npm run research:route -- "AMD ROCm on x86 CPU" [--json]\n');
  process.exitCode=2;
} else {
  const q=query.toLowerCase();
  const tokens=q.split(/[^a-z0-9]+/).filter(Boolean);
  const scored=catalog.domains.map(domain=>{
    const matched=[];
    for(const key of domain.topic_keys || []) {
      const k=key.toLowerCase();
      const isPhrase=k.includes(' ')||k.includes('/')||k.includes('-');
      if(isPhrase?q.includes(k):tokens.includes(k)) matched.push(key);
    }
    return {
      id:domain.id, name:domain.name, matched,
      score:matched.reduce((n,key)=>n+Math.max(1,key.length/6),0),
      docs:domain.canonical_docs, datasets:domain.datasets,
      questions:domain.questions,
      recommended_routes:domain.routes
    };
  }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score);
  const result={
    topic:query,
    warning:'Heuristic discovery, not an AI classifier. Inspect catalog, repo tree and all semantically relevant domains; do not use scores to omit cross-domain routes.',
    matching_domains:scored,
    route_index:'research/routes.json',
    agent_protocol:'RESEARCH-ENTRY.md',
    schema:'research/schema/packet.schema.json',
    available_routes:routeData.route_ids
  };
  if(json) process.stdout.write(JSON.stringify(result,null,2)+'\n');
  else {
    process.stdout.write('Topic: '+query+'\n'+result.warning+'\n');
    if(!scored.length) process.stdout.write('No keyword matches. Read research/catalog.json and routes.json before creating a new domain.\n');
    for(const d of scored) process.stdout.write('\n'+d.id+' ('+d.matched.join(', ')+')\n Docs: '+d.docs.join(', ')+'\n Suggested routes: '+d.recommended_routes.join(', ')+'\n');
  }
}