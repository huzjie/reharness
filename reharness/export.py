# -*- coding: utf-8 -*-
"""Export an optimization run to JSON (reproducibility)."""
from __future__ import annotations

import json

from .pipeline import Pipeline


def export_run(path: str, cfg: dict | None = None):
    out = Pipeline(cfg).run()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return path
