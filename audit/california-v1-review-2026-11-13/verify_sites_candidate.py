"""Read-only guard for the unchanged static candidate prepared for Sites."""
from pathlib import Path
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parent
site = root / 'sites-preview'
app = root / 'candidate/app'
receipt = json.loads((root / 'alternative-preview-preparation.json').read_bytes())
files = {p.relative_to(site / 'dist').as_posix(): p.read_bytes()
         for p in (site / 'dist').rglob('*') if p.is_file()}
assert set(files) == set(receipt['sha256']) and len(files) == 24
for name, data in files.items():
    assert data == (app / name).read_bytes(), name
    assert hashlib.sha256(data).hexdigest() == receipt['sha256'][name], name
build = json.loads(files['build.json'])
assert build['id'] == receipt['ui_build']
assert build['snapshot_id'] == receipt['snapshot_id']
assert hashlib.sha256(json.dumps(build['sha256'], sort_keys=True, separators=(',', ':')).encode()).hexdigest() == build['id']
assert not subprocess.check_output(['git', '-C', str(root / 'candidate'), 'status', '--porcelain=v1']).strip()
print(json.dumps({'status': 'PASS', 'app_files_identical': len(files),
                  'ui_build': build['id'], 'snapshot_id': build['snapshot_id']}))
