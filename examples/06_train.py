# -*- coding: utf-8 -*-
"""Train the skill (monotonic)."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.training.trainer import SkillTrainer

t = SkillTrainer(0.5, lr=0.2)
for i in range(10):
    s = t.train_step()
    print("step %02d  skill=%.4f" % (i + 1, s))
