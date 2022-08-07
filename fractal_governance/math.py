# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Math functions for fractal governance data analysis"""
import numpy as np
import pandas as pd
import uncertainties
import uncertainties.umath
import uncertainties.unumpy

GOLDEN_RATIO = (np.sqrt(5) + 1) / 2


def fibonacci(
    n: float, golden_ratio: float = GOLDEN_RATIO, include_second_term: bool = True
) -> float:
    """Return the Fibonacci number for the given argument.

    We use the general formula for the Fibonacci series derived from "Binet's Formula".

    If the argument include_second_term is True (the default) then return the Fibonacci
    number using this formula. If include_second_term is False then exclude the second
    term of this formula."""
    value = np.power(golden_ratio, n)
    if include_second_term:
        _cos = (
            uncertainties.unumpy.cos
            if isinstance(n, pd.Series)
            else uncertainties.umath.cos
        )
        value -= _cos(n * np.pi) * np.power(golden_ratio, -n)
    return value / np.sqrt(5)  # type: ignore


def respect(level: float, bias: float = 2, **kwargs) -> float:  # type: ignore
    """Return the units of Respect for the given level"""
    return fibonacci(level + bias, **kwargs)
