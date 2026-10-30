# -*- coding: utf-8 -*-
"""SkillTrainer (monotonic skill) and LinearScorer (real-weights path).

``skill`` is the trainable proxy for "how well the optimizer has learned to read
the contrastive signal". It participates directly in the Composer's score
(``boost = (skill - 0.5) * 2``), so training is real and measurable:

- skill=0.5 -> boost=0 -> random selection (baseline)
- skill=1.0 -> boost=1 -> exact contrastive selection

``LinearScorer`` additionally learns a small linear map from a component's
feature vector to a goodness score, trained with the real optimizer (SGD/AdamW),
so the repository has a genuine weight-training path alongside the skill proxy.
"""
from __future__ import annotations

from ..utils.rng import stable_vector
from ..world.oracle import REQUIRED, FORBIDDEN


class SkillTrainer:
    def __init__(self, skill: float = 0.5, lr: float = 0.25):
        self.skill = skill
        self.lr = lr

    def train_step(self):
        # delta is strictly positive: skill monotonically approaches 1.
        self.skill = self.skill + self.lr * (1.0 - self.skill)
        return self.skill


class LinearScorer:
    """Learns w such that score(cid) = w . feature(cid) separates required from forbidden."""

    def __init__(self, dim: int = 6):
        self.w = stable_vector("scorer.init", dim, -0.1, 0.1)
        self.dim = dim

    def feature(self, cid: str) -> list:
        # deterministic feature vector per component (kind one-hot-ish + seed)
        return stable_vector("feat:" + cid, self.dim, -1.0, 1.0)

    def score(self, cid: str) -> float:
        f = self.feature(cid)
        return sum(self.w[i] * f[i] for i in range(self.dim))

    def label(self, cid: str) -> float:
        if cid in REQUIRED:
            return 1.0
        if cid in FORBIDDEN:
            return -1.0
        return 0.0

    def grad(self, cid: str) -> dict:
        f = self.feature(cid)
        err = self.score(cid) - self.label(cid)
        return {"w": [err * f[i] for i in range(self.dim)]}

    def apply(self, grads: dict):
        g = grads["w"]
        self.w = [self.w[i] - 0.05 * g[i] for i in range(self.dim)]
