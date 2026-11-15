"""Read-only data and delivery profile for the hackathon assessment."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import io
import json
import re

root = Path(__file__).resolve().parent
candidate = root / 'candidate'
systems = json.loads((candidate / 'app/data/systems.json').read_bytes())
build = json.loads((candidate / 'app/build.json').read_bytes())
labels = collections.defaultdict(list)
for s in systems:
    labels[f"{s['name']} · {s['county']}"].append(s['id'])
date_names = [{k: s[k] for k in ('id', 'name', 'county', 'pop', 'conn')}
              for s in systems if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', s['name'])]
missing_geo = [s['id'] for s in systems if s['lat'] is None or s['lon'] is None or not s['lat'] or not s['lon']]
csv_text = (root / 'private-sites-hosted-500M.csv').read_text(encoding='utf-8-sig')
funded = {r['water_system_id'] for r in csv.DictReader(io.StringIO('\n'.join(l for l in csv_text.splitlines() if not l.startswith('#'))))}
result = {
  'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'scope': 'Read-only full scan of the frozen app systems; not validation of source-field truth',
  'ui_build': build['id'], 'snapshot_id': build['snapshot_id'],
  'systems': len(systems), 'unique_ids': len({s['id'] for s in systems}),
  'modeled_population_sum_not_deduplicated': sum(s['pop'] for s in systems),
  'missing_or_zero_coordinates': missing_geo,
  'missing_at_risk_forecast': [s['id'] for s in systems if not s['failing'] and s['pf'] is None],
  'duplicate_search_labels': {k: v for k, v in labels.items() if len(v) > 1},
  'date_shaped_system_names': date_names,
  'date_shaped_names_in_default_500M_plan': [s for s in date_names if s['id'] in funded],
  'invalid_population_or_connections': [s['id'] for s in systems if s['pop'] <= 0 or s['conn'] <= 0],
  'spreadsheet_formula_leading_names': [s['id'] for s in systems if s['name'].lstrip().startswith(('=', '+', '-', '@'))],
  'app_total_bytes': sum(p.stat().st_size for p in (candidate / 'app').rglob('*') if p.is_file()),
  'root_license_files': [p.name for p in candidate.glob('LICENSE*')],
  'candidate_systems_sha256': hashlib.sha256((candidate / 'app/data/systems.json').read_bytes()).hexdigest(),
  'frozen_files_modified': False,
}
(root / 'project-review-profile.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
