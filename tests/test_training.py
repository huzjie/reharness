# -*- coding: utf-8 -*-
import unittest

from reharness.training.trainer import SkillTrainer, LinearScorer
from reharness.training.optimizer import SGD, AdamW


class TestTraining(unittest.TestCase):
    def test_skill_monotonic(self):
        t = SkillTrainer(0.5, lr=0.2)
        prev = 0.5
        for _ in range(10):
            s = t.train_step()
            self.assertGreater(s, prev)
            prev = s
        self.assertGreater(prev, 0.9)

    def test_linear_scorer_separates(self):
        sc = LinearScorer(6)
        for _ in range(200):
            sc.apply(sc.grad("skill.search"))
            sc.apply(sc.grad("guardrail.no_overwrite"))
        self.assertGreater(sc.score("skill.search"), sc.score("guardrail.no_overwrite"))

    def test_sgd(self):
        params = {"w": [1.0, 1.0]}
        opt = SGD(params, lr=0.1)
        opt.step({"w": [0.5, 0.5]})
        self.assertAlmostEqual(params["w"][0], 0.95)

    def test_adamw(self):
        params = {"w": [1.0]}
        opt = AdamW(params, lr=0.1)
        opt.step({"w": [1.0]})
        self.assertLess(params["w"][0], 1.0)


if __name__ == "__main__":
    unittest.main()
