# -*- coding: utf-8 -*-
"""Build harnesses from recipes / the component universe."""
from __future__ import annotations

from ..world.universe import UNIVERSE
from .model import Harness, Component


def _default_body(kind: str, cid: str) -> str:
    return {
        "prompt": "Directive: %s" % cid,
        "guardrail": "Never violate: %s" % cid,
        "memory": "Memory policy: %s" % cid,
        "skill": "When asked to %s, follow the skill instructions." % cid.split(".")[-1],
        "tool": "Use %s correctly and pass validated arguments." % cid,
        "script": "Run helper script %s when needed." % cid,
        "subagent": "Delegate to %s for its domain." % cid,
        "middleware": "Apply middleware %s to every step." % cid,
    }.get(kind, cid)


def empty_harness(system_prompt: str = "") -> Harness:
    return Harness(system_prompt=system_prompt, components=[])


def build_harness(system_prompt: str = "", cids: list | None = None) -> Harness:
    """Build a harness containing exactly the given component ids."""
    h = empty_harness(system_prompt)
    for kind, cid in UNIVERSE:
        if cids is None or cid in cids:
            h.add(Component(cid=cid, kind=kind, body=_default_body(kind, cid)))
    return h


def universe_component(cid: str) -> Component:
    for kind, c in UNIVERSE:
        if c == cid:
            return Component(cid=cid, kind=kind, body=_default_body(kind, cid))
    raise KeyError("unknown component id: %s" % cid)
