# Owner-independent HTTPS review — local preparation

**Current update:** The approved private Site is published and its hosted desktop plans/CSV were checked. The user declined the host-added HTML exception and retained the exact-byte requirement, so this route remains blocked as a verified phone-testing build. Use [PRIVATE_PREVIEW_STATUS.md](PRIVATE_PREVIEW_STATUS.md) for current results and remaining gates. The preparation proposal below is history; its authorization-pending statements are superseded by private-sites-approval.json.

The user confirmed they are not the GitHub repository owner. Their current account cannot access the repository's Pages settings. The existing public Pages approval for `palashraks-afk/XylemProject` and commit `2ce2832ffc2be043da6dc194c025d6abdbaf13a1` remains recorded; repository Pages enablement requires an existing admin or maintainer. No access expansion or owner-account sign-in should be assumed.

## Concrete alternative awaiting authorization

Create a **new private Site through Sites in the current user's workspace**, and upload/publish only the reviewed static app and the minimal hosting/source metadata needed by Sites. The proposed slug is `xylem-california-v1-efb5e6e0e986`; availability and the actual HTTPS URL will be determined by registration after approval. No Site identity or URL has been invented or registered. This separate host is not covered by the original repository Pages approval.

The prepared static directory is `sites-preview/dist/`. It contains exactly the 24 reviewed app files, including `build.json`. No UI edits, source acquisition, raw-input archives, Python environments, model-training artifacts or audit recordings are included. Sites requires source synchronization to its own private source repository; this does not involve a push to the original GitHub repository. No source has been uploaded yet.

UI build: `efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b`. Forecast snapshot: `806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd`. See [exact-byte preparation receipt](alternative-preview-preparation.json).

A private Site uses the user's ChatGPT sign-in. The physical phone will need to sign in to that same account. Do not promise an anonymous public testing link or practitioner access. Preserve the private audience; making it public needs explicit authorization.

## After explicit approval

1. Reuse this prepared directory. Confirm no `.openai/hosting.json` identity already exists before creating a Site; register only once and immediately persist the returned project ID. Keep credentials in memory and pass them through stdin as required by the Sites skill.
2. Add only the required hosting configuration outside `dist/`. Preserve and recheck all 24 app bytes. Use the Sites source helper to synchronize the exact static source and package it without a model build or data download.
3. Publish through the supported owner-private Sites operation. Record the actual HTTPS URL, source/version and deployment identity. A native deployment success is not sufficient for this task's exact-hosted-build gate.
4. Verify HTTPS receipt and all 23 asset hashes against the reviewed candidate in an authorized authenticated context, plus the secure-context/crypto, snapshot, default plans and desktop CSV checks. Do not bypass the private sign-in gate, extract browser credentials, generate a bypass token without an explicit user request or claim same-build verification from local hashes alone. If authenticated exact-byte retrieval is unavailable, report that limitation and do not present the link as verified for phone testing.
5. Once those gates pass, guide [PHONE_TEST.md](../../audit/PHONE_TEST.md) and record observations in [PHONE_OBSERVATIONS.md](PHONE_OBSERVATIONS.md). Physical phone, native text/zoom, spoken VoiceOver/TalkBack and actual device downloads remain UNVERIFIED until observed.

## Other work that can proceed without publication

The complete static package, release checks, human walkthrough and platform-specific log are already prepared. Local desktop review can be guided without the repository owner, but it does not establish physical-phone or spoken mobile-AT support. Additional code changes or repeated passing test suites will not resolve the owner permission or human-observation gates.

The repository owner can alternatively perform the single Pages source selection in [Settings → Pages](https://github.com/palashraks-afk/XylemProject/settings/pages): **Source → GitHub Actions**, preserving the existing manual workflow. GitHub's [publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) specifies the required admin/maintainer role. Any owner contact remains a draft unless the user explicitly authorizes sending it.
