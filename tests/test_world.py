# -*- coding: utf-8 -*-
import unittest

from reharness.world.oracle import Oracle, REQUIRED, FORBIDDEN, HAZARD
from reharness.world.agent import Agent


class TestWorld(unittest.TestCase):
    def setUp(self):
        self.oracle = Oracle(20261030)
        self.agent = Agent(max_turns=6)

    def test_deterministic_task(self):
        t1 = self.oracle.make_task("t000")
        t2 = self.oracle.make_task("t000")
        self.assertEqual(t1.required, t2.required)
        self.assertEqual(t1.forbidden, t2.forbidden)

    def test_required_subset(self):
        for i in range(20):
            t = self.oracle.make_task("t%03d" % i)
            self.assertTrue(set(t.required).issubset(set(REQUIRED)))
            self.assertTrue(set(t.forbidden).issubset(set(FORBIDDEN)))

    def test_optimal_harness_solves_all(self):
        batch = self.oracle.make_batch(24)
        present = tuple(REQUIRED)
        for t in batch:
            tr = self.agent.run(t, present)
            self.assertTrue(tr.success)
            self.assertTrue(tr.safe)
            self.assertEqual(tr.reward, 1.0)

    def test_forbidden_breaks(self):
        from reharness.world.task import Task
        t = Task(id="fb", name="fb", description="fb",
                 required=("skill.search",), forbidden=("guardrail.no_overwrite",), hazard=None)
        tr = self.agent.run(t, ("skill.search", "guardrail.no_overwrite"))
        self.assertFalse(tr.success)

    def test_missing_required_fails(self):
        t = self.oracle.make_task("t005")
        present = tuple(c for c in REQUIRED if c not in t.required)
        tr = self.agent.run(t, present)
        self.assertFalse(tr.success)


if __name__ == "__main__":
    unittest.main()
