"""Refresh capital planning costs on a verified saved forecast, without retraining it.

Run from the repository root: python pipeline/refresh_pricing.py
Checks the complete existing snapshot before writing; recomputes costs, default
plans, county totals and all 200 stored sensitivity scenarios. Does not fetch data.
The frozen forecast retains its original provenance and limitations.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr, pearsonr

from costmodel import ROOT, TABLES, fit_curve
from optimizer import optimize, greedy_by_population

OUT = ROOT / "app/data"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pricing_summary(systems, curve, factor):
    return {"method": "Smooth 2024 Table 7 size curves, scaled to the published 2024 statewide total",
            "costmodel_sha256": digest(ROOT/"pipeline/costmodel.py"),
            "curve_knots": curve.to_json(), "scale_factor": factor,
            "source_year": 2024,
            "note": "No price escalation or project-award multiplier. Published grants have mixed scopes and are not final costs. The 0.5x–2x range is illustrative, not a calibrated confidence interval."}


def reprice(systems, summary):
    curve = fit_curve([s["conn"] for s in systems], [s["failing"] for s in systems])
    raw = curve.cost([s["conn"] for s in systems], [s["failing"] for s in systems])
    factor = TABLES["state_total_musd"]["total"] * 1e6 / sum(raw)
    for s, average in zip(systems, raw):
        s["cost"] = round(float(average * factor))
        s["lo"], s["hi"] = round(s["cost"] * .5), round(s["cost"] * 2)
    costs = np.array([s["cost"] for s in systems], dtype=float)
    pops = np.array([s["pop"] for s in systems])
    conns = [s["conn"] for s in systems]
    failing = np.array([s["failing"] for s in systems])
    eq = np.array([np.mean([v for v in s["eq"] if v is not None])
                   if any(v is not None for v in s["eq"]) else np.nan for s in systems])
    eq = np.where(np.isnan(eq), np.nanmedian(eq), eq)
    pf = np.array([0 if s["failing"] else s["pf"] for s in systems])
    def benefit(lam, horizon):
        return pops * np.where(failing, 1., 1-(1-pf)**horizon) * (1+lam*eq)
    defaults = summary["defaults"]
    ben = benefit(defaults["lambda_eq"], defaults["horizon_years"])
    def describe(chosen):
        return {"systems": len(chosen), "people": int(pops[chosen].sum()),
                "spent_musd": round(float(costs[chosen].sum()/1e6), 1),
                "dac_people": int(sum(pops[i] for i in chosen if (systems[i]["eq"][0] or 0) > 0)),
                "small_systems": sum(conns[i] <= 500 for i in chosen)}
    # Retain the established comparison schema.
    comparison = []
    for budget in summary["budgets_musd"]:
        opt = describe(optimize(costs, ben, conns, budget*1e6))
        base = describe(greedy_by_population(costs, pops, failing, budget*1e6))
        comparison.append({"budget_musd": budget, "optimizer": opt,
                           "status_first_baseline": base})
    # Same empirical county draws and seed as build.py, using the legacy fallback.
    county_raw = {}
    for s, cost in zip(systems, raw):
        county_raw[s["county"]] = county_raw.get(s["county"], 0.) + cost*factor/1e6
    official = np.array([sum(v) for v in TABLES["county_totals_musd"].values()])
    modeled = np.array([county_raw.get(c, 0.) for c in TABLES["county_totals_musd"]])
    large = (official >= 10) & (modeled > 0)
    summary["calibration"] = {
        "raw_total_musd": round(float(sum(raw)/1e6), 1),
        "official_total_musd": TABLES["state_total_musd"]["total"],
        "scale_factor": round(float(factor), 4),
        "counties_compared": len(official),
        "spearman_county": round(float(spearmanr(official, modeled)[0]), 3),
        "pearson_county": round(float(pearsonr(official, modeled)[0]), 3),
        "log_ratio_sd_county": round(float(np.log(official[large]/modeled[large]).std(ddof=1)), 3),
        "median_abs_pct_error_county_ge10M": round(float(np.median(np.abs(modeled[large]/official[large]-1))*100), 1),
        "note": "County comparison of the smoothed Table 7 model against historic 2024 totals; this is not project-level price validation."}
    lr = np.array([np.log(sum(v)/county_raw[c]) for c, v in TABLES["county_totals_musd"].items()
                   if sum(v) >= 10 and county_raw.get(c, 0) > 0])
    counties = sorted({s["county"] for s in systems})
    cidx = [counties.index(s["county"]) for s in systems]
    rng = np.random.default_rng(summary["stress_settings"]["seed"])
    hits = {b: np.zeros(len(systems)) for b in summary["budgets_musd"]}
    sigma = float(np.log(2)/1.645)
    for k in range(summary["n_scenarios"]):
        cm = np.exp(rng.choice(lr-lr.mean(), size=len(counties)))[cidx]
        sm = np.exp(rng.normal(0, sigma, size=len(systems)))
        mult = np.clip(cm*sm, .2, 5.)
        b = benefit(rng.uniform(0, 2), rng.uniform(1, 10))
        for budget in hits:
            hits[budget][optimize(costs*mult, b, conns, budget*1e6)] += 1
        if k % 50 == 0:
            print("Pricing scenarios", k, flush=True)
    for i, s in enumerate(systems):
        s["p"] = [round(float(hits[b][i]/summary["n_scenarios"]), 2) for b in hits]
    summary["comparison"] = comparison
    summary["total_modelled_cost_musd"] = round(float(costs.sum()/1e6), 1)
    for county in summary["county"]:
        county["cost_musd"] = round(sum(s["cost"] for s in systems if s["county"] == county["county"])/1e6, 1)
    funded = np.array([s["funded17"] for s in systems])
    ranks = rankdata(ben/costs)
    n1, n0 = funded.sum(), (~funded).sum()
    summary["validation"]["auc_efficiency_vs_funded"] = round(float((ranks[funded].sum()-n1*(n1+1)/2)/(n1*n0)), 3)
    summary["pricing"] = pricing_summary(systems, curve, factor)
    return systems, summary


def main():
    manifest = json.loads((OUT/"snapshot.json").read_text())
    for name, expected in manifest["sha256"].items():
        if digest(OUT/name) != expected:
            raise ValueError("Mixed input snapshot: " + name)
    if manifest["id"] != hashlib.sha256(json.dumps(manifest["sha256"], sort_keys=True).encode()).hexdigest():
        raise ValueError("Invalid input snapshot manifest")
    systems = json.loads((OUT/"systems.json").read_text())
    summary = json.loads((OUT/"summary.json").read_text())
    if summary["forecast_sha256"] != digest(OUT/"forecast.json"):
        raise ValueError("Plans and saved forecast differ")
    systems, summary = reprice(systems, summary)
    (OUT/"systems.json").write_text(json.dumps(systems, separators=(",", ":"))+"\n")
    (OUT/"summary.json").write_text(json.dumps(summary, indent=1)+"\n", newline="\r\n")
    # Forecast, GIS, routes and population inputs stay frozen; reseal changed data.
    hashes = {p.name: digest(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name != "snapshot.json"}
    manifest["sha256"] = hashes
    manifest["id"] = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    manifest["pricing_provenance"] = summary["pricing"]
    (OUT/"snapshot.json").write_text(json.dumps(manifest, indent=2)+"\n", newline="\r\n")
    # Keep the tabular export consistent with the costs consumed by the browser.
    import csv
    path = ROOT/"data/ranked_systems.csv"
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    by_id = {s["id"]: s["cost"] for s in systems}
    for row in rows:
        row["cost"] = str(float(by_id[row["WATER_SYSTEM_NUMBER"]]))
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary["pricing"], indent=2))


if __name__ == "__main__":
    main()
