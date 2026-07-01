"""Shared analysis metrics utilities."""

from __future__ import annotations

import math


def entropy(values: list[float]) -> float:
    return -sum(value * math.log(value + 1e-9) for value in values)


def mean_abs_deviation(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return sum(abs(value - mean) for value in values) / len(values)
