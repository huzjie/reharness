# -*- coding: utf-8 -*-
"""Subagent component: a delegatable specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Subagent:
    cid: str
    name: str
    role: str
    enabled: bool = True
