# -*- coding: utf-8 -*-
"""Memory policy component."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryPolicy:
    cid: str
    window: int = 8
    summarize: bool = False
    retrieval: bool = False
    enabled: bool = True

    def text(self) -> str:
        return "[%s] window=%d summarize=%s retrieval=%s" % (self.cid, self.window, self.summarize, self.retrieval)
