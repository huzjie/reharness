# -*- coding: utf-8 -*-
"""Linear learning-rate schedule."""
from __future__ import annotations


class LinearSchedule:
    def __init__(self, start: float, end: float, steps: int):
        self.start = start
        self.end = end
        self.steps = max(1, steps)

    def lr(self, step: int) -> float:
        t = min(1.0, step / self.steps)
        return self.start + (self.end - self.start) * t
