# -*- coding: utf-8 -*-
"""A few ready-to-use harness presets (illustrative compositions)."""
from __future__ import annotations

from ..harness.builder import build_harness


def coding_agent():
    return build_harness(
        system_prompt="You are a careful coding agent. Read before edit, test after edit.",
        cids=["prompt.think_stepwise", "prompt.plan_first", "skill.code",
              "skill.file", "tool.file_write", "tool.db_query", "guardrail.sandbox"],
    )


def research_agent():
    return build_harness(
        system_prompt="You are a research agent. Cite sources and be honest about uncertainty.",
        cids=["prompt.plan_first", "skill.search", "tool.search",
              "subagent.researcher", "guardrail.cite_sources", "guardrail.refuse_harmful"],
    )


def support_agent():
    return build_harness(
        system_prompt="You are a support agent. Be concise and never fabricate policy.",
        cids=["prompt.be_concise", "skill.search", "skill.email",
              "guardrail.refuse_pii", "guardrail.refuse_harmful"],
    )
