# -*- coding: utf-8 -*-
import unittest

from reharness.config import load_config, deep_merge, DEFAULTS


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        cfg = load_config()
        self.assertEqual(cfg["compose"]["top_k"], 6)
        self.assertEqual(cfg["optimizer"]["seed"], 20261030)

    def test_deep_merge(self):
        merged = deep_merge(DEFAULTS, {"compose": {"top_k": 9}})
        self.assertEqual(merged["compose"]["top_k"], 9)
        self.assertEqual(merged["compose"]["eps"], DEFAULTS["compose"]["eps"])


if __name__ == "__main__":
    unittest.main()
