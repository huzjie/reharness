# -*- coding: utf-8 -*-
"""Compute backend interface (swap pure-python for numpy/torch w/o touching logic)."""
from __future__ import annotations


class Backend:
    def matvec(self, W, x):
        raise NotImplementedError

    def matmul(self, A, B):
        raise NotImplementedError

    def softmax(self, logits):
        raise NotImplementedError

    def argmax(self, vals):
        raise NotImplementedError
