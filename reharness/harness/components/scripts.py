# -*- coding: utf-8 -*-
"""Helper script component."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HelperScript:
    cid: str
    name: str
    body: str
    enabled: bool = True
