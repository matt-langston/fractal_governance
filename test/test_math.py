# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.math module"""

# builtins
import unittest

# 2nd party dependencies
import fractal_governance.math


class TestMath(unittest.TestCase):
    """Test fixture for the fractal_governance.math module"""

    def test_fibonacci(self):  # pylint: disable=C0116
        self.assertEqual(fractal_governance.math.fibonacci(1), 1)


if __name__ == '__main__':
    unittest.main()
