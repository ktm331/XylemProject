# Project pricing evidence and validation

Reviewed November 18, 2026. Official links and publication dates are embedded in the app's Method tab and system detail cards.

The State Water Board's June 2024 Cost Assessment, Table 8 (page 8), supplies separate long-term solution averages per connection for physical consolidation, centralized and decentralized treatment, new wells, other essential infrastructure, and managerial assistance. These are modeled averages, not construction bids. The app preserves status-specific availability, excludes schools from community rates, allows combined components, and rejects mutually exclusive primary solutions. No inflation to 2026 or statewide rescaling is applied to these rates. The existing 0.5–2× sensitivity range is illustrative and is not an empirically verified prediction interval.

Recent primary sources are preserved in `app/project-examples.js`: Tombstone (2025-05-13), West Goshen and Colfax (2025-06-19), Springfield (2025-05-09), Robbins (2025-08-01). They distinguish total project budgets, shared grants and partial financing. Colfax's reported plant budget is $40M, not its $12.5M financing contribution. Springfield's $15M grant serves multiple communities and cannot be assigned to one system.

## What actually improves

The 2026 saved target list includes Robbins (CA5100107, 87 connections). The official August 2025 announcement identifies an $8M arsenic treatment facility. Its default app cost now uses that published budget rather than the $4,573,049 blended estimate. Absolute disagreement with that budget falls from $3,426,951 to zero **by direct source substitution**. This is not independent validation or evidence of final construction cost accuracy. Remaining funding need is unknown; the app plans total budgets, not net new grant requirements.

Blindly applying the Table 8 treatment rate would give $1,171,194 for Robbins, increasing absolute budget disagreement to $6,828,806. This empirical counterexample prevents making type averages the automatic default. They are explicitly user-selected scope scenarios. Other target systems retain blended estimates until project scope and a comparable cost are identified. Scope scenarios affect actual allocation costs, detail ranges, export labels and shared URLs. Existing frozen stability scores are suppressed because they predate the budget correction; users can rerun current scenarios.

## Verification and limits

`node tests/project-pricing.cjs` checks source substitution and identity matching, unavailable status rates, school exclusions, invalid/alternative scope rejection, additive components and budget compliance at five budgets. Static snapshot verification checks the original saved data remains intact. These are implementation checks, not evidence of general predictive improvement.

A defensible general accuracy claim still requires independently collected contracted/final costs with matching capacity, geography, construction year and scope, and a holdout set not used to select rates. The recent announcements above are insufficient for that claim. Well and decentralized-treatment prices especially need recent comparable contracts before replacing the state benchmarks.

Completed checks: 33 Python pipeline/snapshot/pricing tests passed; the Node pricing checks passed; Chromium verified the $8M default, scope selection, URL reload, reset, and source catalog with no page errors. Static snapshot and build receipt verification passed. Run browser checks with a local server on port 8769 (`python -m http.server 8769 --directory app`), then `node tests/project-pricing-browser.cjs`.
