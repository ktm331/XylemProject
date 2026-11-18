const assert = require('node:assert/strict');
const pricing = require('../app/project-pricing.js');
const systems = require('../app/data/systems.json');
const opt = require('../app/optimizer.js');
const robbins = systems.find(s => s.id === 'CA5100107');
assert.equal(pricing.verified(robbins).cost, 8000000);
assert.equal(pricing.verified({...robbins, name: 'Unrelated system'}), null);
assert.equal(systems.filter(s => pricing.verified(s)).length, 1);
assert.equal(pricing.estimate(robbins, ['centralized']).cost, 1171194);
assert.equal(pricing.estimate(robbins, ['centralized', 'consolidation']), null);
assert.equal(pricing.estimate({...robbins, failing: false}, ['centralized']), null);
assert.equal(pricing.estimate({...robbins, name: 'Example Elementary School'}, ['well']), null);
assert.equal(pricing.estimate({...robbins, conn: 0}, ['well']), null);
assert.equal(pricing.estimate(robbins, ['well', 'well']).cost, pricing.estimate(robbins, ['well']).cost);
assert.equal(pricing.estimate(robbins, ['centralized', 'oei']).cost, 2344563);
const costs = systems.map(s => pricing.verified(s)?.cost || s.cost);
// Prove the optimizer consumes the corrected budget and obeys its budget.
for (const budget of [1e8, 2.5e8, 5e8, 1e9, 2e9]) {
  const picks = opt.optimize(costs, systems.map(s => s.pop), systems.map(s => s.conn), budget, 0);
  assert.ok(picks.reduce((sum, i) => sum + costs[i], 0) <= budget);
}
console.log(JSON.stringify({result: 'PASS', verified_project_budgets: 1,
  robbins: {old: robbins.cost, published_budget: 8000000, type_average: 1171194},
  conclusion: 'Published-budget correction verified. General project-cost accuracy improvement not established.'}));
