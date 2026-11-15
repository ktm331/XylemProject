# Private Xylem preview — desktop checks completed, exact-byte gate blocked

The user explicitly approved the private Sites preview. The Site is published at:

https://xylem-california-v1-efb5e6e0e986.srpatlola2020.chatgpt.site

This is a private owner-only Site. It is a review URL, **not a verified phone-testing link**. No public Sites access, additional viewer, original GitHub push, PR or outreach was performed. The separate earlier public GitHub Pages approval remains recorded but has not been executed.

**Subsequent November 13 project review:** [Hackathon assessment and remaining work](HACKATHON_ASSESSMENT.md) records current official event requirements and a newly confirmed identity defect: `CA5610029` is displayed/exported as `10/30/2026`, while the official state record names Vineyard Avenue Acres MWC. Its card was observed in the hosted app. [Frozen-data scan](project-review-profile.json), [observed card](project-review-bad-name.png). No repair or model/data edit was made. CSV consistency passes below establish agreement with the frozen inputs, not correctness of this source name.

## Publication and source identity

- Project: `appgprj_6af7df45649c81918b43785b33a7c926`.
- Saved version: `appgprj_6af7df45649c81918b43785b33a7c926~appgver_8b04f1f526a4819191696c2d8d1c5754`.
- Successful deployment: `appgdep_6af7e0d467dc81919a6c6274c31a2e94`.
- Private Sites source commit: `6f0cd6f96abcc6d8e10605641e4db24666b57912`.
- Original reviewed GitHub commit: `2ce2832ffc2be043da6dc194c025d6abdbaf13a1`.
- UI build: `efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b`.
- Frozen snapshot: `806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd`.

The backend confirmed the current user is owner; access is custom with one allowed user and zero groups. The owner-private publishing operation succeeded. [Deployment receipt](private-sites-deployment.json), [approval](private-sites-approval.json), [package/source verification](private-sites-package-verification.json).

All 24 app files in the private source commit and deployment archive match the reviewed candidate exactly. The archive adds only required Sites hosting metadata outside the app assets. No app, model, data or scientific expectation was changed. Original Pages remains manual-only. No model retraining or raw-input download occurred.

## Exact HTTPS verification — qualified result

All **23 non-HTML app files**, including `build.json`, JavaScript, CSS, vendor assets and data, matched their exact reviewed bytes over authenticated HTTPS. Existing service access returned by `get_site` was used only for this same Site, via an authentication header. No credential was created/rotated, written to disk, exposed in output or put in a browser URL.

The host redirects `/index.html` to `/`. The verifier now follows only HTTPS redirects within the same approved Site origin and still rejects cross-origin redirects. [Focused redirect receipt](private-sites-index-probe.json).

The served HTML contains the entire original 8,903-byte document unchanged **plus one 1,114-byte Cloudflare JavaScript Detection script inserted immediately before `</body>`**. The response is therefore 10,017 bytes, and its raw SHA-256 differs. Independent comparison confirms zero removed or changed original bytes. [HTML comparison](private-sites-html-comparison.json), [served-response metadata; raw response retained locally](private-sites-index-capture.json), [full HTTPS receipt](private-sites-hosted-verification-02.json).

**Strict served-HTML byte check: FAIL.** Original application HTML preserved: PASS. These results must not be conflated. The earlier handoff's all-files-identical hosted gate has not passed. After receiving an explanation, the user explicitly chose **“Keep the exact-byte requirement.”** The hosting-only exception is **DECLINED**, not pending. Private publication approval does not waive this requirement. [Decision receipt](private-sites-exact-byte-decision.json).

Cloudflare documents the HTML-injected `/cdn-cgi/challenge-platform/` JavaScript Detection mechanism in its [primary documentation](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/). No bot/security protection, account setting, firewall, TLS verification or Site audience was changed to suppress it.

## Browser and human gates

After the accidental exit, the original private tab was absent. The existing deployment was reopened without recreating or republishing it. The reopened tab required sign-in again; the user completed it, and the Xylem planner was visibly observed. Authentication was not automated. The Site remains active, owner-private: one allowed user and zero groups. [Reopened sign-in state](private-sites-signin-reopened.png).

