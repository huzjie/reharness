# -*- coding: utf-8 -*-
import unittest

from reharness.scoring.metrics import component_recall, summarize
from reharness.world.oracle import REQUIRED


class TestMetrics(unittest.TestCase):
    def test_recall(self):
        self.assertEqual(component_recall(list(REQUIRED)), 1.0)
        self.assertEqual(component_recall([]), 0.0)

    def test_summarize_monotonic(self):
        results = {
            0.5: {"success_rate": 0.2, "component_recall": 0.15, "contrastive_gain": 0.0, "guardrail_violations": 5},
            1.0: {"success_rate": 1.0, "component_recall": 1.0, "contrastive_gain": 0.8, "guardrail_violations": 0},
        }
        s = summarize(results)
        self.assertTrue(s["success_rate"]["monotonic"])
        self.assertTrue(s["guardrail_violations"]["monotonic"])


if __name__ == "__main__":
    unittest.main()
