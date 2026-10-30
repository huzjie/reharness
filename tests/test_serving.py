# -*- coding: utf-8 -*-
import unittest

from reharness.serving.models import info, ok


class TestServing(unittest.TestCase):
    def test_info(self):
        self.assertEqual(info()["name"], "reharness")

    def test_ok(self):
        o = ok(a=1)
        self.assertEqual(o["status"], "ok")
        self.assertEqual(o["a"], 1)


if __name__ == "__main__":
    unittest.main()
