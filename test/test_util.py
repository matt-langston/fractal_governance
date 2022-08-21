# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.util module"""

import unittest

import fractal_governance.util
import pandas as pd


class TestUtil(unittest.TestCase):
    """Test fixture for the fractal_governance.util module"""

    def test_read_csv(self) -> None:
        df = fractal_governance.util.read_csv()
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    def test_meeting_id_to_timestamp(self) -> None:
        self.assertEqual(
            pd.Timestamp("2022-02-26"),
            fractal_governance.util.meeting_id_to_timestamp(1),
        )
        with self.assertRaises(ValueError):
            fractal_governance.util.meeting_id_to_timestamp(0)


if __name__ == "__main__":
    unittest.main()
