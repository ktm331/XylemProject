"""The revised curve removes bin cliffs while preserving the state total."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'pipeline'))
from costmodel import fit_curve, TABLES


def test_curve_has_no_size_bin_price_cliffs_and_total_reconciles():
    systems = json.loads((ROOT/'app/data/systems.json').read_text())
    curve = fit_curve([s['conn'] for s in systems], [s['failing'] for s in systems])
    factor = json.loads((ROOT/'app/data/summary.json').read_text())['pricing']['scale_factor']
    for failing in (True, False):
        for boundary in (100, 500, 1000, 3300, 30000):
            left, right = float(curve.cost(boundary, failing)), float(curve.cost(boundary+1, failing))
            assert left <= right
            assert right / left < 1.02
        sizes = np.arange(1, 30002)
        costs = curve.cost(sizes, failing)
        assert np.all(np.diff(costs) >= -1e-7)
        assert np.all(np.diff(curve.per_conn(sizes, failing)) <= 1e-7)
    for s in systems:
        assert s['cost'] == round(float(curve.cost(s['conn'], s['failing'])*factor))
    assert abs(sum(s['cost'] for s in systems)-TABLES['state_total_musd']['total']*1e6) < len(systems)
