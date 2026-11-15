"""Prepare only a local static copy; no site registration, upload or publication."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess

root = Path(__file__).resolve().parent
candidate = root / 'candidate'
preview = root / 'sites-preview'
expected_commit = '2ce2832ffc2be043da6dc194c025d6abdbaf13a1'
assert subprocess.check_output(['git', '-C', str(candidate), 'rev-parse', 'HEAD']).decode().strip() == expected_commit
assert not subprocess.check_output(['git', '-C', str(candidate), 'status', '--porcelain=v1']).strip()
assert not preview.exists(), 'Preserve an existing preview; inspect it before repeating'
build = json.loads((candidate / 'app/build.json').read_bytes())
source_files = {p.relative_to(candidate / 'app').as_posix(): p.read_bytes()
                for p in (candidate / 'app').rglob('*') if p.is_file()}
assert len(source_files) == 24
assert set(source_files) == set(build['sha256']) | {'build.json'}
for name, digest in build['sha256'].items():
    assert hashlib.sha256(source_files[name]).hexdigest() == digest, name
shutil.copytree(candidate / 'app', preview / 'dist')
for name, data in source_files.items():
    assert (preview / 'dist' / name).read_bytes() == data, name
receipt = {
    'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS', 'scope': 'Local alternative-host preparation only',
    'source_commit': expected_commit, 'ui_build': build['id'], 'snapshot_id': build['snapshot_id'],
    'static_files_identical': len(source_files),
    'sha256': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(source_files.items())},
    'proposed_host': 'New owner-private Site through Sites, under the current user workspace',
    'proposed_slug': 'xylem-california-v1-efb5e6e0e986',
    'project_id': None, 'site_registered': False, 'uploaded': False, 'deployed': False,
    'alternative_host_authorization': 'PENDING; original approval covers repository Pages only',
    'original_repository': 'unchanged; manual-only Pages preserved',
    'hosted_bytes_and_human_checks': 'UNVERIFIED'
}
(root / 'alternative-preview-preparation.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in receipt.items() if k != 'sha256'}, indent=2))
