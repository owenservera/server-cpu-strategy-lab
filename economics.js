/**
 * Pure, illustrative fleet electricity model.
 * watts = average IT equipment power per server; PUE adds facility overhead.
 * The model intentionally excludes all non-electricity TCO components.
 */
export function computeEnergyScenario({servers,watts,rate,pue,improvement}) {
  if (![servers,watts,rate,pue,improvement].every(Number.isFinite)) throw new RangeError('All assumptions must be finite numbers');
  if (servers < 0 || watts < 0 || rate < 0 || pue < 1 || improvement < 0 || improvement > 100) throw new RangeError('Invalid fleet energy assumptions');
  const annualKwh = servers * watts / 1000 * 8760 * pue;
  const base = annualKwh * rate;
  const fraction = improvement / 100;
  return { annualKwh, base, scenario: base * (1 - fraction), savings: base * fraction, percentRemaining: 100 - improvement };
}