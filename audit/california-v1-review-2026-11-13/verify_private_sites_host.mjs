import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
let request;
let result;
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
try {
  request = await hiddenInput();
  const origin = new URL(request.url);
  if (origin.protocol !== 'https:' || origin.origin !== request.expectedOrigin || origin.username || origin.password)
    throw new Error('Unexpected HTTPS Site origin');
  if (typeof request.bearer !== 'string' || !request.bearer) throw new Error('Supported Site service access is unavailable');
  const output = path.resolve(root, request.outputName);
  if (path.dirname(output) !== root || !request.outputName.endsWith('.json')) throw new Error('Output must stay in the release evidence directory');
  try { await fs.access(output); throw new Error('Choose a new output file to preserve existing evidence'); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (request.probeIndex) {
    const response = await fetch(new URL('index.html',origin.origin+'/'), {redirect:'manual',signal:AbortSignal.timeout(30000),
      headers:{'OAI-Sites-Authorization':'Bearer '+request.bearer,'Cache-Control':'no-cache'}});
    const probe = {scope:'Focused index response diagnostic',http_status:response.status,
      location:response.headers.get('location'),url:response.url,credential_recorded:false,
      recorded_at_utc:new Date().toISOString()};
    await fs.writeFile(output,JSON.stringify(probe,null,2)+'\n',{flag:'wx'});
    console.log(JSON.stringify(probe));process.exit(0);
  }
  const buildBytes = await fs.readFile(path.join(root, 'candidate/app/build.json'));
  const build = JSON.parse(buildBytes);
  const nonce = Date.now().toString();
  const files = [];
  const servedURLs = new Map();
  async function readRemote(name) {
    let target = new URL(name, origin.origin + '/');
    if (target.origin !== origin.origin) throw new Error('Asset origin differs from approved Site');
    target.searchParams.set('xylem_verify', nonce);
    for (let redirects=0; redirects<=3; redirects++) {
      const response = await fetch(target, {redirect:'manual', signal:AbortSignal.timeout(30000),
        headers:{'OAI-Sites-Authorization':'Bearer ' + request.bearer, 'Cache-Control':'no-cache'}});
      if (new URL(response.url).origin !== origin.origin) throw new Error('Unexpected response origin');
      if ([301,302,303,307,308].includes(response.status)) {
        const location=response.headers.get('location');
        if (!location) throw new Error('Redirect without Location for '+name);
        const next=new URL(location,target);
        if(next.protocol!=='https:'||next.origin!==origin.origin) throw new Error('Refusing redirect outside approved HTTPS Site');
        target=next;continue;
      }
      if (response.status !== 200) throw new Error('HTTP ' + response.status + ' for ' + name);
      servedURLs.set(name,response.url);
      return Buffer.from(await response.arrayBuffer());
    }
    throw new Error('Too many same-origin redirects for '+name);
  }
  if (request.captureIndex) {
    const bytes=await readRemote('index.html');
    if(bytes.includes(Buffer.from(request.bearer))) throw new Error('Refusing to persist an authentication value found in response content');
    const local=await fs.readFile(path.join(root,'candidate/app/index.html'));
    await fs.writeFile(path.join(root,'private-sites-served-index.html'),bytes,{flag:'wx'});
    const html=bytes.toString('utf8');
    const scripts=[...html.matchAll(/<script\b[^>]*>/gi)].map(m=>{const src=m[0].match(/\bsrc=["']([^"']+)/i)?.[1];if(!src)return {inline:true};const u=new URL(src,origin);return {src:u.origin+u.pathname};});
    const captured={status:'CAPTURED',http_url:servedURLs.get('index.html'),served_bytes:bytes.length,local_bytes:local.length,
      served_sha256:sha(bytes),local_sha256:sha(local),script_tags:scripts,credential_recorded:false};
    await fs.writeFile(output,JSON.stringify(captured,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(captured));process.exit(0);
  }
  const servedBuild = await readRemote('build.json');
  if (!servedBuild.equals(buildBytes)) throw new Error('Hosted build.json bytes differ from reviewed candidate');
  files.push({file:'build.json',status:'PASS',bytes:servedBuild.length,sha256:sha(servedBuild),served_url:servedURLs.get('build.json')});
  const entries = Object.entries(build.sha256);
  let index = 0;
  await Promise.all(Array.from({length:4}, async () => {
    while (index < entries.length) {
      const [name, expected] = entries[index++];
      try {
        const bytes = await readRemote(name);
        const local = await fs.readFile(path.join(root, 'candidate/app', name));
        if (sha(bytes) !== expected || !bytes.equals(local)) throw new Error('Hosted bytes differ from reviewed candidate');
        files.push({file:name,status:'PASS',bytes:bytes.length,sha256:sha(bytes),served_url:servedURLs.get(name)});
      } catch (error) { files.push({file:name,status:'FAIL',error:error.message}); }
      if (files.length % 6 === 0) console.log(JSON.stringify({files_checked:files.length,total:24}));
    }
  }));
  result = {status:files.length===24 && files.every(f=>f.status==='PASS')?'PASS':'FAIL',
    scope:'Exact authenticated HTTPS response bytes; not physical-phone or spoken-AT testing',
    url:origin.origin,project_id:request.projectId,source_commit:request.sourceCommit,
    original_commit:'2ce2832ffc2be043da6dc194c025d6abdbaf13a1',deployment_id:request.deploymentId,
    version_id:request.versionId,ui_build:build.id,snapshot_id:build.snapshot_id,
    supported_service_access_used:true,credential_recorded:false,
    files:files.sort((a,b)=>a.file.localeCompare(b.file)),
    browser_smoke_test:'PENDING',physical_phone_spoken_AT_actual_phone_download:'UNVERIFIED'};
} catch (error) {
  result = {status:'FAIL',scope:'Private Site HTTPS verification',
    error:String(error.message).split(request?.bearer || '\0').join('[redacted]'),credential_recorded:false};
}
result.recorded_at_utc = new Date().toISOString();
if (request?.outputName && path.basename(request.outputName)===request.outputName)
  await fs.writeFile(path.join(root,request.outputName),JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({status:result.status,files:result.files?.length,ui_build:result.ui_build,error:result.error}));
process.exitCode = result.status==='PASS'?0:1;

async function hiddenInput() {
  const input = await new Promise((resolve,reject)=>{
    let text=''; const terminal=process.stdin.isTTY;
    function finish(error){process.stdin.removeListener('data',onData);process.stdin.removeListener('end',onEnd);if(terminal)process.stdin.setRawMode(false);process.stdin.pause();error?reject(error):resolve(text);}
    function onData(chunk){text+=chunk;if(text.includes('\u0003'))finish(new Error('Verification cancelled'));else if(text.length>65536)finish(new Error('Verification input too large'));else if(/[\r\n]/.test(text))finish();}
    function onEnd(){finish();}
    if(terminal){process.stdin.setRawMode(true);process.stderr.write('Ready for private HTTPS verification input (hidden).\n');}
    process.stdin.setEncoding('utf8');process.stdin.on('data',onData);process.stdin.once('end',onEnd);process.stdin.resume();
  });
  try { return JSON.parse(input); } catch { throw new Error('Invalid verification input'); }
}
