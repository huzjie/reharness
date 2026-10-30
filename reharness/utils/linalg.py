# -*- coding: utf-8 -*-
"""Pure-python linear algebra helpers (zero dependencies).

Conventions (kept identical across the codebase to avoid off-by-one bugs):

- a matrix M is a list of rows: M[row][col]
- ``matvec(W, x)`` computes W @ x: out[i] = sum_j W[i][j] * x[j]
- a "W^T x" projection into an out-dim is always written with i over the
  *output* dimension and j over the *input* dimension.
"""
from __future__ import annotations

import math


def matvec(W: list, x: list) -> list:
    n_out = len(W)
    n_in = len(x)
    return [sum(W[i][j] * x[j] for j in range(n_in)) for i in range(n_out)]


def matmul(A: list, B: list) -> list:
    """A (m x k) times B (k x n) -> (m x n)."""
    m, k = len(A), len(B)
    n = len(B[0]) if k else 0
    return [[sum(A[i][p] * B[p][j] for p in range(k)) for j in range(n)] for i in range(m)]


def softmax(logits: list, temperature: float = 1.0) -> list:
    # NOTE: temperature *division* (logits / T), not uniform scaling.
    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    z = [v / temperature for v in logits]
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def log_softmax(logits: list) -> list:
    m = max(logits)
    e = [v - m for v in logits]
    s = sum(math.exp(v) for v in e)
    ln_s = math.log(s)
    return [v - ln_s for v in e]


def relu(x):
    if isinstance(x, list):
        return [max(0.0, v) for v in x]
    return max(0.0, x)


def sigmoid(x):
    if isinstance(x, list):
        return [1.0 / (1.0 + math.exp(-v)) for v in x]
    return 1.0 / (1.0 + math.exp(-x))


def argmax(vals: list) -> int:
    best_i, best_v = 0, vals[0]
    for i, v in enumerate(vals):
        if v > best_v:
            best_i, best_v = i, v
    return best_i
