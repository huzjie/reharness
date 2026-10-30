# -*- coding: utf-8 -*-
"""Quickstart: build a harness and run the agent."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.harness.builder import build_harness
from reharness.world.oracle import Oracle
from reharness.world.agent import Agent

oracle = Oracle(20261030)
agent = Agent()
task = oracle.make_task("t000")

# A minimal harness with one required component and no forbidden ones.
harness = build_harness(cids=["prompt.think_stepwise", "skill.search"])
tr = agent.run(task, harness.present())
print("task=%s required=%s" % (task.id, task.required))
print("harness=%s" % list(harness.present()))
print("success=%s safe=%s reward=%.1f" % (tr.success, tr.safe, tr.reward))
