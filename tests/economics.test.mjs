import test from 'node:test';
import assert from 'node:assert/strict';
import { computeEnergyScenario } from '../economics.js';

test('baseline formula includes full-year hours, PUE and average IT power', () => {
  const result = computeEnergyScenario({ servers: 1, watts: 1000, rate: 0.1, pue: 1.5, improvement: 20 });
  assert.equal(result.annualKwh, 13140);
  assert.equal(result.base, 1314);
  assert.equal(result.savings, 262.8);
  assert.equal(result.percentRemaining, 80);
  assert.ok(Math.abs(result.scenario - 1051.2) < 1e-10);
});
test('zero efficiency gain cannot create savings', () => {
  const result = computeEnergyScenario({servers:500,watts:300,rate:.2,pue:1.2,improvement:0});
  assert.equal(result.savings,0);
  assert.equal(result.base,result.scenario);
});
test('invalid input is rejected', () => {
  assert.throws(()=>computeEnergyScenario({servers:10,watts:500,rate:0.2,pue:0.8,improvement:20}),RangeError);
  assert.throws(()=>computeEnergyScenario({servers:10,watts:500,rate:0.2,pue:1.2,improvement:120}),RangeError);
});