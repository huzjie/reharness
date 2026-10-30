# -*- coding: utf-8 -*-
"""Serialize / deserialize a harness to and from a YAML-ish dict (zero deps)."""
from __future__ import annotations

from .model import Harness, Component


def to_dict(h: Harness) -> dict:
    return h.to_dict()


def from_dict(d: dict) -> Harness:
    h = Harness(system_prompt=d.get("system_prompt", ""))
    for c in d.get("components", []):
        h.add(Component(cid=c["cid"], kind=c["kind"], body=c["body"], enabled=c.get("enabled", True)))
    return h


def diff(a: Harness, b: Harness) -> dict:
    """Return {added: [...], removed: [...], kept: [...]} between a and b."""
    sa, sb = set(a.component_ids()), set(b.component_ids())
    return {"added": sorted(sb - sa), "removed": sorted(sa - sb), "kept": sorted(sa & sb)}
