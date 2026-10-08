import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = p => readFileSync(new URL(p, import.meta.url), 'utf8');
const json = p => JSON.parse(read(p));
const sources = json('../data/demand-2030/source-registry.json');
const model = json('../data/demand-2030/scenario-model.json');
const fields = json('../data/demand-2030/priority-data-fields.json');

function parseCsv(input) {
  const out = []; let cells = [], value = '', quote = false;
  for (let i = 0; i < input.length; ++i) {
    const c = input[i];
    if (c === '"') {
      if (quote && input[i + 1] === '"') { value += '"'; i++; }
      else quote = !quote;
    } else if (c === ',' && !quote) {
      cells.push(value); value = '';
    } else if ((c === '\n' || c === '\r') && !quote) {
      if (c === '\r' && input[i + 1] === '\n') i++;
      cells.push(value); value = '';
      if (cells.some(x => x !== '')) out.push(cells);
      cells = [];
    } else value += c;
  }
  if (value || cells.length) { cells.push(value); out.push(cells); }
  const [header, ...rows] = out;
  return rows.map((r, i) => {
    assert.equal(r.length, header.length, 'malformed CSV row ' + i);
    return Object.fromEntries(header.map((h, n) => [h, r[n]]));
  });
}
const actual = parseCsv(read('../data/demand-2030/historical-and-forecast-evidence.csv'));
const vintages = parseCsv(read('../data/demand-2030/tam-forecast-vintages.csv'));
const close = (a, b, tol=0.002) => assert.ok(Math.abs(a - b) <= tol, a + ' != ' + b);
const unique = rows => assert.equal(new Set(rows).size, rows.length);

test('registry and claim rows are traceable and unique', () => {
  assert.ok(sources.sources.length >= 30);
  unique(sources.sources.map(x => x.id));
  assert.ok(sources.sources.every(x => /^https:\/\//.test(x.url)));
  const refs = new Set(sources.sources.map(x => x.id));
  assert.equal(actual.length, 41);
  unique(actual.map(x => x.id));
  for (const row of actual) {
    assert.ok(refs.has(row.source_id), 'unknown observation source ' + row.source_id);
    assert.ok(row.measurement_basis && row.evidence_status && row.caution);
    assert.ok(Number.isFinite(Number(row.value)));
  }
  assert.equal(vintages.length, 9);
  unique(vintages.map(x => x.id));
  for (const r of vintages) assert.ok(refs.has(r.source_id), 'unknown TAM source ' + r.source_id);
  assert.ok(vintages.some(r => r.source_id === 'CITI_OCT2026' && r.evidence_type === 'analyst_forecast'));
});

test('IDC full-server system mix reconciles, but remains separate from CPU silicon', () => {
  const get = (year, segment) => Number(actual.find(x => x.period === String(year) && x.metric === 'server_system_spending' && x.segment === segment).value);
  for (const y of [2025, 2026, 2027]) {
    const total = get(y, 'world_all_server_systems');
    const sum = get(y, 'x86_server_systems') + get(y, 'non_x86_server_systems');
    close(total, sum);
  }
  assert.ok(actual.filter(x => x.metric === 'server_system_spending').every(x => x.measurement_basis === 'system_revenue'));
});

test('three model scenarios reconcile workload total and ISA share, with no fake 2025 architecture values', () => {
  assert.equal(model.status, 'synthetic_analyst_sensitivity_scenarios_not_predictions');
  const s = model.year_rows;
  for (const name of ['downside', 'central', 'upside']) {
    assert.equal(s[name].length, 6);
    assert.deepEqual(s[name].map(x => x.year), [2025, 2026, 2027, 2028, 2029, 2030]);
    for (const row of s[name]) {
      close(row.total_cpu_silicon_tam_usd_b, row.foundational_usd_b + row.ai_host_usd_b + row.agent_execution_usd_b, 0.00001);
      assert.ok(row.foundational_usd_b >= 0 && row.ai_host_usd_b >= 0 && row.agent_execution_usd_b >= 0);
      if (row.year === 2025) {
        assert.equal(row.x86_silicon_tam_usd_b, null);
        assert.equal(row.nonx86_silicon_tam_usd_b, null);
        assert.equal(row.total_cpu_silicon_tam_usd_b, 25);
      } else {
        close(row.x86_silicon_tam_usd_b + row.nonx86_silicon_tam_usd_b, row.total_cpu_silicon_tam_usd_b);
        assert.ok(row.measurement_type.startsWith('synthetic'));
      }
    }
  }
  assert.equal(s.central.at(-1).total_cpu_silicon_tam_usd_b, 200);
  assert.ok(s.downside.at(-1).total_cpu_silicon_tam_usd_b < 200);
  assert.ok(s.upside.at(-1).total_cpu_silicon_tam_usd_b > 200);
});

test('demand acquisition backlog has 50 unique definitions and explicit scope', () => {
  assert.equal(fields.fields.length, 50);
  unique(fields.fields.map(f => f.id));
  for (const f of fields.fields) {
    assert.ok(f.metric && f.unit && f.granularity && f.denominator);
    assert.ok(f.source_hint && f.validation && f.dashboard_view);
  }
});
