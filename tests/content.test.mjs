import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { sources, competitors, workloads, aiPaths, strategicQuestions } from '../data.js';

test('all research sources have unique IDs, valid HTTPS links, visible attribution',()=>{
  assert.equal(sources.length,10);
  assert.equal(new Set(sources.map(x=>x.id)).size,sources.length);
  sources.forEach(source=>{
    assert.ok(source.id && source.owner && source.title && source.date && source.trust && source.insight);
    assert.equal(new URL(source.url).protocol,'https:');
  });
});
test('interactive source references resolve',()=>{
  const known=new Set(sources.map(s=>s.id));
  competitors.flatMap(c=>c.sources).concat(strategicQuestions.map(q=>q.source)).forEach(id=>assert.ok(known.has(id),id));
  assert.equal(workloads.length,4);
  assert.equal(aiPaths.length,3);
});
test('published dashboard excludes user-provided expert-network screenshots',async()=>{
  const html=await readFile(new URL('../index.html',import.meta.url),'utf8');
  assert.ok(!html.includes('GLG'));
  assert.ok(!html.includes('consultation until'));
  assert.match(html,/HYPOTHETICAL/);
  assert.match(html,/EPYC 9006/);
  assert.match(html,/Xeon 6\+/);
});