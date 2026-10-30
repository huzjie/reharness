# -*- coding: utf-8 -*-
"""Mutation operators over harnesses. All deterministic given a seed key."""
from __future__ import annotations

from ..utils.rng import stable_shuffle, stable_int, stable_choice
from ..world.universe import UNIVERSE, component_ids
from ..harness.model import Harness, Component
from ..harness.builder import universe_component


def random_subset(key: str, size: int, pool: list | None = None) -> tuple:
    """A deterministic random subset of the component universe of the given size."""
    pool = pool if pool is not None else component_ids()
    return tuple(stable_shuffle(key, pool)[:size])


def add_component(h: Harness, cid: str) -> Harness:
    out = h.clone()
    if not out.has(cid):
        out.add(universe_component(cid))
    else:
        out.set_enabled(cid, True)
    return out


def remove_component(h: Harness, cid: str) -> Harness:
    out = h.clone()
    out.remove(cid)
    return out


def toggle_component(h: Harness, cid: str) -> Harness:
    out = h.clone()
    for c in out.components:
        if c.cid == cid:
            c.enabled = not c.enabled
            return out
    out.add(universe_component(cid))
    return out


def mutate(h: Harness, key: str) -> Harness:
    """Apply one random mutation (add / remove / toggle) chosen deterministically."""
    op = stable_int("op:" + key, 0, 2)
    cid = stable_choice("cid:" + key, component_ids())
    if op == 0:
        return add_component(h, cid)
    if op == 1:
        return remove_component(h, cid)
    return toggle_component(h, cid)
