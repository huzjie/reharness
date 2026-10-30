# -*- coding: utf-8 -*-
"""Harness registry: versioned snapshots with rollback (auditability).

Every composed harness is recorded as an immutable version. This mirrors the
"git tree of adapters" idea from harness-optimization frameworks: you can
always see what changed and roll back to any previous harness.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from ..harness.model import Harness


@dataclass
class HarnessRegistry:
    versions: list = field(default_factory=list)

    def commit(self, harness: Harness, note: str = "") -> int:
        self.versions.append({"note": note, "harness": harness.to_dict()})
        return len(self.versions) - 1

    def get(self, index: int):
        if index < 0 or index >= len(self.versions):
            raise IndexError("version %d out of range" % index)
        from ..harness.serialize import from_dict
        return from_dict(self.versions[index]["harness"])

    def rollback(self, index: int):
        return self.get(index)

    def diff(self, a: int, b: int):
        from ..harness.serialize import diff
        return diff(self.get(a), self.get(b))

    def snapshot(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)
        return path
