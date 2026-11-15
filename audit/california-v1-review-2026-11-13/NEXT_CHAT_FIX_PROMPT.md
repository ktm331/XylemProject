# Continue Xylem: fix the actionable issues locally, then finish the submission

The user wants the issues we can address now fixed, and a simple step-by-step explanation of everything still required. Read this complete handoff and the linked evidence before acting. Do the authorized local work; do not stop at another plan merely because deployment or human testing is blocked. Preserve existing work and all original evidence.

## 1. Read these first

Evidence root (all relative paths below refer to this directory):

`C:\Users\sai71\.codex\visualizations\2026\11\13\01a1d377-9c26-7a73-b228-eb550dde3ef9\california-v1-release`

Read completely:

1. [HACKATHON_ASSESSMENT.md](HACKATHON_ASSESSMENT.md) — assessment, known limitations and 12 remaining steps.
2. [PRIVATE_PREVIEW_STATUS.md](PRIVATE_PREVIEW_STATUS.md) — current private hosting, approvals, exact-byte failure, browser results and human gates.
3. [project-review-profile.json](project-review-profile.json), [observed incorrect card](project-review-bad-name.png), [observed accessibility tree](project-review-bad-name-ax.txt) — the newly confirmed identity defect.
4. [desktop completion](desktop-review-2026-11-13/DESKTOP_COMPLETION.md), [hosted browser receipt](private-sites-browser-smoke.json), [hosted CSV reconciliation](private-sites-hosted-csv-reconciliation.json).
5. [PREPARED_RELEASE.md](PREPARED_RELEASE.md), [publishing approval](publishing-approval.json), [private approval](private-sites-approval.json), [exact-byte decision](private-sites-exact-byte-decision.json).
6. Candidate `SETUP.md`, `README.md`, `GRADING.md`, `PLANNER_EVALUATION.md`, `NOVELTY.md`, `audit/ACCESSIBILITY_REPAIRS.md`, `audit/DEMO_REVIEW.md`, `audit/PHONE_TEST.md`, `audit/APP_REFRESH_REPORT.md` and relevant integrity/provenance tools before editing or refreshing receipts.

The earlier complete historical handoff is:

`C:\Users\sai71\.codex\visualizations\2026\11\12\01a1ceb1-04db-7401-8063-6ff21bd35b5f\NEXT_CHAT_PROMPT.md`

Historical documents contain superseded authorization and deployment statements. This handoff and the explicit continuing user decisions take precedence.

## 2. Baseline to preserve

- Original repository: https://github.com/palashraks-afk/XylemProject
- Latest main verified during the November 13 Pacific assessment: `2ce2832ffc2be043da6dc194c025d6abdbaf13a1`. Recheck remote main before acting; inspect any newer changes instead of silently using them.
- Parent: `f0fa6006032f6b614276395c5628596a63b966fa`.
- Clean detached candidate: `candidate/` under the evidence root. Do not modify this baseline. Create a new isolated checkout/branch in the new chat's writable workspace.
- Original UI build: `efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b`.
- Frozen forecast snapshot: `806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd`.
- Leave `C:\Users\sai71\XylemEvaluation` and `C:\Users\sai71\XylemProject` untouched. Inspect applicable AGENTS.md and workspace permissions first.
- The OneDrive workspace rejected writes earlier. Use the new chat's permitted artifact/workspace directory when needed; do not assume old artifact directories are writable.

An existing independent Python environment, to run without modifying/reinstalling it, is:

`C:\Users\sai71\.codex\visualizations\2026\11\12\01a1ce77-724c-75d3-8916-457d3d586b04\release-work\independent-env\Scripts\python.exe`

Do not retrain models, rerun data-fetch scripts, redownload inputs, change model selection/calibration, alter scientific expectations or rewrite old receipts to make checks pass. Keep `app/data`, `data`, `pipeline`, vendor assets and the manual Pages workflow frozen for this presentation repair. The intended repair changes presentation, not numerical data/results.

## 3. Fix the confirmed issue now

