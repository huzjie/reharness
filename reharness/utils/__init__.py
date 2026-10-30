# -*- coding: utf-8 -*-
"""Small utility helpers: deterministic RNG, minimal YAML, text, linear algebra."""
from .rng import stable_float, stable_int, stable_vector, stable_choice, stable_matrix, stable_shuffle
from .text import edit_distance, tokenize_words, jaccard
from .linalg import matvec, matmul, softmax, relu, argmax, sigmoid, log_softmax

__all__ = [
    "stable_float", "stable_int", "stable_vector", "stable_choice", "stable_matrix", "stable_shuffle",
    "edit_distance", "tokenize_words", "jaccard",
    "matvec", "matmul", "softmax", "relu", "argmax", "sigmoid", "log_softmax",
]
