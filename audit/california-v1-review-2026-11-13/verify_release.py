"""Read-only candidate/HTTPS verification; never dispatches or changes a site."""
from pathlib import Path
import argparse
import datetime
import gzip
import hashlib
import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / 'candidate'
PRIOR = Path(r'C:\Users\sai71\.codex\visualizations\2026\11\12\01a1ceb1-04db-7401-8063-6ff21bd35b5f')
COMMIT = '2ce2832ffc2be043da6dc194c025d6abdbaf13a1'
BASE = 'f0fa6006032f6b614276395c5628596a63b966fa'
BUILD = 'efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b'
SNAPSHOT = '806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd'
SITE = 'https://palashraks-afk.github.io/XylemProject/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return json.loads(path.read_bytes())

def git(*args):
    return subprocess.check_output(['git', '-C', str(CANDIDATE), *args])

def preflight():
    assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
    assert git('rev-parse', 'HEAD^').decode().strip() == BASE
    assert not git('status', '--porcelain=v1').strip(), 'Candidate must be clean'
    prior = read(PRIOR / 'accessibility-final-verification.json')
    tracked = git('ls-files', '-z').decode().strip('\0').split('\0')
    assert set(tracked) == set(prior['tracked_sha256'])
    for name in tracked:
        assert sha((CANDIDATE / name).read_bytes()) == prior['tracked_sha256'][name], name
    assert not git('diff', BASE, 'HEAD', '--', 'app/data', 'data', 'pipeline', '.github')
    build = read(CANDIDATE / 'app/build.json')
    assert build['id'] == BUILD and build['snapshot_id'] == SNAPSHOT
    assert sha(json.dumps(build['sha256'], sort_keys=True, separators=(',', ':')).encode()) == BUILD
    app_files = {p.relative_to(CANDIDATE / 'app').as_posix(): p.read_bytes()
                 for p in (CANDIDATE / 'app').rglob('*') if p.is_file()}
    assert set(app_files) == set(build['sha256']) | {'build.json'}
    for name, expected in build['sha256'].items():
        assert sha(app_files[name]) == expected, name
    snapshot = read(CANDIDATE / 'app/data/snapshot.json')
    assert snapshot['id'] == SNAPSHOT
    assert sha(json.dumps(snapshot['sha256'], sort_keys=True).encode()) == SNAPSHOT
    for name, expected in snapshot['sha256'].items():
        assert sha((CANDIDATE / 'app/data' / name).read_bytes()) == expected, name
    vendor = read(CANDIDATE / 'app/vendor/manifest.json')
    for name, expected in vendor['sha256'].items():
        assert sha((CANDIDATE / 'app/vendor' / name).read_bytes()) == expected, name
    package = read(CANDIDATE / 'audit/accessibility/build-and-package.json')
    package_path = Path(package['zip'])
    assert sha(package_path.read_bytes()) == package['zip_sha256']
    with zipfile.ZipFile(package_path) as archive:
        assert len(archive.namelist()) == len(set(archive.namelist())) == 24
        assert set(archive.namelist()) == set(app_files)
        for name in archive.namelist():
            assert archive.read(name) == app_files[name], name
    archive_root = CANDIDATE / 'audit/accessibility'
    archives = read(archive_root / 'axe-archive.json')
    final_scans = []
    for name, evidence in archives.items():
        compressed = (archive_root / evidence['archive']).read_bytes()
        assert sha(compressed) == evidence['archive_sha256'], name
        raw = gzip.decompress(compressed)
        assert sha(raw) == evidence['raw_sha256'] and len(raw) == evidence['raw_bytes'], name
        if name.startswith('verified/'):
            scan = json.loads(raw)
            assert not scan['violations'], name
            final_scans.append({'file': name, 'violations': 0,
                                'incomplete': [{'id': item['id'], 'nodes': len(item['nodes'])}
                                               for item in scan['incomplete']]})
    assert len(final_scans) == 8
    evaluation = read(CANDIDATE / 'data/planner_evaluation.json')
    presentation = read(CANDIDATE / 'audit/release-qa/presentation-provenance.json')
    diagnostic = {**evaluation['input_and_code_hashes'], **evaluation['output_hashes']}
    nonraw = {k: v for k, v in diagnostic.items() if not k.startswith('data/raw/')}
    assert sha((CANDIDATE / presentation['path']).read_bytes()) == presentation['current_sha256']
    for name, expected in nonraw.items():
        checked_path = presentation['archived_path'] if name == 'app/app.js' else name
        assert sha((CANDIDATE / checked_path).read_bytes()) == expected, name
    exports = read(archive_root / 'export-reconciliation-final.json')
    for export in exports:
        assert export['python_membership'] == 'PASS'
        assert sha((CANDIDATE / export['file']).read_bytes()) == export['sha256']
    a11y = read(archive_root / 'verified/checks.json')
    release = read(archive_root / 'release-verified/checks.json')
    assert all(c['status'] == 'PASS' for c in a11y['checks'] + release['checks'])
    workflow = (CANDIDATE / '.github/workflows/pages.yml').read_text()
    triggers = workflow.split('on:\n', 1)[1].split('permissions:', 1)[0]
    assert triggers.strip() == 'workflow_dispatch:'
    assert 'path: app\n' in workflow
    return {'status': 'PASS', 'candidate_commit': COMMIT, 'ui_build': BUILD,
            'snapshot_id': SNAPSHOT, 'tracked_files_matched': len(tracked),
            'app_files_verified': len(app_files), 'data_files_verified': len(snapshot['sha256']),
            'vendor_files_verified': len(vendor['sha256']), 'zip_sha256': package['zip_sha256'],
            'zip_files_matched': 24, 'lossless_axe_archives_verified': len(archives),
            'final_axe_scans': final_scans, 'nonraw_diagnostic_hashes_verified': len(nonraw),
            'frozen_paths': 'unchanged', 'workflow': 'workflow_dispatch only; unchanged',
            'existing_automated_results_revalidated_by_file_hash': {
                'accessibility': a11y['summary'], 'release_browser': release['summary'],
                'python_tests': 121, 'optimizer_parity_cases': 110,
                'reconciled_csvs': len(exports)},
            'raw_inputs': '335 previously verified; not re-extracted or downloaded this turn',
            'human_phone_spoken_AT_actual_downloads': 'UNVERIFIED',
            'deployment_authorization': ('APPROVED for this commit; see publishing-approval.json'
                                         if (ROOT / 'publishing-approval.json').exists()
                                         and read(ROOT / 'publishing-approval.json')['approved_commit'] == COMMIT
                                         else 'PENDING'), 'deployment': 'NOT PERFORMED'}

class HTTPSOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).scheme != 'https':
            raise ValueError('Refusing non-HTTPS redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def hosted():
    """Verify bytes only; a PASS still requires a browser smoke test and run SHA."""
    opener = urllib.request.build_opener(HTTPSOnly())
    results = []
    local_build_bytes = (CANDIDATE / 'app/build.json').read_bytes()
    build = json.loads(local_build_bytes)
    expected_files = {'build.json': sha(local_build_bytes), **build['sha256']}
    nonce = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for name, expected in expected_files.items():
        url = SITE + urllib.parse.quote(name, safe='/') + '?xylem_verify=' + nonce
        request = urllib.request.Request(url, headers={'Cache-Control': 'no-cache',
                                                     'User-Agent': 'Xylem-release-verifier'})
        with opener.open(request, timeout=30) as response:
            assert response.status == 200, name
            assert urllib.parse.urlsplit(response.url).scheme == 'https'
            data = response.read()
            assert sha(data) == expected, f'Hosted bytes differ: {name}'
            if name == 'build.json':
                assert data == local_build_bytes
                assert json.loads(data)['id'] == BUILD
            results.append({'file': name, 'sha256': sha(data), 'bytes': len(data),
                            'url': response.url, 'status': 'PASS'})
    return {'status': 'PASS', 'scope': 'HTTPS exact-byte verification only', 'site': SITE,
            'candidate_commit_expected': COMMIT, 'ui_build': BUILD, 'snapshot_id': SNAPSHOT,
            'files': results, 'workflow_run_source_sha': 'UNVERIFIED by this script',
            'browser_crypto_snapshot_plan_csv': 'UNVERIFIED by this script',
            'physical_phone_spoken_AT_actual_device_download': 'UNVERIFIED'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['preflight', 'hosted'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Choose a new output path; existing evidence is never overwritten')
    try:
        result = preflight() if args.mode == 'preflight' else hosted()
    except Exception as exc:
        result = {'status': 'FAIL', 'mode': args.mode, 'error': str(exc),
                  'deployment': 'NOT PERFORMED by this script'}
    result['recorded_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
