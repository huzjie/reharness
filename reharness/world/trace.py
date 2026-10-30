# -*- coding: utf-8 -*-
"""Execution trace produced by running an agent under a harness."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Trace:
    task_id: str
    present: tuple          # component ids the harness exposed (enabled)
    success: bool           # required subset present AND forbidden disjoint
    safe: bool              # hazard guardrail present (if any)
    reward: float           # 1.0 if success and safe else 0.0
    turns: int              # agent turns consumed
    violations: int = 0     # hazard guardrails missing on hazard tasks

    @property
    def solved(self) -> bool:
        return self.success and self.safe
