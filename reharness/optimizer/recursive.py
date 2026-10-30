# -*- coding: utf-8 -*-
"""Two-level optimization: optimize the optimizer's own config, then optimize."""
from __future__ import annotations

from ..compose.composer import Composer
from .meta import META_CONFIGS, META_COMPONENTS, CONFIG_META, FLAT_CONFIG, mean


def _meta_lifts(evals: dict) -> dict:
    lifts = {}
    for mc in META_COMPONENTS:
        containing = [evals[n] for n, comps in CONFIG_META.items() if mc in comps]
        not_containing = [evals[n] for n, comps in CONFIG_META.items() if mc not in comps]
        p = mean(containing)
        a = mean(not_containing) if not_containing else 0.0
        lifts[mc] = p - a
    return lifts


def _config_from_selected(selected: list) -> dict:
    return {"direction": "min" if "direction.min" in selected else "max"}


def recursive_optimize(ppc, skill: float, cheap_candidates: int = 12, cheap_tasks: int = 24) -> dict:
    # 1. cheaply evaluate each candidate optimizer config
    evals = {}
    for name, conf in META_CONFIGS:
        r = ppc.run(skill, direction=conf["direction"],
                    n_candidates=cheap_candidates, n_tasks=cheap_tasks)
        evals[name] = r["success_rate"]
    # 2. contrastive meta-lift
    lifts = _meta_lifts(evals)
    # 3. meta-compose (pick the objective direction)
    selected = Composer(skill).select(lifts, top_k=1)
    conf = _config_from_selected(selected)
    # 4. final PPC with the chosen config
    final = ppc.run(skill, direction=conf["direction"])
    final["meta_lifts"] = lifts
    final["meta_selected"] = selected
    final["meta_evals"] = evals
    return final


def flat_optimize(ppc, skill: float) -> dict:
    return ppc.run(skill, direction=FLAT_CONFIG["direction"])
