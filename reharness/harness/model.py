# -*- coding: utf-8 -*-
"""Harness and Component data model."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Component:
    cid: str            # stable id, e.g. "skill.calculator"
    kind: str           # prompt | guardrail | memory | skill | tool | script | subagent | middleware
    body: str           # the instruction text / rule / script body
    enabled: bool = True


@dataclass
class Harness:
    system_prompt: str = ""
    components: list = field(default_factory=list)

    def component_ids(self) -> list:
        return [c.cid for c in self.components if c.enabled]

    def present(self) -> tuple:
        return tuple(sorted(self.component_ids()))

    def has(self, cid: str) -> bool:
        return any(c.cid == cid and c.enabled for c in self.components)

    def add(self, comp: Component):
        if not any(c.cid == comp.cid for c in self.components):
            self.components.append(comp)

    def remove(self, cid: str):
        self.components = [c for c in self.components if c.cid != cid]

    def set_enabled(self, cid: str, enabled: bool):
        for c in self.components:
            if c.cid == cid:
                c.enabled = enabled

    def to_dict(self) -> dict:
        return {"system_prompt": self.system_prompt,
                "components": [asdict(c) for c in self.components]}

    def clone(self) -> "Harness":
        from copy import deepcopy
        return deepcopy(self)
