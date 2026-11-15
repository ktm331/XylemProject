from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import tarfile

root = Path(__file__).resolve().parent
source = json.loads((root / 'private-sites-source.json').read_bytes())
site = Path(source['checkout_path'])
candidate = root / 'candidate/app'
expected = json.loads((root / 'alternative-preview-preparation.json').read_bytes())
tracked = subprocess.check_output(['git', '-C', str(site), 'ls-files', '-z']).decode().strip('\0').split('\0')
assert set(tracked) == {'.gitattributes', '.openai/hosting.json'} | {'dist/' + n for n in expected['sha256']}
for name, digest in expected['sha256'].items():
    data = subprocess.check_output(['git', '-C', str(site), 'show', source['commit_sha'] + ':dist/' + name])
    assert hashlib.sha256(data).hexdigest() == digest, name
    assert data == (candidate / name).read_bytes(), name
with tarfile.open(source['archive'], 'r:*') as archive:
    files = {m.name.removeprefix('./'): m for m in archive.getmembers() if m.isfile()}
    assert set(files) == {'dist/.openai/hosting.json'} | {'dist/' + n for n in expected['sha256']}, sorted(files)
    assert not any(m.issym() or m.islnk() for m in archive.getmembers())
    manifest = json.load(archive.extractfile(files['dist/.openai/hosting.json']))
    assert manifest['project_id'] == source['project_id']
    assert manifest['static']['directory'] == 'dist'
    for name, digest in expected['sha256'].items():
        data = archive.extractfile(files['dist/' + name]).read()
        assert hashlib.sha256(data).hexdigest() == digest, name
        assert data == (candidate / name).read_bytes(), name
result = {'status': 'PASS', 'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          **source, 'original_commit': expected['source_commit'], 'ui_build': expected['ui_build'],
          'snapshot_id': expected['snapshot_id'], 'app_files': 24,
          'source_blobs_exact': True, 'archive_app_files_exact': True,
          'archive_sha256': hashlib.sha256(Path(source['archive']).read_bytes()).hexdigest(),
          'archive_contains_only': '24 app files and required hosting manifest'}
(root / 'private-sites-package-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