Agent-operated hosted desktop checks now establish:

- **PASS:** expected UI build `efb5e6e0e986` and snapshot `806032f64da1` loaded at the private HTTPS URL; no snapshot error; live 3D map observed.
- **PASS:** default $100M gives 20 systems / 171,738 modeled people; default $500M gives 97 / 476,663, displayed cost $488M.
- **PASS:** a real hosted desktop download arrived at `C:\Users\sai71\Downloads\xylem-placement-plan (3).csv`. An evidence copy was independently reconciled with the frozen Python optimizer and visible plan: 97 unique selected IDs, 476,663 people, exact modeled cost $487,919,470, matching rows, costs, weights, stability and full build/snapshot/scenario metadata. CSV SHA-256 `cb24ce54050680505b52a7a0f7b52471ed900082b38ca6d7b7b1c6e09c5643d9`. This file was read for reconciliation; a native app opening of this new hosted CSV was not performed.
- **UNVERIFIED directly:** browser security globals (`isSecureContext`, `crypto.subtle`) are not exposed by the browser-control read-only scope. The initial probe's FAIL is retained, but it is not evidence that the real page lacks crypto. Successful initialization of the unchanged app demonstrates completion of its SHA-256 data-verification path; that is a source-supported inference, not a direct global probe.

[Browser receipt](private-sites-browser-smoke.json), [CSV reconciliation](private-sites-hosted-csv-reconciliation.json), [CSV copy](private-sites-hosted-500M.csv), [full hosted view](private-sites-hosted-full.png), [top view](private-sites-hosted-top.png). Local desktop tasks, including native Chrome 200% zoom and opening the earlier fixed-share download in Notepad, remain separately recorded in [desktop completion](desktop-review-2026-11-13/DESKTOP_COMPLETION.md). They were not repeated or reclassified as phone evidence.

The all-files-identical hosted gate is still blocked. Do not provide this private URL as the verified release/phone-testing build. The prepared GitHub Pages route remains authorized for the exact original commit but needs an existing repository admin/maintainer to select GitHub Actions as the Pages source. Once that route is available, recheck current main, dispatch the unchanged manual workflow once, and verify all served bytes plus browser gates. Do not suppress Cloudflare protection or silently relax the requirement. [Prepared Pages action](PREPARED_RELEASE.md).

After those gates pass, use [PHONE_TEST.md](../../audit/PHONE_TEST.md) and [PHONE_OBSERVATIONS.md](PHONE_OBSERVATIONS.md). Physical phones, native phone text scaling/zoom, spoken VoiceOver/TalkBack and actual phone downloads remain UNVERIFIED. Practitioner review remains pending; no outreach occurred. Annual-risk validity remains a separate unresolved research requirement.

## Attempts retained

Source-network and local ownership failures and the package-layout checker correction are retained in [upload attempts](private-sites-upload-attempts.md). The first HTTPS check rejected the index redirect; the second followed the safe same-origin redirect and correctly reported the HTML mismatch. The focused HTML capture completed and wrote its evidence, then Node's immediate exit hit a Windows libuv shutdown assertion; the saved bytes were independently inspected and compared, with no effect on the static hosted app. An initial longest-common-prefix comparison placed the boundary inside the shared `<` character; the final comparison uses the known closing-body boundary and retains exact reconstruction of the original HTML.

Continue with the same project/version/deployment. Do not recreate, republish, weaken protection, generate a bypass token or broaden sharing merely to address the pending review gates. Source repository credentials and existing service access are held only in session memory; reacquire supported access through the same Site tools if the session is lost.

On this resumed review, the first two CSV reconciliation receipts ended with an unrelated aggregate browser-security assertion after every CSV assertion had passed. Both are retained in `private-sites-hosted-csv-reconciliation-attempt-01.json` and `-attempt-02.json`. The reconciler now reports CSV correctness independently from the unsupported direct browser-global probe; no CSV expectation, frozen number or model result was changed. The initial browser receipt is retained in `private-sites-browser-smoke-attempt-01.json`. The isolated candidate remains clean and Pages remains `workflow_dispatch`-only.
