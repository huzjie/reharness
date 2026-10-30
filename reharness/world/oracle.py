# -*- coding: utf-8 -*-
"""Latent ground-truth oracle: generates tasks and knows the right answer.

CRITICAL DESIGN POINT: the optimizer NEVER sees the oracle's ``required`` /
``forbidden`` sets directly. It only sees execution traces (which harness
components were present and whether the agent succeeded). This is what forces
the optimizer to *learn* the harness from evidence, exactly as in Harness2's
label-free regime.

To make the learning problem falsifiable, the world has ONE global optimal
harness: a fixed set REQUIRED (functional components + one safety guardrail)
that solves every task, and a fixed set FORBIDDEN that breaks every task.
Each task requires a random *subset* of REQUIRED and is broken by a random
*subset* of FORBIDDEN, so a partial harness solves some tasks and the full
REQUIRED set solves all of them.
"""
from __future__ import annotations

from ..utils.rng import stable_int, stable_choice, stable_shuffle
from .task import Task, TaskBatch

# Global ground truth. Deterministic, chosen to be a realistic "good harness":
# 5 functional core capabilities + 1 safety guardrail. Each task depends on
# exactly ONE core capability (plus an optional hazard guardrail), which keeps
# the contrastive "success-lift" of a component clean and falsifiable.
CORES = (
    "skill.calculator",
    "skill.search",
    "skill.code",
    "skill.file",
    "tool.db_query",
)
# Safety-critical guardrail that hazard tasks must carry (measured on its own
# dimension so "safety" is a separate metric).
HAZARD = "guardrail.refuse_pii"
# A realistic "good harness": all cores + the safety guardrail.
REQUIRED = CORES + (HAZARD,)
# A realistic "bad harness": an over-broad guardrail and a detail-skipping
# directive, either of which breaks the agent.
FORBIDDEN = (
    "guardrail.no_overwrite",
    "prompt.be_concise",
)


class Oracle:
    def __init__(self, seed: int = 20261030):
        self.seed = seed
        self._cache = {}

    def make_task(self, task_id: str) -> Task:
        if task_id in self._cache:
            return self._cache[task_id]
        # Each task depends on exactly ONE of the REQUIRED components (uniform),
        # so every component -- including the safety guardrail -- is an equally
        # strong, independent bottleneck. This is what keeps the contrastive
        # success-lift clean (no "needs A and B simultaneously" conjunction).
        required_component = stable_choice("req:%s:%d" % (task_id, self.seed), list(REQUIRED))
        n_forb = stable_int("nforb:%s:%d" % (task_id, self.seed), 0, 1)
        forbidden = tuple(stable_shuffle("forb:%s:%d" % (task_id, self.seed), list(FORBIDDEN))[:n_forb])
        # A task whose required component IS the guardrail is a "safety task".
        hazard = HAZARD if required_component == HAZARD else None
        required = (required_component,)
        task = Task(
            id=task_id,
            name="task %s" % task_id,
            description="Synthetic task %s (deterministic ground truth)" % task_id,
            required=required,
            forbidden=forbidden,
            hazard=hazard,
        )
        self._cache[task_id] = task
        return task

    def make_batch(self, n: int, prefix: str = "t") -> TaskBatch:
        tasks = [self.make_task("%s%03d" % (prefix, i)) for i in range(n)]
        return TaskBatch(tasks)

    def ground_truth(self, task: Task):
        return {"required": task.required, "forbidden": task.forbidden, "hazard": task.hazard}
