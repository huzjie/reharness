# -*- coding: utf-8 -*-
"""Contrastive statistics over traces (evidence-only, no labels).

The core idea: for each component id, contrast how often the agent *solved*
tasks when that component was present vs. absent. A component that reliably
co-occurs with success has a positive "lift"; one that co-occurs with failure
has a negative lift. This is the Harness2 "contrastive" signal -- it is derived
purely from execution traces, never from ground-truth labels.
"""
from __future__ import annotations


def _rates(pres_solved, pres_total, abs_solved, abs_total):
    out = {}
    for cid in pres_total:
        pr = pres_solved.get(cid, 0) / pres_total[cid] if pres_total[cid] else 0.0
        ar = abs_solved.get(cid, 0) / abs_total[cid] if abs_total.get(cid, 0) else 0.0
        out[cid] = pr - ar
    return out


def lift_stats(traces: list, universe_ids: list) -> dict:
    """Return {cid: success-lift in [-1, 1]} over all traces."""
    pres_solved, pres_total = {}, {}
    abs_solved, abs_total = {}, {}
    for t in traces:
        pset = set(t.present)
        for cid in universe_ids:
            if cid in pset:
                pres_total[cid] = pres_total.get(cid, 0) + 1
                if t.solved:
                    pres_solved[cid] = pres_solved.get(cid, 0) + 1
            else:
                abs_total[cid] = abs_total.get(cid, 0) + 1
                if t.solved:
                    abs_solved[cid] = abs_solved.get(cid, 0) + 1
    return _rates(pres_solved, pres_total, abs_solved, abs_total)


def present_rate_stats(traces: list, universe_ids: list) -> dict:
    """A weaker signal: raw solve-rate conditioned on presence (no absence contrast).

    Kept as an alternative scoring rubric for the recursive (two-level) demo,
    where a *weaker* rubric is intentionally worse than the lift rubric.
    """
    pres_solved, pres_total = {}, {}
    for t in traces:
        pset = set(t.present)
        for cid in universe_ids:
            if cid in pset:
                pres_total[cid] = pres_total.get(cid, 0) + 1
                if t.solved:
                    pres_solved[cid] = pres_solved.get(cid, 0) + 1
    out = {}
    for cid in universe_ids:
        out[cid] = pres_solved.get(cid, 0) / pres_total[cid] if pres_total.get(cid, 0) else 0.0
    return out
