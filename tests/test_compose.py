# -*- coding: utf-8 -*-
import unittest

from reharness.compose.composer import Composer
from reharness.compose.contrastive import lift_stats
from reharness.world.oracle import Oracle, REQUIRED, FORBIDDEN
from reharness.world.agent import Agent
from reharness.world.universe import component_ids
from reharness.propose.proposer import Proposer


class TestCompose(unittest.TestCase):
    def test_boost(self):
        self.assertAlmostEqual(Composer(0.5).boost(), 0.0)
        self.assertAlmostEqual(Composer(1.0).boost(), 1.0)
        self.assertAlmostEqual(Composer(0.75).boost(), 0.5)

    def test_lift_signal(self):
        oracle = Oracle(20261030)
        agent = Agent()
        batch = oracle.make_batch(24)
        candidates = Proposer(20261030).propose(120, size=6)
        traces = []
        for cids in candidates:
            traces.extend(agent.run(t, cids) for t in batch)
        lifts = lift_stats(traces, component_ids())
        # required components have positive lift, forbidden negative
        for c in REQUIRED:
            self.assertGreater(lifts[c], 0.0)
        for c in FORBIDDEN:
            self.assertLess(lifts[c], 0.0)

    def test_compose_recovers_required_at_skill_1(self):
        from reharness.compose.composer import Composer
        from reharness.scoring.metrics import component_recall
        oracle = Oracle(20261030)
        agent = Agent()
        batch = oracle.make_batch(24)
        candidates = Proposer(20261030).propose(120, size=6)
        traces = []
        for cids in candidates:
            traces.extend(agent.run(t, cids) for t in batch)
        lifts = lift_stats(traces, component_ids())
        selected = Composer(1.0).select(lifts, 6)
        self.assertGreaterEqual(component_recall(selected), 5 / 6)


if __name__ == "__main__":
    unittest.main()
