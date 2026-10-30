# -*- coding: utf-8 -*-
"""Contrastive lift + compose."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.propose.proposer import Proposer
from reharness.world.oracle import Oracle
from reharness.world.agent import Agent
from reharness.world.universe import component_ids
from reharness.compose.contrastive import lift_stats
from reharness.compose.composer import Composer

oracle = Oracle(20261030)
agent = Agent()
batch = oracle.make_batch(24)
candidates = Proposer(20261030).propose(120, size=6)

traces = []
for cids in candidates:
    traces.extend(agent.run(t, cids) for t in batch)

lifts = lift_stats(traces, component_ids())
print("top lift components:")
for cid, lift in sorted(lifts.items(), key=lambda kv: kv[1], reverse=True)[:8]:
    print("  %-24s %+.3f" % (cid, lift))

selected = Composer(1.0).select(lifts, 6)
print("composed harness:", ", ".join(selected))
