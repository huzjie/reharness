# -*- coding: utf-8 -*-
import unittest

from reharness.utils.rng import stable_float, stable_int, stable_vector, stable_choice, stable_matrix


class TestRng(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(stable_float("a"), stable_float("a"))
        self.assertNotEqual(stable_float("a"), stable_float("b"))

    def test_ranges(self):
        for k in ["x", "y", "z"]:
            self.assertGreaterEqual(stable_float(k), 0.0)
            self.assertLessEqual(stable_float(k), 1.0)
            self.assertGreaterEqual(stable_int(k, 2, 4), 2)
            self.assertLessEqual(stable_int(k, 2, 4), 4)

    def test_vector_length(self):
        self.assertEqual(len(stable_vector("v", 8)), 8)
        self.assertEqual(len(stable_matrix("m", 3, 4)), 3)
        self.assertEqual(len(stable_matrix("m", 3, 4)[0]), 4)

    def test_choice(self):
        items = ["a", "b", "c"]
        self.assertIn(stable_choice("c", items), items)


if __name__ == "__main__":
    unittest.main()
