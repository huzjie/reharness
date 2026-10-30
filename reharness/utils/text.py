# -*- coding: utf-8 -*-
"""Text utilities: tokenization, edit distance, token Jaccard similarity."""
from __future__ import annotations

import re

_WORD = re.compile(r"[a-zA-Z0-9]+")


def tokenize_words(text: str) -> list:
    return _WORD.findall(text.lower())


def edit_distance(a: str, b: str) -> int:
    """Classic Levenshtein edit distance between two strings."""
    if a == b:
        return 0
    n, m = len(a), len(b)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[m]


def jaccard(a: str, b: str) -> float:
    """Token-level Jaccard similarity in [0, 1]."""
    sa, sb = set(tokenize_words(a)), set(tokenize_words(b))
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)
