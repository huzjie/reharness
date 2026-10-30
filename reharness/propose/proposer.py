# -*- coding: utf-8 -*-
"""Proposer: turn a base harness into K candidate variants (random subsets)."""
from __future__ import annotations

from ..utils.rng import stable_shuffle
from ..world.universe import component_ids
from .operators import random_subset


class Proposer:
    def __init__(self, seed: int = 20261030):
        self.seed = seed

    def propose(self, n: int, size: int = 8, base=None) -> list:
        """Return n candidate component-id tuples (deterministic)."""
        return [random_subset("cand:%d:%d" % (i, self.seed), size) for i in range(n)]

    def propose_around(self, base_ids: tuple, n: int, size: int = 8) -> list:
        """Propose candidates that keep base_ids and add fresh components."""
        pool = component_ids()
        out = []
        for i in range(n):
            extra = [c for c in pool if c not in base_ids]
            fill = stable_shuffle("around:%d:%d" % (i, self.seed), extra)[: size - len(base_ids)]
            out.append(tuple(sorted(set(base_ids) | set(fill))))
        return out
