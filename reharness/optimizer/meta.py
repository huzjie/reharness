# -*- coding: utf-8 -*-
"""Two-level (recursive) meta-space: the optimizer's own harness.

Level 1 optimizes the *agent's* harness. Level 2 treats the *optimizer* as an
agent whose harness is its own configuration -- here, the *direction* of its
objective -- and optimizes that too, using the SAME Propose-Probe-Compose loop.
This is the recursive architecture of Harness2.

The meta-space is deliberately minimal and clean:
  - direction.max : compose by keeping the top-k contrastive lift (correct)
  - direction.min : keep the bottom-k lift -- the classic "sign error" of
    optimizing the objective in the wrong direction (gradient ascent vs descent)
"""
from __future__ import annotations

META_CONFIGS = [
    ("cfg_max", {"direction": "max"}),
    ("cfg_min", {"direction": "min"}),
]

META_COMPONENTS = ["direction.max", "direction.min"]

CONFIG_META = {
    "cfg_max": {"direction.max"},
    "cfg_min": {"direction.min"},
}

FLAT_CONFIG = {"direction": "min"}


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0
