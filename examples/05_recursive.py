# -*- coding: utf-8 -*-
"""Two-level (recursive) harness optimization."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.optimizer.ppc import PPC
from reharness.optimizer.recursive import recursive_optimize, flat_optimize

ppc = PPC()
for skill in (0.5, 1.0):
    rec = recursive_optimize(ppc, skill)
    flat = flat_optimize(ppc, skill)
    print("skill=%.1f  recursive=%.3f  flat=%.3f  gain=%+.3f  meta=%s" % (
        skill, rec["success_rate"], flat["success_rate"],
        rec["success_rate"] - flat["success_rate"], ",".join(rec["meta_selected"])))
