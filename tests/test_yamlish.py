# -*- coding: utf-8 -*-
import unittest

from reharness.utils.yamlish import yaml_loads


class TestYamlish(unittest.TestCase):
    def test_nested(self):
        doc = yaml_loads("a:\n  b: 1\n  c:\n    - x\n    - y\n")
        self.assertEqual(doc["a"]["b"], 1)
        self.assertEqual(doc["a"]["c"], ["x", "y"])

    def test_scalars(self):
        doc = yaml_loads("i: 3\nf: 1.5\ns: hello\nb: true\nn: null\n")
        self.assertEqual(doc["i"], 3)
        self.assertAlmostEqual(doc["f"], 1.5)
        self.assertEqual(doc["s"], "hello")
        self.assertIs(doc["b"], True)
        self.assertIsNone(doc["n"])


if __name__ == "__main__":
    unittest.main()