**CA5610029 is incorrectly named `10/30/2026`.** It is in the default $500M selected plan and appears with that date in the table, detail card and CSV. The state identifies the same ID as **Vineyard Avenue Acres MWC**, Ventura County, with 1,820 people served and 336 connections.

Primary identity evidence, read November 13 Pacific:

https://sdwis.waterboards.ca.gov/PDWW/JSP/WaterSystemDetail.jsp?tinwsys_is_number=6171&tinwsys_st_code=CA&wsnumber=CA5610029

Recheck that primary record and inspect local provenance before applying a correction. `pipeline/build.py` passes `row.SYSTEM_NAME.title()` through to app output; the initial corruption's cause is unresolved. Do not guess a cause or rebuild the pipeline.

Prepare a small, documented presentation-only correction keyed by the stable PWSID. Prefer a central sourced display-name alias shared by the card, table, search, maps/popups and CSV, so all surfaces agree. Preserve the original source value and explanation in provenance/audit evidence. Do not alter the frozen `app/data/systems.json` or any forecast/cost/population input. A named constant/helper or alias layer outside frozen data can make the distinction clear. Choose the simplest implementation that achieves this consistently.

After implementation:

1. Verify the correct name appears in the table, detail card, search/datalist, applicable 2D/3D displays and a real downloaded CSV. Verify ID search and name search with supported UI interactions.
2. Verify other systems retain their names and that the selected IDs, populations, costs, allocation weights and stability values are unchanged.
3. Verify default $100M and $500M and the reserve/fixed-share examples below. A corrected CSV name may change CSV bytes; numerical rows and scenario semantics must not change.
4. Refresh the UI presentation build deliberately using the existing receipt workflow (`tools/presentation_build.py --write` after reviewing UI changes). Record the new UI build while preserving the exact same forecast snapshot. Review all dependent presentation-provenance checks; never blindly replace scientific hashes or loosen guards.
5. Run focused meaningful regression checks plus required repository checks. Reuse established unchanged evidence instead of repeatedly running every old passing suite. Preserve before/after evidence, exact diffs and any failed attempts.
6. Produce a concrete local reviewable candidate, with changed files, new build ID, tests/results, unchanged model/data hashes and remaining limitations. Local commits are acceptable when permitted; no remote push or deployment of this repaired candidate is authorized yet.

Known frozen expectations:

| Controls | Systems | Modeled people | Exact modeled cost |
|---|---:|---:|---:|
| Defaults, $100M | 20 | 171,738 | Check existing frozen evidence |
| Defaults, $500M | 97 | 476,663 | $487,919,470 |
| $500M, reserve 30%, other defaults | 112 | 393,742 | $486,059,328 |
| $500M, fixed share 50%, reserve 0%, other defaults | 54 | 966,559 | $493,070,597 |

The read-only full scan found 1,062 unique IDs; no duplicate name/county labels, missing/zero coordinates, missing At-Risk forecasts or nonpositive population/connection values. Only one date-shaped name was found. This is not proof that every source field is valid.

## 4. Useful work that can proceed without publication

- Prepare a simple submission draft: intended user, one funding decision, honest benefits, differentiating workflow, realistic pilot and known limitations.
- Draft a 3–4 minute video script and concise slide outline using the actual demo and frozen numbers. Do not invent team identities, interviews, endorsements, adoption, measured benefit or results.
- Suggest distinct project-name options because the current title is also the sponsor's name. Do not silently rebrand the app or expand the repair into a redesign; get the user's choice if an actual rename is desired.
- Prepare a short practitioner test sheet and an unsent outreach draft if useful. Do not send messages, invite viewers or quote anyone without the necessary user instruction/permission.
- Clarify the tested difference from official SAFER dashboards and a simple spreadsheet workflow using primary sources. Avoid unsupported claims that competitors lack a feature or that Xylem is first-of-kind.
- Keep the work focused. New model families, more geography, extra map layers and model retraining are outside this release pass.

