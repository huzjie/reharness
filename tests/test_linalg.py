# -*- coding: utf-8 -*-
import unittest

from reharness.utils import linalg


class TestLinalg(unittest.TestCase):
    def test_matvec(self):
        self.assertEqual(linalg.matvec([[1, 2], [3, 4]], [1, 1]), [3, 7])

    def test_matmul(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        self.assertEqual(linalg.matmul(A, B), [[19, 22], [43, 50]])

    def test_softmax(self):
        p = linalg.softmax([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(p), 1.0, places=6)
        self.assertGreater(p[2], p[0])

    def test_argmax(self):
        self.assertEqual(linalg.argmax([1.0, 5.0, 3.0]), 1)

    def test_relu(self):
        self.assertEqual(linalg.relu([-1.0, 2.0]), [0.0, 2.0])


if __name__ == "__main__":
    unittest.main()
