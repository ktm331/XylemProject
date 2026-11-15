# Desktop walkthrough — November 13, 2026 Pacific

**Completion update:** The user requested a browser-control retry. Native Chrome 200% zoom and opening the actual CSV in Notepad have now been completed. See [current desktop completion](DESKTOP_COMPLETION.md) and [native retry receipt](native-retry-checks.json). The initially incomplete observations below are retained as history.

This is an agent-operated visible desktop review of the exact local candidate. No physical-phone or spoken-screen-reader pass is claimed.

## Push check, performed first

GitHub `main` remains `2ce2832ffc2be043da6dc194c025d6abdbaf13a1` (Repair California v1 accessibility interactions and verification). There are no newer commits on main relative to the handoff. Other branches are outside this statement. See [remote receipt](remote-main-check.json). No application change or push occurred during this walkthrough.

## Completed checks

The active in-app desktop browser showed UI build `efb5e6e0e986` and snapshot `806032f64da1`. The loopback address is http://127.0.0.1:8891/. Preset buttons and actual keyboard range input were used; no control values were changed by injected DOM mutation.

| Settings | Expected and observed systems | Expected and observed modeled people | Result |
|---|---:|---:|---|
| Default $100M | 20 | 171,738 | PASS |
| Default $500M | 97 | 476,663 | PASS |
| $500M, reserve 30%, other defaults | 112, including 70 small systems | 393,742 | PASS |
| $500M, fixed share 50%, reserve 0%, other defaults | 54 | 966,559 | PASS |

Reserve reached 30% through Home and six ArrowRight key presses, and retained focus at the slider. Incompatible stored stability was shown as unavailable for reserve/fixed-share alternatives.

Lemoore (`CA1610005`) opened by keyboard activation from its table button. Initial focus moved to its heading; Tab reached Close; Enter closed the card and returned focus to the invoking system button with a visible 3px outline. Details showed the selected system and current-plan stability availability. The fixed-share system Monterey Park (`CA1910092`) also opened with heading focus and returned to its own table button on keyboard close. These are agent-driven focus/DOM observations in the desktop in-app browser, not human or spoken-AT findings. See [raw checks](checks-progress.json).

## Real desktop download and independent reconciliation

The browser downloaded a real file to `C:\Users\sai71\Downloads\xylem-placement-plan (2).csv`. An exact evidence copy is [fixed-share-500M.csv](fixed-share-500M.csv). It matches the fixed-share plan left visible in the in-app browser:

- Budget $500,000,000; 54 systems; 966,559 modeled people; exact modeled cost $493,070,597 (screen rounds to $493M).
- Fixed At-Risk share 50%, equity 1, reserve 0%, routes off, cost multiplier 1.
- Full UI build `efb5e6e0e986178bef4bb6c9d3810854623d0c8947d3ecb631c80accda6c7a1b` and forecast snapshot `806032f64da14561b81c55e72179ec22f299774fa97b9b5f08c4742909f9c0bd`.
- All selected IDs, per-system populations/costs/allocation weights, total population/cost, scenario metadata, blank incompatible stability and rounded-budget feasibility independently reproduced by the frozen Python optimizer. Monterey Park's ID is in the export.

CSV SHA-256: `066cc95b176f228ae3892581f27f493cefbf204e2798382b6dfecc219cd95e6b`. [Reconciliation](csv-reconciliation.json) is PASS. The first verifier attempt stopped at an integer-versus-float string formatting assertion in the checker; its explanation is preserved in [initial attempt](csv-verifier-initial-attempt.txt). Numeric comparison corrected that checker; no app, CSV or expected scientific result changed.

**Opening this CSV in a desktop viewer remains UNVERIFIED.** Saving, reading and independently parsing the real file passed; a native viewer was not opened before computer use was stopped. The user can open the linked CSV to complete that observation.

## Uncompleted native browser checks

A separate desktop Chrome window was selected for actual browser zoom. Native input initially failed because the foreground process was unavailable; one recovery selected a fresh New Tab window. After observing focus, typing the loopback URL succeeded. The subsequent Enter attempt stopped Computer Use because the active Windows browser URL could not be established confidently. No further UI actions were issued.

**Native browser zoom/enlarged text is UNVERIFIED.** No 200% or 400% native page-zoom pass is claimed. Earlier responsive emulation is not being relabeled as native zoom. Native Chrome keyboard navigation is also not passed by this attempt; the completed keyboard/focus results above belong to the in-app desktop browser.

To finish: open the local preview in desktop Chrome, enlarge browser page zoom to 200% (optionally 400%), and observe whether labels, buttons, totals, details and map overlays remain readable and operable. Record actual percentage, viewport/window size, settings and any cut-off/overlap. Open the CSV in a viewer and confirm its comment header and rows are readable. The currently visible fixed-share plan should show 54 systems / 966,559 modeled people / $493M rounded cost. Human observations remain pending until supplied.

Original model/data/scoring files, manual-only Pages and prior evidence remain preserved. No deployment, Site upload, PR or outreach occurred. Physical phones, VoiceOver/TalkBack speech, native phone text scaling/zoom and actual phone downloads remain UNVERIFIED.
