# -*- coding: utf-8 -*-
import unittest

from reharness.pipeline import Pipeline
from reharness.benchmark import run_bench


class TestPipeline(unittest.TestCase):
    def test_run(self):
        cfg = {"training": {"epochs": 3}}
        out = Pipeline(cfg).run()
        self.assertIn("success_rate", out)
        self.assertGreater(out["trained_skill"], 0.5)

    def test_bench(self):
        b = run_bench()
        self.assertIn("summary", b)
        self.assertAlmostEqual(b["summary"]["success_rate"]["end"], 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
