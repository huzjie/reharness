# -*- coding: utf-8 -*-
"""Runtime configuration with layered defaults (code default < recipe yaml < cli)."""
from __future__ import annotations

import copy

from .utils.yamlish import yaml_loads

# Defaults are deliberately small so a reference run stays interactive
# (<10s on a laptop), while remaining large enough to exercise every code path.
DEFAULTS = {
    "harness": {
        "max_guardrails": 8,
        "max_skills": 8,
        "max_tool_rules": 6,
        "memory_window": 8,
        "system_prompt": "You are a careful agent. Follow every guardrail and use the right skill for each task.",
    },
    "propose": {
        "candidates": 24,       # candidate harnesses per round
        "probe_size": 6,        # components per candidate (random subset size)
        "mutations": 2,         # mutations per candidate
        "temperature": 1.0,
    },
    "probe": {
        "n_tasks": 32,          # tasks per probe batch
        "max_turns": 6,        # max agent turns per task
    },
    "compose": {
        "top_k": 6,            # top components kept after contrastive scoring
        "eps": 1e-6,
    },
    "optimizer": {
        "rounds": 10,          # evidence-aggregation rounds (candidates * rounds probes)
        "recursive": True,     # apply PPC to the optimizer itself
        "seed": 20261030,
    },
    "training": {
        "lr": 0.25,
        "epochs": 12,
        "target_skill": 0.95,
    },
    "serving": {"host": "127.0.0.1", "port": 8790},
}


def deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(recipe: str | None = None) -> dict:
    cfg = copy.deepcopy(DEFAULTS)
    if recipe:
        try:
            with open(recipe, "r", encoding="utf-8") as f:
                user = yaml_loads(f.read())
            cfg = deep_merge(cfg, user)
        except FileNotFoundError:
            raise SystemExit("[config] recipe not found: %s" % recipe)
    return cfg
