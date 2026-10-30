# -*- coding: utf-8 -*-
import unittest

from reharness.propose.proposer import Proposer
from reharness.propose.operators import random_subset, add_component, remove_component
from reharness.harness.builder import build_harness


class TestPropose(unittest.TestCase):
    def test_propose_size(self):
        p = Proposer(20261030)
        cands = p.propose(6, size=8)
        self.assertEqual(len(cands), 6)
        self.assertTrue(all(len(c) == 8 for c in cands))

    def test_deterministic(self):
        p1 = Proposer(20261030)
        p2 = Proposer(20261030)
        self.assertEqual(p1.propose(4, size=8), p2.propose(4, size=8))

    def test_operators(self):
        h = build_harness(cids=["skill.search"])
        h2 = add_component(h, "skill.calculator")
        self.assertTrue(h2.has("skill.calculator"))
        h3 = remove_component(h2, "skill.search")
        self.assertFalse(h3.has("skill.search"))


if __name__ == "__main__":
    unittest.main()
