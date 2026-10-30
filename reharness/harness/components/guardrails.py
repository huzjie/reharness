# -*- coding: utf-8 -*-
"""Guardrail component: a rule the agent must never violate."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Guardrail:
    cid: str
    rule: str
    severity: str = "block"       # block | warn | log
    enabled: bool = True

    def text(self) -> str:
        return "[%s] %s (severity=%s)" % (self.cid, self.rule, self.severity)
