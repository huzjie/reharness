# -*- coding: utf-8 -*-
"""Middleware component: a pre/post processor applied to every step."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Middleware:
    cid: str
    stage: str       # pre | post
    action: str
    enabled: bool = True
