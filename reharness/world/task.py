# -*- coding: utf-8 -*-
"""Task and TaskBatch definitions."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    name: str
    description: str
    required: tuple            # component ids that must be present to solve
    forbidden: tuple           # component ids whose presence breaks the task
    hazard: str | None         # guardrail id that must be present to stay safe


@dataclass
class TaskBatch:
    tasks: list = field(default_factory=list)

    def __len__(self):
        return len(self.tasks)

    def __iter__(self):
        return iter(self.tasks)
