# -*- coding: utf-8 -*-
"""Composer: pick components by contrastive score, driven by a trainable skill.

``skill`` models "how well the optimizer has learned to read the contrastive
signal". skill=0.5 -> boost=0 -> selection is pure noise (random baseline);
skill=1.0 -> boost=1 -> selection is exactly by lift (recovers the optimal set).
"""
from __future__ import annotations

from ..utils.rng import stable_float


class Composer:
    def __init__(self, skill: float = 0.5):
        self.skill = skill

    def boost(self) -> float:
        return max(0.0, min(1.0, (self.skill - 0.5) * 2.0))

    def score(self, cid: str, signal: float) -> float:
        b = self.boost()
        noise = stable_float("noise:" + cid, -1.0, 1.0)
        return b * signal + (1.0 - b) * noise

    def select(self, signals: dict, top_k: int) -> list:
        # Min-max normalize the signal to [-1, 1] so it lives on the same scale
        # as the noise term; otherwise a small-magnitude lift (~0.1) is swamped
        # by the (-1, 1) noise and the boost never meaningfully dominates.
        vals = list(signals.values())
        lo, hi = min(vals), max(vals)
        span = (hi - lo) if (hi - lo) > 1e-12 else 1.0
        norm = {cid: 2.0 * (signals[cid] - lo) / span - 1.0 for cid in signals}
        scored = [(cid, self.score(cid, norm[cid])) for cid in signals]
        scored.sort(key=lambda kv: kv[1], reverse=True)
        return [cid for cid, _s in scored[:top_k]]
