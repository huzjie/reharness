# -*- coding: utf-8 -*-
"""Skill component: a reusable capability the agent can invoke."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Skill:
    cid: str
    name: str
    trigger: str
    instructions: str
    enabled: bool = True

    def text(self) -> str:
        return "[%s] %s: trigger=%s\n%s" % (self.cid, self.name, self.trigger, self.instructions)
