# California v1 — prepared manual Pages publication

Prepared November 12, 2026 Pacific. **The user has explicitly approved public Pages enablement and deployment of `2ce2832`.** See [approval receipt](publishing-approval.json). The browser is now signed in as `Spondasas`; that same connected account has push access but no admin/maintainer access. Execution remains pending Pages source selection by the repository owner `palashraks-afk` or another existing admin/maintainer. See [signed-in access status](signed-in-access-status.json). Nothing has been dispatched, deployed, exposed or sent.

## Exact approved action

Enable this repository's public GitHub Pages source as **GitHub Actions**, then manually run its existing **Deploy app to GitHub Pages** workflow on `main` only while it still equals **`2ce2832ffc2be043da6dc194c025d6abdbaf13a1`**. Publish only the existing `app` folder. Preserve `workflow_dispatch` as the sole trigger.

Intended default public address: `https://palashraks-afk.github.io/XylemProject/`. This address is inferred from GitHub's project-site convention; it is **not a verified phone-testing link**. Record the actual Pages URL after setup. A different destination requires review before publication.

UI build: `efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b` (header `efb5e6e0e986`). Forecast snapshot: `806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd`.

## Setup finding that changes the handoff assumption

The GitHub repository API reports **`has_pages: false`**. All four recorded workflow attempts failed; the latest failed in `actions/configure-pages@v5` with “Get Pages site failed” / “Not Found,” with `enablement: false`. Upload and deployment were skipped. This appears to be initial Pages enablement, rather than replacement of a verified existing site.

