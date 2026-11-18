"""Per-system cost model built from the state's published 2024 Cost Assessment averages.

The state does not publish per-system remediation costs. It publishes the average
long-term solution cost per service connection by system size and status (Table 7)
and total cost by county (Table 9). We interpolate size-band averages to remove
artificial discontinuities, then scale and compare against Table 9.
"""
import json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = json.loads((ROOT / "data" / "cost_tables.json").read_text())
_PC = TABLES["per_connection_usd"]
_BINS = _PC["bins"]


def size_bin(connections):
    for i, (lo, hi) in enumerate(_BINS):
        if connections >= lo and (hi is None or connections <= hi):
            return i
    return 0


def per_connection(connections, status):
    key = "failing" if status == "Failing" else "at_risk"
    i = size_bin(connections)
    v = _PC[key][i]
    if v is None:  # state lists N/A for At-Risk above 30,000 connections
        v = _PC["failing"][i]
    return v


def system_cost(connections, status):
    return max(int(connections), 1) * per_connection(max(int(connections), 1), status)


# Smooth the published size-bin averages without applying an unverified
# project-wide inflation or grant-to-cost multiplier.
def _pav(y, w, increasing):
    """Pool-adjacent-violators: the closest monotone sequence to y (weighted least squares)."""
    sign = 1.0 if increasing else -1.0
    out = []
    for v, wt in zip((sign * float(a) for a in y), w):
        out.append([v, float(wt), 1])
        while len(out) > 1 and out[-2][0] > out[-1][0]:      # violation of non-decreasing order (after the sign flip)
            v2, w2, n2 = out.pop()
            v1, w1, n1 = out.pop()
            out.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, n1 + n2])
    res = []
    for v, _, n in out:
        res += [sign * v] * n
    return res


def monotone_knots(x, per_conn, weights):
    """Make the knots obey both rules a cost curve should: cost per connection never rises with size, and a bigger system never costs less in total.
    The state's At-Risk average for the smallest bin ($252,513 a connection) breaks the second rule if used as published."""
    x = [float(v) for v in x]
    v = [float(a) for a in per_conn]
    for _ in range(100):
        v1 = _pav(v, weights, increasing=False)
        total = _pav([a * b for a, b in zip(x, v1)], weights, increasing=True)
        v2 = [t / a for t, a in zip(total, x)]
        if max(abs(a - b) / b for a, b in zip(v2, v)) < 1e-12:
            break
        v = v2
    return v


class Curve:
    """Cost per connection as a smooth non-increasing function of system size, one curve per status."""

    def __init__(self, knots):
        self.knots = knots   # {"failing": {"conn": [...], "per_conn": [...]}, "at_risk": {...}}

    def _one(self, name, x):
        k = self.knots[name]
        return np.exp(np.interp(x, np.log(k["conn"]), np.log(k["per_conn"])))   # clamps outside the end knots

    def per_conn(self, conn, failing):
        x = np.log(np.maximum(np.asarray(conn, float), 1.0))
        return np.where(np.asarray(failing, bool), self._one("failing", x), self._one("at_risk", x))

    def cost(self, conn, failing):
        """Interpolated state-basis cost in 2024 dollars."""
        n = np.maximum(np.asarray(conn, float), 1.0)
        return n * self.per_conn(n, failing)

    def to_json(self):
        return self.knots


def fit_curve(conn, failing):
    """Fit the curve from the target systems' own sizes: a knot at the median size of each Table 7 bin that contains systems."""
    conn = np.asarray(conn, float)
    failing = np.asarray(failing, bool)
    knots = {}
    for name, is_f in (("failing", True), ("at_risk", False)):
        xs, ys, ws = [], [], []
        for i, (lo, hi) in enumerate(_BINS):
            v = _PC[name][i]
            if v is None:
                v = _PC["failing"][i]
            sel = (failing == is_f) & (conn >= lo) & ((conn <= hi) if hi is not None else True)
            if sel.sum() == 0:
                continue
            xs.append(float(np.median(conn[sel])))
            ys.append(float(v))
            ws.append(float(sel.sum()))
        ys = monotone_knots(xs, ys, ws)
        knots[name] = {"conn": xs, "per_conn": [float(v) for v in ys]}
    return Curve(knots)