The assessment's optional HTML report builder failed on Windows with `Invalid prebuilt source path: assets\\visualize-data\\assets\\cdn.json`. Its source is retained in `hackathon-review/`; the completed readable assessment is `HACKATHON_ASSESSMENT.md`. This is a report-tool problem, not an Xylem app defect. Do not spend the repair task modifying protected plugin/runtime code or weakening its validation. Plain Markdown drafts are sufficient here.

## 5. Approvals and hosting — retain the exact decisions

The user explicitly approved enabling public Pages and deploying **commit 2ce2832**. Do not ask for that same approval again. The current connected GitHub account had push permission but no admin/maintain permission. The user said they are not the owner. Pages enablement still needs an existing repository admin/maintainer; operating the user's computer does not confer that permission.

The admin setup is Settings → Pages → Build and deployment → Source → GitHub Actions:

https://github.com/palashraks-afk/XylemProject/settings/pages

Keep `.github/workflows/pages.yml` manual-only (`workflow_dispatch`), using the existing workflow and app-only upload. Do not broaden account access or change security/firewall settings. If the selected release is repaired, the old commit-specific approval does not cover its new SHA: finish the repair and verification first, then present the exact new candidate and ask for specific push/deployment approval only as the final step.

The user also explicitly approved a private Sites preview. It is already published; do not recreate or republish it during local repairs:

https://xylem-california-v1-efb5e6e0e986.srpatlola2020.chatgpt.site

- Project: `appgprj_6af7df45649c81918b43785b33a7c926`.
- Saved version: `appgprj_6af7df45649c81918b43785b33a7c926~appgver_8b04f1f526a4819191696c2d8d1c5754`.
- Deployment: `appgdep_6af7e0d467dc81919a6c6274c31a2e94`, succeeded.
- Sites source commit: `6f0cd6f96abcc6d8e10605641e4db24666b57912`.
- Audience: current owner only, one allowed user, zero groups. Preserve it.

All 24 source/archive app files match the original candidate. Over HTTPS, all 23 non-HTML app files matched. Served HTML contains the unchanged original 8,903 bytes plus a 1,114-byte Cloudflare verification script. **Strict served-HTML check FAIL.** The user was offered a documented exception and explicitly chose **“Keep the exact-byte requirement.”** The exception is DECLINED, not pending. Do not ask again, relabel the mismatch PASS, strip it during verification or suppress hosting security to make the receipt pass. This private URL is not a verified release/phone-testing build.

Existing supported service access from Sites `get_site` may be used only for that same Site's authorized reads. Never generate/rotate bypass tokens to fix access; never put tokens in URLs, files, output or shell arguments. User sign-in is a user action; do not automate authentication dialogs. Reobserve browser inventory because tabs/IDs and sessions may have changed.

## 6. Completed checks are not human testing

The three requested local desktop tasks are complete: budgets/reserve/fixed share/details, keyboard focus return and native Chrome 200% zoom, and saving/opening the fixed-share CSV in Notepad. Their evidence is in `desktop-review-2026-11-13/`.

Hosted agent-operated desktop checks also passed expected build/snapshot loading, live 3D, $100M/$500M defaults and a real desktop CSV reconciled with the frozen Python optimizer. The hosted CSV was read for reconciliation; its opening in a native application was not performed. The earlier local CSV was opened in Notepad. Do not conflate these files or checks.

The browser-control read-only scope did not expose `isSecureContext` or `crypto.subtle`. Direct confirmation remains UNVERIFIED. Successful application initialization supports the inference that the app's real SHA-256 snapshot path completed; it is not a direct security-global probe. Initial failed proxy assertions and corrected scoped receipts remain preserved. Do not invent a browser defect or a direct PASS from an undefined proxy value.

All physical-phone, native phone text/zoom, spoken VoiceOver/TalkBack and actual phone save/open checks remain **UNVERIFIED**. Browser automation and screenshots do not replace them. Use `PHONE_OBSERVATIONS.md` and `candidate/audit/PHONE_TEST.md`, updating expected UI build only after a deliberate reviewed repair. The forecast snapshot and modeled expectations should remain unchanged.

