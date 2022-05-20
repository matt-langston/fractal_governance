# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Math functions for fractal governance data analysis"""


def fibonacci(n: int) -> int:  # pylint: disable=C0103
    """Return the nth Fibonacci number"""
    if n in (1, 2):
        return 1
    if n < 0:
        if (n + 1) % 2:
            return -fibonacci(-n)
        return fibonacci(-n)
    return fibonacci(n - 1) + fibonacci(n - 2)


def respect(rank: int) -> int:
    """Return the units of Respect for the given rank"""
    if rank < 1:
        raise ValueError(f"rank={rank} must be >= 1")
    return fibonacci(rank + 2)
