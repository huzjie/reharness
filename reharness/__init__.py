# -*- coding: utf-8 -*-
"""reharness: a recursive agent harness optimization framework.

Most ways to make an LLM agent better change the *model* (fine-tune, more
compute). reharness changes the *harness* instead: the system prompt, guardrails,
memory, skills, tool guidance, scripts, subagents and middleware that wrap the
model. The key idea -- introduced by Google's Harness2 work -- is that a
carefully optimized harness can matter more than the choice of base model.

reharness implements the full loop as a self-contained, zero-dependency
reference:

- Propose  -- mutate the current harness into candidate variants
- Probe    -- run the agent under each candidate, collect execution traces
- Compose  -- contrastively score components (success-lift) and rebuild a
              better harness, using *evidence from the agent's own runs*,
              not ground-truth labels
- Recurse   -- treat the optimizer's own config as a harness and optimize it too

Everything runs on the Python standard library (no numpy / torch / requests).
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
