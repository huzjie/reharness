# -*- coding: utf-8 -*-
"""Benchmark metrics. All must be monotonic in skill (asserted in `bench`)."""
from __future__ import annotations

from ..world.oracle import REQUIRED


def component_recall(selected: list, required=None) -> float:
    """Fraction of the globally-required components the optimizer recovered."""
    req = set(required if required is not None else REQUIRED)
    if not req:
        return 1.0
    return len(set(selected) & req) / len(req)


def contrastive_gain(result: dict) -> float:
    """Contrastive-composed success minus a pure-noise (random) selection.

    At skill=0.5 the composed harness equals the random baseline (boost=0), so
    gain is exactly 0; at skill=1.0 the contrastive signal recovers the optimal
    set, so gain is large and positive."""
    return result["success_rate"] - result["random_sr"]


def recursion_gain(recursive_result: dict, flat_result: dict) -> float:
    """Two-level optimizer success minus the flat (suboptimal-config) optimizer."""
    return recursive_result["success_rate"] - flat_result["success_rate"]


def _monotonic(values, name, direction):
    """direction: +1 ascending, -1 descending."""
    ok = True
    for a, b in zip(values, values[1:]):
        if direction == 1 and b < a:
            ok = False
        if direction == -1 and b > a:
            ok = False
    return ok


def summarize(results: dict) -> dict:
    """results: {skill: result_dict}. Returns per-metric monotonicity + endpoints."""
    skills = sorted(results.keys())
    keys = ["success_rate", "component_recall", "contrastive_gain"]
    summary = {"skills": skills}
    for k in keys:
        vals = [results[s][k] for s in skills]
        summary[k] = {"start": vals[0], "end": vals[-1],
                      "monotonic": _monotonic(vals, k, 1)}
    gv = [results[s]["guardrail_violations"] for s in skills]
    summary["guardrail_violations"] = {"start": gv[0], "end": gv[-1],
                                       "monotonic": _monotonic(gv, "gv", -1)}
    return summary
