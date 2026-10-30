# -*- coding: utf-8 -*-
"""Prober: evaluate candidate harnesses against a task batch."""
from __future__ import annotations

from ..world.agent import Agent
from ..world.task import TaskBatch


class Prober:
    def __init__(self, agent: Agent):
        self.agent = agent

    def probe(self, candidates: list, batch: TaskBatch) -> list:
        """Return a list of (candidate_ids, traces)."""
        results = []
        for cids in candidates:
            traces = [self.agent.run(t, cids) for t in batch]
            results.append((cids, traces))
        return results
