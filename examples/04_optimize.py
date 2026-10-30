# -*- coding: utf-8 -*-
"""Full Propose-Probe-Compose optimization."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.optimizer.ppc import PPC

ppc = PPC()
for skill in (0.5, 0.8, 1.0):
    r = ppc.run(skill)
    print("skill=%.1f  success=%.3f  recall=%.3f  violations=%d  gain=%+.3f" % (
        skill, r["success_rate"], r["component_recall"],
        r["guardrail_violations"], r["contrastive_gain"]))
