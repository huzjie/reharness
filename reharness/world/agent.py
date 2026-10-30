# -*- coding: utf-8 -*-
"""Mock agent: runs a task under a harness and emits a deterministic trace.

The agent is deliberately dumb: it "solves" a task iff the harness exposes every
required component and none of the forbidden ones, and it stays safe iff the
hazard guardrail is present. This is the minimal falsifiable model of "the
harness determines agent behavior", which is exactly the Harness2 thesis.
"""
from __future__ import annotations

from .trace import Trace
from .task import Task


class Agent:
    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns

    def run(self, task: Task, present: tuple) -> Trace:
        present_set = set(present)
        success = set(task.required).issubset(present_set) and not (set(task.forbidden) & present_set)
        safe = task.hazard is None or task.hazard in present_set
        violations = 0
        if task.hazard is not None and task.hazard not in present_set:
            violations = 1
        reward = 1.0 if (success and safe) else 0.0
        # A harness that is missing required components "wanders" more turns.
        turns = self.max_turns if success else min(self.max_turns, 1 + len(set(task.required) - present_set) * 2)
        return Trace(
            task_id=task.id,
            present=present,
            success=success,
            safe=safe,
            reward=reward,
            turns=turns,
            violations=violations,
        )
