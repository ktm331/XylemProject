"""Reconcile an actual desktop download with frozen Python allocation inputs."""
from pathlib import Path
import csv
import datetime
import hashlib
import io
import json
import math
import re
import sys
from urllib.parse import parse_qs
import numpy as np

evidence = Path(__file__).resolve().parent
candidate = evidence.parent / 'candidate'
sys.path.insert(0, str(candidate / 'pipeline'))
from optimizer import optimize

file = evidence / 'fixed-share-500M.csv'
raw = file.read_bytes()
text = raw.decode('utf-8-sig')
build = json.loads((candidate / 'app/build.json').read_bytes())
assert f"UI_build {build['id']};" in text
assert f"Snapshot {build['snapshot_id']};" in text
query = parse_qs(re.search(r'; scenario ([^;]+);', text).group(1))
st = {k: v[0] if k == 'v' else float(v[0]) for k, v in query.items()}
assert st == {'b': 500, 'l': 1, 'h': 5, 'v': 'fixed', 'a': .5, 'r': 0, 'c': 0, 'm': 1}
systems = json.loads((candidate / 'app/data/systems.json').read_bytes())
equity = np.array([np.mean([v for v in s['eq'] if v is not None])
                   if any(v is not None for v in s['eq']) else np.nan for s in systems])
equity = np.where(np.isnan(equity), np.nanmedian(equity), equity)
costs = [s['cost'] * st['m'] for s in systems]
weights = [1 if s['failing'] else st['a'] for s in systems]
benefits = [s['pop'] * w * (1 + st['l'] * e) for s, w, e in zip(systems, weights, equity)]
chosen = optimize(costs, benefits, [s['conn'] for s in systems], st['b'] * 1e6, st['r'])
rows = list(csv.DictReader(io.StringIO('\n'.join(l for l in text.splitlines() if not l.startswith('#')))))
assert sorted(r['water_system_id'] for r in rows) == sorted(systems[i]['id'] for i in chosen)
people = sum(systems[i]['pop'] for i in chosen)
cost = sum(costs[i] for i in chosen)
assert len(rows) == len(chosen) == 54
assert sum(int(r['people']) for r in rows) == people == 966559
assert math.isclose(sum(float(r['cost_usd']) for r in rows), cost, abs_tol=.0001, rel_tol=0)
assert cost == 493070597
by_id = {s['id']: i for i, s in enumerate(systems)}
for row in rows:
    i = by_id[row['water_system_id']]
    assert math.isclose(float(row['cost_usd']), costs[i], abs_tol=.0001, rel_tol=0)
    assert math.isclose(float(row['allocation_weight']), weights[i], abs_tol=1e-12, rel_tol=0)
    if systems[i]['pf'] is not None:
        assert float(row['snapshot_probability']) == systems[i]['pf']
    assert row['stability_pct'] == '', 'Incompatible saved stability must be blank'
assert sum(max(1, math.ceil(costs[i] / 250000)) * 250000 for i in chosen) <= st['b'] * 1e6
assert f'selected_systems {len(rows)};' in text
assert f'modeled_people {people};' in text
metadata_cost = float(re.search(r'; modeled_cost_usd ([^;]+);', text).group(1))
assert math.isclose(metadata_cost, cost, abs_tol=.0001, rel_tol=0)
assert 'CA1910092' in [r['water_system_id'] for r in rows]
review = json.loads((evidence / 'checks-progress.json').read_bytes())
visible = next(c for c in review['checks'] if c['name'] == 'Fixed At-Risk share 50% at $500M')['observed']
assert '966,559' in visible['kpis'] and '\n54\n' in visible['kpis'] and '$493M' in visible['kpis']
result = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'result': 'PASS', 'scope': 'Actual desktop CSV download; independent frozen Python optimizer',
          'csv': str(file), 'sha256': hashlib.sha256(raw).hexdigest(),
          'systems': len(rows), 'people': people, 'cost_usd': cost,
          'budget_usd': st['b'] * 1e6, 'scenario': st,
          'ui_build': build['id'], 'snapshot_id': build['snapshot_id'],
          'membership_costs_population_weights_stability_metadata': 'PASS',
          'visible_plan_match': 'PASS', 'system_detail_CA1910092_in_export': 'PASS',
          'physical_phone_download': 'UNVERIFIED'}
(evidence / 'csv-reconciliation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
