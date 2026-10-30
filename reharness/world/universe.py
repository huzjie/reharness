# -*- coding: utf-8 -*-
"""The finite universe of harness components the optimizer can pick from.

Each component is identified by a ``kind`` and an ``id``. Kinds mirror the
Harness2 anatomy: system-prompt directives, guardrails, memory, skills, tool
guidance, scripts, subagents, middleware. The optimizer mutates a harness by
adding/removing these components; the oracle decides which are *required* and
which are *forbidden* for each task.
"""
from __future__ import annotations

KIND = {
    "prompt": "system-prompt directive",
    "guardrail": "guardrail rule",
    "memory": "memory policy",
    "skill": "skill",
    "tool": "tool guidance",
    "script": "helper script",
    "subagent": "subagent",
    "middleware": "middleware",
}

# (kind, id) universe. Deterministic, stable ordering is intentional.
# 24 components: rich enough to be realistic, small enough that the contrastive
# success-lift of the REQUIRED set stays clearly above the noise floor of the
# neutral distractor components.
UNIVERSE = [
    ("skill", "skill.calculator"),
    ("skill", "skill.search"),
    ("skill", "skill.file"),
    ("skill", "skill.email"),
    ("skill", "skill.code"),
    ("skill", "skill.db"),
    ("guardrail", "guardrail.refuse_pii"),
    ("guardrail", "guardrail.refuse_harmful"),
    ("guardrail", "guardrail.no_overwrite"),
    ("guardrail", "guardrail.rate_limit"),
    ("guardrail", "guardrail.sandbox"),
    ("guardrail", "guardrail.cite_sources"),
    ("tool", "tool.calculator"),
    ("tool", "tool.search"),
    ("tool", "tool.file_write"),
    ("tool", "tool.db_query"),
    ("prompt", "prompt.think_stepwise"),
    ("prompt", "prompt.plan_first"),
    ("prompt", "prompt.be_concise"),
    ("memory", "memory.window"),
    ("memory", "memory.summarize"),
    ("memory", "memory.retrieval"),
    ("subagent", "subagent.researcher"),
    ("subagent", "subagent.coder"),
]


def component_ids():
    return [cid for _k, cid in UNIVERSE]


def kind_of(cid: str) -> str:
    for k, c in UNIVERSE:
        if c == cid:
            return k
    return "unknown"
