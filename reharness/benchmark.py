# -*- coding: utf-8 -*-
"""Reusable benchmark driver (skill scan + two-level recursion)."""
from __future__ import annotations

from .config import DEFAULTS, deep_merge
from .optimizer.ppc import PPC
from .optimizer.recursive import recursive_optimize, flat_optimize
from .scoring.metrics import summarize, recursion_gain

SKILLS = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def run_bench(cfg: dict | None = None) -> dict:
    cfg = deep_merge(DEFAULTS, cfg or {})
    ppc = PPC(cfg)
    results = {s: ppc.run(s) for s in SKILLS}
    rec = {s: recursive_optimize(ppc, s) for s in (0.5, 1.0)}
    flat = {s: flat_optimize(ppc, s) for s in (0.5, 1.0)}
    rg = {s: recursion_gain(rec[s], flat[s]) for s in (0.5, 1.0)}
    return {
        "summary": summarize(results),
        "results": results,
        "recursion": {"recursive": {s: rec[s]["success_rate"] for s in (0.5, 1.0)},
                      "flat": {s: flat[s]["success_rate"] for s in (0.5, 1.0)},
                      "gain": rg,
                      "meta_selected": {s: rec[s]["meta_selected"] for s in (0.5, 1.0)}},
    }
