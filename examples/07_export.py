# -*- coding: utf-8 -*-
"""Export an optimization run to JSON."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from reharness.export import export_run

path = export_run("example_export.json")
print("wrote", path)
