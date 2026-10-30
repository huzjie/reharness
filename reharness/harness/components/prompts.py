# -*- coding: utf-8 -*-
"""System-prompt directive component."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PromptDirective:
    cid: str
    text: str
    enabled: bool = True
