# -*- coding: utf-8 -*-
import unittest

from reharness.optimizer.ppc import PPC
from reharness.optimizer.recursive import recursive_optimize, flat_optimize


class TestRecursive(unittest.TestCase):
    def setUp(self):
        self.ppc = PPC()

    def test_recursion_gain_positive_at_skill_1(self):
        rec = recursive_optimize(self.ppc, 1.0)
        flat = flat_optimize(self.ppc, 1.0)
        self.assertGreater(rec["success_rate"], flat["success_rate"])

    def test_recursion_grows_with_skill(self):
        g05 = recursive_optimize(self.ppc, 0.5)["success_rate"] - flat_optimize(self.ppc, 0.5)["success_rate"]
        g10 = recursive_optimize(self.ppc, 1.0)["success_rate"] - flat_optimize(self.ppc, 1.0)["success_rate"]
        self.assertGreaterEqual(g10, g05)


if __name__ == "__main__":
    unittest.main()
