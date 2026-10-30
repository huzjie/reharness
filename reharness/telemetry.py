# -*- coding: utf-8 -*-
"""Tiny timing / counters for observability."""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class Timer:
    start: float = field(default_factory=time.perf_counter)

    def elapsed(self) -> float:
        return time.perf_counter() - self.start

    def reset(self):
        self.start = time.perf_counter()
