# -*- coding: utf-8 -*-
"""The core Propose-Probe-Compose loop (evidence-only, label-free)."""
from __future__ import annotations

from ..config import DEFAULTS, deep_merge
from ..world.universe import component_ids
from ..world.oracle import Oracle
from ..world.agent import Agent
from ..world.reward import success_rate, violation_count
from ..propose.proposer import Proposer
from ..probe.prober import Prober
from ..compose.contrastive import lift_stats, present_rate_stats
from ..compose.composer import Composer
from ..compose.merge import merge_harness
from ..scoring.metrics import component_recall


class PPC:
    def __init__(self, cfg: dict | None = None):
        self.cfg = deep_merge(DEFAULTS, cfg or {})
        self.oracle = Oracle(self.cfg["optimizer"]["seed"])
        self.agent = Agent(max_turns=self.cfg["probe"]["max_turns"])
        self.proposer = Proposer(self.cfg["optimizer"]["seed"])
        self.prober = Prober(self.agent)

    def run(self, skill: float, top_k: int | None = None, scoring: str = "lift",
            probe_size: int | None = None, n_candidates: int | None = None,
            n_tasks: int | None = None, direction: str = "max") -> dict:
        top_k = top_k if top_k is not None else self.cfg["compose"]["top_k"]
        probe_size = probe_size if probe_size is not None else self.cfg["propose"]["probe_size"]
        n_candidates = n_candidates if n_candidates is not None else (
            self.cfg["propose"]["candidates"] * self.cfg["optimizer"]["rounds"])
        n_tasks = n_tasks if n_tasks is not None else self.cfg["probe"]["n_tasks"]

        batch = self.oracle.make_batch(n_tasks)
        candidates = self.proposer.propose(n_candidates, size=probe_size)
        probed = self.prober.probe(candidates, batch)
        all_traces = [tr for _, traces in probed for tr in traces]
        universe = component_ids()

        if scoring == "present":
            signals = present_rate_stats(all_traces, universe)
        else:
            signals = lift_stats(all_traces, universe)
        # "min" models the classic sign-error bug: optimizing the objective in
        # the wrong direction. It lets the recursion demo have a real gap.
        if direction == "min":
            signals = {cid: -v for cid, v in signals.items()}

        composer = Composer(skill)
        selected = composer.select(signals, top_k)
        composed = merge_harness(selected)
        composed_traces = [self.agent.run(t, composed.present()) for t in batch]
        sr = success_rate(composed_traces)

        # Random baseline: select top_k by *pure noise* (boost=0), no contrastive
        # signal. This isolates exactly what the contrastive signal adds.
        random_selected = Composer(0.5).select(signals, top_k)
        random_composed = merge_harness(random_selected)
        random_traces = [self.agent.run(t, random_composed.present()) for t in batch]
        random_sr = success_rate(random_traces)

        return {
            "skill": skill,
            "top_k": top_k,
            "scoring": scoring,
            "probe_size": probe_size,
            "selected": selected,
            "composed_ids": composed.present(),
            "success_rate": sr,
            "component_recall": component_recall(selected),
            "guardrail_violations": violation_count(composed_traces),
            "random_sr": random_sr,
            "contrastive_gain": sr - random_sr,
        }
