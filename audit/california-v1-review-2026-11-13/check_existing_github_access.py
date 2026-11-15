"""Check existing repository-scoped Git credentials, without interactive sign-in."""
from pathlib import Path
import datetime
import json
import os
import subprocess
import urllib.request

root = Path(__file__).resolve().parent
output = root / 'existing-github-access.json'
if output.exists():
    raise SystemExit('Preserve existing receipt; choose a new filename before repeating')
env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GCM_INTERACTIVE': 'Never'}
result = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'Read-only existing Git credential and repository access check',
          'credentials_disclosed': False, 'mutation': 'NONE'}
try:
    credential = subprocess.run(
        ['git', '-C', str(root / 'candidate'), 'credential', 'fill'],
        input='protocol=https\nhost=github.com\npath=palashraks-afk/XylemProject.git\n\n',
        text=True, capture_output=True, env=env, timeout=20)
    values = dict(line.split('=', 1) for line in credential.stdout.splitlines() if '=' in line)
    secret = values.get('password')
    result['existing_credential_available'] = bool(secret)
    if secret:
        req = urllib.request.Request('https://api.github.com/repos/palashraks-afk/XylemProject',
              headers={'Authorization': 'Bearer ' + secret,
                       'User-Agent': 'Xylem-approved-release',
                       'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=20) as response:
            repo = json.load(response)
        result.update({'has_pages': repo.get('has_pages'),
                       'permissions': repo.get('permissions'), 'status': 'CHECKED'})
    else:
        result['status'] = 'NO_EXISTING_CREDENTIAL'
except Exception as exc:
    result.update({'status': 'ACCESS_CHECK_UNAVAILABLE', 'error_type': type(exc).__name__})
output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
