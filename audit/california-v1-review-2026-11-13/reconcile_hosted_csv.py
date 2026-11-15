"""Reconcile the real hosted desktop download with the frozen $500M plan."""
from pathlib import Path
import csv
import datetime
import hashlib
import io
import json
import math
import re
import sys
import traceback
from urllib.parse import parse_qs
import numpy as np

root = Path(__file__).resolve().parent
candidate = root / 'candidate'
sys.path.insert(0, str(candidate / 'pipeline'))
from optimizer import optimize

result = {
    'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Actual authenticated hosted desktop CSV; independent frozen Python optimizer',
    'physical_phone_spoken_AT_actual_phone_download': 'UNVERIFIED',
    'strict_served_html_bytes': 'FAIL; user retained the exact-byte requirement',
}
try:
    browser = json.loads((root / 'private-sites-browser-smoke.json').read_bytes())
    original = Path(browser['actual_desktop_download_path'])
    raw = original.read_bytes()
    copy = root / 'private-sites-hosted-500M.csv'
    if copy.exists():
        assert copy.read_bytes() == raw, 'Existing evidence differs; preserve it'
    else:
        copy.write_bytes(raw)
    text = raw.decode('utf-8-sig')
    build = json.loads((candidate / 'app/build.json').read_bytes())
    assert f"UI_build {build['id']};" in text
    assert f"Snapshot {build['snapshot_id']};" in text
    scenario = re.search(r'; scenario ([^;]+);', text).group(1)
    st = {k: v[0] if k == 'v' else float(v[0]) for k, v in parse_qs(scenario).items()}
    assert st == {'b': 500, 'l': 1, 'h': 5, 'v': 'fc', 'a': .5, 'r': 0, 'c': 0, 'm': 1}
    assert parse_qs(browser['visible_export_plan']['scenario']) == parse_qs(scenario)
    systems = json.loads((candidate / 'app/data/systems.json').read_bytes())
    forecast = json.loads((candidate / 'app/data/forecast.json').read_bytes())
    summary = json.loads((candidate / 'app/data/summary.json').read_bytes())
    eq = np.array([np.mean([x for x in s['eq'] if x is not None])
                   if any(x is not None for x in s['eq']) else np.nan for s in systems])
    eq = np.where(np.isnan(eq), np.nanmedian(eq), eq)
    fallback = forecast['metrics']['fallback_at_risk_probability']
    weights = [1 if s['failing'] else 1 - (1 - (fallback if s['pf'] is None else s['pf'])) ** st['h']
               for s in systems]
    costs = [s['cost'] for s in systems]
    benefits = [s['pop'] * w * (1 + st['l'] * e) for s, w, e in zip(systems, weights, eq)]
    chosen = optimize(costs, benefits, [s['conn'] for s in systems], st['b'] * 1e6, st['r'])
    rows = list(csv.DictReader(io.StringIO('\n'.join(l for l in text.splitlines() if not l.startswith('#')))))
    ids = [r['water_system_id'] for r in rows]
    assert len(ids) == len(set(ids)) == len(chosen) == 97
    assert sorted(ids) == sorted(systems[i]['id'] for i in chosen)
    assert sorted(ids) == sorted(browser['visible_export_plan']['selected_ids'])
    people = sum(systems[i]['pop'] for i in chosen)
    cost = sum(costs[i] for i in chosen)
    assert sum(int(r['people']) for r in rows) == people == 476663
    assert sum(float(r['cost_usd']) for r in rows) == cost == 487919470
    assert sum(max(1, math.ceil(costs[i] / 250000)) * 250000 for i in chosen) <= 500e6
    by_id = {s['id']: i for i, s in enumerate(systems)}
    stability_index = min(range(len(summary['budgets_musd'])),
                          key=lambda k: abs(math.log(summary['budgets_musd'][k] / st['b'])))
    for row in rows:
        i = by_id[row['water_system_id']]
        s = systems[i]
        assert row['name'] == s['name'] and row['county'] == s['county']
        assert row['status'] == ('Failing' if s['failing'] else 'At-Risk')
        assert int(row['people']) == s['pop'] and int(row['connections']) == s['conn']
        assert float(row['cost_usd']) == costs[i]
        assert math.isclose(float(row['allocation_weight']), weights[i], abs_tol=1e-12, rel_tol=0)
        assert row['snapshot_probability'] == '' if s['pf'] is None else float(row['snapshot_probability']) == s['pf']
        assert int(row['stability_pct']) == math.floor(s['p'][stability_index] * 100 + .5)
    assert f'selected_systems {len(rows)};' in text and f'modeled_people {people};' in text
    assert float(re.search(r'; modeled_cost_usd ([^;]+);', text).group(1)) == cost
    visible = browser['visible_export_plan']['kpis']
    assert '476,663' in visible and '\n97\n' in visible and '$488M' in visible
    result.update(result='PASS', original_download=str(original), evidence_copy=str(copy),
                  sha256=hashlib.sha256(raw).hexdigest(), systems=len(rows), people=people,
                  cost_usd=cost, scenario=st, ui_build=build['id'], snapshot_id=build['snapshot_id'],
                  selected_ids_rows_costs_populations_weights_stability_metadata='PASS',
                  visible_plan_match='PASS',
                  direct_browser_security_globals='UNVERIFIED; browser-control scope does not expose them')
except Exception as error:
    result.update(result='FAIL', error=f'{type(error).__name__}: {error}',
                  failure_line=traceback.extract_tb(error.__traceback__)[-1].lineno)
(root / 'private-sites-hosted-csv-reconciliation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
sys.exit(0 if result['result'] == 'PASS' else 1)
