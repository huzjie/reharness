# -*- coding: utf-8 -*-
"""Response payload shapes."""
from __future__ import annotations


def info():
    return {"name": "reharness", "version": "0.1.0",
            "endpoints": ["/health", "/v1/info", "/v1/optimize", "/v1/recursive"]}


def ok(**kw):
    out = {"status": "ok", "name": "reharness"}
    out.update(kw)
    return out
