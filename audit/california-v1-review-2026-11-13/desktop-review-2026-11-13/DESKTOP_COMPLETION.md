# Desktop review completed after browser-control retry

All three requested desktop tasks are complete within the agent-operated scope below. Original UI build `efb5e6e0e986` and frozen forecast snapshot `806032f64da1` remain unchanged. No app edit, push, PR, publication, Site upload or outreach occurred.

## Current results

| Task | Result and evidence |
|---|---|
| Budgets, reserve, fixed share and system details | PASS in the visible in-app desktop browser. Default $100M: 20 systems / 171,738 modeled people. Default $500M: 97 / 476,663. Reserve 30%: 112 / 393,742. Fixed share 50%: 54 / 966,559. [Original checks](checks-progress.json). |
| Keyboard navigation and focus return | PASS in the in-app desktop browser: keyboard system activation, heading focus, Tab to Close, Enter to close and focus return to the invoking row with a visible 3px outline; checked in reserve and fixed-share plans. These are agent-driven focus observations, not spoken-AT or user-study evidence. |
| Enlarged browser text | PASS for the observed **native Chrome 200% page zoom** on a maximized desktop window. Browser zoom control explicitly reported 200%. Header, budget controls, totals and live 3D map overlays remained readable and separated. The native $100M button remained operable and showed 20 systems / 171,738 modeled people. [Top](chrome-200-top.png), [map](chrome-200-map.png), [settled native tree](chrome-200-budget-settled.txt). |
| Save and open desktop CSV | PASS. Actual Downloads file `C:\Users\sai71\Downloads\xylem-placement-plan (2).csv` opened in a new Notepad tab. Screenshot shows both metadata and data rows. [Opened file](notepad-csv-open.png), [exact evidence copy](fixed-share-500M.csv). |
| CSV versus exported visible plan | PASS. Fixed share 50% at $500M: 54 systems / 966,559 modeled people / exact modeled cost $493,070,597; matching full UI build, snapshot and scenario. The frozen Python optimizer independently reproduced selected IDs, populations, costs, weights and budget feasibility. [Reconciliation](csv-reconciliation.json). |

The CSV SHA-256 remained `066cc95b176f228ae3892581f27f493cefbf204e2798382b6dfecc219cd95e6b` after opening. No document text was edited. Existing Notepad documents were preserved; the CSV is displayed in its own tab.

Chrome was restored to 100% zoom, its original window size, and the default $500M plan after the native zoom test. The user's separate in-app browser scenario was not changed during this retry. The CSV corresponds to the earlier exported fixed-share scenario, not the restored default scenario.

## Observation limitations preserved

The first native accessibility-tree read after the $100M click preceded the queued redraw. Its assertion returned FAIL even though the screenshot already showed the correct result. A fresh settled native tree confirmed the intended 20 systems / 171,738 people. Both reads remain retained; no app defect was inferred or hidden.

Notepad's body text was not exposed through this UIA capture, so a UIA-only metadata assertion returned FAIL. The current filename, direct screenshot inspection of the actual file, unchanged file hash and prior independent CSV reconciliation establish the file-opening result. This does not establish Notepad screen-reader compatibility. [Native retry receipt and attempts](native-retry-checks.json).

The earlier [desktop review](DESKTOP_REVIEW.md) retains the initial browser-control stop and original incomplete state as history; this completion record supersedes its pending native-zoom/file-opening status.

No 400% native zoom, physical-phone behavior, native phone text scaling/zoom, spoken VoiceOver/TalkBack or actual phone download pass is claimed. Hosted HTTPS exact-build verification and practitioner review remain separate release gates. This is not accessibility certification. Annual failure probabilities and the multi-year conversion remain unvalidated; reach/costs are modeled and routes approximate.
