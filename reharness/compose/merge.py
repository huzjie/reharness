# -*- coding: utf-8 -*-
"""Merge selected component ids into a fresh harness."""
from __future__ import annotations

from ..harness.builder import build_harness


def merge_harness(selected: list, system_prompt: str = ""):
    return build_harness(system_prompt=system_prompt, cids=selected)
