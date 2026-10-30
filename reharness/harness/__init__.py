# -*- coding: utf-8 -*-
"""The harness: a structured, versionable description of everything that wraps
the model (system prompt, guardrails, memory, skills, tool guidance, scripts,
subagents, middleware)."""
from .model import Harness, Component
from .builder import build_harness, empty_harness

__all__ = ["Harness", "Component", "build_harness", "empty_harness"]
