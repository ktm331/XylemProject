"""Verify this computer's loopback preview against the frozen app bytes."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

root = Path(__file__).resolve().parent
app = root / 'candidate/app'
url = 'http://127.0.0.1:8891/'
build = json.loads((app / 'build.json').read_bytes())
files = ['build.json', *build['sha256']]
checks = []
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
for name in files:
    with opener.open(url + name, timeout=10) as response:
        assert response.status == 200, name
        data = response.read()
    assert data == (app / name).read_bytes(), name
    checks.append({'file': name, 'sha256': hashlib.sha256(data).hexdigest(), 'status': 'PASS'})
receipt = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'scope': 'Local loopback preview, desktop only', 'status': 'PASS',
           'url': url, 'ui_build': build['id'], 'snapshot_id': build['snapshot_id'],
           'files': checks, 'external_upload_or_publication': 'NONE',
           'physical_phone_and_spoken_AT_actual_device_download': 'UNVERIFIED'}
output = root / ('local-preview-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.json')
output.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'files': len(files), 'ui_build': build['id'], 'url': url, 'receipt': str(output)}))
