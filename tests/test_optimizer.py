# -*- coding: utf-8 -*-
import unittest

from reharness.optimizer.ppc import PPC


class TestOptimizer(unittest.TestCase):
    def setUp(self):
        self.ppc = PPC()

    def test_skill_1_solves_all(self):
        r = self.ppc.run(1.0)
        self.assertAlmostEqual(r["success_rate"], 1.0, places=6)
        self.assertEqual(r["guardrail_violations"], 0)
        self.assertGreater(r["component_recall"], 0.9)

    def test_skill_monotonic(self):
        rs = [self.ppc.run(s) for s in (0.5, 0.7, 0.9, 1.0)]
        srs = [r["success_rate"] for r in rs]
        for a, b in zip(srs, srs[1:]):
            self.assertGreaterEqual(b, a)

    def test_contrastive_gain_positive(self):
        r = self.ppc.run(1.0)
        self.assertGreater(r["contrastive_gain"], 0.0)


if __name__ == "__main__":
    unittest.main()
