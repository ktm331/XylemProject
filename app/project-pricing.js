/* Published solution averages are scope benchmarks, in source-year dollars. */
(function (root) {
  const source = "https://www.waterboards.ca.gov/drinking_water/certlic/drinkingwater/documents/needs/2024/2024costassessment.pdf";
  const types = [
    {id: "consolidation", name: "Physical consolidation", failing: 93091, at_risk: 188175},
    {id: "centralized", name: "Centralized treatment", failing: 13462, at_risk: null},
    {id: "decentralized", name: "Decentralized treatment", failing: 4734, at_risk: null},
    {id: "well", name: "New well", failing: 73910, at_risk: 167024},
    {id: "oei", name: "Other essential infrastructure", failing: 13487, at_risk: 15963},
    {id: "management", name: "Managerial assistance", failing: 18834, at_risk: 17232}
  ];
  function estimate(system, ids) {
    if (!Array.isArray(ids) || !ids.length) return null;
    // K-12 averages use a different population; no silent community-rate substitution.
    if (/school|elementary|high school|academy/i.test(system.name)) return null;
    const n = Number(system.conn);
    if (!Number.isFinite(n) || n <= 0) return null;
    const selected = [...new Set(ids)].map(id => types.find(t => t.id === id));
    if (selected.some(t => !t || t[system.failing ? "failing" : "at_risk"] == null)) return null;
    // Consolidation and stand-alone treatment are alternative primary solutions.
    if (selected.filter(t => ["consolidation", "centralized", "decentralized"].includes(t.id)).length > 1) return null;
    return {cost: Math.round(n * selected.reduce((v, t) => v + t[system.failing ? "failing" : "at_risk"], 0)),
      label: selected.map(t => t.name).join(" + "), year: 2024, source};
  }
  const known = {
    CA5100107: {namePattern: /robbins/i, cost: 8000000, label: "Robbins arsenic treatment facility", year: 2025,
      kind: "Published grant-funded facility budget; remaining funding need unknown",
      source: "https://water.waterboards.ca.gov/press_room/press_releases/2025/pr20250801-SAFER-progress.html"}
  };
  function verified(system) {
    const p = known[system.id];
    return p && p.namePattern.test(system.name) ? p : null;
  }
  root.XylemPricing = {source, types, estimate, verified};
  if (typeof module !== "undefined") module.exports = root.XylemPricing;
})(typeof window === "undefined" ? globalThis : window);
