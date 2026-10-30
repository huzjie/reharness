# -*- coding: utf-8 -*-
import unittest

from reharness.harness.builder import build_harness, empty_harness
from reharness.harness.serialize import to_dict, from_dict, diff


class TestHarness(unittest.TestCase):
    def test_build(self):
        h = build_harness(cids=["skill.search", "tool.file_write"])
        self.assertEqual(sorted(h.present()), ["skill.search", "tool.file_write"])

    def test_add_remove(self):
        h = empty_harness()
        h.add(build_harness(cids=["skill.search"]).components[0])
        self.assertTrue(h.has("skill.search"))
        h.remove("skill.search")
        self.assertFalse(h.has("skill.search"))

    def test_roundtrip(self):
        h = build_harness(system_prompt="hi", cids=["skill.search"])
        h2 = from_dict(to_dict(h))
        self.assertEqual(h.present(), h2.present())
        self.assertEqual(h2.system_prompt, "hi")

    def test_diff(self):
        a = build_harness(cids=["skill.search"])
        b = build_harness(cids=["skill.calculator"])
        d = diff(a, b)
        self.assertEqual(d["added"], ["skill.calculator"])
        self.assertEqual(d["removed"], ["skill.search"])


if __name__ == "__main__":
    unittest.main()
