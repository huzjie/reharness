# -*- coding: utf-8 -*-
"""High-level end-to-end pipeline: train skill -> optimize harness -> export."""
from __future__ import annotations

from .config import DEFAULTS, deep_merge
from .training.trainer import SkillTrainer
from .optimizer.ppc import PPC


class Pipeline:
    def __init__(self, cfg: dict | None = None):
        self.cfg = deep_merge(DEFAULTS, cfg or {})

    def run(self):
        ppc = PPC(self.cfg)
        trainer = SkillTrainer(0.5, self.cfg["training"]["lr"])
        for _ in range(self.cfg["training"]["epochs"]):
            trainer.train_step()
        result = ppc.run(trainer.skill)
        result["trained_skill"] = trainer.skill
        return result
