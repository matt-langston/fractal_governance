# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.util module"""

# builtins
import unittest

# 3rd party
import pandas as pd

# 2nd party dependencies
import fractal_governance.util


class TestUtil(unittest.TestCase):
    """Test fixture for the fractal_governance.util module"""

    def test_read_csv(self):  # pylint: disable=C0116
        df = fractal_governance.util.read_csv(  # pylint: disable=C0103
            'data/genesis-weekly_measurements.csv')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    def test_meeting_id_to_timestamp(self):  # pylint: disable=C0116
        self.assertEqual(pd.Timestamp('2022-02-26'),
                         fractal_governance.util.meeting_id_to_timestamp(1))
        with self.assertRaises(ValueError):
            fractal_governance.util.meeting_id_to_timestamp(0)


if __name__ == '__main__':
    unittest.main()
