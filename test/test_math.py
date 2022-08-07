# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.math module"""

import unittest

import fractal_governance.math


class TestMath(unittest.TestCase):
    """Test fixture for the fractal_governance.math module"""

    def test_fibonacci(self) -> None:
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-10), -55)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-9), 34)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-8), -21)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-7), 13)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-6), -8)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-5), 5)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-4), -3)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-3), 2)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-2), -1)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(-1), 1)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(0), 0)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(1), 1)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(2), 1)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(3), 2)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(4), 3)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(5), 5)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(6), 8)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(7), 13)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(8), 21)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(9), 34)
        self.assertAlmostEqual(fractal_governance.math.fibonacci(10), 55)


if __name__ == "__main__":
    unittest.main()
