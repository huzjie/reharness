# -*- coding: utf-8 -*-
"""Reward aggregation over traces (evidence-only, no labels)."""
from __future__ import annotations


def batch_reward(traces: list) -> float:
    if not traces:
        return 0.0
    return sum(t.reward for t in traces) / len(traces)


def success_rate(traces: list) -> float:
    if not traces:
        return 0.0
    return sum(1.0 for t in traces if t.solved) / len(traces)


def violation_count(traces: list) -> int:
    return sum(t.violations for t in traces)
