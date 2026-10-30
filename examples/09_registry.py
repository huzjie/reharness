# -*- coding: utf-8 -*-
"""Versioned harness registry + rollback."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.harness.builder import build_harness
from reharness.optimizer.registry import HarnessRegistry

reg = HarnessRegistry()
reg.commit(build_harness(cids=["skill.search"]), "baseline")
reg.commit(build_harness(cids=["skill.search", "skill.calculator"]), "add calculator")

print("diff v0->v1:", reg.diff(0, 1))
print("rollback to v0:", reg.rollback(0).present())
