# -*- coding: utf-8 -*-
"""Small pure-python optimizers (SGD / AdamW) for the real-weights path."""
from __future__ import annotations

import math


class SGD:
    def __init__(self, params: dict, lr: float = 0.05):
        self.params = params
        self.lr = lr

    def step(self, grads: dict):
        for k, g in grads.items():
            p = self.params[k]
            if isinstance(p, list):
                self.params[k] = [p[i] - self.lr * g[i] for i in range(len(p))]
            else:
                self.params[k] = p - self.lr * g


class AdamW:
    def __init__(self, params: dict, lr: float = 0.01, betas=(0.9, 0.999),
                 eps: float = 1e-8, weight_decay: float = 0.0):
        self.params = params
        self.lr = lr
        self.b1, self.b2 = betas
        self.eps = eps
        self.wd = weight_decay

        def _zeros(v):
            return [0.0] * len(v) if isinstance(v, list) else 0.0

        self.m = {k: _zeros(v) for k, v in params.items()}
        self.v = {k: _zeros(v) for k, v in params.items()}
        self.t = 0

    def step(self, grads: dict):
        self.t += 1
        for k, g in grads.items():
            p = self.params[k]
            if isinstance(p, list):
                new_p = []
                for i in range(len(p)):
                    self.m[k][i] = self.b1 * self.m[k][i] + (1 - self.b1) * g[i]
                    self.v[k][i] = self.b2 * self.v[k][i] + (1 - self.b2) * g[i] * g[i]
                    m_hat = self.m[k][i] / (1 - self.b1 ** self.t)
                    v_hat = self.v[k][i] / (1 - self.b2 ** self.t)
                    new_p.append(p[i] - self.lr * (m_hat / (math.sqrt(v_hat) + self.eps) + self.wd * p[i]))
                self.params[k] = new_p
            else:
                self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
                self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g * g
                m_hat = self.m[k] / (1 - self.b1 ** self.t)
                v_hat = self.v[k] / (1 - self.b2 ** self.t)
                self.params[k] -= self.lr * (m_hat / (math.sqrt(v_hat) + self.eps) + self.wd * p)