The connected account has `push: true`, `admin: false`, `maintain: false`. GitHub requires admin or maintainer permission to configure a publishing source. After publication is approved, a repository administrator/maintainer must open [Settings → Pages](https://github.com/palashraks-afk/XylemProject/settings/pages) and select **Build and deployment → Source → GitHub Actions**. Reuse the existing workflow; no new template is needed. Do not select branch-based publication or add automatic triggers.

The connected GitHub tools can inspect the repository, workflow and runs, but expose no workflow-dispatch or Pages-configuration action. Browser inspection was attempted and stopped because its current URL could not be confidently established. No browser setting was changed. The exact Pages source, custom-domain/HTTPS settings and environment approval rules have consequently not been inspected in a signed-in settings page.

Evidence: [GitHub preparation receipt](github-preparation.json), [prior failed job log](prior-deployment-failure.log), [current repository](https://api.github.com/repos/palashraks-afk/XylemProject), [latest failed attempt](https://github.com/palashraks-afk/XylemProject/actions/runs/41766913118), [reviewed workflow](https://github.com/palashraks-afk/XylemProject/blob/2ce2832ffc2be043da6dc194c025d6abdbaf13a1/.github/workflows/pages.yml). GitHub's [publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) establish the role requirement and source choice. Its [site-address documentation](https://docs.github.com/en/get-started/start-your-journey/deploying-your-website-automatically) supports the inferred default URL only; this release retains its own manual workflow.

## Preparation completed and preserved

An isolated, clean, detached checkout is in `candidate/`. Both read-only GitHub `main` checks returned the reviewed SHA. No new application edits, commits, pushes or PRs were made. The earlier checkouts and separate supplied work repositories were not modified. The OneDrive workspace rejected creation of a new release directory, so this package uses the current chat's writable artifact directory.

[New local verification receipt](preflight-01.json):

- **PASS:** all 612 tracked files match the complete handoff delivery hash map.
- **PASS:** all 24 static files, including `build.json`, match the prepared ZIP; all 23 receipt-bound assets match; build and snapshot identities recompute correctly.
- **PASS:** 10 frozen data hashes, 6 vendor hashes, 32 non-raw diagnostic hashes and all 32 lossless axe archives.
- **PASS:** all 34 previously reconciled CSV files still match their hashes and existing Python membership results.
- **PASS:** `app/data`, `data`, `pipeline` and `.github` retain their reviewed base bytes; manual-only workflow and app-only upload preserved.
- **PASS, newly run:** static verification, JavaScript syntax and whitespace checks; isolated candidate remains clean.

Existing passing evidence is preserved and its bytes rechecked: 32 targeted accessibility checks, 37 broader browser checks, 121 Python tests, 110 optimizer parity cases, 34 independent CSV reconciliations and eight axe scans with zero returned violations. **Those suites were not rerun in this preparation turn.** Incomplete/manual review items remain; this is not accessibility certification. The 335 raw-input hashes were verified in the prior repair task; no raw archive was extracted, source redownloaded or model retrained here.

The original static preview ZIP remains unchanged at `C:\Users\sai71\.codex\visualizations\2026\11\12\01a1ceb1-04db-7401-8063-6ff21bd35b5f\XylemAccessibility-efb5e6e0e986-preview.zip`; SHA-256 `3edd4ad7c698057798b700e9872baacafc548b957482092ae2d9f6f2b5eee006`.

## Authorized execution sequence

1. Approval has been recorded. The current browser is signed out: its Pages URL shows GitHub's 404 page with a Sign in link. The connected account still lacks admin/maintainer access, and a noninteractive Git credential check found no existing credential. The user must sign in using a repository owner/admin account. Then complete the approved GitHub Actions source selection, confirming the actual HTTPS destination and any environment review requirements without weakening protections. Do not ask for publication approval again for this unchanged release.
2. Re-read GitHub `main`. If it differs from the approved SHA, stop before dispatch and inspect the changes; do not silently publish them. No tag, workflow edit, new push or broader permission is part of this package.
3. Open [the existing manual workflow](https://github.com/palashraks-afk/XylemProject/actions/workflows/pages.yml), select `main`, and use **Run workflow** once. A signed-in owner can do this if browser control remains unavailable. Do not rerun an older failed push-triggered run, since that would deploy its old source.
4. Record the new run ID, `event: workflow_dispatch`, source SHA equal to `2ce2832ffc2be043da6dc194c025d6abdbaf13a1`, successful deploy job and actual Pages environment URL. A green job alone does not pass the hosted gate.
5. Run the prepared read-only HTTPS verifier against the agreed URL. Fetch `build.json` and every asset in its `sha256` map, compare exact bytes against `candidate/app`, verify the full build ID and preserve a new timestamped receipt. Keep TLS validation enabled. The verifier is currently fixed to the intended default address and must be deliberately reviewed if the actual address differs.
6. In a real HTTPS browser session, confirm `isSecureContext`, working `crypto.subtle`, snapshot verification, header build and no snapshot error. Check default $100M and $500M plans and capture a desktop CSV. Reconcile IDs, exact costs, people and UI/snapshot/scenario metadata. Label this as an automated/desktop check, not a physical-phone download.
7. Only after the run-source, exact hosted bytes and browser smoke gates pass, provide the verified phone link and guide the physical-phone/spoken-AT checks. Keep unavailable platforms and unperformed steps **UNVERIFIED**.

`verify_release.py preflight --output <new-receipt.json>` repeats the read-only candidate checks. `verify_release.py hosted --output <new-hosted-receipt.json>` verifies all 24 HTTPS files and refuses to overwrite evidence. It does not dispatch anything and does not pass the browser, run-SHA or human gates. Use Python standard library only; the already installed independent Python can run it without installation.

The pre-approval HTTPS attempt is retained in [hosted-before-approval.json](hosted-before-approval.json): **FAIL to access network**, Windows socket access denied. A web-tool attempt also could not access that endpoint. These are access limitations, not proof of an HTTP 404, asset mismatch or website defect. No hosted pass is claimed.

## Human test gate

Use [the complete phone walkthrough](../../audit/PHONE_TEST.md) and [this build-specific observation log](PHONE_OBSERVATIONS.md). Start with a 15–20-minute physical-phone smoke test, then a spoken VoiceOver/TalkBack walkthrough. Record actual model, OS, browser/version, assistive technology, orientation, text size/zoom, exact build, expected behavior and observed behavior. One platform does not cover the other.

Frozen default expectations: **$100M → 20 systems / 171,738 modeled people**; **$500M → 97 / 476,663 / $487,919,470 modeled cost**. Cover portrait/landscape, enlarged text, 30% reserve, fixed share 50%, detail updates/closing/focus return, map bypass and 3D/2D recovery, settled announcements and scenario cancellation. Save and open a real CSV in Files/Downloads with the screen reader enabled and match its full UI build, snapshot and scenario metadata.

Physical phones, Safari/iOS, spoken VoiceOver/TalkBack, OS text scaling/native zoom and actual device downloads remain **UNVERIFIED**. Annual failure probabilities and constant-annual-risk multi-year conversion remain unvalidated; reach and costs are modeled and routes approximate. Practitioner review remains a later human gate; no outreach was sent or authorized.
