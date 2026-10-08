import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const parse = file => JSON.parse(readFileSync(new URL(file, import.meta.url), 'utf8'));
const curated = parse('../data/claims/amd-advancing-ai-2026-curated.json');
const numeric = parse('../data/sources/amd-advancing-ai-2026-numeric-anchors.json');
const qualitative = parse('../data/claims/amd-advancing-ai-2026-strategic-signals.json');

test('complete transcript numeric-line anchor coverage snapshot', () => {
  assert.equal(numeric.original_line_count, 3189);
  assert.equal(numeric.numeric_bearing_lines, 196);
  assert.equal(numeric.anchors.length, 196);
  assert.equal(new Set(numeric.anchors.map(x => x.line)).size, numeric.anchors.length);
  for (const a of numeric.anchors) {
    assert.ok(a.line >= 1 && a.line <= numeric.original_line_count);
    assert.ok(a.numeric_tokens.length > 0);
    assert.match(a.source_locator, /^transcript:L\d+$/);
    assert.equal(a.review_status, 'untriaged');
  }
  assert.equal(numeric.index_policy.includes('not exhaustive'), true);
});

test('curated claims have traceable source line ranges, classifications and caveats', () => {
  assert.equal(curated.record_count, 97);
  assert.equal(curated.records.length, curated.record_count);
  assert.equal(new Set(curated.records.map(x => x.id)).size, curated.record_count);
  for (const x of curated.records) {
    assert.ok(x.source_lines[0] >= 1 && x.source_lines[1] <= 3189 && x.source_lines[0] <= x.source_lines[1]);
    assert.ok(x.metric && x.statement_class && x.caveat);
    assert.equal(x.verification_status, 'keynote_extracted');
    assert.ok(['P0','P1','P2'].includes(x.priority_for_follow_up));
  }
});

test('qualitative signals distinct from audited company facts', () => {
  assert.equal(qualitative.count, 38);
  assert.equal(qualitative.records.length, qualitative.count);
  assert.equal(new Set(qualitative.records.map(x => x.id)).size, qualitative.count);
  for (const x of qualitative.records) {
    assert.equal(x.is_factual_independent_confirmation, false);
    assert.ok(x.normalized_statement.length > 20);
    assert.match(x.source_line_range, /^L\d+-L\d+$/);
  }
});

test('high-priority uncertainties are explicitly retained in research path', () => {
  const text = readFileSync(new URL('../docs/research/AMD-ADVANCING-AI-2026-RESEARCH-PATH.md', import.meta.url), 'utf8');
  for (const needed of [
    '75 vs 72 Helios GPUs',
    '96-core CPU + >4,600',
    'agents per watt',
    'ROCm / x86',
    'Marg', // not required: keep explicit CPU margin section check instead
  ].slice(0, 4)) {
    assert.ok(text.includes(needed), `missing contradiction: ${needed}`);
  }
  assert.ok(text.includes('CPU-only margins'));
});
