# -*- coding: utf-8 -*-
import unittest
import tempfile
import os

from reharness.harness.builder import build_harness
from reharness.optimizer.registry import HarnessRegistry


class TestRegistry(unittest.TestCase):
    def test_commit_rollback(self):
        reg = HarnessRegistry()
        h1 = build_harness(cids=["skill.search"])
        h2 = build_harness(cids=["skill.calculator"])
        reg.commit(h1, "v1")
        reg.commit(h2, "v2")
        self.assertEqual(reg.get(0).present(), h1.present())
        self.assertEqual(reg.rollback(0).present(), h1.present())

    def test_snapshot(self):
        reg = HarnessRegistry()
        reg.commit(build_harness(cids=["skill.search"]), "v1")
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            reg.snapshot(path)
            self.assertTrue(os.path.exists(path))
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
