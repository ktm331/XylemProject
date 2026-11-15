from pathlib import Path
import datetime
import hashlib
import json

root = Path(__file__).resolve().parent
local = (root / 'candidate/app/index.html').read_bytes()
served = (root / 'private-sites-served-index.html').read_bytes()
prefix = local.rfind(b'</body>')
assert prefix >= 0
suffix = len(local) - prefix
assert served.startswith(local[:prefix]) and served.endswith(local[prefix:])
removed = b''
added = served[prefix:len(served)-suffix]
assert not removed, 'The hosting response changed or removed original HTML bytes'
assert added.startswith(b'<script>') and added.endswith(b'</script>')
assert b'window.__CF$cv$params' in added
assert b'/cdn-cgi/challenge-platform/scripts/jsd/main.js' in added
assert served[:prefix] + served[prefix+len(added):] == local
result = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'strict_served_html_byte_check': 'FAIL', 'original_application_html_preserved': True,
          'only_difference': 'One added Cloudflare JavaScript Detection script immediately before closing body',
          'local_bytes': len(local), 'served_bytes': len(served), 'added_bytes': len(added),
          'removed_or_changed_original_bytes': 0, 'insertion_offset': prefix,
          'original_sha256': hashlib.sha256(local).hexdigest(),
          'served_sha256': hashlib.sha256(served).hexdigest(),
          'added_script_sha256': hashlib.sha256(added).hexdigest(),
          'other_23_served_app_files': 'PASS; exact bytes in private-sites-hosted-verification-02.json',
          'hosting_security_changed': False, 'source_or_model_changed': False,
          'strict_gate_exception': 'PENDING; do not silently relabel strict byte failure as PASS'}
(root / 'private-sites-html-comparison.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
