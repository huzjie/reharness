# -*- coding: utf-8 -*-
"""Propose candidates and probe them."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.propose.proposer import Proposer
from reharness.world.oracle import Oracle
from reharness.world.agent import Agent
from reharness.world.reward import success_rate

oracle = Oracle(20261030)
agent = Agent()
batch = oracle.make_batch(16)

proposer = Proposer(20261030)
candidates = proposer.propose(6, size=6)
for i, cids in enumerate(candidates):
    traces = [agent.run(t, cids) for t in batch]
    print("candidate %02d  success_rate=%.3f  (%d components)" % (i, success_rate(traces), len(cids)))
