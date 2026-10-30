# -*- coding: utf-8 -*-
"""Tool guidance component: when and how to call a tool."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolRule:
    cid: str
    tool: str
    when: str
    how: str
    enabled: bool = True

    def text(self) -> str:
        return "[%s] %s: use when %s, do %s" % (self.cid, self.tool, self.when, self.how)