## 7. Explain everything left simply, with who does it

Give the user one ordered list in plain language. Distinguish completed local repairs, external admin actions, approvals and actual human observations. Recommended sequence:

1. **Assistant:** finish the local name repair, focused checks and reviewable evidence; prepare the draft story/script/slide outline.
2. **User:** confirm the school track, chosen challenge, team registration and eligibility. Choose a new product name only if desired.
3. **User and assistant:** review the exact repaired build. Obtain any new commit-specific push/deployment authorization after the result is concrete. Do not ask again for old 2ce2832 approval.
4. **Existing repo admin/maintainer:** enable GitHub Actions as the Pages source. No new automatic deployment triggers.
5. **Assistant, within the selected build's authority:** manually deploy, verify source/run identity, every asset in the selected UI build receipt over HTTPS, browser loading and a real CSV. The original candidate has 24 app files; if a deliberate repair adds an asset, document and verify the expanded set too. Keep failures recorded.
6. **User/human tester, guided by assistant:** test actual phones, enlarged text/orientation, controls, focus, speech and real saved/opened files. One platform does not cover another.
7. **User-approved practitioner reviewer:** try one real planning task and provide critical feedback. Assistant can draft the request but must not send it without explicit authorization.
8. **Assistant with user facts:** finalize the distinction from existing tools, intended adopter, pilot plan, slides and short script. Keep all scientific limitations honest.
9. **User:** record the final presentation/demo. Assistant can guide timing, captions and link checks.
10. **User and assistant:** check approved demo, slides and video access while signed out; retain a recorded fallback for network/map failure.
11. **User:** publish the completed competition project page with the intended materials and required disclosures. App publishing is not competition submission; a saved draft is not submitted.
12. **User/assistant using authorized reads:** verify published/submitted status and every attachment; save the receipt and final build identity.

Some steps can run in parallel. Do not make practitioner scheduling or slide drafting wait unnecessarily for Pages. Do not claim phone-release verification while the exact hosted-byte gate remains blocked.

## 8. Event facts and limits

Reviewed event: **2026 Xylem Global Student Innovation Challenge**. Public deadline: **Friday, November 20, 2026, 1:00 PM Pacific**. Target November 19 completion for a buffer. Recheck current rules if this handoff is used later.

Public primary sources:

- Event and criteria: https://xyleminnovationchallenge.bemyapp.com/
- Rules: https://docs.google.com/document/d/e/2PACX-1vQrUoJgv3RBA3b3oWcrYhFzOf51Yke2DWjTalpDUpLfHjiVTAkSJvk4Y6cmcocOSBq_d0YLYy9-n1gx/pub
- Event platform: https://xyleminnovationchallenge-platform.bemyapp.com/

The rules call for slides and a 3–4 minute presentation/demo, team/category/challenge identification and outside-assistance disclosure. The old saved walkthrough is five minutes and is not the final compliant video. The event platform says the project must be published to count as submitted. The full challenge cards were sign-in gated; the user's actual track, eligibility, project page and final materials were not inspected. No AI-specific permission policy was established; do not invent one.

The assessment is qualitative: a credible prototype and plausible prize case, with weak practitioner/adoption evidence and unproven novelty. No defensible win percentage, official score, measured intervention benefit or prospective annual-risk accuracy is established. Water Access is the recommended fit, not proof of the user's selected category.

## 9. What not to promise or attempt now

Annual failure probabilities and `1-(1-p)^h` remain unvalidated. Historical release vintages, complete failure episodes, prospective outcomes, actual project quotes, consent/capacity and person-level overlap need external evidence. More UI code cannot supply them. Keep these as explicit limits and longer-term pilot/research work; do not retrain or change expected results to improve the pitch.

No new remote push, PR, repaired-build deployment, Site sharing change, practitioner outreach, competition submission or public quotation is authorized merely by this handoff. Prepare and verify local fixes and drafts first. End with what changed, the meaningful checks performed, what remains blocked, and the user's next concrete action—using simple language, not a repeated broad plan or fabricated completion percentage.
